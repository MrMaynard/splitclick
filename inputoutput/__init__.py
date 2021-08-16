from common import Rectangle
import cv2
import numpy as np


def find_bounding_rectangle(img):
    min_x, min_y = float("inf"), float("inf")
    max_x, max_y = float("-inf"), float("-inf")

    _, img = cv2.connectedComponents(img)
    for x in range(0, img.shape[1]):
        for y in range(0, img.shape[0]):
            if img[y][x] > 0:
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
    return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)


def bgr_filter(image, bgr_lower, bgr_upper):
    mask = cv2.inRange(image, np.array(bgr_lower), np.array(bgr_upper))
    result = cv2.bitwise_and(image, image, mask=mask)
    return cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)