import numpy as np

import visualize

# Define the flow
from useCustomFlow import Flow
flow = Flow()

# flow.cartesianFlow(lambda x, y : - x, lambda x, y : y, (0.5, 0.5))
# flow.cartesianFlow(lambda x, y : - y, lambda x, y : x, (0, 0))

flow.polarFlow(lambda r, theta : r, lambda r, theta : r * 0 + 1)

# Define the dye to put into the fluid
from useCustomDye import Dye

dye = Dye()
dye.lineDye(np.array([0,-1]), np.array([0,1]), 10000, 0)
# dye.rectangleDye(0.2, 0.2, np.array([0,0]), 10000, 0)
# dye.rectangleDye(0.2, 0.2, np.array([0.2,0.3]), 10000, 0)
# dye.circleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0)

# Setup the flow sim object
flowSim = visualize.Visualizer(
    setupData = visualize.SimSetupData(timeStep=0.01),
    flowData = flow.getSimFlowFunc(),
    particleData = dye.getParticleData(),
    plottingData = visualize.PlottingData()
)

# Simulate the flow
flowSim.iterate(numbIter=20)
flowSim.plot()