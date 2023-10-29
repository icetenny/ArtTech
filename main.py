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
import os
import shutil

# Initialize Pygame
pygame.init()

video = cv2.VideoCapture("pic/VAVSA_BG.mp4")
success, video_image = video.read()
fps = video.get(cv2.CAP_PROP_FPS)
print("fps:", fps)


# Constants for the window
WINDOW_WIDTH = video.get(3)
WINDOW_HEIGHT = video.get(4)
MAX_GHOST = 5

init_folder = "data/ghost/init"
spawning_folder = "data/ghost/spawning"
all_folder = "data/ghost/all"

# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600

# Colors
# BACKGROUND = (0, 0, 0)
start_time = time.time()

# Create the window
clock = pygame.time.Clock()
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("VAVSA 5lloween")
print(f"Width: {WINDOW_WIDTH}, Height: {WINDOW_HEIGHT}")

icon = pygame.image.load("pic/vavsa_logo.png")
pygame.display.set_icon(icon)

attractor = Attractor()

ghosts = AllGhost(screen=screen, window_size=(
    WINDOW_WIDTH, WINDOW_HEIGHT), attractor=attractor, max_ghosts=MAX_GHOST)

# ghosts.add_ghost(img_path="pic/ghost1.png", size=80, speed=5, effect=1)
# ghosts.add_ghost(img_path="pic/ghost2-1.png", size=75, speed=8, effect=1)
# ghosts.add_ghost(img_path="pic/ghost3.png", size=85, speed=4.5, effect=1)
# ghosts.add_ghost(img_path="pic/kitty.png", size=90, speed=2.5, effect=2)
# ghosts.add_ghost(img_path="pic/ghost3.png", size=85, speed=4.5, effect=2)
# ghosts.add_ghost(img_path="pic/ghost3.png", size=85, speed=4.5, effect=1)
# ghosts.add_ghost(img_path="pic/ghost3.png", size=85, speed=4.5, effect=1)



# Spawning first batch ghost
for sg in os.listdir(init_folder):
    # Open the JSON file for reading
    with open(os.path.join(init_folder, sg), 'r') as json_file:
        # Load the contents of the file into a Python dictionary
        ghost_data = json.load(json_file)
    if ghost_data.get("task") == "spawn":
        size = ghost_data["size"]
        speed = ghost_data["speed"]
        effect = ghost_data["effect"]
        image = np.array(ghost_data["img"])
        ghosts.add_ghost(img=image, size=size, speed=speed, effect=effect)

if len(os.listdir(all_folder)) <= MAX_GHOST:
    ags = os.listdir(all_folder)
else:
    ags = sorted(os.listdir(all_folder), reverse=True)[:MAX_GHOST]

for ag in ags:
    # Open the JSON file for reading
    with open(os.path.join(all_folder, ag), 'r') as json_file:
        # Load the contents of the file into a Python dictionary
        ghost_data = json.load(json_file)
    if ghost_data.get("task") == "spawn":
        size = ghost_data["size"]
        speed = ghost_data["speed"]
        effect = ghost_data["effect"]
        image = np.array(ghost_data["img"])
        ghosts.add_ghost(img=image, size=size, speed=speed, effect=effect)

# Main game loop
running = True
while running:
    clock.tick(fps)

    # Check spawing folder
    spawning_files = sorted(os.listdir(spawning_folder))

    # Check if the source directory is empty
    if spawning_files:
        first_spawning_file = os.path.join(spawning_folder, spawning_files[0])
        # Load the contents of the file into a Python dictionary
        try:
            with open(first_spawning_file, 'r') as json_file:
                spawning_ghost_data = json.load(json_file)
            json_file.close()
            if spawning_ghost_data.get("task") == "spawn":
                size = spawning_ghost_data["size"]
                speed = spawning_ghost_data["speed"]
                effect = spawning_ghost_data["effect"]
                image = np.array(spawning_ghost_data["img"])
                ghosts.add_ghost(img=image, size=size, speed=speed, effect=effect)

                # Move the first file to the destination directory
                shutil.move(first_spawning_file, all_folder)
        except Exception as e:
            print(e)
            pass

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

    # if attractor:
    #     pygame.draw.circle(screen, [(0, 255, 100), (200,0,20)][attractor.is_active], attractor.pos, 8)

    # Update the display
    # pygame.display.update()
    pygame.display.flip()


# Quit Pygame
pygame.quit()
