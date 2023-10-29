import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radiation Effect")

# Create a new surface with transparency
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the surface
    surface.fill((0, 0, 0, 0))

    # Define the center point of the radiation effect
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # Create a simple radiation effect by adjusting the alpha based on distance from the center
    for x in range(WIDTH):
        for y in range(HEIGHT):
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            # Adjust the alpha based on the distance
            alpha = max(255 - distance, 0)
            color = (255, 0, 0, alpha)  # Red color with varying alpha
            surface.set_at((x, y), color)

    # Draw the surface on the screen
    screen.blit(surface, (0, 0))

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
