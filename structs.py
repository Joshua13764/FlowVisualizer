from dataclasses import dataclass

import numpy as np

@dataclass
class SimFlowFuncs():

    ## Placeholder variables for the fields (Eulerian specification of the flow field)

    # Cartesian coordinates
    vx = None
    vy = None

    # Polar coodinates
    vr = None
    vtheta = None

@dataclass
class SimSetupData():

    ## Simulation variables
    timeStep : float
    subtimeSteps = 32

@dataclass
class ParticleData():

    ## Particle positions, velocity, mass (so can add drifing effects)
    particlePositions = np.array([0])
    particleVelocities = np.array([0])
    particleMasses = np.array([1])

    ## Create the post init vars
    def markInitPositions(self):
        self.particleInitPositions = self.particlePositions.copy()

    # Giving adding dye functionality
    def __add__(self, other): #  particleData1 + particleData2

        if type(other) != ParticleData: return TypeError

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

        return self

    def __iadd__(self, other): #  particleData1 += particleData2
        
        return self.__add__(other)

@dataclass
class PlottingData():

    ## Plot dimentions
    plotSimWidth = 1
    plotSimHeight = 1
    plotCenter = np.array([0,0])

    ## Plot flow map
    flowMapResolution = 400
    brokenStreamlines = False
    # colour = lambda x,y : np.sqrt(x**2 + y**2)
    cmap = 'autumn'
    backgroundAlpha = 1
    maxVelocity = 10
    minVelocity = -10