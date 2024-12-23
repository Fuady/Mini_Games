import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
GREEN = (75, 181, 67)
BLUE = (52, 152, 219)
RED = (231, 76, 60)
HOVER_GREEN = (88, 214, 79)
HOVER_RED = (231, 116, 100)
BUTTON_BORDER = (45, 109, 40)
EXIT_BORDER = (180, 45, 35)

# Set up the game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Rock Paper Scissors')
clock = pygame.time.Clock()

# Font setup
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, border_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        # Draw border (slightly larger rectangle)
        border_rect = self.rect.inflate(4, 4)
        pygame.draw.rect(surface, self.border_color, border_rect, border_radius=10)
        # Draw main button
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Draw text
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class ScoreSheet:
    def __init__(self):
        self.match_history = []
        self.rect = pygame.Rect(50, 50, 200, 300)

    def add_match(self, player_choice, computer_choice, result):
        self.match_history.append({
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result
        })
        # Keep only last 10 matches
        if len(self.match_history) > 10:
            self.match_history.pop(0)

    def draw(self, surface, player_score, computer_score):
        # Draw score sheet background
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw header
        title = font.render('Score Sheet', True, BLACK)
        surface.blit(title, (self.rect.centerx - title.get_width()//2, self.rect.top + 10))

        # Draw total score
        total_score = font.render(f'Total: {player_score} - {computer_score}', True, BLACK)
        surface.blit(total_score, (self.rect.centerx - total_score.get_width()//2, self.rect.top + 40))

        # Draw match history
        y_offset = 80
        for i, match in enumerate(reversed(self.match_history[-8:])):  # Show last 8 matches
            # Match number
            match_num = small_font.render(f'#{len(self.match_history)-i}:', True, BLACK)
            surface.blit(match_num, (self.rect.left + 10, self.rect.top + y_offset))

            # Choices
            choices = small_font.render(
                f'{match["player_choice"]} vs {match["computer_choice"]}',
                True, BLACK
            )
            surface.blit(choices, (self.rect.left + 50, self.rect.top + y_offset))

            # Result (with color)
            result_color = GREEN if "win" in match["result"].lower() else (
                BLUE if "tie" in match["result"].lower() else RED
            )
            result = small_font.render(match["result"], True, result_color)
            surface.blit(result, (self.rect.left + 10, self.rect.top + y_offset + 20))

            y_offset += 45

class Game:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.game_state = 'choosing'  # States: 'choosing', 'result'

        # Create buttons with new Button class
        button_y = WINDOW_HEIGHT - 150
        self.choice_buttons = {
            'rock': Button(150, button_y, 120, 50, 'Rock', GREEN, HOVER_GREEN, BUTTON_BORDER),
            'paper': Button(340, button_y, 120, 50, 'Paper', GREEN, HOVER_GREEN, BUTTON_BORDER),
            'scissors': Button(530, button_y, 120, 50, 'Scissors', GREEN, HOVER_GREEN, BUTTON_BORDER)
        }

        # Create play again and exit buttons
        self.play_again_button = Button(250, 400, 140, 50, 'Play Again', BLUE, (65, 184, 255), (40, 116, 166))
        self.exit_button = Button(410, 400, 140, 50, 'Exit', RED, HOVER_RED, EXIT_BORDER)

        # Create score sheet
        self.score_sheet = ScoreSheet()

    def determine_winner(self, player, computer):
        if player == computer:
            return "It's a tie!"
        elif (
            (player == 'rock' and computer == 'scissors') or
            (player == 'paper' and computer == 'rock') or
            (player == 'scissors' and computer == 'paper')
        ):
            self.player_score += 1
            return "You win!"
        else:
            self.computer_score += 1
            return "Computer wins!"

    def handle_click(self, pos):
        if self.game_state == 'choosing':
            for choice, button in self.choice_buttons.items():
                if button.is_clicked(pos):
                    self.player_choice = choice
                    self.computer_choice = random.choice(self.choices)
                    self.result = self.determine_winner(self.player_choice, self.computer_choice)
                    self.score_sheet.add_match(self.player_choice, self.computer_choice, self.result)
                    self.game_state = 'result'
        elif self.game_state == 'result':
            if self.play_again_button.is_clicked(pos):
                self.game_state = 'choosing'
                self.player_choice = None
                self.computer_choice = None
                self.result = None
            elif self.exit_button.is_clicked(pos):
                pygame.quit()
                sys.exit()

    def handle_hover(self, pos):
        if self.game_state == 'choosing':
            for button in self.choice_buttons.values():
                button.handle_hover(pos)
        elif self.game_state == 'result':
            self.play_again_button.handle_hover(pos)
            self.exit_button.handle_hover(pos)

    def draw(self):
        WINDOW.fill(WHITE)

        # Draw score sheet
        self.score_sheet.draw(WINDOW, self.player_score, self.computer_score)

        if self.game_state == 'choosing':
            # Draw instruction
            instruction = font.render('Choose your move:', True, BLACK)
            WINDOW.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 150))

            # Draw buttons
            for button in self.choice_buttons.values():
                button.draw(WINDOW)

        elif self.game_state == 'result':
            # Draw choices
            player_text = font.render(f'Your choice: {self.player_choice.capitalize()}', True, BLACK)
            computer_text = font.render(f'Computer choice: {self.computer_choice.capitalize()}', True, BLACK)
            result_text = large_font.render(self.result, True, BLACK)

            WINDOW.blit(player_text, (WINDOW_WIDTH // 2 - player_text.get_width() // 2, 200))
            WINDOW.blit(computer_text, (WINDOW_WIDTH // 2 - computer_text.get_width() // 2, 250))
            WINDOW.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, 300))

            # Draw play again and exit buttons
            self.play_again_button.draw(WINDOW)
            self.exit_button.draw(WINDOW)

def main():
    game = Game()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        game.handle_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

        game.draw()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
