import os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from IPython.display import display
from skimage import io, data
from skimage.util import crop

# split input image in 16 sections and save as list of images
def crop_input(image):
    img = io.imread(image)
    height, width, channel = img.shape
    
    #split image in 4x4 sections
    x = width/4
    y = height/4
    
    #create list and fill with sections of input image
    img_array = [0] * 16
    c=0
    for i in range(0,4):
        for j in range (0,4):
            x1 = int(x*i)
            x2 = int(x*i+x)
            y1 = int(y*j)
            y2 = int(y*j+y)
            box = img[y1:y2,x1:x2]
            img_array[c] = box
            c += 1


    return img_array

def merge_image(images):
    col1 = np.vstack((images[0:4]))
    col2 = np.vstack((images[4:8]))
    col3 = np.vstack((images[8:12]))
    col4 = np.vstack((images[12:16]))


    results = np.hstack((col1,col2,col3,col4))
    
    return results