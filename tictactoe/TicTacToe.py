import re, secrets

from enum import Enum

class TicTacToe:
    '''Represents a game of tic-tac-toe against a computer player.
    
    Args:
        size  (int): Size of the game board, defaults to 3
        first (str): Determines who makes the first move
            'p' for Player (default), 'c' for computer
    '''
    class Turn(Enum):
        PLAYER   = 'X'
        COMPUTER = 'O'

    def __init__(self, size=3, first='p'):
        self.size  = size
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.turn  = self.Turn.PLAYER   if first=='p' else\
                     self.Turn.COMPUTER if first=='c' else\
                     secrets.choice(list(self.Turn.__members__.values()))

    def _spotOpen(self, r, c):
        return self.board[r][c] == ' '

    def _updateCell(self, r, c, val):
        self.board[r][c] = val

    def _advanceTurn(self):
        self.turn = self.Turn.PLAYER if self.turn.name == 'COMPUTER' else self.Turn.COMPUTER

    def getWinner(self):
        # TODO: Implement a more efficient check of win, perhaps using last move
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
        diag1 = [self.board[r][c] for r in range(self.size) \
                                  for c in range(self.size) \
                                  if r == c]
        if diag1[0] != ' ' and diag1.count(diag1[0]) == self.size:
            return diag1[0]

        # Check top right to bot left diagonal win
        diag2 = [self.board[r][c] for r in range(self.size) \
                                  for c in range(self.size) \
                                  if r + c == self.size - 1]
        if diag2[0] != ' ' and diag2.count(diag2[0]) == self.size:
            return diag2[0]

        return None

    def showBoard(self):
        b = '\n\t  ' + ' '.join([chr(65+i) for i in range(self.size)]) + '\n'
        rowDiv = '\t  ' + ''.join([('─','┼')[i%2] for i in range(self.size*2-1)]) + '\n'
        for i, row in enumerate(self.board):
            if i != 0:
                b += rowDiv
            for j, cell in enumerate(row):
                leading  = f'\t{i+1} '   if j == 0          else '│'
                trailing = '\n' if j == self.size-1 else ''
                value = '.' if cell == ' ' else cell
                b += f'{leading}{value}{trailing}'
        print(b)

    def makeMove(self, msg="Where would you like to go? "):
        '''Updates state of the board, player, and move count

        '''
        validCol  = '[' + ''.join([chr(x+97) for x in range(self.size)])        + ']'
        validRow  = '[' + ''.join(map(str, [x for x in range(1, self.size+1)])) + ']'
        ansPattern = validCol + validRow + '|' + validRow + validCol
        ans = ''.join(input(msg).strip().split())
        while True:
            while not re.fullmatch(ansPattern, ans.lower()):
                msg = "Choose a valid row and column. "
                ans = ''.join(input(msg).strip().split())
            try:
                # Assume ans in form \d\w
                r = int(ans[0]) - 1
                c = ord(ans[1].lower()) - 97
            except ValueError:
                # Ans in form \w\d
                r = int(ans[1]) - 1
                c = ord(ans[0].lower()) - 97
            if not self._spotOpen(r,c):
                print("That spot has already been taken.")
                ans = ''
                continue
            else:
                break
        self._updateCell(r, c, self.turn.value)
        self._advanceTurn()
        return (r,c)
