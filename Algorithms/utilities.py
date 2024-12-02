
import numpy as np

def board_to_state(board, turn):
    state = 0
    rows = len(board)
    cols = len(board[0])
    for j in range (cols):
        for i in range (rows):
            if board[i][j] == turn:
                pos = j * rows +((rows) - i - 1)
                state |= (1 << pos)
    return state

def state_to_board(player1_state, player2_state):
    rows = 6
    cols = 7
    board = np.zeros((rows, cols), dtype=int)
    for j in range (cols):
        for i in range (rows-1,-1,-1):
            if player1_state & 1:
                board[i][j] = 1
            elif player2_state & 1:
                board[i][j] = 2
            player1_state >>= 1  
            player2_state >>= 1                  
    return board

