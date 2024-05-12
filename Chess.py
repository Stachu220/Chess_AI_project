import pygame
import sys

# Define a function to convert a position to chess notation
def to_chess_notation(row, col):
    return f"{chr(col + 97)}{8 - row}"

def is_king_not_on_board(board):
    white_king_missing = True
    black_king_missing = True
    for row in board:
        for piece in row:
            if piece is not None and "king" in piece['piece']:
                if piece['color'] == 'white':
                    white_king_missing = False
                else:
                    black_king_missing = False
    return white_king_missing, black_king_missing

def is_valid_move(current_pos, target_pos, piece, check_check=True):
    current_row, current_col = current_pos
    target_row, target_col = target_pos
    piece_color = piece['color']

    # Determine the type of the piece
    for piece_type, piece_image in pieces.items():
        if piece_image == piece['piece']:
            break

    if "pawn" in piece_type:
        if piece_color == "white":
            if current_col == target_col and current_row == target_row + 1 and board[target_row][target_col] is None:
                return True
            elif current_col == target_col and current_row == target_row + 2 and current_row == 6 and board[target_row][target_col] is None:
                return True
            elif abs(current_col - target_col) == 1 and current_row == target_row + 1 and board[target_row][target_col] is not None and board[target_row][target_col]['color'] == 'black':
                return True
        elif piece_color == "black":
            if current_col == target_col and current_row == target_row - 1 and board[target_row][target_col] is None:
                return True
            elif current_col == target_col and current_row == target_row - 2 and current_row == 1 and board[target_row][target_col] is None:
                return True
            elif abs(current_col - target_col) == 1 and current_row == target_row - 1 and board[target_row][target_col] is not None and board[target_row][target_col]['color'] == 'white':
                return True
    elif "bishop" in piece_type or ("queen" in piece_type and abs(current_row - target_row) == abs(current_col - target_col)):
        if abs(current_row - target_row) == abs(current_col - target_col):  # Check if the move is diagonal
            # Check if all squares between the current position and the target position are empty
            row_step = 1 if target_row > current_row else -1
            col_step = 1 if target_col > current_col else -1
            for i in range(1, abs(current_row - target_row)):
                if board[current_row + i * row_step][current_col + i * col_step] is not None:
                    return False
            # Check if the target square contains a piece of the same color
            if board[target_row][target_col] is not None and board[target_row][target_col]['color'] == piece_color:
                return False
            return True
    elif "rook" in piece_type or ("queen" in piece_type and (current_row == target_row or current_col == target_col)):
        if current_row == target_row:  # Check if the move is along the same row
            # Check if all squares between the current position and the target position are empty
            col_step = 1 if target_col > current_col else -1
            for i in range(current_col + col_step, target_col, col_step):
                if board[current_row][i] is not None:
                    return False
        elif current_col == target_col:  # Check if the move is along the same column
            # Check if all squares between the current position and the target position are empty
            row_step = 1 if target_row > current_row else -1
            for i in range(current_row + row_step, target_row, row_step):
                if board[i][current_col] is not None:
                    return False
        else:
            return False  # The move is neither along the same row nor the same column
        # Check if the target square contains a piece of the same color
        if board[target_row][target_col] is not None and board[target_row][target_col]['color'] == piece_color:
            return False
        return True
    elif "knight" in piece_type:
        # Check if the move is an L-shape
        if (abs(current_row - target_row) == 2 and abs(current_col - target_col) == 1) or (abs(current_row - target_row) == 1 and abs(current_col - target_col) == 2):
            # Check if the target square contains a piece of the same color
            if board[target_row][target_col] is not None and board[target_row][target_col]['color'] == piece_color:
                return False
            return True
    elif "king" in piece_type:
        if abs(current_row - target_row) <= 1 and abs(current_col - target_col) <= 1:  # Check if the move is one square in any direction
            # Check if the target square contains a piece of the same color
            if board[target_row][target_col] is not None and board[target_row][target_col]['color'] == piece_color:
                return False
    return True


