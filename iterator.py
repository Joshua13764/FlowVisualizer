import numpy as np

from structs import SimFlowFuncs, ParticleData, SimSetupData

# Returns an array of poistions from flow data
def getVelocitiesFromPositions(postions : np.array, flowData : SimFlowFuncs) -> np.array:

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
        particleVelocities = flowData.v(x,y,xHat,yHat, r,theta,rHat,thetaHat)

    # Cartesian coordinates
    elif flowData.vx and flowData.vy:

        particleVelocities = np.zeros(postions.shape)
        particleVelocities[0,:] = flowData.vx(*postions)
        particleVelocities[1,:] = flowData.vy(*postions)

    else:
        # There is no flowfunction(s) to use to simulate the flow
        raise ModuleNotFoundError
    
    # Return the found velocities
    return particleVelocities

def iterateParticles(particleData : ParticleData, flowData : SimFlowFuncs, setupData : SimSetupData):

    # Run for each substep in the iteration
    for substep in range(setupData.subtimeSteps):

        # Find new velocities of particles
        particleData.particleVelocities = getVelocitiesFromPositions(
            postions = particleData.particlePositions,
            flowData = flowData
        )

        # Iterate the positions
        # TODO 2 point acceleration
        particleData.particlePositions += particleData.particleVelocities * ( setupData.timeStep / setupData.subtimeSteps)