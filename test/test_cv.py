import cv2

# Load the image
image = cv2.imread('pic/turtle.jpg')

# Calculate the new dimensions for scaling (1/3 of the original size)
new_width = image.shape[1] // 3
new_height = image.shape[0] // 3

# Resize the image to the new dimensions
image = cv2.resize(image, (new_width, new_height))

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Set a threshold value to separate the background from the foreground
threshold_value = 200  # You may need to adjust this value based on your image

# Create a binary mask where the background is white and the foreground is black
ret, mask = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

# Invert the mask so that the background is black and the foreground is white
mask = cv2.bitwise_not(mask)

# Apply the mask to the original image to remove the white background
result = cv2.bitwise_and(image, image, mask=mask)


# Display the scaled image using imshow
cv2.imshow('Scaled Image', result)

# Wait for a key press and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
