import matplotlib.pyplot as plt
import numpy as np
import pathing
from mapper import Mapper


select_map = Mapper('italy300')
select_map.imshow_dataset()

# (1620,2692)
path = pathing.gradient_a_star((1400,1900), (960,370), np.gradient(select_map.dataset)[0])
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')

plt.show()
