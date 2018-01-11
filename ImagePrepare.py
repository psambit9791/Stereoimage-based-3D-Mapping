import numpy as np
from DepthSense import DepthSense

imageL = None
imageR = None

class ImagePrepare(object):
    def __init__(self, i_L, i_R, max_block, min_block):
        global imageL
        global imageR
        imageL = i_L
        imageR = i_R
        self.block_list = []
        self.height = 0
        self.length = 0
        self.max_block = max_block
        self.min_block = min_block
        self.height_block = []
        self.length_block = []

    # set/get length and height
    def set_dimensions(self):
        global imageL
        self.height = imageL.shape[0]
        self.length = imageL.shape[1]

    # checks if dimension value is prime or not
    def is_prime(self, x):
        for i in range(self.min_block, self.max_block+1):#14
            if x % i == 0:
                return False
        return True

    # sets a new divisible size if dimension is a prime number
    def set_new_size(self):
        global imageR
        global imageL
        if self.is_prime(imageR.shape[1]):
            new_width = imageR.shape[1] - 1
            imageR = imageR[:, :new_width]
            imageL = imageL[:, :new_width]
        if self.is_prime(imageR.shape[0]):
            new_height = imageR.shape[0] - 1
            imageR = imageR[:new_height, :]
            imageL = imageL[:new_height, :]

    # checks if right and left image dimensions are equal
    @staticmethod
    def check_shape():
        global imageL
        global imageR
        if imageL.shape != imageR.shape:
            return False
        return True

    def get_right(self):
        global imageR
        return imageR

    def get_left(self):
        global imageL
        return imageL

    # converts the input image to grayscale
    def rgb2gray(self, image):
        for i in range(0, self.height):
            for j in range(0, self.length):
                image[i][j] = image[i, j, 0] * 0.299 + image[i, j, 1] * 0.587 + image[i, j, 2] * 0.114
                # converting each pixel r-g-b to grayscale using weighted average.
        return image

    # read image from source and initialise disparity map
    def read_image(self):
        global imageL
        global imageR
        imageL = self.rgb2gray(imageL)
        imageR = self.rgb2gray(imageR)

    # generates the block to optimise the execution time and accuracy of result
    def block_dimension(self):
        self.height_block = []
        self.length_block = []
        # finding a common factor as length for tile
        for i in range(self.max_block, self.min_block-1, -1):  #14
            if self.height % i == 0:
                self.height_block.append(i)
        # finding a common factor as height for tile
        for i in range(self.max_block, self.min_block-1, -1):
            if self.length % i == 0:
                self.length_block.append(i)
        return self.height_block, self.length_block

    # list a set of blocks for optimum shape
    def generate_block_list(self):
        global imageR
        height_list, length_list = self.block_dimension()
        for i in range(len(height_list)):
            for j in range(len(length_list)):
                self.block_list.append((height_list[i], length_list[j]))
                if len(self.block_list) >= 1:
                    return self.block_list
        return self.block_list

    # iterates size modification until optimum size is reached
    def check_blocks(self):
        count = 0
        while len(self.block_list) < 1 or len(self.length_block) == 0 or len(self.height_block) == 0:
            count += 1
            self.block_list = []
            self.set_new_size()
            self.set_dimensions()
            self.generate_block_list()
        return count

    # final call function
    def main(self):
        global imageL
        global imageR
        self.read_image()
        if self.check_shape():
            if self.check_blocks() <= 60:
                return self.block_list
        else:
            return []