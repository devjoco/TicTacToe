import os
import re
import secrets
import time
from enum import Enum


class TicTacToe:
    """Represents a game of tic-tac-toe."""

    class Turn(Enum):
        PLAYER = '█'
        COMPUTER = '░'

    def __init__(self, width=3, first='player', multi=False):
        self.width = width
        self.first = first
        self.random = False
        self.multi = multi
        self.last_move = {'row': None, 'col': None}
        self.board = [[' ' for _ in range(width)] for _ in range(width)]
        self.turn = self.Turn.PLAYER
        if first == 'computer':
            self.turn = self.Turn.COMPUTER
        elif first == 'random':
            self.turn = secrets.choice(list(self.Turn.__members__.values()))
            self.first = self.turn.name.lower()
            self.random = True

    def _spot_open(self, r, c):
        return self.board[r][c] == ' '

    def _update_cell(self, r, c, val):
        self.board[r][c] = val

    def _advance_turn(self):
        self.turn = (self.Turn.PLAYER if self.turn.name == 'COMPUTER' else
                     self.Turn.COMPUTER)

    def _reset_board(self):
        self.board = [[' ' for _ in range(self.width)]
                      for _ in range(self.width)]

    @staticmethod
    def convert_row_col(row, col):
        return chr(col + ord('A')) + str(row + 1)

    def get_winner(self):
        # TODO: Implement more efficient check of win, perhaps using last move
        # Check horizontal wins
        for r in range(self.width):
            row = self.board[r]
            lead_char = row[0]
            if lead_char != " " and row.count(lead_char) == self.width:
                return lead_char

        # Check vertical wins
        for c in range(self.width):
            column = []
            for row in self.board:
                column.append(row[c])
            if column[0] != ' ' and column.count(column[0]) == self.width:
                return column[0]

        # Check top left to bot right diagonal win
        diag1 = [self.board[r][c]
                 for r in range(self.width)
                 for c in range(self.width)
                 if r == c]
        if diag1[0] != ' ' and diag1.count(diag1[0]) == self.width:
            return diag1[0]

        # Check top right to bot left diagonal win
        diag2 = [self.board[r][c]
                 for r in range(self.width)
                 for c in range(self.width)
                 if r + c == self.width - 1]
        if diag2[0] != ' ' and diag2.count(diag2[0]) == self.width:
            return diag2[0]

        # Check for tie
        blanks = 0
        for row in self.board:
            blanks += row.count(' ')
        if blanks == 0:
            return 'T'

        return None

    def show_board(self):
        """Displays the current state of the board centered on the screen.

        Fills the entire cell with the shading for the current player's turn.
        """

        board_repr = ''       # The string repr of the board to be printed
        screen_width = os.get_terminal_size().columns
        screen_height = os.get_terminal_size().lines
        cell_width = (screen_height - 9 - self.width) // self.width
        buffer_needed = screen_height - 9 - (cell_width * self.width)
        buffer_above = buffer_needed // 2
        buffer_below = buffer_needed - buffer_above
        row_sep = '┼'.join(['─' * cell_width for _ in range(self.width)])
        col_head = ' '.join([chr(65+i).center(cell_width)
                             for i in range(self.width)])

        # Add the header showing the column labels
        board_repr += "\n" * buffer_above
        board_repr += ("  " + col_head).center(screen_width) + "\n"

        # Add each of the rows, and cell_buff's if necessary
        for i, row in enumerate(self.board):
            # Add row_sep if not first row
            if i != 0:
                board_repr += ("  " + row_sep).center(screen_width) + "\n"

            # Determine row_repr to be used for each layer of row
            # Builds each row from the "leader" char and the cell value
            # Leader char is vertical bar if cell is not first cell
            row_repr = "".join("".join([("" if col == 0 else "│"),
                                        ("".center(cell_width, cell))])
                               for col, cell in enumerate(row))

            # Add non-labelled, upper layers of row
            for _ in range(cell_width // 2):
                board_repr += ("  " + row_repr).center(screen_width) + '\n'

            # Add labelled, middle layer of row
            board_repr += (f"{i+1} " + row_repr).center(screen_width) + '\n'

            # Add non-labelled, lower layers of row
            for _ in range(cell_width // 2):
                board_repr += ("  " + row_repr).center(screen_width) + '\n'
        board_repr += "\n" * buffer_below
        print(board_repr)

    def show_info(self):
        """Prints out a heading which will show the games info.

        Takes up three lines of the screen and includes:
            - Whether it is against a computer or another player
            - The dimensions of the tic tac toe board
            - Who the first move is, and whether that was randomly chosen

        Example:
        ~~~~~~~~~~~~~~~~~~~~~~~~~ Tic Tac Toe ~~~~~~~~~~~~~~~~~~~~~~~~~
        First Move: Player █       3x3 Board         Opponent: Computer
        Last Move: Computer ░ A3
        """

        screen_width = os.get_terminal_size().columns
        opponent = 'Human' if self.multi else 'Computer'
        first_turn = (self.Turn.PLAYER if self.first == 'player' else
                      self.Turn.COMPUTER)
        first_name = first_turn.name.capitalize()
        first_repr = f'First Move: {first_name} {first_turn.value}'
        oppon_repr = f'Opponent: {opponent}'
        dimen_width = screen_width - sum(map(len, [first_repr, oppon_repr]))
        dimen_repr = f'{self.width}x{self.width} Board'.center(dimen_width)
        info_repr = ''.join([first_repr, dimen_repr, oppon_repr])
        last_repr = ''
        if self.last_move['row'] is not None:
            last_turn = (self.Turn.PLAYER if self.turn == self.Turn.COMPUTER
                         else self.Turn.COMPUTER)
            last_name = last_turn.name.capitalize()
            last_value = last_turn.value
            last_spot = self.convert_row_col(**self.last_move)
            last_repr = ('' if self.last_move['row'] is None else
                         f'Last Move: {last_name} {last_value} {last_spot}')
        print('Tic Tac Toe'.center(screen_width, '~'))
        print(info_repr)
        print(last_repr)

    def show_game(self):
        """Update the terminal screen with the current state of the game.

        Elements of the screen:
        Title/Header: Name of game, dimensions, solo vs multi, first(random?)
        Last Move: Show's who went last and in what spot. Empty line if N/A
        Play Area: State of board w/ row/col labels
        Error Msg: Display if user chose invalid/taken spot. Empty if N/A

        Title/Header and Last Move takes up two lines to the top, Error Msg &
        prompt for next move takes two lines on bottom, Play Area takes up
        remaining lines in between.
        """

        self.show_info()
        self.show_board()

    def make_move(self):
        if self.turn == self.Turn.PLAYER or self.multi:
            self.make_player_move()
        else:
            self.make_computer_move()

    def apply_move(self, row, col):
        self._update_cell(row, col, self.turn.value)
        self.last_move['row'] = row
        self.last_move['col'] = col
        self._advance_turn()

    def make_computer_move(self):
        """Randomly chooses a spot for the computer to move."""

        print("Computer is thinking...")
        sleep_time = 1 + secrets.randbelow(2)
        time.sleep(sleep_time)
        r, c = secrets.choice([(i, j)
                               for i in range(self.width)
                               for j in range(self.width)
                               if self.board[i][j] == ' '])
        self.apply_move(r, c)
        chosen_spot = self.convert_row_col(**self.last_move)
        print(f'Computer went in {chosen_spot}')

    def make_player_move(self):
        """Collect player move, and updates board, player."""

        validCol = ''.join([chr(x+97) for x in range(self.width)])
        validRow = ''.join(map(str, [x for x in range(1, self.width+1)]))
        ansPattern = f'[{validCol}][{validRow}]|[{validRow}][{validCol}]'
        msgLead = '\n' if not self.multi else ''
        msg = f'{msgLead}Player {self.turn.value} move: '
        ans = ''.join(input(msg).strip().split())
        while True:
            while not re.fullmatch(ansPattern, ans.lower()):
                if ans != '':
                    print("Choose a valid row and column.")
                ans = ''.join(input(msg).strip().split())
            try:
                # Assume ans in form \d\w
                r = int(ans[0]) - 1
                c = ord(ans[1].lower()) - 97
            except ValueError:
                # Ans in form \w\d
                r = int(ans[1]) - 1
                c = ord(ans[0].lower()) - 97
            if not self._spot_open(r, c):
                print("That spot has already been taken.")
                ans = ''
                continue
            else:
                break
        self.apply_move(r, c)
