from dataclasses import dataclass
from typing import TypeVar, Generic, Tuple, Iterator, Callable, Dict
from lanekeeping.udacity.UdacitySimulatorConfig import UdacitySimulatorConfig
from . import dictionaryUtils
T = TypeVar('T')

@dataclass
class SearchField(Generic[T]):
    label: str
    step: T
    range: Tuple[T, T]
    updateConfig: Callable

    def __post_init__(self):
        self.current_value = self.range[0]
        self.__commitToConfig()

    def __commitToConfig(self):
        self.updateConfig(self.current_value)

    def __iter__(self) -> Iterator[T]:
        return self
    
    def get(self) -> T:
        return self.current_value
    
    def __next__(self) -> T:
        if self.current_value >= self.range[1]:
            raise StopIteration
        
        self.current_value += self.step

        self.__commitToConfig()
        return self.get()
    
    def reset(self):
        self.current_value = self.range[0]
        self.__commitToConfig()

    def test(self, val):
        self.updateConfig(val)

    @classmethod
    def fromDict(cls, data: Dict, updateConfMethod: Callable):
        data = dictionaryUtils.filterClassAttributes(data, cls)
        data = dictionaryUtils.listToTuples(data, cls)
        
        return cls(**data, updateConfig=updateConfMethod)
