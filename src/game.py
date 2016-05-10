# encoding=utf8
import util
import movegenerator
from board import Move


def takePlayerMove():
    print gameBoard
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
gameBoard = util.boardFromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
takePlayerMove()
