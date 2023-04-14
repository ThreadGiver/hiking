import matplotlib.pyplot as plt
import numpy as np
import pathing
from mapper import Mapper


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
    (3200, 5100)
]

start_coords = canyon_coords[0]
end_coords = canyon_coords[2]

select_map = Mapper('grand_canyon')
select_map.imshow_dataset()
dataset = np.gradient(select_map.dataset)[0]

path = pathing.directional_gradient_a_star(start_coords, end_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')
plt.show()