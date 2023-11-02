#Data Preprocessing Aligning Individual Tiles 

import numpy as np
import matplotlib.pyplot as plt
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
    new_man_seg = man_seg
    man_seg = man_seg.T
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
    print (vd_1.shape)
    print (vd_2.shape)
    overlap = 600
    end_poss = 840
    error = []
    for k in range(overlap,end_poss):#len(vd_1)):
        total = 0
        for i in range(k,len(vd_1)):
            total = total + np.sqrt(np.sum((vd_1[i] - vd_2[i-k]) ** 2)) 
        error.append(total/(len(vd_1)-k))

    #print (error)
    print (error.index(min(error))+600)
    return (error.index(min(error))+600)


#Calculating vertical SR-CLDs for only the overlap of the two images 
#  input: image array, maximum vertical chord length of entire image 
#                     (*needed since some overlaps do not contain a single chord for each column)
#  output: SR-CLD probabilities
def Vertical_CLDs(array,maximum):
    man_seg  = array
    man_seg = man_seg.T
    mult_k = 1
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
   
    return Ps
    


#Aligning two images horizonally at a time 
#  input: The two calculated vertical SR-CLDS for comparison. 
#  output: The index of the column that the overlap starts for the first image. 
#       * since aligning left and right, over 10 means the bottom image needs to move to the right
def Horizontal_Align(hd_1,hd_2):
    hd_1 = hd_1.T
    hd_2 = hd_2.T

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
# This code is set up to align three three images at a time 

directory = 'Ti64_on_Ti5553_SEM_image_tile_set_thresholded'#'Ti5553_on_Ti64_SEM_image_tile_set_thresholded'
st = time.time()
current = ''
total_array = []
for filename in sorted(glob.glob(os.path.join(directory,'*.npy'))):

    #Only the case for the first image in the file 
    if current == '':
        current = filename[len(directory) + 6: len(directory) + 9]
    
    #Once all three images are loaded in 
    elif filename[len(directory) + 6: len(directory) + 9] != current:

        #Naming the three images we are working with 
        file1 = total_array[0]
        file2 = total_array[1]
        file3 = total_array[2]

        #Finding the maximum horizontal chord length in the entire image
        maximum = Horizontal_Check(file1)
        maximum2 = Horizontal_Check(file2)
        maximum3 = Horizontal_Check(file3)

        #Need two maximum chord lengths for comparing two horizontal CLDs at a time
        max1 = max(maximum,maximum2)  
        max2 = max(maximum2,maximum3)      
        
        #Calculating horizontal SR-CLDs for entire image. 
        file1_HD = Horizontal_CLDs(file1,max1)
        file2_HD = Horizontal_CLDs(file2,max1)
        file2_2_HD = Horizontal_CLDs(file2,max2)
        file3_HD = Horizontal_CLDs(file3,max2)
        
        #Aligning the images vertically
        index_1 = Vertical_Align(file1_HD,file2_HD)
        index_2 = Vertical_Align(file2_2_HD,file3_HD)
        
        #Grabbing just the overlapping section from each pair of images
        file1_1 = file1[index_1:,:]
        file2_1 = file2[0:(len(file2)-index_1),:]
        file2_2 = file2[index_2:,:]
        file3_2 = file3[0:(len(file3)-index_2),:]

        #Finding the maximum vertical chord length in the entire image
        maximum = Vertical_Check(file1)
        maximum2_1 = Vertical_Check(file2)
        maximum2_2 = Vertical_Check(file2)
        maximum3 = Vertical_Check(file3)

        #Need two maximum chord lengths for comparing two vertical CLDs at a time
        max1 = max(maximum,maximum2_1)  
        max2 = max(maximum2_2,maximum3)      

        #Calculating vertical SR-CLDs for entire image. 
        file1_1_VD = Vertical_CLDs(file1_1,max1)
        file2_1_VD = Vertical_CLDs(file2_1,max1)
        file2_2_VD = Vertical_CLDs(file2_2,max2)
        file3_2_VD = Vertical_CLDs(file3_2,max2)

        #Finding Horizontal misalign
        index_3 = Horizontal_Align(file1_1_VD,file2_1_VD)
        index_4 = Horizontal_Align(file2_2_VD,file3_2_VD)


        #Aligning the images horizontally (could be left or right movement)
        Total = file1
        temp1 = file2
        temp2 = file3

        #Working with the first pair of images, if index > 10, shift both bottom images to the left
        if (index_3 > 10):
            HZ_1 = 10 - index_3
            for i in range(0,abs(HZ_1)):
                temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
                temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
                Total = np.insert(Total,0,-1,axis = 1)

        #Working with the second pair of images, if index < 10, shift both bottom images to the right
        elif (index_3 < 10):
            for i in range(0,index_3):
                temp1 = np.insert(temp1,0,-1,axis = 1)
                temp2 = np.insert(temp2,0,-1,axis = 1)
                Total = np.insert(Total,Total.shape[1],-1,axis = 1)
        
        #Working with the second pair of images, if index > 10, shift only the bottom image to the left
        if (index_4 > 10):
            HZ_2 = 10 - index_4
            for i in range(0,abs(HZ_2)):
                temp1 = np.insert(temp1,0,-1,axis = 1)
                temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
                Total = np.insert(Total,0,-1,axis = 1)
                
        #Working with the second pair of images, if index < 10, shift only the bottom image to the right
        elif (index_4 < 10):
            for i in range(0,index_4):
                temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
                temp2 = np.insert(temp2,0,-1,axis = 1)
                Total = np.insert(Total,Total.shape[1],-1,axis = 1)
        
        #Slicing the bottom overlap off the two top images
        Total = Total[:index_1,:]
        temp1 = temp1[:index_2,:]

        #Concatenating the three aligned images into one
        Total = np.concatenate((Total,temp1),axis = 0)
        Total = np.concatenate((Total,temp2),axis = 0)

        #Saving the files
        newfile1 = 'Tile_' + current+ '.npy'
        newfile2 = 'Tile_' + current+ '.png'

        plt.imshow(Total,cmap = plt.cm.gray)
        plt.axis('off')
        plt.savefig(newfile2, bbox_inches='tight', pad_inches=0)
        np.save(newfile1,Total)
        
        current = filename[len(directory) + 6: len(directory) + 9]
        total_array = []

    #Loading the images
    new = np.load(filename)

    total_array.append(new)

    print (current)


