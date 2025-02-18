import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import mpl_interactions.ipyplot as iplt

from dataclasses import dataclass
from time import gmtime, strftime
import os

import numpy as np

from structs import ParticleData, SimFlowFuncs, PlottingData
from iterator import getVelocitiesFromPositionsCartConverted


@dataclass
class Plotting():

    # The data used to define the flow
    flowData: SimFlowFuncs

    # The data used to store the particle infomation
    particleData: ParticleData

    # The data used to aid with plot formatting
    plottingData: PlottingData

    # Pre-processing step auto run after init
    def __post_init__(self):

        # Find min and max values to plot to
        self.xMin = self.plottingData.plotCenter[0] - \
            self.plottingData.plotSimWidth * 0.5
        self.xMax = self.plottingData.plotCenter[0] + \
            self.plottingData.plotSimWidth * 0.5

        self.yMin = self.plottingData.plotCenter[1] - \
            self.plottingData.plotSimWidth * 0.5
        self.yMax = self.plottingData.plotCenter[1] + \
            self.plottingData.plotSimWidth * 0.5

    # Gets an array of flow data (used by stream plots)
    def _getFlowMap(self):

        # Create divisions for the coodinates in x direction
        Xcoords = np.linspace(
            start=self.xMin,
            stop=self.xMax,
            num=self.plottingData.flowMapResolution,
            dtype=np.float64  # Needed to resolve odd divisions
        )

        # Create divisions for the coodinates in y direction
        Ycoords = np.linspace(
            start=self.yMin,
            stop=self.yMax,
            num=self.plottingData.flowMapResolution,
            dtype=np.float64  # Needed to resolve odd divisions
        )

        # Create mesh grid
        xsMatrix, ysMatrix = np.meshgrid(Xcoords, Ycoords)

        # Flatten so is an array of particles xs and ys
        xs = xsMatrix.flatten()
        ys = ysMatrix.flatten()

        # Apply meshgird points to get U, V matrix
        vxs, vys = getVelocitiesFromPositionsCartConverted(
            postions=np.array([xs, ys]),
            flowData=self.flowData
        )

        # Clip values to avoid singularities
        # TODO improve this so dynamic
        vxs = np.clip(vxs, self.plottingData.minVelocity,
                      self.plottingData.maxVelocity)
        vys = np.clip(vys, self.plottingData.minVelocity,
                      self.plottingData.maxVelocity)

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
        plotPath = os.path.join(
            "plots", dateHour, f"{strftime(self.plottingData.plotFileFormat, gmtime())}.{self.plottingData.plotSaveType}")

        # Check plot path exists (if not make it)
        if not os.path.exists(dateHourFolder):
            os.makedirs(dateHourFolder)

        # Save the plot
        plt.savefig(fname=plotPath, dpi=800)

    def plotParticles(self, streamlineWidth=2, args: dict = {}):

        # Functions used for the interactive plotter
        def f_x(time):
            return self.particleData.positionsAtTime(int(time // args['timeStep']), args['visualizer'])[0]

        def f_y(_, time):
            return self.particleData.positionsAtTime(int(time // args['timeStep']), args['visualizer'])[1]

        # Setting up how streamlines are plotted

        # Pre-calculations
        x, y, v_x, v_y = self._getFlowMap()
        flowSpeed = np.sqrt(v_x**2 + v_y**2)
        # Faster flow -> Thicker line
        streamlineWidth *= flowSpeed / np.max(flowSpeed)

        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        # Plotting streamlines
        stream = plt.streamplot(x, y, v_x, v_y,
                                density=self.plottingData.streamLinesPlotDensity,
                                linewidth=streamlineWidth,
                                broken_streamlines=self.plottingData.brokenStreamlines,
                                color="k"
                                )

        # Interactive slider setup
        if args:
            axfreq = plt.axes([0.15, 0.1, 0.65, 0.03])
            slider = Slider(axfreq,
                            label="Time",
                            valmin=self.plottingData.timeSteps_range[0],
                            valmax=self.plottingData.timeSteps_range[1] *
                            args['timeStep'],
                            valstep=args['timeStep'],
                            valinit=0)

        # Plotting the line data
        if self.plottingData.plotInitLine:
            plt.plot(*self.particleData.positions[0],
                     label=f"Inital dye")

        if self.plottingData.plotFinalLine:
            if not args:
                plt.plot(*self.particleData.positions[-1],
                         label=f"Dye line after {self.particleData.timePast()}s")
            else:

                controls = iplt.plot(f_x, f_y,
                                     label=f"Dye line after {self.particleData.timePast()}s",
                                     time=slider, ax=ax)

        # Plotting the scattering data
        if self.plottingData.plotInitPoints:
            plt.scatter(*self.particleData.positions[0],
                        marker=",", c="g", s=1, label="Inital dye")

        if self.plottingData.plotFinalPoints:
            if not args:
                plt.scatter(*self.particleData.positions[-1], marker=",",
                            c="r", s=1, label=f"Dye after {self.particleData.timePast()}s")
            else:
                controls = iplt.scatter(f_x, f_y,
                                        marker=",", c="r", s=1,
                                        label=f"Dye line after {self.particleData.timePast()}s",
                                        time=slider, ax=ax)

        # Setting plot features

        # Set plot limits
        plt.xlim(self.xMin, self.xMax)
        plt.ylim(self.yMin, self.yMax)

        # Setup plot features
        if self.plottingData.includeGird:
            plt.grid()
        if self.plottingData.inlcudeLegend:
            plt.legend()
        if self.plottingData.includeXLabel:
            plt.xlabel(self.plottingData.xLabel)
        if self.plottingData.includeYLabel:
            plt.ylabel(self.plottingData.yLabel)

        # Save and showing plot settings
        if self.plottingData.saveFigure:
            self._savePlot()
        if self.plottingData.showFigure:
            plt.show()
