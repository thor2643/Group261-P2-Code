import RoboDKProgram
from robodk import robomath


def activate_gripper(name):
    match name.lower():
        case "fuse":
            simulation.set_IO(0, 1)
            simulation.set_IO(1, 0)
        case "top":
            simulation.set_IO(0, 1)
            simulation.set_IO(1, 0)
        case "bottom":
            simulation.set_IO(0, 1)
            simulation.set_IO(1, 0)
        
    
names_paths = [["TopDispenser", 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/Cover/CoverDispenserAssembled.step'],
               ["FuseTower", 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/Fuse/FuseTower.step'],
               ["PCBDispenser", 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/PCB/PCBDispenser.step'],
               ["BottomDispenser", 'C:/Users/Thor9/OneDrive - Aalborg Universitet/Dokumenter/AAU\Projektarbejde/_P2 Projekt/Tegninger/Dispenser/Cover/CoverDispenserAssembled.step']]

simulation = RoboDKProgram.RoboDKProgram(ref_frame_name="Ref Frame")

#Uncomment to load files from pc
#simulation.load_dispensers_from_PC(names_paths)

#Retrieve items in robodk by name
names = [name_path[0] for name_path in names_paths]
simulation.load_dispensers_from_roboDK(names)

#Set offset matrices from dispener origin to TCP and correct orientation
name_matrices = [[names[0], robomath.transl(-31,-66,222.5) * robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) *robomath.rotz(2*robomath.pi)],
                 [names[1], robomath.transl(-98.95, -18.3, 197.2)*robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) * robomath.rotz(3/2*robomath.pi)],
                 [names[2], robomath.transl(-20.6, -42.5, 210.7)*robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) * robomath.rotz(robomath.pi)],
                 [names[3], robomath.transl(-31,-66,222.5)*robomath.rotx(-robomath.pi/2) * robomath.rotx(22*robomath.pi/180) * robomath.rotz(robomath.pi/2)]]

simulation.set_T_dispenser_TCP_offset(names_and_matrices=name_matrices)

#Change the dispenser positions to form a circular movement
radius = 550 #mm
names_angles = [[names[0], -35],
                [names[1], -10],
                [names[2], 10],
                [names[3], 35]]

simulation.set_in_circular_position(names_angles, radius=radius)

#Uncomment to create target points
simulation.create_dispenser_targetpoints(names)

prog_name = "Main program"
simulation.initialise_program(prog_name)

target_names = [name+" target" for name in names]
simulation.add_moveJ_from_targets(target_names)

TCP_assembly_position = [350, 0, 127.155] #127.155 comes is the TCP measured in fusion 360

#Offsets relative to TCP of bottom assembly target (found in fusion 360)
pcb_offset = [0.6, 0, 9.5]              #mm
fuse_offset = [-32.15, 1.75, -14.7]      #mm
top_offset = [0, 0, 14.7]               #mm 

approach_z_offset = robomath.transl(0,0,50)

orientation_z = robomath.atan2(TCP_assembly_position[1], TCP_assembly_position[0])-(90*robomath.pi/180)

bottom_assembly_pose = robomath.transl(TCP_assembly_position[0], TCP_assembly_position[1], TCP_assembly_position[2])*robomath.rotz(orientation_z)*robomath.rotx(-robomath.pi/2)*robomath.rotz(robomath.pi/2)
bottom_assembly_approach = approach_z_offset * bottom_assembly_pose

pcb_assembly_pose = robomath.transl(pcb_offset[0], pcb_offset[1], pcb_offset[2]) * bottom_assembly_pose * robomath.rotz(robomath.pi/2)   #robomath.transl(TCP_assembly_position[0]+pcb_offset[0], TCP_assembly_position[1]+pcb_offset[1], TCP_assembly_position[2]+pcb_offset[2])*robomath.rotz(orientation_z)*robomath.rotx(-robomath.pi/2)*robomath.rotz(robomath.pi)
pcb_assembly_approach = approach_z_offset * pcb_assembly_pose 

fuse_assembly_pose = robomath.transl(fuse_offset[0], fuse_offset[1], fuse_offset[2]) * bottom_assembly_pose * robomath.rotz(robomath.pi) #robomath.transl(TCP_assembly_position[0]+fuse_offset[0], TCP_assembly_position[1]+fuse_offset[1], TCP_assembly_position[2]+fuse_offset[2])*robomath.rotz(orientation_z)*robomath.rotx(-robomath.pi/2)*robomath.rotz(robomath.pi*3/2)
fuse_assembly_approach = approach_z_offset * fuse_assembly_pose 

