import rasterio
from rasterio.windows import Window
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import pathing


class Mapper():
    def __init__(self, file_name, remove_zeroes=False, min_zero=True) -> None:
        self.file = rasterio.open(f'data/{file_name}')
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
            
    def imshow_gradient(self, cmap = 'seismic', norm = 'linear', vmin = None):
        plt.imshow(np.gradient(self.dataset)[0], cmap=cmap, norm=norm, vmin=vmin)
    

select_map = Mapper('30N000E_20101117_gmted_mea300.tif')
select_map.imshow_dataset()

path = pathing.a_star((1400,1900), (960,370), select_map.dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')

plt.show()