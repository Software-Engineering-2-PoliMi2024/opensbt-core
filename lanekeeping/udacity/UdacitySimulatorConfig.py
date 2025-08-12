from dataclasses import dataclass
from typing import List
from experimentsRunner import dictionaryUtils
@dataclass
class UdacitySimulatorConfig:
    """
    Configuration for the Udacity simulator.

    Arguments:
        map_size (int): Size of the map. The map is a square with dimensions map_size x map_size. (default: 250)
        initial_position (tuple): Initial position of the ego vehicle in the simulation.
            Format: (x, y, z, road_width) where x and y are the coordinates, z is the height, and road_width is the width of the road.
            (default: (125.0, 0, -28.0, 8))
        maxSpeed (float): Maximum speed of the ego vehicle in the simulation. (default: 30.0)
        minSpeed (float): Minimum speed of the ego vehicle in the simulation. (default: 0.0)
        maxTime (int): Maximum time in seconds for the simulation to run. (default: 30)
        maxXTE (float): Maximum cross-track error (XTE) allowed.
        segLength (float): Length of each segment in the road. (default: 25.0)
        angles (List[int]): Angles for the road segments, to be set during simulation. (default: (0, 0, 0, 0, 0))
    """
    map_size: int = 250
    initial_position: tuple = (125.0, 0.0, -28.0, 8.0)
    maxSpeed: float = 30.0  # Maximum speed of the ego vehicle in the simulation
    minSpeed: float = 0.0  # Minimum speed of the ego vehicle in the simulation
    maxTime: int = 30  # Maximum time in seconds for the simulation to run
    # Maximum cross-track error (XTE) allowed, if negative, no limit is applied
    maxXTE: float = 3.0

    segLength: float = 25.0  # Length of each segment in the road
    # Angles for the road segments, to be set during simulation
    angles: List[int] = (0, 0, 0, 0, 0)

    @classmethod
    def fromDict(cls, data: dict):
        data = dictionaryUtils.filterClassAttributes(data, cls)
        data = dictionaryUtils.listToTuples(data, cls)
        
        return cls(**data)

if __name__ == "__main__":
    config = UdacitySimulatorConfig()
    print(config)
