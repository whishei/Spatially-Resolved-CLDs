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



def Horizontal_Check(array):
    man_seg = array
    new_man_seg = man_seg
    coords = []
    for i in range(0,len(new_man_seg)):
        length = 0
        start_pix = 0
        for j in range(0,len(man_seg[0])):
            if man_seg[i][j] == 1: 
                length = length + 1
            else:
                if length == 0:
                    start_pix = start_pix + 1
                if length != 0: 
                    if start_pix != 0:
                        coords.append(length)
                    else: 
                        start_pix = start_pix + 1
                length = 0

        if coords != []:
            new_max = (max(coords))
   
    return new_max


def Vertical_Check(array):
    man_seg  = array
    man_seg = man_seg.T
    new_man_seg = man_seg
    coords = []
    for i in range(0,len(new_man_seg)):
        length = 0
        start_pix = 0
        for j in range(0,len(man_seg[0])):
            if man_seg[i][j] == 1: 
                length = length + 1
            else:
                if length == 0:
                    start_pix = start_pix + 1
                if length != 0: 
                    if start_pix != 0:
                        coords.append(length)
                    else: 
                        start_pix = start_pix + 1
                length = 0

        if coords != []:
            new_max = (max(coords))
   
    return new_max

def Horizontal_CLDs(array,maximum):
    man_seg = array
    new_man_seg = man_seg
    maxs = []
    Ps = []
    mult_k = 1
    maxs = []
    for k in range (0,len(new_man_seg)):
        coords = []
        for i in range(0,mult_k):
            length = 0
            start_pix = 0
            for j in range(0,len(man_seg[i+(k*mult_k)])):
                if man_seg[i+(k*mult_k)][j] == 1: 
                    length = length + 1
                else:
                    if length == 0:
                        start_pix = start_pix + 1
                    if length != 0: 
                        if start_pix != 0:
                            coords.append(length)
                        else: 
                            start_pix = start_pix + 1
                    length = 0

        if coords != []:
            maxs.append(max(coords))
        vals, edges = np.histogram(coords,20,range = [1,maximum]) 


        middles = [] 
        num = []
        for i in range(0,len(edges)-1):
            middle = (edges[i]+ edges[i+1])/2 
            middles.append(middle)
            num.append(vals[i]*middle)
        
        
        den = sum(num)
        
        if den == 0:
            P = num 
        else:
            P = num/den   
        Ps.append(P)
        
    Ps = np.array(Ps)
   
    return Ps

def Vertical_Misalign(vd_1,vd_2):
    overlap = 700
    end_poss = 1000
    error = []
    for k in range(overlap,end_poss): #len(vd_1)):
        total = 0
        for i in range(k,len(vd_1)):
            total = total + np.sqrt(np.sum((vd_1[i] - vd_2[i-k]) ** 2)) 
        error.append(total/(len(vd_1)-k))

    #print (error)
    print (error.index(min(error))+700)
    return (error.index(min(error))+700)


def Vertical_CLDs(array,maximum):
    man_seg  = array
    man_seg = man_seg.T
    mult_k = 1
    st = time.time()
    Ps = []
    mult_k = 1
    maxs = []
    for k in range (0,len(man_seg)):
        coords = []
        for i in range(0,mult_k):
            length = 0
            start_pix = 0
            for j in range(0,len(man_seg[i+(k*mult_k)])):
                if man_seg[i+(k*mult_k)][j] == 1: 
                    length = length + 1
                else:
                    if length == 0:
                        start_pix = start_pix + 1
                    if length != 0: 
                        if start_pix != 0:
                            coords.append(length)
                        else: 
                            start_pix = start_pix + 1
                    length = 0
                    
        if coords != []:
            maxs.append(max(coords))
        vals, edges = np.histogram(coords,20,range = [1,maximum])#100])
        
        middles = []
        num = []
        for i in range(0,len(edges)-1):
            middle = (edges[i]+ edges[i+1])/2 
            middles.append(middle)
            num.append(vals[i]*middle)
        
        
        den = sum(num)
        #print (vals)
        if den == 0:
            P = num 
        else:
            P = num/den  
        Ps.append(P)
        #print (k)
        

    Ps = np.array(Ps)
    Ps = Ps.T
    end = time.time()
    execution = end - st
   
    return Ps
    
