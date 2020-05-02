import os
import re
import secrets
import time
from enum import Enum


class TicTacToe:
    """Represents a game of tic-tac-toe"""

    class Turn(Enum):
        PLAYER = '█'
        COMPUTER = '░'

    class Error(Enum):
        INVALID = 'Invalid row and column chosen!'
        TAKEN = 'Spot has already been taken!'
        NOERR = 'No Error'

    def __init__(self, width=3, first='player', multi=False):
        """Initializes game according to given width, first, & multi params"""
        self.error = self.Error.NOERR
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
        """Return True if given cell is not taken, False otherwise"""

        return self.board[r][c] == ' '

    def _update_cell(self, r, c, val):
        """Update given cell's value with given val"""

        self.board[r][c] = val

    def _advance_turn(self):
        """Advances turn from PLAYER to COMPUTER, and vice-versa"""

        self.turn = (self.Turn.PLAYER if self.turn.name == 'COMPUTER' else
                     self.Turn.COMPUTER)

    def _reset_board(self):
        """Clears all cell values in the board"""

        self.board = [[' ' for _ in range(self.width)]
                      for _ in range(self.width)]

    @staticmethod
    def convert_row_col(row, col):
        """Returns row and col in 1-based alphanumeric grid notation

        Returns the alphabetic representation of the column first, followed
        by the numerical, 1-based representation of the row. 

        Examples:
            row=0, col=0 -> A1      row=0, col=1 -> B1
            row=1, col=0 -> A2      row=1, col=1 -> B2 . . .
            row=2, col=0 -> A3  .   row=2, col=1 -> B3
                                .
                                .
        """

        return chr(col + ord('A')) + str(row + 1)

    def get_winner(self):
        """Check all possible wins returning winner if found
        
        If win is found:
            Returns symbol in the winning streak

        If no win found:
            If more moves possible -> Returns None
            If no more moves       -> Returns 'T'
        """

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
        """Display current state of the board centered on the screen

        Makes the cells as large as they can be while still fitting on screen.
        Fills the entire cell with the shading for the cell's value.
        """

        # Determine dimensions based on current terminal window height/width
        screen_width = os.get_terminal_size().columns
        screen_height = os.get_terminal_size().lines

        # play_height is screen minus lines needed for info, error, prompt
        play_height = screen_height - 5

        # Determine max cell_height that will fit in play_height
        cell_height = (play_height - self.width) // self.width

        # Determine how many layers of a row before and after labelled layer
        cell_top_half = cell_bot_half = cell_height // 2
        if cell_height % 2 == 0:
            cell_top_half -= 1

        # Determine buffer needed to keep game full-screen and board centered
        buff_needed = play_height - (cell_height * self.width + self.width)
        buff_above = buff_needed // 2
        buff_below = buff_needed - buff_above

        # Start building strings that will make up board
        board_repr = ''
        row_sep = '┼'.join(['─' * cell_height for _ in range(self.width)])
        col_head = ' '.join([chr(65+i).center(cell_height)
                             for i in range(self.width)])

        # Add buffer above board to keep it centered & full-screen
        board_repr += "\n" * buff_above

        # Add the header showing the column labels
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
                                        ("".center(cell_height, cell))])
                               for col, cell in enumerate(row))

            # Add non-labelled, upper layers of row
            for _ in range(cell_top_half):
                board_repr += ("  " + row_repr).center(screen_width) + '\n'

            # Add labelled, middle layer of row
            board_repr += (f"{i+1} " + row_repr).center(screen_width) + '\n'

            # Add non-labelled, lower layers of row
            for _ in range(cell_bot_half):
                board_repr += ("  " + row_repr).center(screen_width) + '\n'

        # Add buffer below board to keep it centered & full-screen
        board_repr += "\n" * buff_below

        # Add error message
        board_repr += self.error.value

        print(board_repr)

    def show_info(self):
        """Print out game information

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
        """Update screen by calling show_info and then show_board"""

        self.show_info()
        self.show_board()

    def make_move(self):
        """Call make_player_move or make_computer_move

        Chosen call depends on the current turn, and opponent type.
        """
        if self.turn == self.Turn.PLAYER or self.multi:
            self.make_player_move()
        else:
            self.make_computer_move()

    def apply_move(self, row, col):
        """Update the given cell with the value of the current turn"""

        self._update_cell(row, col, self.turn.value)
        self.last_move['row'] = row
        self.last_move['col'] = col
        self._advance_turn()
        self.error = self.Error.NOERR

    def make_computer_move(self):
        """Randomly choose a spot for the computer to move"""

        sleep_time = 1 + secrets.randbelow(2)
        time.sleep(sleep_time)
        r, c = secrets.choice([(i, j)
                               for i in range(self.width)
                               for j in range(self.width)
                               if self.board[i][j] == ' '])
        self.apply_move(r, c)

    def make_player_move(self):
        """Collect player move

        If valid move   -> apply to board
        if invalid move -> update error msg
        """

        # Construct the patterns for valid col, row, choice
        validCol = ''.join([chr(x+97) for x in range(self.width)])
        validRow = ''.join(map(str, [x for x in range(1, self.width+1)]))
        ansPattern = f'[{validCol}][{validRow}]|[{validRow}][{validCol}]'

        # Get the player's choice
        # If invalid, update error and return
        msg = f'Player {self.turn.value} move: '
        ans = ''.join(input(msg).strip().split())
        if not re.fullmatch(ansPattern, ans.lower()):
            self.error = self.Error.INVALID
            return

        # Extract the row and col from choice
        try:
            # Assume ans in form \d\w
            r = int(ans[0]) - 1
            c = ord(ans[1].lower()) - 97
        except ValueError:
            # Ans must be in form \w\d
            r = int(ans[1]) - 1
            c = ord(ans[0].lower()) - 97

        if not self._spot_open(r, c):
            # Spot already taken, update error
            self.error = self.Error.TAKEN
        else:
            # Spot isn't taken, apply the valid move
            self.apply_move(r, c)
