import matplotlib.pyplot as plt
import numpy as np
import math

imageInput = None
imageFinal = None


class GaussianSmooth(object):
    def __init__(self, image):
        global imageInput
        global imageFinal
        imageInput = image[:][:]
        imageFinal = np.empty([imageInput.shape[0], imageInput.shape[1]])

    def rgb2gray(self, image):
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                image[i][j] = image[i, j, 0] * 0.299 + image[i, j, 1] * 0.587 + image[i, j, 2] * 0.114
                # converting each pixel r-g-b to grayscale using weighted average.
        return image

    # window wraps over in case of IndexOutOfBounds
    def generate_window(self, image, row, col, kernel_size):
        window = np.empty([kernel_size, kernel_size, 3])
        for i in range(kernel_size):
            for j in range(kernel_size):
                row_normal = (row+i) % image.shape[0]
                col_normal = (col+j) % image.shape[1]
                for k in range(3):
                    window[i][j][k] = image[row_normal][col_normal][k]
        return window

    # apply the gaussian smoothing kernel on the image
    def gaussian_smoothing(self):
        global imageInput
        global imageFinal
        imageFinal = imageInput[:][:]
        kernel_size = 7
        sigma = 1.84
        gauss_mask = self.gauss_kernel(kernel_size, sigma)
        for row in range(-kernel_size//2, imageFinal.shape[0]-kernel_size//2):
            for col in range(-kernel_size//2, imageFinal.shape[1]-kernel_size//2):
                # for windows wrapping the edge
                if (row <= 0 or row + kernel_size >= imageInput.shape[0] or col <= 0 or col + kernel_size >= imageInput.shape[1]):
                    window = self.generate_window(imageInput, row, col, kernel_size)
                # for windows within the frame
                else:
                    window = imageInput[row:row + kernel_size, col:col + kernel_size]
                conv_sum = 0
                # summing the gaussian mask on the window
                for i in range(0, window.shape[0]):
                    for j in range(0, window.shape[1]):
                        conv_sum += (np.sum(window[i][j])/3) * gauss_mask[i][j]
                imageFinal[row+kernel_size//2][col+kernel_size//2] = conv_sum

    @staticmethod
    def display_image(image):
        plt.imshow(image)
        plt.show()

    # generating the gaussian kernel
    @staticmethod
    def gauss_kernel(size, sigma):
        def calc_exp(a, b, sigma):
            num = (1 / (2 * math.pi * sigma * sigma)) * math.exp(-(a * a + b * b) / (2 * sigma * sigma))
            return num

        kernel = np.empty([size, size])
        num = (1 / (2 * math.pi * sigma * sigma)) * math.exp(-(2 * ((-size) // 2 + 1) ** 2) / (2 * sigma * sigma))
        for x in range(-size // 2 + 1, size // 2 + 1, 1):
            for y in range(-size // 2 + 1, size // 2 + 1, 1):
                kernel[x + size // 2][y + size // 2] = round(calc_exp(x, y, sigma) / num, 2)

        summation = np.sum(kernel)
        kernel /= summation
        return kernel

    # send smoothened image to calling function
    @staticmethod
    def get_smooth():
        global imageFinal
        return imageFinal

    def main(self):
        global imageInput
        imageInput = self.rgb2gray(imageInput)
        self.gaussian_smoothing()