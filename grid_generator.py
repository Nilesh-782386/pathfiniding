import numpy as np
import random

GRID_SIZE = 50

def generate_grid():

    grid = np.ones((GRID_SIZE, GRID_SIZE))

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            r = random.random()

            if r < 0.1:
                grid[i][j] = -1

            elif r < 0.2:
                grid[i][j] = 5

            else:
                grid[i][j] = 1

    return grid.tolist()