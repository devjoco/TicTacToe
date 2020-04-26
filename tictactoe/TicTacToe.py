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

    def __init__(self, size=3, first='player', multi=False, cell_width=1):
        self.size = size
        self.first = first
        self.multi = multi
        self.cell_width = cell_width
        self.last_move = {'row': None, 'col': None}
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.turn = self.Turn.PLAYER
        if first == 'computer':
            self.turn = self.Turn.COMPUTER
        elif first == 'random':
            self.turn = secrets.choice(list(self.Turn.__members__.values()))

    def _spot_open(self, r, c):
        return self.board[r][c] == ' '

    def _update_cell(self, r, c, val):
        self.board[r][c] = val

    def _advance_turn(self):
        self.turn = self.Turn.PLAYER if self.turn.name == 'COMPUTER' else \
                self.Turn.COMPUTER

    def _reset_board(self):
        self.board = [[' ' for _ in range(self.size)]
                      for _ in range(self.size)]

    @staticmethod
    def convert_row_col(row, col):
        return chr(col + ord('A')) + str(row + 1)

    def get_winner(self):
        # TODO: Implement more efficient check of win, perhaps using last move
        # Check horizontal wins
        for r in range(self.size):
            row = self.board[r]
            lead_char = row[0]
            if lead_char != " " and row.count(lead_char) == self.size:
                return lead_char

        # Check vertical wins
        for c in range(self.size):
            column = []
            for row in self.board:
                column.append(row[c])
            if column[0] != ' ' and column.count(column[0]) == self.size:
                return column[0]

        # Check top left to bot right diagonal win
        diag1 = [self.board[r][c]
                 for r in range(self.size)
                 for c in range(self.size)
                 if r == c]
        if diag1[0] != ' ' and diag1.count(diag1[0]) == self.size:
            return diag1[0]

        # Check top right to bot left diagonal win
        diag2 = [self.board[r][c]
                 for r in range(self.size)
                 for c in range(self.size)
                 if r + c == self.size - 1]
        if diag2[0] != ' ' and diag2.count(diag2[0]) == self.size:
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
        row_sep = '┼'.join(['─' * self.cell_width for _ in range(self.size)])
        col_head = ' '.join([chr(65+i).center(self.cell_width)
                             for i in range(self.size)])

        # Add the header showing the column labels
        board_repr += "\n" + ("  " + col_head).center(screen_width) + "\n"

        # Add each of the rows, and cell_buff's if necessary
        for i, row in enumerate(self.board):
            # Add row_sep if not first row
            if i != 0:
                board_repr += ("  " + row_sep).center(screen_width) + "\n"

            # Determine row_repr
            row_repr = ""
            for col, cell in enumerate(row):
                lead_val = "" if col == 0 else "│"
                cell_val = "".center(self.cell_width, cell)
                # tail_val = "" if col != self.size - 1 else "\n"
                row_repr += lead_val + cell_val #+ tail_val

            # Add non-labelled, upper layers of row
            for _ in range(self.cell_width // 2):
                board_repr += ("  " + row_repr).center(screen_width) + '\n'

            # Add labelled, middle layer of row
            board_repr += (f"{i+1} " + row_repr).center(screen_width) + '\n'

            # Add non-labelled, lower layers of row
            for _ in range(self.cell_width // 2):
                board_repr += ("  " + row_repr).center(screen_width) + '\n'
        print(board_repr)

    def show_info(self):
        """Prints out a heading which will show the games info.

        This includes:
            - Whether it is against a computer or another player
            - The dimensions of the tic tac toe board
            - Who the first move is, and whether that was randomly chosen
        """

        play_area = (self.size * 2 - 1) + 18
        user = 'Player' if self.multi or self.turn == self.Turn.PLAYER else \
               'Computer'
        sym = '\b' if user == 'Computer' else \
              self.turn.value
        rand = '' if self.first != 'random' else \
               'Randomly chosen'
        print('Tic Tac Toe'.center(play_area, '-'))
        print(f'{self.size}x{self.size}'.center(play_area))
        print(f'{user} {sym} first!'.center(play_area))
        print(f'{rand}'.center(play_area))

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
                               for i in range(self.size)
                               for j in range(self.size)
                               if self.board[i][j] == ' '])
        self.apply_move(r, c)
        chosen_spot = self.convert_row_col(**self.last_move)
        print(f'Computer went in {chosen_spot}')

    def make_player_move(self):
        """Collect player move, and updates board, player."""

        validCol = ''.join([chr(x+97) for x in range(self.size)])
        validRow = ''.join(map(str, [x for x in range(1, self.size+1)]))
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
