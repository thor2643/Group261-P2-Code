import sympy as sp
import numpy as np
import math

class Kinematics:
    trans_mats = {}
    trans_order = []
    forwardMatrix = None
    forward_symbols = []

    pi = 3.14159265359

    def setDHParams(self, dh_list):
        """
        Takes a sympy matrix (dh_list) where each row are the dh-parameters.
        The dh-variale (theta for the UR5) must be a symbolic sympy variable within the matrix.
        """ 
        if self.forwardMatrix == None:
            for i in range(len(dh_list)):
                matrix = sp.Matrix([[sp.cos(dh_list[i][3]*self.pi/180),  -sp.sin(dh_list[i][3]*self.pi/180),  0,  dh_list[i][1]],
                                    [sp.sin(dh_list[i][3]*self.pi/180)*sp.cos(dh_list[i][0]*self.pi/180),  sp.cos(dh_list[i][3]*self.pi/180)*sp.cos(dh_list[i][0]*self.pi/180),  -sp.sin(dh_list[i][0]*self.pi/180),  -sp.sin(dh_list[i][0]*self.pi/180)*dh_list[i][2]],
                                    [sp.sin(dh_list[i][3]*self.pi/180)*sp.sin(dh_list[i][0]*self.pi/180),  sp.cos(dh_list[i][3]*self.pi/180)*sp.sin(dh_list[i][0]*self.pi/180),  sp.cos(dh_list[i][0]*self.pi/180),  sp.cos(dh_list[i][0]*self.pi/180)*dh_list[i][2]],
                                    [0, 0, 0, 1]
                                    ])
                self.trans_order.append(f"T_{i}_{i+1}")
                self.trans_mats[f"T_{i}_{i+1}"] = matrix

        final_matrix = sp.eye(4)
        for mat in self.trans_order:
            final_matrix *= self.trans_mats.get(mat)

        self.forwardMatrix = final_matrix

       
    def forward(self, values, symbols = "default"):
        """
        Calculates the forward kinematics and return the robots pose.

        If the symbols (theta variables) have been declared by "setForwardSymbols" this function takes the
        angle variables as a list (values). If symbols have not been declared the symbols param must be changed
        from "default" to a list containing the sympy symbolic variables used for the dh-matrix.
        """ 
        if symbols == "default":
            symbols = self.forward_symbols

        vals = [(sym, values) for sym, values in zip(symbols, values)]
        #print(vals)
        return self.forwardMatrix.subs(vals)  
    
    
    def declareForwardSymbols(self, syms):
        """
        Takes a list with symbol variables used for the dh-param-matrix and saves it as member to the class.
        This is necessary in order to substitute the symbolic variables of the forward transformation matrix
        with actual valued when calling "forward".
        """
        self.forward_symbols = syms
    
    def setForwardTransMatrix(self, matrix):
        self.forwardMatrix = matrix

    def addTransMatrix(self, name, matrix, idx):

        if idx == -1:
            self.trans_order.append(name)
        else:
            self.trans_order.insert(idx, name)

        self.trans_mats[name] = matrix
        #print(self.trans_order)
        final_matrix = sp.eye(4)
        for mat in self.trans_order:
            final_matrix *= self.trans_mats.get(mat)

        self.forwardMatrix = final_matrix

    def MatrixToAngleAxis(self, R_matrix):
        """
        Takes in an sympy or numpy rotational matrix and returns the angle-axis counterpart (sympy matrix)
        """
        angle = sp.acos((R_matrix[0,0]+R_matrix[1,1]+R_matrix[2,2]-1)/2)

        k = (1/(2*sp.sin(angle)))*sp.Matrix([   [R_matrix[2,1]-R_matrix[1,2]],
                                                [R_matrix[0,2]-R_matrix[2,0]],
                                                [R_matrix[1,0]-R_matrix[0,1]],
                                                [angle]
                                            ])
        return k

    def AngleAxisToMatrix(self, k):
        """
        Takes in an angle axis representation in the form [x, y, z, angle] and returns the matrix counterpart
        """
        R_matrix = sp.Matrix([  [k[0]*k[0]*(1-math.cos(k[3]))+math.cos(k[3]),  k[0]*k[1]*(1-math.cos(k[3]))-k[2]*math.sin(k[3]),  k[0]*k[2]*(1-math.cos(k[3]))+k[1]*math.sin(k[3])],
                                [k[0]*k[1]*(1-math.cos(k[3]))+k[2]*math.sin(k[3]),  k[1]*k[1]*(1-math.cos(k[3]))+math.cos(k[3]),  k[1]*k[2]*(1-math.cos(k[3]))-k[0]*math.sin(k[3])],
                                [k[0]*k[2]*(1-math.cos(k[3]))-k[1]*math.sin(k[3]),  k[1]*k[2]*(1-math.cos(k[3]))+k[0]*math.sin(k[3]),  k[2]*k[2]*(1-math.cos(k[3]))+math.cos(k[3])],
                            ])

        return R_matrix
