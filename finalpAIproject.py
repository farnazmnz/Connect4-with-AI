import numpy as np
import sys
import math
import random
import pygame

BLUE = (0, 80, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)

ROW = 8
COLUMN = 8


SQUARESIZE = 70    #pixel
RADIUS = int(SQUARESIZE / 2 - 5)   #shoa dayere



width = COLUMN * SQUARESIZE  #abad safhe
height = (ROW + 2) * SQUARESIZE
endGame = False    #sharte khateme bazi
turn = 0           #nobat

size = (width, height)   #size safhe

#graphic dokme haye start va quit
def button(screen, position, text, size, colors):       
    frontg, backg = colors.split(" ")
    font = pygame.font.SysFont("calibri", size)
    text_render = font.render(text, 1, frontg)
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.rect(screen, backg, (x, y, w , h))
    return screen.blit(text_render, (x, y))

#dadane abad board
def makeBoard():
    board = np.zeros((ROW, COLUMN))
    return np.flip(board, 0)

#sakhtan graphic safhe
def guiBoard(board):
    bstart = button(screen, (10, 30), "Start", 40, "black white")
    bquit = button(screen, (450, 30), "Quit", 40, "black white")
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r * SQUARESIZE)+ (2*SQUARESIZE) , SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (
                int(c * SQUARESIZE + SQUARESIZE / 2),
                int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

#tabe baraye check kardane in ke aya sotone morede nazar jaye khali dare ya na
def notFull(board, col):
    if board[ROW - 1][col] == 0:
        return True
    else:
        return False

#tabe baraye peyda kardane avalin radif khali dar sotone morede nazar
def findRow(board, col):
    for r in range(ROW):
        if board[r][col] == 0:
            return r

#tabe baraye andakhtan mohre dar makane morede nazar
def move(board, row, col, piece):
    board[row][col] = piece


#tabe baraye check kardane bordane yek bazikon
#ke dar 4 jahat check mishe
def checkWin(board, piece):

    for c in range(COLUMN - 3):
        for r in range(ROW):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True


    for c in range(COLUMN):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][ c] == piece:
                return True


    for c in range(COLUMN - 3):
        for r in range(ROW - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][ c + 3] == piece:
                return True


    for c in range(COLUMN - 3):
        for r in range(3, ROW):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

#tabe barye check kardane mosavi shodan
def checkDraw(board , p):
    counter = 0
    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] != 0:
                counter += 1
    if counter == ROW * COLUMN and not checkWin(board, p):
        return True

#tabe barye afzayesh score dar halat haye mokhtalef
def measureScore(window, piece):
    score = 0
    opp_piece = 1

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 50
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 20

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 70

    return score

#tabe barye joda kardane 4 ta 4 ta
def findScore(board, piece):
    score = 0

    for i in list(board[:, COLUMN // 2]):
        arrCenter = [int(i)]

    center_count = arrCenter.count(piece)
    score += center_count * 3

    for r in range(ROW):
        for i in list(board[r, :]):
          arrRow =[int(i)]
        for c in range(COLUMN - 3):
            window = arrRow [c:c + 4]
            score += measureScore(window, piece)

    for c in range(COLUMN):
        for i in list(board[:, c]):
            arrCol = [int(i)]
        for r in range(ROW - 3):
            window = arrCol [r:r + 4]
            score += measureScore(window, piece)

    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += measureScore(window, piece)

    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += measureScore(window, piece)

    return score

#tabe asli  algoritm negamax
def negamax(board, depth, alpha, beta, maxP):
    isValid = []
    for col in range(COLUMN):
        if notFull(board, col):
            isValid.append(col)
    if checkWin(board, 1) or checkWin(board, 2) or checkDraw(board ,1) or checkDraw(board ,2):
        terminalNode = True
    else:
        terminalNode = False

    if depth == 0 or terminalNode:
        if terminalNode:
            if checkWin(board, 2):
                return (None, math.inf)
            elif checkWin(board, 1):
                return (None, -math.inf)
            else:
                return (None, 0)
        else:
            return (None, findScore(board, 2))
    value = -math.inf
    column = random.choice(isValid)
    for col in isValid:
        row = findRow(board, col)
        b_copy = board.copy()
        move(b_copy, row, col, 2)
        if maxP:
            new_score = -negamax(b_copy, depth - 1, -beta, -alpha, False)[1]
        else:
            new_score = -negamax(b_copy, depth - 1, -beta, -alpha, True)[1]
        if new_score > value:
            value = new_score
            column = col
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return column, value




pygame.init()

board = makeBoard()
screen = pygame.display.set_mode(size)
guiBoard(board)

gameFont = pygame.font.SysFont("calibri",30)

bstart = button(screen, (10, 30), "Start", 40, "black white")
bquit = button(screen, (450, 30), "Quit", 40, "black white")

while not endGame:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            label = gameFont.render("Player 1 !!", 1, WHITE)
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
	    
            #check kardane dokme quit
            if bquit.collidepoint(pygame.mouse.get_pos()):
                sys.exit()
 
             #check kardane dokme start
            if bstart.collidepoint(pygame.mouse.get_pos()):
                board = makeBoard()
                turn = 0
                endGame = False
		
	   #age nobat player 1 she vorodi migire va bade endakhtane mohre
           #sharte bord ya mosavi shodan ro check mikone
            elif turn == 0:
                label = gameFont.render("Player 2!!", 1, WHITE)
                screen.blit(label, (160, 40))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if notFull(board, col):
                    row = findRow(board, col)
                    move(board, row, col, 1)
                    turn += 1
                    if checkWin(board, 1):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = gameFont.render("Player 1 wins XO", 1, WHITE)
                        screen.blit(label, (140, 40))
                        endGame = True

                    if checkDraw(board ,1):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = gameFont.render("DRAW !!", 1, WHITE)
                        screen.blit(label, (140, 40))
                        endGame = True

           #age nobat player 2(computer) she sotone ro ba negamax peida kare va bade endakhtane mohre
           #sharte bord ya mosavi shodan ro check mikone
            elif not endGame and turn == 1:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                label = gameFont.render("Player 1 !!", 1, WHITE)
                screen.blit(label, (160, 40))

                col, negamax_score = negamax(board, 6, -math.inf, math.inf, True)

                if notFull(board, col):
                    # pygame.time.wait(500)
                    row = findRow(board, col)
                    move(board, row, col, 2)
                    turn += 1

                    if checkWin(board, 2):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = gameFont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        endGame = True

                    if checkDraw(board ,2):
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = gameFont.render("DRAW !!", 1, WHITE)
                        screen.blit(label, (140, 40))
                        endGame = True

            guiBoard(board)
            turn = turn % 2
	
	    #bade etmame bazi check mikone age dokme quit ya start zade she kareshon anjam she
            while endGame:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if bstart.collidepoint(pygame.mouse.get_pos()):
                            board = makeBoard()
                            turn = 0
                            endGame = False

                        if bquit.collidepoint(pygame.mouse.get_pos()):
                            sys.exit()