import socket
from custom_socket import CustomSocket

HOST = socket.gethostname()
# HOST = "192.168.228.125"
PORT = 10011

client = CustomSocket(HOST, PORT)
client.clientConnect()

# Receive the welcome message from the server
welcome_msg = client.recvMsg(client.sock)
print(f"Server says: {welcome_msg.decode()}")

# Send a message to the server
message = "Hello, server!"
client.sendMsg(client.sock, message.encode())

# Close the client socket
client.clientDisconnect()
