import queue
import numpy as np


coords = tuple[int, int]


def directional_array_neighbors(
        center_node: coords,
        array: list[list[int|float]]
        ) -> set:
    """Returns the neighbors nodes of a node in a an array.
    Args:
        center_node (coords): The node whose neighbors are to be returned.
        array (list[list[int]]): The array in which the nodes are.
    Returns:
        set: The immediate neighbors of allowed values.
    """
    x, y = center_node
    neighbors_set = set()
    for i, j in ((x, y-1), (x, y+1)):
        try:
            if array[0][i][j] != 0:
                neighbors_set.add((i, j))
        except:
            pass
    for i, j in ((x-1, y), (x+1, y)):
        try:
            if array[1][i][j] != 0:
                neighbors_set.add((i, j))
        except:
            pass
    return neighbors_set

def heuristic_cost(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def walk_time(dh, dx):
    """How much time it takes to walk according to dh and dx.

    Args:
        dh (int or float): vertical delta in m 
        dx (int or float): horizontal delta in m

    Returns:
        float: time in h
    """
    return (dx/1000) / (6 * ( np.e ** (-3.5 * abs(dh/dx + 0.05)) ))


def axis_finder(current_node, new_node):
    """Identify on which axis is the delta

    Returns:
        int: The delta axis
    """
    if current_node[0] - new_node[0]:
        return 0
    else:
        return 1

def a_star(
        start_node: coords, 
        end_node: coords, 
        array: list[list[list[int|float]]],
        h_factor = 10,
        dx = 800,
        offroad = True
        ) -> list[coords]:
    """A* pathfinding from start_node to end_node in array.
    Args:
        start_node (tuple of int): starting coordinates.
        end_node (tuple of int): goal coordinates.
        array (list of lists): array to pathfind through.
        h_factor (int) : divides the estimated cost by this number.
        dx (int or float) : real life distance between two cells. Default based on italy map. Grand canyon is about 30.
        offroad (bool) : adjusts for offroad time if the itinerary is offroad
    Returns:
        list: list of node coordinates from (including) start_node to (including) end_node.
    """
    nodes_to_explore = queue.PriorityQueue()
    origin_node = dict()
    g_cost = dict()  # g cost: # of moves from the start_node
    nodes_to_explore.put((0, start_node))
    origin_node[start_node] = None
    g_cost[start_node] = 0


    while not nodes_to_explore.empty():
        current_node = nodes_to_explore.get()
        for new_node in directional_array_neighbors(current_node[1], array):
            axis = axis_finder(current_node[1], new_node)
            new_g_cost = (
                g_cost[current_node[1]] 
                + walk_time(array[axis][current_node[1][0], current_node[1][1]], dx)
            ) 
            # it's currently quite slow since it computes the cost at every cell.
            # Precomputing the cost wasn't successful in improving performance.  
            if (new_node not in g_cost) or (new_g_cost < g_cost[new_node]):
                g_cost[new_node] = new_g_cost
                nodes_to_explore.put((
                    new_g_cost + heuristic_cost(end_node, new_node)/h_factor,
                    new_node
                ))
                origin_node[new_node] = current_node[1]
        if current_node[1] == end_node:
            break
        
    active_node = end_node
    path = [active_node]
    while active_node != start_node:
        active_node = origin_node[active_node]
        path.append(active_node)
    path.reverse()
    if offroad:
        print(round(g_cost[end_node] * 5/3, 2))
    else:
        print(round(g_cost[end_node], 2))
    return path
