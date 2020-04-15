#!/usr/bin/env python3
import unittest
from tictactoe.TicTacToe import TicTacToe as TTT

class Test_Default_Game(unittest.TestCase):
    def setUp(self):
        self.game = TTT()

    def test_player_choice(self):
        self.assertEqual(self.game.turn.value, 'X')

    def test_default_size_3(self):
        self.assertEqual(self.game.size, 3)

    def test_advance_turn(self):
        self.assertEqual(self.game.turn.value, 'X')
        self.game._advanceTurn()
        self.assertEqual(self.game.turn.value, 'O')

    def tearDown(self):
        del self.game

class Test_Custom_Game(unittest.TestCase):
    def setUp(self):
        self.game = TTT(5, 'c')

    def test_player_choice(self):
        self.assertEqual(self.game.turn.value, 'O')

    def test_custom_game_size(self):
        self.assertEqual(self.game.size, 5)

    def test_advance_turn(self):
        self.assertEqual(self.game.turn.value, 'O')
        self.game._advanceTurn()
        self.assertEqual(self.game.turn.value, 'X')

    def tearDown(self):
        del self.game

if __name__ == '__main__':
    unittest.main()
