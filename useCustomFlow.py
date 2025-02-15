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
            offsetTheta = lambda r, theta, xOff, yOff : np.arctan2(
                (r * np.sin(theta) + yOff),(r * np.cos(theta) + xOff)
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

    def streamFunctionFlow(self, streamFunction, functionOffset = None):
        # Adds a flow using a stream function

        compute_gradientX = lambda f, x, y, h=1e-5 : (f(x + h, y) - f(x - h, y)) / (2 * h)
        compute_gradientY = lambda f, x, y, h=1e-5 : (f(x, y + h) - f(x, y - h)) / (2 * h)
        
        if functionOffset:

            self.flowFunctions["cartesianFlow"].append({
                    "vx" : lambda x, y : compute_gradientY(streamFunction, x - functionOffset[0], y - functionOffset[1]),
                    "vy" : lambda x, y : - compute_gradientX(streamFunction, x - functionOffset[0], y - functionOffset[1])
                    })

        else:

            self.flowFunctions["cartesianFlow"].append({
                    "vx" : lambda x, y : compute_gradientY(streamFunction, x, y),
                    "vy" : lambda x, y : - compute_gradientX(streamFunction, x, y)
                    })

            



    # def complexPotential(complexPotentialFunction):
    #     # A complex potentail is such that the vx - ivy = d_z complexPotentialFunction
    #     # Since the complex potential function is a function of a single complex coodinate z
    #     # The imaginary part of the complex potential function is the stream function
    #     # which describes z = x + iy


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



