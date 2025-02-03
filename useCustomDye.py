from dataclasses import dataclass
from structs import ParticleData

import numpy as np

@dataclass
class Dye():

    particlesData = ParticleData()

    # Private method to get a particle data object with data for a line of dye
    def _getLineDye(self,
            lineStart : np.array,
            lineEnd : np.array,
            lineParticles : np.int64,
            particleMass : np.float64) -> ParticleData:

        # Define particle data
        particleData = ParticleData()

        # Set particle values
        particleData.particlePositions = np.linspace(lineStart, lineEnd, lineParticles).T
        particleData.particleVelocities = np.zeros((2, lineParticles))
        particleData.particleMasses = np.zeros((2, lineParticles))

        # Return the created particle data
        return particleData

    # Private method to get a particle data object with data for a rectangle of dye
    def _getRectangleDye(self,
            height : np.float64,
            width : np.float64,
            center : np.array,
            shapeParticles : np.int64,
            particleMass : np.float64) -> ParticleData:
        
        # Corners in clockwise formation starting from the bottom left 
        bottomLeft = center + np.array([- height, - width]) * 0.5
        topLeft = center + np.array([height, - width]) * 0.5
        topRight = center + np.array([height, width]) * 0.5
        bottomRight = center + np.array([- height, width]) * 0.5

        # Loop through verticies
        particleData = self._getLineDye(bottomLeft, topLeft, shapeParticles // 4, particleMass)
        particleData += self._getLineDye(topLeft, topRight, shapeParticles // 4, particleMass)
        particleData += self._getLineDye(topRight, bottomRight, shapeParticles // 4, particleMass)
        particleData += self._getLineDye(bottomRight, bottomLeft, shapeParticles // 4, particleMass)

        # Return the created particle data
        return particleData

    # Private method to get a particle data object with data for a circle of dye
    def _getCircleDye(self,
            circleCenter : np.array,
            circleRadius : np.float64,
            shapeParticles : np.int64,
            particleMass : np.float64) -> ParticleData:
        
        # Define particle data
        particleData = ParticleData()

        # Create points evenly as a function of theta
        evenPoints = np.linspace(0, 2 * np.pi, shapeParticles)

        # Distorbute these points around a circle
        particleData.particlePositions = np.row_stack(
            (circleRadius * np.cos(evenPoints) + circleCenter[0],
            circleRadius * np.sin(evenPoints) + circleCenter[1])
        )

        # Set other particle values
        particleData.particleVelocities = np.zeros((2, shapeParticles))
        particleData.particleMasses = np.zeros((2, shapeParticles))

        # Return the created particle data
        return particleData
    
    # Returns the particle data
    def getParticleData(self):
        return self.particlesData

    # Add a line dye to the particles data
    def lineDye(self,
            lineStart : np.array,
            lineEnd : np.array,
            lineParticles : np.int64,
            particleMass : np.float64) -> None:
        self.particlesData += self._getLineDye(
            lineStart,
            lineEnd,
            lineParticles,
            particleMass
        )

    # Add a rectangle dye the particles data
    def rectangleDye(self,
            height : np.float64,
            width : np.float64,
            center : np.array,
            shapeParticles : np.int64,
            particleMass : np.float64) -> None:
        self.particlesData += self._getRectangleDye(
            height,
            width,
            center,
            shapeParticles,
            particleMass
        )

    # Add a circle dye the particles data
    def circleDye(self,
            circleCenter : np.array,
            circleRadius : np.float64,
            shapeParticles : np.int64,
            particleMass : np.float64) -> None:
        self.particlesData += self._getCircleDye(
            circleCenter,
            circleRadius,
            shapeParticles,
            particleMass
        )