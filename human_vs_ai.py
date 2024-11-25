#Import Modules
import pygame
import sys
import math
import random
import numpy as np

# Define Constants
COLUMNS = 7
ROWS = 6
PLAYER = 1
AI = 2
WINDOW_LENGTH = 4
EMPTY = 0
BACKGROUND_COLOUR = (62, 58, 93)
EMPTY_CIRCLE_COLOUR = (78, 73, 119)
BLUE_CIRCLE_COLOUR = (78, 214, 202)
RED_CIRCLE_COLOUR = (232, 37, 94)

 
def make_board():
    """
    This function makes 2D array of zeros in size 6*7 to represent the board.

    Returns:
        2D array: zeros in size 6*7.
    """
    return np.zeros((ROWS, COLUMNS))

def print_board(board):
    """
    This function displays the current state of the game board in the consol

    Parameters:
        board (numpy.ndarray): The current game board.

    Note:
        The function uses the `numpy.flip` method to flip the board vertically. The '0's
        represent empty positions, '1' represents the human player's pieces, and '2'
        represents the AI player's pieces.    
    """
    print(np.flip(board, 0))

def draw_board(board):
    """ 
    This function is responsible for drawing the current game board on the Pygame screen

    Parameters:
        board  (numpy.ndarray): game board.
      """
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BACKGROUND_COLOUR, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED_CIRCLE_COLOUR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), radius)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, BLUE_CIRCLE_COLOUR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), radius)
            else:
                pygame.draw.circle(screen, EMPTY_CIRCLE_COLOUR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), radius)
    pygame.display.update() # This will make the changes visible on the screen.

def check_valid_place(board, column):
    """ 
     This function checks if a column is a valid place to drop a piece.

     Parameters:
        board  (numpy.ndarray): game board.
        column (int): column index to check for validity.

     Returns:
        boolean: True if the `column` is a valid place to drop a piece, False otherwise.
    """
    return board[0][column] == 0

def find_next_empty_row(board, column):
    """ 
     This function searches the specified `column` of the `board` from the bottom row to the top row to find the next empty row.
      
     Parameters:
        board  (numpy.ndarray): game board.
        column (int): column index to check for validity.

     Returns:
        int: The index of the next empty row   
     """
    for row in range(len(board) - 1, -1, -1):
        if board[row][column] == 0:
            return row
         
def drop_piece(board, column, row, piece):
    """
    This function places a game piece in the specified column and row of the game board. 

    Parameters:
        board  (numpy.ndarray): game board.
        column (int): column position to drop the piece.
        row    (int): row position to drop the piece.
        piece  (int): the player's game piece. It can be either 1 (human player) or 2 (AI player).
    """
    board[row][column] = piece
 
