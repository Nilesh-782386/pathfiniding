def dfs(grid,start,goal):

    rows=len(grid)
    cols=len(grid[0])

    stack=[start]

    # FIX: Do NOT mark visited when pushing — mark when POPPING
    # Original marked visited on push which can miss valid paths
    # because DFS may push the same node multiple times via different paths
    visited=set()
    visited_order=[]

    parent={}

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

            nx=current[0]+d[0]
            ny=current[1]+d[1]

            if 0<=nx<rows and 0<=ny<cols:

                if grid[nx][ny]==-1:
                    continue

                if (nx,ny) not in visited:

                    stack.append((nx,ny))

                    # Only update parent if not yet seen
                    # This keeps the most recent path (DFS behavior)
                    if (nx,ny) not in parent:
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