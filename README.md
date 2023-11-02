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
x_a, x_b, x_L,T = sy.symbols('x_α, x_β, x_L,T')

x_a0,x_L0,x_b0 = .2,.5,.8
b_a,b_L,b_b = 10,12,11
a = 40

g_α = a*(x_a-x_a0)**2 + b_a
g_β = a*(x_b-x_b0)**2 + b_b
g_L = a*(x_L-x_L0)**2 + b_L - T

T_grid = np.concatenate((np.linspace(1,2.5,10),np.linspace(1.45,1.55,10)))

binary_A_0 = three_phase(g_α,g_β,g_L,A=0)
binary_A_2 = three_phase(g_α,g_β,g_L,A=2)

binary_A_0.plot_diagram(T_grid,title = 'Binary Phase Diagram, A = 0')
binary_A_2.plot_diagram(T_grid,title = 'Binary Phase Diagram, A = 2')

binary_A_0.plot_specific_temp(T_grid[2],x_lim = [.15,.85],y_lim = [9,12])
binary_A_2.plot_specific_temp(T_grid[2],x_lim = [.15,.85],y_lim = [9,12])
```

## Examples
There are two provided examples, a Neper case study and a Titanium Case Study. To run either study, uncomment the corresponding section to load the data and run. 
Some settings to play around with would be your choice of bin calculation ('Square', 'Sturges','Scotts', 'Freed', 'Rice', 'Doane') and how you would like to edit the visualization. 

### Figures

The figures below are using the following free energy functions: 
$$g^\alpha(x^\alpha) = a(x_1^\alpha - x_0^\alpha)^2 + b^\alpha, g^\beta(x^\beta) = a(x_1^\beta - x_0^\beta)^2 + b^\beta ,g^L(x^\beta) = a(x_1^L - x_0^L)^2 + b^L - T$$
Where, $a = 40, x_0^\alpha = .2, x_0^\beta = .8, x_0^L = .5 b^\alpha = 10, b^\beta = 11, b^L = 12$.
<p float="left">
  <img src="Images/A%20=%200.png" width="45%" /> 
<img src="Images/A%20=%202.png" width="45%" /> 
</p>
<p float="left">
  <img src="Images/A%20=%203.png" width="45%" /> 
<img src="Images/A%20=%2010.png" width="45%" /> 
</p>





