```python
import numpy as np

import visualize

# Define flow data
flowData = visualize.SimFlowFuncs()
flowData.vx = lambda x, y : x + 2 * y # (y + 0.001) / np.sqrt(x**2 + y**2)
flowData.vy = lambda x, y : - y # - (x + 0.001) / np.sqrt(x**2 + y**2)

# Define particle data
from useCustomDye import RectangleDye, CircleDye

particleData = RectangleDye(0.2, 0.2, np.array([0,0]), 10000, 0).getParticleData()
particleData += RectangleDye(0.2, 0.2, np.array([0.2,0.3]), 10000, 0).getParticleData()
particleData += CircleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0).getParticleData()

flowSim = visualize.Visualizer(
    setupData = visualize.SimSetupData(timeStep=0.01),
    flowData = flowData,
    particleData = particleData,
    plottingData = visualize.PlottingData()
)

flowSim.iterate(numbIter=20)
flowSim.plot()
```
