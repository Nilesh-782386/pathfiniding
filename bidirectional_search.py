from collections import deque
from typing import List, Tuple, Dict, Set, Optional, Generator

def bidirectional_search(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]):
    """
    Performs Bidirectional BFS on a grid.
    Returns the path from start to goal and the order in which nodes were visited.
    """
    if not grid or not grid[0]:
        return [], []
        
    rows = len(grid)
    cols = len(grid[0])

    if start == goal:
        return [start], [start]

    if grid[start[0]][start[1]] == -1 or grid[goal[0]][goal[1]] == -1:
        return [], []

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    start_queue = deque([start])
    goal_queue = deque([goal])

    start_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    goal_parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {goal: None}

    start_visited: Set[Tuple[int, int]] = {start}
    goal_visited: Set[Tuple[int, int]] = {goal}

    visited_order: List[Tuple[int, int]] = []
    meeting_node: Optional[Tuple[int, int]] = None

    def get_neighbors(node: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
        r, c = node
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != -1:
                yield (nr, nc)

    while start_queue and goal_queue and meeting_node is None:
        # Expand from the start side.
        for _ in range(len(start_queue)):
            current = start_queue.popleft()
            visited_order.append(current)

            for neighbor in get_neighbors(current):
                if neighbor in start_visited:
                    continue

                start_visited.add(neighbor)
                start_parent[neighbor] = current
                start_queue.append(neighbor)

                if neighbor in goal_visited:
                    meeting_node = neighbor
                    break
            if meeting_node is not None:
                break

        if meeting_node is not None:
            break

        # Expand from the goal side.
        for _ in range(len(goal_queue)):
            current = goal_queue.popleft()
            visited_order.append(current)

            for neighbor in get_neighbors(current):
                if neighbor in goal_visited:
                    continue

                goal_visited.add(neighbor)
                goal_parent[neighbor] = current
                goal_queue.append(neighbor)

                if neighbor in start_visited:
                    meeting_node = neighbor
                    break
            if meeting_node is not None:
                break

    if meeting_node is None:
        return [], visited_order

    # Reconstruct path from start to meeting node.
    path_start: List[Tuple[int, int]] = []
    curr: Optional[Tuple[int, int]] = meeting_node
    while curr is not None:
        path_start.append(curr)
        curr = start_parent[curr]
    path_start.reverse()

    # Reconstruct path from meeting node to goal.
    path_goal: List[Tuple[int, int]] = []
    curr = goal_parent[meeting_node]
    while curr is not None:
        path_goal.append(curr)
        curr = goal_parent[curr]

    return path_start + path_goal, visited_order
