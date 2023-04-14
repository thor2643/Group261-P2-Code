import robodk
from robodk import robomath
import time
import numpy as np
RDK = robodk.robolink.Robolink()

robot = RDK.Item('UR5')      # retrieve the robot by name
robot.setJoints([0,-90,-90,0,90,90])      # set all robot axes to zero

target = [60,-90,-90,0,90,90]      # retrieve the Target item
target = RDK.Item('Target 1')
target = robomath.Mat([  [0.000000,    -0.866025,     0.500000,   331.906577],
                        [0.000000,     0.500000,     0.866025,   356.279054],
                        [-1.000000,    0.000000,     0.000000,   488.950000],
                        [0.000000,     0.000000,     0.000000,     1.000000 ]])
                
# Set the robot speed and acceleration
robot.setSpeed(100) # mm/s
robot.setAcceleration(100) # mm/s^2

target = RDK.Item('Target 1')

test_program = RDK.AddProgram("TestProg")
targets = []
for i in range(5):
    target = RDK.Item(f'Target {i+1}')
    target = target.Pose()
    targets.append(target.Pos())

#targets = [333, 356, 488], [403, 380, 824], [367, 207,500], [600, 256, 800]
#targets = robomath.Mat(targets)
#targets = robomath.tr(targets)
#print(targets)

#RDK.AddCurve([[333, 356, 488], [403, 380, 824], [367, 207,500], [600, 256, 800]])
#test_program.AddCurve(targets)

# Add a curve to the program
points = [[0, 0, 0], [100, 0, 0], [100, 100, 0], [0, 100, 0]]
curve = RDK.AddCurve(points)

# Generate a simulation of your program
test_program.AddCurve(curve)
test_program.RunProgram()