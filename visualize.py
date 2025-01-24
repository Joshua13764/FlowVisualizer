from dataclasses import dataclass
from structs import simFlowFuncs, simSetupData
import numpy

@dataclass
class Visualizer():

    # The data used to define the flow
    flowData : simFlowFuncs

    # The data used to setup how iterations run
    setupData : simSetupData

    

