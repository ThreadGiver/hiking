import matplotlib.pyplot as plt
import numpy as np
import pathing
from mapper import Mapper


def walk_speed(slope):
    return 6 * ( np.e ** (-3.5 * abs(slope + 0.05)) )

select_map = Mapper('italy300')
select_map.imshow_gradient()

path = pathing.a_star((1400,1900), (960,370), select_map.dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')

plt.show()
