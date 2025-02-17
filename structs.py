from dataclasses import dataclass

import numpy as np

@dataclass
class SimFlowFuncs():

    ## Placeholder variables for the fields (Eulerian specification of the flow field)

    # Cartesian coordinates (in terms of x, y)
    vx = None
    vy = None

    # Polar coodinates
    vr = None
    vtheta = None

    # Vector flow function (in terms of x, y, r, theta, xHat, yHat, rHat, thetaHat)
    v = None

@dataclass
class SimSetupData():

    ## Simulation variables
    timeStep : float
    subtimeSteps = 32

@dataclass
class ParticleData():

    ## Particle positions, velocity, mass (so can add drifing effects)
    particlePositions = np.array([[],[]])
    particleVelocities = np.array([[],[]])
    particleMasses = np.array([])

    # Array of the index of the first particle in a shape used to draw the shapes correctly
    shapeStarts = []
    
    ## Create the post init vars
    def markInitPositions(self):
        self.particleInitPositions = self.particlePositions.copy()

    # Giving adding dye functionality
    def __add__(self, other): #  particleData1 + particleData2

        if type(other) != ParticleData: return TypeError

        # If no items in self then set self to the added item
        if self.particlePositions.size == 0: self = other

        # If no items in other then no effect
        if other.particlePositions.size == 0: return self

        # Positions
        self.particlePositions = np.concatenate(
            (self.particlePositions,
            other.particlePositions),
            axis = 1
        )

        # Velocity
        self.particleVelocities = np.concatenate(
            (self.particleVelocities,
            other.particleVelocities),
            axis = 1
        )

        # Masses
        self.particleMasses = np.concatenate(
            (self.particleMasses,
            other.particleMasses),
            axis = 1
        )

        # Shape starts
        shapeStartOffset = len(self.shapeStarts) - 1
        self.shapeStarts += [shapeStart + shapeStartOffset for shapeStart in other.shapeStarts]

        return self

    def __iadd__(self, other): #  particleData1 += particleData2
        
        return self.__add__(other)

@dataclass
class PlottingData():

    ## Flags

    # General flags
    includeGird = False
    inlcudeLegend = True
    includeXLabel = True
    includeYLabel = True

    saveFigure = False
    showFigure = True

    # Data plotting flags
    plotInitLine = False
    plotFinalLine = False
    plotInitPoints = True
    plotFinalPoints = True

    ## Save settings
    plotFolderFormat = "%Y-%m-%d %HH"
    plotFileFormat = "%Y-%m-%d %HH%MM%SS"
    plotSaveType = "png"

    ## Plot dimentions
    plotSimWidth = 4
    plotSimHeight = 4
    plotCenter = np.array([0,0])

    ## Plot streamlines
    flowMapResolution = 2048
    brokenStreamlines = False
    backgroundAlpha = 1
    maxVelocity = 10
    minVelocity = -10
    streamLinesPlotDensity = 0.5

    ## Plotting axis labels
    xLabel = "x"
    yLabel = "y"