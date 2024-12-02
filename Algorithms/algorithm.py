class Algorithm:
    def __init__(self):
        self.tree = {}
        self.node_expanded = 0
        
    def reset_attributes(self):
        self.tree = {}
        self.node_expanded = 0
    
    @staticmethod
    def drop_disc(player_state, column, row):
        pos = column * 6 + row
        return player_state | (1 << pos)  # Place the piece
    
    @staticmethod
    def get_lowest_available_row(agent_state, human_state, column):
        base_pos = column * 6
        for row in range(6):
            pos =  base_pos + row
            if not ((agent_state & (1 << pos)) or (human_state & (1 << pos))) :  
                return row
        return -1
    
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
            
                
            