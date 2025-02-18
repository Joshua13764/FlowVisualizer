from dataclasses import dataclass

import numpy as np


@dataclass
class SimFlowFuncs():

    # Placeholder variables for the fields (Eulerian specification of the flow field)

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

    # Simulation variables
    timeStep: float
    subtimeSteps = 32


@dataclass
class ParticleData():

    # Particle positions, velocity, mass (so can add drifing effects)
    positions = np.array([[[], []]])
    velocities = np.array([[], []])
    masses = np.array([])

    # Store the past positions of the particles
    positionHistory = []

    # Array of the index of the first particle in a shape used to draw the shapes correctly
    shapeStarts = []

    # Positions at time finds the position of a particle for a given time
    def positionsAtTime(self, iterationIndex: float):

        # TODO make so renders more if needed
        # Check that not accsessing iterations that don't exist
        if iterationIndex >= len(self.positionHistory):
            raise ValueError(
                "Iteration index exceeds what is currently rendered")

        # Find bounding indices
        floorIndex = int(np.floor(iterationIndex))
        ceilIndex = int(np.ceil(iterationIndex))

        # Find bounding positions
        floorPositions = self.positionHistory[floorIndex]
        ceilPositions = self.positionHistory[ceilIndex]

        # Find interp positions
        frac, integer = np.modf(iterationIndex)
        interpPos = floorPositions * frac + (1 - frac) * ceilPositions

        # Return the interp positions
        return interpPos

    def timePast(self):
        return self.positions.shape[1]

    # Giving adding dye functionality
    def __add__(self, new_particle):  # particleData1 + particleData2

        if type(new_particle) != ParticleData:
            return TypeError

        # If no items in self then set self to the added item
        if self.positions.size == 0:
            self = new_particle

        # If no items in new_particle then no effect
        if new_particle.positions.size == 0:
            return self

        # Positions
        self.positions = np.concatenate(
            (self.positions,
             new_particle.positions),
            axis=2
        )

        # Velocity
        self.velocities = np.concatenate(
            (self.velocities,
             new_particle.velocities),
            axis=1
        )

        # Masses
        self.masses = np.concatenate(
            (self.masses,
             new_particle.masses),
            axis=1
        )

        # Shape starts
        shapeStartOffset = len(self.shapeStarts) - 1
        self.shapeStarts += [shapeStart +
                             shapeStartOffset for shapeStart in new_particle.shapeStarts]

        return self

    def __iadd__(self, new_particle):  # particleData1 += particleData2

        return self.__add__(new_particle)


@dataclass
class PlottingData():

    # Flags

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

    # Save settings
    plotFolderFormat = "%Y-%m-%d %HH"
    plotFileFormat = "%Y-%m-%d %HH%MM%SS"
    plotSaveType = "png"

    # Plot dimentions
    plotSimWidth = 4
    plotSimHeight = 4
    plotCenter = np.array([0, 0])

    # Plot streamlines
    flowMapResolution = 300
    brokenStreamlines = False
    cmap = 'autumn'
    backgroundAlpha = 1
    maxVelocity = 10
    minVelocity = -10
    streamLinesPlotDensity = 0.5

    # Plotting axis labels
    xLabel = "x"
    yLabel = "y"

    # Interactive plot settings
    timeSteps_range = (0, 100)
