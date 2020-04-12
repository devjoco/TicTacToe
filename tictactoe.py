#!/usr/bin/env python3
import re, secrets

class TicTacToe:
    ''' TicTacToe Class '''
    SYMBOLS = ('X', 'O')

    def __init__(self, size):
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.moves = 0
        self.player = secrets.randbelow(100) % 2

    def getWinner(self):
        # Check horizontal wins
        for r in range(len(self.board)):
            row = self.board[r]
            leadChar = row[0]
            if leadChar != " " and row.count(leadChar) == len(row):
                return leadChar

        # Check horizontal wins
        for c in range(len(self.board[0])):
            column = []
            for row in self.board:
                column.append(row[c])
            if column[0] != ' ' and column.count(column[0]) == len(column):
                return column[0]

        # Check top left to bot right diagonal win
        diag1 = [self.board[r][c] for r in range(len(self.board)) \
                                  for c in range(len(self.board)) \
                                  if r == c]
        if diag1[0] != ' ' and diag1.count(diag1[0]) == len(diag1):
            return diage1[0]

        # Check top right to bot left diagonal win
        diag1 = [self.board[r][c] for r in range(len(self.board)) \
                                  for c in range(len(self.board)) \
                                  if r + c == len(self.board)]
        if diag1[0] != ' ' and diag1.count(diag1[0]) == len(diag1):
            return diage1[0]

        return None

    def showBoard(self):
        b = '\n\t  ' + ' '.join([chr(65+i) for i in range(len(self.board))]) + '\n'
        rowDiv = '\t  ' + ''.join([('─','┼')[i%2] for i in range(len(self.board)*2-1)]) + '\n'
        for i, row in enumerate(self.board):
            if i != 0:
                b += rowDiv
            for j, cell in enumerate(row):
                leading  = f'\t{i+1} '   if j == 0          else '│'
                trailing = '\n' if j == len(row)-1 else ''
                value = '.' if cell == ' ' else cell
                b += f'{leading}{value}{trailing}'
        print(b)

    def spotOpen(self, r, c):
        return self.board[r][c] == ' '

    def getMove(self, msg="Where would you like to go? "):
        validCol  = '[' + ''.join([chr(x+97) for x in range(len(self.board))])        + ']'
        validRow  = '[' + ''.join(map(str, [x for x in range(1, len(self.board)+1)])) + ']'
        ansPattern = validCol + validRow + '|' + validRow + validCol
        ans = ''.join(input(msg).strip().split())
        while True:
            while not re.fullmatch(ansPattern, ans.lower()):
                msg = "Choose a valid row and column. "
                ans = ''.join(input(msg).strip().split())
            try:
                r = int(ans[0]) - 1
                c = ord(ans[1].lower()) - 97
            except ValueError:
                r = ord(ans[0].lower()) - 97
                c = int(ans[1]) - 1
            if not self.spotOpen(r,c):
                print("That spot has already been taken.")
                ans = ''
                continue
            else:
                break
        return (r,c)
    

if __name__ == '__main__':
    print("     --Tic-Tac-Toe--")
    game  = TicTacToe(3)
    while game.getWinner() == None:
        game.showBoard()
        row, col = game.getMove()



