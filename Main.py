import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import os
import shutil
import numpy as np

from DepthSense import DepthSense
from GaussianSmooth import GaussianSmooth
from EdgeDetect import EdgeDetect
from ImagePrepare import ImagePrepare
from Transparency import Transparency

sample = "Motorcycle"
desktop = str(os.environ['USERPROFILE'])+r"\\Desktop\\"
root_path = desktop+sample+r"\\"
original_file_dir = root_path+r"Source\\"
imageL = mpimg.imread(original_file_dir+r"im0.png")
imageR = mpimg.imread(original_file_dir+r"im1.png")

block_list = []
max_block = 29
min_block = 25
span = 3


# display generated image (testing)
def display_image(image):
    plt.imshow(image, cmap='jet')
    plt.show()


# calls the class to generate the disparity map
def disparity_map(block_size, distance):
    global imageL, imageR
    #imageL = imageL[:, :, 0]
    #imageR = imageR[:, :, 0]
    ds = DepthSense(imageL, imageR, distance)
    ds.main(block_size)
    disparityMap = ds.return_disparity()
    np.savetxt(root_path+r"image_array.txt", disparityMap)
    file_name = root_path+r"disparity_map.png"
    mpimg.imsave(file_name, disparityMap, cmap='jet')


# applies the gaussian mask (7x7) on the image and then detects edges
def edge_map(path, count, image):
    imageInput = image[:][:]
    # gaussian smoothing
    gs = GaussianSmooth(imageInput)
    gs.main()
    smoothImage = gs.get_smooth()
    # smoothed image used for edge detection
    imageInput = smoothImage[:][:]
    ed = EdgeDetect(imageInput)
    ed.main()
    edge_image = ed.get_image()
    file_name = path+"\im"+str(count)+".png"
    mpimg.imsave(file_name, edge_image, cmap='jet')

# detects the appropriate size for blocks
# also modifies image if the blocks are not apropos
def prepareImage():
    global imageR
    global imageL
    global block_list
    global max_block, min_block
    ip = ImagePrepare(imageL, imageR, max_block, min_block)
    block_list = ip.main()
    imageR = ip.get_right()
    imageL = ip.get_left()
    if block_list is None:
        print("No blocks generated")
    elif len(block_list) == 0:
        print("Stereoscopic Image Pair dimensions are not equal")
    else:
        print("Modified Image Dimensions: ", imageR.shape[0:2])
        #print(block_list)


# adds 12% colour from the original image to the generated edge map
def transparent_image(path, image, name):
    t = Transparency(path, image, name)
    t.generate_image()


def main():
    global root_path
    global block_list, span
    global imageL, imageR
    global original_file_dir
    # creates a temporary directory to save data generated at runtime
    temp_path = root_path+r"temp\\"
    try:
        os.makedirs(temp_path)
    except OSError:
        if os.path.isdir(temp_path):
            pass
    start = time.time()
    print("Started at : ", time.ctime())
    print("Original Image Dimensions: ", imageR.shape[0:2])
    # image prepared for processing
    prepareImage()
    print("Image prepared at : ", time.ctime())

    if block_list is not None:
        print("Block Size Used: ", block_list[0])
        print("Distance to Check for Disparity: ", imageL.shape[1] // span)
        # checks if stereo pair is same
        if np.array_equal(imageL, imageR):
            print("Same Image")
        # generates edge map for Left Image
        #edge_map(temp_path, 0, imageL)
        print("Edge Map for Left Image generated at : ", time.ctime())
        # generates edge map for Right Image
        #edge_map(temp_path, 1, imageR)
        print("Edge Map for Right Image generated at : ", time.ctime())
        # saves edge map
        filename = root_path+"edge_map.png"
        #mpimg.imsave(filename, mpimg.imread(temp_path+"im1.png"))

        # applies a colour mask on the edge map for better detection
        #transparent_image(original_file_dir, temp_path, "im0.png")
        #transparent_image(original_file_dir, temp_path, "im1.png")
        # reads the image for disparity map generation
        imageL = mpimg.imread(temp_path+r"im0.png")
        imageR = mpimg.imread(temp_path+r"im1.png")

        block = block_list[0]
        disparity_map(block, span)
        print("Disparity Map generated at : ", time.ctime())

        # resize the edge map as per size of disparity map
        file_path = root_path + "edge_map.png"
        edge_image = mpimg.imread(file_path)
        disp_image = mpimg.imread(root_path + "disparity_map.png")
        edge_image = edge_image[:disp_image.shape[0], :disp_image.shape[1]]
        mpimg.imsave(file_path, edge_image)

    # deletes the temporary folder and its content
    #shutil.rmtree(path)

    end = time.time()
    print("Ended at : ", time.ctime())
    print("Time Taken : ~", (end-start)//60, " minutes")

main()