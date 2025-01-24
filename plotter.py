import matplotlib.pyplot as plt


from structs import ParticleData

def plotParticles(particleData : ParticleData):

    plt.scatter(*particleData.particlePositions)
    plt.show()