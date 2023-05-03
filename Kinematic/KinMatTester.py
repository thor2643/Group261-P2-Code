import Kinematics as km
import KinematicsSilas as kms
import sympy as sp
import math

UR5Kin = km.Kinematics()
UR5KinS = kms.KinematicsSilas()
sp.init_printing()
t1, t2, t3, t4, t5, t6 = sp.symbols("t1, t2, t3, t4, t5, t6")


dh_params = [[0, 0, 0, t1],
             [90, 0, 0, t2-180],
             [0, 425, 0, t3],
             [0, 392, 109.3, t4],
             [-90, 0, 94.75, t5],
             [90, 0, 0, t6]
            ]

T_base_0 = sp.Matrix([[1,  0,  0,   0],
                      [0,  1,  0,   0],
                      [0,  0,  1,  89.2],
                      [0,  0,  0,   1]
                    ])
T_6_tool = sp.Matrix([  [-1,  0,  0,   0],
                        [0,  -1,  0,   0],
                        [0,  0,  1,  82.5],
                        [0,  0,  0,   1]
                    ])

UR5Kin.declareForwardSymbols([t1, t2, t3, t4, t5, t6])
UR5Kin.setDHParams(dh_params)
t01 = UR5Kin.setDHParams(dh_params[0])
#t_0_1 = sp.Matrix(t01)
UR5Kin.addTransMatrix("T_base_0", T_base_0, 0)
UR5Kin.addTransMatrix("T_6_tool", T_6_tool, -1)



#matrix = UR5Kin.forward(values = [90, -80, 20, 30, 0, 0])
#sp.pprint(matrix)
#print()
#sp.pprint(matrix[0:3, 0:3])
print()
#sp.pprint(UR5Kin.MatrixToAngleAxis(matrix[0:3, 0:3]))

k = [0.3379, 0.4808, 0.8093, 21.8583*math.pi/180]#*math.pi/180]
r = UR5Kin.AngleAxisToMatrix(k)
#sp.pprint(r)
#print()
#sp.pprint(UR5Kin.MatrixToAngleAxis(r))


UR5KinS.getJointsFromPose([0,0,0,30,40,50])

