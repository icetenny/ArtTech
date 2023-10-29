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

fps = 30

clock = pygame.time.Clock()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BACKGROUND = (200,200, 200)
start_time = time.time()

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("VAVSA 5lloween")
print(f"Width:{WINDOW_WIDTH} , Height:{WINDOW_HEIGHT}")

icon = pygame.image.load("pic/vavsa_logo.png")
pygame.display.set_icon(icon)

attractor = Attractor()

ghosts = AllGhost(screen=screen, window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), attractor=attractor, max_ghosts=5)

ghosts.add_ghost(img_path="pic/ghost1.png", size=80, speed=5, effect=1)
ghosts.add_ghost(img_path="pic/ghost2-1.png", size=75, speed=8, effect=1)
ghosts.add_ghost(img_path="pic/ghost3.png", size=85, speed=4.5, effect=1)
ghosts.add_ghost(img_path="pic/kitty.png", size=90, speed=2.5, effect=1)

# Main game loop
running = True
while running:
    clock.tick(fps) 
  
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

    screen.fill(BACKGROUND)

    # Move and draw each ghost
    ghosts.runall()
   
    if attractor:
        pygame.draw.circle(screen, [(0, 255, 100), (200,0,20)][attractor.is_active], attractor.pos, 8)

    # Update the display
    # pygame.display.update()
    pygame.display.flip()


# Quit Pygame
pygame.quit()
