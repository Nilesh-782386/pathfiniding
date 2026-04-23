from bfs_algorithm import bfs
from dfs_algorithm import dfs
from astar_algorithm import astar
from greedy_best_first import greedy_best_first
from best_first import best_first


grid = [
    [1, 1, 1, 1],
    [1, -1, -1, 1],
    [1, 1, 1, 1],
    [1, -1, 1, 1],
]
start = (0, 0)
goal = (3, 3)

algos = [
    ("bfs", bfs),
    ("dfs", dfs),
    ("astar", astar),
    ("greedy", greedy_best_first),
    ("best", best_first),
]

for name, fn in algos:
    path, visited = fn(grid, start, goal)
    print(
        name.upper(),
        "path=", path,
        "len=", len(path),
        "visited=", len(visited),
        "goal_reached=", bool(path),
    )
