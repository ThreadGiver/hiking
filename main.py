import rasterio
from rasterio.windows import Window
import matplotlib.pyplot as plt
import numpy as np


class Idk():
    def __init__(self, file_name, remove_zeroes=False) -> None:
        self.file = rasterio.open(f'data/{file_name}')
        self.dataset = self.file.read(1)
        self.height = self.dataset.shape[0]
        self.width = self.dataset.shape[1]

        if remove_zeroes:
            self.dataset = np.ma.masked_where(self.dataset == 0, self.dataset)


    def crop(self, col_off: int, row_off: int, width: int, height: int):
        """Crops the dataset

        Args:
            col_off (int): column offset
            row_off (int): row offset
            width (int): crop to width
            height (int): crop to height
        """
        self.dataset = self.file.read(1, window=Window(col_off, row_off, width, height))
    
    def imshow(self, cmap: int | str = 0, norm='log'):
        """Calls the matplotlib imshow method with preset variables.

        Args:
            cmap (int | str, optional): plt.imshow cmap var. Defaults to 0.
            norm (str, optional): plt.imshow norm var. Defaults to 'log'.
        """
        if isinstance(cmap, int):
            cmap = ['gist_earth', 'gray', 'terrain'][cmap]
        
        plt.imshow(self.dataset, cmap=cmap, norm=norm)


italy = Idk('30N000E_20101117_gmted_mea300.tif')

italy.imshow()

plt.show()
