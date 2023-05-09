# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project

# You can also use the new version of the API:
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

RDK = robolink.Robolink()

# Program example:
robot = RDK.Item("UR5")

robot.setParam("PAYLOAD", 0.5)


from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

RDK = robolink.Robolink()

# Notify user:
print('To edit this program:\nright click on the Python program, then, select "Edit Python script"')

robot = RDK.Item("UR5")
target1 = RDK.Item("Target 7")
target2 = RDK.Item("Target 30")
target3 = RDK.Item("Target 48")

RDK.setRunMode(5)

val1 = list(target1.Joints()[0])
val2 = list(target2.Joints()[0])
val3 = list(target3.Joints()[0])

done1 = False
done2 = False
done3 = False

robot.setDO(10, 0)
robot.setDO(11, 0)

r
# Program example:
while True:
    
    rob_pose = robot.Joints()
    
    if val1[0][0] >= val2[0][0] and not done1:
        RDK.ShowMessage("Turning on the gripper")
        robot.setDO(10, 1)
    elif val1[0][0] >= val2[0][0] and not done2:
        RDK.ShowMessage("Turning on the gripper")
        robot.setDO(11, 1)
    elif val1[0][0] >= val2[0][0] and not done3:
        RDK.ShowMessage("Turning on the gripper")
        robot.setDO(10, 0)
        break