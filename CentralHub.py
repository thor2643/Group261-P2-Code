import serial
import serial.tools.list_ports
import time
import threading
import socket
import csv
import os

#Definition of our alarm and emergency stop parameters. The values are stored in arrays
component_Alarm_List = [5,41,5,5,5,5,5,5]
component_EStop_List = [0,0,0,0,0,0,0,0]

# - - - - - - - - - All initilization of the communication protocols and functions for connection - - - - - - - - - 

# Set up the serial connections
arduino_ser = serial.Serial()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific IP address and port - To make this code work, on AAU's wifi a group members pc
# is used as a router. Ip used: '192.168.137.141'
server_address = ('192.168.137.141',53432)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

# This function is used to find the serial port of the arduino. A library is used, which can help identify what port are available, and 
# which of those contain the search_key phrase. In this case Arduino will be passed as the search key.
def Find_Serial_Port(search_Key):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if search_Key in p.description:
            return p.device

# This function is used to connect to the arduino. When the port is identified, we can adjust the values and then connect to the serial.port
def Connect_To_Arduino():
    while True:
        port = Find_Serial_Port('Arduino')
        #Here we use 'port' as a boolean truth value. As python's interpreter interpret non-empties as true and empties as false
        if port:
            arduino_ser.port = port
            arduino_ser.baudrate = 9600
            #The serial port is opened
            arduino_ser.open()
            break
        else:
            # If a serial port is not found, it will wait 5 seconds and try again. Meaning the program is stuck in this loop until the port is found. 
            print("No Arduino board found. Please make sure it is connected.")
            time.sleep(5) 

# This function is used to receive data from the arduino. Specifically this function is used to keep the program from sending any signals
# To the dispenser trough the serial port until, the dispensing mechanism is ready to dispense again. 
def Receive_data_Arduino():
    # This function reads from the serial port, and only return true if the arduino outputs Proces complete!
    data = arduino_ser.readline().decode().strip()
    if data == "Process complete!":
        return True
    else:
        return False

# Here we establish a connection to the arduino
Connect_To_Arduino()

# - - - - - - - - - All initilization of the .csv document - - - - - - - - - 

#These variable are integers and are used to keep track of what phone was lasted produced and which should be produced next
last_Line_Number = 0
line_Number = 0

# This variable is used to initialize and setup the orderlist .csv document
start_Num = 3

# Definitions the file names and column headers for the .csv files
filename = ['OrderList.csv', 'StatusList.csv' ]
fieldnames = ['data'], ['data_s']

# Lets the user choose whether or not they want to delete the current files. In a updated version of the code, this feature should maybe be implemented in the operator
delete_File_1 = input("Do you want to delete the list of orders? (y/n)").lower() == 'y'
delete_File_2 = input("Do you want to delete the file containing the current inventory status? (y/n)").lower() == 'y'

# Delete the .csv file if it exists, and the delete_File variable is True
for i in range(2):
    if os.path.exists(filename[i]) and eval(f"delete_File_{i+1}"):
        os.remove(filename[i])

# Open the .csv files in 'append' mode and write the header row if the file is empty/none empty. Append mode in this case, means that we can add new rows, not remove old ones
# This is done to initialize the documents, if the are not existant or is missing a header. The for-loop will be run two times, as we have to files in this case
for i in range(len(filename)):
    # Document is opened in append mode
    with open(filename[i], 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames[i])
        
        # This if-statements is used to check if the file exist and if there is any information stored.
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
            #Reset the poiner of the document if it is either empty or non-existent
            csvfile.seek(0)

