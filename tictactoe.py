#!/usr/bin/env python3
from tictactoe.TicTacToe import TicTacToe
import argparse


def main():
    parser = argparse.ArgumentParser(description='Tic-Tac-Toe Game')
    parser.add_argument('-s', '--size', default=3, type=int,
                        help='Width & Height of the board')
    parser.add_argument('-f', '--first', default='player',
                        choices=['player', 'computer', 'random'],
                        help='Who makes first move')
    parser.add_argument('-m', '--multi', action='store_true',
                        help='Player vs Player')
    parser.add_argument('-b', '--bigger', action='count', default=0,
                        help='Display the board bigger')
    args = parser.parse_args()

    # Create an instance of TicTacToe
    cell_width = min(1 + 2 * (args.bigger), 5)
    game = TicTacToe(size=args.size,
                     first=args.first,
                     multi=args.multi,
                     cell_width=cell_width)

    # Display game info and begin getting moves
    game.show_game()
    while True:
        game.make_move()
        game.show_game()
        # Stop game if someone won or there's a tie
        if game.get_winner() is not None:
            break

    # Display who won
    win = game.get_winner()
    if (win == game.Turn.PLAYER.value or win == game.Turn.COMPUTER.value):
        print(f'Player {game.get_winner()} wins!')
    else:
        print("It's a tie. You both lose!")


if __name__ == '__main__':
    main()
