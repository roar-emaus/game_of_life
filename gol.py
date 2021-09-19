import time
from typing import Optional
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
    def __init__(self):
        self.n = None
        self.m = None
        self.grid = None
        self.counter = itertools.count(0)
        self.i_step = next(self.counter)
        self.fig, self.ax = None, None

    def empty_grid_to_file(self, n: int, m: int, name: Optional[str]=None):
        name = name if name is not None else f"{n}x{m}.input"
        with open(name, "w") as f:
            for i in range(n):
                f.write(" ".join("." for _ in range(m)) + "\n")
    
    def grid_from_file(self, name: str): 
        with open(name, 'r') as f:
            grid = []
            for line in f.readlines():
                grid.append(list(map(int, line.replace(".", "0").replace("O", "1").split(' ')))) 
    
        self.grid = np.asarray(grid)
        self.n, self.m = self.grid.shape

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
        fig, ax = plt.subplots(figsize=(19.2, 10.8))
        ax.matshow(self.grid)
        print(self.i_step)
        plt.savefig(f"step_{self.i_step:04d}.png")
        plt.close(fig)

    def generate_pngs(self, steps):
        self.plot_grid()
        for i in range(steps):
            self.step()
            self.plot_grid()

    def init_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(19.2, 10.8))
        self.ln = plt.matshow(self.grid, fignum=0)
        return self.ln
    
    def update_plot(self, i):
        self.step()
        self.ln.set_data(self.grid)
        return [self.ln]

    def run_animation(self, repeat=False, interval=20):

        board.init_plot()
        ani = FuncAnimation(
                self.fig,
                self.update_plot,
                interval=interval,
                blit=True,
                repeat=repeat)

        plt.show()
    
    def print_grid(self):
        for i in range(self.n):
            outrow = str(self.grid[i, :])
            print(outrow.replace("0", ".").replace("1", "O"), end='\r')
        print(" # "*self.n)

    def terminal_animate(self, steps):
        self.print_grid()
        for _ in range(steps):
            self.step()
            self.print_grid()
            time.sleep(0.5)


if __name__ == "__main__":
    board = Board()
    board.grid_from_file("50x50.input")
    board.terminal_animate(100)
    #board.run_animation(interval=20)
    #board.generate_pngs(steps=40)
