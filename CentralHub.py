import serial
import serial.tools.list_ports
import time
import threading
import socket
import csv
import os
#from GUI_OPERATOR import OperatorGUI

last_Line_Number = 0
data = True
dispense_Cycle_Time_Sec = 20

# - - - - - - - - - All initilization of the communication protocols and functions for connection - - - - - - - - - 

# Set up the serial connections
arduino_ser = serial.Serial()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific IP address and port - thors er '192.168.137.141'
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
            time.sleep(5) 


#Connects to the arduino and pc
Connect_To_Arduino()

# - - - - - - - - - All initilization of the .CSV document - - - - - - - - - 

line_Number = 0
start_Num = 3

# Define the file name and column headers
filename = ['OrderList.csv', 'StatusList.csv' ]
fieldnames = ['data'], ['data_s']

delete_File_1 = input("Do you want to delete the list of orders? (y/n)").lower() == 'y'
delete_File_2 = input("Do you want to delete the file containing the current inventory status? (y/n)").lower() == 'y'


# Delete the CSV file if it exists, and the delete_File variable is true
if delete_File_1 and os.path.exists(filename[0]):
    os.remove(filename[0])

if delete_File_2 and os.path.exists(filename[1]):
    os.remove(filename[1])

# Open the .csv files in 'append' mode and write the header row if the file is empty/none empty
for i in range(len(filename)):
    with open(filename[i], 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames[i])
        
        if os.path.exists(filename[i]) and os.stat(filename[i]).st_size > 0:
            # file exists and is not empty, do nothing
            pass
        else:
            # file does not exist or is empty, write header
            writer.writeheader()
            if i == 0:
                writer.writerow({'data': 0})
            else:
                writer.writerow({'data_s': 0})
                for i in range(7):
                    writer.writerow({'data_s': 0 })

            csvfile.seek(0)
    
def Update_Data_Row_Reached(line,File_Number):
    with open(filename[File_Number], 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_Injection = list(reader)
   
    # Replace the second row with new data. The data has to be a string. A comma seems to arrive when str() is used. Therefore this method is used.
    data_Injection[1] = str(line).replace(',', '')

    # Write the updated data back to the CSV file
    with open(filename[0], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_Injection)

def Update_Component_Status():
    with open(filename[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_Injection = list(reader)

    for i in range(7):
        data_Injection[i + 2] = '0'
    
    # Write the updated data back to the CSV file
    with open(filename[0], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_Injection)
    

def read_data_from_csv(File_Number, line_number):
    with open(filename[File_Number], 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        # Skip all rows until we reach the desired row number
        for i in range(line_number - 2):
            next(reader)
        
        # Check if there are more rows in the file
        try:
            row = next(reader)
            is_last_row = False
        except StopIteration:
            is_last_row = True
            row = []
       
        #An error occured, where an array where only ['3'] would be present would be passed. If this occours, it is set to empty. The rest of the code, can handle that gracefully.
        if row == ['3']:
            row = ''

        txt = row[0] if row else ''
        x = []
        if txt.strip():
            x = [int(num) for num in txt.split(', ')]

        # Adjust the line_number if there are more rows in the file
        line_number += 1 if not is_last_row else 0

    return x, line_number


#The next line of code will setup the documents, so that they are in a state ready to get the formated information.
#Find out what line number which the program reached last time it was run. In the document "data" is the header, and on line 2 the value of the last reached data line is found.
#The default value is 3, as the first two lines are occupied.
with open(filename[0], "r") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    row = next(reader)
    line_Number = int(row[0]) # There is a conversion error some place. That makes a double digits in the document become a comma separeted value  
  
Update_Data_Row_Reached(start_Num,0)



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

                    # Save the received data to the CSV file
                    with open(filename[0], 'a', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames[0])
                        writer.writerow({'data': data.decode()})
                    connection.sendall(data)

                else:
                    break
        finally:
            # Clean up the connection
            connection.close()

# - - - - - - - - - Main controller function and instantiation of the OperatorGUI - - - - - - - - -

def Main_controller(line_Number, last_Line_Number):
    last_Line_Number = line_Number
    
    phone_assembly, line_Number = read_data_from_csv(0, line_Number)
    
    if line_Number > last_Line_Number and phone_assembly:
        Double_Digit = Conversion_Arr_To_DD(phone_assembly)   
            
        for i in range(phone_assembly[3]):
            Send_To_Arduino(Double_Digit)
            time.sleep(dispense_Cycle_Time_Sec)
        
        Update_Data_Row_Reached(line_Number,0)
    else:
        #print('No new number')
        pass
    return line_Number, last_Line_Number

#GUIOperator = OperatorGUI()

# - - - - - - - - - Threading - - - - - - - - -

# Create a thread for receiving data from the PC
#GUI_Operator_thread = threading.Thread(target=GUIOperator.Run_Operator_GUI)
pc_thread = threading.Thread(target=Receive_From_Pc)

# Start thread
pc_thread.start()
#GUI_Operator_thread.start()

# - - - - - - - - - Main Code - - - - - - - - -
while True:
    #print('Main controller received this line number:' + str(line_Number))
    line_Number, last_Line_Number = Main_controller(line_Number, last_Line_Number)

#close the thread - This part of the code cannot be reached. This is on purpose, as we at all times want to have the server opened if the program is running. 
pc_thread.join()
#GUI_Operator_thread.join()