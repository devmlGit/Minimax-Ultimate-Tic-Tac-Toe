"""
--------------- Minimax ultimate tic tac toe solver -----------------
Author: Mounir LBATH
Creation Date: 12/2022
-----------------------------------------------------------
"""

import random
INF=100000 # infinity constant
maxDepth = 5
calls = 0

# initialize the tic tac toe grid
grid = [[[[0]*3 for i in range(3)] for j in range(3)] for l in range(3)]
bigGrid = [[0]*3 for i in range(3)]

currentPosStack = [[0,0]]*(maxDepth+1) # stack used to keep track of past moves when exploring the graph in minimax function
top = -1 # top of the stack index

################### GAME STATE ###################

# returns 0 if game continues, 1 if win, 2 if draw
def boardState(board):
    win = False

    # for each row and column
    for i in range(3):
        lin = True
        col = True
        for j in range(1,3):
            lin = lin and board[i][j] == board[i][j-1] != 0
            col = col and board[j][i] == board[j-1][i] != 0
        win = win or lin or col
    
    # for each diagonal
    diag1 = True
    diag2 = True
    for i in range(1,3):
        diag1 = diag1 and board[i][i] == board[i-1][i-1] != 0
        diag2 = diag2 and board[i][-i-1] == board[i-1][-i] != 0
    win = win or diag1 or diag2
    
    if win:
        return 1

    # check draw
    draw = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                draw = False
    if draw:
        return 2

    return 0

################### HEURISTICS ###################

# heuristic score for a line/column/or diagonal depending on the number of aligned marks
def score(nbAlign):
    if nbAlign == 1:
        return 1
    elif nbAlign == 2:
        return 10
    elif nbAlign == 3:
        return 100
    return 0
# evaluates the position depending on the player
def evalPlayer(board, player):
    result = 0

    # for each row and column
    for i in range(3):
        lin = 0
        col = 0
        for j in range(3):
            lin += board[i][j] == player
            col += board[j][i] == player
        result += score(lin) + score(col)
    
    # for each diagonal
    diag1 = 0
    diag2 = 0
    for i in range(3):
        diag1 += board[i][i] == player
        diag2 += board[i][-i-1] == player
    result += score(diag1) + score(diag2)

    return result
# heuristic evaluation of the game position (max for player 1, min for player -1)
def evalGamePos():
    eval = 0
    for k in range(3):
        for l in range(3):
            eval += evalPlayer(grid[k][l],1)-evalPlayer(grid[k][l],-1)
    eval += 5*(evalPlayer(bigGrid,1)-evalPlayer(bigGrid,-1))
    return eval


################### MINIMAX ALGORITHM ###################

# returns the best heuristic value that can be reached for player in at most maxDepth steps, and plays the corresponding move
def minimax(depth, alpha, beta, player):
    global calls
    calls += 1

    global INF, maxDepth

    # if game over or maxdepth is reached
    if depth == maxDepth or boardState(bigGrid) != 0:
        #drawGrid(player)
        return evalGamePos()    # return the  heuristic evaluation of the pos

    value = 0
    bestMove = [0,0,0,0]

    # 1 is maximizing, -1 is minimizing
    if player == 1:
        value = -INF
        for k in range(3):
            for l in range(3):
                for i in range(3):
                    for j in range(3):
                        if isLegal(k,l,i,j): # if move is legal
                            # make the move
                            move(k,l,i,j,1, True)
                            
                            # compute best evaluation after this move
                            newValue = minimax(depth+1,alpha, beta, -1)

                            # if the newValue is better than the previous best move, update it
                            alpha = max(alpha, newValue)
                            if newValue > value:
                                value = newValue
                                bestMove = [k,l,i,j]

                            # undo the move
                            undoMove(k,l,i,j)

                            # alpha beta pruning
                            if alpha >= beta:
                                break
    # same thing for minimizing player        
    else:
        value = +INF
        for k in range(3):
            for l in range(3):
                for i in range(3):
                    for j in range(3):
                        if isLegal(k,l,i,j): # if move is legal      
                            move(k,l,i,j,-1, True)
                            
                            newValue = minimax(depth+1,alpha, beta, 1)
                            
                            beta = min(beta, newValue)
                            if newValue < value:
                                value = newValue
                                bestMove = [k,l,i,j]

                            # undo the move
                            undoMove(k,l,i,j)

                            if alpha >= beta:
                                break

    # if the minimax recursion has finished determining the best move, do it
    if depth == 0:
        move(bestMove[0],bestMove[1],bestMove[2],bestMove[3], player)

    # return the best evaluation in the current branch of the tree
    return value

