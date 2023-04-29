import serial
import serial.tools.list_ports
import time
import threading
import socket
import csv
import os

# - - - - - - - - - All initilization of the communication protocols and functions for connection - - - - - - - - - 

# Set up the serial connections
arduino_ser = serial.Serial()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific IP address and port
server_address = ('192.168.0.229',53432)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

# Search for available serial ports
def Find_Serial_Port(search_Key):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if search_Key in p.description:
            return p.device

# Wait until the Arduino is found
def Connect_To_Arduino():
    while True:
        port = Find_Serial_Port('Arduino')
        if port:
            arduino_ser.port = port
            arduino_ser.baudrate = 9600
            arduino_ser.open()
            break
        else:
            print("No Arduino board found. Please make sure it is connected.")
            #time.sleep(5) - Uncomment, and remove the break under
            break


#Connects to the arduino and pc
Connect_To_Arduino()

# - - - - - - - - - All initilization of the .CSV document - - - - - - - - - 

line_Number = 0

# Define the file name and column headers
filename = 'OrderList.csv'
fieldnames = ['data']

delete_File = input("Do you want to delete the CSV file? (y/n)").lower() == 'y'

# Delete the CSV file if it exists, and the delete_File variable is true
if delete_File and os.path.exists(filename):
    os.remove(filename)

# Open the CSV file in 'append' mode and write the header row if the file is empty/none empty
with open(filename, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if os.path.exists(filename) and os.stat(filename).st_size > 0:
        # file exists and is not empty, do nothing
        pass
    else:
        # file does not exist or is empty, write header
        writer.writeheader()
        writer.writerow({'data': 3})

def Update_Data_Row_Reached(line):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(file)
        data_Injection = list(reader)
   
    # Replace the second row with new data
    data_Injection[1] = line

    # Write the updated data back to the CSV file
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_Injection)

def read_data_from_csv(filename, line_number):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        # Skip all rows until we reach the desired row number
        for i in range(line_number - 1):
            next(reader)
        # Return the data from the desired row
        row = next(reader)
        return row[0]

#Find out what line number which the program reached last time it was run. In the document "data" is the header, and on line 2 the value of the last reached data line is found.
#The default value is 3, as the first two lines are occoupied.
with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    row = next(reader)
    line_Number = int(row[0])

# - - - - - - - - - Function to append and recive data. From both the arduino, but also the PC - - - - - - - - -

# Function to send data to the Arduino
def Send_To_Arduino():
    #the code here is not complete. This could be done by another function like Data_Decoder
    line_data = read_data_from_csv(filename, line_Number)
    
    while True:
        # Append digits to the Arduino
        # Make sure that the digits are contained within the following list or the Arduino won't do anything:
        # {0, 4, 5, 6, 10, 14, 15, 16, 20, 24, 25, 26, 30, 34, 35, 36}
        arduino_ser.write(line_data.encode())
        time.sleep(1)

# Function to receive data from the PC
def Receive_From_Pc():
    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        print('Connected by', client_address)

        try:
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print('Received:', data.decode())
                if data:
                    # Save the received data to the CSV file
                    with open(filename, 'a', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({'data': data.decode()})
                    connection.sendall(data)
                else:
                    break
        finally:
            # Clean up the connection
            connection.close()

# - - - - - - - - - Threading - - - - - - - - -

# Create two threads for sending data to the Arduino and receiving data from the PC
arduino_thread = threading.Thread(target=Send_To_Arduino)
pc_thread = threading.Thread(target=Receive_From_Pc)

# Start both threads
arduino_thread.start()
pc_thread.start()

# Wait until both threads have completed
arduino_thread.join()
pc_thread.join()


# - - - - - - - - - Main Code - - - - - - - - -

Receive_From_Pc()