#Same process as above, just working with the last set of three images in the file. 
file1 = total_array[0]
file2 = total_array[1]
file3 = total_array[2]

maximum = Horizontal_Check(file1)
maximum2 = Horizontal_Check(file2)
maximum3 = Horizontal_Check(file3)

max1 = max(maximum,maximum2)  
max2 = max(maximum2,maximum3)      

file1_HD = Horizontal_CLDs(file1,max1)
file2_HD = Horizontal_CLDs(file2,max1)
file2_2_HD = Horizontal_CLDs(file2,max2)
file3_HD = Horizontal_CLDs(file3,max2)

#Finding Vertical misalign
index_1 = Vertical_Align(file1_HD,file2_HD)
index_2 = Vertical_Align(file2_2_HD,file3_HD)

file1_1 = file1[index_1:,:]
file2_1 = file2[0:(len(file2)-index_1),:]

file2_2 = file2[index_2:,:]
file3_2 = file3[0:(len(file3)-index_2),:]

maximum = Vertical_Check(file1)
maximum2 = Vertical_Check(file2)
maximum3 = Vertical_Check(file3)

max1 = max(maximum,maximum2)  
max2 = max(maximum2,maximum3)      

file1_1_VD = Vertical_CLDs(file1_1,max1)
file2_1_VD = Vertical_CLDs(file2_1,max1)
file2_2_VD = Vertical_CLDs(file2_2,max2)
file3_2_VD = Vertical_CLDs(file3_2,max2)

#Finding Horizontal misalign
index_3 = Horizontal_Align(file1_1_VD,file2_1_VD)
index_4 = Horizontal_Align(file2_2_VD,file3_2_VD)

Total = file1
temp1 = file2
temp2 = file3

if (index_3 > 10):
    HZ_1 = 10 - index_3
    for i in range(0,abs(HZ_1)):
        temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
        temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
        Total = np.insert(Total,0,-1,axis = 1)
        #print (i)
elif (index_3 < 10):
    for i in range(0,index_3):
        temp1 = np.insert(temp1,0,-1,axis = 1)
        temp2 = np.insert(temp2,0,-1,axis = 1)
        Total = np.insert(Total,Total.shape[1],-1,axis = 1)
        #print(i)

if (index_4 > 10):
    HZ_2 = 10 - index_4
    for i in range(0,abs(HZ_2)):
        temp1 = np.insert(temp1,0,-1,axis = 1)
        temp2 = np.insert(temp2,temp2.shape[1],-1,axis = 1)
        Total = np.insert(Total,0,-1,axis = 1)
        #print (i)
elif (index_4 < 10):
    for i in range(0,index_4):
        temp1 = np.insert(temp1,temp1.shape[1],-1,axis = 1)
        temp2 = np.insert(temp2,0,-1,axis = 1)
        Total = np.insert(Total,Total.shape[1],-1,axis = 1)
        #print(i)

Total = Total[:index_1,:]
temp1 = temp1[:index_2,:]
Total = np.concatenate((Total,temp1),axis = 0)
Total = np.concatenate((Total,temp2),axis = 0)

newfile1 = 'Tile_' + current+ '.npy'
newfile2 = 'Tile_' + current+ '.png'

plt.imshow(Total,cmap = plt.cm.gray)
plt.axis('off')
plt.savefig(newfile2, bbox_inches='tight', pad_inches=0)
#plt.show()

np.save(newfile1,Total)

end = time.time()
execution = end - st
print (execution)