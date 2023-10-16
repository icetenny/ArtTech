import socket
import cv2
from custom_socket import CustomSocket
import time
host = socket.gethostname()
port = 10011
c = CustomSocket(host, port)
c.clientConnect()
i = 0
while True:
    # input()
    c.sendMsg(c.sock, str(i).encode("utf-8"))
    print("sending", i)
    i += 1
    # time.sleep(1)
