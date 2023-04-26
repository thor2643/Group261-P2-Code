import robodk
from robodk import robomath
import time
import numpy as np

RDK = robodk.robolink.Robolink()

robot = RDK.Item('UR5')      # retrieve the robot by name
robot_base = RDK.Item('UR5 Base')      # retrieve the robot by name
ref_frame = RDK.Item('UR5 Base')

#Helps to choose an appropriate solution
default_config = [1, 2, 3]   #[REAR, LOWER-ARM UP, WRIST FLIP]

# Load a STEP file
path_to_cover_file = 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/Cover/CoverDispenserAssembled.step'
path_to_fuse_file = 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/Fuse/FuseTower.step'
path_to_pcb_file = 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/PCB/PCBDispenser.step'
path_to_gripper_file = 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Gripper/GripperAssembled.step'

paths = [path_to_cover_file, path_to_fuse_file, path_to_pcb_file, path_to_gripper_file]
names = ["BottomDispenserAssembled", "TopDispenser", "FuseTower", "PCBDispenser", "Gripper"]

item_list = RDK.ItemList(list_names=True)

#Import or get the dispensers
if names[0] not in item_list:
    bottom_dispenser = RDK.AddFile(paths[0], robot_base)
    bottom_dispenser.setName(names[0])
    top_dispenser = RDK.AddFile(paths[0], robot_base)
    top_dispenser.setName(names[1])
    fuse_dispenser = RDK.AddFile(paths[1], robot_base)
    pcb_dispenser = RDK.AddFile(paths[2], robot_base)
else:
    bottom_dispenser = RDK.Item(names[0])
    top_dispenser = RDK.Item(names[1])
    fuse_dispenser = RDK.Item(names[2])
    pcb_dispenser = RDK.Item(names[3])

# Retrieve the item's position and orientation
ref_pose = ref_frame.Pose()

#define radius and angular spacing between dispenser positions
radius = 500

top_angle = 0 * robomath.pi/180
fuse_angle = 30 * robomath.pi/180
pcb_angle = 60 * robomath.pi/180
bottom_angle = 90 * robomath.pi/180


# Change the pose of the item
bottom_pos = [robomath.cos(bottom_angle)*radius, robomath.sin(bottom_angle)*radius, 0]    # x, y, z coordinates in mm
bottom_orient = robomath.atan2(bottom_pos[1], bottom_pos[0])-(90*robomath.pi/180)  #-robomath.pi/2

pcb_pos = [robomath.cos(pcb_angle)*radius, robomath.sin(pcb_angle)*radius, 0]
pcb_orient = robomath.atan2(pcb_pos[1], pcb_pos[0])-(90*robomath.pi/180) #-robomath.pi/2 180+

fuse_pos = [robomath.cos(fuse_angle)*radius, robomath.sin(fuse_angle)*radius, 0] 
fuse_orient = robomath.atan2(fuse_pos[1], fuse_pos[0])-(90*robomath.pi/180) #-robomath.pi/2

top_pos = [robomath.cos(top_angle)*radius, robomath.sin(top_angle)*radius, 0]
top_orient = robomath.atan2(top_pos[1], top_pos[0])-(90*robomath.pi/180) #-robomath.pi/2


bottom_pose = ref_pose * robomath.transl(bottom_pos[0], bottom_pos[1], bottom_pos[2]) * robomath.rotz(bottom_orient) #robomath.TxyzRxyz_2_Pose(bottom_pos + [0,0,0]) 
bottom_pose = bottom_pose * robomath.transl(31,66, 0)

top_pose = ref_pose * robomath.transl(top_pos[0], top_pos[1], top_pos[2]) * robomath.rotz(top_orient) #* robomath.rotz(-robomath.pi/4) #robomath.TxyzRxyz_2_Pose(top_pos + [0,0, 0]) * robomath.rotz(-robomath.pi/4) #-robomath.pi/4])
top_pose = top_pose * robomath.transl(31,66, 0)

fuse_pose = ref_pose * robomath.transl(fuse_pos[0], fuse_pos[1], fuse_pos[2]) * robomath.rotz(fuse_orient)
fuse_pose = fuse_pose * robomath.transl(98.95, 18.3, 0) #* robomath.rotx(robomath.pi/2)

