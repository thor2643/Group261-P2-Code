import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_address = (' 172.26.50.66', 53432)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

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
                connection.sendall(data)
            else:
                break

    finally:
        # Clean up the connection
        connection.close()
