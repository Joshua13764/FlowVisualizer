from dataclasses import dataclass

import numpy

from structs import SimFlowFuncs, SimSetupData, ParticleData

@dataclass
class Visualizer():

    # The data used to define the flow
    flowData : SimFlowFuncs

    # The data used to setup how iterations run
    setupData : SimSetupData

    # The data used to store the particle infomation
    particleData : ParticleData