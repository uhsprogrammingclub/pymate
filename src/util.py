'''
Created on Mar 22, 2016

@author: Stiven
'''
import board
import util
from itertools import cycle


def rshift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n

setMask = [0] * 64
clearMask = [0] * 64


def boardToFEN(b):

    # Converting pieces
    FEN = ""
    adjEmpty = 0
    indeces = []
    for i in range(8):
        indeces.extend(range(56 - i * 8, 64 - i * 8))
    li = cycle(indeces)
    for index in [next(li) for _ in xrange(64)]:
        piece = util.getPieceAtIndex(b, index)
        if piece is not None:
            FEN += str(adjEmpty) if adjEmpty > 0 else ""
            adjEmpty = 0
            FEN += piece
        else:
            adjEmpty += 1
        if index % 8 == 7:
            FEN += str(adjEmpty) if adjEmpty > 0 else ""
            adjEmpty = 0
            FEN += "/" if index != 7 else ""
    FEN += " w " if b.sideToMove == board.Side.W else " b "

    # Castle rights
    castling = [board.WKCA, board.WQCA, board.BKCA, board.BQCA]
    castleReference = {board.WKCA: 'K', board.WQCA: 'Q', board.BKCA: 'k', board.BQCA: 'q'}
    for kind in castling:
        FEN += castleReference[kind] if (b.castleRights & kind) != 0 else ""
    FEN += "-" if b.castleRights == 0 else ""

    # Move counters
    FEN += " %s " % b.EPTarget if b.EPTarget is not None else " - "
    FEN += "%d %d" % (b.halfMoveClock, b.fullMoveCounter)

    return FEN


def boardFromFEN(FEN):
    newBoard = board.Board()
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
                index = asIndex((x, y))
                bit = asBit(index)
                newBoard.pieceList[index] = piece
                piece = piece.lower()
                pieceBoardMap = {'p': board.PAWNS, 'n': board.KNIGHTS, 'b': board.BISHOPS,
                                 'r': board.ROOKS, 'q': board.QUEENS, 'k': board.KINGS}
                newBoard.pieceBitBoards[pieceBoardMap[piece]] |= bit
                if pieceIsUpperCase:
                    newBoard.pieceBitBoards[board.WHITE] |= bit
                else:
                    newBoard.pieceBitBoards[board.BLACK] |= bit
                x += 1
        y -= 1

    newBoard.sideToMove = board.Side.W if sideToMove == "w" else board.Side.B
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
    if type(coord) is int:
        return setMask[coord]
    elif type(coord) == tuple:
        return asBit(asIndex(coord))
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
    return rshift(bb, num * 8)


def right(bb, num=1):
    if num == 0:
        return bb
    mask = 0
    for i in range(num):
        mask |= board.FILE_BB[i]
    return bb << num & ~mask & board.FULL_BOARD


def left(bb, num=1):
    if num == 0:
        return bb
    mask = 0
    for i in range(num):
        mask |= board.FILE_BB[7 - i]
    return rshift(bb, num) & ~mask


def upRight(bb):
    return up(right(bb))


def upLeft(bb):
    return up(left(bb))


def downRight(bb):
    return down(right(bb))


def downLeft(bb):
    return down(left(bb))


def getPieceAtIndex(gameBoard, index):
    index = asIndex(index)
    return gameBoard.pieceList[index]
    '''bit = asBit(index)
    if (gameBoard.pieceBitBoards[board.WHITE] | gameBoard.pieceBitBoards[board.BLACK]) & bit != 0:
        for bbIndex in range(board.PAWNS, 8):
            if gameBoard.pieceBitBoards[bbIndex] & bit != 0:
                piece = board.pieceStringMap[bbIndex]
                return piece.upper() if gameBoard.pieceBitBoards[board.WHITE] & bit != 0 else piece
    return None
    '''
    """
    bit = asBit(index)
    piece = None
    if gameBoard.pieceBitBoards[board.WHITE] & bit != 0 or gameBoard.pieceBitBoards[board.BLACK] & bit != 0:
        for bbIndex in range(board.PAWNS, 8):
            if gameBoard.pieceBitBoards[bbIndex] & bit != 0:
                piece = board.pieceStringMap[bbIndex]
        if gameBoard.pieceBitBoards[board.WHITE] & bit != 0:
            piece = piece.upper()
    return piece
    """


def clearBit(bb, index):
    """
    Clears the bit at a given index in a passed bit board
    """
    bb &= clearMask[index]
    return bb


def lastSetBit(x):
    """
    Find the last set bit in a binary value
    """
    return (x & -x).bit_length() - 1


def getSetBits(bb):
    """
    Returns a list of the indexes of the set bits in the passed bit board
    """
    setBits = []
    while bb != 0:
        index = lastSetBit(bb)
        setBits.append(index)
        bb = clearBit(bb, index)
    return setBits


def countSetBits(bb):
    s = 0
    while bb != 0:
        bb &= (bb - 1)
        s += 1
    return s


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
