import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def simple_gray(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return gray

def simple_hist(gray_img):
    hist = cv.calcHist([gray_img], [0], None, [256], [0, 256])
    return hist

def complicated_gray(img):
    b, g, r = cv.split(img)
    gray = 0.299 * r + 0.587 * g + 0.114 * b
    gray = gray.astype(np.uint8)
    return gray

def complicated_hist(gray_img):
    hist = np.zeros((256, 1), dtype=np.int32)
    for i in range(gray_img.shape[0]):
        for j in range(gray_img.shape[1]):
            pixel_value = gray_img[i, j]
            hist[pixel_value] += 1
    return hist

img = cv.imread('!HUSTImageProcessing/images/thanlan.PNG')
img_gray = simple_gray(img)
img_hist = simple_hist(img_gray)
img_gray_complicated = complicated_gray(img)
img_hist_complicated = complicated_hist(img_gray)

cv.imshow('Original Image', img_gray)
cv.imshow('Complicated Image', img_gray_complicated)
plt.figure()

plt.title('Grayscale Histogram')
plt.xlabel('Bins')
plt.ylabel('# of Pixels')
plt.plot(img_hist)
plt.plot(img_hist_complicated, color='r', linestyle='--')
plt.xlim([0, 256])
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()