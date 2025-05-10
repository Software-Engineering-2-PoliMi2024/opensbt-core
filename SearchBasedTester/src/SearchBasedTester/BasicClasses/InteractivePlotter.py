import numpy as np
from typing import List, Tuple
from matplotlib import pyplot as plt
from IPython import display
import time
from .SampleBase import SampleBase
from .FitnessBase import FitnessBase
import seaborn as sns


class InteractivePlotter:
    def __init__(self):
        plt.ioff()
        self.fig, self.axs = plt.subplots(1, 2, figsize=(16, 8))

    def __call__(self, sampleBase: SampleBase, fitnessBase: FitnessBase, f=lambda x: x):
        self.draw(sampleBase, fitnessBase, f)
        display.clear_output(wait=True)
        display.display(plt.gcf())
        time.sleep(1e-16)

    def draw(self, sampleBase: SampleBase, fitnessBase: FitnessBase, f=lambda x: x):
        sns.set_theme()
        self.axs[0].cla()
        x = np.linspace(
            sampleBase.sampleRanges[0][0],
            sampleBase.sampleRanges[0][1],
            100,
        )

        y = np.linspace(
            sampleBase.sampleRanges[1][0],
            sampleBase.sampleRanges[1][1],
            100,
        )

        X, Y = np.meshgrid(x, y)
        Z = np.zeros(X.shape)
        try:
            Z = f(X, Y)
        except Exception as e:
            print(f"Error in fitness function: {e}")
            return

        self.axs[0].contourf(X, Y, Z, levels=100)

        samples = sampleBase.getAllSamples()
        fitnesses = np.array(
            [fitnessBase.getFitness(sample) for sample in samples]
        )

        # scatter the samples
        self.axs[0].scatter(
            samples[:, 0],
            samples[:, 1],
            c=fitnesses,
            cmap="viridis",
            s=100,
        )

        self.axs[0].set_xlabel("X")
        self.axs[0].set_ylabel("Y")
        self.axs[0].set_title("Fitness Landscape")
        self.axs[0].set_xlim(sampleBase.sampleRanges[0][0],
                             sampleBase.sampleRanges[0][1])
        self.axs[0].set_ylim(sampleBase.sampleRanges[1][0],
                             sampleBase.sampleRanges[1][1])
        self.axs[0].set_aspect("equal")
        self.axs[0].grid()

        # plot the fitness distribution
        self.axs[1].cla()
        fitnesses = list(fitnessBase.fitnesses.values())
        sns.histplot(fitnesses, bins=50, kde=True, ax=self.axs[1])
        self.axs[1].set_xlabel("Fitness")
        self.axs[1].set_ylabel("Count")
        self.axs[1].set_title("Fitness Distribution")
        if fitnesses:
            self.axs[1].set_xlim(min(fitnesses), max(fitnesses))
        self.axs[1].grid()
