# imports related to OpenSBT
try:
    import time
    import pymoo
    from lanekeeping.agent.agent_utils import calc_yaw_ego
    from opensbt.simulation.simulator import Simulator, SimulationOutput

    from opensbt.model_ga.individual import IndividualSimulated
    from lanekeeping.udacity.os_utils import kill_udacity_simulator

    pymoo.core.individual.Individual = IndividualSimulated

    from opensbt.model_ga.population import PopulationExtended
    pymoo.core.population.Population = PopulationExtended

    from opensbt.model_ga.result import SimulationResult
    pymoo.core.result.Result = SimulationResult

    from opensbt.model_ga.problem import SimulationProblem
    pymoo.core.problem.Problem = SimulationProblem
except ImportError as e:
    print(f"OpenSBT imports failed: {e}")
    raise ImportError(
        "OpenSBT is not installed or not properly configured. Please install OpenSBT to use this module.")

# all other imports
try:
    from distutils import config
    from typing import List, Tuple
    import numpy as np
    import os
    import gym
    import cv2
    from numpy import uint8
    from tensorflow.keras.models import load_model
    import requests
except ImportError as e:
    print(f"Import failed: {e}")
    raise ImportError(
        "Some required packages are not installed. Please install the necessary packages to use this module.")

# related to this simulator
from lanekeeping.road_generator.road_generator import RoadGenerator
from lanekeeping.udacity.env.udacity_gym_env import (
    UdacityGymEnv_RoadGen
)

from lanekeeping.road_generator.custom_road_generator import CustomRoadGenerator

import lanekeeping.config as config

from lanekeeping.self_driving.supervised_agent import SupervisedAgent
from timeit import default_timer as timer
import logging as log
from .UdacitySimulatorConfig import UdacitySimulatorConfig


class UdacitySimulator(Simulator):
    @staticmethod
    def simulate(
        simulator_config: UdacitySimulatorConfig,
    ) -> List[SimulationOutput]:
        """
        Runs all individual simulations and returns simulation outputs
        """
        # TODO: maybe e possibility to run multiple configs in this loop
        list_individuals = [simulator_config.angles]

        results = []
        test_generator = CustomRoadGenerator(map_size=simulator_config.map_size,
                                             num_control_nodes=len(
                                                 list_individuals[0]),
                                             seg_length=simulator_config.segLength)
        env = None
        # obs, done, info = env.observe()
        agent = SupervisedAgent(
            env_name=config.UDACITY_SIM_NAME,
            model_path=config.DNN_MODEL_PATH,
            min_speed=simulator_config.minSpeed,
            max_speed=simulator_config.maxSpeed,
            input_shape=config.INPUT_SHAPE,
            predict_throttle=False,
            fake_images=False
        )
        # print("[UdacitySimulator] loaded model")

        for ind in list_individuals:
            speed = 0
            try:
                speeds = []
                pos = []
                xte = []
                steerings = []
                throttles = []

                angles = UdacitySimulator._process_simulation_vars(ind)
                road = test_generator.generate(
                    starting_pos=simulator_config.initial_position,
                    angles=angles,
                    simulator_name=config.UDACITY_SIM_NAME)
                # road = test_generator.generate()
                waypoints = road.get_string_repr()

                # set up of params
                done = False

                if env is None:
                    env = UdacityGymEnv_RoadGen(
                        seed=1,
                        test_generator=test_generator,
                        exe_path=config.UDACITY_EXE_PATH)

                obs = env.reset(skip_generation=False, track_string=waypoints)

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
                    actions = agent.predict(obs=obs,
                                            state=dict(speed=speed,
                                                       simulator_name=config.UDACITY_SIM_NAME)
                                            )
                    # # clip action to avoid out of bound errors
                    if isinstance(env.action_space, gym.spaces.Box):
                        actions = np.clip(
                            actions,
                            env.action_space.low,
                            env.action_space.high
                        )
                    # obs is the image, info contains the road and the position of the car
                    obs, done, info = env.step(actions)

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

                results.append(result)
            except Exception as e:
                # print(f"Received exception during simulation {e}")

                raise e
            finally:
                if env is not None:
                    env.close()
                    env = None
                kill_udacity_simulator()
                # print("Finished individual")
        # # close the environment
        # env.close()
        return results

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
    def _process_simulation_vars(
        instance_values: List[float]
    ) -> Tuple[List[int]]:
        angles = [int(round(x)) for x in instance_values]
        return angles

    @staticmethod
    def calc_acceleration(speeds: List, fps: int):
        acc = [0]
        for i in range(1, len(speeds)):
            a = (speeds[i] - speeds[i-1])*fps / 3.6  # convert to m/s
            acc.append(a)
        return acc
