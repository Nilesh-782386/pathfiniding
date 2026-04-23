from bfs_algorithm import bfs
from dfs_algorithm import dfs
from astar_algorithm import astar
from greedy_best_first import greedy_best_first
from bidirectional_search import bidirectional_search


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
    ("bidirectional", bidirectional_search),
    ("greedy", greedy_best_first),
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
