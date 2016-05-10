'''
Created on May 9, 2016

@author: nathanielcorley
'''

import unittest
import movegenerator
import util
from datetime import datetime
import sys


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Initialize all arrays and bit boards necessary
        movegenerator.initPresets()
        self.leafNodes = 0
        self.TEST_LIMIT = 10000

    def testPERFT(self):
        tStart = datetime.now()
        filePath = "../tests/perftests"
        f = open(filePath)
        numLines = sum(1 for _ in f)
        tests = []

        for i in range(numLines):
            tests[i] = f.readline()

        file.close()
        
        print "CLOSING"
        sys.exit(0)

        testNum = 0
        for test in tests:
            testNum += 1
            if testNum > self.TEST_LIMIT: break
            strSplit = test.split(";")

            # Map array to correct variables
            FEN = strSplit[0]

            depths = []
            for i in range(len(strSplit) - 1):
                depths[i] = strSplit[i + 1][4:]

            b = util.boardFromFEN(FEN)

            print "\n### Running Test #%d ###\n" % testNum

            for i in range(1, len(depths) + 1):
                print b
                print "Starting Test To Depth:", i
                leafNodes = 0
                moves = movegenerator.generatePseudoMoves(b)
                moveNum = 0
                for move in moves:
                    moveNum += 1
                    oldNodes = leafNodes
                    b.makeMove(move)
                    self.perftTest(b, i - 1)
                    b.takeMove(move)
                    print "Move: %d %s &d" % (moveNum, move, (leafNodes - oldNodes))

                print "Leaf nodes: %d, expected:: %d" % (leafNodes, depths[i-1])
                self.assertTrue("Depth " + i + ": " + FEN, depths[i - 1], leafNodes)

        c = tStart - datetime.now()
        print "PERFT test finished successfully in %d minutes" % c.minutes

    def perftTest(self, b, depth):

        if depth == 0:
            self.leafNodes += 1
            return

        moves = movegenerator.generatePseudoMoves(b)

        for move in moves:
            b.makeMove(move)
            self.perftTest(b, depth - 1)
            b.takeMove(move)

if __name__ == '__main__':
    unittest.main()
