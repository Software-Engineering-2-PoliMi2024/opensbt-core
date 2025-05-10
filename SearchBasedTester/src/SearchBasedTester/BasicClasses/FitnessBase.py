from typing import List, Tuple, Dict, Any
import numpy as np
from operator import itemgetter


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

    def getFitnesses(self, samples: List[List[float]]) -> List[float]:
        """
        Get the fitnesses of a list of samples from the dictionary
        :param samples: The samples to get the fitnesses for
        :return: The fitnesses of the samples
        """
        return itemgetter(*map(tuple, samples))(self.fitnesses)
