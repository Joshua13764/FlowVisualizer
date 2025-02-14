import numpy as np

from structs import SimFlowFuncs, ParticleData, SimSetupData


# Helper functions
_posToPol = lambda x, y : [
            np.sqrt(x ** 2 + y ** 2),
            np.arctan(y / x)
        ]

def _polVeltoCartVel(x, y, vr, vtheta):

    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan(y / x)

    return [
        vr * np.cos(theta) - r * vtheta * np.sin(theta),
        vr * np.sin(theta) + r * vtheta * np.cos(theta)
    ]

# Returns an array of poistions from flow data
def getVelocitiesFromPositions(postions : np.array, flowData : SimFlowFuncs) -> list:

    # Velocity in the x, y plane
    cartParticleVelocities = np.zeros(postions.shape)

    # Velocity in the r, theta plane
    polarParticleVelocities = np.zeros(postions.shape)

    # Cartesian coordinates
    if flowData.vx and flowData.vy:

        cartParticleVelocities[0,:] += flowData.vx(*postions)
        cartParticleVelocities[1,:] += flowData.vy(*postions)

    # Polar coordinates
    if flowData.vr and flowData.vtheta:

        # returns r, theta
        polarParticleVelocities[0,:] += flowData.vr(*_posToPol(*postions))
        polarParticleVelocities[1,:] += flowData.vtheta(*_posToPol(*postions))

    # Mixed coodinates
    if flowData.v:

        # Cartesian coordinates
        x = postions[0, :]
        y = postions[1, :]
        xHat = [np.ones(x.size), np.zeros(y.size)]
        yHat = [np.zeros(x.size), np.ones(y.size)]

        # Polar coordinates
        r = postions
        theta = np.arctan(y / x)
        rHat = postions / np.linalg.norm(postions)
        thetaHat = [- y, x] / np.linalg.norm(postions)

        # Calculate particleVelocities
        cartParticleVelocities += flowData.v(x,y,xHat,yHat, r,theta,rHat,thetaHat)
    
    # Return the found velocities
    return cartParticleVelocities, polarParticleVelocities

# Returns an array of poistions from flow data and converts all velocity types to cartesian
def getVelocitiesFromPositionsCartConverted(postions : np.array, flowData : SimFlowFuncs) -> np.array:

    # Find new velocities of particles
    cartParticleVelocities, polarParticleVelocities = getVelocitiesFromPositions(
        postions = postions,
        flowData = flowData
    )

    print(cartParticleVelocities)
    print(polarParticleVelocities)
    print(np.min(polarParticleVelocities[0]))

    # Get overall velocities
    particleVelocities = cartParticleVelocities
    particleVelocities += _polVeltoCartVel(*postions, *polarParticleVelocities)

    print(particleVelocities)

    return particleVelocities

def iterateParticles(particleData : ParticleData, flowData : SimFlowFuncs, setupData : SimSetupData):

    # Run for each substep in the iteration
    for substep in range(setupData.subtimeSteps):

        # Find new velocities of particles
        cartParticleVelocities, polarParticleVelocities = getVelocitiesFromPositions(
            postions = particleData.particlePositions,
            flowData = flowData
        )

        # Iterate the cartesian positions
        particleData.particlePositions += cartParticleVelocities * ( setupData.timeStep / setupData.subtimeSteps)

        # Iterate the Polar coordinates
        if flowData.vr and flowData.vtheta: # Use if for performance
            particlePositionsPolar = _posToPol(*particleData.particlePositions)
            particlePositionsPolar += polarParticleVelocities * ( setupData.timeStep / setupData.subtimeSteps)

        # Get overall velocities
        particleData.particleVelocities = cartParticleVelocities
        particleData.particleVelocities += _polVeltoCartVel(*particleData.particlePositions, *polarParticleVelocities)
