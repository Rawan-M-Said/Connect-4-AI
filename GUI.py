import pygame
import pygame_menu
import sys
import numpy as np

from Algorithms.algorithm_factory import AlgorithmFactory
from heuristic import Heuristic
from Algorithms.utilities import board_to_state, state_to_board

SQUARE_SIZE = 100
NAVBAR_SIZE = 400
BLUE_COLOR = (41, 102, 182)
RED_COLOR = (255, 34, 59)
GREEN_COLOR = (50, 222, 132)
YELLOW_COLOR = (255, 190, 38)
BACKGROUND_COLOR = (20, 55, 112)
WHITE_COLOR = (255, 255, 255)
GRAY_COLOR = (128, 128, 128)
FONT_SIZE = 32
FONT_FAMILY = 'fonts/Doto.ttf'




class ConnectFour:
    def __init__(self, columns=7, rows=6):
        pygame.init()
        self.columns = columns
        self.rows = rows
        self.board = np.zeros((rows, columns), dtype=int)
        self.turn = 1
        self.game_over = False
        self.winner = None
        self.moves = 0
        self.player1_score = 0
        self.player2_score = 0
        self.boardCopy = self.board.copy()
        self.x_offsets = []
        self.tree = {}
        self.current_depth = 1
        self.depth = 4
        self.selected_algorithm = "minmax without alpha-beta pruning"
        self.selected_depth = 1
        self.node_expanded = 0

    def main_menu(self):
        width = self.columns * SQUARE_SIZE + NAVBAR_SIZE
        height = (self.rows + 1) * SQUARE_SIZE
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Connect Four - Main Menu")

        menu = pygame_menu.Menu('Connect Four', width, height, theme=pygame_menu.themes.THEME_DARK)

        algorithms = ["minmax without alpha-beta pruning", "minmax with alpha-beta pruning", "expected minmax"]
        depths = list(range(1, 11))

        def set_algorithm(value, algorithm):
            self.selected_algorithm = algorithm

        def set_depth(value, depth):
            self.selected_depth = depth

        menu.add.selector('Algorithm: ', [(alg, alg) for alg in algorithms], onchange=set_algorithm)
        menu.add.selector('Depth: ', [(str(depth), depth) for depth in depths], onchange=set_depth)
        menu.add.button('Play', self.start_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(screen)

    def start_game(self):
        self.depth = self.selected_depth
        self.algorithm = AlgorithmFactory(self.selected_algorithm, self.depth)
        self.main()

    # Check if column is not full
    def is_valid_column(self, column,board):
        return board[0][column] == 0

    # Get the next open row in the column
    def get_next_open_row(self, column,board):
        for r in range(self.rows - 1, -1, -1):
            if board[r][column] == 0:
                return r

    # Make a move
    def drop_piece(self, column):
        if not self.is_valid_column(column,self.board):
            return False
        row = self.get_next_open_row(column,self.board)
        self.board[row][column] = self.turn
        self.moves += 1



    # Check for connect four
    def check_connect_four(self, player, row, col):
        player1_bitboard = board_to_state(self.board, 1)
        player2_bitboard = board_to_state(self.board, 2)
        state = Heuristic(player1_bitboard, player2_bitboard)

        self.player1_score, self.player2_score = state.calculate_score()

    def draw_navbar(self, screen):
        pygame.draw.rect(screen, BACKGROUND_COLOR, (self.columns * SQUARE_SIZE, 0, NAVBAR_SIZE, (self.rows + 1) * SQUARE_SIZE))
        font = pygame.font.Font(FONT_FAMILY, FONT_SIZE)
        text = font.render("Player {}'s turn".format(self.turn), True, RED_COLOR if self.turn == 1 else YELLOW_COLOR)
        screen.blit(text, (self.columns * SQUARE_SIZE + 50, 100))
        text = font.render("Player 1: {}".format(self.player1_score), True, RED_COLOR)
        screen.blit(text, (self.columns * SQUARE_SIZE + 50, 200))
        text = font.render("Player 2: {}".format(self.player2_score), True, YELLOW_COLOR)
        screen.blit(text, (self.columns * SQUARE_SIZE + 50, 250))
        # Define margin and border size
        margin = 20
        border_size = 2

        # Render text
        text = font.render("Show Tree", True, WHITE_COLOR)
        text_rect = text.get_rect()
        text_rect.topleft = (self.columns * SQUARE_SIZE + 60 + margin, 550 + margin)

        # Draw border
        border_rect = pygame.Rect(text_rect.left - margin, text_rect.top - margin, text_rect.width + 2 * margin,
                                  text_rect.height + 2 * margin)
        pygame.draw.rect(screen, WHITE_COLOR, border_rect, border_size)

        # Blit text
        screen.blit(text, text_rect.topleft)

    def draw_winner(self, screen):
        font = pygame.font.Font(FONT_FAMILY, FONT_SIZE)
        if self.player1_score > self.player2_score:
            winner = "Player 1 wins"
            color = RED_COLOR
            img = "images/winner.png"
        elif self.player1_score < self.player2_score:
            winner = "Player 2 wins"
            color = YELLOW_COLOR
            img = "images/loser.png"
        else:
            winner = "It's a draw"
            color = GREEN_COLOR
            img = "images/handshake.png"
        text = font.render(winner, True, color)
        screen.blit(text, (self.columns * SQUARE_SIZE + 50, 350))
        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (100, 100))
        screen.blit(image, (self.columns * SQUARE_SIZE + 150, 400))

    def draw_board(self, screen, board, x_offset=0, y_offset=0, scale=1):
        scaled_square_size = int(SQUARE_SIZE * scale)
        pygame.draw.rect(screen, BACKGROUND_COLOR,
                         (x_offset, y_offset, self.columns * scaled_square_size, self.rows * scaled_square_size))
        pygame.draw.rect(screen, BLUE_COLOR,
                         (x_offset, y_offset + scaled_square_size, self.columns * scaled_square_size,
                          self.rows * scaled_square_size))
        for c in range(self.columns):
            for r in range(self.rows):
                color = BACKGROUND_COLOR
                if board[r][c] == 1:
                    color = RED_COLOR
                elif board[r][c] == 2:
                    color = YELLOW_COLOR
                pygame.draw.circle(
                    screen,
                    color,
                    (
                        int(c * scaled_square_size + scaled_square_size / 2) + x_offset,
                        int(r * scaled_square_size + scaled_square_size + scaled_square_size / 2) + y_offset
                    ),
                    int(45 * scale)
                )

    def draw_circle(self, screen, posix,width):
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, width, SQUARE_SIZE))
        if posix < SQUARE_SIZE / 2:
            posix = 0 + int(SQUARE_SIZE / 2)
        elif posix > width - SQUARE_SIZE / 2:
            posix = width - int(SQUARE_SIZE / 2)
        if self.turn == 1:
            color = RED_COLOR
        else:
            color = YELLOW_COLOR
        pygame.draw.circle(screen, color, (posix, int(SQUARE_SIZE / 2)), 45)
        pygame.display.update()

    def generate_children(self, player=2, parent=None):
        children = []
        player1_bitboard = board_to_state(parent, 1)
        player2_bitboard = board_to_state(parent, 2)
        heuristic = self.tree.get((player2_bitboard, player1_bitboard))
        if heuristic:
            for state in heuristic:
                if 'agent_state' in state and 'human_state' in state:
                    child_agent = state['agent_state']
                    child_human = state['human_state']
                    child = state_to_board( child_human,child_agent)
                    children.append((child, state['heuristic']))
            return children
    def draw_children(self, screen, children):
        child_width = self.columns * SQUARE_SIZE // 7
        child_height = self.rows * SQUARE_SIZE // 7
        margin = 40
        parent_x = (screen.get_width() - self.columns * SQUARE_SIZE // 7) // 2 + self.columns * SQUARE_SIZE // 14
        parent_y = 100 + self.rows * SQUARE_SIZE // 7 + 15
        font = pygame.font.Font(None, FONT_SIZE)

        self.x_offsets = []
        for i, child in enumerate(children):
            x_offset = (i % 7) * (child_width + margin) + 80
            y_offset = 400
            self.x_offsets.append(x_offset)
            child_center_x = x_offset + child_width // 2
            child_center_y = y_offset

            # Draw line from parent to child
            pygame.draw.line(screen, WHITE_COLOR, (parent_x, parent_y), (child_center_x, child_center_y), 2)

            self.draw_board(screen, child[0], x_offset, y_offset, scale=1 / 7)
            # Draw number below child board
            text = font.render(str(child[1]), True, WHITE_COLOR)
            text_rect = text.get_rect(center=(child_center_x, y_offset + child_height + 30))
            screen.blit(text, text_rect)

    def show_tree(self, player, board, previous_states=[]):
        width = self.columns * SQUARE_SIZE + NAVBAR_SIZE
        height = (self.rows + 1) * SQUARE_SIZE
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Tree Visualisation")
        screen.fill(GRAY_COLOR)
        children = self.generate_children(player, board)
        x_offset = (width - self.columns * SQUARE_SIZE // 7) // 2
        self.draw_board(screen, board, x_offset, 100, scale=1 / 7)
        self.draw_children(screen, children)
        pygame.display.update()

        # Back button image
        back_button = pygame.image.load("images/back.png")
        back_button = pygame.transform.scale(back_button, (50, 50))
        screen.blit(back_button, (10, 10))

        # forward button image
        forward_button = pygame.image.load("images/forward.png")
        forward_button = pygame.transform.scale(forward_button, (50, 50))
        screen.blit(forward_button, (width - 60, 10))

        # Node expanded
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render("Nodes Expanded: {}".format(self.node_expanded), True, WHITE_COLOR)
        screen.blit(text, (width // 2 - 100, 50))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 10 < event.pos[0] < 60 and 10 < event.pos[1] < 60:
                            self.current_depth = 1
                            self.main()
                    if width - 60 < event.pos[0] < width - 10 and 10 < event.pos[1] < 60:
                        if previous_states:
                            self.current_depth -= 1
                            last_state = previous_states.pop()
                            self.show_tree(last_state['player'], last_state['board'], previous_states)
                    if 400 < event.pos[1] < 500:

                        if self.current_depth < self.depth:
                            self.current_depth += 1
                            for i, x_offset in enumerate(self.x_offsets):
                                if x_offset < event.pos[0] < x_offset + 100:
                                    player = 1 if player == 2 else 2
                                    previous_states.append({'player': player, 'board': board})
                                    self.show_tree(player, children[i][0], previous_states)

    def ai_move(self):
        best_move, self.tree,self.node_expanded = self.algorithm.solve(self.board)
        self.drop_piece(best_move)
        self.check_connect_four(self.turn, self.get_next_open_row(best_move,self.board), best_move)
        self.turn = 1  # Switch back to the human player


    def main(self):
        width = self.columns * SQUARE_SIZE
        height = (self.rows + 1) * SQUARE_SIZE
        size = (width + NAVBAR_SIZE, height)
        screen = pygame.display.set_mode(size)
        self.draw_board(screen, self.board)
        self.draw_navbar(screen)
        pygame.display.update()
        pygame.display.set_caption("Connect Four")
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.main_menu()
                        return
                if event.type == pygame.MOUSEMOTION:
                    posix = event.pos[0]
                    self.draw_circle(screen, posix, width)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.columns * SQUARE_SIZE + 60 < event.pos[
                        0] < self.columns * SQUARE_SIZE + 60 + 200 and 550 < \
                            event.pos[1] < 550 + 50:
                        self.show_tree(2, self.boardCopy)
                    if self.turn == 1:  # Human player's turn
                        if event.pos[0] > width:
                            continue
                        column = int(event.pos[0] // SQUARE_SIZE)
                        if self.is_valid_column(column, self.board):
                            row = self.get_next_open_row(column, self.board)
                            self.drop_piece(column)
                            self.check_connect_four(self.turn, row, column)
                            self.boardCopy = self.board.copy()
                            self.turn = 2  # Switch to AI's turn
                            self.draw_board(screen, self.board)
                            self.draw_navbar(screen)
                            pygame.display.update()
                            if self.moves == self.columns * self.rows:
                                self.game_over = True
                                self.draw_winner(screen)
                                pygame.display.update()
                            if self.game_over:
                                pygame.time.wait(3000)
                                pygame.quit()
                                sys.exit()
            if self.turn == 2 and not self.game_over:  # AI's turn
                self.ai_move()
                self.draw_board(screen, self.board)
                self.draw_navbar(screen)
                pygame.display.update()
                if self.moves == self.columns * self.rows:
                    self.game_over = True
                    self.draw_winner(screen)
                    pygame.display.update()
                if self.game_over:
                    pygame.time.wait(3000)
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    game = ConnectFour()
    game.main_menu()