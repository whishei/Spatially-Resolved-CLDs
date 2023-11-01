#Data Preprocessing - Thresholding the Images

import numpy as np
import skimage
import matplotlib.pyplot as plt
import os
import glob

from PIL import Image
from skimage.morphology import binary_erosion,binary_dilation,square
from scipy import ndimage as ndi


#Renaming Files from Image # _ Tile # to Tile # _ Image #
def RenameImages(directory):
    for filename in sorted(glob.glob(os.path.join(directory,'*.tif'))):
        print (filename)
        og = filename
        first = og[39:42]
        second = og[43:46]

        old_name = filename
        new_name = 'Tile_' + second + '_' + first + '-000_0.tif'
        new_name = os.path.join(directory,new_name)
        os.rename(old_name, new_name)
        print (new_name)


#Thresholding the image into a binary, segmented image using skimage filters 
def Thresholding(directory):
    for filename in os.listdir(directory):
        if not filename.startswith('.'):
            #print (filename)
            f = os.path.join(directory, filename)
            mask_raw1= Image.open(f)
            mask1 = mask_raw1.convert('L')
            mask1 = np.asarray(mask1)

            image = ndi.gaussian_filter(mask1,1)
            
            thresh = skimage.filters.threshold_yen(image)
            #print (thresh)
            thresh = image >= thresh 

            erode = binary_erosion(thresh,square(3))

            dilate = binary_dilation(erode)

            new = np.zeros((dilate.shape))
            new[dilate] = 1

            #plt.imshow(new,cmap=plt.cm.gray)
            #plt.show()

            #new = np.rot90(new,3)
            #plt.imshow(new,cmap = plt.cm.gray)
            #plt.show()

            if not os.path.exists(directory + '_thresholded'):
                os.makedirs(directory + '_thresholded')
            file = directory + '_thresholded/' + filename[:-4] + '.npy'
            np.save(file, new)


directory = 'Ti5553_on_Ti64_SEM_image_tile_set'#'Ti64_on_Ti5553_SEM_image_tile_set'
#RenameImages(directory)
Thresholding(directory)

