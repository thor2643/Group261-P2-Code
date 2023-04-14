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
joints1 = np.array([0, -90, -90, 0, 90, 0])
joints2 = np.array([78, -48, -150, -138, 265, 0])

#Create parabolic blend function
f1, t0, tf = TPPlanner.get2PointMoveLFunction(joints1, joints2, 400, 0, 0)

target = None

new_program = 1

if new_program:
    #Creat the robodk program
    program = RDK.AddProgram("Test program", robot)

    # Very important: Make sure we set the reference frame and tool frame so that the robot is aware of it
    program.setPoseFrame(ref_frame)
    program.setPoseTool(robot.PoseTool())
    program.setSpeed(100, 50, 1 1)   #linear vel and joint vel
    idx = 0

    #Divide the trajectory into 50 points
    for i in np.linspace(t0, tf, 100):

        joint_pose = list(f1(i))

        #target = RDK.AddTarget('T%i' % idx, ref_frame)
        #arget = target.setJoints(joint_pose)

        #print(target.Pose())
        # Add a linear movement (with the exception of the first point which will be a joint movement)
        if i == 0:
            program.MoveJ(joint_pose)
        else:
            program.MoveJ(joint_pose)

        idx += 1

program.RunProgram()