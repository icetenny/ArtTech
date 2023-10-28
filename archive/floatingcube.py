import pygame
import random
import math
import time
from ghost import Ghost, AllGhost
from attractor import Attractor
# Initialize Pygame
pygame.init()

# Constants for the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
BACKGROUND = (0, 0, 0)

clock = pygame.time.Clock()

start_time = time.time()
# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Floating Ghosts")

attractor = Attractor()

ghosts = AllGhost(screen=screen, window_size=(WINDOW_WIDTH, WINDOW_HEIGHT), attractor=attractor)

ghosts.add_ghost(img="pic/ghost1.png", size=80, speed=0.05)
# ghosts.add_ghost(img="pic/ghost2-1.png", size=60, speed=0.035)

# Main game loop
running = True
while running:
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
    screen.fill(BACKGROUND)

    # Move and draw each ghost
    ghosts.runall()
    # print(ghosts.ghosts[0].status)
   
    if attractor:
        pygame.draw.circle(screen, (0, 255, 100), attractor.pos, 5)

    # Update the display
    pygame.display.update()

    dt = time.time() - start_time
    if dt > 0:
        fps = 1 / (time.time() - start_time)
        start_time = time.time()
        print("FPS: {:.2f}".format(fps))

# Quit Pygame
pygame.quit()
