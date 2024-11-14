class State:
    # The board is represented by 64-bit integer for each player.
    # Since there are 2 players, then there will be 2 integers.
    # The 1-bit indicates the presence of a disc, the 0-bit indicates an empty space.
    # The way of storing the board is by column.
    # The max board size can be stored is 8 * 8.

    # Suppose a 6 (rows/height) * 7 (columns/width):
        #           Column 1  Column 2  Column 3  Column 4  Column 5  Column 6  Column 7
        # Height 1  bit 0     bit 6     bit 12    bit 18    bit 24    bit 30    bit 36
        # Height 2  bit 1     bit 7     bit 13    bit 19    bit 25    bit 31    bit 37
        # Height 3  bit 2     bit 8     bit 14    bit 20    bit 26    bit 32    bit 38
        # Height 4  bit 3     bit 9     bit 15    bit 21    bit 27    bit 33    bit 39
        # Height 5  bit 4     bit 10    bit 16    bit 22    bit 28    bit 34    bit 40
        # Height 6  bit 5     bit 11    bit 17    bit 23    bit 29    bit 35    bit 41
    
    def __init__(self, player1_state=0, player2_state=0, column=7, height=6):
        self.player1_state = player1_state
        self.player2_state = player2_state
        self.max_column = column
        self.max_height = height

    def drop_disc(self, player_num, column):
        # Find the lowest available row in the chosen column
        base_pos = (column - 1) * self.max_height
        for row in range(self.max_height):
            pos =  base_pos + row
            if not ((self.player1_state & (1 << pos)) and (self.player2_state & (1 << pos))) :  # If position is empty
                if player_num == 1:
                    self.player1_state |= (1 << pos)  # Place the piece
                else:
                    self.player2_state |= (1 << pos)  # Place the piece
                return True

        return False  # indicates failure, so the player should consider another column

    # This function should be used in the algorithms, so as not to manipulate the original state
    # Then you can use the returned state to do whatever you want.
    def copy(self):
        # Create a copy of the current state
        return State(self.player1_state, self.player2_state, self.max_column, self.max_height)
    
    def is_board_complete(self):
        # Check if the board is full (no empty spots left)
        full_mask = (1 << (self.max_column * self.max_height)) - 1
        return (self.player1_state | self.player2_state) == full_mask
    
    # Horizontal check (shift by height to move to the next column)
    def _horizontal_check(self, state):
        score = 0
        horizontal = state & (state >> self.max_height)
        horizontal = horizontal & (horizontal >> (2 * self.max_height))
        while horizontal:
            horizontal &= horizontal - 1  # Clear the lowest set bit
            score += 1
        return score
    
    # Vertical check (shift by 1 within the column)
    def _vertical_check(self, state):
        score = 0
        for col in range(self.max_column):
            # Create a mask for the current column
            column_mask = (1 << self.max_height) - 1
            column_state = (state >> (col * self.max_height)) & column_mask  # isolate the current column

            # Check for consecutive pieces (vertical connect-four) in the current column
            row_mask = (1 << 4) - 1
            for row in range(self.max_height - 3):
                # Create 4 cosecutive 1-bits
                mask = row_mask << row
                if (column_state & mask) == mask:
                    score += 1  # if 4 consecutive bits are set, add to the score
        return score
    
    # Bottom-left to top-right diagonal (shift by max_height + 1)
    def _diagonal_check(self, state):
        score = 0
        for col in range(self.max_column - 3):
            for row in range(self.max_height - 3):
                # Create a mask for the diagonal from bottom-left to top-right
                mask = (1 << (col * self.max_height + row)) | \
                    (1 << ((col + 1) * self.max_height + (row + 1))) | \
                    (1 << ((col + 2) * self.max_height + (row + 2))) | \
                    (1 << ((col + 3) * self.max_height + (row + 3)))
                
                if (state & mask) == mask:
                    score += 1
        return score
    
    # Top-left to bottom-right diagonal (shift by max_height - 1)
    def _anti_diagonal_check(self, state):
        score = 0
        for col in range(self.max_column - 3):
            for row in range(3, self.max_height):
                # Create a mask for the diagonal from top-left to bottom-right
                mask = (1 << (col * self.max_height + row)) | \
                    (1 << ((col + 1) * self.max_height + (row - 1))) | \
                    (1 << ((col + 2) * self.max_height + (row - 2))) | \
                    (1 << ((col + 3) * self.max_height + (row - 3)))
                
                if (state & mask) == mask:
                    score += 1
        return score