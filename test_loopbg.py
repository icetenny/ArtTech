import pygame
import os
import time

# Initialize Pygame
pygame.init()

# Set the screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the folder path containing your background images
background_folder = "pic/new_backgrounds"

# List all image files in the folder
background_files = [os.path.join(background_folder, filename) for filename in os.listdir(background_folder) if filename.endswith(".png")]
print(background_files)

# Load the images
background_images = [pygame.transform.scale(pygame.image.load(file), (WIDTH, HEIGHT)) for file in background_files]
fade_images = [image.copy() for image in background_images]

# Set initial opacity
for img in fade_images:
    img.set_alpha(0)

# Initialize variables for controlling image loop
image_index = 0
last_image_change = time.time()
image_change_interval = 10  # Change the image every 10 seconds
fade_duration = 5  # Duration of the fade effect in seconds

running = True

clock = pygame.time.Clock()

bg_status = "static"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate elapsed time since the last image change
    current_time = time.time()
    time_elapsed = current_time - last_image_change

    if bg_status == "static":
        fade_images[image_index].set_alpha(255)
        screen.blit(fade_images[image_index], (0, 0))
    elif bg_status == "fading":
        # Calculate the alpha value for the fading effect
        alpha = int(255 * min(time_elapsed / fade_duration, 1))
        # Display the old and new images with fading effect
        fade_images[image_index].set_alpha(255 - alpha)
        background_images[(image_index + 1) % len(background_images)].set_alpha(alpha)
        screen.blit(fade_images[image_index], (0, 0))
        screen.blit(background_images[(image_index + 1) % len(background_images)], (0, 0))

        # Update the display
    pygame.display.update()

    if time_elapsed >= fade_duration and bg_status == "fading":
        # Control the image loop based on real-time
        image_index = (image_index + 1) % len(background_images)
        last_image_change = current_time
        bg_status = "static"
    elif time_elapsed >= image_change_interval and bg_status == "static":
        # image_index = (image_index + 1) % len(background_images)
        last_image_change = current_time
        bg_status = "fading"

    

    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()

