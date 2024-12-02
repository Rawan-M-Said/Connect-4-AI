from math import ceil
from state import State

class Heuristic (State):
    def __init__(self, player1_state=0, player2_state=0, column=7, height=6):
        super().__init__(player1_state, player2_state, column, height)
        self.center_column = self.max_column // 2

    # Function to calculate score for each player based on the number of connect-fours
    def calculate_score(self):
        player1_score = self.count_connections(self.player1_state)
        player2_score = self.count_connections(self.player2_state)

        return player1_score, player2_score
    
    def count_connections(self, state):
            score = 0

            score += self._horizontal_check(state)
            score += self._vertical_check(state)
            score += self._diagonal_check(state)
            score += self._anti_diagonal_check(state)
            
            return score
    
    def calculate_heuristic(self):
        move_count = bin(self.player1_state | self.player2_state).count("1")

        if move_count < 15:  
            weights = {'center': 3, 'two_connect': 8, 'three_connect': 25}
        elif 15 <= move_count < 30:  
            weights = {'center': 2, 'two_connect': 10, 'three_connect': 30}
        else:  
            weights = {'center': 1, 'two_connect': 12, 'three_connect': 35}

        score = 0

        score += self.__evaluate(self.player1_state)
        score -= self.__evaluate(self.player2_state)

        # Adding center control
        score += self.__center_control(self.player1_state) * weights['center']
        score -= self.__center_control(self.player2_state) * weights['center']

        # Consider open spots to complete a connected 3/2 in a row
        score += self.__connected_3_or_2_with_open_spot(self.player1_state, weights)
        score -= self.__connected_3_or_2_with_open_spot(self.player2_state, weights)

        return score
    
    def __evaluate(self, state):
        score = 0
        
        # Check horizontal, vertical, diagonal, and anti-diagonal connections
        score += self._horizontal_check(state) * 10  # Horizontal gets moderate weight
        score += self._vertical_check(state) * 20    # Vertical is more important
        score += self._diagonal_check(state) * 20    # Diagonal gets moderate weight
        score += self._anti_diagonal_check(state) * 20  # Anti-diagonal gets moderate weight
        
        return score
    
    def __center_control(self, state):
        score = 0
        for col in range(self.center_column - 1, self.center_column + 2):
            column_mask = (1 << self.max_height) - 1
            column_state = (state >> (col * self.max_height)) & column_mask
            if column_state:
                score += 1  # Favor center placement
        return score
    
    def __connected_3_or_2_with_open_spot(self, state, weights):
        score = 0
        
        score += self.__connected_check_horizontal(state, weights)
        score += self.__connected_check_vertical(state, weights)
        score += self.__connected_check_diagonal(state, weights)
        score += self.__connected_check_anti_diagonal(state, weights)

        return score
    
    def __connected_check_horizontal(self, state, weights):
        score = 0
        for col in range(self.max_column - 1):
            for row in range(self.max_height):
                positions = [(row, col), (row, col + 1)]
                if col <= self.max_column - 3:
                    positions.append((row, col + 2))  # 3 connected horizontally
                    
                num_connected = self.__num_connected(state, positions)
                if num_connected == 3:
                    left_empty = self.__check_empty_slot(row, col + 3) if col <= self.max_column - 4 else False
                    right_empty = self.__check_empty_slot(row, col - 1) if col > 0 else False
                    if left_empty or right_empty:
                        score += weights['three_connect']  # Favor 3-connected with both sides open
                
                elif num_connected == 2:
                    left_empty = self.__check_empty_slot(row, col + 2) if col <= self.max_column - 3 else False
                    right_empty = self.__check_empty_slot(row, col - 1) if col > 0 else False
                    if left_empty or right_empty:
                        score += weights['two_connect']  # Favor 2-connected with one open side
        return score
    
    def __connected_check_vertical (self, state, weights):
        score = 0

        for col in range(self.max_column):
            for row in range(self.max_height - 1):
                num_connected = 0
                positions = [(row, col), (row + 1, col)]
                if row <= self.max_height - 3:
                    positions.append((row + 2, col))  # 3 connected vertically

                num_connected = self.__num_connected(state, positions)
                if num_connected == 3:
                    left_empty = self.__check_empty_slot(row + 3, col) if row <= self.max_height - 4 else False
                    right_empty = self.__check_empty_slot(row - 1, col) if row > 0 else False
                    if left_empty or right_empty:
                        score += weights['three_connect']  # Favor 3-connected with both sides open
                
                elif num_connected == 2:
                    left_empty = self.__check_empty_slot(row, col + 2) if col <= self.max_column - 3 else False
                    right_empty = self.__check_empty_slot(row, col - 1) if col > 0 else False
                    if left_empty or right_empty:
                        score += weights['two_connect']  # Favor 2-connected with one open side
        return score

    def __connected_check_diagonal(self, state, weights):
        score = 0

        for col in range(self.max_column - 2):
            for row in range(self.max_height - 2):
                num_connected = 0
                positions = [(row, col), (row + 1, col + 1)]
                if row <= self.max_height - 3 and col <= self.max_column - 3:
                    positions.append((row + 2, col + 2))  # 3 connected diagonally

                num_connected = self.__num_connected(state, positions)
                if num_connected == 3:
                    left_empty = self.__check_empty_slot(row + 3, col + 3) if row <= self.max_height - 4 and col <= self.max_column - 4 else False
                    right_empty = self.__check_empty_slot(row - 1, col - 1) if row > 0 and col > 0 else False
                    if left_empty or right_empty:
                        score += weights['three_connect']  # Favor 3-connected with both sides open
                
                elif num_connected == 2:
                    left_empty = self.__check_empty_slot(row + 2, col + 2) if row <= self.max_height - 3 and col <= self.max_column - 3 else False
                    right_empty = self.__check_empty_slot(row - 1, col - 1) if row > 0 and col > 0 else False
                    if left_empty or right_empty:
                        score += weights['two_connect']  # Favor 2-connected with one open side
        return score

    def __connected_check_anti_diagonal(self, state, weights):
        score = 0

        for col in range(self.max_column - 2):
            for row in range(self.max_height):
                num_connected = 0
                if row >= 2 :
                    positions = [(row, col), (row - 1, col + 1)]
                    if row >= 2 and col <= self.max_column - 3:
                        positions.append((row - 2, col + 2))  # 3 connected anti-diagonally

                    num_connected = self.__num_connected(state, positions)
                    if num_connected == 3:
                        left_empty = self.__check_empty_slot(row - 3, col + 3) if row >= 3 and col <= self.max_column - 4 else False
                        right_empty = self.__check_empty_slot(row + 1, col - 1) if row <= self.max_height - 2 and col > 0 else False
                        if left_empty or right_empty:
                            score += weights['three_connect']  # Favor 3-connected with both sides open
                    
                    elif num_connected == 2:
                        left_empty = self.__check_empty_slot(row - 2, col + 2) if row >=2 and col <= self.max_column - 3 else False
                        right_empty = self.__check_empty_slot(row + 1, col - 1) if row <= self.max_height - 2 and col > 0 else False
                        if left_empty or right_empty:
                            score += weights['two_connect']  # Favor 2-connected with one open side
        return score
    
    def __num_connected(self, state, positions):
        # Count how many of the positions are occupied by the player
        num_connected = 0
        for r, c in positions:
            pos = r + c * self.max_height
            if state & (1 << pos):
                num_connected += 1
        return num_connected

    def __check_empty_slot(self, row, col):
        board = self.player1_state | self.player2_state
        empty = not(board & (1 << (row + col * self.max_height)))
        return empty