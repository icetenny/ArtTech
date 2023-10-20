import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trailing Image")
clock = pygame.time.Clock()
fps = 30
# Load the image with transparency
image = pygame.image.load("pic/ghost3.png")
image = pygame.transform.scale(image, (50, 50))  # Resize the image if needed

# List to store previous positions for the trail effect
trail_positions = []

# Main game loop
running = True
while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Append the current image position to the trail_positions list
    trail_positions.append((mouse_x, mouse_y))

    # Limit the trail length to avoid excessive images
    if len(trail_positions) > 20:
        trail_positions.pop(0)

    # Fill the screen with a background color
    screen.fill((0, 255, 255))

    for i, (x, y) in enumerate(trail_positions):
        alpha = int(255 * (i / len(trail_positions)))

        # Scale the image based on the position in the trail
        scale_factor = (i / len(trail_positions))
        trail_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))
        trail_image.set_alpha(alpha)

        # trail_image = image.copy()
        trail_image.fill((0, 0, 0, alpha), None, pygame.BLEND_RGBA_MULT)

        image_rect = trail_image.get_rect()
        image_rect.center = (x, y)
        screen.blit(trail_image, image_rect)

    # Draw the main image at the current mouse cursor position
    image_rect = image.get_rect()
    image_rect.center = (mouse_x, mouse_y)
    screen.blit(image, image_rect)

    # Update the screen
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
