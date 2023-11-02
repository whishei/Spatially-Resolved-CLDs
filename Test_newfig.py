############ SR-CLD Calculation and Visualization #################

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage  
import time
from scipy.stats import iqr,tstd,tmean
import statistics
import math


#Getting all of the horizontal chords for the entire image 
#  input: image array
#  output: chords
def Horizontal_Check(input):
    man_seg = input
    mult_k = 1
    total_coords = []
    for k in range (0,int(len(man_seg)/mult_k)):
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
                            total_coords.append(length)
                        else: 
                            start_pix = start_pix + 1
                    length = 0

        coords = np.array(total_coords)
    return coords


#Calculating the horizontal SR-CLD for the image. 
#  input: image array, number of bins, max range value 
#  output: SR-CLD probabilities (Ps), means, index of first row with a chord (first),
#           index of last row with a chord (last), middle value of bins (middles)
def Horizontal_CLDs(input,N,maximum):
    man_seg = input
    Ps = []
    mult_k = 1
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
            if first == 0:
                first = k
            means.append(statistics.mean(coords))
            #modes.append(statistics.mode(coords))
            last = k
        vals, edges = np.histogram(coords,N, range=[1,maximum]) 
        coords = np.array(coords)
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
        
        print (k)
        
    Ps = np.array(Ps)
    return Ps, means, first,last,middles


#Getting all of the vertical chords for the entire image 
#  input: image array
#  output: chords
def Vertical_Check(input):
    man_seg = input
    man_seg = man_seg.T
    mult_k = 1
    total_coords = []
    for k in range (0,int(len(man_seg)/mult_k)):
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
                            total_coords.append(length)
                        else: 
                            start_pix = start_pix + 1
                    length = 0

        coords = np.array(coords)
    return coords


#Calculating the vertical SR-CLD for the image. 
#  input: image array, number of bins, max range value 
#  output: SR-CLD probabilities (Ps), means, index of first row with a chord (first),
#           index of last row with a chord (last), middle value of bins (middles)
def Vertical_CLDs(input,N,maximum):
    man_seg = input
    man_seg = man_seg.T
    Ps = []
    mult_k = 1
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
            vals, edges = np.histogram(coords,N, range=[1,maximum]) 
            if first == 0:
                first = k
            means.append(statistics.mean(coords))
            #modes.append(statistics.mode(coords))
            last = k
        
        coords = np.array(coords)
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
        
        print (k)
        
    Ps = np.array(Ps)
    Ps = Ps.T
    return Ps, means,first,last,middles


#Calculating the ideal number of bins and largest range value for the probability distributions  
#  input: coords, setting ('Square','Sturges','Scotts','Freed','Doane','Rice')
#  output: the number of bins and largest range value for the probability distributions  
def BinSize(coords,setting):

    total = coords

    numba = len(total)

    print (total)
    #print (max(total))
    #print (min(total))

    #Square Root Rule
    if setting == 'Square':
        square = math.sqrt(len(total))
        #print ('Square Root',square)
        maximum = math.ceil(max(total)/int(square))*int(square)
        return int(square),maximum

    #Sturges Formula
    elif setting == 'Sturges':
        k = (1 + 3.322*math.log10(len(total)))
        #print ('Sturges', k)
        maximum = math.ceil(max(total)/int(k))*int(k)
        return int(k), maximum
   
    #Scott's Normal Reference Rule:
    elif setting == 'Scotts':
        scott = (max(total)-min(total))/(3.5*tstd(total)*len(total)**(-1/3))
        #print('Scotts:',scott)
        maximum = math.ceil(max(total)/int(scott))*int(scott)
        return int(scott),maximum

    #Freedman-Diaconis Rule:
    elif setting == 'Freed':
        freed = 2*iqr(len(total))/(numba**(1/3))
        #print ('Freedman:',freed)
        maximum = math.ceil(max(total)/int(freed))*int(freed)
        return int(freed), maximum 

    #Rice's Rule:
    elif setting == 'Rice':
        rice = 2*(numba**(1/3))
        #print ('Rices:',rice)
        maximum = math.ceil(max(total)/int(rice))*int(rice)
        return int(rice), maximum

    #Doane's Rule:
    elif setting == 'Doane':
        skewness = (3*(tmean(total)-np.median(total)))/tstd(total)
        N = len(total)
        error_skewness = math.sqrt((6 * (N - 1)) / ((N - 2) * (N + 1) * (N + 3)))
        g1 = skewness/error_skewness

        doane = 1 + np.log2(N) + np.log2(1 + abs(g1)/error_skewness)
        #print ('Doane:',doane)
        maximum = math.ceil(max(total)/int(doane))*int(doane)
        return int(doane), maximum 

