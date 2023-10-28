import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set the display dimensions
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)

# Create the Pygame window
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Waving Background")

# Load your background image
background_image = pygame.image.load("pic/screenshot.png").convert()

# Define variables for the waving effect
amplitude = 20  # Adjust this value to control the amplitude of the wave
frequency = 0.02  # Adjust this value to control the frequency of the wave
offset = 0

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Calculate the y-offset for the waving effect
    offset += 1
    if offset > 360:
        offset = 0

    # Draw the background image with the waving effect
    for x in range(0, WIDTH, background_image.get_width()):
        for y in range(0, HEIGHT, background_image.get_height()):
            y_offset = amplitude * math.sin(frequency * (x + offset))
            screen.blit(background_image, (x, y + y_offset))

    # Update the display
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
