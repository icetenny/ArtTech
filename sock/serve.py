import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to a specific IP and port
server_ip = "localhost"
server_port = 12345
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(5)  # Allow up to 5 clients to queue for connection

print(f"Server is listening on {server_ip}:{server_port}")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Send a welcome message to the client
    response = "Welcome to the server!"
    client_socket.send(response.encode())

    # Receive data from the client
    data = client_socket.recv(1024)
    print(f"Received from client: {data.decode()}")

    # Close the client socket
    client_socket.close()
