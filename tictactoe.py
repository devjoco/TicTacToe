#!/usr/bin/env python3
from tictactoe.TicTacToe import TicTacToe

if __name__ == '__main__':
    print("     --Tic-Tac-Toe--")
    game = TicTacToe(3)
    while game.get_winner() is None:
        game.show_board()
        curr_turn = game.turn.value
        row, col = game.make_move()
        print(f'\nPlayer {curr_turn} went in ({row},{col})\n')
    game.show_board()
    print(game.get_winner())
