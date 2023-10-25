import cv2
from rembg import remove
import numpy as np

# Create a VideoCapture object to access the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a window to display the webcam feed
cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Display the frame in the "Webcam" window
    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1)

    # Press 'q' to exit the loop
    if key == ord('q'):
        break
    elif key == ord('s'):

        output = remove(frame)
        non_empty_coordinates = np.argwhere(output[:, :, 3] > 0)

        x, y, w, h = cv2.boundingRect(non_empty_coordinates)

        cropped = output[x:x+w, y:y+h]
        side_length = max(cropped.shape[0], cropped.shape[1])

        square_image = np.zeros((side_length, side_length, 4), dtype=np.uint8)

        x_offset = (side_length - cropped.shape[1]) // 2
        y_offset = (side_length - cropped.shape[0]) // 2

        square_image[y_offset:y_offset+cropped.shape[0], x_offset:x_offset+cropped.shape[1]] = cropped

        print("saving..")
        cv2.imwrite("data/capture/pic1.png", square_image)


# Release the VideoCapture and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
