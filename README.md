# [Spatially-Resolved-CLDs](https://arxiv.org/html/2409.03729v1)
This study introduces the calculation of spatially-resolved chord length distribution (SR-CLD) as an efficient approach for quantifying and visualizing non-uniform microstructures in heterogeneous materials. SR-CLD enables detailed analysis of spatial variation of microstructure constituent sizes in different directions that can be overlooked with traditional descriptions. We present the calculation of SR-CLD using efficient scan-line algorithm that counts pixels in constituents along pixel rows or columns of microstructure images for detailed, high-resolution SR-CLD maps. We demonstrate the application of SR-CLD in two case studies: one on synthetic polycrystalline microstructures with known and intentionally created uniform and gradient spatial distributions of grain size; and one on experimental images of two-phase microstructures of additively manufactured Ti alloys with significant spatially non-uniform distributions of laths of one of the phases. Additionally, we present how SR-CLDs can enable automated and computationally efficient alignment of large sets of images  that emphasizes consistency of merged composite images in terms of chord length distributions, i.e., size of constituents. 

## Using the Code
To run this project either download the full project:
```
git clone https://github.com/whishei/Spatially-Resolved-CLDs.git
```
or 
download the files "utils.py" (contains all relevant functions) and "SR_CLDs.py" (main script for loading data and running SR-CLD calculations)


The only file that needs to be adapted is SR_CLDs.py. In here, you will need a path to your preprocessed image, where each pixel of your optical image has a label, with the interior pixels that you wish to count labeled as 1. All other pixels that are outside of your microstructure constiuent of interest should have a different label. The SR-CLD calculation will be performed either horizontally or vertically (or both) and can be visualized by a heatmap. 








