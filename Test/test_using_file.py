
import sys
import time
from Algorithms.algorithm_factory import AlgorithmFactory

def parse_file(path):
    with open(path, 'r') as file:
        text  = file.read()
    return eval(text)

def find_best_move (board, turn):
    algorithm = AlgorithmFactory("minmax with alpha-beta pruning",10)    
    best_move,_,_ = algorithm.solve(board, turn)
    return best_move
        
        
if __name__ == "__main__":
    board = parse_file(sys.argv[1])
    turn = sys.argv[2]
    start = time.time()
    best_move = find_best_move(board, turn)
    end = time.time()
    elapsed_time = end - start 
    print(elapsed_time)