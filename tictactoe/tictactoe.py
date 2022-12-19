"""
Tic Tac Toe Player
"""

from asyncio import FastChildWatcher
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    emptiness = 0
    for row in board:
        for cell in row:
            if cell == EMPTY:
                emptiness += 1
    if emptiness % 2 == 1: return X
    else: return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for row in range(3):
        for col in range(3):
           if board[row][col] == EMPTY:
                possible_moves.add((row, col))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    def deep_copy(board):
        copy = initial_state()
        for row in range(3):
            for col in range(3):
                copy[row][col] = board[row][col]

        return copy

    #make a copy with no memory sharing
    new_board = deep_copy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #horizontal
    if board[0][0] == board[0][1] == board[0][2] != EMPTY: return  board[0][0]
    if board[1][0] == board[1][1] == board[1][2] != EMPTY: return  board[1][0]
    if board[2][0] == board[2][1] == board[2][2] != EMPTY: return  board[2][0]

    #vertical
    if board[0][0] == board[1][0] == board[2][0] != EMPTY: return  board[0][0]
    if board[0][1] == board[1][1] == board[2][1] != EMPTY: return  board[0][1]
    if board[0][2] == board[1][2] == board[2][2] != EMPTY: return  board[0][2]

    #diagonal
    if board[0][0] == board[1][1] == board[2][2] != EMPTY: return  board[0][0]
    if board[2][0] == board[1][1] == board[0][2] != EMPTY: return  board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #when calling for winner im checking all the board and then i recheck to find empty slots, thats wasteful
    #I should remake winner here instead of calling it
    win = winner(board)
    if win != None: return True
    else: 
        emptiness = False
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    emptiness = True
                    break
            if emptiness: break
    return not emptiness


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X: return 1
    elif win == O: return -1
    else: return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    counter = [0]
    
    def opt_val(maximizing, board):
        """
        Returns the best possible value
        """
        counter[0] += 1

        state = winner(board)
        if terminal(board):
            if state == None:
                return 0
            elif state == X:
                return 1 
            else: return -1

        if maximizing:
            score = float("-inf")
            func = max
            opt = 1
        else:
            score = float("inf")
            func = min
            opt = -1
        for move in actions(board):
            score = func(score, opt_val(not maximizing, result(board, move)))
            if score == opt: break
        return score

    turn = player(board)
    if turn == X:
        bestScore = float("-inf")
        flag = False
        func = lambda a,b : a>b
        opt = 1
    else:
        bestScore = float("inf")
        flag = True
        func = lambda a,b : a<b
        opt = -1
    bestMove = ()
    for move in actions(board):
        score = opt_val(flag, result(board, move))
        if func(score, bestScore):
            bestScore = score
            bestMove = move
        if bestScore == opt: break
    print(counter)
    return bestMove

