from dataclasses import dataclass

import numpy

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

    # Iterate the particles one step in time
    def iterate(self, numbIter=1):

        # Make record of init particle positions
        self.particleData.markInitPositions()

        for i in range(numbIter):

            iterateParticles(self.particleData, self.flowData, self.setupData)

        # Find the time passed in seconds
        self.timePast = numbIter * self.setupData.timeStep

    # Plot the particles currently
    def plot(self):

        plotter = Plotting(self.flowData, self.particleData,
                           self.plottingData, self.timePast)
        plotter.plotParticles()
