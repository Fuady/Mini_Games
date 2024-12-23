import pygame
import sys
import random
import time

# Initialize Pygame
check_errors = pygame.init()
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting...".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) Pygame successfully initialized!")

pygame.font.init()

# Initialize the game board
SIZE = 4

# Screen Parameters
width = 600
height = 600
trans_x = 100
trans_y = 100
box_w = 100
box_h = 100
gap = 10

# Colors
def get_color_dic():
    return {
        'gray': (187, 173, 160),
        'white': (238, 228, 218),
        'light_yellow': (237, 224, 200),
        'sandy_brown': (242, 177, 121),
        'coral': (245, 149, 99),
        'tomato': (246, 124, 95),
        'red': (246, 94, 59),
        'yellow_1': (237, 207, 114),
        'yellow_2': (237, 204, 97),
        'yellow_3': (237, 200, 80),
        'green': (119, 173, 101),
        'blue': (36, 113, 163),
        'black': (0, 0, 0)
    }

color_dic = get_color_dic()

# Screen
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048 Game!')

# Board Movement

def slide_and_merge_left(board):
    new_board = [[0] * SIZE for _ in range(SIZE)]
    score_increment = 0
    for i in range(SIZE):
        pos = 0
        for j in range(SIZE):
            if board[i][j] != 0:
                if new_board[i][pos] == 0:
                    new_board[i][pos] = board[i][j]
                elif new_board[i][pos] == board[i][j]:
                    new_board[i][pos] *= 2
                    score_increment += new_board[i][pos]
                    pos += 1
                else:
                    pos += 1
                    new_board[i][pos] = board[i][j]
    return new_board, score_increment

def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

def move(board, direction):
    for _ in range(direction):
        board = rotate_board(board)
    board, score_increment = slide_and_merge_left(board)
    for _ in range(-direction % 4):
        board = rotate_board(board)
    return board, score_increment

def add_new_number(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def can_move(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return True
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return True
    return False


# Colors

def ColorChange(num):
    return {
        0: 'gray',
        2: 'white',
        4: 'light_yellow',
        8: 'sandy_brown',
        16: 'coral',
        32: 'tomato',
        64: 'red',
        128: 'yellow_1',
        256: 'yellow_2',
        512: 'yellow_3',
        1024: 'yellow_3',
        2048: 'yellow_3',
        4096: 'green',
        8192: 'blue',
    }[num]

# Display Grid
def show(board, score, start_time):
    playSurface.fill((250, 248, 239))  # Neutral background color

    # Title
    title_font = pygame.font.SysFont('monaco', 60, bold=True)
    title_surface = title_font.render('2048 GAME', True, color_dic['black'])
    title_rect = title_surface.get_rect(center=(width // 2, 50))
    playSurface.blit(title_surface, title_rect)

    # Score
    score_font = pygame.font.SysFont('monaco', 40, bold=True)
    score_surface = score_font.render(f'Score: {score}', True, color_dic['black'])
    score_rect = score_surface.get_rect(center=(width // 2, 100))
    playSurface.blit(score_surface, score_rect)

    # Time Counter
    elapsed_time = int(time.time() - start_time)
    time_surface = score_font.render(f'Time: {elapsed_time}s', True, color_dic['black'])
    time_rect = time_surface.get_rect(topright=(width - 10, 10))
    playSurface.blit(time_surface, time_rect)

    # Grid Background
    background = pygame.Rect(trans_x - 10, trans_y - 10, 4 * box_w + 3 * gap + 20, 4 * box_h + 3 * gap + 20)
    bg_color = color_dic['gray']
    pygame.draw.rect(playSurface, bg_color, background, border_radius=15)

    # Grid
    for i in range(4):
        for j in range(4):
            x_pos = j * (box_w + gap) + trans_x
            y_pos = i * (box_h + gap) + trans_y
            color_name = ColorChange(board[i][j])
            RGB = color_dic[color_name]
            box_rect = pygame.Rect(x_pos, y_pos, box_w, box_h)
            pygame.draw.rect(playSurface, RGB, box_rect, border_radius=10)

            # Font
            Font1 = pygame.font.SysFont('monaco', 50, bold=True)
            FontColor = bg_color if board[i][j] == 0 else color_dic['black']
            surf1 = Font1.render(f'{board[i][j] if board[i][j] != 0 else ""}', True, FontColor)
            rect1 = surf1.get_rect()
            rect1.center = box_rect.center
            playSurface.blit(surf1, rect1)

if __name__ == "__main__":
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_number(board)
    add_new_number(board)
    score = 0
    paused = False
    start_time = time.time()

    while True:
        show(board, score, start_time)
        pygame.display.update()

        if not can_move(board):
#            print("Game Over! No more moves available.")
            pygame.display.set_caption('Game Over! No more moves available.')
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                if paused:
                    continue

                if event.key == pygame.K_UP:
                    new_board, score_increment = move(board, 3)
                elif event.key == pygame.K_DOWN:
                    new_board, score_increment = move(board, 1)
                elif event.key == pygame.K_LEFT:
                    new_board, score_increment = move(board, 4)
                elif event.key == pygame.K_RIGHT:
                    new_board, score_increment = move(board, 2)
                else:
                    continue

                if new_board != board:
                    board = new_board
                    score += score_increment
                    add_new_number(board)
