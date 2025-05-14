from utils import * 
import cv2


#########################################################################################
#### Loading Neper Case Study images
# file = 'Neper Case Study/seeded.png'

# mask_raw1= Image.open(file)
# mask1 = mask_raw1.convert('RGB')
# mask1 = np.asarray(mask1)
# man_seg = mask1
# new = np.zeros((man_seg.shape[0],man_seg.shape[1])) 
# for i in range(0,len(man_seg)):
#     for j in range(0,len(man_seg[0])):
#         first = np.array_equal(man_seg[i][j],[0,0,255])
#         second = np.array_equal(man_seg[i][j],[255,255,255])  
#         if first == True and second == False:
#             new[i][j] = 1

# man_seg = new[:2112,:6345]

#########################################################################################
#### Loading SPPARKS Case Study images

# File name
img = 'SPPARKS/SPPARKS_seg_1.png'

# Load the image
img = cv2.imread(img)

# Create a mask for black pixels (R, G, B all below 30)
is_black = np.all(img < 100, axis=-1)

# Create binary mask: 1 for grains (non-black), 0 for boundaries (black)
grain_mask = np.where(is_black, 0, 1).astype(np.uint8)

# (Optional) Multiply by 255 if you want to save it as an image
grain_mask = np.invert(grain_mask)

kernel = np.ones((3, 3), np.uint8)
closed = cv2.morphologyEx(grain_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

man_seg = np.invert(closed)

man_seg = man_seg[60:1376, 60:3036]

man_seg = np.rot90(man_seg,1)

#########################################################################################
#### Loading Titanium Case Study images

# man_seg = np.load('64_Sample1_113000_125000.npy')

#########################################################################################
#### Loading Demo Arrays

# man_seg = [[1,1,1,1,1,0,1,1,1,1,1,0,1,1,1],
#             [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
#             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
#             [0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],
#             [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1],
#             [0,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
#             [0,1,1,1,0,1,1,1,0,1,1,1,0,1,1],
#             [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
#             [1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
#             [1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
#             [1,1,1,1,1,0,1,1,1,1,1,0,1,1,1],
#             [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
#             [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
#             [0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],
#             [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1]]


# # man_seg = [[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
# #            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
# #            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
# #            [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1],
# #            [1,1,0,1,1,0,1,1,0,1,1,0,1,1,0],
# #            [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1],
# #            [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
# #            [0,1,1,1,0,1,1,1,0,1,1,1,0,1,1],
# #            [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
# #            [0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],
# #            [1,1,1,1,0,1,1,1,1,0,1,1,1,1,0],
# #            [0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],
# #            [1,1,1,1,1,0,1,1,1,1,1,0,1,1,1],
# #            [0,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
# #            [1,1,1,1,1,0,1,1,1,1,1,0,1,1,1]]

# man_seg = np.array(man_seg)
# plt.imshow(man_seg, cmap = plt.cm.gray)
# plt.show()


# # # # #########################################################################################

# Verifying correct loading of image:
# Pixels to be counted should all be white == 1, all other pixels should be black == 0

plt.imshow(man_seg, cmap = plt.cm.gray)
plt.show()

# # # Running the SR-CLD Calculations 

# Finding all of the vertical chords and all the horizontal chords in the image
v_chords, v_krow_chords = Vertical_Chords(man_seg,1)
h_chords, h_krow_chords = Horizontal_Chords(man_seg,1)

# Calculating the optimal number of bins via a chosen formula 
v_Num,v_maximum = BinSize(v_chords, 'Doane') 
h_Num,h_maximum = BinSize(h_chords, 'Doane') 


print (v_Num, v_maximum)
print (h_Num, h_maximum)

# Calculation of the vertical and horizontal SR-CLDs for the image
v_Ps,v_means = SRCLD(v_krow_chords,v_chords, v_Num, v_maximum) 
h_Ps,h_means = SRCLD(h_krow_chords,h_chords, h_Num, h_maximum)

# Visualing the SR-CLD heat maps and mean plots for both directions
# If you wish to save the files, add the name as an additional argument, for example 'SPPARKS_1' 
Visualization(v_Ps, v_means, "Vertical", v_maximum)
Visualization(h_Ps, h_means, "Horizontal",h_maximum)