# plays randomly
def randomAI(player):
    if top == -1 or bigGrid[currentPosStack[top][0]][currentPosStack[top][1]] != 0:
        k,l=random.randint(0,2),random.randint(0,2)
        while bigGrid[k][l] !=0:
            k,l=random.randint(0,2),random.randint(0,2)
    else:
        k,l = currentPosStack[top]
    i,j = random.randint(0,2),random.randint(0,2)
    while grid[k][l][i][j] != 0:
        i,j = random.randint(0,2),random.randint(0,2)
        
    move(k,l,i,j,player)

def humanPlayer(player):

    while True:
        if top == -1 or bigGrid[currentPosStack[top][0]][currentPosStack[top][1]] != 0:
            print("Line then column of the big grid (between 0 and 2)")
            k = int(input())
            l = int(input())
        else:
            k,l = currentPosStack[top]
        print("Line then column on the small grid with coordinates [", str(k),",", str(l),"] (between 0 and 2)")
        i=int(input())
        j = int(input())
        if 0<=i<3 and 0<=j<3 and 0<=k<3 and 0<=l<3 and isLegal(k,l,i,j):
            break
        else:
            print("Incorrect input !")

    move(k,l,i,j,player)

################### GRAPHICS ###################

def design(p):
    if p == 0:
        return "."
    elif p == 1:
        return "O"
    elif p == -1:
        return "X"
    else:
        return "N"

def color(p, select = False):
    if p==1:
        return '\u001b[31m'
    elif p == -1:
        return '\u001b[36m'
    elif p == 2:
        return '\u001b[32m'
    elif p==0 and select:
        return '\u001b[33m'
    else:
        return '\033[0m'

def drawGrid(player):
    global COLORS
    output = ""
    output+=color(player) + "\n Player "+ design(player) + color(0) +"\n"
    for y in range(9):
        if y % 3 == 0:
            output+="  _ _ _   _ _ _   _ _ _\n"
        for x in range(9):
            if x == 0:
                output += " "
            if x % 3 == 0:
                output+="|"
            
            select = top>=0 and [y//3,x//3] == currentPosStack[top]
            if bigGrid[y//3][x//3] != 0:
                output+=color(bigGrid[y//3][x//3])+"\033[4m"+design(bigGrid[y//3][x//3])+"\033[0m"+color(0)+"|"
            else:
                output+=color(grid[y//3][x//3][y%3][x%3], select)+"\033[4m"+design(grid[y//3][x//3][y%3][x%3])+"\033[0m"+color(0)+"|"
            if x % 3 == 2:
                output+=" "
        output+="\n"
    print(output)

################### GAMEPLAY ###################
def move(k,l,i,j, player, fiction=False):
    global currentPos, top

    grid[k][l][i][j] = player
    
    if fiction or top==-1:
        top+=1
        currentPosStack[top] = [i,j]
    else:
        currentPosStack[top] = [i,j]
    
    a = boardState(grid[k][l])
    if a == 1:
        bigGrid[k][l] = player
    else:
        bigGrid[k][l] = a

def undoMove(k,l,i,j):
    global top

    grid[k][l][i][j] = 0
    top-=1

    bigGrid[k][l] = 0

# check whether a move is legal or not
def isLegal(k,l,i,j):
    return (top==-1 or\
    (bigGrid[currentPosStack[top][0]][currentPosStack[top][1]] == 0 and [k,l] == currentPosStack[top]) or\
        (bigGrid[currentPosStack[top][0]][currentPosStack[top][1]] != 0  and bigGrid[k][l]==0) ) and\
            grid[k][l][i][j] == 0

def game():


    print("\n\n################################################################## \n\n\t\t ULTIMATE TIC TAC TOE")
    print("\n##################################################################\n")
    typePlayer1 =int(input("Player 1? (1 for human, 2 for minimax, 3 for random heuristic)"))
    typePlayer2 = int(input("Player 2? (1 for human, 2 for minimax, 3 for random heuristic)"))

    print("\n##################################################################\n")

    player = 1

    # while no win or draw
    while  boardState(bigGrid) == 0:

        if player == 1:
            if typePlayer1 == 3:
                randomAI(1)
            elif typePlayer1 == 2:
                minimax(0,-INF,+INF,1)
            else:
                humanPlayer(1)
        else:
            if typePlayer2 == 3:
                randomAI(-1)
            elif typePlayer2 == 2:
                minimax(0,-INF,+INF,-1)
            else:
                humanPlayer(-1)
        
        # change the role
        player = -player
        drawGrid(player)
        print("Heuristic (higher scores are best for player O, lower scores are best for player X) :", evalGamePos(),"\n")


    if boardState(bigGrid) == 1:
        print(design(-player)+ " won !")
    else:
        print("Draw !")

game()