def Horizontal_Misalign(hd_1,hd_2):
    hd_1 = hd_1.T
    hd_2 = hd_2.T

    #print (hd_1.shape)
    #print (hd_2.shape)

    overlap = 0
    error = []
    for k in range(overlap,10):
        total = 0
        for i in range(k,len(hd_1)):
            total = total + np.sqrt(np.sum((hd_1[i] - hd_2[i-k]) ** 2)) 
        error.append(total/(len(hd_1)-k))

    overlap = 0
    #error = []
    for k in range(overlap,10):
        total = 0
        for i in range(k,len(hd_2)):
            total = total + np.sqrt(np.sum((hd_2[i] - hd_1[i-k]) ** 2)) 
        error.append(total/(len(hd_2)-k))

    #print (error)
    print (error.index(min(error)))
    return error.index(min(error))


directory = '../Preprocessing/Ti64_on_Ti5553_Tiles'#'NEW_Tiles'#'Testing'#'RenamedImages'

current = 0
total_array = []
Misalign = []
max_x = 0
max_y = 0
for filename in sorted(glob.glob(os.path.join(directory,'*.npy'))):#os.listdir(directory):
    print (filename)
    
    array = np.load(filename)

    array = np.rot90(array,3)

    # if array.shape[0] > max_x:
    #     max_x = array.shape[0]
    # if array.shape[1] > max_y:
    #     max_y = array.shape[1]

    #plt.imshow(array,cmap = plt.cm.gray)
    #plt.show()

    total_array.append(array)

    #print (current)
    if current != 0:
        #print (total_array)
        file1 = total_array[current - 1]
        #print (file1.shape)
        file2 = total_array[current]
        #file3 = total_array[2]
        Align = []
        '''
        plt.imshow(file1,cmap = plt.cm.gray)
        plt.show()
        plt.imshow(file2,cmap = plt.cm.gray)
        plt.show()
        '''
    
        #print (file1.shape)
        #print (file2.shape)
        
        #5553- max x: 1041, max y: 2521

        max_shape_x = 1042#1041#1034#1042#max(file1.shape[0],file2.shape[0])
        max_shape_y = 2420#2521#2514#2337#max(file1.shape[1],file2.shape[1])
        #max_shape =  (max(file1.shape,file2.shape))
    
        file1_shape_x = max_shape_x - file1.shape[0]
        #print (file1_shape_x)
        file1_shape_y = max_shape_y - file1.shape[1]
        #print (file1_shape_y)
        file2_shape_x = max_shape_x - file2.shape[0]
        #print (file2_shape_x)
        file2_shape_y = max_shape_y - file2.shape[1]
        #print (file2_shape_y)


        #[(0, 1), (0, 1)]
        file1 = np.pad(file1, [(file1_shape_x,0),(0,file1_shape_y)], 'constant', constant_values=(-1))
        file2 = np.pad(file2, [(file2_shape_x,0),(0,file2_shape_y)], 'constant', constant_values=(-1))

        # #plt.imshow(file2,cmap = plt.cm.gray)
        # #plt.show()
        # #plt.imshow(file1,cmap = plt.cm.gray)
        # #plt.show()
        # #print (file1.shape)
        # #print (file2.shape)

        maximum = Horizontal_Check(file1)
        maximum2 = Horizontal_Check(file2)
        #maximum3 = Horizontal_Check(file3)

        max1 = max(maximum,maximum2)  
        #max2 = max(maximum2,maximum3)      
        
        file1_HD = Horizontal_CLDs(file1,max1)
        file2_HD = Horizontal_CLDs(file2,max1)
        #file2_2_HD = Horizontal_CLDs(file2,max2)
        #file3_HD = Horizontal_CLDs(file3,max2)
        
        #Finding Vertical misalign
        index_1 = Vertical_Misalign(file1_HD,file2_HD)
        #index_2 = Vertical_Misalign(file2_2_HD,file3_HD)
        
        file1_1 = file1[index_1:,:]
        file2_1 = file2[0:(len(file2)-index_1),:]

        # file1_1 = np.insert(file1_1,0,-1,axis = 0)
        # file1_1 = np.insert(file1_1,(len(file1)-index_1)+1,-1,axis = 0)
        # file2_1 = np.insert(file2_1,0,-1,axis = 0)
        # file2_1 = np.insert(file2_1,(len(file2)-index_1)+1,-1,axis = 0)

        # plt.imshow(file1_1,cmap = plt.cm.gray)
        # plt.show()
        # plt.imshow(file2_1,cmap = plt.cm.gray)
        # plt.show()
        
        # file2_2 = file2[index_2:,:]
        # file3_2 = file3[0:(len(file3)-index_2),:]

        # plt.imshow(file2_2,cmap = plt.cm.gray)
        # plt.show()

        # plt.imshow(file3_2,cmap = plt.cm.gray)
        # plt.show()

        maximum = Vertical_Check(file1)
        maximum2 = Vertical_Check(file2)
        #maximum3 = Vertical_Check(file3)

        max1 = max(maximum,maximum2)  
        #max2 = max(maximum2,maximum3)      
        
        file1_1_VD = Vertical_CLDs(file1_1,max1)
        file2_1_VD = Vertical_CLDs(file2_1,max1)
        #file2_2_VD = Vertical_CLDs(file2_2,max2)
        #file3_2_VD = Vertical_CLDs(file3_2,max2)

        #Finding Horizontal misalign
        index_3 = Horizontal_Misalign(file1_1_VD,file2_1_VD)
        #index_4 = Horizontal_Misalign(file2_2_VD,file3_2_VD)
        Align.append(index_1)
        Align.append(index_3)
        Misalign.append(Align)
        
        
        # Total = file1
        # temp1 = file2
        # #temp2 = file3

        
        # if (index_3 > 10):
        #     HZ_1 = 10 - index_3
        #     for i in range(0,abs(HZ_1)):
        #         temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
        #         #temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
        #         Total = np.insert(Total,0,-1,axis = 1)
        #         #print (i)
        # elif (index_3 < 10):
        #     for i in range(0,index_3):
        #         temp1 = np.insert(temp1,0,-1,axis = 1)
        #         #temp2 = np.insert(temp2,0,-1,axis = 1)
        #         Total = np.insert(Total,Total.shape[1],-1,axis = 1)
        #         #print(i)
        
        # if (index_4 > 10):
        #     HZ_2 = 10 - index_4
        #     for i in range(0,abs(HZ_2)):
        #         temp1 = np.insert(temp1,0,-1,axis = 1)
        #         temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
        #         Total = np.insert(Total,0,-1,axis = 1)
        #         #print (i)
        # elif (index_4 < 10):
        #     for i in range(0,index_4):
        #         temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
        #         temp2 = np.insert(temp2,0,-1,axis = 1)
        #         Total = np.insert(Total,Total.shape[1],-1,axis = 1)
        #         #print(i)
        # Total = Total[:index_1+40,:]
        # temp1 = temp1[40:,:]
        # Total = np.concatenate((Total,temp1),axis = 0)
        #Total = np.concatenate((Total,temp2),axis = 0)

        # newfile1 = 'Tile_' + current+ '.npy'
        # newfile2 = 'Tile_' + current+ '.png'

        # plt.imshow(Total,cmap = plt.cm.gray)
        # plt.axis('off')
        # #plt.savefig(newfile2, bbox_inches='tight', pad_inches=0)
        # plt.show()
        
        #np.save(newfile1,Total)

        #new_p = Image.fromarray(Total)
        #new_p = new_p.convert("L")
        #new_p.save(newfile2)
        
        #current = filename[19:22]
        #total_array[0] = total_array[1]
        

    # mask = Image.open(filename)
    # mask = mask.convert('L')
    # mask = np.asarray(mask)

    # new = np.zeros((mask.shape))
    # new[mask < 125] = 1

    #plt.imshow(new,cmap = plt.cm.gray)
    #plt.show()
    current = current + 1

    print (current)
    #print (len(total_array))
