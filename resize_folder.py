import cv2
import os

import os
import cv2

# Set the input and output folders
input_folder = "pic/backgrounds"
output_folder = "pic/new_backgrounds"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Set the target size for resizing
target_width = 1500  # Set your desired width
target_height = 700  # Set your desired height

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # Add more extensions as needed
        # Read the image
        input_path = os.path.join(input_folder, filename)
        img = cv2.imread(input_path)

        # Resize the image
        img_resized = cv2.resize(img, (target_width, target_height))

        # Define the output file path
        output_path = os.path.join(output_folder, filename)

        # Save the resized image
        cv2.imwrite(output_path, img_resized)

        print(f"Resized and saved: {output_path}")

print("All images resized and saved.")