def end_screen(color):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 24)
    message = f"{color} player wins!"
    text = font.render(message, True, (255, 255, 255))
    play_again_button = pygame.Rect(200, 300, 200, 50)
    exit_button = pygame.Rect(400, 300, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    # Start a new game
                    board = []
                    moves = []  # Replace with your moves history initialization
                    return
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.draw.rect(screen, (0, 255, 0), play_again_button)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)
        play_again_text = button_font.render('Play Again', True, (0, 0, 0))
        exit_text = button_font.render('Exit', True, (0, 0, 0))
        screen.blit(play_again_text, (play_again_button.x + 50, play_again_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 80, exit_button.y + 10))
        pygame.display.flip()   

# Initialize Pygame
pygame.init()

# Define the size of the chessboard
board_size = (480, 480)

# Define the size of the moves table
moves_table_size = (320, 480)

# Create the application window
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Chess Board")

# Define the colors for the chessboard
white = (227, 192, 172)
brown = (92, 64, 51)

# Define the size of each square on the chessboard
square_size = board_size[0] / 8

# Define the font for the moves table
font = pygame.font.Font(None, 24)

# Load chess piece images
max_size = (60, 60)  # Define the maximum size for the images

pieces = {
    "white_pawn": pygame.transform.scale(pygame.image.load("Assets/white_pawn.png"), max_size),
    "black_pawn": pygame.transform.scale(pygame.image.load("Assets/black_pawn.png"), max_size),
    "white_rook": pygame.transform.scale(pygame.image.load("Assets/white_rook.png"), max_size),
    "black_rook": pygame.transform.scale(pygame.image.load("Assets/black_rook.png"), max_size),
    "white_knight": pygame.transform.scale(pygame.image.load("Assets/white_knight.png"), max_size),
    "black_knight": pygame.transform.scale(pygame.image.load("Assets/black_knight.png"), max_size),
    "white_bishop": pygame.transform.scale(pygame.image.load("Assets/white_bishop.png"), max_size),
    "black_bishop": pygame.transform.scale(pygame.image.load("Assets/black_bishop.png"), max_size),
    "white_queen": pygame.transform.scale(pygame.image.load("Assets/white_queen.png"), max_size),
    "black_queen": pygame.transform.scale(pygame.image.load("Assets/black_queen.png"), max_size),
    "white_king": pygame.transform.scale(pygame.image.load("Assets/white_king.png"), max_size),
    "black_king": pygame.transform.scale(pygame.image.load("Assets/black_king.png"), max_size)
}

# Initialize the list of moves
moves = []

