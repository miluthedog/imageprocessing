from sklearn.cluster import KMeans
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class imageClustering:
    def __init__(self):
        self.image = cv.imread('KmeanRmBG\images\image1.png')
        self.threshold_ratio = 0.05 # only variables

        self.output = False
        self.clustering()
    
    def clustering(self):
        if self.image.shape[1]>2000:
            self.image = cv.resize(self.image, (0, 0), fx=0.5, fy=0.5)

        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
        edges = cv.Canny(blurred, 50, 150)

        contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        largest_contour = np.zeros_like(gray)
        cv.drawContours(largest_contour, [contours[0]], -1, 255, thickness=cv.FILLED)

        blue_background = np.zeros_like(self.image)
        blue_background[:, :] = [0, 0, 255]
        image_with_contour = cv.bitwise_and(self.image, self.image, mask=largest_contour)
        image_or = cv.bitwise_or(blue_background, image_with_contour)
        image_with_contour = cv.bitwise_and(image_or, image_or, mask=largest_contour)
        image_xor = cv.bitwise_xor(blue_background, image_with_contour)
        self.image = image_xor

        data = self.image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=3, random_state=0).fit(data)
        clustered_image = kmeans.labels_.reshape(self.image.shape[:2])

        clustered_data = np.bincount(clustered_image.flatten())
        pattern_index = np.argmin(clustered_data)
        pattern = (clustered_image == pattern_index).astype(np.uint8)

        nums, connected_patterns, stats, centroids = cv.connectedComponentsWithStats(pattern, connectivity=8)

        pattern_area = clustered_data[pattern_index]
        threshold = int(self.threshold_ratio * pattern_area)

        clean_pattern = np.zeros_like(pattern)
        for i in range(1, nums):
            if stats[i, cv.CC_STAT_AREA] > threshold:
                clean_pattern[connected_patterns == i] = 255
        
        clean_pattern_height, clean_pattern_width = clean_pattern.shape
        image_transpattern = np.zeros((clean_pattern_height, clean_pattern_width, 4), dtype=np.uint8)
        image_transpattern[clean_pattern != 0] = [0, 0, 0, 255]
        image_transpattern[clean_pattern == 0] = [0, 0, 0, 0]

        plt.imshow(image_transpattern)
        plt.show()

        if self.output:
            cv.imwrite('image_transpattern.png', image_transpattern)


if __name__ == "__main__":
    imageClustering()