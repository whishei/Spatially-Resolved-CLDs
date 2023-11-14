import numpy as np
import time
import os
import glob


#Finding the maximum horizontal chord length for the entire image 
#  input: image array
#  output: maximum horizontal chord length 
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

#Finding the maximum vertical chord length for the entire image 
#  input: image array
#  output: maximum vertical  chord length 
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

#Calculating horizontal SR-CLDs for the entire image
#  input: image array, maximum horizontal chord length 
#  output: SR-CLD probabilities
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

#Aligning two images vertically at a time 
#  input: The two calculated horizontal SR-CLDS for comparison. 
#  output: The index of the row that the overlap starts for the first image. 
def Vertical_Align(vd_1,vd_2):
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


#Calculating vertical SR-CLDs for only the overlap of the two images 
#  input: image array, maximum vertical chord length of entire image 
#                     (*needed since some overlaps do not contain a single chord for each column)
#  output: SR-CLD probabilities
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


 #Aligning two images horizonally at a time 
#  input: The two calculated vertical SR-CLDS for comparison. 
#  output: The index of the column that the overlap starts for the first image. 
#       * since aligning left and right, over 10 means the bottom image needs to move to the right   
def Horizontal_Align(hd_1,hd_2):
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


#############################################################################
#Chose the directory your images are in. 
# This code is set up to align two images at a time 
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

    if current != 0:
        file1 = total_array[current - 1]
        file2 = total_array[current]
        Align = []

        #Need to find the maximum sizes of all the images first, code available above to find maxs if needed
        max_shape_x = 1042#1041
        max_shape_y = 2420#2521
    
        #Starting all files the same shape
        file1_shape_x = max_shape_x - file1.shape[0]
        file1_shape_y = max_shape_y - file1.shape[1]
        file2_shape_x = max_shape_x - file2.shape[0]
        file2_shape_y = max_shape_y - file2.shape[1]

        file1 = np.pad(file1, [(file1_shape_x,0),(0,file1_shape_y)], 'constant', constant_values=(-1))
        file2 = np.pad(file2, [(file2_shape_x,0),(0,file2_shape_y)], 'constant', constant_values=(-1))

        #Finding Alignment horizontally
        maximum = Horizontal_Check(file1)
        maximum2 = Horizontal_Check(file2)

        max1 = max(maximum,maximum2)      
        
        file1_HD = Horizontal_CLDs(file1,max1)
        file2_HD = Horizontal_CLDs(file2,max1)
        
        #Finding Alignment vertically
        index_1 = Vertical_Align(file1_HD,file2_HD)
       
        file1_1 = file1[index_1:,:]
        file2_1 = file2[0:(len(file2)-index_1),:]

        maximum = Vertical_Check(file1)
        maximum2 = Vertical_Check(file2)
        
        max1 = max(maximum,maximum2)   
        
        file1_1_VD = Vertical_CLDs(file1_1,max1)
        file2_1_VD = Vertical_CLDs(file2_1,max1)

        #Finding Horizontal misalign
        index_3 = Horizontal_Align(file1_1_VD,file2_1_VD)

        #Saving the alignment indexs for reconstruction
        Align.append(index_1)
        Align.append(index_3)
        Misalign.append(Align)
        
    current = current + 1

    print (current)
    
#print (max_x,max_y)
np.save('Misalignments_64.npy',Misalign)
