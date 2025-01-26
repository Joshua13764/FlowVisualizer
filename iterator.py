import numpy as np

from structs import SimFlowFuncs, ParticleData, SimSetupData

def iterateParticles(particleData : ParticleData, flowData : SimFlowFuncs, setupData : SimSetupData):

    # Run for each substep in the iteration
    for substep in range(setupData.subtimeSteps):

        # Find new velocities of particles for Cartesian coordinates
        # TODO check if proper Eular conversions

        particleData.particleVelocities[0,:] = flowData.vx(*particleData.particlePositions)
        particleData.particleVelocities[1,:] = flowData.vy(*particleData.particlePositions)

        # Iterate the positions
        particleData.particlePositions += particleData.particleVelocities * ( setupData.timeStep / setupData.subtimeSteps)