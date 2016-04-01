# encoding=utf8
import util
from board import Move
import board
import movegenerator


def takePlayerMove():
    print gameBoard
    pseudoMoves = movegenerator.generatePsuedoMoves(gameBoard)
    print pseudoMoves
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
gameBoard = util.boardFromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
takePlayerMove()
