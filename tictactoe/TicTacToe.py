import re
import secrets

from enum import Enum


class TicTacToe:
    '''Represents a game of tic-tac-toe against a computer player.
    Args:
        size  (int): Size of the game board, defaults to 3
        first (str): Determines who makes the first move
            'p' for Player (default), 'c' for computer
    '''
    class Turn(Enum):
        PLAYER = 'X'
        COMPUTER = 'O'

    def __init__(self, size=3, first='p', multi=False):
        self.size = size
        self.multi = multi
        self.board = []
        for row in range(size):
            self.board.append([' ' for _ in range(size)])
        self.turn = self.Turn.PLAYER if first == 'player' else \
            self.Turn.COMPUTER if first == 'computer' else \
            secrets.choice(list(self.Turn.__members__.values()))

    def _spot_open(self, r, c):
        return self.board[r][c] == ' '

    def _update_cell(self, r, c, val):
        self.board[r][c] = val

    def _advance_turn(self):
        self.turn = self.Turn.PLAYER if self.turn.name == 'COMPUTER' else \
                self.Turn.COMPUTER

    def _reset_board(self):
        self.board = []
        for row in range(self.size):
            self.board.append([' ' for _ in range(self.size)])

    @staticmethod
    def convertRowCol(row, col):
        return chr(col + ord('A')) + str(row + 1)

    def get_winner(self):
        # TODO: Implement more efficient check of win, perhaps using last move
        # Check horizontal wins
        for r in range(self.size):
            row = self.board[r]
            leadChar = row[0]
            if leadChar != " " and row.count(leadChar) == self.size:
                return leadChar

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
        b = '\n\t  ' + ' '.join([chr(65+i) for i in range(self.size)]) + '\n'
        rowDiv = ''.join([('─', '┼')[i % 2] for i in range(self.size*2-1)])
        for i, row in enumerate(self.board):
            if i != 0:
                b += '\t  ' + rowDiv + '\n'
            for j, cell in enumerate(row):
                leading = f'\t{i+1} ' if j == 0 else '│'
                trailing = '\n' if j == self.size-1 else ''
                b += f'{leading}{cell}{trailing}'
        print(b)

    def comp_move(self):
        ''' Randomly chooses a spot for the computer to move '''
        r, c = secrets.choice([(i, j) 
                               for i in range(self.size)
                               for j in range(self.size)
                               if self.board[i][j] == ' '])
        self._update_cell(r, c, self.turn.value)
        self._advance_turn()
        return r, c


    def make_move(self):
        ''' Collect player move, and updates board, player '''
        validCol = ''.join([chr(x+97) for x in range(self.size)])
        validRow = ''.join(map(str, [x for x in range(1, self.size+1)]))
        ansPattern = f'[{validCol}][{validRow}]|[{validRow}][{validCol}]'
        msg = f'Player {self.turn.value} move: '
        ans = ''.join(input(msg).strip().split())
        while True:
            while not re.fullmatch(ansPattern, ans.lower()):
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
        self._update_cell(r, c, self.turn.value)
        self._advance_turn()
        return (r, c)