top_assembly_pose = robomath.transl(top_offset[0], top_offset[1], top_offset[2]) * bottom_assembly_pose * robomath.rotz(robomath.pi* 3/2)   #robomath.transl(TCP_assembly_position[0]+top_offset[0], TCP_assembly_position[1]+top_offset[1], TCP_assembly_position[2]+top_offset[2])*robomath.rotz(orientation_z)*robomath.rotx(-robomath.pi/2)*robomath.rotz(robomath.pi*2)
top_assembly_approach = approach_z_offset * top_assembly_pose 

assembly_targets = []

assembly_targets.append(simulation.add_target(bottom_assembly_approach, "BottomAssemblyApproach", setAsjoint=False))
assembly_targets.append(simulation.add_target(bottom_assembly_pose, "BottomAssembly", setAsjoint=False))
assembly_targets.append(simulation.add_target(bottom_assembly_approach, "BottomAssemblyRetract", setAsjoint=False))

assembly_targets.append(simulation.add_target(pcb_assembly_approach, "PCBAssemblyApproach", setAsjoint=False))
assembly_targets.append(simulation.add_target(pcb_assembly_pose, "PCBAssembly", setAsjoint=False))
assembly_targets.append(simulation.add_target(pcb_assembly_approach, "PCBAssemblyRetract", setAsjoint=False))

assembly_targets.append(simulation.add_target(fuse_assembly_approach, "FuseAssemblyApproach", setAsjoint=False))
assembly_targets.append(simulation.add_target(fuse_assembly_pose, "FuseAssembly", setAsjoint=False))
assembly_targets.append(simulation.add_target(fuse_assembly_approach, "FuseAssemblyRetract", setAsjoint=False))

assembly_targets.append(simulation.add_target(top_assembly_approach, "TopAssemblyApproach", setAsjoint=False))
assembly_targets.append(simulation.add_target(top_assembly_pose, "TopAssembly", setAsjoint=False))
assembly_targets.append(simulation.add_target(top_assembly_approach, "TopAssemblyRetract", setAsjoint=False))



simulation.add_moveJ(assembly_targets[0])


"""
for i in range(len(assembly_targets)):
    if (i%3) == 0:
        simulation.add_moveJ(assembly_targets[i])
    else:
        simulation.add_moveL(assembly_targets[i])
"""
simulation.set_IO(0, 1)
simulation.set_IO(1, 1)

"""
bottom_target_approach = simulation.add_target(bottom_assembly_approach, "BottomAssemblyApproach", setAsjoint=False)
bottom_target = simulation.add_target(bottom_assembly_pose, "BottomAssembly", setAsjoint=False)
bottom_target_retract = simulation.add_target(bottom_assembly_approach, "BottomAssemblyRetract", setAsjoint=False)

pcb_target_approach = simulation.add_target(pcb_assembly_approach, "PCBAssemblyApproach", setAsjoint=False)
pcb_target = simulation.add_target(pcb_assembly_pose, "PCBAssembly", setAsjoint=False)
pcb_target_retract = simulation.add_target(pcb_assembly_approach, "PCBAssemblyRetract", setAsjoint=False)

fuse_target_approach = simulation.add_target(fuse_assembly_approach, "FuseAssemblyApproach", setAsjoint=False)
fuse_target = simulation.add_target(fuse_assembly_pose, "FuseAssembly", setAsjoint=False)
fuse_target_retract = simulation.add_target(fuse_assembly_approach, "FuseAssemblyRetract", setAsjoint=False)

top_target_approach = simulation.add_target(top_assembly_approach, "TopAssemblyApproach", setAsjoint=False)
top_target = simulation.add_target(top_assembly_pose, "TopAssembly", setAsjoint=False)
top_target_retract = simulation.add_target(top_assembly_approach, "TopAssemblyRetract", setAsjoint=False)


simulation.add_moveJ(bottom_target)
simulation.add_moveJ(pcb_target)
simulation.add_moveJ(fuse_target)
simulation.add_moveJ(top_target)



#position = [100, 100, 0]

"""