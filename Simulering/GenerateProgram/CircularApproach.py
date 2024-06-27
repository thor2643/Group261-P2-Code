import robodk
from robodk import robomath
import numpy as np
import sys
import math
sys.path.append('c:\\Users\\Thor9\\OneDrive - Aalborg Universitet\\Dokumenter\\AAU\\Projektarbejde\\P2-Code\\Kinematic')


#Setup RoboDK
RDK = robodk.robolink.Robolink()
robot = RDK.Item('UR5')                # retrieve the robot by name
robot_base = RDK.Item('UR5 Base')      # retrieve the robot by name
ref_frame = RDK.Item('UR5 Base')

x = np.array([5, 5])


#Define the two positions
Pos_A = np.array([350.000, 0, 171.855])
Rad_2 = math.sqrt(Pos_A[0]**2+Pos_A[1]**2)

#Pos_D = np.array([-277.606, -354.966, 227.579])
Pos_D = np.array([279.737, -353.289, 227.579])
theta_1 = math.atan2(Pos_D[1], Pos_D[0])

Pos_O = np.array([Rad_2*math.cos(theta_1), Rad_2*math.sin(theta_1), Pos_A[2]])

Pos_C = np.array([Pos_D[0]-(Pos_D[0]-Pos_O[0])/2,
                Pos_D[1]-(Pos_D[1]-Pos_O[1])/2,
                Pos_D[2]])

Rad_1 = math.sqrt(((Pos_D[0]-Pos_O[0])/2)**2+((Pos_D[1]-Pos_O[1])/2)**2)
t_max = 15
theta_0 = -math.pi + theta_1

def r(t):
    return Pos_C - np.array([Rad_1*math.cos((theta_0+(math.pi/t_max)*t)), Rad_1*math.sin((theta_0+(math.pi/t_max)*t)), ((Pos_D[2]-Pos_A[2])/t_max)*t])



#pose_D = robomath.Mat([[-0.787870,    -0.232451,    -0.570287,  -277.605646],
#                        [0.615840,    -0.295618,    -0.730309,  -354.966402], 
#                        [0.001174,    -0.926594,     0.376061,   227.579214], 
#                        [0.000000,     0.000000,     0.000000,     1.000000]])
pose_D = robomath.Mat([[0.232670,     0.783834,     0.575733,   279.736722],
                        [-0.295446,     0.620969,    -0.726023,  -353.289411], 
                        [-0.926594,    -0.001174,     0.376061,   227.579214 ], 
                        [0.000000,     0.000000,     0.000000,     1.000000]])


pose_D.setPos(r(0))

idx = 300

for t in range(t_max+1):
    target = RDK.AddTarget(f'T{idx}', ref_frame)
    pose = pose_D.setPos(r(t))
    target = target.setPose(pose_D)
    idx+=1