import matplotlib.pyplot as plt
from dataclasses import dataclass

import numpy as np

from structs import ParticleData, SimFlowFuncs, PlottingData

@dataclass
class Plotting():

    # The data used to define the flow
    flowData : SimFlowFuncs

    # The data used to store the particle infomation
    particleData : ParticleData

    # The data used to aid with plot formatting
    plottingData : PlottingData

    # Pre-processing step auto run after init
    def __post_init__(self):

        # Find min and max values to plot to
        self.xMin = self.plottingData.plotCenter[0] - self.plottingData.plotSimWidth * 0.5
        self.xMax = self.plottingData.plotCenter[0] + self.plottingData.plotSimWidth * 0.5

        self.yMin = self.plottingData.plotCenter[1] - self.plottingData.plotSimWidth * 0.5
        self.yMax = self.plottingData.plotCenter[1] + self.plottingData.plotSimWidth * 0.5

    # Gets an array of flow data (used by stream plots)
    def _getFlowMap(self):

        # Create divisions for the coodinates in x direction
        Xcoords = np.linspace(
            start = self.xMin,
            stop = self.xMax,
            num = self.plottingData.flowMapResolution
        )

        # Create divisions for the coodinates in y direction
        Ycoords = np.linspace(
            start = self.yMin,
            stop = self.yMax,
            num = self.plottingData.flowMapResolution
        )

        # Create mesh grid
        xs, ys = np.meshgrid(Xcoords, Ycoords, sparse=True)
        
        # Apply meshgird to get U, V matrix
        # TODO get rid off the term (xs + ys)*0 to improve matrix maths
        vxs = self.flowData.vx(xs, ys) + (xs + ys)*0
        vys = self.flowData.vy(xs, ys) + (xs + ys)*0

        # Return the calculated values
        return xs, ys, vxs, vys 

    def plotParticles(self):

        x, y, u, v = self._getFlowMap()

        
        # Plot background matrix
        # plt.matshow(u)

        # Plot streamlines

        flowSpeed = np.sqrt(u**2 + v**2)
        streamLineWidth = flowSpeed / np.max(flowSpeed)

        stream = plt.streamplot(x, y, u, v,
            density=0.5,
            linewidth = streamLineWidth,
            broken_streamlines=self.plottingData.brokenStreamlines,
            color=flowSpeed,
            cmap=self.plottingData.cmap
            )
        
        plt.colorbar(stream.lines)

        # Plot points
        plt.scatter(*self.particleData.particlePositions)

        # Set plot limits
        plt.xlim(self.xMin, self.xMax)
        plt.ylim(self.yMin, self.yMax)

        # Add chart features
        plt.grid()
        plt.show()