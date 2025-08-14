from pydantic.dataclasses import dataclass
from typing import Dict, List, Tuple
import os
import sys
import json
from dataclasses import field


@dataclass
class SimulationOutput():
    """A class to sequentially store the outputs of a simulation

    Returns:
        _type_: _description_
    """
    elapsedTime : float = -1
    iterations : int = -1
    positions : List[Tuple[float, float, float]] = field(default_factory=lambda: [])
    speeds: List[float] = field(default_factory=lambda: [])
    xtes: List[float] = field(default_factory=lambda: [])
    steerings : List[float] = field(default_factory=lambda: [])
    throttles: List[float] = field(default_factory=lambda: [])
    road: List[Tuple] = field(default_factory=lambda: [])

    # def to_json(self):
    #     return json.dumps(self.__dict__)

    def addStats(
            self,
            position:Tuple[float, float, float],
            speed:float,
            xte:float,
            steering: float,
            throttle:float) -> None:
        self.positions.append(position)
        self.speeds.append(speed)
        self.xtes.append(xte)
        self.steerings.append(steering)
        self.throttles.append(throttle)

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)