def winner(board, piece):
    """
      This function checks the board for four consecutive pieces of the same pieceeither horizontally, vertically, or diagonally

      Parameters:
        board  (numpy.ndarray): game board.
        piece  (int): the player's game piece. It can be either 1 (human player) or 2 (AI player). 
        
      Returns:
        bool: True if the player with the specified `piece` has won the game, False
        otherwise.  
     """
    ## Check horizontal lines
    for column in range(COLUMNS-3): # We decrement the columns range by 3 to ensure enough columns for checking four consecutive pieces vertically.
        for row in range(ROWS): #must loop through intire rows to check horizontally
            #check 4 columns locations by increasing column number
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True

    # Check vertical lines
    for column in range(COLUMNS): #must loop through intire columns to check vertically
        for row in range(ROWS - 3): # We decrement the row range by 3 to ensure enough rows for checking four consecutive pieces vertically.
            #check 4 rows locations by increasing row number
            if board[row][column] == piece and board[row + 1][column] == piece and board[row + 2][column] == piece and board[row + 3][column] == piece:
                return True

    # Check positive diagonal lines
    for column in range(COLUMNS - 3):# We decrement the column range by 3 to ensure enough columns for checking four consecutive pieces diagonally.
        for row in range(ROWS - 3): # We decrement the row range by 3 to ensure enough rows for checking four consecutive pieces diagonally.
            #check 4 rows and columns locations by increasing rows and columns togather.
            """
            that's why we are increasing both columns and rows by 1.
            [[0. 0. 0. 0. 0. (5,5). 0.]
             [0. 0. 0. 0. (4,4). 0. 0.]
             [0. 0. 0. (3,3). 0. 0. 0.]
             [0. 0. (2,2). 0. 0. 0. 0.]
             [0. (1,1). 0. 0. 0. 0. 0.]
             [(0,0). 0. 0. 0. 0. 0. 0.]] 

            """
            if board[row][column] == piece and board[row + 1][column + 1] == piece and board[row + 2][column + 2] == piece and board[row + 3][column + 3] == piece:
                return True

    # Check negative diagonal lines
    for column in range(COLUMNS - 3): # We decrement the column range by 3 to ensure enough columns for checking four consecutive pieces diagonally.
        for row in range(3, ROWS): #we start rows from 3-5 because we need at least three rows above the current row to form a diagonal of length 4.
            #check 4 rows and columns locations by increasing columns and decreasing rows . 
            """ 
            columns are increasing
            --------------------->
            [[(5,0). 0. 0. 0. 0. 0. 0.]  | rows are decreasing
             [0. (4,1). 0. 0. 0. 0. 0.]  |
             [0. 0. (3,2). 0. 0. 0. 0.]  |
             [0. 0. 0. (2,3). 0. 0. 0.]  |
             [0. 0. 0. 0. (1,4). 0. 0.]  |
             [0. 0. 0. 0. 0. (0,5). 0.]] V
            """
            if board[row][column] == piece and board[row - 1][column + 1] == piece and board[row - 2][column + 2] == piece and board[row - 3][column + 3] == piece:
                return True

    return False

