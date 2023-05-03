#import sys
#sys.path.append('C:\ProgramData\Anaconda3\Lib\site-packages')
import sympy as sp
from sympy import *
import numpy as np
import math


class KinematicsSilas:
    trans_mats = {}
    trans_order = []
    forwardMatrix = None
    forward_symbols = []

    theta_1, theta_2, theta_3, theta_4, theta_5, theta_6 = symbols("theta_1, theta_2, theta_3, theta_4, theta_5, theta_6")

    pi = 3.14159265359

    def setDHParams(self, dh_list):
        """
        Takes a sympy matrix (dh_list) where each row are the dh-parameters.
        The dh-variable (theta for the UR5) must be a symbolic sympy variable within the matrix.
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

    def getTransformationMatrix(self, alpha, a, d, theta):
        matrix = sp.Matrix([[sp.cos(theta*self.pi/180),  -sp.sin(theta*self.pi/180),  0,  a],
                                    [sp.sin(theta*self.pi/180)*sp.cos(theta*self.pi/180),  sp.cos(theta*self.pi/180)*sp.cos(alpha*self.pi/180),  -sp.sin(alpha*self.pi/180),  -sp.sin(alpha*self.pi/180)*d],
                                    [sp.sin(theta*self.pi/180)*sp.sin(alpha*self.pi/180), sp.cos(theta*self.pi/180)*sp.sin(alpha*self.pi/180),  sp.cos(alpha*self.pi/180),  sp.cos(alpha*self.pi/180)*d],
                                    [0, 0, 0, 1]
                                    ])
        return matrix


    def getJointsFromPose(self, pose):
        # DH parameters for UR5 robot
        DH_Params_UR5 = [[0,0,0,self.theta_1],[-pi/2,0,0,self.theta_2],[0,425,0,self.theta_3],[0,392.25,109.15,self.theta_4],[-pi/2,0,94.65,self.theta_5],[pi/2,0,0,self.theta_6]]
        #pose = [x, y, z, roll, pitch, yaw]


        pose_Transformation_Matrix = sp.Matrix([[cos(pose[4]) * sp.cos(pose[5]), sp.sin(pose[3]) * sp.sin(pose[4]) * sp.cos(pose[5]) - sp.cos(pose[3]) * sp.sin(pose[5]), sp.cos(pose[3]) * sp.sin(pose[4]) * sp.cos(pose[5]) + sp.sin(pose[3]) * sp.sin(pose[5]), pose[0]],
                                               [sp.cos(pose[4]) * sp.sin(pose[5]), sp.sin(pose[3]) * sp.sin(pose[4]) * sp.sin(pose[5]) + sp.cos(pose[3]) * sp.cos(pose[5]), sp.cos(pose[3]) * sp.sin(pose[4]) * sp.sin(pose[5]) - sp.sin(pose[3]) * sp.cos(pose[5]), pose[1]],
                                               [-sp.sin(pose[4]), sp.sin(pose[3]) * sp.cos(pose[4]), sp.cos(pose[3]) * sp.cos(pose[4]), pose[2]],
                                               [0, 0, 0, 1]])
        
        T_base_0 = sp.Matrix([[-1, 0, 0, 0],
                            [0, -1, 0, 0],
                            [0, 0, 1, 89.159],
                            [0, 0, 0, 1]])

        T_6_tool= sp.Matrix([[-1, 0, 0, 0],
                            [0, -1, 0, 0],
                            [0, 0, 1, 82.3],
                            [0, 0, 0, 1]])

        T06 = (T_base_0**-1) * (pose_Transformation_Matrix) * (T_6_tool**-1)
        T_0_6 = sp.Matrix(T06)

        a_2 = DH_Params_UR5[3][2]
        a_3 = DH_Params_UR5[4][2]
        d_4 = DH_Params_UR5[4][3]
        d_5 = DH_Params_UR5[5][3]

        r_11, r_21, r_31, r_12, r_22, r_32, r_13, r_23, r_33 = T_0_6[0,0], T_0_6[1,0], T_0_6[2,0], T_0_6[0,1], T_0_6[1,1], T_0_6[2,1], T_0_6[0,2], T_0_6[1,2], T_0_6[2,2]
        x_0_6, y_0_6, z_0_6 = T_0_6[0,3], T_0_6[1,3], T_0_6[2,3] 

        # theta 1 - two solutions
        theta_1_a = sp.atan2(y_0_6,x_0_6) + sp.acos(d_4/(sqrt(x_0_6**2+y_0_6**2)))-self.pi/2
        theta_1_b = sp.atan2(y_0_6,x_0_6) - sp.acos(d_4/(sqrt(x_0_6**2+y_0_6**2)))-self.pi/2

        # theta 5 - four solutions
        theta_5_a = sp.acos(-r_23*sp.cos(theta_1_a)+r_13*sin(theta_1_a)) # theta_1_a
        theta_5_b = -sp.acos(-r_23*sp.cos(theta_1_a)+r_13*sin(theta_1_a)) # theta_1_a

        theta_5_c = sp.acos(-r_23*sp.cos(theta_1_b)+r_13*sin(theta_1_b)) # theta_1_b
        theta_5_d = -sp.acos(-r_23*sp.cos(theta_1_b)+r_13*sin(theta_1_b)) # theta_1_b

        angles = [[theta_1_a,0,0,0,theta_5_a,0],
                 [theta_1_a,0,0,0,theta_5_a,0],
                 [theta_1_a,0,0,0,theta_5_b,0],
                 [theta_1_a,0,0,0,theta_5_b,0],
                 [theta_1_b,0,0,0,theta_5_c,0],
                 [theta_1_b,0,0,0,theta_5_c,0],
                 [theta_1_b,0,0,0,theta_5_d,0],
                 [theta_1_b,0,0,0,theta_5_d,0]]

        # theta 6 - four solutions
        for i in range(4):
            r21_T_1_6 = (r_21*sp.cos(angles[i][1]))-(r_11*sp.sin(angles[i][1]))/(sp.sin(angles[i][5]))
            r22_T_1_6 = (r_22*sp.cos(angles[i][1]))-(r_12*sp.sin(angles[i][1]))/(-sp.sin(angles[i][5]))
            th_6 = sp.atan2(r22_T_1_6,r21_T_1_6)
            angles[2*i-1][5] = th_6
            angles[2*i][5] = th_6

        # theta 3

        for i in range(4):
            T_0_1 = self.getTransformationMatrix(DH_Params_UR5[0][0],DH_Params_UR5[0][1],DH_Params_UR5[0][2],angles[i][0])
            T_4_5 = self.getTransformationMatrix(DH_Params_UR5[4][0],DH_Params_UR5[4][1],DH_Params_UR5[4][2],angles[i][4])
            T_5_6 = self.getTransformationMatrix(DH_Params_UR5[5][0],DH_Params_UR5[5][1],DH_Params_UR5[5][2],angles[i][5])
            T14 = (T_0_1**-1)*T_0_6*((T_4_5*T_5_6)**-1)
            T_1_4 = sp.Matrix(T14)

            x_1_4 = T_1_4[0,3]
            z_1_4 = T_1_4[2,3]
            
            angles[2*i-1][2] = sp.acos((x_1_4**2+z_1_4**2-a_2**2-a_3**2)/(2*a_2*a_3))
            angles[2*i][2] = -sp.acos((x_1_4**2+z_1_4**2-a_2**2-a_3**2)/(2*a_2*a_3))

        # theta 2
        for i in range(8):
            T2_0_1 = self.getTransformationMatrix(DH_Params_UR5[0][0],DH_Params_UR5[0][1],DH_Params_UR5[0][2],angles[i][0])
            T2_4_5 = self.getTransformationMatrix(DH_Params_UR5[4][0],DH_Params_UR5[4][1],DH_Params_UR5[4][2],angles[i][4])
            T2_5_6 = self.getTransformationMatrix(DH_Params_UR5[5][0],DH_Params_UR5[5][1],DH_Params_UR5[5][2],angles[i][5])

            T214 = (T2_0_1**-1)*T_0_6*(T2_4_5*T_5_6)**-1
            T2_1_4 = sp.Matrix(T214)
            x2_1_4 = T2_1_4[0,3]
            z2_1_4 = T2_1_4[2,3]
            angles[i][1] = sp.atan2(x2_1_4,z2_1_4) - sp.asin((a_3*sp.sin(angles[i][2]))/sp.sqrt(x2_1_4**2+z2_1_4**2))

        # theta 4
        for i in range(8):
            if (angles[i][1]).is_real == True and (angles[i][2]).is_real == True:
                T_1 = self.getTransformationMatrix(DH_Params_UR5[0][0],DH_Params_UR5[0][1],DH_Params_UR5[0][2],angles[i][0])
                T_2 = self.getTransformationMatrix(DH_Params_UR5[1][0],DH_Params_UR5[1][1],DH_Params_UR5[1][2],angles[i][1])
                T_3 = self.getTransformationMatrix(DH_Params_UR5[2][0],DH_Params_UR5[2][1],DH_Params_UR5[2][2],angles[i][2])
                T_5 = self.getTransformationMatrix(DH_Params_UR5[4][0],DH_Params_UR5[4][1],DH_Params_UR5[4][2],angles[i][4])
                T_6 = self.getTransformationMatrix(DH_Params_UR5[5][0],DH_Params_UR5[5][1],DH_Params_UR5[5][2],angles[i][5])
                
                T_3_4_ = (T_1*T_2*T_3)**-1*T_0_6*(T_5*T_6)**-1
                X_y_3_4 = T_3_4_[1,0] 
                X_x_3_4 = T_3_4_[0,0] 
                angles[i][3] = sp.atan2(X_y_3_4,X_x_3_4)
        
        return angles