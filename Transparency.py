import matplotlib.image as mpimg
import matplotlib
import numpy as np


class Transparency(object):
    def __init__(self, root_path, path, name):
        self.root_path = root_path
        self.path = path
        self.image = None
        self.imageEdge = None
        self.name = name

    # adds 12% colour from original image and highlights edges for better disparity measurement
    def generate_image(self):
        edge_path = self.path + self.name
        image_path = self.root_path + self.name
        self.imageEdge = mpimg.imread(edge_path)
        self.image = mpimg.imread(image_path)
        self.image = self.image[:self.imageEdge.shape[0], :self.imageEdge.shape[1]]
        rows_total = self.image.shape[0]
        
        image_map = np.empty([self.imageEdge.shape[0], self.imageEdge.shape[1], 3])
        # create checkerboard effect to create texture for easier block matching in uni-colour areas
        for i in range(rows_total):
            for j in range(self.image.shape[1]):
                for k in range(3):
                    image_map[i][j][k] = self.imageEdge[i][j][k] * 1.4 + self.image[i][j][k] * 0.1
        mpimg.imsave(edge_path, image_map)