import numpy as np

import visualize

# Define the flow
flowData = visualize.SimFlowFuncs()
flowData.v = lambda x,y,xHat,yHat, r,theta,rHat,thetaHat : thetaHat / np.linalg.norm(r)

# Define the dye to put into the fluid
from useCustomDye import Dye

dye = Dye()
dye.rectangleDye(0.2, 0.2, np.array([0,0]), 10000, 0)
dye.rectangleDye(0.2, 0.2, np.array([0.2,0.3]), 10000, 0)
dye.circleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0)

# Setup the flow sim object
flowSim = visualize.Visualizer(
    setupData = visualize.SimSetupData(timeStep=0.01),
    flowData = flowData,
    particleData = dye.getParticleData(),
    plottingData = visualize.PlottingData()
)

# Simulate the flow
flowSim.iterate(numbIter=20)
flowSim.plot()