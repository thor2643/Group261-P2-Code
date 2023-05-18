import robodk
from robodk import robomath
import numpy as np
import math


#Matrix = robomath.transl(537.955,-94.856,206.472)*robomath.transl(0,0,-14)

#print(Matrix)

"""
m1 = robomath.Mat([[    -0.595476,     0.310757,    -0.740836,  -360.479080 ],
      [0.287176,    -0.778890,    -0.557549,  -271.217348],
     [-0.750292,    -0.544758,     0.374568,   224.956337 ],
     [ 0.000000,     0.000000,     0.000000,     1.000000 ]
])
"""

"""
Matrix = m1*robomath.transl(0,0,-50)

print(Matrix)

x_center = 210.39 #240.05
y_center = -279.70 #319.95

v_start = -36.95 * math.pi/180

points = []
for v in np.linspace(v_start, v_start-math.pi, 10):
      x = x_center + math.sin(v)*100
      y = y_center + math.cos(v)*100

      points.append([x,y])
      print([x,y])

"""

start_vel_lin = 20  
end_vel_lin = 330

start_vel_angular = 15 * math.pi/180

end_vel_angular = 191 * math.pi/180

for lin, ang in zip(np.linspace(start_vel_lin, end_vel_lin, 14), np.linspace(start_vel_angular, end_vel_angular, 14)):
      print([lin, ang])


print(3.333*180/math.pi)