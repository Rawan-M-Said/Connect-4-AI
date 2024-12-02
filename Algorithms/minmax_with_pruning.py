import math
from Algorithms.algorithm import Algorithm
from Algorithms.utilities import board_to_state
from heuristic import Heuristic


class MinmaxWithPruning(Algorithm):
    def __init__(self):
        super().__init__()
            
    def solve(self, agent_state, human_state, is_maximizing, depth=10, alpha=-math.inf, beta=math.inf):
        # base case when depth is zero
        if depth == 0 :
            heuristic = Heuristic(agent_state, human_state)
            eval = heuristic.calculate_heuristic()
            self.save_node_in_tree(agent_state, human_state, None, None, eval, None)
            return eval, None
        
        # Base case when the board is complete
        if (agent_state + human_state) == (1<<42)-1 :
            heuristic = Heuristic(agent_state, human_state)
            score1, score2 = heuristic.calculate_score()
            eval = score2 - score1
            self.save_node_in_tree(agent_state, human_state, None, None, eval, None)
            return eval, None
        
        arr = [3, 4, 2, 5, 1, 6, 0]
        best_col = None
        if is_maximizing:
            max_eval = -math.inf
            # check all possible children
            for i in arr:
                # check if it's possible to drop the disc
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = self.drop_disc(agent_state, i, lowest_row)
                eval, _ = self.solve(child_state, human_state, not is_maximizing, depth-1, alpha, beta)
                # save in the tree
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, True)
                if max_eval < eval :
                    max_eval = eval
                    best_col = i
                
                alpha = max(alpha, eval)
                if beta <= alpha :
                    break
            return max_eval, best_col
                
        else :
            min_eval = math.inf
            # check all possible children
            for i in arr:
                # check if it's possible to drop the disc
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = self.drop_disc(human_state, i, lowest_row)
                eval, _ = self.solve(agent_state, child_state, not is_maximizing, depth-1, alpha, beta) 
                # save in the tree
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, False)
                
                if min_eval > eval :
                    min_eval = eval
                    best_col = i
                
                beta = min(beta, eval)
                if beta <= alpha :
                    break
                
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

    minmax = MinmaxWithPruning()
    _ , col = minmax.solve(player1_bitboard, player2_bitboard, True, depth=8)
    print(minmax.tree)
    print(col)
   

