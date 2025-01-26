import matplotlib.pyplot as plt
from dataclasses import dataclass
from time import gmtime, strftime
import os

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

    # The time passed in seconds since simulation start
    timePast : np.float64

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
            num = self.plottingData.flowMapResolution,
            dtype = np.float64 # Needed to resolve odd divisions
        )

        # Create divisions for the coodinates in y direction
        Ycoords = np.linspace(
            start = self.yMin,
            stop = self.yMax,
            num = self.plottingData.flowMapResolution,
            dtype = np.float64 # Needed to resolve odd divisions
        )

        # Create mesh grid
        xs, ys = np.meshgrid(Xcoords, Ycoords)

        # Apply meshgird to get U, V matrix
        vxs = self.flowData.vx(xs, ys)
        vys = self.flowData.vy(xs, ys)

        # Clip values to avoid singularities
        # TODO improve this so dynamic
        vxs = np.clip(vxs, self.plottingData.minVelocity, self.plottingData.maxVelocity)
        vys = np.clip(vys, self.plottingData.minVelocity, self.plottingData.maxVelocity)

        # Return the calculated values
        return xs, ys, vxs, vys 

    def plotParticles(self):

        # Pre-calculations
        x, y, u, v = self._getFlowMap()
        flowSpeed = np.sqrt(u**2 + v**2)
        streamLineWidth = 2 * flowSpeed / np.max(flowSpeed)
        
        # Plot background matrix
        # extent = (self.xMin, self.xMax, self.yMin, self.yMax)
        # plt.matshow(flowSpeed, origin = "lower", extent = extent, alpha = self.plottingData.backgroundAlpha)

        # Plot streamlines
        flowSpeed = np.sqrt(u**2 + v**2)
        streamLineWidth = 2 * flowSpeed / np.max(flowSpeed)

        stream = plt.streamplot(x, y, u, v,
            density=1,
            linewidth = streamLineWidth,
            broken_streamlines=self.plottingData.brokenStreamlines,
            color="k"
            )
        
        # plt.colorbar(stream.lines)

        # Plot init points
        plt.scatter(*self.particleData.particleInitPositions, marker=",", c = "g", s = 1, label="Inital dye")

        # Plot time iterated points points
        plt.scatter(*self.particleData.particlePositions, marker=",", c = "r", s = 1, label=f"Dye after {self.timePast}s")

        # Set plot limits
        plt.xlim(self.xMin, self.xMax)
        plt.ylim(self.yMin, self.yMax)

        # Add chart features
        # plt.grid()
        # plt.colorbar(boundaries = (0, np.max(flowSpeed)))

        plt.xlabel(self.plottingData.xLabel)
        plt.ylabel(self.plottingData.yLabel)
        plt.legend()
        plt.grid()

        dateHour = strftime('%Y-%m-%d %HH', gmtime())
        dateHourFolder = os.path.join("plots", dateHour)
        plotPath = os.path.join("plots", dateHour, f"{strftime('%Y-%m-%d %HH%MM%SS', gmtime())}.png")
        if not os.path.exists(dateHourFolder): os.makedirs(dateHourFolder)

        plt.savefig(fname =plotPath, dpi=800)
        plt.show()
        