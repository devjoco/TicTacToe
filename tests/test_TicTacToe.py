#!/usr/bin/env python3
import unittest
from tictactoe.TicTacToe import TicTacToe

class TestGame(unittest.TestCase):
    def test_player_choice(self):
        'Tests that user can choose who goes first when creating game'
        game = TicTacToe(3, 'p')
        self.assertEqual(game.turn.value, 'X')

if __name__ == '__main__':
    unittest.main()
