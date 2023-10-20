import pygame
import random
import math
import time
import cv2
from ghost import Ghost, AllGhost
from attractor import Attractor
from custom_socket import CustomSocket
import socket
import json
import traceback
import numpy as np

# Initialize Pygame
pygame.init()

HOST = socket.gethostname()
PORT = 10011

server = CustomSocket(HOST, PORT)
server.startServer()

video = cv2.VideoCapture("pic/bg2.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
print("fps:", fps)

clock = pygame.time.Clock()

# Constants for the window
WINDOW_WIDTH = video.get(3)
WINDOW_HEIGHT = video.get(4)

# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600

# Colors
# BACKGROUND = (0, 0, 0)
start_time = time.time()

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Floating Ghosts")

attractor = Attractor()

ghosts = AllGhost(screen=screen, window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), attractor=attractor)

ghosts.add_ghost(img_path="pic/ghost1.png", size=80, speed=5)
ghosts.add_ghost(img_path="pic/ghost2-1.png", size=75, speed=8)
ghosts.add_ghost(img_path="pic/ghost3.png", size=85, speed=4.5)
ghosts.add_ghost(img_path="pic/kitty.png", size=90, speed=2.5)


client_connected = False

# Main game loop
running = True
while running:
    clock.tick(fps) 

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
            data = json.loads(server.recvMsg(conn))
            if data:
                print(data)
                size = data["size"]
                speed = data["speed"]
                image = np.array(data["img"])
 
                ghosts.add_ghost(img=image, size=size, speed=speed)

            server.sendMsg(conn, json.dumps("message received"))

        except Exception as e:
            # client_connected = False
            # traceback.print_exc()
            print(e)
            print("Connection Closed")
            client_connected = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                attractor.pos = event.pos
                attractor.is_active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                attractor.is_active = False
        elif event.type == pygame.MOUSEMOTION:
            attractor.pos = event.pos  # Update circle position based on mouse cursor

    # Fill the background
    success, video_image = video.read()
    if success:
        video_surf = pygame.image.frombuffer(
            video_image.tobytes(), video_image.shape[1::-1], "BGR")
    else:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, video_image = video.read()
    screen.blit(video_surf, (0, 0))
    # screen.fill(BACKGROUND)

    # Move and draw each ghost
    ghosts.runall()
    # print(ghosts.ghosts[0].status)
   
    if attractor:
        pygame.draw.circle(screen, [(0, 255, 100), (200,0,20)][attractor.is_active], attractor.pos, 8)

    # Update the display
    # pygame.display.update()
    pygame.display.flip()


# Quit Pygame
pygame.quit()
