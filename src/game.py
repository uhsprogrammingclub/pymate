# encoding=utf8
import util
import movegenerator
from board import Move
#import board


def takePlayerMove():
    print gameBoard
    pseudoMoves = movegenerator.generatePseudoMoves(gameBoard)
    print "Possible moves: ", pseudoMoves
    move = input("Enter the next move:")
    if move == "undo":
        gameBoard.takeMove()
    else:
        move = Move.fromUCI(move)
        if move in pseudoMoves:
            gameBoard.makeMove(move)
        else:
            print "Illegal move!"
    takePlayerMove()


movegenerator.initPresets()
gameBoard = util.boardFromFEN("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")
takePlayerMove()