#print (max_x,max_y)
np.save('Misalignments_64.npy',Misalign)
# file1 = total_array[0]
# #print (file1.shape)
# file2 = total_array[1]
# file3 = total_array[2]

# maximum = Horizontal_Check(file1)
# maximum2 = Horizontal_Check(file2)
# maximum3 = Horizontal_Check(file3)

# max1 = max(maximum,maximum2)  
# max2 = max(maximum2,maximum3)      

# file1_HD = Horizontal_CLDs(file1,max1)
# file2_HD = Horizontal_CLDs(file2,max1)
# file2_2_HD = Horizontal_CLDs(file2,max2)
# file3_HD = Horizontal_CLDs(file3,max2)

# #Finding Vertical misalign
# index_1 = Vertical_Misalign(file1_HD,file2_HD)
# index_2 = Vertical_Misalign(file2_2_HD,file3_HD)

# file1_1 = file1[index_1:,:]
# file2_1 = file2[0:(len(file2)-index_1),:]

# #file1_1 = np.insert(file1_1,0,-1,axis = 0)
# #file1_1 = np.insert(file1_1,(len(file1)-index_1)+1,-1,axis = 0)
# #file2_1 = np.insert(file2_1,0,-1,axis = 0)
# #file2_1 = np.insert(file2_1,(len(file2)-index_1)+1,-1,axis = 0)

