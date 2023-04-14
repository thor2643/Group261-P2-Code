import robodk
from robodk import robomath
import time
import numpy as np

RDK = robodk.robolink.Robolink()

robot = RDK.Item('UR5')      # retrieve the robot by name
robot_base = RDK.Item('UR5 Base')      # retrieve the robot by name
ref_frame = RDK.Item('UR5 Base')

# Load a STEP file
path_to_step_file = 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/BottomCoverDispenser.step'

item_list = RDK.ItemList(list_names=True)

#Import or get the cover dispenser
if "BottomCoverDispenser" not in item_list:
    dispenser = RDK.AddFile(path_to_step_file, robot_base)
else:
    dispenser = RDK.Item("BottomCoverDispenser")

# Retrieve the item's position and orientation
pose = dispenser.Pose()

# Change the position of the item
new_position = [400, 500, 25]    # x, y, z coordinates in mm

pos = robomath.Mat([[ 1.000, 0.000, 0.000, new_position[0] ],
                [ 0.000, 1.000, 0.000, new_position[1] ],
                [ 0.000, 0.000, 1.000, new_position[2] ],
                [ 0.000, 0.000, 0.000, 1.000 ]])
dispenser.setPose(pos)           # update item's pose

target = dispenser.Pose()
target = target.setPos([target[0,3]-100, target[1,3]-10, target[2,3]+145]) #Offset op til telefon

# Get the position and orientation of the pose
pos_2 = robomath.Pose_2_TxyzRxyz(target)

# Change only the orientation
orient_new = [-68*robomath.pi/180, 0, robomath.pi/2] 
orient_approach = [-68*robomath.pi/180, 0, orient_new[2]+robomath.pi/4] 
orient_leave = [-68*robomath.pi/180, 0, orient_new[2]-robomath.pi/4] 
pose_new = robomath.TxyzRxyz_2_Pose(pos_2[0:3] + orient_new)

target_approach = robomath.TxyzRxyz_2_Pose([pos_2[0]+180, pos_2[1], pos_2[2]+100] + orient_approach)
target_leave = robomath.TxyzRxyz_2_Pose([pos_2[0]-180, pos_2[1], pos_2[2]+100] + orient_leave)  
print(robot.Valid())
robot.setPoseFrame(ref_frame)
robot.setJoints([45,-90,90,62,82,0])
robot.setSpeed(25, 10)
robot.MoveJ(target_approach)
robot.MoveL(pose_new)
robot.MoveL(target_leave)