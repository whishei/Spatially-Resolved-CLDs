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

from scipy.ndimage.filters import gaussian_filter
from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter

#import cv2 as cv
import scipy.ndimage as ndimage  
import time
import os
import glob

from scipy.stats import iqr
import statistics

f = 'check_long.png'#'check2.png'#'Test2_crop.png'#'Neper3.png'#'newcheck2_copy.png'
mask_raw1= Image.open(f)
mask1 = mask_raw1.convert('RGB')
mask1 = np.asarray(mask1)
print (mask1)

# plt.imshow(mask1,cmap = plt.cm.gray)
# plt.show()

man_seg = mask1#[10:20]#np.load('TOTAL_COORDS_newcheck2.npy')
# #print (man_seg.shape)
print (mask1.shape)

new = np.zeros((man_seg.shape[0],man_seg.shape[1])) #zeros

#white = man_seg[:] == [255,255,255]
#black = man_seg[:] == [0,0,0]

for i in range(0,len(man_seg)):
    for j in range(0,len(man_seg[0])):
        first = np.array_equal(man_seg[i][j],[0,0,255])
        second = np.array_equal(man_seg[i][j],[255,255,255])  
        if first == True and second == False:
            new[i][j] = 1

# for i in range(0,len(man_seg)):
#     for j in range(0,len(man_seg[0])):
#         first = np.array_equal(man_seg[i][j],[0,0,0])
#         second = np.array_equal(man_seg[i][j],[255,255,255])  
#         if first == False and second == False: 
#             third = np.array_equal(man_seg[i][j],man_seg[i+1][j])
#             fourth = np.array_equal(man_seg[i][j],man_seg[i-1][j])
#             if third == True or fourth == True: 
#                 new[i][j] = 1
#print (white[0])
#print (black[0])
#
# plt.imshow(new,cmap = plt.cm.gray)
# plt.show()

man_seg = new


#print (man_seg.shape)

#plt.imshow(man_seg,cmap = plt.cm.gray)
#plt.show()

st = time.time()
#mult_k = 1
Ps = []
#print (len(mask1[0]))
mult_k = 1#1024 #len(mask1[0]) - 1
maxs = []
total_coords = []
modes = []
means = []
first = 0
print (len(man_seg)/mult_k)
for k in range (0,int(len(man_seg)/mult_k)):
    coords = []
    for i in range(0,mult_k):
        length = 0
        start_pix = 0
        for j in range(0,len(man_seg[i+(k*mult_k)])):
            #print (man_seg[i+(k*mult_k)][j])
            # first = np.array_equal(man_seg[i+(k*mult_k)][j],[0,0,0])
            # second = np.array_equal(man_seg[i+(k*mult_k)][j],[255,255,255])  
            # if first == False and second == False: 
            if man_seg[i+(k*mult_k)][j] == 1: 
                length = length + 1
            else:
                if length == 0:
                    start_pix = start_pix + 1
                if length != 0: 
                    if start_pix != 0:
                        coords.append(length)
                        total_coords.append(length)
                    else: 
                        start_pix = start_pix + 1
                length = 0

    if coords != []:
       maxs.append(max(coords))
    vals, edges = np.histogram(coords,48, range=[1,96]) #check_long
    #vals, edges = np.histogram(coords,50, range=[1,50])
    #vals, edges = np.histogram(coords,46, range=[1,92])
    #vals, edges = np.histogram(coords,46, range=[1,132])
    #vals, edges = np.histogram(coords,41, range=[1,320])
#     #vals, edges = np.histogram(coords,37, range=[1,252])
#     #vals, edges = np.histogram(coords,37, range=[1,366])#,50,range = [1,574])#,100,range = [1,2510]) 26 75,
    
    if coords != []:
        if first == 0:
            first = k
        means.append(statistics.mean(coords))
        modes.append(statistics.mode(coords))
        last = k
    coords = np.array(coords)
# #     # print (len(man_seg[i+(k*mult_k)]))
# #     # print (coords)
# #     # print (vals)
# #     # print (edges)


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
    
    
    #Ps.append(vals)
    #print (middles)
    print (k)
    
Ps = np.array(Ps)

end = time.time()
execution = end - st
print (execution)

#np.save('check_long.npy',total_coords)
#print (middles[:15])

'''
print (np.unique(maxs))
print (len(total_coords))
print (sum(total_coords)/len(total_coords))
print (iqr(total_coords))
'''
#a = np.random.random((16, 16))

#NASA HZ Distribution = 192.73896884918213
#RF HZ Distribution = 188.45563912391663

#np.save('Total_HZ_Neper3.npy',Ps)


#Ps = np.load('Total_HZ.npy')

# # print (Ps.shape)
new_Ps = Ps[:,:25]
print (middles[:25])
#print (new_Ps.shape)
# new_Ps = np.flip(new_Ps,0)
#Visualization 
'''
fig, ax = plt.subplots(figsize=(1,5))
#plt.imshow(Ps)

my_cmap = plt.cm.get_cmap('Spectral')
my_cmap = my_cmap.reversed()
my_cmap.set_over("white")
my_cmap.set_under("white")
ax.imshow(new_Ps,
          #origin='lower',
          cmap=my_cmap, 
          interpolation='bilinear'
          )

# Set tick mark range and spacing
#ax.set_xticks(range(0, 50, 1))
#ax.set_yticks(range(len(new_Ps)))
plt.show()

'''

# fig, ax = plt.subplots(figsize=(1, 5))

