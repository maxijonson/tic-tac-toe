from os import system, name

TOKEN_EMPTY = "#"
TOKEN_X = "X"
TOKEN_O = "O"
CELL_MIN = 0
CELL_MAX = 8
ROWS = 3
COLS = 3
WIN = 3


# Clears the console
def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


# Draws a cell in the board
def draw_cell(cell, name):
    return cell if cell != TOKEN_EMPTY else name


# Draws the board
def draw_board(board):
    clear()
    for row in range(0, ROWS):
        if (row != 0):
            print(COLS * "---" + (COLS - 1) * "-")
        print(" " +
              " | ".join(
                  list(
                      map(
                          lambda cell: draw_cell(board[cell], str(cell + 1)),
                          range(row * ROWS, row * ROWS + COLS)
                      )
                  )
              )
              )


# Asks for the next move
def next_move(is_p1, board):
    cell = CELL_MIN - 1
    while cell < CELL_MIN or cell > CELL_MAX:
        try:
            cell = int(
                input(("Player 1" if is_p1 else "Player 2") + ". Your move. ")) - 1
        except ValueError:
            cell = CELL_MIN - 1
    if board[cell] != TOKEN_EMPTY:
        cell = next_move(is_p1, board)
    return cell


# Puts a token on the board
def place_token(board, cell, token):
    board[cell] = token
    return board


# Check if there's a win
def check_win(board):
    # Check for horizontal wins
    for row in range(0, ROWS):
        if (TOKEN_X * WIN in "".join(board[row * ROWS:row * ROWS + COLS])):
            return TOKEN_X
        elif (TOKEN_O * WIN in "".join(board[row * ROWS:row * ROWS + COLS])):
            return TOKEN_O

    # Check for vertical wins
    for col in range(0, COLS):
        if (TOKEN_X * WIN in "".join(board[col:col + ROWS + COLS + 1:COLS])):
            return TOKEN_X
        if (TOKEN_O * WIN in "".join(board[col:col + ROWS + COLS + 1:COLS])):
            return TOKEN_O

    # Check for diagonal wins
    limit = ROWS if ROWS < COLS else COLS
    # right diagonals
    for i in range(0, COLS * ROWS):
        if (TOKEN_X * WIN in "".join(board[i:COLS * ROWS - i * limit:COLS + 1])):
            return TOKEN_X
        if (TOKEN_O * WIN in "".join(board[i:COLS * ROWS - i * limit:COLS + 1])):
            return TOKEN_O
    # left diagonals. TODO: intelligent find
    if TOKEN_X * WIN in "".join([board[2], board[4], board[6]]):
        return TOKEN_X
    if TOKEN_O * WIN in "".join([board[2], board[4], board[6]]):
        return TOKEN_O

    # No wins
    return TOKEN_EMPTY


# Start the play loop
def play():
    board = (f"{TOKEN_EMPTY} " * (ROWS * COLS)).split()
    p1 = TOKEN_EMPTY
    p2 = TOKEN_EMPTY

    while p1 != TOKEN_X and p1 != TOKEN_O:
        p1 = input(f"Player 1. {TOKEN_X} or {TOKEN_O}? ").upper()
    p2 = TOKEN_O if p1 == TOKEN_X else TOKEN_X

    is_p1 = True

    while True:
        draw_board(board)
        win = check_win(board)
        if win != TOKEN_EMPTY:
            return win
        elif not "#" in "".join(board):
            return TOKEN_EMPTY
        cell = next_move(is_p1, board)
        board = place_token(board, cell, p1 if is_p1 else p2)
        is_p1 = not is_p1


replay = True
while (replay):
    result = play()
    if result == TOKEN_EMPTY:
        print("It's a tie!")
    else:
        print(f"The {result}s win!")
    wants_replay = input("Play again?")
    if (wants_replay.lower() != "y"):
        replay = False
