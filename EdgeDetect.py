import matplotlib.pyplot as plt
import numpy as np
import math

imageInput = None


class EdgeDetect(object):
    def __init__(self, image):
        global imageInput
        self.gradient_degree = None
        imageInput = image[:][:]
        plt.imshow(imageInput)
        self.imageFinal = np.empty([imageInput.shape[0], imageInput.shape[1], 3])

    # convert RGB image to grayscale
    def rgb2gray(self, image):
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                for k in range(3):
                    image[i][j][k] = image[i, j, 0] * 0.299 + image[i, j, 1] * 0.587 + image[i, j, 2] * 0.114
                    # converting each pixel r-g-b to grayscale using weighted average.
        return image

    # generates the sobel edge detection kernel
    @staticmethod
    def sobel_kernel(kernel_type):
        kernel = None
        if kernel_type == "x":
            kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        elif kernel_type == "y":
            kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        return kernel

    # generates the window on which the sobel filter is applied
    def generate_window(self, image, row, col, kernel_size):
        window = np.empty([kernel_size, kernel_size, 3])
        for i in range(kernel_size):
            for j in range(kernel_size):
                row_normal = (row+i) % image.shape[0]
                col_normal = (col+j) % image.shape[1]
                for k in range(3):
                    window[i][j][k] = image[row_normal][col_normal][k]
        return window

    # applies the soble kernel on the image tile-wise
    def laplace_edge(self):
        global imageInput
        imageInput = self.rgb2gray(imageInput)
        kernel_size = 3
        sobel_mask_x = self.sobel_kernel("x")
        sobel_mask_y = self.sobel_kernel("y")
        for row in range(-kernel_size//2, imageInput.shape[0]-kernel_size//2):
            for col in range(-kernel_size//2, imageInput.shape[1]-kernel_size//2):
                if (row <= 0 or row + kernel_size >= imageInput.shape[0] or col <= 0 or col + kernel_size >= imageInput.shape[1]):
                    window = self.generate_window(imageInput, row, col, kernel_size)
                else:
                    window = imageInput[row:row + kernel_size, col:col + kernel_size]
                g_x = 0
                g_y = 0
                for i in range(0, window.shape[0]):
                    for j in range(0, window.shape[1]):
                        g_x += window[i][j][0] * sobel_mask_x[i][j]
                        g_y += window[i][j][0] * sobel_mask_y[i][j]
                for i in range(3):
                    self.imageFinal[row+kernel_size//2][col+kernel_size//2][i] = (g_x**2 + g_y**2)**0.5

    @staticmethod
    def display_image(image):
        plt.imshow(image)
        plt.show()

    def get_image(self):
        return self.imageFinal

    def main(self):
        self.laplace_edge()