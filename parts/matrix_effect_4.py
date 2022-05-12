import cv2
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import time
from random import randint

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
font_speed = 0

fps_start_time = 0
fps = 0


def matrix_background(i, j):
    matrix_text = randint(0, 1)
    cv2.putText(matrix_window, str(matrix_text), (j * cell_width, i * cell_height + font_speed),
                font, font_size, (80, 120 - i * 3, 0), 1)


def matrix(image):
    global matrix_window, font_speed

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

            if color[1] == 0:
                if (i * cell_height + font_speed) < HEIGHT:
                    matrix_background(i, j)
                else:
                    font_speed = 0
            else:
                char = chars[char_index]
                cv2.putText(matrix_window, char, (j * cell_width + 5, i * cell_height + 12), font, font_size,
                            (0, G, 0), 1)

    font_speed += 1


def framerate(start_time):
    global fps_start_time

    fps_end_time = time.time()
    time_diff = fps_end_time - start_time
    fps = 1 / time_diff
    fps_start_time = fps_end_time
    fps_text = "FPS: {:.1f}".format(fps)
    cv2.putText(matrix_window, fps_text, (10, 20), font, 0.5, (255, 0, 255), 1)


while True:

    _, frame = cap.read()
    result = frame.copy()

    matrix(result)

    framerate(fps_start_time)

    cv2.imshow('result', matrix_window)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
