import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def simple_canny(img, low_threshold=100, high_threshold=200):
    edges = cv.Canny(img, low_threshold, high_threshold)
    return edges

def complicated_canny(img, low_threshold=100, high_threshold=200):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blurred = cv.GaussianBlur(gray, (1, 1), 1.4) # Gaussian Blur (1x1) to keep results similar

    sober_filter_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sober_filter_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    grad_x = cv.filter2D(blurred, cv.CV_64F, sober_filter_x)
    grad_y = cv.filter2D(blurred, cv.CV_64F, sober_filter_y)
    magnitude = np.sqrt(grad_x**2 + grad_y**2)

    angle = np.arctan2(grad_y, grad_x) * (180.0 / np.pi)
    angle[angle < 0] += 180
    non_max_suppressed = non_maximum_suppression(magnitude, angle)

    edges = double_threshold_and_hysteresis(non_max_suppressed, low_threshold, high_threshold)
    return edges

def non_maximum_suppression(magnitude, angle):
    rows, cols = magnitude.shape
    suppressed = np.zeros((rows, cols), dtype=np.float32)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if angle[i, j] < 22.5 or angle[i, j] >= 157.5:
                neighbors = [magnitude[i, j+1], magnitude[i, j-1]]
            elif 22.5 <= angle[i, j] < 67.5:
                neighbors = [magnitude[i+1, j-1], magnitude[i-1, j+1]] 
            elif 67.5 <= angle[i, j] < 112.5:
                neighbors = [magnitude[i+1, j], magnitude[i-1, j]]
            else:
                neighbors = [magnitude[i-1, j-1], magnitude[i+1, j+1]]
            if magnitude[i, j] >= np.max(neighbors):
                suppressed[i, j] = magnitude[i, j]
    return suppressed

def double_threshold_and_hysteresis(img, low_threshold, high_threshold):
    rows, cols = img.shape
    strong = 255
    weak = 75   
    result = np.zeros((rows, cols), dtype=np.uint8)
    strong_i, strong_j = np.where(img >= high_threshold)
    weak_i, weak_j = np.where((img >= low_threshold) & (img < high_threshold))
    result[strong_i, strong_j] = strong
    result[weak_i, weak_j] = weak
    return result

img = cv.imread('!HUSTImageProcessing/images/logo.PNG')
img_canny_simple = simple_canny(img)
img_canny_complicated = complicated_canny(img)

cv.imshow('Original Image', img )
cv.imshow('Simple Canny Edge Detection', img_canny_simple)
cv.imshow('Complicated Canny Edge Detection', img_canny_complicated)

cv.waitKey(0)
cv.destroyAllWindows()