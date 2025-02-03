## Aim
FlowVisualizer aims to allow users to view how the flow will deform fluid elements. This is done by allowing users to put a "dye" into a flow which they specify and then iterate the simulation foward in time to view the resulting deformation.

# How to use?

## Specifying the flow

This can currently be done by specifying the flow in the x and y directions separately.

```python
flowData = visualize.SimFlowFuncs()
flowData.vx = lambda x, y : x + 2 * y # (y + 0.001) / np.sqrt(x**2 + y**2)
flowData.vy = lambda x, y : - y # - (x + 0.001) / np.sqrt(x**2 + y**2)
```
Or can be done by using vectors (this includes support for polar coodinates).

```python
flowData = visualize.SimFlowFuncs()
flowData.v = lambda x,y,xHat,yHat, r,theta,rHat,thetaHat : thetaHat / np.linalg.norm(r)
```

## Specifying the dye

There are currently 3 primitive shapes to choose from LineDye, RectangleDye and CircleDye. The dyes can be combined by using either A + B or A += B logic.

Example of how this is done.

```python
from useCustomDye import RectangleDye, CircleDye

particleData = RectangleDye(0.2, 0.2, np.array([0,0]), 10000, 0).getParticleData()
particleData += RectangleDye(0.2, 0.2, np.array([0.2,0.3]), 10000, 0).getParticleData()
particleData += CircleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0).getParticleData()
```

## LineDye
Line dye can simulated by creating a particleData object using the getParticleData() method of LineDye (as seen in the example). The LineDye object takes the following arguments.

```python
    lineStart : np.array
    lineEnd : np.array
    lineParticles : np.int64
    particleMass : np.float64
```

## RectangleDye
Rectangle dye can simulated by creating a particleData object using the getParticleData() method of RectangleDye (as seen in the example). The RectangleDye object takes the following arguments.

```python
    height : np.float64
    width : np.float64
    center : np.array
    shapeParticles : np.int64
    particleMass : np.float64
```

## CircleDye
Circle dye can simulated by creating a particleData object using the getParticleData() method of CircleDye (as seen in the example). The CircleDye object takes the following arguments.

```python
    circleCenter : np.array
    circleRadius : np.float64
    shapeParticles : np.int64
    particleMass : np.float64
```

## Init the simulation
This is simply done by init of the class Visualizer.

Example of how this is done.

```python
# Setup the flow sim object
flowSim = visualize.Visualizer(
    setupData = visualize.SimSetupData(timeStep=0.01),
    flowData = flowData,
    particleData = particleData,
    plottingData = visualize.PlottingData()
)
```

## Run the simulation
The simulation can be ran by simply using the iterate method of flowSim i.e. ```flowSim.iterate(numbIter=20)```.

## Plot the results
The simulation results can be plotted by using the plot method of flowSim i.e. ```flowSim.plot()```.

## Overall example use case

```python
import numpy as np

import visualize

# Define the flow
flowData = visualize.SimFlowFuncs()
flowData.vx = lambda x, y : x + 2 * y # (y + 0.001) / np.sqrt(x**2 + y**2)
flowData.vy = lambda x, y : - y # - (x + 0.001) / np.sqrt(x**2 + y**2)

# Define the dye to put into the fluid
from useCustomDye import RectangleDye, CircleDye

particleData = RectangleDye(0.2, 0.2, np.array([0,0]), 10000, 0).getParticleData()
particleData += RectangleDye(0.2, 0.2, np.array([0.2,0.3]), 10000, 0).getParticleData()
particleData += CircleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0).getParticleData()

# Setup the flow sim object
flowSim = visualize.Visualizer(
    setupData = visualize.SimSetupData(timeStep=0.01),
    flowData = flowData,
    particleData = particleData,
    plottingData = visualize.PlottingData()
)

# Simulate the flow
flowSim.iterate(numbIter=20)
flowSim.plot()
```
