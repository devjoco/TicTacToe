#!/usr/bin/env python3
from tictactoe.TicTacToe import TicTacToe
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description='Tic-Tac-Toe Game')
    parser.add_argument('-s', '--size', default=3, type=int,
                        help='Width & Height of the board')
    parser.add_argument('-f', '--first', default='player',
                        choices=['player', 'computer', 'random'],
                        help='Who makes first move')
    parser.add_argument('-m', '--multi', action='store_true',
                        help='Player vs Player')
    args = parser.parse_args()

    print('--Tic-Tac-Toe--'.center(26))
    game = TicTacToe(size=args.size, first=args.first, multi=args.multi)
    game.show_board()
    while True:
        game.make_player_move()
        game.show_board()
        if game.get_winner() is not None:
            break
        if not game.multi:
            print("Computer is thinking...")
            time.sleep(2.4)
            curr_turn = game.turn.value
            game.make_comp_move()
            row = game.last_move['row']
            col = game.last_move['col']
            chosen_spot = game.convert_row_col(row, col)
            game.show_board()
            print(f'Player {curr_turn} went in {chosen_spot}')
            if game.get_winner() is not None:
                break
    print(f'And the winner is.. {game.get_winner()}')


if __name__ == '__main__':
    main()