# # plt.imshow(file1_1,cmap = plt.cm.gray)
# # plt.show()
# # plt.imshow(file2_1,cmap = plt.cm.gray)
# # plt.show()

# file2_2 = file2[index_2:,:]
# file3_2 = file3[0:(len(file3)-index_2),:]

# # plt.imshow(file2_2,cmap = plt.cm.gray)
# # plt.show()

# # plt.imshow(file3_2,cmap = plt.cm.gray)
# # plt.show()

# maximum = Vertical_Check(file1)
# maximum2 = Vertical_Check(file2)
# maximum3 = Vertical_Check(file3)

# max1 = max(maximum,maximum2)  
# max2 = max(maximum2,maximum3)      

# file1_1_VD = Vertical_CLDs(file1_1,max1)
# file2_1_VD = Vertical_CLDs(file2_1,max1)
# file2_2_VD = Vertical_CLDs(file2_2,max2)
# file3_2_VD = Vertical_CLDs(file3_2,max2)

# #Finding Horizontal misalign
# index_3 = Horizontal_Misalign(file1_1_VD,file2_1_VD)
# index_4 = Horizontal_Misalign(file2_2_VD,file3_2_VD)

# Total = file1
# temp1 = file2
# temp2 = file3

# if (index_3 > 10):
#     HZ_1 = 10 - index_3
#     for i in range(0,abs(HZ_1)):
#         temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
#         temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
#         Total = np.insert(Total,0,-1,axis = 1)
#         #print (i)
# elif (index_3 < 10):
#     for i in range(0,index_3):
#         temp1 = np.insert(temp1,0,-1,axis = 1)
#         temp2 = np.insert(temp2,0,-1,axis = 1)
#         Total = np.insert(Total,Total.shape[1],-1,axis = 1)
#         #print(i)

# if (index_4 > 10):
#     HZ_2 = 10 - index_4
#     for i in range(0,abs(HZ_2)):
#         temp1 = np.insert(temp1,0,-1,axis = 1)
#         temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
#         Total = np.insert(Total,0,-1,axis = 1)
#         #print (i)
# elif (index_4 < 10):
#     for i in range(0,index_4):
#         temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
#         temp2 = np.insert(temp2,0,-1,axis = 1)
#         Total = np.insert(Total,Total.shape[1],-1,axis = 1)
#         #print(i)

# Total = Total[:index_1,:]
# temp1 = temp1[:index_2,:]
# Total = np.concatenate((Total,temp1),axis = 0)
# Total = np.concatenate((Total,temp2),axis = 0)

# newfile1 = 'Tile_' + current+ '.npy'
# newfile2 = 'Tile_' + current+ '.png'

# #plt.imshow(Total,cmap = plt.cm.gray)
# #plt.axis('off')
# #plt.savefig(newfile2, bbox_inches='tight', pad_inches=0)
# #plt.show()

# np.save(newfile1,Total)