#########################################################################################

#Specific Settings for Neper simulation data
man_seg = np.random.randint(2, size=(32, 32))
plt.imshow(man_seg, cmap = plt.cm.gray)
plt.show()

#Specific Loading instructions for Titanium data 
# man_seg = np.load('Total_img.npy')
# man_seg = np.flip(man_seg,0)
# man_seg = man_seg[162895:174895]


#  Overall man_seg should be equal to your binary (or greyscale) array where 1 represents inside of the grain
#  and 0 is outside 

st = time.time()
chords = Horizontal_Check(man_seg)
Num,maximum = BinSize(chords, 'Doane')
Ps,means,first,last,middles = Horizontal_CLDs(man_seg, Num,maximum)
end = time.time()
execution = end - st
print (execution)


#####################################################################################

#       Visualization: All very subjective. Up to you how you choose to visualize it. 

# Current Visualization for Neper 
new_Ps = Ps[:,:25]
print (middles[:25])


methods = 'hermite'


fig, ax = plt.subplots(figsize=(1, 5),
                        subplot_kw={'xticks': [], 'yticks': []})  

plot = ax.imshow(new_Ps, interpolation=methods, cmap = 'jet', vmax =0.35, extent=[0,middles[25],0,252], aspect='auto')
#ax.set_title(str(method#))
fig.colorbar(plot)#, cax=cax, orientation='vertical')
#plt.savefig('compare_HZ_NEW.png', bbox_inches='tight', pad_inches=0)
plt.tight_layout()
plt.show()

ys = np.arange(first,last+1)
ys = np.flip(ys)
fig, ax = plt.subplots(figsize=(1, 5),
                        subplot_kw={'xticks': [], 'yticks': []})

two = plt.plot(means,ys, color='#EA334B')
plt.tight_layout()
plt.ylim(first, last+1)
plt.xlim(0,middles[25])
#plt.savefig('compare_mean.svg', bbox_inches='tight', pad_inches=0)

#plt.legend([one,two],['Modes','Means'])
plt.show()




# Current Visualization for Titanium 

# methods = 'hermite'


# fig, ax = plt.subplots(figsize=(1, 5),
#                         subplot_kw={'xticks': [], 'yticks': []}) 

# plot = ax.imshow(new_Ps, interpolation=methods, cmap = 'jet',extent=[0,middles[25],0,12000], aspect='auto', vmax =0.30)
# #ax.set_title(str(method#))
# #fig.colorbar(plot)#, cax=cax, orientation='vertical')
# plt.savefig('compare_HZ_NEW2.png', bbox_inches='tight', pad_inches=0)
# plt.tight_layout()
# plt.show()

# ys = np.arange(first,last+2)
# ys = np.flip(ys)
# fig, ax = plt.subplots(figsize=(1, 5),
#                         subplot_kw={'xticks': [], 'yticks': []})

# two = plt.plot(means,ys, color='#EA334B')
# plt.tight_layout()
# plt.ylim(first, last+1)
# plt.xlim(0,middles[25])
# plt.savefig('compare_mean_NEW2.svg', bbox_inches='tight', pad_inches=0)

# plt.show()