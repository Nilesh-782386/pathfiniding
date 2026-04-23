import heapq

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid,start,goal):

    rows=len(grid)
    cols=len(grid[0])

    open_set=[]
    heapq.heappush(open_set,(0,start))

    parent={}
    cost={start:0}

    visited_order=[]
    visited_set=set()          # FIX: track finalized nodes to skip stale heap entries

    directions=[(1,0),(-1,0),(0,1),(0,-1)]

    while open_set:

        _,current=heapq.heappop(open_set)

        # FIX: skip if already finalized (stale duplicate in heap)
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

                # FIX: skip already finalized neighbors
                if (nx,ny) in visited_set:
                    continue

                new_cost=cost[current]+grid[nx][ny]

                if (nx,ny) not in cost or new_cost<cost[(nx,ny)]:

                    cost[(nx,ny)]=new_cost

                    priority=new_cost+heuristic((nx,ny),goal)  # FIX: heuristic(node, goal) not heuristic(goal, node) — same result but semantically correct

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