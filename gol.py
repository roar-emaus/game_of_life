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
        self.counter = itertools.count(0)
        self.i_step = next(self.counter)
        self.fig, self.ax = None, None

    def _create_glider(self, direction='down_right'):
        glider = np.array([
                    [0, 1, 0],
                    [0, 0, 1],
                    [1, 1, 1],
                    ])
        if direction == 'down_right':
            return glider
        elif direction == 'up_right':
            return np.rot90(glider)
        elif direction == 'down_left':
            return np.rot90(np.rot90(np.rot90(glider)))
        elif direction == 'up_left':
            return np.rot90(np.rot90(glider))
    
    def _create_cross(self):
        return np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
            ])

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

    def initialise_colliding_gliders(self):
        mid_row = self.n//2
        mid_col = self.m//2
        down_right = self._create_glider(direction='down_right')
        down_left = self._create_glider(direction='down_left')
        up_right = self._create_glider(direction='up_right')
        up_left = self._create_glider(direction='up_left')
        self.grid[0:3, 0:3] = down_right
        self.grid[self.n-3:self.n, 0:3] = up_right
        self.grid[self.n-3:self.n, self.m-3:self.m] = up_left
        self.grid[0:3, self.m-3:self.m] = down_left

        cross = self._create_cross()
        self.grid[mid_row-1:mid_row+2, mid_col-1:mid_col+2] = cross


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
        from matplotlib import rcParams

        # configure full path for ImageMagick
        rcParams['animation.convert_path'] = r'/usr/bin/convert'

        board.init_plot()
        ani = FuncAnimation(
                self.fig,
                self.update_plot,
                interval=interval,
                blit=True,
                repeat=repeat)

        plt.show()
    
if __name__ == "__main__":
    board = Board(20, 20)
    #board.initialise_mid()
    #board.initialise_every_other_row()
    #board.initialise_every_other_col()
    board.initialise_colliding_gliders()
    #board.run_animation()
    board.generate_pngs(steps=40)
