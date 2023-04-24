import queue
import numpy as np


coords = tuple[int, int]


def array_neighbors(center_node: coords,
                    array: list[list[int|float]],
                    excluded_values: tuple) -> set:
    """Returns the neighbors nodes of a node in a an array.
    Args:
        center_node (coords): The node whose neighbors are to be returned.
        array (list[list[int]]): The array in which the nodes are.
        excluded_values (tuple): Values which exclude a node from being a neighbor.
    Returns:
        set: The immediate neighbors of allowed values.
    """
    x, y = center_node
    neighbors_set = set()
    for i, j in ((x-1, y), (x, y-1), (x+1, y), (x, y+1)):
        try:
            if array[i][j] not in excluded_values:
                neighbors_set.add((i, j))
        except:
            pass
    return neighbors_set

def directional_array_neighbors(center_node: coords,
                    array: list[list[int|float]],
                    excluded_values: tuple) -> set:
    """Returns the neighbors nodes of a node in a an array.
    Args:
        center_node (coords): The node whose neighbors are to be returned.
        array (list[list[int]]): The array in which the nodes are.
        excluded_values (tuple): Values which exclude a node from being a neighbor.
    Returns:
        set: The immediate neighbors of allowed values.
    """
    x, y = center_node
    neighbors_set = set()
    for i, j in ((x, y-1), (x, y+1)):
        try:
            if array[0][i][j] not in excluded_values:
                neighbors_set.add((i, j))
        except:
            pass
    for i, j in ((x-1, y), (x+1, y)):
        try:
            if array[1][i][j] not in excluded_values:
                neighbors_set.add((i, j))
        except:
            pass
    return neighbors_set

def breadth_first_map(array, start_node: coords, unreachable_values: tuple):
    """Explores an array
    Args:
        array (list[list[int]]): Array to explore.
        start_node ([type]): A reachable node.
        unreachable_values (tuple[int], optional): Values which can't be reached.
    Returns:
        set: Reachable nodes.
    """
    nodes_to_explore = queue.Queue()
    explored_nodes = set()
    nodes_to_explore.put(start_node)

    while not nodes_to_explore.empty():
        current_node = nodes_to_explore.get()
        for new_node in array_neighbors(current_node, array, unreachable_values):
            if new_node not in explored_nodes:
                nodes_to_explore.put(new_node)
            explored_nodes.add(current_node)
    
    return explored_nodes



def heuristic_cost(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_cost2(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]))/100

def a_star(start_node: coords, 
           end_node: coords, 
           array: list[list[int|float]],
           unreachable_values: tuple = (0,)
           ) -> list[coords]:
    """A* pathfinding from start_node to end_node in an array.
    Args:
        start_node (tuple of int): starting coordinates.
        end_node (tuple of int): goal coordinates.
        array (list of lists): array to pathfind through.
        unreachable_values (tuple of int) : node values in the array that can't be navigated.
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
        for new_node in array_neighbors(current_node[1], array, unreachable_values):
            new_g_cost = g_cost[current_node[1]] + 1
            if (new_node not in g_cost) or (new_g_cost < g_cost[new_node]):
                g_cost[new_node] = new_g_cost
                nodes_to_explore.put((new_g_cost + heuristic_cost(end_node, new_node),
                                      new_node))
                origin_node[new_node] = current_node[1]
        if current_node[1] == end_node:
            break
    
    active_node = end_node
    path = [active_node]
    while active_node != start_node:
        active_node = origin_node[active_node]
        path.append(active_node)
    path.reverse()
    return path

def walk_speed(slope):
    return 6 * ( np.e ** (-3.5 * abs(slope + 0.05)) )
    # km/h

def axis_finder(current_node, new_node):
    if current_node[0] - new_node[0]:
        return 0
    else:
        return 1


def directional_gradient_a_star(start_node: coords, 
           end_node: coords, 
           array: list[list[list[int|float]]],
           unreachable_values: tuple = (0,),
           h_cost_divider = 100,
           dx = 800
           ) -> list[coords]:
    """A* pathfinding from start_node to end_node in an array.
    Args:
        start_node (tuple of int): starting coordinates.
        end_node (tuple of int): goal coordinates.
        array (list of lists): array to pathfind through.
        unreachable_values (tuple of int) : node values in the array that can't be navigated.
        h_cost_divider (int) : divides the estimated cost by this number.
        dx (in or float) : real life distance between two cells.
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
        for new_node in directional_array_neighbors(current_node[1], array, unreachable_values):
            axis = axis_finder(current_node[1], new_node)
            new_g_cost = (g_cost[current_node[1]] 
                          + ((dx/1000) / walk_speed(
                                array[axis][current_node[1][0], current_node[1][1]] / dx
                            ))
                         ) 
                        # it's currently quite slow since it computes the cost at every cell.
                        # Precomputing the cost wasn't successful in improving performance.  
            if (new_node not in g_cost) or (new_g_cost < g_cost[new_node]):
                g_cost[new_node] = new_g_cost
                nodes_to_explore.put((new_g_cost + heuristic_cost(end_node, new_node)/h_cost_divider,
                                      new_node))
                origin_node[new_node] = current_node[1]
        if current_node[1] == end_node:
            break
        
    active_node = end_node
    path = [active_node]
    while active_node != start_node:
        active_node = origin_node[active_node]
        path.append(active_node)
    path.reverse()
    print(round(g_cost[end_node], 2))
    return path
