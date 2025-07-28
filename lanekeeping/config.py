import os

# DNN Model
DNN_MODEL_PATH = r"./SelfDrivingModels/mixed-chauffeur.h5"


# Simulators
UDACITY_EXE_PATH = "./Simulator/ubuntu_binaries/ubuntu.x86_64"

################

IN_WIDTH = 320
IN_HEIGHT = 160

DEFAULT_THROTTLE = 0.1  # Not used

MAX_XTE = 3  # used

ROAD_WIDTH = 8.0  # Used but useless as far as I have tested
# NUM_CONTROL_NODES = 5   #Not used
NUM_SAMPLED_POINTS = 100  # Number of points used to build the road
MAX_ANGLE = 270  # Not used
MIN_ANGLE = 20  # Not used

MAX_EPISODE_STEPS = 2000

IMAGE_CHANNELS = 3
INPUT_SHAPE = (IN_HEIGHT, IN_WIDTH, IMAGE_CHANNELS)
INPUT_DIM = INPUT_SHAPE
DISPLACEMENT = 2

MAX_SPEED = 30  # Maximum speed for the car
MIN_SPEED = 10  # Minimum speed for the car

MAP_SIZE = 250  # Size of the map in meters

# The portion of the image to crop in the Udacity simulator, it will keep the vertical strip of the image whose x coordinate is between [0] and [1]
CROP_UDACITY = [60, -25]
CROP_DONKEY = [60, 0]

# Wait time for the Udacity simulator to load
UDACITY_SLEEP = 2

STEERING_CORRECTION = 1
TIME_LIMIT = 30
CAP_XTE = True

# USI

BEAMNG_SIM_NAME = "beamng"
DONKEY_SIM_NAME = "donkey"
UDACITY_SIM_NAME = "udacity"
MOCK_SIM_NAME = "mock"
SIMULATOR_NAMES = [BEAMNG_SIM_NAME, DONKEY_SIM_NAME,
                   UDACITY_SIM_NAME, MOCK_SIM_NAME]
AGENT_TYPE_RANDOM = "random"
AGENT_TYPE_SUPERVISED = "supervised"
AGENT_TYPE_AUTOPILOT = "autopilot"
AGENT_TYPES = [AGENT_TYPE_RANDOM, AGENT_TYPE_SUPERVISED, AGENT_TYPE_AUTOPILOT]
TEST_GENERATORS = ["random", "sin"]

IMAGE_HEIGHT = IN_HEIGHT
IMAGE_WIDTH = IN_WIDTH

WAIT_RESETCAR = 3
MAX_CTE_ERROR = MAX_XTE

# BEAMNG_USER = r"C:\\Users\\Lev\\Documents\\BeamNG_User\\"
BEAMNG_USER = r"C:\\Users\\sorokin\\Documents\\BeamNG_User\\"
# BEAMNG_HOME = r"C:\BeamNG\BeamNG.drive-0.23.5.1.12888\\"
BEAMNG_HOME = r"C:\BeamNG.tech.v0.23.5.1\BeamNG.drive-0.23.5.1.12888\\"

SEG_LENGTH = 25
CRITICAL_XTE = 2.2
CRITICAL_AVG_XTE = 1
MAX_ACC = 2.0

DO_PLOT_GIFS = True
FPS_DESIRED_DONKEY = 19

TIME_WAIT_DONKEY_RERUN = 3
