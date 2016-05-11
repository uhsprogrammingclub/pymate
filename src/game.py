# encoding=utf8
import util
import movegenerator
from board import Move


def takePlayerMove():
    print gameBoard
    print util.boardToFEN(gameBoard)
    pseudoMoves = movegenerator.generatePseudoMoves(gameBoard)
    print "Pseudo moves (" + str(len(pseudoMoves)) + "): ", pseudoMoves
    legalMoves = filter(lambda move: gameBoard.isLegalMove(move), pseudoMoves)
    print "Legal moves (" + str(len(legalMoves)) + "): ", legalMoves
    move = input("Enter the next move:")
    if move == "undo":
        gameBoard.takeMove()
    else:
        move = Move.fromUCI(move)
        if move in legalMoves:
            gameBoard.makeMove(move)
        else:
            print "Illegal move!"
    takePlayerMove()


movegenerator.initPresets()
gameBoard = util.boardFromFEN("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
takePlayerMove()
