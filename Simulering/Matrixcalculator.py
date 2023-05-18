import robodk
from robodk import robomath



Matrix = robomath.transl(537.955,-94.856,206.472)*robomath.transl(0,0,-14)

#print(Matrix)


m1 = robomath.Mat([[    -0.369837,    -0.173191,     0.912812,   525.690408],
      [0.065916,    -0.984888,    -0.160159,   -92.303757],
      [0.926756,     0.000936,     0.375664,   196.034880],
      [0.000000,     0.000000,     0.000000,     1.000000 ]
])



Matrix = m1*robomath.transl(0,0,1)*robomath.transl(-9,0,0)

print(Matrix)


#RDK = robodk.robolink.Robolink()

#RDK.setRunMode(1)

#RDK.RunProgram("0 Fuses")