def pick_best_move(board, piece):
    """ 
    This function is used by the AI player to determine the best column to place its piece in the game of Connect 4.
      The function evaluates the possible moves by simulating each move and calculating a score for each move using 
      the score_position function. The move with the highest score is considered the best move, and the function
      returns the column index corresponding to this move

    Parameters:
        board  (numpy.ndarray): game board.
        piece  (int): the player's game piece. It can be either 1 (human player) or 2 (AI player).  

    Returns:
       (int): The column index representing the best move for the AI player.    

      """
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_column = random.choice(valid_locations)

    for column in valid_locations:
        row = find_next_empty_row(board, column)
        temp_board = board.copy()
        drop_piece(temp_board, column, row, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = column

    return best_column

def get_valid_locations(board):
    """ 
    This function takes the current game board as input and returns a list of valid column locations where a player can drop a piece.

    Parameters:
        board  (numpy.ndarray): game board.

    Returns:
        (list): A list of integers representing the valid column locations    
    """
    valid_locations = []
    for column in range(COLUMNS):
        if check_valid_place(board, column):
            valid_locations.append(column)
    return valid_locations


def score_position(board, piece): 
    """ 
    This function calculates the score of the current game board for the given player piece.

    Parameters:
        board  (numpy.ndarray): game board.
        piece  (int): the player's game piece. It can be either 1 (human player) or 2 (AI player). 

    Returns:
        int: The score representing the strength of the player's position on the board.

    Score Calculation:
        - The function checks the center column of the board and gives extra points for having the player's
          pieces in the center, encouraging the player to control the center of the board.

        - It then checks all the horizontal, vertical, and diagonal (both positive and negative) windows
          of length 4 on the board and evaluates the player's pieces in these windows using the `evaluate_window`
          function.

        - The scores from all the evaluated windows are summed up to get the final score for the player's position.    
    """
    score = 0  

    ##Score Center Column 
     #the center index is 3 = COLUMNS//2
     #list(board[:,COLUMNS//2]) selects all rows and columns at index 3 and store them on alist 
    center_array=[int(i) for i in list(board[:,COLUMNS//2])] #storing center columns and rows values
    center_count=center_array.count(piece) #counting how many a spesific piece is located conectely in the center 
    score+=center_count*3 #encourage the AI to place its pieces in the center column since controlling the center can be strategically advantageous in Connect 4.
    """ 
    1 is for player , 2 is for ai 

    [[0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 0. 0. 0. 0.]
    [0. 0. 0. 1. 0. 0. 0.]
    [0. 0. 0. 2. 0. 0. 0.]
    [0. 0. 0. 2. 0. 0. 0.]
    [0. 0. 0. 2. 0. 0. 0.]]

    The score for the AI's center column is 3 * 3 = 9
    The score for the player's center column is 1 * 3 = 3
       """
    ##Score Horizontal
     #the board has 6 rows , from each row there will be 4 windows cuz there are 4 posiple lines within 4 pieces 
    for row in range(ROWS):
        row_array = [int(i) for i in list(board[row])] #each row values are stored in row_array
        for column in range(COLUMNS - 3): #decrement columns by 3 to ensure that we can create a window of four consecutive positions without going out of bounds.
            window = row_array[column:column + WINDOW_LENGTH] #create a window of four consecutive positions in the current row
            score+= evaluate_window(window,piece) 
    """ 
     [[0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 1, 2, 2, 1, 1, 1]]
     
     this board has 20 windows like this [0,0,0,0] and those 4 windows coming from the first row 
     [0, 1, 2, 2]
     [1, 2, 2, 1]
     [2, 2, 1, 1]
     [2, 1, 1, 1]
     those windows will bes sent to evalute_window() function to get the score 
     """        

    ##Score Vertical  
    for column in range(COLUMNS):
        column_array=[int(i) for i in list(board[:,column])]
        for row in range(ROWS-3):
            window = column_array[row:row + WINDOW_LENGTH]  
            score+= evaluate_window(window,piece)  


    ##Score diagnol 1 positively :)
    for row in range(ROWS-3):
        for column in range(COLUMNS-3):
            window=[board[row+i][column+i] for i in range (WINDOW_LENGTH)]
            score+= evaluate_window(window,piece)
                   
    ##Score diagnol 2 negatively :)
    for row in range(ROWS-3):
        for column in range(COLUMNS-3):
            window=[board[row+3-i][column+i] for i in range (WINDOW_LENGTH)]
            score+= evaluate_window(window,piece)       
    return score



def evaluate_window(window, piece):
    """
    This function evaluate a window of pieces in the game board for a given player.

    Parameters:
        window (list): A list containing a segment of the game board (e.g., row, column, diagonal).
        piece (int): The player's piece value (1 for PLAYER, 2 for AI).

    Returns:
        score (int): The score calculated for the given player based on the window.
    """
    score = 0
    #Determine the value of the opponent's piece.This allows the function to consider the presence of both the player's and the opponent's pieces in the window.
    opp_piece=AI if piece==PLAYER else PLAYER    

    ##If there are four pieces of the given piece in the window,
     #it means the player has four consecutive pieces,
     #which is a winning situation. So, the function adds a high score of 100 to reflect a strong winning position.
    if window.count(piece) == 4:
            score += 100

    ##If there are three pieces of the given piece and one empty space in the window,
     #it indicates the possibility of forming a winning sequence by placing one more piece.
     #This is a valuable position, but not as strong as a winning position. 
     #So, the function adds a score of 5 to indicate a favorable situation.        
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5

    ##the less piece count , the less score         
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

    ##in this case we have a potential threat from the opponent.
     # The player should be cautious as the opponent might be close to forming a winning sequence.
     #So, the function penalizes the player with a negative score of -4 to indicate a disadvantageous position.
    if window.count(opp_piece) == 3 and window.count(EMPTY)==1:
            score -= 4  

    return score

def minmax(board,depth,maxmizingPlayer):
     """
     This function implements the Minimax algorithm, a recursive algorithm used in two-player, zero-sum games
       to find the best move for the current player. It considers all possible moves and outcomes to make the 
       optimal decision, assuming that both players play optimally.

    Parameters:
        board  (numpy.ndarray): game board.
        depth (int): The depth of the game tree to explore (how many moves ahead to look).
        maximizingPlayer (bool): indicates whether it is the turn of the maximizing player (AI) or not (PLAYER).

    Returns:
        tuple: A tuple containing the best column (move) and its corresponding score for the current player.   
     """
     valid_locations= get_valid_locations(board)
     is_terminal=is_terminal_node(board)
     if depth==0 or is_terminal:
         if is_terminal:
            """ 
            the winning scores:
            ai     =  1000000000000000
            player = -1000000000000000
            no-one =  0
            """
            if winner(board,AI):
               return  (None,1000000000000000)
            elif winner(board,PLAYER):
               return (None,-100000000000000)
            else: #game is over , no more valid locations 
               return (None,0)
         else:
              return (None,score_position(board,AI))
           
     if maxmizingPlayer: #maximizing AI
         value=-math.inf #initialize it with negative to ensure it will be updated with the heigest score
         col= random.choice(valid_locations)
         for column in valid_locations:
             row=find_next_empty_row(board,column)
             board_copy=board.copy()
             drop_piece(board_copy,column,row,AI)
             new_score=minmax(board_copy,depth-1,False)[1] #false points to player's turn 
             if new_score> value:
                 value=new_score
                 col= column
         return col, value
          
     else: #minimizing player 
         value=math.inf #initialize it with positive to ensure it will be updated with the lowest score
         col= random.choice(valid_locations)
         for column in valid_locations:
             row=find_next_empty_row(board,column)
             board_copy=board.copy()
             drop_piece(board_copy,column,row,PLAYER)
             new_score = minmax(board_copy,depth-1,True)[1] #true points to player's turn 
             if new_score < value:
                 value=new_score
                 col= column
         return col, value     

def is_terminal_node(board):
    """ 
    This function is used to determine whether a given game board is a terminal node 
    in the game tree or not. A terminal node is a board state where the game is over,
     either because a player has won or there are no valid moves left

    Parameters:
        board  (numpy.ndarray): game board. 
    
    Returns:
        bool: True if the board is a terminal node, False otherwise.     
    """
    return winner(board,PLAYER) or winner(board,AI) or len(get_valid_locations(board))==0

#======================================================================================
# Initialize the game
board = make_board()
pygame.init()
SQUARE_SIZE = 100
WIDTH = 7 * SQUARE_SIZE
HEIGHT = (6 + 1) * SQUARE_SIZE
size = (WIDTH, HEIGHT)
radius = int(SQUARE_SIZE / 2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
game_font = pygame.font.SysFont("monospace", 35)

# Game loop
game_over = False
turn = random.choice([PLAYER, AI])
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BACKGROUND_COLOUR, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED_CIRCLE_COLOUR, (posx, int(SQUARE_SIZE / 2)), radius)
            else:
                pygame.draw.circle(screen, BLUE_CIRCLE_COLOUR, (posx, int(SQUARE_SIZE / 2)), radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BACKGROUND_COLOUR, (0, 0, WIDTH, SQUARE_SIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                column_input = int(math.floor(posx / SQUARE_SIZE))
                if check_valid_place(board, column_input):
                    row_position = find_next_empty_row(board, column_input)
                    drop_piece(board, column_input, row_position, PLAYER)

                    if winner(board, PLAYER):
                        label = game_font.render("PLAYER 1 WINS!!! game over :)", PLAYER, RED_CIRCLE_COLOUR)
                        screen.blit(label, (40, 20))
                        game_over = True
                    else:
                        turn = AI

                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:
        #column_input = pick_best_move(board, AI)
        column_input,minimax_score=minmax(board,4,True)
        if check_valid_place(board, column_input):
            pygame.time.wait(500)
            row_position = find_next_empty_row(board, column_input)
            drop_piece(board, column_input, row_position, AI)

            if winner(board, AI):
                label = game_font.render("PLAYER 2 WINS!!! game over :)", AI, BLUE_CIRCLE_COLOUR)
                screen.blit(label, (40, 20))
                game_over = True
            else:
                turn = PLAYER

            print_board(board)
            draw_board(board)

    # Check for a tie (draw) condition
    if len(get_valid_locations(board)) == 0 and not game_over:
        label = game_font.render("It's a tie! Game over :)", 1, (255, 255, 255))
        screen.blit(label, (40, 20))
        game_over = True

    pygame.display.update()

if game_over:
    pygame.time.wait(5000)
