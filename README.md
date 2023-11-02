# Spatially-Resolved-CLDs
This code works to implement Spatially-resolved chord length distribution (SR-CLD) as a new statistical metric, designed to address the challenges associated with quantitatively analyzing heterogeneous microstructure constituents. SR-CLD is able to quantitatively represent a gradient structure by taking into account the spatial variation throughout an optical image which the traditional methods of analysis, namely area-based estimators and intercept lengths, fail to represent. In this repository there are examples of this metric being used to analyze both synthetic grain microstructures (Neper Case Study) and SEM alloy data (Titanium Case Study). 

## Formulation

A chord is defined as a line segment completely contained within a microstructure constituent of interest. For calculation of individual chords, we adopt a pixel-based approach proposed by [Turner](https://iopscience.iop.org/article/10.1088/0965-0393/24/7/075002). The method relies on a digital representation of a microstructure where microstructure constituents have pixel labels distinct from either boundaries or neibhgor constituents. To calculate a chord length, the sequence of voxels (pixels) labeled as interior to each microstructure constituent are counted as we move either vertically or horizontally across an image until a boundary pixel is hit. At that point, the length of the chord (the count of continuous interior pixels) is added to the bag of chords.

Typically, to obtain a single chord length distribution (CLD) for an optical image, there would be a single bag of chords for the whole image. A chord length distribution can then be calculated from the bag of chords in the form of a discrete probability density function using [Latypov](https://www.sciencedirect.com/science/article/pii/S1044580318313743):

$$P_i = \cfrac{N_i l_i}{\sum^{n}_{i = 1}{N_i l_i}}$$

where the index $i$ goes from $1$ to $n$, the number of chord length bins; $N_i$ denotes the number of chords within the interval of the $i$th bin, with its center corresponding to the chord length $l_i$. Upon calculation, $P_i$ can be interpreted as the probability of finding a pixel that belongs to a chord of length $l_i$ ****Rewrite

To obtain a spatially-resolved chord length distribution (SR-CLD), a distribution is found for each row or each column, rather than for the entire optical image. If the image has vertical spatial heterogeneity, you calculate a distribution horizontally, for each pixel row. Similarly, if the image has horizontal spatial heterogeneity, you calculate a distribution vertically, for each pixel column. To obtain interpretable results, the maximum chord for the entire optical image in the chosen direction is first found before setting the equivalent range and number of bins for every row / column distribution calculated. 

This results in an array of probabilities of size length of rows x $B$ bins. To visualize the spatial heterogeneity, we suggest a heatmap of smoothed SR-CLD probability densities with one axis aligned with the direction of interest, the other axis representing the chord length, and the color representing the probability of finding a chord of a specific length.

Note: The choice of number of bins for the heatmap is not trivial. There are many research groups focused on this question of how to choose the right number of bins to convey an accurate representation of your data. Once all chords are counted along the chosen direction, the distribution of total chords is used to determine the number of bins that will be used throughout the SR-CLD calculation. Some common methods of choosing number of bins include Square Root rule, Sturges' Formula, Scott's Normal Reference Rule, Freedman-Diaconis Rule, Rice's Rule, and Doane's Formula. For this paper, both Rice's rule and Doane's formula were chosen due to the large number of chords and skewness of the distribution, but the authors suggest that future users look into the alternative methods to see which works best for their dataset. 

## Using the Code
To run this project, 

```
git clone https://github.com/whishei/Spatially-Resolved-CLDs.git
```
The only file that needs to be adapted is SR_CLDs.py. In here, you will need a path to your preprocessed image, where each pixel of your optical image has a label, with the interior pixels labeled as 1. (All other pixels that are outside of your grain microstructure can have a different label. The SR-CLD calculation will be performed either horizontally or vertically (or both) and can be visualized by a heatmap. 

```python
#Specific Settings for Neper simulation data
file = 'check_long.png'
mask_raw1= Image.open(file)
mask1 = mask_raw1.convert('RGB')
mask1 = np.asarray(mask1)
man_seg = mask1
new = np.zeros((man_seg.shape[0],man_seg.shape[1])) 
for i in range(0,len(man_seg)):
    for j in range(0,len(man_seg[0])):
        first = np.array_equal(man_seg[i][j],[0,0,255])
        second = np.array_equal(man_seg[i][j],[255,255,255])  
        if first == True and second == False:
            new[i][j] = 1
man_seg = new

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
```

## Examples
There are two provided examples, a Neper case study and a Titanium Case Study. To run either study, uncomment the corresponding section to load the data and run. 
Some settings to play around with would be your choice of bin calculation ('Square', 'Sturges','Scotts', 'Freed', 'Rice', 'Doane') and how you would like to edit the visualization. 

### Figures

The figures below are the results of the Neper Case Study and the Titanium Case Study. For the Titanium Case Study, the horizontal SR-CLD was found for the entire gradient of both alloy samples and two areas of interest were chosen from each sample for analysis. 
<p float="left">
  <img src="Images/Titanium_png.png" />
</p>
<p float="left">
  <img src="Images/Neper_png.png" />
</p>







