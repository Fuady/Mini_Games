import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake block size
BLOCK_SIZE = 10

# Font
FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
TITLE_FONT = pygame.font.SysFont("comicsansms", 50)

def draw_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block_size, block_size])

def display_title_and_score(score):
    title = TITLE_FONT.render("SNAKE GAME", True, BLUE)
    screen.blit(title, [WIDTH / 2 - title.get_width() / 2, 10])
    value = SCORE_FONT.render("Score: " + str(score), True, BLUE)
    screen.blit(value, [WIDTH / 2 - value.get_width() / 2, 60])

def message(msg1, msg2, color):
    mesg1 = FONT_STYLE.render(msg1, True, color)
    mesg2 = FONT_STYLE.render(msg2, True, color)
    screen.blit(mesg1, [WIDTH / 2 - mesg1.get_width() / 2, HEIGHT / 3])
    screen.blit(mesg2, [WIDTH / 2 - mesg2.get_width() / 2, HEIGHT / 3 + 30])

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        screen.fill(WHITE)
        message("Game Paused", "Press Space to Resume or Esc to Exit.", BLUE)
        pygame.display.update()

# Game loop
def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    clock = pygame.time.Clock()
    while not game_over:

        while game_close:
            screen.fill(WHITE)
            message("You lost!", "Press Q-Quit or C-Play Again", RED)
            display_title_and_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    pause_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Border crossing logic
        if x1 >= WIDTH:
            x1 = 0
        elif x1 < 0:
            x1 = WIDTH - BLOCK_SIZE
        if y1 >= HEIGHT:
            y1 = 0
        elif y1 < 0:
            y1 = HEIGHT - BLOCK_SIZE

        x1 += x1_change
        y1 += y1_change
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_title_and_score(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(15)

    pygame.quit()
    quit()

# Main execution
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    game_loop()
