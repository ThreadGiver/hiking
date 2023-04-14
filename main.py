import matplotlib.pyplot as plt
import numpy as np
import pathing
from mapper import Mapper

import time

def gradient_to_time(array, dx=800):
    output = array / dx
    output += 0.05
    output = np.abs(output)
    output *= -3.5
    output = np.e ** output
    output *= 6 # 6km/h is the max speed
    output = (dx/1000) / output # /1000 if dx with dx in m, if you don't divide it takes wayyy longer
    return output


# end_coords = (600, 300)
# end_coords = (700, 500)
end_coords = (1400, 1900)
start_coords = (960,370)


# (1620,2692)
# (1400,1900)
# (960,370)

select_map = Mapper('italy300', replace_zeroes=True)
select_map.imshow_dataset()

time6 = time.time()
dataset = gradient_to_time(np.gradient(select_map.dataset)[0])
time7 = time.time()
print(time7-time6, 'prep time A star - replace zeroes')

path = pathing.time_a_star(end_coords, start_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')
time8 = time.time()
print(time8-time7, 'time A star - replace zeroes - r')


select_map = Mapper('italy300')
select_map.imshow_dataset()
dataset = np.gradient(select_map.dataset)[0]

time9 = time.time()
path = pathing.gradient_a_star(end_coords, start_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='c')
time10 = time.time()
print(time10-time9, 'gradient A star - c')
plt.show()