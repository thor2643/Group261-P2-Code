import RoboDKProgram
from robodk import robomath

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
names_angles = [[names[0], 0],
                [names[1], 30],
                [names[2], 60],
                [names[3], 90]]

simulation.set_in_circular_position(names_angles)

#Uncomment to create target points
simulation.create_dispenser_targetpoints(names)

prog_name = "Main program"
simulation.initialise_program(prog_name)

target_names = [name+" target" for name in names]
simulation.add_moveJ_from_targets(target_names)



#position = [100, 100, 0]

