import unittest
from BewareOfMatchBoxes import Model
from BewareOfMatchBoxes import Game
from BewareOfMatchBoxes import train

class TestMenace(unittest.TestCase):

    # Test that X wins
    def test_getWinner_1(self):
        g = Game()
        g.move(1)
        g.move(2)
        g.move(4)
        g.move(3)
        g.move(7)
        self.assertTrue(g.isGameOver())
        self.assertEqual(g.getWinner(), "X")

    # Test that O wins
    def test_getWinner_2(self):
        g = Game()
        g.move(1)
        g.move(2)
        g.move(3)
        g.move(5)
        g.move(4)
        g.move(8)
        self.assertTrue(g.isGameOver())
        self.assertEqual(g.getWinner(), "O")
    
    # Test that diagonal win is possible
    def testDiagonalWin(self):
        g = Game()
        g.move(1)
        g.move(2)
        g.move(5)
        g.move(3)
        g.move(9)
        self.assertTrue(g.isGameOver())
        self.assertEqual(g.getWinner(), 'X')
    
    # Test that game ends in a draw
    def testDraw(self):
        g = Game()
        g.move(1)
        g.move(2)
        g.move(3)
        g.move(5)
        g.move(4)
        g.move(7)
        g.move(6)
        g.move(9)
        g.move(8)
        self.assertTrue(g.isGameOver())
        self.assertEqual(g.getWinner(), 'Draw')
    
    # Test if model is trained 100 times
    def modelTrainCount(self):
        m = Model(100, 2, -1, 1)
        train(m, 100)
        self.assertEqual(100, m.trainLoses + m.trainDraws + m.trainWins)
    

    def highlyTrainedModelWinsOften(self):
        m1 = Model(100, 2, -1, 1)
        m2 = Model(100, 2, -1, 1)
        train(m1, 100)
        train(m2, 10000)
        winLossRatio1 = m1.trainWins / m1.trainLoses
        winLossRatio2 = m2.trainWins / m2.trainLoses
        print(winLossRatio1, winLossRatio2)
        self.assertTrue(winLossRatio1 < winLossRatio2)



unittest.main()
