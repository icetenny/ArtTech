from PIL import Image

# Open the PNG image
image = Image.open("pic/vavsa_logo.png")  # Replace with the path to your image
r, g, b, a = image.split()

# Invert the color channels (RGB) while keeping the alpha channel (A) unchanged
inverted_r = r.point(lambda x: 255 - x)
inverted_g = g.point(lambda x: 255 - x)
inverted_b = b.point(lambda x: 255 - x)

# Merge the inverted color channels with the original alpha channel
inverted_image = Image.merge("RGBA", (inverted_r, inverted_g, inverted_b, a))

# Save the inverted image
inverted_image.save("pic/vavsa_logo_2.png")

# Close the images (optional but good practice)
image.close()
inverted_image.close()
