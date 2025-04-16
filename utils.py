############ SR-CLD Calculation and Visualization #################

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage  
import time
from scipy.stats import iqr,tstd,tmean
import statistics
import math
from numba import jit
import scipy.stats as stats
from scipy.stats import chisquare
import cv2

@jit(nopython=True)

# Calculating the horizontal chords for the image
#  img: image array
#  k: number of rows to be considered at once (default = 1)
#  output: total chords, chords per row(or k rows)
def Horizontal_Chords(img, k=1):
    total_chords = []
    krow_chords = []

    for i in range (0,int(len(img)/k)):
        krow = []
        for j in range(0,k):     
            length = 0
            start_pix = 0
            for m in range(0,len(img[j+(i*k)])):   
                if img[j+(i*k)][m] == 1: 
                    length = length + 1
                else:
                    if length == 0:
                        start_pix = start_pix + 1
                    if length != 0: 
                        if start_pix != 0:
                            krow.append(length)
                            total_chords.append(length)
                        else: 
                            start_pix = start_pix + 1
                    length = 0
        krow_chords.append(krow)
    total_chords = np.array(total_chords)
    return total_chords, krow_chords


# Calculating the vertical chords for the image
#  img: image array
#  k: number of columns to be considered at once (default = 1)
#  output: chords
def Vertical_Chords(img, k =1):
    img_T = img.T
    return Horizontal_Chords(img_T, k)


# Calculating the single chord length distribution for the image
#  chords: calculated chords
def CLD(chords, N, maximum,name):
    vals, edges = np.histogram(chords,N, range=[0.5, maximum + 0.5])

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

    plt.plot(P, color='#EA334B')
    if name != "":
        plt.savefig(name, dpi=600, bbox_inches='tight')
    plt.show()

    return P


# Calculating the spatially-resolved chord length distributions for the image (each k-section)
#  chords: calculated chords
def SRCLD(krow_chords, chords, Num=0, maximum=0):

    if Num == 0 or maximum == 0:
        Num,maximum = max(chords)
    
    Ps = []
    means = []
    min_num = []

    for i in range(0,len(krow_chords)):
        vals, edges = np.histogram(krow_chords[i],Num, range=[0.5, maximum + 0.5])

        middles = [] 
        num = []
        
        for j in range(0,len(edges)-1):
            middle = (edges[j]+ edges[j+1])/2 
            middles.append(middle)
            num.append(vals[j]*middle)
        
        den = sum(num)
        
        if den == 0:
            P = num 
        else:
            P = num/den  
            mean = np.mean(krow_chords[i])
            means.append(mean)
            Ps.append(P)
            min_num.append(len(krow_chords[i]))

    Ps = np.array(Ps)
    means = np.array(means) 
    min_num = np.array(min_num)

    return Ps,means,min_num


#Calculating the ideal number of bins and largest range value for the probability distributions  
#  input: coords, setting ('Square','Sturges','Scotts','Freed','Doane','Rice')
#  output: the number of bins and largest range value for the probability distributions  
def BinSize(chords,setting):

    total = chords

    numba = len(total)

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


def Visualization(Ps,means, setting, maximum, name=""):


    if setting == "Horizontal":
        fig, ax = plt.subplots(figsize=(1, 5),
                            subplot_kw={'xticks': [], 'yticks': []})  

        plot = ax.imshow(Ps, cmap = 'Spectral_r', aspect='auto') #vmax = )
        cbar = fig.colorbar(plot)
        #cbar.set_ticks(np.linspace(0, vmax_val, num=5))
        plt.title("SR-CLD")
        if name != "":
            name_P = name+"_Ps.png"
            plt.savefig(name_P, dpi=600, bbox_inches='tight')
        plt.tight_layout()
        plt.show()
        

        vals = np.arange(1,len(means)+1)
        vals = np.flip(vals)
        fig, ax = plt.subplots(figsize=(1, 5),
                                subplot_kw={'xticks': [], 'yticks': []})

        plt.plot(means,vals, color='#00B8FF')
        plt.tight_layout()
        plt.ylim(vals[-1],vals[0])
        plt.xlim(1,maximum)
        plt.title("Mean")
        if name != "":
            name_mean = name+"_means.svg"
            plt.savefig(name_mean, dpi=600, bbox_inches='tight')
        plt.show()

    if setting == "Vertical":
        Ps = Ps.T
        Ps = np.flipud(Ps) 
        means = np.flip(means)
        fig, ax = plt.subplots(figsize=(5, 1),
                            subplot_kw={'xticks': [], 'yticks': []})  

        plot = ax.imshow(Ps, cmap = 'Spectral_r', aspect='auto')#, vmax = 0.2)
        cbar = fig.colorbar(plot)
        #cbar.set_ticks(np.linspace(0, vmax_val, num=5))
        plt.title("SR-CLD")
        if name != "":
            name_P = name+"_Ps.png"
            plt.savefig(name_P, dpi=600, bbox_inches='tight')
        plt.tight_layout()
        plt.show()

        vals = np.arange(1,len(means)+1)

        fig, ax = plt.subplots(figsize=(5,1),
                                subplot_kw={'xticks': [], 'yticks': []})

        plt.plot(vals, means, color='#FF0045')
        plt.tight_layout()
        plt.xlim(vals[-1],vals[0])
        plt.ylim(0,maximum)
        plt.title("Mean")
        if name != "":
            name_mean = name+"_means.svg"
            plt.savefig(name_mean, dpi=600, bbox_inches='tight')
        plt.show()