# Initialize the board state with chess pieces
board = [
    [{"piece": "black_rook", "color": "black"}, {"piece": "black_knight", "color": "black"}, {"piece": "black_bishop", "color": "black"}, {"piece": "black_queen", "color": "black"},
     {"piece": "black_king", "color": "black"}, {"piece": "black_bishop", "color": "black"}, {"piece": "black_knight", "color": "black"}, {"piece": "black_rook", "color": "black"}],
    [{"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"},
     {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [{"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"},
     {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}],
    [{"piece": "white_rook", "color": "white"}, {"piece": "white_knight", "color": "white"}, {"piece": "white_bishop", "color": "white"}, {"piece": "white_queen", "color": "white"},
     {"piece": "white_king", "color": "white"}, {"piece": "white_bishop", "color": "white"}, {"piece": "white_knight", "color": "white"}, {"piece": "white_rook", "color": "white"}]
]

# Variables to track a piece being moved
selected_piece = None
selected_pos = None

# Initialize the turn
turn = 'white'

# Game loop
running = True
while running:
    white_king_missing, black_king_missing = is_king_not_on_board(board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif white_king_missing:
            end_screen("Black")
            board = [
    [{"piece": "black_rook", "color": "black"}, {"piece": "black_knight", "color": "black"}, {"piece": "black_bishop", "color": "black"}, {"piece": "black_queen", "color": "black"},
     {"piece": "black_king", "color": "black"}, {"piece": "black_bishop", "color": "black"}, {"piece": "black_knight", "color": "black"}, {"piece": "black_rook", "color": "black"}],
    [{"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"},
     {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [{"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"},
     {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}],
    [{"piece": "white_rook", "color": "white"}, {"piece": "white_knight", "color": "white"}, {"piece": "white_bishop", "color": "white"}, {"piece": "white_queen", "color": "white"},
     {"piece": "white_king", "color": "white"}, {"piece": "white_bishop", "color": "white"}, {"piece": "white_knight", "color": "white"}, {"piece": "white_rook", "color": "white"}]
]
            moves = []
        elif black_king_missing:
            end_screen("White")
            board = [
    [{"piece": "black_rook", "color": "black"}, {"piece": "black_knight", "color": "black"}, {"piece": "black_bishop", "color": "black"}, {"piece": "black_queen", "color": "black"},
     {"piece": "black_king", "color": "black"}, {"piece": "black_bishop", "color": "black"}, {"piece": "black_knight", "color": "black"}, {"piece": "black_rook", "color": "black"}],
    [{"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"},
     {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}, {"piece": "black_pawn", "color": "black"}],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [{"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"},
     {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}, {"piece": "white_pawn", "color": "white"}],
    [{"piece": "white_rook", "color": "white"}, {"piece": "white_knight", "color": "white"}, {"piece": "white_bishop", "color": "white"}, {"piece": "white_queen", "color": "white"},
     {"piece": "white_king", "color": "white"}, {"piece": "white_bishop", "color": "white"}, {"piece": "white_knight", "color": "white"}, {"piece": "white_rook", "color": "white"}]
]
            moves = []
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User pressed the mouse button: select the piece
            x, y = pygame.mouse.get_pos()
            row, col = int(y // square_size), int(x // square_size)
            if 0 <= row < 8 and 0 <= col < 8 and board[row][col] is not None and board[row][col]['color'] == turn:
                selected_piece = board[row][col]
                selected_pos = (row, col)
        elif event.type == pygame.MOUSEBUTTONUP:
            # User released the mouse button: try to place the piece
            if selected_piece is not None:
                x, y = pygame.mouse.get_pos()
                row, col = int(y // square_size), int(x // square_size)
                # Check if the released position is within the chessboard
                if 0 <= row < 8 and 0 <= col < 8:
                    if is_valid_move(selected_pos, (row, col), selected_piece):
                        board[selected_pos[0]][selected_pos[1]] = None  # Remove piece from old position
                        board[row][col] = selected_piece  # Place piece at new position
                        # Add the move to the moves list
                        moves.append((selected_pos[0], selected_pos[1], row, col))
                        selected_piece = None
                        selected_pos = None
                        # Switch the turn
                        turn = 'black' if turn == 'white' else 'white'
                    else:
                        # If the move is not valid, just deselect the piece and wait for another move
                        selected_piece = None
                        selected_pos = None
    # Rtarget_poser the chessboard
    for row in range(8):
        for col in range(8):
            pygame.draw.rect(window, white if (row + col) % 2 == 0 else brown, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
            if board[row][col] is not None:
                window.blit(pieces[board[row][col]['piece']], (col * square_size, row * square_size))
    
    # Rtarget_poser the moves table
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(board_size[0], 0, moves_table_size[0], moves_table_size[1]))

    # Rtarget_poser and display the moves
    for i, move in enumerate(moves):
        # Convert the move to chess notation
        move_notation = f"{to_chess_notation(move[0], move[1])}{to_chess_notation(move[2], move[3])}"
        # Determine the position of the move text
        if i % 2 == 0:
            x = board_size[0] + 10
        else:
            x = board_size[0] + moves_table_size[0] / 2
        y = i // 2 * 30 + 10
        text = font.render(move_notation, True, (0, 0, 0))
        window.blit(text, (x, y))
    white_king_missing, black_king_missing = is_king_not_on_board(board)
    pygame.display.flip()


pygame.quit()

#TODO:
# castling