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
            e: The exception recieved during the simulation

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

        speed = 0
        try:
            speeds = []
            pos = []
            xte = []
            steerings = []
            throttles = []

            angles = simulator_config.angles

            # Generate a road
            road : Road = test_generator.generate(
                starting_pos=simulator_config.initial_position,
                angles=angles,
                simulator_name=config.UDACITY_SIM_NAME)
            
            # Convert it to the string reppresentation
            waypoints : str = road.get_string_repr()

            # set up of params
            done = False

            # Reset the enviroment, this also sets the road configuration
            obs = self.env.reset(skip_generation=False, track_string=waypoints)

            start = timer()

            fps_time_start = time.time()
            counter = 0
            counter_all = []

            while not done:
                # calculate fps
                if time.time() - fps_time_start > 1:
                    # reset
                    log.info(f"Frames in 1s: {counter}")
                    log.info(
                        f"Time passed: {time.time() - fps_time_start}")

                    counter_all.append(counter)
                    counter = 0
                    fps_time_start = time.time()
                else:
                    counter += 1
                # time.sleep(0.15)
                actions = self.agent.predict(obs=obs,
                                        state=dict(speed=speed,
                                                    simulator_name=config.UDACITY_SIM_NAME)
                                        )
                # # clip action to avoid out of bound errors
                if isinstance(self.env.action_space, gym.spaces.Box):
                    actions = np.clip(
                        actions,
                        self.env.action_space.low,
                        self.env.action_space.high
                    )
                # obs is the image, info contains the road and the position of the car
                obs, done, info = self.env.step(actions)

                speed = 0.0 if info.get(
                    "speed", None) is None else info.get("speed")

                speeds.append(info["speed"])
                pos.append(info["pos"])

                if config.CAP_XTE:
                    xte.append(info["cte"]
                                if abs(info["cte"]) <= config.MAX_XTE
                                else config.MAX_XTE)

                    assert np.all(abs(np.asarray(
                        xte)) <= config.MAX_XTE), f"At least one element is not smaller than {config.MAX_XTE}"
                else:
                    xte.append(info["cte"])
                steerings.append(actions[0][0])
                throttles.append(actions[0][1])

                end = timer()
                time_elapsed = int(end - start)
                if time_elapsed % 2 == 0:
                    pass  # print(f"time_elapsed: {time_elapsed}")
                elif time_elapsed > simulator_config.maxTime:
                    # print(f"Over time limit, terminating.")
                    done = True
                elif abs(info["cte"]) > simulator_config.maxXTE:
                    # print("Is above MAXIMAL_XTE. Terminating.")
                    done = True
                else:
                    pass

            fps_rate = np.sum(counter_all)/time_elapsed
            log.info(f"FPS rate: {fps_rate}")

            # morph values into SimulationOutput Object
            result = SimulationOutput(
                simTime=time_elapsed,
                times=[x for x in range(len(speeds))],
                location={
                    "ego": [(x[0], x[1]) for x in pos],  # cut out z value
                },
                velocity={
                    "ego": UdacitySimulator._calculate_velocities(pos, speeds),
                },
                speed={
                    "ego": speeds,
                },
                acceleration={"ego": UdacitySimulator.calc_acceleration(
                    speeds=speeds, fps=20)},
                yaw={
                    "ego": calc_yaw_ego(pos)
                },
                collisions=[],
                actors={
                    "ego": "ego",
                    "pedestrians": [],
                    "vehicles": ["ego"]
                },
                otherParams={"xte": xte,
                                "simulator": "Udacity",
                                "road": road.get_concrete_representation(to_plot=True),
                                "steerings": steerings,
                                "throttles": throttles,
                                "fps_rate": fps_rate}
            )

        except Exception as e:
            # print(f"Received exception during simulation {e}")

            raise e

        return result
    
    def killSimulation(self):
        """
        This method closes the simulator
        """
        self.env.close()
        kill_udacity_simulator()

    @staticmethod
    def _calculate_velocities(positions, speeds) -> Tuple[float, float, float]:
        """
        Calculate velocities given a list of positions and corresponding speeds.
        """
        velocities = []
        for i in range(len(positions) - 1):
            displacement = np.array(positions[i + 1]) - np.array(positions[i])
            direction = displacement / np.linalg.norm(displacement)
            velocity = direction * speeds[i]
            velocities.append(velocity)

        return velocities

    @staticmethod
    def calc_acceleration(speeds: List, fps: int):
        acc = [0]
        for i in range(1, len(speeds)):
            a = (speeds[i] - speeds[i-1])*fps / 3.6  # convert to m/s
            acc.append(a)
        return acc
