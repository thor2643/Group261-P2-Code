import robodk
from robodk import robomath
import time
import numpy as np



class RoboDKProgram:
    RDK = None
    robot = None
    robot_base = None
    ref_frame = None
    ref_pose = None
    program = None

    default_config = [[1.0, 0.0, 0.0, 0.0]]

    dispensers = {}
    T_dispenser_TCP = {}    #T=transformation matrix and TCP = tool center point


    def __init__(self, robot_name = 'UR5', robot_base_name = 'UR5 Base', ref_frame_name = 'UR5 Base'):
        """Initialises roboDK and retrieves the robot, robot base and reference fram"""

        self.RDK = robodk.robolink.Robolink()
        self.robot = self.RDK.Item(robot_name)                  # retrieve the robot by name
        self.robot_base = self.RDK.Item(robot_base_name)        # retrieve the robot base by name
        self.ref_frame = self.RDK.Item(ref_frame_name)
        self.ref_pose = self.ref_frame.Pose()

    def load_dispensers_from_PC(self, names_and_paths):
        """loads objects into robodk by giving a list with the paths to the file and a name, example: 
        [[C:/Users/Thor9/Drawings/Dispenser1.stp, "TopcoverDispenser"], [C:/Users/Thor9/Drawings/Dispenser2.stp, "FuseDispenser"]] """
        
        for name_and_path in names_and_paths:
            try:
                self.dispensers[name_and_path[0]] = self.RDK.AddFile(name_and_path[1], self.robot_base)
                self.dispensers[name_and_path[0]].setName(name_and_path[0])
            except:
                print("Could not load object. Try to check the file names")

    def load_dispensers_from_roboDK(self, names):
        """Takes a list of dispenser names as they are in robodk and loads them into the dispenser dictionary"""

        for name in names:
            try:
                self.dispensers[name] = self.RDK.Item(name)
                self.T_dispenser_TCP[name] = None
            except:
                print(f"No object with the name: {name}")
   
    def set_T_dispenser_TCP_offset(self, names_and_matrices):
        """Makes sure to create targets and position dispensers appropriately according to x, y, and z offsets and orientation,
        which could be found in CAD programs: 
        [["dispenser1", robomath.transl(-20.6, -42.5, 210.7)], ["dispenser2", robomath.rotx(22*robomath.pi/180)]]"""

        for name_matrix in names_and_matrices:
            self.T_dispenser_TCP[name_matrix[0]] = name_matrix[1]

    def set_in_circular_position(self, names_and_angles, radius = 500, radians = False):
        """Positions the dispensers in a circular pattern and makes them point towards the origin of the ref_frame.
        Radius: distance from origin to TCP 
        names_and_angles: list of lists with name of object and the angular position of the dispenser
        Radians: Choose whether to give angles in radians og degrees"""

        #Convert to radians
        if not radians:
            for i in range(len(names_and_angles)):
                names_and_angles[i][1] = names_and_angles[i][1] * robomath.pi/180
        
        for name_angle in names_and_angles:
            position = [robomath.cos(name_angle[1])*radius, robomath.sin(name_angle[1])*radius, 0]      # x, y, z coordinates in mm
            orientation = robomath.atan2(position[1], position[0])-(90*robomath.pi/180)                 #radians around the z-axis

            pose = self.ref_pose * robomath.transl(position[0], position[1], position[2]) * robomath.rotz(orientation)

            if self.T_dispenser_TCP[name_angle[0]]:
                pose = pose * robomath.transl(-self.T_dispenser_TCP[name_angle[0]][0, 3], -self.T_dispenser_TCP[name_angle[0]][1, 3], 0)

            self.dispensers[name_angle[0]].setPose(pose)

    def create_dispenser_targetpoints(self, names_in_order, configuration = None):
        """Creates targetpoints relative to the dispensers given by a list of robodk names """

        if not configuration:
            configuration = self.default_config

        prev_val = 360
        for name in names_in_order:
            dispenser_target = self.dispensers[name].Pose() * self.T_dispenser_TCP[name]

            target = self.RDK.AddTarget(name, self.ref_frame)
            joints = self.robot.SolveIK_All(dispenser_target)

            #We want to choose the same config for all targets e.g. having the arm above the table
            for joint in joints:
                config_type = self.robot.JointsConfig(joint)
                conf = list(config_type)
                
                if conf == configuration:
                    if joint[5] < prev_val:
                        target.setJoints(joint)
                        prev_val = joint[5]
                        break
            
            target.setAsJointTarget()

    def initialise_program(self, name):
        """Creates an empty program and configures it to use correct reference frames"""

        #Create the robodk program
        self.program = self.RDK.AddProgram(name, self.robot)

        #Set relevant frames
        self.program.setPoseFrame(self.ref_frame)
        self.program.setPoseTool(self.robot.PoseTool())

    def get_target_pose(self, name):
        return self.RDK.Item("name")