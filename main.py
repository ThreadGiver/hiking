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
    
x = 1000
y = 1000
select_map = Mapper('gc_dem.tif')

path = pathing.a_star((1400,1900), (960,370), select_map.dataset, (0, ))

pathTransposed = np.array(path).T.tolist()

# select_map2 = Mapper('30N000E_20101117_gmted_mea300.tif')

# idk = np.full(select_map2.dataset.shape, np.nan)
# select_map2.dataset[:] = 0
# select_map2.dataset[0] = np.nan
# select_map2.dataset[tuple(pathTransposed)] = 10000

idk = np.zeros(select_map.dataset.shape)
idk[tuple(pathTransposed)] = 1

select_map.imshow_dataset()


# c_white = mpl.colors.colorConverter.to_rgba('yellow',alpha = 0.01)
# c_black= mpl.colors.colorConverter.to_rgba('red',alpha = 1)
# cmap_rb = mpl.colors.LinearSegmentedColormap.from_list('rb_cmap',[c_white,c_black],2)

# plt.imshow(idk, 'hsv', alpha=0.5)

plt.show()