import time

from bfs_algorithm import bfs
from dfs_algorithm import dfs
from astar_algorithm import astar
from greedy_best_first import greedy_best_first
from best_first import best_first

def compare_algorithms(grid,start,goal):

    results=[]

    algorithms=[
        ("BFS",bfs),
        ("DFS",dfs),
        ("A*",astar),
        ("Greedy Best First",greedy_best_first),
        ("Best First",best_first)
    ]

    for name,algo in algorithms:

        start_time=time.time()

        path, visited = algo(grid,start,goal)

        execution_time=round(time.time()-start_time,5)

        results.append({
            "algorithm":name,
            "length":len(path),
            "time":execution_time
        })

    return results