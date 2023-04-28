import serial
import serial.tools.list_ports
import time
import threading

# Set up the serial connections
arduino_ser = serial.Serial()
pc_ser = serial.Serial()

# Search for available serial ports
def find_serial_port(search_Key):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if search_Key in p.description:
            return p.device

# Function to send data to the Arduino
def send_To_Arduino():
    while True:
        # Append digits to the Arduino
        # Make sure that the digits are contained within the following list or the Arduino won't do anything:
        # {0, 4, 5, 6, 10, 14, 15, 16, 20, 24, 25, 26, 30, 34, 35, 36}
        arduino_ser.write('20'.encode())
        time.sleep(1)

# Function to receive data from the PC
def receive_from_pc():
    while True:
        # Wait for data to be available on the PC serial port
        if pc_ser.in_waiting > 0:
            # Read the data from the PC and print it to the console
            data = pc_ser.readline().decode().strip()
            print("Received from PC: " + data)

# Wait until the Arduino is found
def connect_to_arduino():
    while True:
        port = find_serial_port('Arduino')
        if port:
            arduino_ser.port = port
            arduino_ser.baudrate = 9600
            arduino_ser.open()
            break
        else:
            print("No Arduino board found. Please make sure it is connected.")
            time.sleep(5)

# Wait until the PC serial port is found
def connect_to_pc():
    while True:
        port = find_serial_port('USB Transfer Cable')
        if port:
            pc_ser.port = port
            pc_ser.baudrate = 9600
            pc_ser.open()
            break
        else:
            print("No PC serial port found. Please make sure it is connected.")
            time.sleep(5)

# Create two threads for sending data to the Arduino and receiving data from the PC
arduino_thread = threading.Thread(target=send_To_Arduino)
pc_thread = threading.Thread(target=receive_from_pc)

# Start both threads
arduino_thread.start()
pc_thread.start()

# Wait until both threads have completed
arduino_thread.join()
pc_thread.join()

#Connects to the arduino and pc
connect_to_arduino()
connect_to_pc()

# The rest of the code goes here
while True:
    receive_from_pc()





