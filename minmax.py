import sys
from heuristic import Heuristic
from state import State
from utilities import *
import math

class Minmax:
    def __init__(self):
        self.tree = {}
        
    def minmax(self, agent_state, human_state, is_maximizing, depth=10):
        # base case when depth is zero or the board is complete
        if depth == 0 or (agent_state + human_state) == (2**42)-1:
            heuristic = Heuristic(agent_state, human_state)
            return heuristic.calculate_heuristic(), None
        
        best_col = None
        if is_maximizing:
            max_eval = -math.inf
            # check all possible children
            for i in range (7):
                # check if it's possible to drop the disc
                lowest_row = get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = drop_disc(agent_state, i, lowest_row)
                eval, _ = self.minmax(child_state, human_state, not is_maximizing, depth-1)
                # save in the tree
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, True)
                
                if max_eval < eval :
                    max_eval = eval
                    best_col = i
                
            return max_eval, best_col
                
        else :
            min_eval = math.inf
            # check all possible children
            for i in range (7):
                # check if it's possible to drop the disc
                lowest_row = get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = drop_disc(human_state, i, lowest_row)
                eval, _ = self.minmax(agent_state, child_state, not is_maximizing, depth-1) 
                # save in the tree
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, False)
                
                if min_eval > eval :
                    min_eval = eval
                    best_col = i
                    
            return min_eval, best_col
    
    def save_node_in_tree(self, agent_state, human_state, child_state, column, heuristic, is_agent_move):
        
        parent_key = (agent_state, human_state)
        if parent_key not in self.tree:
            self.tree[parent_key] = []
            
        if is_agent_move:
            self.tree[parent_key].append({
                "column": column,
                "heuristic": heuristic,
                "agent_state": child_state,          
                "human_state": human_state           
            })
        else:
            self.tree[parent_key].append({
                "column": column,
                "heuristic": heuristic,
                "agent_state": agent_state,           
                "human_state": child_state           
            })
            
    
    
    
if __name__ == "__main__":

    board = [
        [0, 0, 0, 0, 0, 0, 0],   
        [0, 0, 1, 1, 1, 0, 0],   
        [0, 1, 1, 1, 1, 0, 0],   
        [0, 1, 1, 1, 1, 0, 0],   
        [0, 1, 1, 1, 2, 0, 0],   
        [1, 1, 2, 2, 2, 2, 1],   
    ]


    # Convert the board to bitboards
    player1_bitboard = board_to_state(board, 1)
    player2_bitboard = board_to_state(board, 2)

    minmax = Minmax()
    _ , col = minmax.minmax(player1_bitboard, player2_bitboard, True, 3)
    print(minmax.tree)
    print(col)
   

