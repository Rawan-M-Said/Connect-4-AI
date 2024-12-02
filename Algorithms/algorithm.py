

from Algorithms.expected_minmax import ExpectedMinmax
from Algorithms.minmax import Minmax
from Algorithms.minmax_with_pruning import MinmaxWithPruning
from Algorithms.utilities import board_to_state


class Algorithm:
    def __init__(self, algorithm):
        match algorithm:
            case "minmax without alpha-beta pruning":
                self.algorithm = Minmax()
            case "minmax with alpha-beta pruning":
                self.algorithm = MinmaxWithPruning()
            case _:
                self.algorithm = ExpectedMinmax()
        
    def solve(self, board):
        human_state = board_to_state(board, 1)
        agent_state = board_to_state(board, 2)
        _, best_move = self.algorithm.solve(agent_state, human_state, True, depth=4)
        return best_move, self.algorithm.tree