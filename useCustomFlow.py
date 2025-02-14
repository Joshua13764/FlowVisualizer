from structs import SimFlowFuncs
import numpy as np

class Flow():

    def __init__(self):

        self.flowFunctions = {
            "cartesianFlow" : [],
            "polarFlow" : []
        }

    def cartesianFlow(self, relativeFlowFunctionX, relativeFlowFunctionY,
                      functionOffset = None):
        # Relative flow function must have form lambda x, y: some function

        if functionOffset:

            self.flowFunctions["cartesianFlow"].append({
                "vx" : lambda x, y : relativeFlowFunctionX(x - functionOffset[0], y - functionOffset[1]),
                "vy" : lambda x, y : relativeFlowFunctionY(x - functionOffset[0], y - functionOffset[1])
                })
            
        else:

            self.flowFunctions["cartesianFlow"].append({
                "vx" : lambda x, y : relativeFlowFunctionX(x,y),
                "vy" : lambda x, y : relativeFlowFunctionY(x,y)
                })
        
    def polarFlow(self, relativeFlowFunctionR, relativeFlowFunctionTheta,
                  functionOffsetCartesian = None, functionOffsetPolar = None):
        # Relative flow function must have form lambda r, theta: some function

        if functionOffsetCartesian:

            offsetR = lambda r, theta, xOff, yOff : np.sqrt(
                (r * np.cos(theta) + xOff) ** 2 + (r * np.sin(theta) + yOff) ** 2
            )
            offsetTheta = lambda r, theta, xOff, yOff : np.arctan(
                (r * np.sin(theta) + yOff) / (r * np.cos(theta) + xOff)
            )

            self.flowFunctions["polarFlow"].append({
                "vr" : lambda r, theta : relativeFlowFunctionR(
                    offsetR(r, theta, *functionOffsetCartesian), offsetTheta(r, theta, *functionOffsetCartesian)
                    ),
                "vtheta" : lambda r, theta : relativeFlowFunctionTheta(
                    offsetR(r, theta, *functionOffsetCartesian), offsetTheta(r, theta, *functionOffsetCartesian)
                )
                })
            
        elif functionOffsetPolar:
        
            self.flowFunctions["polarFlow"].append({
                "vr" : lambda r, theta : relativeFlowFunctionR(r - functionOffsetPolar[0], theta - functionOffsetPolar[0]),
                "vtheta" : lambda r, theta : relativeFlowFunctionTheta(r - functionOffsetPolar[0], theta - functionOffsetPolar[0])
                })
            
        else:
            self.flowFunctions["polarFlow"].append({
                "vr" : lambda r, theta : relativeFlowFunctionR(r, theta),
                "vtheta" : lambda r, theta : relativeFlowFunctionTheta(r, theta)
                })

    def getSimFlowFunc(self):

        simFlow = SimFlowFuncs()

        # Handle cartesianFlow
        if len(self.flowFunctions["cartesianFlow"]) != 0:
            def vxFunc(x,y):
                sumFlow = 0

                for flowFunc in self.flowFunctions["cartesianFlow"]:
                    sumFlow += flowFunc["vx"](x, y)
                return sumFlow
            
            def vyFunc(x,y):
                sumFlow = 0

                for flowFunc in self.flowFunctions["cartesianFlow"]:
                    sumFlow += flowFunc["vy"](x, y)
                return sumFlow
            
            simFlow.vx = vxFunc
            simFlow.vy = vyFunc

        # Handle polarFlow
        if len(self.flowFunctions["polarFlow"]) != 0:
            def vrFunc(r,theta):
                sumFlow = 0

                for flowFunc in self.flowFunctions["polarFlow"]:
                    sumFlow += flowFunc["vr"](r, theta)
                return sumFlow
            
            def vthetaFunc(r,theta):
                sumFlow = 0

                for flowFunc in self.flowFunctions["polarFlow"]:
                    sumFlow += flowFunc["vtheta"](r, theta)
                return sumFlow
            
            simFlow.vr = vrFunc
            simFlow.vtheta = vthetaFunc


        return simFlow