pcb_pose = ref_pose * robomath.transl(pcb_pos[0], pcb_pos[1], pcb_pos[2]) * robomath.rotz(pcb_orient) #robomath.TxyzRxyz_2_Pose(pcb_pos + [0,0, 0])
pcb_pose = pcb_pose * robomath.transl(20.6, 42.5, 0)


# update items' pose
bottom_dispenser.setPose(bottom_pose)           
top_dispenser.setPose(top_pose)
fuse_dispenser.setPose(fuse_pose)
pcb_dispenser.setPose(pcb_pose)


#Sets an offset from target to make an approach and leave point
#Note that it does not account for the angle of 22 degrees e.g. does not
#Offset ortogonally to the plane of the dispenser
approach_offset = robomath.transl(80, 0, 30)
leave_offset = robomath.transl(-80, 0, 30)

#Create targets by multiplying relevant transformation matrices to the dispernser pose
#The correct measurements is found in the file robot cell in fusion 360
bottom_dispenser_pose = bottom_dispenser.Pose()
bottom_to_target = robomath.transl(-31,-66,222.5)*robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) * robomath.rotz(robomath.pi/2)
bottom_target = bottom_dispenser_pose * bottom_to_target
bottom_target_approach = bottom_dispenser_pose * approach_offset * bottom_to_target * robomath.rotz(robomath.pi/4)
bottom_target_leave = bottom_dispenser_pose * leave_offset * bottom_to_target * robomath.rotz(-robomath.pi/4)


top_dispenser_pose = top_dispenser.Pose()
top_to_target = robomath.transl(-31,-66,222.5) * robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) *robomath.rotz(2*robomath.pi)  
top_target =  top_dispenser_pose * top_to_target  
top_target_approach = top_dispenser_pose * approach_offset * top_to_target * robomath.rotz(robomath.pi/4)
top_target_leave = top_dispenser_pose * leave_offset * top_to_target * robomath.rotz(-robomath.pi/4)


fuse_dispenser_pose = fuse_dispenser.Pose()
fuse_to_target = robomath.transl(-98.95, -18.3, 197.2)*robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) * robomath.rotz(3/2*robomath.pi)
fuse_target = fuse_dispenser_pose * fuse_to_target
fuse_target_approach = fuse_dispenser_pose * approach_offset * fuse_to_target * robomath.rotz(robomath.pi/4)
fuse_target_leave = fuse_dispenser_pose * leave_offset * fuse_to_target * robomath.rotz(-robomath.pi/4)


pcb_dispenser_pose = pcb_dispenser.Pose()
pcb_to_target = robomath.transl(-20.6, -42.5, 210.7)*robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) * robomath.rotz(robomath.pi)
pcb_target = pcb_dispenser_pose * pcb_to_target
pcb_target_approach = pcb_dispenser_pose * approach_offset * pcb_to_target * robomath.rotz(robomath.pi/4)
pcb_target_leave = pcb_dispenser_pose * leave_offset * pcb_to_target * robomath.rotz(-robomath.pi/4)


targets = [top_target_approach, top_target, top_target_leave, 
           fuse_target_approach, fuse_target, fuse_target_leave,
           pcb_target_approach, pcb_target, pcb_target_leave,
           bottom_target_approach, bottom_target, bottom_target_leave]

#generate target points in robodk
if "T1" not in RDK.ItemList(list_names=True):
    for i in range(len(targets)):
        target = RDK.AddTarget('T%i' % i, ref_frame)
        joints = robot.SolveIK_All(targets[i])

        #We want to choose the same config for all targets e.g. having the arm above the table
        for joint in joints:
            config_type = robot.JointsConfig(joint)
            conf = list(config_type)
            
            if conf == [[1.0, 0.0, 0.0, 0.0]]:
                target.setJoints(joint)
                break
        
        target.setAsJointTarget()
        
#Puts the robot in a default position           
robot.setJoints([-170, -60, 80, -75, 28, 260])

#Create the robodk program
program = RDK.AddProgram("Test program", robot)

# Very important: Make sure we set the reference frame and tool frame so that the robot is aware of it
program.setPoseFrame(ref_frame)
program.setPoseTool(robot.PoseTool())
program.setSpeed(20, 500)   #linear vel and joint vel

#Add the movement commands
for i in range(len(targets)):
    if (i+2) % 3 == 0:
        program.MoveL(RDK.Item(f"T{i}"))
    else:
        program.MoveJ(RDK.Item(f"T{i}"))

program.RunProgram()

