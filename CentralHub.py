import serial
import time

# Set up the serial connection
ser = serial.Serial()

# Search for available serial ports
def find_serial_port():
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description:
            return p.device
        
def Append_Digits_To_Arduino(motor_num):
    if motor_num.isdigit():
        # Send the motor number to the Arduino
        ser.write(motor_num.encode())
    else:
        print("Invalid input!")

# Wait until an Arduino is found
while True:
    port = find_serial_port()
    if port:
        ser.port = port
        ser.baudrate = 9600
        ser.open()
        break
    else:
        print("No Arduino board found. Please make sure it is connected.")
        time.sleep(5)

#The beginning of out main code
while True:
    # Is is very important that the digits send, is contained within the following list, or the arduino will no do anything.
    # {0,4,5,6,10,14,15,16,20,24,25,26,30,34,35,36}
    Append_Digits_To_Arduino(20)



    