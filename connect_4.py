import pygame
import numpy as np
import math
import random



# define all the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOLD = (255,215,0)
YELLOW = (255, 255, 0)
LIGHTER_BLUE = (0,128,128)
ORANGE = (255,150,0)
PURPLE = (138,43,226)


width = 700
height = 700

# Images used for this code
Connect_4 = pygame.image.load('Connect 4.png')
main_image = pygame.image.load('Connect 4.png')

# game initialization settings
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Connect 4')
clock = pygame.time.Clock()
pygame.display.set_icon(Connect_4)

# text tool


def text_objects(text, font, color):
    '''This function helps to render the text format so that it can be displayed '''
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, x, y, fontzise, color): # text, then x coord, y coord, font size, color
    '''This funciton is is in charge of displaying text'''
    LargeText = pygame.font.Font('Modern Machine.ttf',fontzise)
    TextSurface, TextRect = text_objects(text, LargeText,color)
    TextRect.center = ((x),(y))
    screen.blit(TextSurface, TextRect)

    pygame.display.update()


# ---------------------------------------

# Button function

def text_object(text, font):
    '''This function renders the text in the button'''
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def button(message, x, y, width, height, inactive_color, active_color, action=None):
    '''This function displays the button, and allows for interaction '''
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    # Creating text for the buttons
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurface, textRectangle = text_object(message, smallText)
    textRectangle.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(textSurface, textRectangle)

pygame.init()

# intro screen
def title_screen():
    '''For this function this is what plays the title screen of the game in a running loop '''
    intro = True

    pygame.mixer_music.load('UnFazedCutMP3.mp3')
    pygame.mixer_music.play(loops=100, start=0.0)

    while intro:
        x = 700 / 2
        y = 200
        screen.fill(GOLD)
        n_Y = 700 / 2
        pygame.time.delay(1000)

        message_display('Connect 4', x, y, 115, RED)
        message_display('Press Space to start the game', x, n_Y, 20, BLACK)
        message_display('c 2019 Game Bam inc.',350,650,30,BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer_music.stop()
                    main_menu()
                    intro = False
        pygame.display.update()
        clock.tick(100)

    pygame.mixer_music.stop()


# main menu screen

def main_menu():
    '''This function is what display the main menu and loops its components '''
    mouse = pygame.mouse.get_pos()
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # x + width > mouse[0] > x and y + height > mouse[1] > y
            # button(message, x, y, width, height, inactive_color, active_color, action=None)
            if event.type == pygame.MOUSEBUTTONDOWN and (200 + 400 > mouse[0] > 200 or 85 + 70 > mouse[1] > 85):
                game_exit = True
            if event.type == pygame.MOUSEBUTTONDOWN and (200 + 400 > mouse[0] > 200 or 260 + 70 > mouse[1] > 260):
                game_exit = True
            if event.type == pygame.MOUSEBUTTONDOWN and (200 + 400 > mouse[0] > 200 or 425 + 70 > mouse[1] > 425):
                game_exit = True
            if event.type == pygame.MOUSEBUTTONDOWN and (200 + 400 > mouse[0] > 200 or 590 + 70 > mouse[1] > 450):
                game_exit = True

        screen.fill(GOLD)
        button('Player VS Player', 150, 115, 400, 70, BLUE, GREEN, PvP)
        button('Player VS AI', 150, 200, 400, 70, ORANGE, RED, PvAI)
        button('AI VS AI', 150, 285, 400, 70, YELLOW, LIGHTER_BLUE, AIvAI)
        button('Help', 150, 370, 400, 70, GREEN, BLUE, Help)
        button('Credits',150,450,400,70,PURPLE,YELLOW,credits_screen)
        pygame.display.update()
        clock.tick(60)

# --------------------------------- functions for the board -------------------------------------
num_rows = 6
num_cols = 7
square_size = 100
token_radius = 45


def create_matrix():
    '''This functions creates a metix of 6x7 so that the game can run and interact with it'''
    board = np.zeros((num_rows, num_cols))
    return board


def drop_piece(board, row, col, piece):
    '''This function places the piece in the appropriate section of the matrix '''
    board[row][col] = piece


def is_valid_location(board, col):
    '''This function check that the piece doesnt go out of bound on the left side and right side'''
    return board[num_rows - 1][col] == 0


def get_next_open_row(board, col):
    '''This dunction is the one in charge of allowing pieces to stack vertically '''
    for i in range(num_rows):
        if board[i][col] == 0:
            return i


def game_logic(board, piece):
    '''This function check in for all the direction in which a piece can win '''
    # Check horizontal locations for win
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece \
                    and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece \
                    and board[r + 3][ c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(num_cols - 3):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece \
                    and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(num_cols - 3):
        for r in range(3, num_rows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece \
                    and board[r - 3][c + 3] == piece:
                return True


def draw_board(board):
    '''This function has the duty to draw the board in the right proportions'''
    for c in range(num_cols):
        for r in range(num_rows):
            pygame.draw.rect(screen, GREEN, (c * square_size, r * square_size + square_size, square_size, square_size))
            pygame.draw.circle(screen, BLACK, (
            int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), token_radius)

    for c in range(num_cols):
        for r in range(num_rows):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), token_radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), token_radius)
    pygame.display.update()

