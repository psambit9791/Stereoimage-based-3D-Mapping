import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sample = "Aloe"
desktop = str(os.environ['USERPROFILE'])+r"\\Desktop\\"
path = desktop+sample+r"\\image_array.txt"

class generate_3d(object):
    def __init__(self, name, path):
        global desktop
        self.name = name
        self.path = path
        self.new_dir = desktop+self.name+r"\\3D_Map\\"
        try:
            os.makedirs(self.new_dir)
        except OSError:
            if os.path.isdir(self.new_dir):
                pass

    # generates images of model from 360 degrees
    def generate_map(self):
        global desktop
        image_file = np.loadtxt(self.path)
        print("File read complete")
        plt.imshow(image_file, cmap='jet')
        r, c = np.shape(image_file)
        X, Z = np.meshgrid(range(0, r, 8), range(0, c, 8))#not 8, 15
        col_map = plt.get_cmap("jet")
        height = 8.0
        length = ((height/image_file.shape[0])*image_file.shape[1]) + 1.0
        plt.ioff()
        fig = plt.figure(figsize=(length, height))
        ax = Axes3D(fig)
        ax.set_frame_on(False)
        ax.scatter(-Z, image_file[X, Z], -X, s=4, c=image_file[X, Z], cmap=col_map)
        for degree in range(0, 360):
            ax.view_init(elev=15, azim=degree)
            filename = self.new_dir+self.name+"_3D_map"+str(degree)+".png"
            fig.savefig(filename, bbox_inches='tight')
        fig.clear()
        plt.close('all')

gmap = generate_3d(sample, path)
gmap.generate_map()
print("Execution completed.")
os._exit(0)
