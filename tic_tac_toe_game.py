import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 700
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont('monaco', 60)
SMALL_FONT = pygame.font.SysFont('monaco', 40)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')

# Board setup
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = "X"
game_over = False
x_score, o_score = 0, 0


def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, WIDTH), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                    int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


def check_winner():
    global game_over, x_score, o_score

    # Check rows
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            pygame.draw.line(screen, TEXT_COLOR,
                             (15, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                             (WIDTH - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
            game_over = True
            update_score(board[row][0])
            return

    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            pygame.draw.line(screen, TEXT_COLOR,
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15),
                             (col * SQUARE_SIZE + SQUARE_SIZE // 2, WIDTH - 15), 15)
            game_over = True
            update_score(board[0][col])
            return

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        pygame.draw.line(screen, TEXT_COLOR, (15, 15), (WIDTH - 15, WIDTH - 15), 15)
        game_over = True
        update_score(board[0][0])
    elif board[2][0] == board[1][1] == board[0][2] and board[2][0] is not None:
        pygame.draw.line(screen, TEXT_COLOR, (15, WIDTH - 15), (WIDTH - 15, 15), 15)
        game_over = True
        update_score(board[2][0])


def update_score(winner):
    global x_score, o_score
    if winner == "X":
        x_score += 1
    elif winner == "O":
        o_score += 1


def draw_status():
    title = FONT.render("TIC TAC TOE", True, TEXT_COLOR)
    score_text = SMALL_FONT.render(f"X: {x_score}   O: {o_score}", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, WIDTH + 20))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, WIDTH + 80))


def restart():
    global board, player, game_over
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False
    screen.fill(BG_COLOR)
    draw_lines()
    draw_status()


# Main loop
screen.fill(BG_COLOR)
draw_lines()
draw_status()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if clicked_row < BOARD_ROWS and clicked_col < BOARD_COLS:
                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = player
                    check_winner()
                    player = "O" if player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_status()
    pygame.display.update()
