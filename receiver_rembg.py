import random
import math
import time
from custom_socket import CustomSocket
import socket
import json
import traceback
import numpy as np
import datetime
import os

spawning_folder = "data/ghost/spawning"

# HOST = socket.gethostname()
HOST = "192.168.228.125"
PORT = 10011

server = CustomSocket(HOST, PORT)
server.startServer(timeout=-1)

while True:
    # Accept a connection from a client
    conn, addr = server.sock.accept()
    print(f"Accepted connection from {addr}")

    # Send a welcome message to the client
    # response = "Welcome to the server!"
    # server.sendMsg(conn, response.encode())

    data = json.loads(server.recvMsg(conn))
    if data:
        current_time = datetime.datetime.now()

        # Format the current time as a string
        time_string = current_time.strftime("%H-%M-%S-%f")

        # Create a filename using the current time
        file_name = f"ghost_{time_string}.json"

        # Save the file
        with open(os.path.join(spawning_folder, file_name), 'w') as json_file:
            json.dump(data, json_file)

        print(f"File '{file_name}' created.")
        json_file.close()

    # Receive data from the client
    # data = server.recvMsg(conn)
    # print(f"Received from client: {data.decode()}")

    # Close the client socket
    conn.close()


