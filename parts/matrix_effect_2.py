import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
# print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
segmenter = SelfiSegmentation(1)

WIDTH, HEIGHT = 800, 600
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

cell_width, cell_height = 10, 15
new_width, new_height = int(WIDTH / cell_width), int(HEIGHT / cell_height)
new_dimensions = (new_width, new_height)

chars = " .,-~:;=!*#$@"
norm = 255 / len(chars)
font = cv2.FONT_HERSHEY_SIMPLEX
font_size = 0.4

def matrix(image):
    global matrix_window

    matrix_window = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

    small_image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_NEAREST)
    small_image = segmenter.removeBG(small_image, (0, 0, 0))
    gray_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    for i in range(new_height):
        for j in range(new_width):
            intensity = gray_image[i, j]
            char_index = int(intensity / norm)
            color = small_image[i, j]
            # B = int(color[0])
            G = int(color[1])
            # R = int(color[2])

            char = chars[char_index]
            cv2.putText(matrix_window, char, (j * cell_width + 5, i * cell_height + 12), font, font_size,
                        (0, G, 0), 1)

while True:

    _, frame = cap.read()
    result = frame.copy()

    matrix(result)

    cv2.imshow('result', matrix_window)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
