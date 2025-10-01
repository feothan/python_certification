# Filename: grid_game.py

import pygame
import random

# --- Setup ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6, 6
TILE_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 150, 255)
GREEN = (50, 255, 150)
RED = (255, 100, 100)
BLACK = (0, 0, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Game")
clock = pygame.time.Clock()

# --- Grid Initialization ---
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid[0] = [-3, -2, -1, -1, -2, -3]  # Enemies
grid[5] = [1, 2, 3, 4, 2, 1]        # Player pieces

selected = None
valid_moves = []
player_turn = True

# --- Helper Functions ---
def is_on_board(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def get_valid_moves(piece_type, row, col):
    moves = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        # Straight move
        r = row + dr * piece_type
        c = col + dc * piece_type
        if is_on_board(r, c):
            moves.add((r, c))
        # Turned (knight-like) moves
        for i in range(1, piece_type):
            mid_r = row + dr * i
            mid_c = col + dc * i
            if not is_on_board(mid_r, mid_c): continue
            remaining = piece_type - i
            for tdr, tdc in [(-dc, dr), (dc, -dr)]:
                end_r = mid_r + tdr * remaining
                end_c = mid_c + tdc * remaining
                if is_on_board(end_r, end_c):
                    moves.add((end_r, end_c))
    return list(moves)

def draw_grid(hovered=None):
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if hovered == (r, c) and (r, c) in valid_moves:
                pygame.draw.rect(win, GREEN, rect)
            else:
                pygame.draw.rect(win, GRAY, rect, 1)

            val = grid[r][c]
            if val != 0:
                color = RED if val < 0 else BLUE
                pygame.draw.circle(win, color, rect.center, TILE_SIZE//3)
                font = pygame.font.SysFont(None, 24)
                text = font.render(str(abs(val)), True, BLACK)
                win.blit(text, text.get_rect(center=rect.center))

def get_hover_tile():
    mx, my = pygame.mouse.get_pos()
    r, c = my // TILE_SIZE, mx // TILE_SIZE
    return (r, c) if is_on_board(r, c) else (None, None)

def update_enemy_states():
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] < 0:
                grid[r][c] -= 1
                if grid[r][c] < -3:
                    grid[r][c] = -1

def enemy_turn():
    enemies = [(r, c, grid[r][c]) for r in range(ROWS) for c in range(COLS) if grid[r][c] < 0]
    best_score = -float('inf')
    best_move = None

    for r, c, val in enemies:
        moves = get_valid_moves(2, r, c)
        for mr, mc in moves:
            if not is_on_board(mr, mc):
                continue
            target = grid[mr][mc]
            score = 0
            if val == -3 and target > 0:
                score = 100
            elif target == 0:
                score = 10 - abs(mr - 5)
            if score > best_score:
                best_score = score
                best_move = ((r, c), (mr, mc))

    if best_move:
        (sr, sc), (er, ec) = best_move
        if grid[er][ec] > 0 and grid[sr][sc] == -3:
            grid[er][ec] = 0
        grid[er][ec] = grid[sr][sc]
        grid[sr][sc] = 0

def check_game_over():
    player_pieces = any(grid[r][c] > 0 for r in range(ROWS) for c in range(COLS))
    enemy_pieces = any(grid[r][c] < 0 for r in range(ROWS) for c in range(COLS))
    if not player_pieces:
        print("You lost!")
        return True
    if not enemy_pieces:
        print("You won!")
        return True
    return False

# --- Game Loop ---
running = True
while running:
    clock.tick(60)
    win.fill(WHITE)
    hovered = get_hover_tile()
    draw_grid(hovered)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            row, col = hovered
            if row is not None:
                if selected:
                    if (row, col) in valid_moves:
                        sr, sc = selected
                        if grid[row][col] < 0 and grid[row][col] == -3:
                            grid[row][col] = 0
                            grid[sr][sc] = 0
                        else:
                            grid[row][col] = grid[sr][sc]
                            grid[sr][sc] = 0
                        selected = None
                        valid_moves = []
                        player_turn = False
                elif grid[row][col] > 0:
                    selected = (row, col)
                    valid_moves = get_valid_moves(grid[row][col], row, col)

    if not player_turn:
        update_enemy_states()
        enemy_turn()
        player_turn = True
        if check_game_over():
            pygame.time.wait(3000)
            running = False

    pygame.display.flip()

pygame.quit()