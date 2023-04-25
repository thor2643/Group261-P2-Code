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

# Wait until an Arduino is found
while True:
    port = find_serial_port()
    if port:
        ser.port = port
        ser.baudrate = 9600
        ser.open()
        break


while True:
    # Get input from the user
    motor_num = input("Enter the motor number (1-6): ")
    if motor_num.isdigit() and 0 < int(motor_num) <= 6:
        # Send the motor number to the Arduino
        ser.write(motor_num.encode())
        time.sleep(17)
    else:
        print("Invalid input! Please enter a number between 1 and 6.")
