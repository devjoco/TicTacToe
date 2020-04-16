#!/usr/bin/env python3
from tictactoe.TicTacToe import TicTacToe
import argparse


def convertRowCol(row: int, col: int) -> str:
    return chr(row + 65) + str(col + 1)


def main():
    parser = argparse.ArgumentParser(description='Tic-Tac-Toe Game')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--computer', action='store_const', const='c',
                       help='Computer first')
    group.add_argument('-p', '--player', action='store_const', const='p',
                       help='Player first')
    group.add_argument('-r', '--random', action='store_const', const='r',
                       help='Randomly player or computer first')
    parser.add_argument('-m', '--multiplayer', action='store_true',
                        help='Player vs Player')
    parser.add_argument('-s', '--size', default=3, type=int,
                        help='Width & Height of the board')
    args = parser.parse_args()
    chosen_first = args.computer if args.computer else \
        args.random if args.random else \
        args.player if args.player else \
        'p'

    print('--Tic-Tac-Toe--'.center(26))
    game = TicTacToe(size=args.size, first=chosen_first)
    while game.get_winner() is None:
        game.show_board()
        curr_turn = game.turn.value
        row, col = game.make_move()
        print(f'\nPlayer {curr_turn} went in {convertRowCol(row, col)}\n')
    game.show_board()
    print(game.get_winner())


if __name__ == '__main__':
    main()
