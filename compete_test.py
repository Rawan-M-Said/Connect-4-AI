import sys
from Algorithms.algorithm_factory import AlgorithmFactory
   
    
def find_best_move (board, turn):
    algorithm = AlgorithmFactory("minmax with alpha-beta pruning",9)    
    best_move,_,_ = algorithm.solve(board, turn)
    return best_move
        
        
