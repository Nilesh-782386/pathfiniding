import heapq

def best_first(grid,start,goal):

    rows=len(grid)
    cols=len(grid[0])

    # Priority queue: (cumulative_cost, node)
    # Best First (Uniform Cost / Dijkstra) uses only actual cost as priority
    open_set=[]
    heapq.heappush(open_set,(0,start))

    parent={}
    cost={start:0}

    visited_order=[]
    visited_set=set()

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while open_set:

        current_cost,current=heapq.heappop(open_set)

        # Skip if already processed (stale entry in heap)
        if current in visited_set:
            continue

        visited_set.add(current)
        visited_order.append(current)

        if current==goal:
            break

        for d in directions:

            nx=current[0]+d[0]
            ny=current[1]+d[1]

            if 0<=nx<rows and 0<=ny<cols:

                if grid[nx][ny]==-1:
                    continue

                if (nx,ny) in visited_set:
                    continue

                new_cost=cost[current]+grid[nx][ny]

                if (nx,ny) not in cost or new_cost<cost[(nx,ny)]:

                    cost[(nx,ny)]=new_cost

                    # Priority = only actual cost (no heuristic — this is what makes it Dijkstra/UCS)
                    heapq.heappush(open_set,(new_cost,(nx,ny)))

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