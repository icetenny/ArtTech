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
from rembg import remove
import cv2

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
    if data.get("task") == "spawn":
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
        
    elif data.get("task") == "rembg":
        frame = np.array(data.get("img"), dtype="uint8")
        output = remove(frame)
        non_empty_coordinates = np.argwhere(output[:, :, 3] > 0)
        x, y, w, h = cv2.boundingRect(non_empty_coordinates)

        cropped = output[x:x+w, y:y+h]
        side_length = max(cropped.shape[0], cropped.shape[1])

        square_image = np.zeros((side_length, side_length, 4), dtype=np.uint8)

        x_offset = (side_length - cropped.shape[1]) // 2
        y_offset = (side_length - cropped.shape[0]) // 2

        square_image[y_offset:y_offset+cropped.shape[0], x_offset:x_offset+cropped.shape[1]] = cropped

        b, g, r, a = cv2.split(square_image)

        # Merge the channels into RGBA format
        rgba_image = cv2.merge((r, g, b, a))
        rgba_image_rotated = np.transpose(rgba_image, (1, 0, 2))

        response = dict()
        response['img'] = rgba_image_rotated.tolist()

        server.sendMsg(conn, json.dumps(response))


    # Receive data from the client
    # data = server.recvMsg(conn)
    # print(f"Received from client: {data.decode()}")

    # Close the client socket
    conn.close()


