from collections import deque

def bfs(grid,start,goal):

    rows=len(grid)
    cols=len(grid[0])

    queue=deque([start])

    visited=set([start])
    visited_order=[]

    parent={}

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while queue:

        current=queue.popleft()

        visited_order.append(current)

        if current==goal:
            break

        for d in directions:

            nx=current[0]+d[0]
            ny=current[1]+d[1]

            if 0<=nx<rows and 0<=ny<cols:

                if grid[nx][ny]==-1:
                    continue

                if (nx,ny) not in visited:

                    queue.append((nx,ny))

                    visited.add((nx,ny))

                    # FIX: only set parent once (first time = shortest hop path)
                    # Original was correct here — keeping as-is, BFS guarantees shortest hops
                    parent[(nx,ny)]=current


    path=[]
    node=goal

    while node in parent:
        path.append(node)
        node=parent[node]

    if node!=start:
        return [],visited_order

    path.append(start)
    path.reverse()

    return path,visited_order