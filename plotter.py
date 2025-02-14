import matplotlib.pyplot as plt
from dataclasses import dataclass
from time import gmtime, strftime
import os

import numpy as np

from structs import ParticleData, SimFlowFuncs, PlottingData
from iterator import getVelocitiesFromPositionsCartConverted

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
        xsMatrix, ysMatrix = np.meshgrid(Xcoords, Ycoords)

        # Flatten so is an array of particles xs and ys
        xs = xsMatrix.flatten()
        ys = ysMatrix.flatten()

        # Apply meshgird points to get U, V matrix
        vxs, vys = getVelocitiesFromPositionsCartConverted(
            postions = np.array([xs, ys]),
            flowData = self.flowData
        )

        # Clip values to avoid singularities
        # TODO improve this so dynamic
        vxs = np.clip(vxs, self.plottingData.minVelocity, self.plottingData.maxVelocity)
        vys = np.clip(vys, self.plottingData.minVelocity, self.plottingData.maxVelocity)

        # Reshape velocity outputs into matrices
        vxsMatrix = vxs.reshape(xsMatrix.shape)
        vysMatrix = vys.reshape(ysMatrix.shape)

        # Return the calculated values
        return xsMatrix, ysMatrix, vxsMatrix, vysMatrix 

    # Saves the plot with correct structure
    def _savePlot(self):
        
        # Get path names
        dateHour = strftime(self.plottingData.plotFolderFormat, gmtime())
        dateHourFolder = os.path.join("plots", dateHour)
        plotPath = os.path.join("plots", dateHour, f"{strftime(self.plottingData.plotFileFormat, gmtime())}.{self.plottingData.plotSaveType}")
        
        # Check plot path exists (if not make it)
        if not os.path.exists(dateHourFolder): os.makedirs(dateHourFolder)

        # Save the plot
        plt.savefig(fname = plotPath, dpi = 800)

    def plotParticles(self):

        ## Setting up how streamlines are plotted

        # Pre-calculations
        x, y, u, v = self._getFlowMap()
        flowSpeed = np.sqrt(u**2 + v**2)
        streamLineWidth = 2 * flowSpeed / np.max(flowSpeed)

        # Finding flow speeds
        flowSpeed = np.sqrt(u**2 + v**2)
        streamLineWidth = 0.75 * flowSpeed / np.max(flowSpeed)

        # Plotting streamlines
        stream = plt.streamplot(x, y, u, v,
            density=self.plottingData.streamLinesPlotDensity,
            linewidth = streamLineWidth,
            broken_streamlines=self.plottingData.brokenStreamlines,
            color="k"
            )
        
        # Setting how points are plotted
        
        # Plotting the line data
        if self.plottingData.plotInitLine:
            plt.plot(*self.particleData.particleInitPositions, label=f"Inital dye")

        if self.plottingData.plotFinalLine:
            plt.plot(*self.particleData.particlePositions, label=f"Dye line after {self.timePast}s")

        # Plotting the scattering data
        if self.plottingData.plotInitPoints:
            plt.scatter(*self.particleData.particleInitPositions, marker=",", c = "g", s = 1, label="Inital dye")

        if self.plottingData.plotFinalPoints:
            plt.scatter(*self.particleData.particlePositions, marker=",", c = "r", s = 1, label=f"Dye after {self.timePast}s")

        ## Setting plot features

        # Set plot limits
        plt.xlim(self.xMin, self.xMax)
        plt.ylim(self.yMin, self.yMax)

        # Setup plot features
        if self.plottingData.includeGird: plt.grid()
        if self.plottingData.inlcudeLegend: plt.legend()
        if self.plottingData.includeXLabel: plt.xlabel(self.plottingData.xLabel)
        if self.plottingData.includeYLabel: plt.ylabel(self.plottingData.yLabel)

        # Save and showing plot settings
        if self.plottingData.saveFigure: self._savePlot()
        if self.plottingData.showFigure: plt.show()
        