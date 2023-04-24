import matplotlib.pyplot as plt
import numpy as np
import pathing
from mapper import Mapper


italy300_coords = [
    (1400, 1900), # Ceramida, Italy - end
    (960,370), # Verges, Spain - start
    (1620,2692),
    (600, 300),
    (700, 400)
]

italy075_coords = [
    (2670, 4200),
    (5300, 7800)
]

canyon_coords = [
    (3680, 1670), # start
    (3320, 2240),
    (3030, 2560), # end
    (2500, 3900),
    (3200, 5100),
    (3600, 2000)
]

start_coords = italy300_coords[0]
end_coords = italy300_coords[1]

select_map = Mapper('italy300')
select_map.imshow_dataset()

dataset = np.gradient(select_map.dataset)

path = pathing.a_star(start_coords, end_coords, dataset)
path_transposed = np.array(path).T.tolist()
plt.plot(path_transposed[1], path_transposed[0], c='r')

plt.show()