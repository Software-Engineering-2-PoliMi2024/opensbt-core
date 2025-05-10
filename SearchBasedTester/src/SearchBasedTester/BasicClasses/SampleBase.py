from typing import List, Tuple
import numpy as np


class SampleBase:
    """
    This class will store all the samples produced so far.
    """

    def __init__(self, sampleRanges: List[Tuple[float, float]], gridSize: float):
        """
        :param sampleDimension: The dimension of the sample
        :param gridSize: The size of the grid
        """

        self.sampleDimension = len(sampleRanges)
        self.sampleRanges = np.array(sampleRanges)
        self.gridSize = gridSize
        self.binNumbers = (
            self.sampleRanges[:, 1] - self.sampleRanges[:, 0]) / gridSize

        self.binNumbers = np.ceil(self.binNumbers).astype(int)

        self.samples = np.empty(self.binNumbers, dtype=object)
        for index, _ in np.ndenumerate(self.samples):
            self.samples[index] = []

    def getSampleIndex(self, sample: List[float]) -> Tuple[int]:
        """
        Get the index of the sample in the grid
        :param sample: The sample to get the index for
        :return: The index of the sample in the grid
        """
        index = []
        for i in range(self.sampleDimension):
            index.append(
                int((sample[i] - self.sampleRanges[i][0]) / self.gridSize))
        return tuple(index)

    def addSample(self, sample: List[float]):
        """
        Add a sample to the grid
        :param sample: The sample to add
        """
        index = self.getSampleIndex(sample)
        self.samples[index].append(sample)

    def getAllSamples(self) -> np.ndarray:
        """
        Get all the samples in the grid
        :return: All the samples in the grid
        """
        return np.array([sample for sublist in self.samples.flat for sample in sublist if len(sublist) != 0], dtype=float)

    def getNeighbours(self, sample: List[float]) -> np.ndarray:
        """
        Get the neighbours of a sample in the grid
        :param sample: The sample to get the neighbours for
        :return: The neighbours of the sample in the grid
        """
        index = self.getSampleIndex(sample)
        index = tuple([slice(max(0, i - 1), min(i + 2, self.binNumbers[j]), 1)
                       for j, i in enumerate(index)])
        neighbours = [sample for sublist in self.samples[index].flat
                      for sample in sublist if len(sublist) != 0]
        return neighbours


if __name__ == "__main__":
    sample = SampleBase([(0, 1), (0, 1)], 0.1)
    print(sample.sampleDimension)
    print(sample.gridSize)
    print(sample.sampleRanges)
    print(sample.binNumbers)
    print(sample.samples)
    print(sample.samples.shape)

    sample.addSample(np.array([0.1, 0.2]))
    print(sample.getAllSamples())

    sample.addSample(np.array([0.2, 0.3]))
    print(sample.getAllSamples())
    sample.addSample(np.array([0.3, 0.4]))
    print(sample.getAllSamples())

    sample.addSample(np.array([0.4, 0.5]))
    print(sample.getAllSamples())

    print(sample.getNeighbours(np.array([0.1, 0.2])))
