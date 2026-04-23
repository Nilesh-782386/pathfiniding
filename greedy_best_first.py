import heapq

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def greedy_best_first(grid,start,goal):

    rows=len(grid)
    cols=len(grid[0])

    open_set=[]
    heapq.heappush(open_set,(0,start))

    visited=set([start])
    visited_order=[]

    parent={}

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while open_set:

        _,current=heapq.heappop(open_set)

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

                    visited.add((nx,ny))

                    # Greedy Best First: priority = heuristic ONLY (ignores actual cost)
                    # This is intentional — greedy always heads toward goal by estimate
                    priority=heuristic((nx,ny),goal)

                    heapq.heappush(open_set,(priority,(nx,ny)))

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