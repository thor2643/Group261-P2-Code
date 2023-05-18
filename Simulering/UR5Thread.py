from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

def activate_gripper(name):
    match name.lower():
        case "pcb":
            robot.set_DO(0, 1)
            robot.set_DO(1, 0)
        case "top":
            robot.set_DO(0, 0)
            robot.set_DO(1, 1)
        case "bottom":
            robot.set_DO(0, 1)
            robot.set_DO(1, 1)

RDK = robolink.Robolink()

# Notify user:
print('To edit this program:\nright click on the Python program, then, select "Edit Python script"')

# Program example:
while True:
    robot = RDK.Item("UR5")
    top_target = RDK.Item("TopDispenser target")
    pcb_target = RDK.Item("PCBDispenser target")
    bottom_target = RDK.Item("BottomDispenser target")

    bottom_assembly_target = RDK.Item("BottomAssembly target")
    pcb_assembly_target = RDK.Item("PCBAssembly target")
    top_assembly_target = RDK.Item("TopAssembly target")

    rob_pose = robot.Joints()

    val1 = list(rob_pose[0])
    val2 = list(top_target.Joints()[0])

    if int(val1[0][0]) == int(val2[0][0]):
        activate_gripper("top")

    if int(val1[0][0]) == int(val2[0][0]):
        activate_gripper("pcb")
    
    if int(val1[0][0]) == int(val2[0][0]):
        activate_gripper("bottom")

    
