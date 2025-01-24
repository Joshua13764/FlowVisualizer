from dataclasses import dataclass

import numpy

from structs import SimFlowFuncs, SimSetupData, ParticleData, PlottingData
from iterator import iterateParticles
from plotter import Plotting

@dataclass
class Visualizer():

    # The data used to define the flow
    flowData : SimFlowFuncs

    # The data used to setup how iterations run
    setupData : SimSetupData

    # The data used to store the particle infomation
    particleData : ParticleData

    # The data used to plot the results
    plottingData : PlottingData

    # Iterate the particles one step in time
    def iterate(self, numbIter = 1):

        for i in range(numbIter):

            iterateParticles(self.particleData, self.flowData, self.setupData)

    # Plot the particles currently
    def plot(self):

        plotter = Plotting(self.flowData, self.particleData, self.plottingData)
        plotter.plotParticles()

        