'''
Created on May 9, 2016

@author: nathanielcorley
'''

import unittest
import movegenerator
import util
import board
from datetime import datetime


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Initialize all arrays and bit boards necessary
        movegenerator.initPresets()
        self.leafNodes = 0
        self.TEST_LIMIT = 10000

    def testPERFT(self):
        tStart = datetime.now()
        filePath = "../tests/perfttests"
        with open(filePath, "r") as ins:
            tests = []
            for line in ins:
                tests.append(line)

        testNum = 0
        for test in tests:
            testNum += 1
            if testNum > self.TEST_LIMIT: 
                break
            strSplit = test.split(";")

            # Map array to correct variables
            FEN = strSplit[0]

            depths = []
            for i in range(len(strSplit) - 1):
                depths.append(strSplit[i + 1][3:].replace("\n", ""))

            b = util.boardFromFEN(FEN)

            print "\n### Running Test #%d ###\n" % testNum

            for i in range(1, len(depths) + 1):
                print b
                print "Starting Test To Depth:", i
                self.leafNodes = 0
                moves = [move for move in movegenerator.generatePseudoMoves(b) if b.isLegalMove(move)]
                moveNum = 0
                for move in moves:
                    moveNum += 1
                    oldNodes = self.leafNodes
                    b.makeMove(move)
                    self.perftTest(b, i - 1)
                    b.takeMove()
                    print "Move:", moveNum, move, self.leafNodes - oldNodes

                print "Leaf nodes: %d, expected: %s" % (self.leafNodes, depths[i - 1])
                self.assertEqual(int(depths[i - 1]), self.leafNodes, "Depth %d : %s" % (i, FEN))

        c = tStart - datetime.now()
        print "PERFT test finished successfully in %d minutes" % c.minutes

    def perftTest(self, b, depth):

        if depth == 0:
            self.leafNodes += 1
            return

        moves = [move for move in movegenerator.generatePseudoMoves(b) if b.isLegalMove(move)]

        for move in moves:
            b.makeMove(move)
            self.perftTest(b, depth - 1)
            b.takeMove()

if __name__ == '__main__':
    unittest.main()
