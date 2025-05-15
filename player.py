from pathfinding import a_star

class Player:
    def __init__(self, start_pos, color):
        self.position = start_pos
        self.color = color
        self.score = 0
        self.active = True
        self.winner = False

    def move(self, direction, maze):
        if not self.active:
            return False
        
        r, c = self.position
        dr, dc = direction
        nr, nc = r + dr, c + dc
        
        if maze.is_valid_position((nr, nc)):
            self.position = (nr, nc)
            self.score += 1
            return True
        return False

    def has_moves(self, maze):
        r, c = self.position
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if maze.is_valid_position((nr, nc)):
                return True
        return False

    def is_at_goal(self, maze):
        return self.position == maze.goal