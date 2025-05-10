import numpy as np
from typing import List, Tuple
from matplotlib import pyplot as plt
from IPython import display
import time
from .SampleBase import SampleBase
from .FitnessBase import FitnessBase
import seaborn as sns
import ipywidgets as widgets


class InteractivePlotter:
    def __init__(self):
        plt.ioff()
        self.fig, self.axs = plt.subplots(1, 2, figsize=(16, 8))

    def __call__(self, sampleBase: SampleBase, fitnessBase: FitnessBase, spikeFitnessBase: FitnessBase, f=lambda x: x, gridSize=0.1):
        self.draw(sampleBase, fitnessBase, spikeFitnessBase, f, gridSize)
        display.clear_output(wait=True)
        display.display(plt.gcf())
        time.sleep(1e-16)

    def draw(self, sampleBase: SampleBase, fitnessBase: FitnessBase, spikeFitnessBase: FitnessBase, f=lambda x: x, gridSize=0.1):
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
            [spikeFitnessBase.getFitness(sample) for sample in samples]
        )

        # scatter the samples
        scatter = self.axs[0].scatter(
            samples[:, 0],
            samples[:, 1],
            c=fitnesses,
            cmap="viridis",
            s=100,
        )
        # Add a single color bar for the first axes if it doesn't already exist
        if not hasattr(self, 'cbar') or self.cbar is None:
            self.cbar = self.fig.colorbar(scatter, ax=self.axs[0])
            self.cbar.set_label("Fitness Value")
        else:
            self.cbar.update_normal(scatter)

        self.axs[0].set_xlabel("X")
        self.axs[0].set_ylabel("Y")
        self.axs[0].set_title("Fitness Landscape")
        self.axs[0].set_xlim(sampleBase.sampleRanges[0][0],
                             sampleBase.sampleRanges[0][1])
        self.axs[0].set_ylim(sampleBase.sampleRanges[1][0],
                             sampleBase.sampleRanges[1][1])
        self.axs[0].set_aspect("equal")
        # Plot a grid using the grid size
        for i in range(int((sampleBase.sampleRanges[0][1] - sampleBase.sampleRanges[0][0]) / gridSize) + 1):
            self.axs[0].axvline(
                x=sampleBase.sampleRanges[0][0] + i * gridSize,
                color="black",
                linestyle="--",
                alpha=0.5,
            )

        for i in range(int((sampleBase.sampleRanges[1][1] - sampleBase.sampleRanges[1][0]) / gridSize) + 1):
            self.axs[0].axhline(
                y=sampleBase.sampleRanges[1][0] + i * gridSize,
                color="black",
                linestyle="--",
                alpha=0.5,
            )

        # plot the fitness distribution
        self.axs[1].cla()
        fitnesses = list(fitnessBase.fitnesses.values())
        sns.histplot(fitnesses, bins=50, kde=True,
                     ax=self.axs[1], label="Fitness")
        spikeFitnesses = list(spikeFitnessBase.fitnesses.values())
        sns.histplot(spikeFitnesses, bins=50, kde=True,
                     ax=self.axs[1], color="red", label="Spike Fitness", alpha=0.5)
        self.axs[1].set_xlabel("Fitness")
        self.axs[1].set_ylabel("Count")
        self.axs[1].set_title("Fitness Distribution")
        if fitnesses:
            self.axs[1].set_xlim(min(fitnesses), max(fitnesses))
        self.axs[1].legend()
