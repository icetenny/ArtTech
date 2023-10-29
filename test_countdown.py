import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT_SIZE = 300  # Change font size
FONT_COLOR = (0, 200, 200)  # Change font color to blue
COUNTDOWN_DURATION = 3  # Countdown duration in seconds
FPS = 30
font = pygame.font.Font(None, FONT_SIZE)

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Countdown")

# Load the font

countdown_status = False
# Function to display a countdown

# Control frame rate
clock = pygame.time.Clock()

# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not countdown_status:
                countdown_status = True
                start_time = time.time()
                end_time = start_time + COUNTDOWN_DURATION
                print(start_time, end_time)


    if countdown_status:
        if time.time() >= end_time:
            print(time.time(), end_time)
            print("BOOM")
            countdown_status = False

        else:
            print("here")
            screen.fill(WHITE)
            remaining_time = int(end_time - time.time())
            print(remaining_time)
            text = font.render(str(remaining_time), True, FONT_COLOR)  # Use new font size and color
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)


    pygame.display.flip()
    clock.tick(FPS)  # Control frame rate

# Quit Pygame
pygame.quit()
sys.exit()
