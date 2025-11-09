import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (96, 216, 232)
LOCKED_CELL_COLOR = (189, 189, 189)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Fonts
font = pygame.font.SysFont('monaco', 40)
title_font = pygame.font.SysFont('monaco', 50, bold=True)
info_font = pygame.font.SysFont('monaco', 30)

# Board setup (0 = empty)
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

# Keep track of fixed cells
fixed_cells = [[cell != 0 for cell in row] for row in board]

# Constants
CELL_SIZE = WIDTH // 9

# Variables
selected = None
start_time = time.time()


# Helper Functions
def draw_grid():
    for x in range(9):
        if x % 3 == 0:
            line_width = 4
        else:
            line_width = 1
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 60), (x * CELL_SIZE, HEIGHT - 60), line_width)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE + 60), (WIDTH, x * CELL_SIZE + 60), line_width)


def draw_numbers():
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                color = LOCKED_CELL_COLOR if fixed_cells[i][j] else BLACK
                text = font.render(str(num), True, color)
                screen.blit(text, (j * CELL_SIZE + 20, i * CELL_SIZE + 70))


def highlight_cell(row, col):
    pygame.draw.rect(screen, LIGHTBLUE, (col * CELL_SIZE, row * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE))


def is_valid(num, row, col):
    # Row and column check
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # 3x3 box check
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def draw_header():
    # Title
    title = title_font.render("SUDOKU", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 25))
    screen.blit(title, title_rect)

    # Timer
    elapsed_time = int(time.time() - start_time)
    minutes, seconds = divmod(elapsed_time, 60)
    timer = info_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
    screen.blit(timer, (WIDTH - 150, 25))

    # Score (number of filled cells)
    filled_cells = sum(1 for row in board for val in row if val != 0)
    score = info_font.render(f"Score: {filled_cells}", True, BLACK)
    screen.blit(score, (20, 25))


def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(WHITE)
    screen.blit(overlay, (0, 0))
    text = title_font.render("CONGRATULATIONS!", True, GREEN)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(3000)


def is_game_complete():
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
    return True


# Main Game Loop
running = True
while running:
    screen.fill(WHITE)
    draw_header()
    draw_grid()

    if selected:
        highlight_cell(selected[0], selected[1])
    draw_numbers()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif selected and not fixed_cells[selected[0]][selected[1]]:
                row, col = selected
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    if is_valid(num, row, col):
                        board[row][col] = num
                    else:
                        # Flash red if invalid
                        pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE))
                        pygame.display.update()
                        pygame.time.wait(150)
                elif event.key == pygame.K_BACKSPACE:
                    board[row][col] = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 60 < y < HEIGHT - 60:
                selected = ((y - 60) // CELL_SIZE, x // CELL_SIZE)

    if is_game_complete():
        draw_game_over()
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
