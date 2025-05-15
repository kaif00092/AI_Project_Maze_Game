import pygame
import sys
from config import *
from maze import Maze
from player import Player
from ai_engine import adaptive_modification
from game_modes import GameModes

pygame.init()
pygame.display.set_caption("Maze Game")

win = pygame.display.set_mode((WIDTH, HEIGHT + 100))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 36)

def draw_button(surface, text, rect, hover, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
    pygame.draw.rect(surface, hover_color if hover else color, rect, border_radius=5)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2, border_radius=5)  # Border
    txt_surface = font.render(text, True, TEXT_COLOR)
    text_rect = txt_surface.get_rect(center=rect.center)
    surface.blit(txt_surface, text_rect)

def show_message(message, color=TEXT_COLOR, y_offset=0):
    win.fill(PATH_COLOR)
    text = title_font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

def draw_menu():
    win.fill(PATH_COLOR)
    
    title = title_font.render("Maze Game", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    win.blit(title, title_rect)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Singleplayer button
    sp_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 50)
    sp_hover = sp_button.collidepoint(mouse_pos)
    draw_button(win, "Single Player", sp_button, sp_hover)
    
    # Multiplayer button
    mp_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50)
    mp_hover = mp_button.collidepoint(mouse_pos)
    draw_button(win, "Multi Player", mp_button, mp_hover)
    
    pygame.display.update()
    return sp_button, mp_button

def draw_game():
    win.fill(PATH_COLOR)
    
    # Draw maze
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze.grid[r][c] == 1:
                pygame.draw.rect(win, WALL_COLOR, rect)
            pygame.draw.rect(win, (200, 200, 200), rect, 1)
    
    # Draw goal
    gr, gc = maze.goal
    pygame.draw.rect(win, GOAL_COLOR, (gc * CELL_SIZE, gr * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw players
    for player in players:
        if player.active:
            pr, pc = player.position
            pygame.draw.rect(win, player.color, (pc * CELL_SIZE, pr * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw scores
    for i, player in enumerate(players):
        txt = font.render(f"Player {i+1}: {player.score}", True, player.color)
        win.blit(txt, (10 + i * 150, HEIGHT + 10))
    
    # Draw restart button
    mouse_pos = pygame.mouse.get_pos()
    restart_button = pygame.Rect(WIDTH//2 - 50, HEIGHT + 50, 100, 40)
    hover = restart_button.collidepoint(mouse_pos)
    draw_button(win, "Menu", restart_button, hover)
    
    pygame.display.update()
    return restart_button

def check_game_end():
    active_players = [p for p in players if p.active]
    
    # Check if any player reached the goal
    for i, player in enumerate(players):
        if player.is_at_goal(maze):
            player.winner = True
            show_message(f"Player {i+1} Wins!", WINNER_COLOR)
            return True
    
    # Check if only one player remains
    if len(active_players) == 1 and len(players) > 1:
        winner_idx = next(i for i, p in enumerate(players) if p.active)
        players[winner_idx].winner = True
        show_message(f"Player {winner_idx+1} Wins!", WINNER_COLOR)
        return True
    
    # Check if all players are stuck
    if not active_players:
        show_message("Game Over - No Winners!", (255, 0, 0))
        return True
    
    return False

def reset_game(mode):
    global maze, players, turn_counter, current_player_index, game_over
    maze = Maze()
    
    if mode == "single":
        players = GameModes.singleplayer()
    else:
        players = GameModes.multiplayer()
    
    turn_counter = 0
    current_player_index = 0
    game_over = False

def main_menu():
    while True:
        sp_button, mp_button = draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sp_button.collidepoint(event.pos):
                    return "single"
                elif mp_button.collidepoint(event.pos):
                    return "multi"

def game_loop():
    global current_player_index, turn_counter, game_over
    
    MODIFY_EVERY = 3  # Modify maze every 3 moves
    
    while True:
        clock.tick(FPS)
        restart_button = draw_game()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return  # Return to main menu
        
        if not game_over:
            keys = pygame.key.get_pressed()
            direction = None
            if keys[pygame.K_UP]:
                direction = (-1, 0)
            elif keys[pygame.K_DOWN]:
                direction = (1, 0)
            elif keys[pygame.K_LEFT]:
                direction = (0, -1)
            elif keys[pygame.K_RIGHT]:
                direction = (0, 1)
            
            if direction:
                player = players[current_player_index]
                moved = player.move(direction, maze)
                
                if moved:
                    turn_counter += 1
                    
                    # Adaptive maze modification
                    if turn_counter % MODIFY_EVERY == 0:
                        adaptive_modification(maze, player.position)
                    
                    # Switch player in multiplayer mode
                    if len(players) > 1:
                        current_player_index = (current_player_index + 1) % len(players)
                    
                    # Check if players have moves
                    for p in players:
                        if not p.has_moves(maze):
                            p.active = False
                    
                    game_over = check_game_end()

# Main game loop
while True:
    game_mode = main_menu()
    reset_game(game_mode)
    game_loop()