from collections import deque
from typing import List, Tuple, Dict, Set

def bfs(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]):
    """
    Performs Breadth-First Search on a grid.
    Returns the shortest path (by steps) and the order nodes were visited.
    """
    if not grid or not grid[0]:
        return [], []
    if grid[start[0]][start[1]] == -1 or grid[goal[0]][goal[1]] == -1:
        return [], []

    rows=len(grid)
    cols=len(grid[0])

    queue=deque([start])
    visited: Set[Tuple[int, int]] = {start}
    visited_order: List[Tuple[int, int]] = []
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while queue:
        current=queue.popleft()
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
                    parent[(r, c)] = current
                    queue.append((r, c))

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