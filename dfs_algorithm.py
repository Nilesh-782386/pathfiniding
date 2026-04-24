from typing import List, Tuple, Dict, Set

def dfs(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]):
    """
    Performs Depth-First Search on a grid.
    Returns the path from start to goal and the order in which nodes were visited.
    """
    if not grid or not grid[0]:
        return [], []
    if grid[start[0]][start[1]] == -1 or grid[goal[0]][goal[1]] == -1:
        return [], []

    rows=len(grid)
    cols=len(grid[0])

    stack=[start]

    # FIX: Do NOT mark visited when pushing — mark when POPPING
    # Original marked visited on push which can miss valid paths
    # because DFS may push the same node multiple times via different paths
    visited: Set[Tuple[int, int]] = set()
    visited_order: List[Tuple[int, int]] = []

    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while stack:

        current=stack.pop()

        # FIX: skip if already visited (handles duplicates in stack)
        if current in visited:
            continue

        visited.add(current)
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

                    stack.append((r, c))

                    # Only update parent if not yet seen
                    # This keeps the most recent path (DFS behavior)
                    if (r, c) not in parent:
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