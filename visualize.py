from dataclasses import dataclass
from matplotlib.widgets import RangeSlider
import mpl_interactions.ipyplot as iplt

import numpy as np

from structs import SimFlowFuncs, SimSetupData, ParticleData, PlottingData
from iterator import iterateParticles
from plotter import Plotting


@dataclass
class Visualizer():

    # The data used to define the flow
    flowData: SimFlowFuncs

    # The data used to setup how iterations run
    setupData: SimSetupData

    # The data used to store the particle infomation
    particleData: ParticleData

    # The data used to plot the results
    plottingData: PlottingData

    def __post_init__(self):
        self.plotter = Plotting(
            self.flowData, self.particleData, self.plottingData)

    # Iterate the particles one step in time
    def iterate(self, numIter=1):

        # TODO: @Joshua13764 Each loop takes ~ 500ms to run! This needs to be optimised!
        for _ in range(numIter):

            iterateParticles(self.particleData, self.flowData, self.setupData)

    # Plot the particles currently
    def plot(self, interactive=False):
        if interactive:
            self.plotter.plotParticles(args={'interactive': True,
                                             'timeStep': self.setupData.timeStep,
                                             'visualizer': self})
        else:
            self.plotter.plotParticles()
