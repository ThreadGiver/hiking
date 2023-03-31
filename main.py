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
    output *= 6
    output = 800 / output
    return output

select_map = Mapper('italy300', remove_zeroes=True)
select_map.imshow_dataset()

# print(gradient_to_time(np.gradient(select_map.dataset)[0]))

# (1620,2692)
# (1400,1900)
# (960,370)

time0 = time.time()
dataset = gradient_to_time(np.gradient(select_map.dataset)[0])
time1 = time.time()
print(time1-time0)

path = pathing.time_a_star((900,370), (960,370), dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')
time2 = time.time()
print(time2-time1)

plt.show()

select_map = Mapper('italy300')
select_map.imshow_dataset()

time3 = time.time()
path = pathing.gradient_a_star((900,370), (960,370), np.gradient(select_map.dataset)[0])
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')
time4 = time.time()
print(time4-time3)
plt.show()