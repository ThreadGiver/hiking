import matplotlib.pyplot as plt
import numpy as np
import pathing
from mapper import Mapper

import time

italy_coords = [
    (1400, 1900),
    (960,370),
    (1620,2692),
    (600, 300),
    (700, 500)
]

canyon_coords = [
    (3800, 1900),
    (3400, 2100),
    (3200, 2500),
    (2500, 3900),
    (3200, 5100),
    (3700, 2000)
]

start_coords = canyon_coords[2]
end_coords = canyon_coords[1]

select_map = Mapper('grand_canyon')
select_map.crop(200, 200, select_map.width-400, select_map.height-400)
select_map.imshow_gradient(axis=0)
select_map.imshow_gradient(axis=1, alpha=0.5)

time1 = time.time()
dataset = np.gradient(select_map.dataset)

path = pathing.directional_gradient_a_star(start_coords, end_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')
time2 = time.time()
print(time2-time1, 'Directional red')


time3 = time.time()
dataset = np.gradient(select_map.dataset)[0]

path = pathing.gradient_a_star(start_coords, end_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='g')
time4 = time.time()
print(time4-time3, 'y green')


time5 = time.time()
dataset = np.gradient(select_map.dataset)[1]

path = pathing.gradient_a_star(start_coords, end_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='c')
time6 = time.time()
print(time6-time5, 'x cyan')


plt.show()