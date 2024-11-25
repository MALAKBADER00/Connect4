'''
CONNECT4 GAME (HUMAN vs HUMAN)
'''

import pygame
import sys
import math
#---------------------------------------------------------------------------
def make_board():
    return [[' ' for i in range(7)] for j in range (6)]

def print_board(board):
    for row in board:
        for place in row :
            print('| ' + ' | '.join(place) , end=" ")
        print("|" + "\n" +"+---"*7 +"+")  
        
def drop_piece(board,column,row,piece):
    board[row][column]=piece

def check_vaild_place(board,column):
    return board[0][column]==" "

#to find the next row of a specific column to drop the next pice on 
def find_next_empty_row(board,column):
    for row in range(len(board)-1,-1,-1):
        if (board[row][column]==" "):
            return row

def winner(board,piece):
    #piece "o","x
    #check  horizontal lines
    for i in board:
        count4=0
        for j in i:
            if j==piece:
               count4+=1
               if count4==4:
                   return True
            else: 
                count4=0
    #check vertical lines
    for i in range (COLUMNS):
        for j in range(ROWS-3):
            if board[j][i]==piece and board[j+1][i]==piece and board[j+2][i]==piece and board[j+3][i]==piece:
                return True
    
    #check negative diagonal lines
    for i in range(COLUMNS-3):
        for j in range(ROWS-3):
            if board[i][j]==piece and board[i+1][j+1]==piece and board[i+2][j+2]==piece and board[i+3][j+3]==piece:
                return True

    #check positive diagonal lines
    for i in range(COLUMNS-3):
        for j in range(3,ROWS):
            if board[j][i]==piece and board[j-1][i+1]==piece and board[j-2][i+2]==piece and board[j-3][i+3]==piece:
                return True
    return False

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BACKGROUND_COLOUR ,(c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c]=="x":
               pygame.draw.circle(screen, RED_CIRCLE_COLOUR, (int(c*SQUARE_SIZE+SQUARE_SIZE/2) , int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2) ), radius)
            elif board[r][c]=="o":
                pygame.draw.circle(screen, BLUE_CIRCLE_COLOUR, (int(c*SQUARE_SIZE+SQUARE_SIZE/2) , int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2) ), radius)
            else:
                pygame.draw.circle(screen, EMPTY_CIRCLE_COLOUR, (int(c*SQUARE_SIZE+SQUARE_SIZE/2) , int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2) ), radius)
    pygame.display.update()

#---------------------------------------------------------------------------------------------------
COLUMNS=7
ROWS=6

BACKGROUND_COLOUR=(62,58,93)
EMPTY_CIRCLE_COLOUR=(78,73,119)
BLUE_CIRCLE_COLOUR=(78,214,202)
RED_CIRCLE_COLOUR=(232,37,94)

board=make_board()
pygame.init()
SQUARE_SIZE=100
WIDTH=7*SQUARE_SIZE
HEIGHT=(6+1)*SQUARE_SIZE         
size=(WIDTH,HEIGHT)
radius= int(SQUARE_SIZE/2-5)
screen = pygame.display.set_mode(size) 
draw_board(board)
pygame.display.update()
game_font=pygame.font.SysFont("monospace",35)

game_over=False
turn="x"
while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BACKGROUND_COLOUR, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == "x":
                pygame.draw.circle(screen, RED_CIRCLE_COLOUR, (posx, int(SQUARE_SIZE/2)), radius)
            else:
                pygame.draw.circle(screen, BLUE_CIRCLE_COLOUR, (posx, int(SQUARE_SIZE/2)), radius)
            pygame.display.update()  # Add this line to update the display      


        if event.type== pygame.MOUSEBUTTONDOWN:
           pygame.draw.rect(screen, BACKGROUND_COLOUR, (0, 0, WIDTH, SQUARE_SIZE))
           if turn=="x":
            posx=event.pos[0]
            column_input=int(math.floor(posx/SQUARE_SIZE))  #to get the closest integer
            if check_vaild_place(board,column_input):
                row_position=find_next_empty_row(board, column_input)
                drop_piece(board, column_input, row_position, "x")

                if winner(board, "x"):
                    lable=game_font.render("PLAYER 1 WINS!!! game over :)","x",RED_CIRCLE_COLOUR)
                    screen.blit(lable,(40,20))
                    game_over=True
           else:
             posx=event.pos[0]
             column_input=int(math.floor(posx/SQUARE_SIZE))  #to get the closest integer
             if check_vaild_place(board,column_input):
                row_position=find_next_empty_row(board, column_input)
                drop_piece(board, column_input, row_position, "o")

                if winner(board, "o"):
                    lable=game_font.render("PLAYER 2 WINS!!! game over :)","o",BLUE_CIRCLE_COLOUR)
                    screen.blit(lable,(40,20))
                    game_over=True 
           print_board(board) 
           draw_board(board)
           print()
           print() 
           turn="x" if turn=="o" else "o"  

           if game_over:
               pygame.time.wait(3000)     
      
            
                         
    
    
    