import numpy as np
from main import select_map, gradient_to_time
import timeit

dataset1 = gradient_to_time(np.gradient(select_map.dataset)[0])
dataset2 = np.gradient(select_map.dataset)[0]

def walk_speed(slope):
    return 6 * ( np.e ** (-3.5 * abs(slope + 0.05)) )

def statement1(dataset):
    return (dataset[50][50] + dataset[60][60])

def statement2(dataset):
    return (dataset[50, 50] + dataset[60, 60])

def statement3(dataset):
    return (
        800 /walk_speed(dataset[50][50]/800) +
        800 /walk_speed(dataset[60][60]/800)
    )

def statement4(dataset):
    return (
        800 /walk_speed(dataset[50,50]/800) +
        800 /walk_speed(dataset[60,60]/800)
    )

print(
    timeit.timeit(
        stmt='statement1(dataset1)',
        setup='from __main__ import dataset1, statement1',
        number=10000
    ),
    'statement1'
)

print(
    timeit.timeit(
        stmt='statement2(dataset1)',
        setup='from __main__ import dataset1, statement2',
        number=10000
    ),
    'statement2'
)

print(
    timeit.timeit(
        stmt='statement3(dataset2)',
        setup='from __main__ import dataset2, statement3',
        number=10000
    ),
    'statement3'
)

print(
    timeit.timeit(
        stmt='statement4(dataset2)',
        setup='from __main__ import dataset2, statement4',
        number=10000
    ),
    'statement4'
)