import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's IP address and port
server_address = (' 172.26.50.66', 53432)
sock.connect(server_address)

try:
    # Send data
    message = b'Hello, server!'
    sock.sendall(message)
    print('Sent:', message.decode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('Received:', data.decode())

finally:
    # Clean up the connection
    sock.close()
