import cv2
from rembg import remove
import numpy as np
from custom_socket import CustomSocket
import socket
import json

l = []
for i in range(10):
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if cap.isOpened():
            if ret:
                l.append(i)
    except:
        pass
print(l)

if len(l) == 1:
    cap = cv2.VideoCapture(l[0])
else:
    cap = cv2.VideoCapture(int(input("Cam index: ")))


# # Check if the camera is opened successfully
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# # Create a window to display the webcam feed
# cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)


HOST = socket.gethostname()
PORT = 10012

server = CustomSocket(HOST, PORT)
server.startServer()

client_connected = False

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    if not client_connected:
        try:
            conn, addr = server.sock.accept()
            client_connected = True
            print("client connected")
        except:
            # print("No client connect")
            pass
    else:
        try:
            # Receive ghost from spawn gui
            data = json.loads(server.recvMsg(conn))
            if data:
                out = dict()

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

                out["size"] = rgba_image_rotated.shape[0]
                out["img"] = rgba_image_rotated.tolist()

                server.sendMsg(conn, json.dumps(out))
            else:
                server.sendMsg(conn, json.dumps(""))

        except Exception as e:
            # client_connected = False
            # traceback.print_exc()
            print(e)
            print("Connection Closed")
            client_connected = False


    # Display the frame in the "Webcam" window
    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1)

    # Press 'q' to exit the loop
    if key == ord('q'):
        break

# Release the VideoCapture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
