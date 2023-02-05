import rasterio
import matplotlib.pyplot as plt
import numpy as np


dataset = rasterio.open('data/30N000E_20101117_gmted_mea300.tif').read()[0]

height = dataset.shape[0]
width = dataset.shape[1]

def crop(ymin, ymax, xmin, xmax):
    dataset = dataset[ymin:height-ymax, xmin:width-xmax]
    height -= ymin + ymax
    width -= xmin + xmax

def remove_zeroes():
    dataset = np.ma.masked_where(dataset == 0, dataset)

# nice cmap with norm log: gist_earth gray terrain
plt.imshow(dataset, cmap='gist_earth', norm='log')

plt.show()
