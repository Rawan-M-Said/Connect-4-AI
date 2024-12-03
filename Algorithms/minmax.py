from Algorithms.algorithm import Algorithm
from heuristic import Heuristic
from Algorithms.utilities import *
import math

class Minmax(Algorithm):
    def __init__(self):
        super().__init__()
        self.transposition_table = {}
            
    def solve(self, agent_state, human_state, is_maximizing, depth=10):

        state_key = (agent_state, human_state, is_maximizing)

        #  If the key has been already evaluated, then don't reevaluate it.
        if state_key in self.transposition_table:
            return self.transposition_table[state_key]

        # base case when depth is zero or the board is complete
        if depth == 0 or (agent_state + human_state) == (1<<42)-1:
            heuristic = Heuristic(agent_state, human_state)
            eval = heuristic.calculate_heuristic()
            self.save_node_in_tree(agent_state, human_state, None, None, eval, None)
            return eval, None
        
        best_col = None
        if is_maximizing:
            max_eval = -math.inf
            # check all possible children
            for i in range (7):
                # check if it's possible to drop the disc
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = self.drop_disc(agent_state, i, lowest_row)
                eval, _ = self.solve(child_state, human_state, not is_maximizing, depth-1)
                # save in the tree
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, True)
                
                if max_eval < eval :
                    max_eval = eval
                    best_col = i
                result = (max_eval, best_col)
                    
            self.transposition_table[state_key] = result
            return max_eval, best_col
                
        else :
            min_eval = math.inf
            # check all possible children
            for i in range (7):
                # check if it's possible to drop the disc
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = self.drop_disc(human_state, i, lowest_row)
                eval, _ = self.solve(agent_state, child_state, not is_maximizing, depth-1) 
                # save in the tree
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, False)
                
                if min_eval > eval :
                    min_eval = eval
                    best_col = i
            result = (min_eval, best_col)
                    
            self.transposition_table[state_key] = result
            return min_eval, best_col
    
    
    
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
    _ , col = minmax.solve(player1_bitboard, player2_bitboard, True, 3)
    print(minmax.tree)
    print(col)
   

