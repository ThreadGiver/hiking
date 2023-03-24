import rasterio
from rasterio.windows import Window
import matplotlib.pyplot as plt
import numpy as np

class Mapper():
    def __init__(self, file_name, remove_zeroes=False, min_zero=True) -> None:
        file_ref = {
            'italy300': '30N000E_20101117_gmted_mea300.tif',
            'italy075': '30N000E_20101117_gmted_mea075.tif',
            'midUS300': '30N120W_20101117_gmted_mea300.tif',
            'midUS075': '30N120W_20101117_gmted_mea075.tif',
            'grand_canyon': 'gc_dem.tif'
        }
        self.file = rasterio.open(f'data/{file_ref.get(file_name, file_name)}')
        self.dataset = self.file.read(1)
        self.height = self.dataset.shape[0]
        self.width = self.dataset.shape[1]

        if remove_zeroes:
            self.dataset = np.ma.masked_where(self.dataset == 0, self.dataset)
        
        if min_zero:
            self.dataset[self.dataset < 0] = 0


    def crop(self, col_off: int, row_off: int, width: int, height: int):
        """Crops the dataset

        Args:
            col_off (int): column offset
            row_off (int): row offset
            width (int): crop to width
            height (int): crop to height
        """
        self.dataset = self.file.read(1, window=Window(
            col_off, row_off, width, height
        ))
        return self
    
    def imshow_dataset(self, cmap = 'gist_earth', norm = 'log', vmin = None):
        """Calls the matplotlib imshow method with preset variables.

        Args:
            cmap (int | str, optional): plt.imshow cmap variable. 
                An int input selects a recommended cmap. Defaults to 'gist_earth'.
            norm (str, optional): plt.imshow norm variable. Defaults to 'log'.

        """
        if isinstance(cmap, int):
            cmap = ['gist_earth', 'gray', 'terrain'][cmap]
        plt.imshow(self.dataset, cmap=cmap, norm=norm, vmin=vmin)
            
    def imshow_gradient(self, axis = 0, cmap = 'seismic', norm = 'linear', vmin = None, alpha = 1):
        plt.imshow(np.gradient(self.dataset)[axis], cmap=cmap, norm=norm, vmin=vmin, alpha=alpha)