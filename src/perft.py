'''
Created on May 9, 2016

@author: nathanielcorley
'''

import cProfile
import unittest
import movegenerator
import util
import board
import time

maxDepth = 6
legalityChecker = "normal"
#legalityChecker = "lazy"
perftStart = 1
divideFEN = None
#divideFEN = "rnb1kbnr/pp1ppppp/8/q1p5/8/3P4/PPPKPPPP/RNBQ1BNR w KQkq - 0 1"


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Initialize all arrays and bit boards necessary
        movegenerator.initPresets()
        self.leafNodes = 0
        self.TEST_LIMIT = 10000

    def testPERFT(self):
        tStart = time.time()
        filePath = "../tests/perfttests"
        with open(filePath, "r") as ins:
            tests = []
            for line in ins:
                tests.append(line)
        tests = tests[(perftStart - 1):]
        testNum = perftStart - 1
        if divideFEN is not None:
            b = util.boardFromFEN(divideFEN)
            isLegal = b.isLegalMove
            if legalityChecker == "lazy":
                isLegal = b.lazyIsLegalMove
            iStart = time.time()
            print b
            print "Divide at depth", maxDepth
            self.leafNodes = 0
            moves = [move for move in movegenerator.generatePseudoMoves(b) if isLegal(move)]
            moveNum = 0
            for move in moves:
                moveNum += 1
                oldNodes = self.leafNodes
                b.makeMove(move)
                self.perftTest(b, maxDepth - 1)
                b.takeMove()
                print "Move:", moveNum, move, self.leafNodes - oldNodes

            print "Leaf nodes: %d" % (self.leafNodes), "Finished in %f seconds." % ((time.time() - iStart))
        else:
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

                # b = util.boardFromFEN("rnbqkbnr/pp1ppppp/8/2p5/8/3P4/PPPKPPPP/RNBQ1BNR b KQkq - 0 1")
                b = util.boardFromFEN(FEN)

                isLegal = b.isLegalMove
                if legalityChecker == "lazy":
                    isLegal = b.lazyIsLegalMove

                print "\n### Running Test #%d ###\n" % testNum

                for i in range(1, len(depths) + 1):
                    if i > maxDepth:
                        break
                    # i = 2
                    iStart = time.time()
                    print b
                    print "Starting Test To Depth:", i
                    self.leafNodes = 0
                    moves = [move for move in movegenerator.generatePseudoMoves(b) if isLegal(move)]
                    moveNum = 0
                    for move in moves:
                        moveNum += 1
                        oldNodes = self.leafNodes
                        b.makeMove(move)
                        self.perftTest(b, i - 1)
                        b.takeMove()
                        print "Move:", moveNum, move, self.leafNodes - oldNodes

                    print "Leaf nodes: %d, expected: %s" % (self.leafNodes, depths[i - 1]), "Finished in %f seconds." % ((time.time() - iStart))
                    self.assertEqual(int(depths[i - 1]), self.leafNodes, "Depth %d : %s" % (i, FEN))

        c = time.time() - tStart
        print "PERFT test finished successfully in %d minutes" % c / 60

    def perftTest(self, b, depth):

        if depth == 0:
            self.leafNodes += 1
            return

        isLegal = b.isLegalMove
        if legalityChecker == "lazy":
            isLegal = b.lazyIsLegalMove

        moves = [move for move in movegenerator.generatePseudoMoves(b) if isLegal(move)]

        for move in moves:
            b.makeMove(move)
            self.perftTest(b, depth - 1)
            b.takeMove()

if __name__ == '__main__':
    # cProfile.run('unittest.main()')
    unittest.main()
