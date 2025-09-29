import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
from pyts.image import MarkovTransitionField
import pandas as pd

# Modify the variable parameters according to your needs.
filename = "yourfile.xlsx"  # Path to the file to be processed
savepath = "./data"  # MTF image save path
img_sz = 165  # Determine the size of the generated MTF image


print("MTF Image size：%d * %d" % (img_sz, img_sz))
img_path = "%s/images" % savepath  # Folder for Saving Visualization Images
data_path = "%s/data" % savepath  # Folder where data files are saved
if not os.path.exists(img_path):
    os.makedirs(img_path)  # If the folder does not exist, create one.
if not os.path.exists(data_path):
    os.makedirs(data_path)  # If the folder does not exist, create one.

print("Start generating...")
print("Visualization images are saved in the folder %s, and data files are saved in the folder %s." % (img_path, data_path))

# Reading Excel files using pandas
df = pd.read_excel(filename)
src_data = df.values

img_num = src_data.shape[1]  # The total number of generated images equals the number of columns in the data matrix.
mtf = MarkovTransitionField(image_size=img_sz)
mtf_images = mtf.fit_transform(src_data.T)

# mtf_images  shape is （img_num, img_sz, img_sz)
for i in range(img_num):  # Save each image
    mtf_img = mtf_images[i, :, :]  # Obtain the data for the i-th image
    img_save_path = "%s/%d.png" % (img_path, i)
    data_save_path = "%s/%d.csv" % (data_path, i)
    image.imsave(img_save_path, mtf_img)  # save image
    np.savetxt(data_save_path, mtf_img, delimiter=',')  # Save data as a CSV file

print("Generation complete. A total of %d images were processed." % img_num)
