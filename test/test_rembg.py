import cv2
from rembg import remove
import numpy as np

input_path = 'pic/pol.jpg'

output_path = 'pic/pol_out2.png'

input = cv2.imread(input_path)
output = remove(input)

non_empty_coordinates = np.argwhere(output[:, :, 3] > 0)

x, y, w, h = cv2.boundingRect(non_empty_coordinates)

cropped = output[x:x+w, y:y+h]
side_length = max(cropped.shape[0], cropped.shape[1])

square_image = np.zeros((side_length, side_length, 4), dtype=np.uint8)

x_offset = (side_length - cropped.shape[1]) // 2
y_offset = (side_length - cropped.shape[0]) // 2

square_image[y_offset:y_offset+cropped.shape[0], x_offset:x_offset+cropped.shape[1]] = cropped

cv2.imwrite(output_path, square_image)

print(f"Saving to {output_path}........")