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

@dataclass
class RectangleDye():

    height : np.float64
    width : np.float64
    center : np.array
    shapeParticles : np.int64
    particleMass : np.float64

    def __post_init__(self):

        # Corners in clockwise formation starting from the bottom left 

        self.bottomLeft = self.center + np.array([- self.height, - self.width]) * 0.5
        self.topLeft = self.center + np.array([self.height, - self.width]) * 0.5
        self.topRight = self.center + np.array([self.height, self.width]) * 0.5
        self.bottomRight = self.center + np.array([- self.height, self.width]) * 0.5

    def getParticleData(self) -> ParticleData:

        # Loop through verticies
        particleData = LineDye(self.bottomLeft, self.topLeft, self.shapeParticles // 4, self.particleMass).getParticleData()
        particleData += LineDye(self.topLeft, self.topRight, self.shapeParticles // 4, self.particleMass).getParticleData()
        particleData += LineDye(self.topRight, self.bottomRight, self.shapeParticles // 4, self.particleMass).getParticleData()
        particleData += LineDye(self.bottomRight, self.bottomLeft, self.shapeParticles // 4, self.particleMass).getParticleData()

        # return particle data
        return particleData

@dataclass
class CircleDye():

    circleCenter : np.array
    circleRadius : np.float64
    shapeParticles : np.int64
    particleMass : np.float64

    def getParticleData(self) -> ParticleData:

        # Define particle data
        particleData = ParticleData()

        # Create points evenly as a function of theta
        evenPoints = np.linspace(0, 2 * np.pi, self.shapeParticles)

        # Distorbute these points around a circle
        particleData.particlePositions = np.row_stack(
            (self.circleRadius * np.cos(evenPoints) + self.circleCenter[0],
            self.circleRadius * np.sin(evenPoints) + self.circleCenter[1])
        )

        # Set other particle values
        particleData.particleVelocities = np.zeros((2, self.shapeParticles))
        particleData.particleMasses = np.zeros((2, self.shapeParticles))

        # return particle data
        return particleData