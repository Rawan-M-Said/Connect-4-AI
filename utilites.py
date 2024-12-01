from state import State
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

def drop_disc(player_state, column, row):
    pos = column * 6 + row
    return player_state | (1 << pos)  # Place the piece
    
def get_lowest_available_row(agent_state, human_state, column):
    base_pos = column * 6
    for row in range(6):
        pos =  base_pos + row
        if not ((agent_state & (1 << pos)) or (human_state & (1 << pos))) :  
            return row
    return -1
                
            
# # Initialize a 2D board (6x7)
# board = [
#     [0, 1, 0, 0, 0, 0, 1],   
#     [0, 2, 0, 0, 0, 0, 0],  
#     [0, 1, 0, 0, 0, 0, 0],  
#     [0, 2, 0, 0, 0, 0, 0],  
#     [0, 0, 1, 0, 2, 0, 0],  
#     [0, 0, 2, 0, 1, 0, 0],   
# ]

# # Convert the board to bitboards
# player1_bitboard = board_to_state(board, 1)
# player2_bitboard = board_to_state(board, 2)

# # Initialize the State object
# game_state = State(player1_state=player1_bitboard, player2_state=player2_bitboard)

# # Test dropping a disc
# print(f"Initial Player 1 Bitboard: {bin(game_state.player1_state)}")
# print(f"Initial Player 2 Bitboard: {bin(game_state.player2_state)}")

# success = game_state.drop_disc(1, column=6)  # Player 1 drops a disc in column 1
# print(f"Drop Disc Success: {success}")
# print(f"Updated Player 1 Bitboard: {bin(game_state.player1_state)}")

# # Check if the board is complete
# board2 = state_to_board(game_state.player1_state, game_state.player2_state)
# print(board2)




