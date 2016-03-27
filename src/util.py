'''
Created on Mar 22, 2016

@author: Stiven
'''
import board
from board import Board
from board import Side

def boardFromFEN(FEN):
    newBoard = Board()
    subFEN = FEN.split(" ")
    piecesByRow = subFEN[0].split("/")
    sideToMove = subFEN[1]
    castlingRights = subFEN[2]
    enPassantTarget = subFEN[3]
    halfMoveClock = int(subFEN[4])
    fullMoveCounter = int(subFEN[5])

    y = 7
    for row in piecesByRow:
        x = 0

        for piece in row:
            if piece.isdigit():
                x += int(piece)
            else:
                pieceIsUpperCase = piece != piece.lower()
                piece = piece.lower()
                if piece == 'p':
                    newBoard.pieceBitBoards[board.PAWNS] |= coordToBit((x, y))
                elif piece == 'n':
                    newBoard.pieceBitBoards[board.KNIGHTS] |= coordToBit((x, y))
                elif piece == 'b':
                    newBoard.pieceBitBoards[board.BISHOPS] |= coordToBit((x, y))
                elif piece == 'r':
                    newBoard.pieceBitBoards[board.ROOKS] |= coordToBit((x, y))
                elif piece == 'k':
                    newBoard.pieceBitBoards[board.KINGS] |= coordToBit((x, y))
                elif piece == 'q':
                    newBoard.pieceBitBoards[board.QUEENS] |= coordToBit((x, y))
                if pieceIsUpperCase:
                    newBoard.pieceBitBoards[board.WHITE] |= coordToBit((x, y))
                else:
                    newBoard.pieceBitBoards[board.BLACK] |= coordToBit((x, y))
                x += 1
        y -= 1

    newBoard.sideToMove = Side.W if sideToMove == "w" else Side.B
    for c in castlingRights:
        if c == 'K':
            castlingRights |= board.WKCA
        elif c == "Q":
            castlingRights |= board.WQCA
        elif c == "k":
            castlingRights |= board.BKCA
        elif c == "q":
            castlingRights |= board.BQCA
    newBoard.EPTarget = stringToCoord(enPassantTarget)
    newBoard.halfMoveClock = halfMoveClock
    newBoard.fullMoveCounter = fullMoveCounter
    return newBoard

def indexToBit(index):
    bit = 1 << index
    return bit

def coordToIndex(coord):
    index = coord[1]*8+coord[0]
    return index

def coordToBit(coord):
    return indexToBit(coordToIndex(coord))

def stringToCoord(loc):
    if len(loc) != 2:
        return None
    x = ord(loc[0].upper()) - 65
    y = int(loc[1]) - 1
    return (x, y)
