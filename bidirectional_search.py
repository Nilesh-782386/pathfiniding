from collections import deque


def bidirectional_search(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    if start == goal:
        return [start], [start]

    if grid[start[0]][start[1]] == -1 or grid[goal[0]][goal[1]] == -1:
        return [], []

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    start_queue = deque([start])
    goal_queue = deque([goal])

    start_parent = {start: None}
    goal_parent = {goal: None}

    start_visited = {start}
    goal_visited = {goal}

    visited_order = []
    meeting_node = None

    def neighbors(node):
        x, y = node
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != -1:
                yield (nx, ny)

    while start_queue and goal_queue and meeting_node is None:
        # Expand from the start side.
        for _ in range(len(start_queue)):
            current = start_queue.popleft()
            visited_order.append(current)

            for neighbor in neighbors(current):
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

            for neighbor in neighbors(current):
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
    path_start = []
    node = meeting_node
    while node is not None:
        path_start.append(node)
        node = start_parent[node]
    path_start.reverse()

    # Reconstruct path from meeting node to goal.
    path_goal = []
    node = goal_parent[meeting_node]
    while node is not None:
        path_goal.append(node)
        node = goal_parent[node]

    return path_start + path_goal, visited_order
