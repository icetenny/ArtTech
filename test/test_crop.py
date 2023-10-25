from PIL import Image

# Load the image
image = Image.open('pic/turtle_out.png')

# Get the bounding box of non-empty (non-transparent) pixels
bbox = image.getbbox()

# Crop the image to the bounding box
cropped_image = image.crop(bbox)

print(cropped_image)
# Save the cropped image
cropped_image.save('pic/turtle_crop.png')