# The function is used to update what row is reached in the "Orderlist" document. In the order list document, the second line (starting from 1 not 0!) contains an whole number 
# which describes what array (order containing information about the phone ), which has to be produced next. It takes two inputs, the line which has been reached and what file it has to acces     
def Update_Data_Row_Reached(line,File_Number):
    with open(filename[File_Number], 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_Injection = list(reader)
   
    # Replace the second row with new data. The data has to be a string.
    data_Injection[1] = str(line)

    # Write the updated data back to the CSV file, by opening the docuement in write mode.
    with open(filename[0], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_Injection)

# This function is used to update the amount of components left. For it to work an array must be passed which contains information about the phone which has to be build.
def Update_Component_Status(Orderlist):
    # The document, StatusList, is opened to find out the how many components are available
    with open(filename[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_Injection = list(reader)
        
        # The for-loop iterates trough all the entries in the list, an converst them from comma separated values to an array with integers
        for i in range(len(data_Injection)):
            data_Injection[i] = str(data_Injection[i]).strip('[]').replace(",", "").replace("'", "").replace(" ", "")
        print(data_Injection)

        # The value of the PCB and Fuse component is subtracted with respectively 1 and the amount of fuses being taken.
        data_Injection[1] = str(int(data_Injection[1]) - 1)
        data_Injection[2] = str(int(data_Injection[2])- Orderlist[1] )

       # First a dictionary is defined, which is used to map Orderlist values to data_Injection indices. This is done to make sure that 1 is subtracted from the correct component values.
        indices = {0: 3, 1: 4, 2: 5}
        data_Injection[indices[Orderlist[0]]] = str(int(data_Injection[indices[Orderlist[0]]]) - 1)

        indices = {0: 6, 1: 7, 2: 8}
        data_Injection[indices[Orderlist[2]]] = str(int(data_Injection[indices[Orderlist[2]]]) - 1)

    # Write the updated data back to the .csv file
    with open(filename[1], 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_Injection)

# This function is used to check if enough components are available, and if a refill i needed, and alarm will be sent. Else a stop will be engaged if not enough components are available.
def Check_Component_status():
    with open(filename[1], 'r') as csvfile:
        reader = csv.reader(csvfile)
        component_list = list(reader)   


        #Check if there are any components left, if not then it will stop
        for i in range(len(component_Alarm_List)):
            if int(str(component_list[i+1]).strip('[]').replace("'","").replace(", ","")) <= component_EStop_List[i]:
                EStop = True
                break
            else:
                EStop = False

        #Check if there are any components left, if not then it will stop
        for i in range(len(component_Alarm_List)):
            if int(str(component_list[i+1]).strip('[]').replace("'","").replace(", ","")) < component_Alarm_List[i]:
                Alarm = True
                break
            else:
                Alarm = False
    return EStop, Alarm

# This function is used to read the arrays from the orderlist. I cannot be used to read the components list.
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

with open(filename[0], 'r') as csvfile:
    reader = csv.reader(csvfile)
    data_Injection = list(reader)

    # If the document is new, it will contain 0 on line two. If this is the case, it should be changed into 3. Which is the line where new data will begin.
    if data_Injection[1] == ['0']:
        Update_Data_Row_Reached(start_Num,0)

# This line of code updates the line number. If the program was run earlier it might be 8, the code would then save this value, and continue the production from there.
with open(filename[0], "r") as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    row = next(reader)
    line_Number = int(row[0]) 
  


# - - - - - - - - - Function to convert array to "more" useful information. - - - - - - - - -

def Conversion_Arr_To_DD(array):
    #The array phone_assembly consist of 4 entries. The first (0) and the third (2) entries describe the covers. 
    # If the value is 0 then it is black. If the value is 1 then it is blue, and lastly the cover it white if the value is 2 
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

        # By adding these numbers a double digit is found which the arduino can translate to dispenser movement sequence
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

# This function is used to receive data from the PC. This Function will run on an individual thread, meaning a server will always be open and ready to receive data
def Receive_From_Pc():
    while True:
        # Wait for a connection, with the specified IP
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

# - - - - - - - - - Main controller function - - - - - - - - -

#This function is the main function. It is here all the other functions are called when needed. This function takes two arguments as input
# The inputs in this case are the line number in the csv document, and the value of the last line number
def Main_controller(line_Number, last_Line_Number):
    #The last value of the line number is saved.
    last_Line_Number = line_Number
    
    # Then the read_data_from_csv funtion is called to can an order, being the array phone_assembly and the value for the line_number.
    # The same line number will be returned, if there is no new available data, and all the orders has been produced.
    phone_assembly, line_Number = read_data_from_csv(0, line_Number)
    
    # It is checked if it is a new order, meaning the line number is larger than the last line number and if phone_assebly is non-empty
    if line_Number > last_Line_Number and phone_assembly:
        # Based on the order, phone_assembly, a double digit is produced which will be send to the Arduino
        Double_Digit = Conversion_Arr_To_DD(phone_assembly)   

        # A for-loop is then used to iterate over this order as many times as is specified in the last entry of the array. 
        # Meaning that as many phones as is specified in the array will be made.    
        for i in range(phone_assembly[3]):
            # The Check_Component_status function is run, to see if enough available phone components are available and if a refill should be made.
            Estop, Alarm = Check_Component_status()
            
            # If a refill is needed and there is no emergency stop then a this will be printet
            if Alarm and not Estop:
                print('Components needs to be filled up. To find out which please check the operator GUI, or the dispensers')
            
            # If there is no emergency stop, then the production should continue as normal else if there is, a print will be made to show that the proces has stopped.
            if not Estop:
                # The status list is updated.
                Update_Component_Status(phone_assembly)
                # A double digit is send to the arduino, so it can start the dispensing sequence
                Send_To_Arduino(Double_Digit)


                #The program is keept inside the loop until the arduino sends back a message telling it has completed the process. 
                while not Receive_data_Arduino():
                    pass

                
                #Lastly the line number inside the csv document Orderlist is updated so the next phone in the list will be produced when called next time.
                Update_Data_Row_Reached(line_Number,0)
            else:
                print('A stop has been engaged, as there are not enough components to build a phone')
                break     
    else:
        #print('No new number')
        pass
    
    # The current and last line number is then returned, so they can be used in the next loop of the main function.
    return line_Number, last_Line_Number


# - - - - - - - - - Threading - - - - - - - - -

# Create a thread for receiving data from the PC
pc_thread = threading.Thread(target=Receive_From_Pc)

# Starts the thread
pc_thread.start()

# - - - - - - - - - Main loop - - - - - - - - -
while True:
    line_Number, last_Line_Number = Main_controller(line_Number, last_Line_Number)

#close the thread - This part of the code cannot be reached. This is on purpose, as we at all times want to have the server opened if the program is running. 
pc_thread.join()