from utils import * 

#########################################################################################

# Load your data here. Expected format is that your pixels to be counted will be represented as a 1.

#########################################################################################
#Specific Settings for Neper simulation data
file = 'Neper Case Study/seeded.png' 
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

# # # #########################################################################################

# # # Running the SR-CLD Calculations 

#### Horizontally
chords, krow_chords = Horizontal_Chords(man_seg,1) #Vertical_Chords(man_seg,1)

Num,maximum = BinSize(chords, 'Doane')

#### Optional - Overall CLD 
# CLD(chords,Num, maximum, "")

Ps,means,min = SRCLD(krow_chords,chords, Num, maximum) 

Visualization(Ps, means, "Horizontal",maximum)#,"name")   
