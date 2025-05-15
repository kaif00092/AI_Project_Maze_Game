import numpy as np
from config import ROWS, COLS

class Maze:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.grid = np.zeros((ROWS, COLS), dtype=int)
        self.goal = (ROWS - 1, COLS - 1)
        self.place_walls()

    def place_walls(self):
        """Place random walls ensuring players and goal are accessible"""
        wall_count = 0
        max_walls = (ROWS * COLS) // 5  # 20% walls
        
        while wall_count < max_walls:
            r, c = np.random.randint(ROWS), np.random.randint(COLS)
            if (r, c) != (0, 0) and (r, c) != self.goal and self.grid[r][c] == 0:
                self.grid[r][c] = 1
                wall_count += 1

    def is_valid_position(self, position):
        r, c = position
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 0