# 6 rows
# 7 columns

# ------------------------ draw -------------------------


def draw(board):
    '''This function  check for the top layer of the board so that it can account for draws if ever happen'''
    if board[5][0] != 0 and board[5][1] != 0 and board[5][2] != 0 and board[5][3] != 0 and board[5][3] != 0 and\
        board[5][4] != 0 and board[5][5] != 0 and board[5][6] != 0 :
        return True

def check_edge(board):
    '''This function  check for the top layer of the board so that it can account for draws if ever happen'''
    if board[5][0] != 0 or board[5][1] != 0 or board[5][2] != 0 or board[5][3] != 0 or board[5][3] != 0 or \
            board[5][4] != 0 or board[5][5] != 0 or board[5][6] != 0:
        return True

def edge_move(board):
    ''' This function performs a move to the right if the edge is already taken '''
    for c in range(num_cols - 6):
        if board[5][c] != 0:
            return c + 1

# ----------------- ai movements ------------------------

    # ai 1 always going to move towards a certain direction if 3 pieces are in a row
def ai1_vertcial_check_true(board,piece):
    ''' this function checks that it has 3 pieces in a row so that tries to connect 4'''
    # check for vertical
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r +2][c] == piece and board[r + 3][c] == 0:
                return True

def ai1_vertcial_check(board,piece):
    ''' This functions makes the move to a 4th row if available '''
    # check for vertical
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r +2][c] == piece and board[r + 3][c] == 0:
                drop_piece(board,r + 3, c, piece)


def ai_horizontal_check_true(board,piece):
    ''' This function checks for available spots to move the column'''
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c +3] == 0:
                return True
            elif board[r][c] == piece and board[r][c - 1] == piece and board[r][c - 2] == piece and board[r][c -3] == 0:
                return True


def ai_horizontal_check(board,piece):
    '''This drops the piece in a horizontal spot'''
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c +3] == 0:
                drop_piece(board,r, c +3, piece)
            elif board[r][c] == piece and board[r][c - 1] == piece and board[r][c - 2] == piece and board[r][c -3] == 0:
                drop_piece(board,r, c - 3, piece)

# check for missing spots in the 4 in a row
def missing_spot_check(board,piece):
    '''This functions checks to see if there is an in between spot'''
    # can not happen vertically
    for c in range(num_cols - 3):
        for r in range( num_rows):
            if board[r][c] == piece and board[r][c + 1] == 0 and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
            elif board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == 0 and board[r][c + 3] == piece:
                return True


def missing_spot(board,piece):
    '''This puts a token on the in between spots'''
    # can not happen vertically
    for c in range(num_cols - 3):
        for r in range( num_rows):
            if board[r][c] == piece and board[r][c + 1] == 0 and board[r][c + 2] == piece and board[r][c + 3] == piece:
                drop_piece(board, r, c + 1, piece)
            elif board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == 0 and board[r][c + 3] == piece:
                drop_piece(board, r, c + 2, piece)

def block_check(board, opp_piece):
    ''' This function checks that a block is available to perform'''
    # check vertially
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == opp_piece and board[r + 1][c] == opp_piece and board[r + 2][c] == opp_piece:
                return True

# check horizontally check to the right
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == opp_piece and board[r][c + 1] == opp_piece and board[r][c + 2] == opp_piece \
                    and board[r][c + 3] == 0:
                return True
            elif board[r][c] == opp_piece and board[r][c - 1] == opp_piece and board[r][c - 2] == opp_piece \
                    and board[r][c - 3] == 0:
                return True

    # check the in betweens
    for c in range(num_cols - 3):
        for r in range( num_rows):
            if board[r][c] == opp_piece and board[r][c + 1] == 0 and board[r][c + 2] == opp_piece \
                    and board[r][c + 3] == opp_piece:
                return True
            elif board[r][c] == opp_piece and board[r][c + 1] == opp_piece and board[r][c + 2] == 0 \
                    and board[r][c + 3] == opp_piece:
                return True

