import numpy as np
import skimage
from PIL import Image
from skimage.feature import canny, blob_dog, peak_local_max

from skimage.util import invert
from skimage import data
from skimage import color
from skimage.filters import meijering, sato, frangi, hessian
from skimage.morphology import skeletonize, thin, dilation, disk,closing
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage.segmentation import random_walker

from skimage.filters.rank import median 
from skimage import segmentation, feature, future
from sklearn.ensemble import RandomForestClassifier
from functools import partial
import seaborn as sns

from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter

#import cv2 as cv
import scipy.ndimage as ndimage  
import time
import os
import glob


directory = '../Preprocessing/Ti5553_on_Ti64_Tiles'

current = 0
total_array = []
Misalign = np.load('Misalignments_5553.npy')
length = 0

for filename in sorted(glob.glob(os.path.join(directory,'*.npy'))):
    print (filename)
    
    array = np.load(filename)

    array = np.rot90(array,3)

    total_array.append(array)

    if current != 0:
        file1 = total_array[0]
        file2 = total_array[1]
        
        if current == 1:
            max_shape_x = 1041#1042
            max_shape_y = 2521#2420#2337
        else:
            max_shape_x = max(file1.shape[0],file2.shape[0])
            max_shape_y = max(file1.shape[1],file2.shape[1])

        file1_shape_x = max_shape_x - file1.shape[0]
        file1_shape_y = max_shape_y - file1.shape[1]
        file2_shape_x = max_shape_x - file2.shape[0]
        file2_shape_y = max_shape_y - file2.shape[1]

        file1 = np.pad(file1, [(file1_shape_x,0),(0,file1_shape_y)], 'constant', constant_values=(-1))
        file2 = np.pad(file2, [(file1_shape_x,0),(0,file2_shape_y)], 'constant', constant_values=(-1))
    
   
        index_1 = Misalign[current-1][0] + length
        index_3 = Misalign[current-1][1]

        print (index_1)
        print (index_3)


        Total = file1
        temp1 = file2

        if (index_3 > 10):
            HZ_1 = 10 - index_3
            for i in range(0,abs(HZ_1)):
                temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
                Total = np.insert(Total,0,-1,axis = 1)
        elif (index_3 < 10):
            for i in range(0,index_3):
                temp1 = np.insert(temp1,0,-1,axis = 1)
                Total = np.insert(Total,Total.shape[1],-1,axis = 1)

        Total = Total[:index_1+40,:]
        length = Total.shape[0] - 40
        temp1 = temp1[40:,:]
        Total = np.concatenate((Total,temp1),axis = 0)
        
        total_array = []
        total_array.append(Total) 

    current = current + 1

    print (current)

np.save('Total_img_5553.npy', Total)
#plt.imshow(Total,cmap = plt.cm.gray)
#plt.axis('off')
#plt.savefig('Total_image.eps', bbox_inches='tight', pad_inches=0)
#plt.show()