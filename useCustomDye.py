from dataclasses import dataclass
from structs import ParticleData

import numpy as np

@dataclass
class LineDye():

    lineStart : np.array
    lineEnd : np.array
    lineParticles : np.int64
    particleMass : np.float64

    def getParticleData(self) -> ParticleData:

        # Define particle data
        particleData = ParticleData()

        # Set particle values
        particleData.particlePositions = np.linspace(self.lineStart, self.lineEnd, self.lineParticles).T
        particleData.particleVelocities = np.zeros((2, self.lineParticles))
        particleData.particleMasses = np.zeros((2, self.lineParticles))

        # return particle data
        return particleData