def block_move(board, opp_piece, your_piece):
    '''This function makes a move that will block a token if it is one move away from winning'''
    # check vertically
    for c in range(num_cols):
        for r in range(num_rows - 3):
            if board[r][c] == opp_piece and board[r + 1][c] == opp_piece and board[r + 2][c] == opp_piece:
                drop_piece(board,r + 3,c,your_piece)

    # check horizontally check to the right
    for c in range(num_cols - 3):
        for r in range(num_rows):
            if board[r][c] == opp_piece and board[r][c + 1] == opp_piece and board[r][c + 2] == opp_piece \
                    and board[r][c + 3] == 0:
                drop_piece(board,r,c + 3,your_piece)
            elif board[r][c] == opp_piece and board[r][c - 1] == opp_piece and board[r][c - 2] == opp_piece \
                    and board[r][c - 3] == 0:
                drop_piece(board,r,c - 3,your_piece)

    for c in range(num_cols - 3):
        for r in range( num_rows):
            if board[r][c] == opp_piece and board[r][c + 1] == 0 and board[r][c + 2] == opp_piece \
                    and board[r][c + 3] == opp_piece:
                drop_piece(board,r,c + 1,your_piece)
            elif board[r][c] == opp_piece and board[r][c + 1] == opp_piece and board[r][c + 2] == 0 \
                    and board[r][c + 3] == opp_piece:
                drop_piece(board,r,c + 2,your_piece)


# ------------ function for game over
# buttons used for game over
# main menu == M
# restart == R
# Quit == Q

