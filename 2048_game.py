import random
import os

# Initialize the game board
SIZE = 4

def initialize_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2 if random.random() < 0.9 else 4

# Display the game board

def display_board(board):
    os.system("cls" if os.name == "nt" else "clear")
    print("2048 GAME")
    print("Press W (Up), S (Down), A (Left), D (Right) to move. Q to Quit.")
    print("+----" * SIZE + "+")
    for row in board:
        print("|" + "|".join(f"{cell:^4}" if cell != 0 else "    " for cell in row) + "|")
        print("+----" * SIZE + "+")

# Shift and merge operations

def compress(row):
    new_row = [num for num in row if num != 0]
    return new_row + [0] * (SIZE - len(new_row))

def merge(row):
    for i in range(SIZE - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(board):
    for r in range(SIZE):
        compressed = compress(board[r])
        merged = merge(compressed)
        board[r] = compress(merged)

def move_right(board):
    for r in range(SIZE):
        board[r] = compress(merge(compress(board[r][::-1])))[::-1]

def move_up(board):
    for c in range(SIZE):
        col = compress([board[r][c] for r in range(SIZE)])
        col = merge(col)
        col = compress(col)
        for r in range(SIZE):
            board[r][c] = col[r]

def move_down(board):
    for c in range(SIZE):
        col = compress([board[r][c] for r in range(SIZE)][::-1])
        col = merge(col)
        col = compress(col)
        col = col[::-1]
        for r in range(SIZE):
            board[r][c] = col[r]

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

def play_game():
    board = initialize_board()
    while True:
        display_board(board)

        if not can_move(board):
            print("Game Over! No more moves available.")
            break

        move = input("Enter your move (W/A/S/D/Q): ").strip().lower()
        if move == 'q':
            print("Exiting the game. Thanks for playing!")
            break
        elif move == 'w':
            move_up(board)
        elif move == 'a':
            move_left(board)
        elif move == 's':
            move_down(board)
        elif move == 'd':
            move_right(board)
        else:
            print("Invalid input! Use W, A, S, D to move or Q to quit.")
            continue

        add_new_tile(board)

if __name__ == "__main__":
    play_game()
