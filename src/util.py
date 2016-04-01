'''
Created on Mar 22, 2016

@author: Stiven
'''
import board
from board import Board
from board import Side

setMask = [0] * 64
clearMask = [0] * 64


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
                pieceBoardMap = {'p': board.PAWNS, 'n': board.KNIGHTS, 'b': board.BISHOPS,
                                 'r': board.ROOKS, 'q': board.QUEENS, 'k': board.KINGS}
                newBoard.pieceBitBoards[pieceBoardMap[piece]] |= asBit((x, y))
                if pieceIsUpperCase:
                    newBoard.pieceBitBoards[board.WHITE] |= asBit((x, y))
                else:
                    newBoard.pieceBitBoards[board.BLACK] |= asBit((x, y))
                x += 1
        y -= 1

    newBoard.sideToMove = Side.W if sideToMove == "w" else Side.B
    for c in castlingRights:
        if c == 'K':
            newBoard.castleRights |= board.WKCA
        elif c == "Q":
            newBoard.castleRights |= board.WQCA
        elif c == "k":
            newBoard.castleRights |= board.BKCA
        elif c == "q":
            newBoard.castleRights |= board.BQCA
    newBoard.EPTarget = asCoord(enPassantTarget)
    newBoard.halfMoveClock = halfMoveClock
    newBoard.fullMoveCounter = fullMoveCounter
    return newBoard


def asIndex(coord):
    if type(coord) is tuple:
        return coord[1] * 8 + coord[0]
    return coord


def asBit(coord):
    if type(coord) == tuple:
        return asBit(asIndex(coord))
    elif type(coord) is int:
        return setMask[coord]
    return coord


def asCoord(loc):
    if type(loc) is str:
        if len(loc) != 2:
            return None
        x = ord(loc[0].upper()) - 65
        y = int(loc[1]) - 1
        return (x, y)
    elif type(loc) is int:
        x = loc % 8
        y = (loc - x) / 8
        return (x, y)
    return loc


def asSANSqr(coord):
    coord = asCoord(coord)
    letter = chr(coord[0] + 65).lower()
    number = str(coord[1] + 1)
    return letter + number


def up(bb, num=1):
    return bb << 8 * num & board.FULL_BOARD


def down(bb, num=1):
    return bb >> 8 * num & board.FULL_BOARD


def right(bb, num=1):
    if num == 0:
        return bb
    return bb << num & ~(board.FILE_A | right(board.FILE_A, num - 1)) & board.FULL_BOARD


def left(bb, num=1):
    if num == 0:
        return bb
    return bb >> num & ~(board.FILE_H | left(board.FILE_H, num - 1)) & board.FULL_BOARD


def upRight(bb):
    return up(right(bb)) & board.FULL_BOARD


def upLeft(bb):
    return up(left(bb)) & board.FULL_BOARD


def downRight(bb):
    return down(right(bb)) & board.FULL_BOARD


def downLeft(bb):
    return down(left(bb)) & board.FULL_BOARD


def getPieceAtIndex(gameBoard, index):
    bit = asBit(index)
    piece = None
    if gameBoard.pieceBitBoards[board.WHITE] & bit != 0 or gameBoard.pieceBitBoards[board.BLACK] & bit != 0:
        for bbIndex in range(board.PAWNS, 8):
            if gameBoard.pieceBitBoards[bbIndex] & bit != 0:
                piece = board.pieceStringMap[bbIndex]
        if gameBoard.pieceBitBoards[board.WHITE] & bit != 0:
            piece = piece.upper()
    return piece


def clearBit(bb, index):
    """
    Clears the bit at a given index in a passed bit board
    """
    bb &= clearMask[index]
    return bb


def lsb(x):
    """
    Find the last set bit in a binary value
    """
    return (x & -x).bit_length() - 1


def ffs(bb):
    """
    Finds the next set bit in the passed bit board (name short for 'find first set')
    NOTE: Perhaps use gmpy library (4x faster)?
    """
    assert bb != 0

    i = 0
    while (bb % 2) == 0:
        i += 1
        bb = bb >> 1
    return i


def getSetBits(bb):
    """
    Returns a list of the indexes of the set bits in the passed bit board
    """
    setBits = []
    print bb
    print bbAsString(bb)
    while bb != 0:
        index = lsb(bb)
        print index
        setBits.append(index)
        bb = clearBit(bb, index)
    return setBits


def bbAsString(bb):
    string = ""
    for y in reversed(range(8)):
        for x in range(8):
            if bb & 1 << (x + y * 8) != 0:
                string += "X "
            else:
                string += "- "
        string += "\n"
    return string
