import robodk
from robodk import robomath
import numpy as np
import sys
sys.path.append('c:\\Users\\Thor9\\OneDrive - Aalborg Universitet\\Dokumenter\\AAU\\Projektarbejde\\P2-Code\\Kinematic')

import TrajectoryPlanning as tp

#Setup RoboDK
RDK = robodk.robolink.Robolink()
robot = RDK.Item('UR5')      # retrieve the robot by name
robot_base = RDK.Item('UR5 Base')      # retrieve the robot by name
ref_frame = RDK.Item('UR5 Base')

#Initiate an trajectory planning object
TPPlanner = tp.TrajectoryPlanner()

#Define the two positions
joints1 = np.array([52.87, -83.08, 119.4, -38.13, 88.11, 89.99])
joints2 = np.array([70.49, -83.08, 119.4, -38.13, 88.11, 0])
joints3 = np.array([90.63, -83.08, 119.4, -38.13, 88.11, -90])
joints4 = np.array([125.87, -83.08, 119.4, -38.13, 88.11, -180])

target_joints = [joints1, joints2, joints3, joints4]

#Information about the movement type between each point, where currently two movement types are supported:
#Cubic polynomial with tf, v0 and vf: [funcType, tf, v0, vf]
#move_info = [["linear", 15], ["linear", 15], ["linear", 15]] #Cubicpolynomial
move_info = [["linear", 15], ["linear", 15], ["linear", 15]]


f_via_points, t0, tf = TPPlanner.getViaPointsMoveLFunction(target_joints, move_info)

#Create parabolic blend function
#f1, t0, tf = TPPlanner.get2PointMoveLFunction(joints1, joints2, 100, 0, 0)

print(tf)
target = None

new_program = 0
via_program = 1

if via_program:
    program = RDK.AddProgram("Test program", robot)

    # Very important: Make sure we set the reference frame and tool frame so that the robot is aware of it
    program.setPoseFrame(ref_frame)
    program.setPoseTool(robot.PoseTool())

    #Divide the trajectory into 50 points
    idx = 0
    for i in np.linspace(t0, tf, 50):

        joint_pose = list(f_via_points(i))

        target = RDK.AddTarget(f'T{idx+5}', ref_frame)
        target = target.setJoints(joint_pose)
        target.setAsJointTarget()

        #print(target.Pose())
        # Add a linear movement (with the exception of the first point which will be a joint movement)
        if idx == 0:
            program.MoveJ(joint_pose)
        else:
            program.MoveL(target)
        
        idx += 1



if new_program:
    #Creat the robodk program
    program = RDK.AddProgram("Test program", robot)

    # Very important: Make sure we set the reference frame and tool frame so that the robot is aware of it
    program.setPoseFrame(ref_frame)
    program.setPoseTool(robot.PoseTool())
    program.setSpeed(1, 500)   #linear vel and joint vel
    idx = 0
    idx1 = 50


    #Divide the trajectory into 50 points
    for i in np.linspace(t0, tf, 35):

        joint_pose = list(f1(i))

        target = RDK.AddTarget('T%i' % idx, ref_frame)
        target = target.setJoints(joint_pose)
        target.setAsJointTarget()

        #print(target.Pose())
        # Add a linear movement (with the exception of the first point which will be a joint movement)
        if i == 0:
            program.MoveJ(joint_pose)
        else:
            program.MoveJ(target)

        idx += 1
        
        if idx<50:
            program.setSpeed(3000, 100)#idx/10)
        else:
            program.setSpeed(3000, 100)# idx1/10)
            idx1 -=1
    

program.RunProgram()