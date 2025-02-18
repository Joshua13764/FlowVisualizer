import numpy as np
from numba import njit
from structs import SimFlowFuncs, ParticleData, SimSetupData


# Helper functions
def _posToPol(x, y): return [
    np.sqrt(x ** 2 + y ** 2),
    np.arctan2(y, x)
]


def _polToPos(r, theta): return np.array([
    r * np.cos(theta),
    r * np.sin(theta)
])


def _polVeltoCartVel(x, y, vr, vtheta):

    r = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)

    return [
        vr * np.cos(theta) - r * vtheta * np.sin(theta),
        vr * np.sin(theta) + r * vtheta * np.cos(theta)
    ]

# Returns an array of poistions from flow data


def getVelocitiesFromPositions(positions: np.array, flowData: SimFlowFuncs) -> list:

    # Velocity in the x, y plane
    cartParticleVelocities = np.zeros(positions.shape)

    # Velocity in the r, theta plane
    polarParticleVelocities = np.zeros(positions.shape)

    # Cartesian coordinates
    if flowData.vx and flowData.vy:

        cartParticleVelocities[0, :] += flowData.vx(*positions)
        cartParticleVelocities[1, :] += flowData.vy(*positions)

    # Polar coordinates
    if flowData.vr and flowData.vtheta:

        # returns r, theta
        polarParticleVelocities[0, :] += flowData.vr(*_posToPol(*positions))
        polarParticleVelocities[1,
                                :] += flowData.vtheta(*_posToPol(*positions))

    # Mixed coodinates
    if flowData.v:

        # Cartesian coordinates
        x = positions[0, :]
        y = positions[1, :]
        xHat = [np.ones(x.size), np.zeros(y.size)]
        yHat = [np.zeros(x.size), np.ones(y.size)]

        # Polar coordinates
        r = positions
        theta = np.arctan(y / x)
        rHat = positions / np.linalg.norm(positions)
        thetaHat = [- y, x] / np.linalg.norm(positions)

        # Calculate particleVelocities
        cartParticleVelocities += flowData.v(x,
                                             y, xHat, yHat, r, theta, rHat, thetaHat)

    # Return the found velocities
    return cartParticleVelocities, polarParticleVelocities

# Returns an array of poistions from flow data and converts all velocity types to cartesian


def getVelocitiesFromPositionsCartConverted(postions: np.array, flowData: SimFlowFuncs) -> np.array:

    # Find new velocities of particles
    cartParticleVelocities, polarParticleVelocities = getVelocitiesFromPositions(

        positions=postions,
        flowData=flowData
    )

    # Get overall velocities
    particleVelocities = cartParticleVelocities
    particleVelocities += _polVeltoCartVel(*postions, *polarParticleVelocities)

    return particleVelocities


def iterateParticles(particleData: ParticleData, flowData: SimFlowFuncs, setupData: SimSetupData):

    new_positions = particleData.positions[-1].copy()

    # Run for each substep in the iteration
    for _ in range(setupData.subtimeSteps):
        # Find new velocities of particles
        cartParticleVelocities, polarParticleVelocities = getVelocitiesFromPositions(
            positions=new_positions,
            flowData=flowData
        )

        # Iterate the cartesian positions
        new_positions += cartParticleVelocities * \
            (setupData.timeStep / setupData.subtimeSteps)

        # Iterate the Polar coordinates
        if flowData.vr and flowData.vtheta:  # Use if for performance
            particlePositionsPolar = _posToPol(*new_positions)
            particlePositionsPolar += polarParticleVelocities * \
                (setupData.timeStep / setupData.subtimeSteps)
            new_positions = _polToPos(*particlePositionsPolar)

        # Get overall velocities
        particleData.velocities = cartParticleVelocities

        if flowData.vr and flowData.vtheta:  # Use if for performance
            particleData.velocities += _polVeltoCartVel(
                *new_positions, *polarParticleVelocities)

    # Update particleData positions to have latest set
    particleData.positions = np.append(particleData.positions,
                                       np.expand_dims(new_positions, axis=0),
                                       axis=0)

    # Append the particle data to history
    particleData.positionHistory.append(new_positions)
