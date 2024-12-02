import math
from Algorithms.algorithm import Algorithm
from heuristic import Heuristic


class MinmaxWithPruning(Algorithm):
    def __init__(self):
        super.__init__(self)
        
    def solve(self, agent_state, human_state, is_maximizing, depth=10):
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
                    
            return min_eval, best_col
    
    def save_node_in_tree(self, agent_state, human_state, child_state, column, heuristic, is_agent_move):
        
        parent_key = (agent_state, human_state)
        if parent_key not in self.tree:
            self.tree[parent_key] = []
            
        if column == None:
             self.tree[parent_key].append({
                "heuristic": heuristic       
            })
        elif is_agent_move:
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
            
    