import sys
from heuristic import Heuristic
from state import State
from utilites import *
import math

class Minmax:
    def __init__(self):
        self.tree = {}
        
    def minmax(self, agent_state, human_state, is_maximizing, depth=10):
        # base case when depth is zero or the board is complete
        if depth == 0 or (agent_state + human_state) == (2**42)-1:
            heuristic = Heuristic(agent_state, human_state)
            return heuristic.calculate_heuristic()

        if is_maximizing:
            max_eval = -math.inf
            # check all possible children
            for i in range (7):
                # check if it's possible to drop the disc
                lowest_row = get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = drop_disc(agent_state, i, lowest_row)
                eval = self.minmax(child_state, human_state , depth-1, not is_maximizing)
                # save in the tree
                if max_eval < eval :
                    max_eval = eval
                
            return max_eval
                
        else :
            min_eval = math.inf
            # check all possible children
            for i in range (7):
                # check if it's possible to drop the disc
                lowest_row = get_lowest_available_row(agent_state, human_state, i)
                if lowest_row == -1:
                    continue
                
                # drop it and get the state => child
                child_state = drop_disc(human_state, i, lowest_row)
                eval = self.minmax(agent_state, child_state, depth-1, not is_maximizing)
                # save in the tree
                min_eval = min(min_eval, eval)
            return min_eval
            
    