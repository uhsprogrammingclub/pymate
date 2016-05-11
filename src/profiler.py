# encoding=utf8
'''
Created on May 10, 2016

@author: Nate
'''

import cProfile
import time
import movegenerator
import util


def averageGenerationTime(loops, FEN="r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"):
    start, count = time.time(), 0
    b = util.boardFromFEN(FEN)
    moves = [move for move in movegenerator.generatePseudoMoves(b) if b.isLegalMove(move)]
    count += len(moves)
    print "There are %d potential moves in this position. Running generation %d times." % (len(moves), loops)

    for _ in range(loops - 1):
        moves = [move for move in movegenerator.generatePseudoMoves(b) if b.isLegalMove(move)]
        count += len(moves)

    print "Completed profiling. Total of %d moves generated in %d seconds. \n" % (count, time.time() - start)


def main():
    averageGenerationTime(5000)

if __name__ == '__main__':
    print "Initializing..."
    movegenerator.initPresets()
    main()
    # cProfile.run('main()', sort='time')