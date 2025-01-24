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
    subtimeSteps = 4

@dataclass
class ParticleData():

    ## Particle positions, velocity, mass (so can add drifing effects)
    particlePositions = np.array([0])
    particleVelocities = np.array([0])
    particleMasses = np.array([1])

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