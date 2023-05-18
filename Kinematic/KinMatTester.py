import Kinematics as km
import sympy as sp
import math


"""
This file can calculate and verify kinematics calculations using the Kinematics class
"""


UR5Kin = km.Kinematics()
sp.init_printing()
t1, t2, t3, t4, t5, t6 = sp.symbols("t1, t2, t3, t4, t5, t6")

#Defining the DH-paramters of the UR5 robot
dh_params = [[0, 0, 0, t1],
             [90, 0, 0, t2-180],
             [0, 425, 0, t3],
             [0, 392, 109.3, t4],
             [-90, 0, 94.75, t5],
             [90, 0, 0, t6]
            ]

#Define the base and tool transformation matrices
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

#Setup the forward transformation matrix from the DH, base, and tool transformation matrices
UR5Kin.setDHParams(dh_params)
UR5Kin.addTransMatrix("T_base_0", T_base_0, 0)
UR5Kin.addTransMatrix("T_6_tool", T_6_tool, -1)

#Test the kinematics (can be compared to robodk)
matrix = UR5Kin.forward(values = [90, -80, 20, 30, 0, 0])
sp.pprint(matrix)
print()
sp.pprint(UR5Kin.MatrixToAngleAxis(matrix[0:3, 0:3]))