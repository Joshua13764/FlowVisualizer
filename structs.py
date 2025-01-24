from dataclasses import dataclass

@dataclass
class simulationPlotData():

    pass

@dataclass
class simFlowFuncs():

    ## Placeholder variables for the fields (Eulerian specification of the flow field)

    # Cartesian coordinates
    vX = None
    vY = None

    # Polar coodinates
    vr = None
    vtheta = None

@dataclass
class simSetupData():

    ## Simulation variables

    timeStep : float
    subtimeSteps = 4

    ## Plotting variables


    