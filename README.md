## Aim
FlowVisualizer aims to allow users to view how the flow will deform fluid elements. This is done by allowing users to put a "dye" into a flow which they specify and then iterate the simulation foward in time to view the resulting deformation.

# How to use?

## Specifying the flow

There are currently 4 primitive flow types to choose from cartesianFlow, polarFlow, streamFunctionFlow and complexPotentialFlow. The flows can be added to a Flow object using the Flow class methods.

## cartesianFlow
Cartesian flow can simulated by using the method cartesianFlow on a Flow object (as seen in the example). The cartesianFlow method takes the following arguments.

```
    relativeFlowFunctionX : function with inputs x, y and a single output
    relativeFlowFunctionY : function with inputs x, y and a single output
    functionOffset = None : The offset of the flow from the origin
```

An example of this:

```python
flow.cartesianFlow(
    lambda x, y: - x,
    lambda x, y: y,
    (0.5, 0.5))
```

## polarFlow
Polar flow can simulated by using the method polarFlow on a Flow object (as seen in the example). The polarFlow method takes the following arguments.

```
    relativeFlowFunctionR : function with inputs r, theta and a single output
    relativeFlowFunctionTheta : function with inputs r, theta and a single output
    functionOffsetCartesian = None : The offset of the flow from the origin in cartesian coodinates
    functionOffsetPolar = None : The offset of the flow from the origin in polar coodinates
```

An example of this:

```python
flow.polarFlow(
    lambda r, theta: r * 0,
    lambda r, theta: 1 / r
)
```

## streamFunctionFlow
Stream function flow can simulated by using the method streamFunctionFlow on a Flow object (as seen in the example). The streamFunctionFlow method takes the following arguments.

```
    streamFunction : function with inputs x, y and a single output
    functionOffset = None : The offset of the flow from the origin
```

An example of this:

```python
flow.streamFunctionFlow(lambda x, y: x * y)
```

## complexPotentialFlow
Complex potential flow can simulated by using the method complexPotentialFlow on a Flow object (as seen in the example). The complexPotentialFlow method takes the following arguments.

```
    complexPotential : complex function with inputs z = x + iy and a single output
    functionOffset = None : The offset of the flow from the origin
```

An example of this:

```python
flow.complexPotentialFlow(
    lambda z: - np.log(z) / 1j,
    functionOffset=(-1, 0))
```

## Specifying the dye

There are currently 3 primitive shapes to choose from lineDye, rectangleDye and circleDye. The dyes can be added to a Dye object using the Dye class methods.

Example of how this is done.

```python
from useCustomDye import Dye

dye = Dye()
dye.rectangleDye(0.2, 0.2, np.array([0,0]), 10000, 0)
dye.rectangleDye(0.2, 0.2, np.array([0.2,0.3]), 10000, 0)
dye.circleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0)
```

## LineDye
Line dye can simulated by using the method lineDye on a Dye object (as seen in the example). The lineDye method takes the following arguments.

```python
    lineStart : np.array
    lineEnd : np.array
    lineParticles : np.int64
    particleMass : np.float64
```

An example of this:

```python
dye.lineDye(np.array([0, -1]), np.array([0, 1]), 10000, 0)
```

## RectangleDye
Rectangle dye can simulated by using the method Rectangle on a Dye object (as seen in the example). The Rectangle method takes the following arguments.

```python
    height : np.float64
    width : np.float64
    center : np.array
    shapeParticles : np.int64
    particleMass : np.float64
```

An example of this:

```python
dye.rectangleDye(0.2, 0.2, np.array([0, 0]), 10000, 0)
```

## CircleDye
Circle dye can simulated by using the method Circle on a Dye object (as seen in the example). The Circle method takes the following arguments.

```python
    circleCenter : np.array
    circleRadius : np.float64
    shapeParticles : np.int64
    particleMass : np.float64
```

An example of this:

```python
dye.circleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0)
```

## Init the simulation
This is simply done by init of the class Visualizer.

Example of how this is done.

```python
# Setup the flow sim object
flowSim = visualize.Visualizer(
    setupData = visualize.SimSetupData(timeStep=0.01),
    flowData = flowData,
    particleData = dye.getParticleData(),
    plottingData = visualize.PlottingData()
)
```

## Run the simulation
The simulation can be ran by simply using the iterate method of flowSim i.e. ```flowSim.iterate(numbIter=20)```.

## Plot the results
The simulation results can be plotted by using the plot method of flowSim i.e. ```flowSim.plot()```.

## Overall example use case

```python
from useCustomDye import Dye
import numpy as np

import visualize

# Define the flow
from useCustomFlow import Flow
flow = Flow()

flow.cartesianFlow(
    lambda x, y: - x,
    lambda x, y: y,
    (0.5, 0.5))

flow.cartesianFlow(
    lambda x, y: - y,
    lambda x, y: x,
    (0, 0))

flow.polarFlow(
    lambda r, theta: r * 0,
    lambda r, theta: 1 / r
)

flow.streamFunctionFlow(lambda x, y: x * y)

flow.complexPotentialFlow(lambda z: - np.log(z) / 1j, functionOffset=(-1, 0))
flow.complexPotentialFlow(lambda z: np.log(z) / 1j, functionOffset=(-1, -4))
flow.complexPotentialFlow(lambda z: np.log(z) / 1j, functionOffset=(1, 0))
flow.complexPotentialFlow(lambda z: - np.log(z) / 1j, functionOffset=(1, -4))

# Define the dye to put into the fluid
dye = Dye()

dye.lineDye(np.array([0, -1]), np.array([0, 1]), 10000, 0)
dye.rectangleDye(0.2, 0.2, np.array([0, 0]), 10000, 0)
dye.rectangleDye(0.2, 0.2, np.array([0.2, 0.3]), 10000, 0)
dye.circleDye(np.array([-0.2, -0.3]), 0.1, 10000, 0)

# Setup the flow sim object
flowSim = visualize.Visualizer(
    setupData=visualize.SimSetupData(timeStep=0.05),
    flowData=flow.getSimFlowFunc(),
    particleData=dye.getParticleData(),
    plottingData=visualize.PlottingData()
)

# Simulate the flow
flowSim.iterate(numbIter=20)
flowSim.plot()

```
