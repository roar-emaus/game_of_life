import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Board:
    """
    Any live cell with two or three live neighbours survives.
    Any dead cell with three live neighbours becomes a live cell.
    All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    """
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = np.zeros(shape=(n, m), dtype=int)
        self.counter = itertools.count()
        self.i_step = 0

    def initialise_mid(self):
        mid_row = self.n//2
        mid_col = self.m//2
        self.grid[mid_row, mid_col] = 1
        self.grid[mid_row, mid_col + 1] = 1
        self.grid[mid_row, mid_col - 1] = 1
        self.grid[mid_row + 1, mid_col] = 1

    def initialise_every_other_row(self):
        for i in range(self.n//2):
            self.grid[i*2, :] = 1

    def initialise_every_other_col(self):
        for j in range(int(np.round(self.m/2))):
            self.grid[:, j*2] = 1

    def find_neighbours(self, i, j):
        above_row = i - 1
        below_row = i + 1
        left_col = j - 1
        right_col = j + 1
        valid_neighbours = []
        if above_row >= 0:
            if left_col >= 0:
                valid_neighbours.append([above_row, left_col])

            valid_neighbours.append([above_row, j])
            
            if right_col < self.m:
                valid_neighbours.append([above_row, right_col])

        if left_col >= 0:
            valid_neighbours.append([i, left_col])

        if right_col < self.m:
            valid_neighbours.append([i, right_col])

        if below_row < self.n:
            if left_col >= 0:
                valid_neighbours.append([below_row, left_col])
            
            valid_neighbours.append([below_row, j])

            if right_col < self.m:
                valid_neighbours.append([below_row, right_col])

        return valid_neighbours

    def step(self):
        grid = np.copy(self.grid)
        for i in range(self.n):
            for j in range(self.m):
                valid_neighbours = self.find_neighbours(i=i, j=j)
                neigh_val = np.asarray(
                        [self.grid[ii, jj] for ii, jj in valid_neighbours]
                )
                neigh_sum = np.sum(neigh_val)
                if neigh_sum == 3:
                    grid[i, j] = 1
                elif neigh_sum < 2 or neigh_sum > 3:
                    grid[i, j] = 0
        self.grid = grid
        self.i_step = next(self.counter)

    def plot_grid(self):
        self.ax.matshow(self.grid)
        plt.savefig(f"step_{self.i_step:04d}.png")
        plt.close(fig)

    def init_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(19.2, 10.8))
        self.ln = plt.matshow(self.grid, fignum=0)
        return self.ln
    
    def update_plot(self, i):
        self.step()
        self.ln.set_data(self.grid)
        return [self.ln]



board = Board(100, 100)
board.initialise_mid()
board.initialise_every_other_row()
#board.initialise_every_other_col()
board.init_plot()
ani = FuncAnimation(board.fig, board.update_plot, frames=range(10),
                    interval=20, blit=True)
plt.show()








