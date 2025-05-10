from typing import List, Tuple, Dict, Any
import numpy as np


class FitnessBase:
    def __init__(self):
        self.fitnesses: Dict = {}

    def writeFitness(self, sample: List[float], fitness: float):
        """
        Write the fitness of a sample to the dictionary
        :param sample: The sample to write the fitness for
        :param fitness: The fitness of the sample
        """
        self.fitnesses[tuple(sample)] = fitness

    def getFitness(self, sample: List[float]) -> float:
        """
        Get the fitness of a sample from the dictionary
        :param sample: The sample to get the fitness for
        :return: The fitness of the sample
        """
        return self.fitnesses.get(tuple(sample), None)
