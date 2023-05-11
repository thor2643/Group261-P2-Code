import robodk
from robodk import robomath


"""
Matrix = robomath.transl(537.955,-94.856,206.472)*robomath.transl(0,0,-14)

#print(Matrix)


m1 = robomath.Mat([[    -0.369271,    -0.173533,     0.912976,   543.280793], 
      [0.065295,    -0.984828,    -0.160780,   -95.829534], 
      [0.927025,     0.000241,     0.374999,   193.131063], 
      [0.000000,     0.000000,     0.000000,     1.000000], ])


Matrix = m1*robomath.transl(0,0,-14)

print(Matrix)
"""

RDK = robodk.robolink.Robolink()

RDK.setRunMode(1)

RDK.RunProgram("0 Fuses")