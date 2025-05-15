from maze import Maze
import random

def adaptive_modification(maze: Maze, player_pos):
    """Modify the maze by adding a wall near the player's position"""
    r, c = player_pos
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)  # Randomize direction selection
    
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < maze.rows and 0 <= nc < maze.cols:
            if maze.grid[nr][nc] == 0 and (nr, nc) != maze.goal:
                maze.grid[nr][nc] = 1
                return