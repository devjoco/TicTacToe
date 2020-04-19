#!/usr/bin/env python3
import unittest
from unittest import TestCase, mock, expectedFailure
from tictactoe.TicTacToe import TicTacToe as TTT


class Test_Utility_Funcs(TestCase):

    def test_convert__r0_c0(self):
        spot = TTT.convertRowCol(0, 0)
        self.assertEqual(spot, "A1")

    def test_convert_r0_c1(self):
        spot = TTT.convertRowCol(0, 1)
        self.assertEqual(spot, "B1")
        
    def test_convert_r0_c2(self):
        spot = TTT.convertRowCol(0, 2)
        self.assertEqual(spot, "C1")

    def test_convert_r1_c0(self):
        spot = TTT.convertRowCol(1, 0)
        self.assertEqual(spot, "A2")

    def test_convert_r1_c1(self):
        spot = TTT.convertRowCol(1, 1)
        self.assertEqual(spot, "B2")

    def test_convert_r1_c2(self):
        spot = TTT.convertRowCol(1, 2)
        self.assertEqual(spot, "C2")

    def test_convert_r2_c0(self):
        spot = TTT.convertRowCol(2, 0)
        self.assertEqual(spot, "A3")

    def test_convert_r2_c1(self):
        spot = TTT.convertRowCol(2, 1)
        self.assertEqual(spot, "B3")

    def test_convert_r2_c2(self):
        spot = TTT.convertRowCol(2, 2)
        self.assertEqual(spot, "C3")


class Test_Single_Player(TestCase):
    @mock.patch('tictactoe.TicTacToe.input', create=True)
    def test_comp_goes_after_player(self, mocked_input):
        mocked_input.side_effect = ['a1']
        self.game = TTT(size=3, first='p')
        self.game.make_move()
        self.assertEqual(self.game.turn, self.game.Turn.PLAYER)

    def tearDown(self):
        self.game = None


class Test_TTT_Parameters(TestCase):
    def test_game_size(self):
        for i in range(20):
            with self.subTest(i=i):
                self.game = TTT(size=i)
                self.assertEqual(self.game.size, i)

    def test_first_move(self):
        for c in 'pcr':
            with self.subTest(first=c):
                self.game = TTT(first=c)
                self.assertIn(self.game.turn, 
                              list(self.game.Turn.__members__.values()))


class Test_Default_Game(TestCase):
    def setUp(self):
        self.game = TTT()

    def test_player_choice(self):
        self.assertEqual(self.game.turn, self.game.Turn.PLAYER)

    def test_default_size_3(self):
        self.assertEqual(self.game.size, 3)

    def test_advance_turn(self):
        self.assertEqual(self.game.turn, self.game.Turn.PLAYER)
        self.game._advance_turn()
        self.assertEqual(self.game.turn, self.game.Turn.COMPUTER)

    def test_hori_wins(self):
        for row in range(self.game.size):
            self.game._reset_board()
            self.assertEqual(self.game.get_winner(), None)
            for col in range(self.game.size):
                self.game.board[row][col] = self.game.Turn.PLAYER.value
            self.assertEqual(self.game.get_winner(), self.game.Turn.PLAYER.value)

    def test_vert_wins(self):
        for col in range(self.game.size):
            self.game._reset_board()
            self.assertEqual(self.game.get_winner(), None)
            for row in range(self.game.size):
                self.game.board[row][col] = self.game.Turn.COMPUTER.value
            self.assertEqual(self.game.get_winner(), self.game.Turn.COMPUTER.value)

    def test_diag_tl_br_win(self):
        for row in range(self.game.size):
            self.assertEqual(self.game.get_winner(), None)
            for col in range(self.game.size):
                if row == col:
                    self.game.board[row][col] = self.game.Turn.PLAYER.value
        self.assertEqual(self.game.get_winner(), self.game.Turn.PLAYER.value)

    def test_diag_bl_tr_win(self):
        for row in range(self.game.size):
            self.assertEqual(self.game.get_winner(), None)
            for col in range(self.game.size):
                if row + col == self.game.size - 1:
                    self.game.board[row][col] = self.game.Turn.COMPUTER.value
        self.assertEqual(self.game.get_winner(), self.game.Turn.COMPUTER.value)

    def test_tie_game(self):
        symbs = (self.game.Turn.PLAYER.value, self.game.Turn.COMPUTER.value)
        for row in range(self.game.size - 1):
            for col in range(self.game.size):
                self.game.board[row][col] = symbs[col % 2]
        for col in range(self.game.size):
            self.game.board[-1][col] = symbs[(col + 1) % 2]
        self.assertEqual(self.game.get_winner(), 'T')

    def tearDown(self):
        del self.game


class Test_Custom_Game(TestCase):
    def setUp(self):
        self.game = TTT(5, 'c')

    def test_player_choice(self):
        self.assertEqual(self.game.turn, self.game.Turn.COMPUTER)

    def test_custom_game_size(self):
        self.assertEqual(self.game.size, 5)

    def test_advance_turn(self):
        self.assertEqual(self.game.turn, self.game.Turn.COMPUTER)
        self.game._advance_turn()
        self.assertEqual(self.game.turn, self.game.Turn.PLAYER)

    def tearDown(self):
        del self.game


if __name__ == '__main__':
    unittest.main()
