# Mini Games
This repository is a collection of my mini-games that is created using Python with its pygame library


## 1. Snake Game

### Descriptions

The Snake Game is a classic arcade-style game where you control a green snake navigating a rectangular playing field. The goal is to eat as much food as possible, represented as black squares, to increase your score and grow the snake's length. As the snake grows, the game becomes more challenging as you must avoid colliding with your own body.

### Rules

1. Move the snake using your up, down, left, and right buttons.
2. The game ends only if the snake's head collides with its own body.
3. The snake grows in length each time it eats food, increasing the difficulty.
4. The snake can cross screen boundaries and will reappear on the opposite side.
5. The player's score increases by 1 for each piece of food eaten.
6. You can pause or resume the game at any time using the space bar.
7. Pressing the escape key immediately exits the game.

### How to play

1. Install the `pygame` library if you don’t have it already:
```bash
pip install pygame
```

2. Run the script:
```bash
python snake_game.py
```


## 2. 2048 Game

### Descriptions

2048 game is a classic sliding tile puzzle game where the player combines tiles with the same value to reach the tile with the number 2048.

### Controls

 - **&uarr; :** Move tiles up.
 - **&larr; :** Move tiles left.
 - **&darr; :** Move tiles down.
 - **&rarr; :** Move tiles right.
 - **Esc:** Quit the game.

### Rules

Tiles with the same number combine into one when they collide. After every move, a new tile (2 or 4) appears randomly on the board. The game ends when no valid moves are left.

### How to play

1. Install the `pygame` library if you don’t have it already:
```bash
pip install pygame
```

2. Run the script:
```bash
python 2048_game_colors.py
```


## 3. Rock, Paper, Scissors Game

### Descriptions

Rock Paper Scissors is a simple but engaging game where two players simultaneously choose one of three options: Rock, Paper, or Scissors. In this digital version, you play against a computer opponent that randomly selects its moves, while keeping track of your score and match history.

### Rules

**Winning Conditions:**
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- Same choices result in a tie

**Scoring System:**
- Win: Player score increases by 1
- Lose: Computer score increases by 1
- Tie: No score change

### How to play

1. Install the `pygame` library if you don’t have it already:
```bash
pip install pygame
```

2. Run the script:
```bash
python rock-paper-scissors.py
```

