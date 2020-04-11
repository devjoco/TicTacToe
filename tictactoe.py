#!/usr/bin/env python3
class TicTacToe:
    ''' TicTacToe Class '''

    def __init__(self, size):
        self.board = [[' ' for _ in range(size)] for _ in range(size)]

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
        b = ''
        rowDiv  = ''.join([('─', '┼')[i%2] for i in range(len(self.board)*2-1)]) + '\n'
        for i, row in enumerate(self.board):
            if i != 0:
                b += rowDiv
            for j, cell in enumerate(row):
                leading  = ''   if j == 0          else '│'
                trailing = '\n' if j == len(row)-1 else ''
                value = '.' if cell == ' ' else cell
                b += f'{leading}{value}{trailing}'
        print(b)

if __name__ == '__main__':
    game = TicTacToe(3)
    while game.getWinner() == None:
        game.showBoard()
        move = input("Show board again? ")


