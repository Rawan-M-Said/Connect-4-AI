from Algorithms.algorithm import Algorithm
from heuristic import Heuristic
import math

class ExpectedMinmax(Algorithm):
    def __init__(self):
        self.chance_nodes = {}
        self.prev_node_type =  'max'
        super().__init__()

    def solve(self, agent_state, human_state, node_type, depth=10,column=0):
        
        # base case when depth is zero or the board is complete
        if depth == 0 or (agent_state + human_state) == (1<<42)-1:
            heuristic = Heuristic(agent_state, human_state)
            final_eval = heuristic.calculate_heuristic()
            self.save_node_in_tree(agent_state, human_state, None, None, final_eval, node_type)
            return final_eval, None

        best_col = None
        if node_type == 'max':
            self.prev_node_type = 'max'
            max_eval = -math.inf
            for i in range(7):
                lowest_row = self.get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                child_state = self.drop_disc(agent_state, i, lowest_row)
                final_eval, _ = self.solve(agent_state, human_state, 'chance', depth-1, i)
                self.save_node_in_tree(agent_state, human_state, child_state, i, final_eval, node_type)
                if max_eval < final_eval:
                    max_eval = final_eval
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
                final_eval, _ = self.solve(agent_state, human_state, 'chance', depth-1, i)
                self.save_node_in_tree(agent_state, human_state, child_state, i, final_eval, node_type)
                if min_eval > final_eval:
                    min_eval = final_eval
                    best_col = i
                    
            return min_eval, best_col


        elif node_type == 'chance':
            if self.prev_node_type == 'max':
                type = 'min'
            else:
                type = 'max'
            
            arr = [0, 1, -1]
            final_eval = 0
            parent_state = None
            
            for i in arr:
                curr_column = column + i
                if curr_column < 0 or curr_column > 6:
                    continue
                lowest_row = self.get_lowest_available_row(agent_state, human_state, curr_column)
                if lowest_row == -1 :
                    continue
                
                eval = 0 
                # if max -> drop in agent
                child_state = None
                if self.prev_node_type == 'max':
                    child_state = self.drop_disc(agent_state, curr_column, lowest_row)
                    if i == 0:
                        parent_state = child_state
                    eval, _ = self.solve(child_state, human_state, type,depth= depth-1)
                    self.save_node_in_tree(parent_state, human_state, child_state, curr_column, eval, node_type)

                else :
                    child_state = self.drop_disc(human_state, curr_column, lowest_row)
                    if i == 0:
                        parent_state = child_state
                    eval, _ = self.solve(agent_state, child_state, type,depth= depth-1)
                    self.save_node_in_tree(agent_state, parent_state, child_state, curr_column, eval, node_type)

                if i == 0:
                    final_eval += 0.6*eval
                else :
                    if column == 6 or column == 0:
                        final_eval +=0.4*eval
                    else:
                        final_eval +=0.2*eval
                    
            return final_eval,column
            
            
            
            
            
            
    def save_node_in_tree(self, agent_state, human_state, child_state, column, heuristic, node_type):
        self.node_expanded += 1
        
        parent_key = (agent_state, human_state)
        formatted_heuristic = f"{heuristic:.6f}".rstrip('0').rstrip(
            '.') if '.' in f"{heuristic:.6f}" else f"{heuristic:.6f}"
        
        if node_type == "chance":
            if parent_key not in self.tree:
                self.chance_nodes[parent_key] = []
            self.chance_nodes[parent_key].append({
                "column": column,
                "heuristic": formatted_heuristic,
                "agent_state": agent_state,
                "human_state": child_state,
            })
        else:
            if parent_key not in self.tree:
                self.tree[parent_key] = []
                
            if column is None:
                self.tree[parent_key].append({
                    "heuristic": formatted_heuristic
                })
            else:
                 self.tree[parent_key].append({
                    "column": column,
                    "heuristic": formatted_heuristic,
                    "agent_state": child_state,
                    "human_state": human_state,
                })
                
                   