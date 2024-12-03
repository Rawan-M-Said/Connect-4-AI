
import sys
import time
from Algorithms.algorithm_factory import AlgorithmFactory

def parse_file(path):
    with open(path, 'r') as file:
        text  = file.read()
    return eval(text)

def find_best_move (board, turn, depth):
    algorithm = AlgorithmFactory("minmax with alpha-beta pruning",depth)    
    best_move,_,_ = algorithm.solve(board, turn)
    return best_move
        
        
if __name__ == "__main__":
    arr = ["D:\\repo\\Connect-4-AI\\test.txt","D:\\repo\\Connect-4-AI\\test copy.txt", "D:\\repo\\Connect-4-AI\\test copy 2.txt","D:\\repo\\Connect-4-AI\\test copy 3.txt","D:\\repo\\Connect-4-AI\\test copy 4.txt"]
    turn = sys.argv[1]
    for i in range (1, 15):
        elapsed_time = 0
        for j in arr:
            board = parse_file(j)
            start = time.time()
            best_move = find_best_move(board, turn, i)
            end = time.time()
            elapsed_time += (end - start) 
        print(f"{i} = > {elapsed_time/5}\n")