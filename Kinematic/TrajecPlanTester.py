import TrajectoryPlanning as tp
import sympy as sp
import numpy as np
import math


"""
This file is used to make and verify trajectory calculation using the TrajectoryPlanning class
"""


UR5 = tp.TrajectoryPlanner()

joints1 = np.array([42.98, -89.59, 125.57, -58.89, 74.26, 189.54])
joints2 = np.array([68.78, -89.74, 125.44, -58.6, 74.26, 96.54])

points = UR5.getJointPath(joints1, joints2)

for point in points:
    print(point)

#Parabolic blend from angle to angle
l1, t0, tf = UR5.get2PointMoveLFunction(15, 75, 0, 3, 10)
UR5.plot2DTrajectory(l1, t0, tf)

#Eksample of linear movement from pose1 to pose2 defined as [x, y, z, roll, pitch, yaw]
pose1 = np.array([289.48, 334.78, 818.21, 55.04, -20.95, 139.63])
pose2 = np.array([561.11, -71.56, 1010.43, -8.28, -55.2, 139.95])

l2, t0, tf = UR5.get2PointMoveLFunction(pose1, pose2, 100, 0, 0)
UR5.plot2DTrajectory(l2, t0, tf)
UR5.plot3DTrajectory(l2, t0, tf)

#Parabolic blend on two vector poses (in this case only the position)
#Minimum required accelearation is automatically calculated and used, but specific acceleration can also be given
l3, t0, tf = UR5.get2PointMoveLFunction(pose1[0:3], pose2[0:3], 0, 0, 10 ,"cb")
UR5.plot2DTrajectory(l3, t0, tf)
UR5.plot3DTrajectory(l3, t0, tf)

#Cubic polynomial with end velocity = 50 for each coordinate
l4, t0, tf = UR5.get2PointMoveLFunction(pose1[0:3], pose2[0:3], 0, 0, 10, "pb")#, 0, np.array([50, -50, 50]))
UR5.plot2DTrajectory(l4, t0, tf)
UR5.plot3DTrajectory(l4, t0, tf)

#Eksample of linear movement with via points from via_pose1, via_pose2, via_pose3, via_pose4 defined as [x, y, z, roll, pitch, yaw]
#Does only work with cubic polynomial for now
via_pose1 = np.array([289.48, 334.78, 1010.43, 55.04, -20.95, 139.63])
via_pose2 = np.array([561.11, -71.56, 1010.43, -8.28, -55.2, 139.95])
via_pose3 = np.array([1500, -71.56, 1500, -8.28, -55.2, 139.95])
via_pose4 = np.array([950, -400, 1200, -10, -90, 180])

points_list = [via_pose1, via_pose2, via_pose3, via_pose4]

#Information about the movement type between each point, where currently two movement types are supported:
#Cubic polynomial with tf, v0 and vf: [funcType, tf, v0, vf]
#Linear with an avg velocity: [funcType, avg_vel]
move_info = [["cb", 13, 0, 15], ["linear", 15], ["cb", 7, 15, 0]] #Cubicpolynomial

l5, t0, tf = UR5.getViaPointsMoveLFunction(points_list, move_info)
UR5.plot2DTrajectory(l5, t0, tf)
UR5.plot3DTrajectory(l5, t0, tf)

l5, t0, tf = UR5.get2PointMoveLFunction(via_pose2, via_pose3, 10, 0, 0, "linear")#, 0, np.array([50, -50, 50]))
UR5.plot2DTrajectory(l5, t0, tf)
UR5.plot3DTrajectory(l5, t0, tf)