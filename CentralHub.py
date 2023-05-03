import serial
import serial.tools.list_ports
import time
import threading
import socket
import csv
import os

last_Line_Number = 0
data_write = False

# - - - - - - - - - All initilization of the communication protocols and functions for connection - - - - - - - - - 

# Set up the serial connections
arduino_ser = serial.Serial()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific IP address and port
server_address = ('192.168.137.141',53432)
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
            time.sleep(5) 


#Connects to the arduino and pc
Connect_To_Arduino()

# - - - - - - - - - All initilization of the .CSV document - - - - - - - - - 

line_Number = 0
start_Num = '3'

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
        writer.writerow({'data':1})

def Update_Data_Row_Reached(line):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_Injection = list(reader)
   
    # Replace the second row with new data
    data_Injection[1] = line

    # Write the updated data back to the CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_Injection)

def read_data_from_csv(filename, line_number):
    global data_write
    if (data_write):
        time.sleep(1)
    
    data_write = True
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        # Skip all rows until we reach the desired row number
        for i in range(line_number - 2):
            next(reader)
        # Return the data from the desired row
        row = next(reader)

        txt = row[0]
        x = [int(num) for num in txt.split(', ')]

        # Check if current row is the last row in the file
        is_last_row = True
        try:
            next(reader)
            is_last_row = False
        except StopIteration:
            is_last_row = True
            pass

    data_write = False

    if not is_last_row:
        line_number += 1

    line_Number = line_number

    return x, line_Number


#Find out what line number which the program reached last time it was run. In the document "data" is the header, and on line 2 the value of the last reached data line is found.
#The default value is 3, as the first two lines are occoupied.
with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    row = next(reader)
    line_Number = int(row[0])

Update_Data_Row_Reached(start_Num)

# - - - - - - - - - Function to convert array to "more" useful information. - - - - - - - - -

def Conversion_Arr_To_DD(array):
    #The array phone_assembly consist of 4 entries. The first (0) and the third (2) entries describe the corvers. 
    # If the value is 0 then it is black. If the value is 1 then it is white, and lastly the cover it blue if the value is 2 
    # We firstly handle the topcover

    d_1 = 0
    d_2 = 0

    try:
        if isinstance(array[0], int):
            match array[0]:
                case 0:
                    #black
                    d_1 = 10
                case 1:
                    #Blue
                    d_1 = 20
                case 2:
                    #White
                    d_1 = 30
        else:
            raise TypeError('Invalid input value for topcover')

        if isinstance(array[2], int):
            match array[2]:
                case 0:
                    #black
                    d_2 = 4
                case 1:
                    #Blue
                    d_2 = 5
                case 2:
                    #White
                    d_2 = 6
        else:
            raise TypeError('Invalid input value for bottomcover')

        # By multiplying these numbers a double digit is found which the arduino can translate to dispenser movement
        dd = d_1 + d_2

        return dd

    except (TypeError, IndexError):
        print('Invalid input values. The input array must contain 4 integers.') 

    
# - - - - - - - - - Function to append and receive data. From both the arduino, but also the PC - - - - - - - - -

# Function to send data to the Arduino
def Send_To_Arduino(Double_Digit):
    # Append digits to the Arduino
    # Make sure that the digits are contained within the following list or the Arduino won't do anything:
    # {0, 4, 5, 6, 10, 14, 15, 16, 20, 24, 25, 26, 30, 34, 35, 36}
    print(Double_Digit)
    arduino_ser.write(str(Double_Digit).encode())
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
                    if data_write:
                        time.sleep(1)

                    data_write = True
                    # Save the received data to the CSV file
                    with open(filename, 'a', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({'data': data.decode()})
                    connection.sendall(data)
                    data_write = False
                else:
                    break
        finally:
            # Clean up the connection
            connection.close()

def Main_controller(line_Number, last_Line_Number):
    phone_assembly, line_Number = read_data_from_csv(filename, line_Number)
    if line_Number > last_Line_Number:
        last_Line_Number = line_Number
        Double_Digit = Conversion_Arr_To_DD(phone_assembly)   

        for i in range(phone_assembly[3]):
            Send_To_Arduino(Double_Digit)
            time.sleep(2)   
    else:
        #print('No new number')
        pass
    return line_Number, last_Line_Number


# - - - - - - - - - Threading - - - - - - - - -

# Create a thread for receiving data from the PC
pc_thread = threading.Thread(target=Receive_From_Pc)

# Start thread
pc_thread.start()

# - - - - - - - - - Main Code - - - - - - - - -
while True:
    #print('Main controller received this line number:' + str(line_Number))
    line_Number, last_Line_Number = Main_controller(line_Number, last_Line_Number)

#close the thread
pc_thread.join()
