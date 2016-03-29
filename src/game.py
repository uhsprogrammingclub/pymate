# encoding=utf8
import util
from board import Move
import board


def takePlayerMove():
    print gameBoard
    move = input("Enter the next move:")
    move = Move.fromUCI(move)
    print move.uci()
    gameBoard.makeMove(move)
    takePlayerMove()


board.initPresets()
gameBoard = util.boardFromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
takePlayerMove()
