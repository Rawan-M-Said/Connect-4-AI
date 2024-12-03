

from Algorithms.expected_minmax import ExpectedMinmax
from Algorithms.minmax import Minmax
from Algorithms.minmax_with_pruning import MinmaxWithPruning
from Algorithms.utilities import board_to_state


class AlgorithmFactory:
    def __init__(self, algorithm_name,depth):
        self.depth = depth
        self.algorithm_name = algorithm_name
        match algorithm_name:
            case "minmax without alpha-beta pruning":
                self.algorithm = Minmax()
            case "minmax with alpha-beta pruning":
                self.algorithm = MinmaxWithPruning()
            case "expected minmax":
                self.algorithm = ExpectedMinmax()
                
            
    def solve(self, board, turn = 2):
        self.algorithm.reset_attributes()
        if turn == 1 :
            agent_state = board_to_state(board, 1)
            human_state = board_to_state(board, 2)
        else :
            agent_state = board_to_state(board, 2)
            human_state = board_to_state(board, 1)
        if self.algorithm_name == "expected minmax":
            _, best_move = self.algorithm.solve(agent_state, human_state, 'max', depth=self.depth)
            return best_move, self.algorithm.tree, self.algorithm.node_expanded, self.algorithm.chance_nodes
        else:
            _, best_move = self.algorithm.solve(agent_state, human_state, True, self.depth)
        return best_move, self.algorithm.tree, self.algorithm.node_expanded
    