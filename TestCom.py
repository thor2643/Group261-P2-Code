import bluetooth

server_address = ''  # leave blank to accept connections from any device
port = 1  # must match the port number on the sending device

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind((server_address, port))
sock.listen(1)

print("Waiting for connection...")

client_sock, client_info = sock.accept()
print("Accepted connection from", client_info)

while True:
    # receive data from sender
    data = client_sock.recv(1024)
    if data:
        # convert bytes to string and display the value received
        value = data.decode('utf-8')
        print("Received value:", value)

client_sock.close()
sock.close()
