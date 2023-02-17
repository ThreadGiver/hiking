import queue


def neighbors(center_node: tuple[int], array: list[list[int]],
              excluded_values: tuple[int]) -> set:
    """Returns the neighbors of a node in a an array.
    Args:
        center_node (tuple[int]): The node whose neighbors are to be returned.
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

def breadth_first_map(array, start_node, wall_values: tuple[int]):
    """Explores an array
    Args:
        array (list[list[int]]): Array to explore.
        start_node ([type]): A reachable node.
        wall_values (tuple[int], optional): Values which exclude a node from 
            being a neighbor.
    Returns:
        set: Reachable nodes.
    """
    nodes_to_explore = queue.Queue()
    explored_nodes = set()
    nodes_to_explore.put(start_node)

    while not nodes_to_explore.empty():
        current_node = nodes_to_explore.get()
        for new_node in neighbors(current_node, array, wall_values):
            if new_node not in explored_nodes:
                nodes_to_explore.put(new_node)
            explored_nodes.add(current_node)
    
    return explored_nodes



def heuristic_cost(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

coordinates = tuple[int, int]
def a_star(start_node: coordinates, end_node: coordinates, 
           array: list[list[int]], wall_values: tuple[int] = 1) -> list[coordinates]:
    """A* pathfinding from start_node to end_node in an array.
    Args:
        start_node (tuple of int): starting coordinates.
        end_node (tuple of int): goal coordinates.
        array (list of lists): array to pathfind through
        wall_values (tuple of int) : node values in the array that can't be navigated.
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
        for new_node in neighbors(current_node[1], array, wall_values):
            new_g_cost = g_cost[current_node[1]] + 1
            if new_node not in g_cost or new_g_cost < g_cost[new_node]:
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