def game_over(text):
    '''This is the game over screen settings, to display there is needed a text variable'''

    over_display = True

    while over_display:
        screen.fill(WHITE)
        message_display('Game Over',350,100,70,RED)
        message_display(text,350,200,60,BLUE)
        message_display('Press m for main menu',350,300,30,BLACK)
        message_display('Press r for restart',350,400,30,BLACK)
        message_display('Press q to exit',350,500,30,BLACK)
        message_display('Press C to play credits', 350, 600, 30, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    over_display = False
                    main_menu()
                if event.key == pygame.K_r:
                    over_display = False
                    PvP()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    over_display = False
                    credits_screen()


def game_over_pvai(text):
    '''This function displays the game over screen for PvAi'''
    over_display = True

    while game_over:

        screen.fill(WHITE)
        message_display('Game Over', 350, 100, 70, RED)
        message_display(text, 350, 200, 60, BLUE)
        message_display('Press m for main menu', 350, 300, 30, BLACK)
        message_display('Press r for restart', 350, 400, 30, BLACK)
        message_display('Press q to exit', 350, 500, 30, BLACK)
        message_display('Press C to play credits', 350, 600, 30, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    over_display = False
                    main_menu()
                if event.key == pygame.K_r:
                    over_display = False
                    PvAI()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    over_display = False
                    credits_screen()


def game_over_aivai(text):
    '''This function displays the screen for Ai v AI'''
    over_display = True

    while over_display:
        screen.fill(WHITE)
        message_display('Game Over', 350, 100, 70, RED)
        message_display(text, 350, 200, 60, BLUE)
        message_display('Press m for main menu', 350, 300, 30, BLACK)
        message_display('Press r for restart', 350, 400, 30, BLACK)
        message_display('Press q to exit', 350, 500, 30, BLACK)
        message_display('Press C to play credits ', 350, 600, 30, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    over_display = False
                    main_menu()
                if event.key == pygame.K_r:
                    over_display = False
                    AIvAI()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    over_display = False
                    credits_screen()


# --------------------------------------------------


def PvP():
    '''This fucntion allows for player vs player game mode and displays it '''

    board = create_matrix()
    playing = True
    turn = 0
    draw_board(board)
    pygame.display.update()
    pygame.mixer_music.load('Runnin Intro-Loop.mp3')
    pygame.mixer_music.play(loops=1,start=0.0)
    pygame.mixer_music.load('Runnin Loop.mp3')
    pygame.mixer_music.play(loops=-1,start=0.34)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
                posx = event.pos[0]
                # draw the circles at the top of the screen for each player
                if turn == 0: # this is player 1 token
                    pygame.draw.circle(screen, RED, (posx, int(square_size / 2)), token_radius)
                else: # player 2 token
                    pygame.draw.circle(screen, YELLOW, (posx, int(square_size / 2)), token_radius)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
                # Ask for Player 1 Input
                if turn == 0:
                    mouse_posx = event.pos[0]
                    col = int(math.floor(mouse_posx / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if game_logic(board, 1):
                            pygame.mixer_music.stop()
                            pygame.time.delay(1000)
                            playing = False
                            text = 'Player 1 wins!!'
                            game_over(text)
                        if draw(board):
                            pygame.mixer_music.stop()
                            playing = False
                            text_3 = 'draw'
                            game_over(text_3)



                #Ask for Player 2 Input
                else:
                    mouse_posx2 = event.pos[0]
                    col = int(math.floor(mouse_posx2 / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if game_logic(board, 2):
                            pygame.mixer_music.stop()
                            pygame.time.delay(1000)
                            playing = False
                            text_2 = 'Player 2 wins!!'
                            game_over(text_2)
                        if draw(board):
                            pygame.mixer_music.stop()
                            playing = False
                            text_4 = 'draw'
                            game_over(text_4)

                draw_board(board)

                turn += 1
                turn = turn % 2

# --------------------- P v Ai -----------------------


def PvAI():
    board = create_matrix()
    playing = True
    turn = 0
    draw_board(board)
    pygame.display.update()
    pygame.mixer_music.load('Pain Theme Naurto OST.mp3')
    pygame.mixer_music.play(loops=-1,start=0.34)
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
                posx = event.pos[0]
                # draw the circles at the top of the screen for each player
                if turn == 0: # this is player 1 token
                    pygame.draw.circle(screen, RED, (posx, int(square_size / 2)), token_radius)
                else: # player 2 token
                    pygame.draw.circle(screen, YELLOW, (posx, int(square_size / 2)), token_radius)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if game_logic(board, 1):
                            pygame.mixer_music.stop()
                            pygame.time.delay(1000)
                            playing = False
                            text = 'Player 1 wins!!'
                            game_over_pvai(text)
                        if draw(board):
                            pygame.mixer_music.stop()
                            playing = False
                            text_3 = 'draw'
                            game_over_pvai(text_3)

                    # ai moves
                    if block_check(board, 1):
                        block_move(board, 1, 2)

                    elif ai1_vertcial_check_true(board, 2):
                        ai1_vertcial_check(board, 2)

                    elif ai_horizontal_check_true(board, 2):
                        ai_horizontal_check(board, 2)

                    elif check_edge(board):
                        edge_move(board)

                    else:
                        num2 = random.randint(1, 700)
                        col = int(math.floor(num2 / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if game_logic(board, 2):
                            pygame.mixer_music.stop()
                            pygame.time.delay(1000)
                            playing = False
                            text2 = 'Ai  wins!!'
                            game_over_pvai(text2)
                        if draw(board):
                            pygame.mixer_music.stop()
                            playing = False
                            text_3 = 'draw'
                            game_over_pvai(text_3)

                draw_board(board)

# ------------------ Ai v Ai -----------------------------

def AIvAI():
    '''This function allows for Ai v Ai game mode and displays it'''
    # use pygame.time.delay to make it wait in between moves
    board = create_matrix()
    playing = True
    turn = 0
    draw_board(board)
    pygame.display.update()
    pygame.mixer_music.load('Bad Bunny.mp3')
    pygame.mixer_music.play(loops=100,start=0.0)
    while playing:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    playing = False
                    main_menu()

        pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
        pygame.display.update()
        pygame.draw.rect(screen, BLACK, (0, 0, width, square_size))
        pygame.display.update()
        if turn == 0:

            if block_check(board,2):
                block_move(board, 2, 1)

            elif ai1_vertcial_check_true(board, 1):
                ai1_vertcial_check(board,1)

            elif ai_horizontal_check_true(board, 1):
                ai_horizontal_check(board, 1)

            elif check_edge(board):
                col = edge_move(board)

            else:
                if block_check(board, 1):
                    block_move(board, 1, 2)

                elif missing_spot_check(board, 1):
                    missing_spot(board, 1)

                else:
                    num = random.randint(1, 650)
                    col = int(math.floor(num / square_size))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if game_logic(board, 1):
                        pygame.time.delay(1000)
                        pygame.mixer_music.stop()
                        playing = False
                        text = 'Ai 1 wins!!'
                        game_over_aivai(text)
                        pygame.time.delay(1000)
                    if draw(board):
                        pygame.mixer_music.stop()
                        playing = False
                        text_3 = 'draw'
                        game_over_aivai(text_3)

        else:
            if block_check(board, 1):
                block_move(board, 1, 2)

            elif ai1_vertcial_check_true(board, 2):
                ai1_vertcial_check(board, 2)

            elif ai_horizontal_check_true(board, 2):
                ai_horizontal_check(board, 2)

            elif check_edge(board):
                edge_move(board)

            else:
                num2 = random.randint(1, 700)
                col = int(math.floor(num2/ square_size))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if game_logic(board, 2):
                    pygame.time.delay(1000)
                    pygame.mixer_music.stop()
                    playing = False
                    text = 'Ai 2 wins!!'
                    game_over_aivai(text)
                    pygame.time.delay(1000)
                if draw(board):
                    pygame.mixer_music.stop()
                    playing = False
                    text_3 = 'draw'
                    game_over_aivai(text_3)
        draw_board(board)

        turn += 1
        turn = turn % 2
        pygame.time.delay(1000)

# ------------- help screen ------------------------


def Help():
    '''This function displays the help screen with all the instructions of the game '''

    help_screen = True

    while help_screen:
        screen.fill(PURPLE)
        message_display('How to play',350,100,90,BLACK)
        message_display('Each player takes a turn,',350,200,30,ORANGE)
        message_display('Dropping only one token at the time.',350,230,30,ORANGE)
        message_display('You must be the first player',350,260,30,BLUE)
        message_display('to get 4 of your colored tokens',350,290,30,BLUE)
        message_display('in a row, horizontally,',350,320,30,BLUE)
        message_display('vertically, or diagonally.',350,350,30,BLUE)
        message_display('During you turn you can',350,380,30,ORANGE)
        message_display('build your own row, or ',350,410,30,ORANGE)
        message_display('Stop your opponent from',350,440,30,ORANGE)
        message_display('Getting 4 in a row.',350,470,30,ORANGE)
        message_display('If at any point want go back',350,500,30,BLUE)
        message_display(' to main menu, press m',350,530,30,BLUE)
        button('<--main menu--', 500, 600, 70, 70, RED, GREEN,main_menu)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# ----------------- credit screen -------------------------------------


def credits_screen():
    '''This function displays the credits screen '''
    credits = True
    y_val = 750
    last = 750

    pygame.mixer_music.load('Harry Styles - Adore You MP3.mp3')
    pygame.mixer_music.play(loops=10, start=0.0)
    #pygame.mixer_music.stop()


    while credits:
        screen.fill(BLACK)
        message_display('Credits', 350, y_val, 90, WHITE)
        y_val -= 2

        last -= 2
        message_display('Creative Director:           Mario Sandoval', 350, y_val + 100,30,WHITE)
        message_display('Presentation:                  Armaan Hyder', 350, y_val + 130,30,WHITE)
        message_display('Audio Engineer:            Brian Munoz', 350, y_val + 160,30,WHITE)
        message_display('                Material              ', 350, y_val + 190,30,WHITE)
        message_display('Teaching material:                        Sentdex', 350, y_val + 220, 30, WHITE)
        message_display('Course Teacher:   Ian Horbaczewski', 350, y_val + 250, 30, WHITE)
        message_display('Course:                                            ENGR 102', 350, y_val + 280, 30, WHITE)
        message_display('School:           Texas A&M University', 350, y_val + 310, 30, WHITE)
        message_display('Music credits:', 350, y_val + 340, 30, WHITE)
        message_display('Song:                          Artist', 350, y_val + 370, 30, WHITE)
        message_display('Runnin:                      A$AP Rocky', 350, y_val + 400, 30, WHITE)
        message_display('Adore you:               Harry Styles', 350, y_val + 430, 30, WHITE)
        message_display('UnFazed:                   Lil Uzi Vert', 350, y_val + 460, 30, WHITE)
        message_display('Pain OST:             Misashi Kishimoto', 350, y_val + 490, 30,WHITE)
        message_display('Nada es como antes:           Bad Bunny',350,y_val + 520,30,WHITE)
        message_display("Gig em'", 350, y_val + 750,30,WHITE)
        message_display('Copyright credits for fair use under', 350, y_val + 800, 20, WHITE)
        message_display('Educational purposes, we do not own any',350, y_val + 830, 20, WHITE)
        message_display('of the songs, nor profit from them.',350, y_val + 860, 20, WHITE)
        message_display('click m for main menu',620,650,12,WHITE)

        message_display('And thank you for playing :)',350, last + 1000,30,WHITE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer_music.stop()
                    credits = False
                    main_menu()

# order of events displayed

title_screen()