# my_cmap = plt.cm.get_cmap('Spectral')
# my_cmap = my_cmap.reversed()
# my_cmap.set_over("white")
# my_cmap.set_under("white")
# # Create a KDE plot from the data
# #kde_data = sns.kdeplot(new_Ps)#, cmap=my_cmap)
# #df3_smooth = gaussian_filter(new_Ps, sigma=1)
# df3_smooth = gaussian_filter(new_Ps, sigma=1) 
# # Create a heatmap with the KDE plot as data source
# plot_1 = sns.heatmap(df3_smooth,cmap = my_cmap)#),vmax = 0.4)#,yticklabels=False,xticklabels=False) #cmap = my_cmap
# #plot_1.set_xlabel('X-Axis', fontsize=10)
# plot_1.set_ylabel('P', rotation = 0, fontsize=10)
# #plt.savefig('compare_HZ.png', bbox_inches='tight', pad_inches=0)
# plt.show()



methods = 'hermite'#, 'kaiser']


fig, ax = plt.subplots(figsize=(1, 5),
                        subplot_kw={'xticks': [], 'yticks': []}) #nrows=1, ncols=2, 

plot = ax.imshow(new_Ps, interpolation=methods, cmap = 'jet', vmax =0.35)#'Spectral')#cmap='viridis')
#ax.set_title(str(method#))
#fig.colorbar(plot)#, cax=cax, orientation='vertical')
#plt.savefig('compare_hermite_HZ.png', bbox_inches='tight', pad_inches=0)
plt.tight_layout()
plt.show()

print (first,last)
ys = np.arange(first,last+1)#length(man_seg))
ys = np.flip(ys)
fig, ax = plt.subplots(figsize=(1, 5),
                        subplot_kw={'xticks': [], 'yticks': []})
#one = plt.scatter(modes,ys, s = 1)
#plt.show()

print (len(means))
print (len(ys))

#ys = np.arange(1,last - first + 2)#length(man_seg))
#fig, ax = plt.subplots(figsize=(1, 5))
two = plt.scatter(means,ys, s = 1)#, ymin = first, ymax = last+1)
plt.tight_layout()
plt.ylim(first, last+1)
#plt.savefig('compare_mean.png', bbox_inches='tight', pad_inches=0)

#plt.legend([one,two],['Modes','Means'])
plt.show()



#Vertical Distribution

# #man_seg  = Test1
# man_seg = man_seg.T
# mult_k = 1
# #plt.imshow(man_seg,cmap=plt.cm.gray)
# #plt.colorbar()
# #plt.axis('off')
# #plt.savefig('Look.eps', bbox_inches='tight', pad_inches=0)
# st = time.time()
# #mult_k = 1
# Ps = []
# mult_k = 1
# maxs = []
# total_coords = []
# for k in range (0,len(man_seg)):
#     coords = []
#     for i in range(0,mult_k):
#         length = 0
#         start_pix = 0
#         for j in range(0,len(man_seg[i+(k*mult_k)])):
#             if man_seg[i+(k*mult_k)][j] == 1: 
#                 length = length + 1
#             else:
#                 if length == 0:
#                     start_pix = start_pix + 1
#                 if length != 0: 
#                     if start_pix != 0:
#                         coords.append(length)
#                         total_coords.append(length)
#                     else: 
#                         start_pix = start_pix + 1
#                 length = 0
                
#     if coords != []:
#        maxs.append(max(coords))
#     vals, edges = np.histogram(coords)#,6,range = [0,6])
    
#     #coords = np.array(coords)
#     # print (len(man_seg[i+(k*mult_k)]))
#     # print (coords)
#     # print (vals)
#     # print (edges)
    
#     middles = []
#     num = []
#     for i in range(0,len(edges)-1):
#         middle = (edges[i]+ edges[i+1])/2 
#         middles.append(middle)
#         num.append(vals[i]*middle)
    
    
#     den = sum(num)
#     #print (vals)
#     if den == 0:
#         P = num 
#     else:
#         P = num/den  
#     Ps.append(P)
#     print (k)
    

# Ps = np.array(Ps)
# Ps = Ps.T
# end = time.time()
# execution = end - st
# print (execution)
# #print (middles[:10])
# print (np.unique(maxs))
# np.save('TOTAL_VT_COORDS.npy',total_coords)
#a = np.random.random((16, 16))

#NASA VT Distribution = 197.434907913208
#RF VT Distribution = 195.33019709587097

#np.save('NASA_Vertical_Distribution.npy',Ps)

#a = np.random.random((16, 16))
#np.save('Vertical_Distribution.npy',Ps)
#
#Ps = np.load('RF_Vertical_Distribution.npy')
'''
print (Ps.shape)
new_Ps = Ps#[:10,:]

fig, ax = plt.subplots(figsize=(5, 1))

#create heatmap
#sns.heatmap(data, linewidths=.3)
my_cmap = plt.cm.get_cmap('Spectral')
my_cmap = my_cmap.reversed()
my_cmap.set_over("white")
my_cmap.set_under("white")
plot_1 = sns.heatmap(new_Ps,cmap = my_cmap)# xticklabels=False,,yticklabels=False, vmax = 0.45)
#plot_1.set_xlabel('X-Axis', fontsize=10)
plot_1.set_xlabel('P', fontsize=10)
#plt.savefig('RF_Vt_Dist.png', bbox_inches='tight', pad_inches=0)
plt.show()

print (coords)
'''