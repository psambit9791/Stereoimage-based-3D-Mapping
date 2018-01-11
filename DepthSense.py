import matplotlib.pyplot as plt
import numpy as np

imageL = None  # Left Image
imageR = None  # Right Image


class DepthSense(object):
    def __init__(self, i_L, i_R, span):
        global imageL
        global imageR
        imageR = i_R
        imageL = i_L
        self.iterator = min(imageL.shape[1]//150, 5)
        self.disparityMap = np.empty([imageL.shape[0], imageL.shape[1]])
        self.pixel_range = int(imageL.shape[1]//span)
        self.height = imageL.shape[0]
        self.length = imageL.shape[1]

    # set/get disparity map
    def return_disparity(self):
        return self.disparityMap

    # set/get length and height
    def set_dimensions(self):
        self.height = imageL.shape[0]
        self.length = imageL.shape[1]

    # get dimensions of image
    def get_dimensions(self):
        return self.height, self.length

    # generate a window from the input image based on the row & column passed as argument and the block size
    def generate_window(self, row, col, image, block_size):
        window = (image[row:row + block_size[0], col:col + block_size[1]])
        return window

    # calculating sub-pixel accuracy based on Lagrange interpolation
    def subpixel_accuracy(self, row, col, colL, block_size, windowRight, disparity_value, SAD):
        global imageL
        if col == 0 or col == imageL.shape[1] - block_size[1] - 1:
            return disparity_value
        else:
            C2 = SAD
            window = self.generate_window(row, colL - 1, imageL, block_size)
            C1 = int(abs(windowRight - window).sum())
            window = self.generate_window(row, colL + 1, imageL, block_size)
            C3 = int(abs(windowRight - window).sum())
            if C3 + C1 - 2 * C2 == 0:
                return disparity_value
            d_est = disparity_value - (C3 - C1) / (C3 + C1 - 2 * C2)
            return d_est

    # crop the final image from the point where the right and left images don't correspond anymore
    def crop_image(self):
        mean_disparity = int(np.mean(self.disparityMap))
        new_width = self.length - mean_disparity
        self.disparityMap = self.disparityMap[:, :new_width]

    # compares window on the Right image to windows on the Left image to find the closest matching block
    def block_matching(self, block_size):
        global imageL
        global imageR
        for row in range(0, imageR.shape[0] - block_size[0] + 1,
                         min(self.iterator, block_size[0])):  # setting image row
            for col in range(0, imageR.shape[1] - block_size[1] + 1,
                             min(self.iterator, block_size[1])):  # setting image column
                # min() used for iterator so that in case block smaller than iterator, no blank space in image
                windowRight = self.generate_window(row, col, imageR, block_size)
                # a window is generated from the right image from row and col as per block size
                SAD = 99999  # initialised sum of added differences variable
                disparity_val = 0
                for colL in range(col + block_size[1], min(imageR.shape[1] - block_size[1], col + self.pixel_range)):
                    # loop for creating the sliding window, if pixel range goes beyond image, min func will limit it.
                    windowLeft = self.generate_window(row, colL, imageL, block_size)
                    # a window is generated from the left image from row and colL as per block size
                    temp = int(abs(windowRight - windowLeft).sum())  # calculating SAD
                    if temp < SAD:
                        SAD = temp
                        disparity_val = abs(colL - col)
                        if SAD == 0:
                            break  # break the loop if the closest match is found
                        disparity_val = self.subpixel_accuracy(row, col, colL, block_size, windowRight,
                                                               disparity_val, SAD)
                    # setting disparity for the closest matching block. If SAD lower than before, set new SAD

                for i in range(row, row + block_size[0]):
                    for j in range(col, col + block_size[1]):
                        self.disparityMap[i][j] = disparity_val
                        # updating disparity values in the disparity map image
        self.crop_image()
#       self.normalise_image()
#       self.display_image(imageFinal)

    # displays the image sent as argument
    @staticmethod
    def display_image(image):
        plt.imshow(image, cmap='jet')
        plt.show()

    # final call function
    def main(self, block_size):
        self.block_matching(block_size)