from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox

RDK = robolink.Robolink()

value = RDK.RunProgram(f"{phone_assembly[1]} Fuses", True) 

print(value)