import bluetooth

server_address = 'F8-A2-D6-BA-93-5E'  # replace with the MAC address of the receiving device
port = 1  # must match the port number on the receiving device

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((server_address, port))

while True:
    # get a double digit value from user
    value = input("Enter a double digit value (00-99): ")
    if len(value) == 2 and value.isdigit():
        # send the value as bytes
        sock.send(bytes(value, 'utf-8'))
    else:
        print("Invalid input, please enter a double digit value (00-99)")

sock.close()
