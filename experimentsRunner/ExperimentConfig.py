from lanekeeping.udacity.UdacitySimulatorConfig import UdacitySimulatorConfig
from .SearchField import SearchField
from typing import List, Iterator
from dataclasses import dataclass
import copy

@dataclass
class ExperimentConfig:
    scenarioConf: UdacitySimulatorConfig
    searchFields: List[SearchField]

    def __post_init__(self):
        self.reset()
        self._firstIter = True

    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self) -> UdacitySimulatorConfig:
        if not self.searchFields:
            raise StopIteration
        
        if self._firstIter:
            self._firstIter = False
            return copy.deepcopy(self.scenarioConf)            
        
        for i, field in enumerate(self.searchFields):
            try:
                next(field)
                return copy.deepcopy(self.scenarioConf)
            except StopIteration:
                field.reset()
                if i == len(self.searchFields) - 1:
                    raise StopIteration
                continue

    def reset(self):
        for field in self.searchFields:
            field.reset()