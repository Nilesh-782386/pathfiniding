import heapq
from typing import List, Tuple, Dict, Set

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def greedy_best_first(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]):
    """
    Performs Greedy Best-First Search on a grid.
    Returns the path from start to goal and the order in which nodes were visited.
    """
    if not grid or not grid[0]:
        return [], []
    if grid[start[0]][start[1]] == -1 or grid[goal[0]][goal[1]] == -1:
        return [], []

    rows=len(grid)
    cols=len(grid[0])

    open_set=[]
    heapq.heappush(open_set,(0,start))

    visited: Set[Tuple[int, int]] = set([start])
    visited_order: List[Tuple[int, int]] = []

    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while open_set:

        _,current=heapq.heappop(open_set)

        visited_order.append(current)

        if current==goal:
            break

        for d in directions:

            r = current[0] + d[0]
            c = current[1] + d[1]

            if 0 <= r < rows and 0 <= c < cols:

                if grid[r][c] == -1:
                    continue

                if (r, c) not in visited:

                    visited.add((r, c))

                    # Greedy Best First: priority = heuristic ONLY (ignores actual cost)
                    # This is intentional — greedy always heads toward goal by estimate
                    priority=heuristic((r, c), goal)

                    heapq.heappush(open_set,(priority,(r, c)))

                    parent[(r, c)] = current


    path: List[Tuple[int, int]] = []
    node=goal

    while node in parent:
        path.append(node)
        node=parent[node]

    if node!=start:
        return [],visited_order

    path.append(start)
    path.reverse()

    return path,visited_order