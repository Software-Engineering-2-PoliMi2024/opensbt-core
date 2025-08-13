# imports related to OpenSBT
try:
    import time
    from lanekeeping.agent.agent_utils import calc_yaw_ego
    from opensbt.simulation.simulator import Simulator, SimulationOutput
    from lanekeeping.udacity.os_utils import kill_udacity_simulator

except ImportError as e:
    print(f"OpenSBT imports failed: {e}")
    raise ImportError(
        "OpenSBT is not installed or not properly configured. Please install OpenSBT to use this module.")

# all other imports
try:
    from distutils import config
    from typing import List, Tuple
    import numpy as np
    import gym
except ImportError as e:
    print(f"Import failed: {e}")
    raise ImportError(
        "Some required packages are not installed. Please install the necessary packages to use this module.")

# related to this simulator
from lanekeeping.udacity.env.udacity_gym_env import UdacityGymEnv_RoadGen
from lanekeeping.road_generator.custom_road_generator import CustomRoadGenerator
from lanekeeping.self_driving.road import Road
import lanekeeping.config as config

from lanekeeping.self_driving.supervised_agent import SupervisedAgent
from timeit import default_timer as timer
import logging as log
from .UdacitySimulatorConfig import UdacitySimulatorConfig as simConfig
from queue import Queue
from typing import Callable
class UdacitySimulator():
    def __init__(self) -> None:
        # Initialize the agent
        self.agent : SupervisedAgent = SupervisedAgent(
            env_name=config.UDACITY_SIM_NAME,
            model_path=config.DNN_MODEL_PATH,
            min_speed=0,
            max_speed=1,
            input_shape=config.INPUT_SHAPE,
            predict_throttle=False,
            fake_images=False
        )

        #Initialize the environment
        self.env : UdacityGymEnv_RoadGen = UdacityGymEnv_RoadGen(
                        seed=1,
                        exe_path=config.UDACITY_EXE_PATH
                        )



    def simulate(self, simulator_config: simConfig) -> SimulationOutput:
        """Runs a simulation with the given simulator configurations

        Args:
            simulator_config (simConfig): The input simulator configuration

        Raises:
            e: The exception received during the simulation

        Returns:
            SimulationOutput: The output of the simulation
        """
        # Set up the given speed limits for the agent
        self.agent.setSpeedLimits(
            minSpeed=simulator_config.minSpeed,
            maxSpeed=simulator_config.maxSpeed
            )
        
        # Initialize the road generator
        test_generator : CustomRoadGenerator = CustomRoadGenerator(map_size=simulator_config.map_size,
                                             num_control_nodes=len(simulator_config.angles),
                                             seg_length=simulator_config.segLength)

        try:
            #Instantiate the output accumulator
            simulationOutput = SimulationOutput()

            angles = simulator_config.angles

            # Generate a road
            road : Road = test_generator.generate(
                starting_pos=simulator_config.initial_position,
                angles=angles,
                simulator_name=config.UDACITY_SIM_NAME)

            #Add the road configuration to the output
            simulationOutput.road = road.get_concrete_representation(to_plot=True)
            
            # Convert it to the string reppresentation
            waypoints : str = road.get_string_repr()

            # Reset the enviroment, this also sets the road configuration
            obs = self.env.reset(skip_generation=False, track_string=waypoints)

            # This variable will contains the current speed, it is needed by the agent to compute the next action
            speed:float = 0

            # This is the content of the main simulation loop
            def loopingFunction():
                #Variables coming from outside this function
                nonlocal obs, speed, simulationOutput

                # Infer next actions
                actions = self.agent.predict(obs=obs,
                                        state=dict(
                                            speed=speed,
                                            simulator_name=config.UDACITY_SIM_NAME
                                            )
                                        )
                
                # Clip action to avoid out of bound errors
                if isinstance(self.env.action_space, gym.spaces.Box):
                    actions = np.clip(
                        actions,
                        self.env.action_space.low,
                        self.env.action_space.high
                    )

                # Perform the actions and get the new obs is the image, info contains the road and the position of the car
                obs, done, info = self.env.step(actions)

                # Update the current speed
                speed_candidate = info.get("speed", None)
                speed = 0.0 if speed_candidate is None else speed_candidate

                # Compute and cap (if necessary) the xte
                xte = info['cte']
                xte_sign = 1 if xte == 0 else xte / abs(xte)
                xte = abs(xte)
                if xte > config.MAX_XTE and config.CAP_XTE:
                    xte = config.MAX_XTE
                xte *= xte_sign

                # Add the stats of this iteration to the output
                simulationOutput.addStats(
                    position = info['pos'],
                    speed=speed,
                    xte=xte,
                    steering=actions[0][0],
                    throttle=actions[0][1]
                )

                #Check loop end conditions
                self.checkEndConditions(
                    simulatorConfig=simulator_config,
                    xte = info["cte"],
                    envDone=done
                    )

            # Execute the main loop
            elapsedTime, iterations = self.timedConditionalLoop(
                loopingFunction=loopingFunction
            )

            #Add the timing stats to the output
            simulationOutput.elapsedTime = elapsedTime
            simulationOutput.iterations = iterations

        except Exception as e:
            raise e

        return simulationOutput
    
    def killSimulation(self):
        """
        This method permanently closes the simulator
        """
        self.env.close()
        kill_udacity_simulator()

    def endSimulation(self):
        """
        This method stops the simulation loop.
        When this is called the current loop iteration becomes the last one.
        After that the simulation outputs are computed and returned
        """
        self.done = True

    def timedConditionalLoop(self, loopingFunction : Callable) -> Tuple[float, int]:
        """A method to run and time a conditional loop. The loop keeps calling the loopingFunction
        until the self.endSimulation method is called.

        Args:
            loopingFunction (Callable): the function to be called inside the loop

        Returns:
            Tuple[float, int]: Returns the elapsed time in seconds and the number of executed iterations
        """
        self.done = False
        self.loopStartTime = time.time()
        iterations = 0

        while not self.done:
            loopingFunction()
            iterations += 1
        
        elapsedTime = self.getElapsedTime()
        return elapsedTime, iterations

    def getElapsedTime(self) -> float:
        """Computes  and returns the elapsed time in seconds since the beginning of the main loop

        Returns:
            float: the elapsed time in seconds since the beginning of the main loop
        """

        return time.time() - self.loopStartTime


    def checkEndConditions(self, simulatorConfig: simConfig, xte: float, envDone:bool) -> None:
        """This method checks if the end conditions for the simulation are met.
        If that's the case it stops the simulation using self.endSimulation()

        Args:
            simulatorConfig (simConfig): The current config of the simulation
            xte (float): The current xte
            envDone(bool): The done signal coming for the gym env
        """
        # Exceeded maximum time
        simShouldEnd = self.getElapsedTime() > simulatorConfig.maxTime

        # Exceeded maximum error
        simShouldEnd = simShouldEnd or abs(xte) > simulatorConfig.maxXTE

        #Env Done
        simShouldEnd = simShouldEnd or envDone

        if simShouldEnd:
            self.endSimulation()
