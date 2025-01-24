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