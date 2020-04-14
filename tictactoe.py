#!/usr/bin/env python3
from tictactoe.TicTacToe import TicTacToe

if __name__ == '__main__':
    print("     --Tic-Tac-Toe--")
    game = TicTacToe(3)
    while game.getWinner() == None:
        game.showBoard()
        currPlayer = game.turn.value
        row, col = game.makeMove()
        print(f'\nPlayer {currPlayer} went in ({row},{col})\n')
    game.showBoard()
    print(game.getWinner())
