from Algorithms.algorithm import Algorithm
from heuristic import Heuristic
import math

class ExpectedMinmax(Algorithm):
    def __init__(self):
        self.prev_node_type =  'max'
        super().__init__()

    def solve(self, agent_state, human_state, node_type, depth=10):
        print("Solving",depth)
        # base case when depth is zero or the board is complete
        if depth == 0 or (agent_state + human_state) == (1<<42)-1:
            heuristic = Heuristic(agent_state, human_state)
            eval = heuristic.calculate_heuristic()
            self.save_node_in_tree(agent_state, human_state, None, None, eval, node_type)
            return eval, None

        best_col = None
        if node_type == 'max':
            self.prev_node_type = 'max'
            max_eval = -math.inf
            for i in range(7):
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                child_state = self.drop_disc(agent_state, i, lowest_row)
                eval, _ = self.solve(child_state, human_state, 'chance', depth-1)
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, node_type)
                if max_eval < eval:
                    max_eval = eval
                    best_col = i
            return max_eval, best_col

        elif node_type == 'min':
            self.prev_node_type = 'min'
            min_eval = math.inf
            for i in range(7):
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                child_state = self.drop_disc(human_state, i, lowest_row)
                eval, _ = self.solve(agent_state, child_state, 'chance', depth-1)
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, node_type)
                if min_eval > eval:
                    min_eval = eval
                    best_col = i
            return min_eval, best_col

        elif node_type == 'chance':
            if self.prev_node_type == 'max':
                type = 'min'
            else:
                type = 'max'
            expected_eval = 0
            valid_moves = 0
            for i in range(7):
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                child_state = self.drop_disc(human_state, i, lowest_row)
                eval, _ = self.solve(agent_state, child_state, type, depth-1)
                self.save_node_in_tree(agent_state, human_state, child_state, i, eval, node_type)
                prob = 0.6
                expected_eval += prob * eval
                if i > 0:
                    left_child_state = self.drop_disc(human_state, i-1, self.get_lowest_available_row(agent_state, human_state, i-1))
                    left_eval, _ = self.solve(agent_state, left_child_state, type, depth-1)
                    expected_eval += 0.2 * left_eval
                if i < 6:
                    right_child_state = self.drop_disc(human_state, i+1, self.get_lowest_available_row(agent_state, human_state, i+1))
                    right_eval, _ = self.solve(agent_state, right_child_state, type, depth-1)
                    expected_eval += 0.2 * right_eval
                if i == 0:
                    right_child_state = self.drop_disc(human_state, i + 1,
                                                       self.get_lowest_available_row(agent_state, human_state, i + 1))
                    right_eval, _ = self.solve(agent_state, right_child_state, type, depth - 1)
                    expected_eval += 0.4 * right_eval
                if i == 6:
                    left_child_state = self.drop_disc(human_state, i - 1,
                                                      self.get_lowest_available_row(agent_state, human_state, i - 1))
                    left_eval, _ = self.solve(agent_state, left_child_state, type, depth - 1)
                    expected_eval += 0.4 * left_eval
                valid_moves += 1
            if valid_moves == 0:
                return 0, None
            return expected_eval / valid_moves, None

    def save_node_in_tree(self, agent_state, human_state, child_state, column, heuristic, node_type):
        self.node_expanded += 1
        parent_key = (agent_state, human_state)
        if parent_key not in self.tree:
            self.tree[parent_key] = []

        if column is None:
            self.tree[parent_key].append({
                "heuristic": heuristic
            })
        elif node_type == 'max':
            self.tree[parent_key].append({
                "column": column,
                "heuristic": heuristic,
                "agent_state": child_state,
                "human_state": human_state
            })
        elif node_type == 'min':
            self.tree[parent_key].append({
                "column": column,
                "heuristic": heuristic,
                "agent_state": agent_state,
                "human_state": child_state
            })
        elif node_type == 'chance':
            self.tree[parent_key].append({
                "column": column,
                "heuristic": heuristic,
                "agent_state": agent_state,
                "human_state": child_state
            })