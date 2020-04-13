#!/usr/bin/env python3
from tictactoe.TicTacToe import TicTacToe

if __name__ == '__main__':
    print("     --Tic-Tac-Toe--")
    game = TicTacToe(3)
    while game.getWinner() == None:
        game.showBoard()
        row, col = game.getMove()
