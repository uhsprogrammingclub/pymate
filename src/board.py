# encoding=utf8
'''
Created on Mar 22, 2016

@author: Stiven
'''
import util

setMask = [0] * 64
clearMask = [0] * 64
kingAttacks = [0] * 64
knightAttacks = [0] * 64

RANK_1 = 0x00000000000000FF
RANK_8 = 0xFF00000000000000
FILE_A = 0x0101010101010101
FILE_H = 0x8080808080808080
LEFT_HALF = 0xF0F0F0F0F0F0F0F0

WHITE, BLACK, PAWNS, KNIGHTS, BISHOPS, ROOKS, QUEENS, KINGS = 0, 1, 2, 3, 4, 5, 6, 7
pieceStringMap = {WHITE: 'white', BLACK: 'black', PAWNS: 'p', KNIGHTS: 'n', BISHOPS: 'b', ROOKS: 'r', QUEENS: 'q', KINGS: 'k'}
pieceBoardMap = {'p': PAWNS, 'n': KNIGHTS, 'b': BISHOPS, 'r': ROOKS, 'q': QUEENS, 'k': KINGS}

WKCA, WQCA, BKCA, BQCA = 1, 2, 4, 8

UNICODE_PIECES = {'r': u'♜', 'n': u'♞', 'b': u'♝', 'q': u'♛', 'k': u'♚', 'p': u'♟', 'R': u'♖', 'N': u'♘', 'B': u'♗', 'Q': u'♕', 'K': u'♔', 'P': u'♙', None: u'⬚'}


class Side:
    W, B, NONE, BOTH = range(4)

    @staticmethod
    def other(side):
        if side == Side.W:
            return Side.B
        elif side == Side.B:
            return Side.W
        elif side == Side.NONE:
            return Side.BOTH
        else:
            return Side.NONE


class Board:
    def __init__(self):
        self.pieceBitBoards = [0] * 8
        self.castleRights = 0
        self.EPTarget = None
        self.halfMoveClock = 0
        self.fullMoveCounter = 0
        self.sideToMove = Side.NONE
        self.history = []

    def __str__(self):
        pieceList = self.asList()
        string = ''
        for y in reversed(range(8)):
            string += str(y + 1)
            for x in range(8):
                string += "|" + UNICODE_PIECES[pieceList[y * 8 + x]]
            string += "|\n"
        string += "  a b c d e f g h "
        return string.encode('utf-8')

    def asList(self):
        pieceList = [None] * 64
        for i in range(64):
            pieceList[i] = util.getPieceAtIndex(self, i)
        return pieceList

    def makeMove(self, move):
        move.capturedPiece = util.getPieceAtIndex(self, move.toSqr)
        self.movePiece(move.fromSqr, move.toSqr)
        if move.promotion is not None:
            if self.sideToMove == Side.W:
                self.addPiece(move.promotion.upper(), move.toSqr)
            else:
                self.addPiece(move.promotion, move.toSqr)

        self.sideToMove = Side.other(self.sideToMove)

    def clearSquare(self, coord):
        coord = util.asIndex(coord)
        for i in range(8):
            self.pieceBitBoards[i] &= clearMask[coord]

    def addPiece(self, piece, coord):
        bit = util.asBit(coord)
        self.clearSquare(coord)
        self.pieceBitBoards[pieceBoardMap[piece.lower()]] |= bit
        if piece.upper() == piece:
            self.pieceBitBoards[WHITE] |= bit
        else:
            self.pieceBitBoards[BLACK] |= bit

    def movePiece(self, coordFrom, coordTo):
        coordFrom = util.asIndex(coordFrom)
        coordTo = util.asIndex(coordTo)
        bitFrom = util.asBit(coordFrom)
        bitTo = util.asBit(coordTo)

        for i in range(8):
            self.pieceBitBoards[i] &= clearMask[coordTo]
            if self.pieceBitBoards[i] | bitFrom == self.pieceBitBoards[i]:
                print "Moving"
                self.pieceBitBoards[i] &= clearMask[coordFrom]
                self.pieceBitBoards[i] |= bitTo


class Undo:
    def __init__(self, move=None, castleRights=None, EPTarget=None, halfMoveClock=None, board=None):
        self.move = move
        if board is None:
            self.castleRights = castleRights
            self.EPTarget = tuple(EPTarget)
            self.halfMoveClock = halfMoveClock
        else:
            self.castleRights = board.castleRights
            self.EPTarget = tuple(board.EPTarget)
            self.halfMoveClock = board.halfMoveClock


class Move:
    def __init__(self, fromSqr=(0, 0), toSqr=(0, 0), promotion=None):
        self.toSqr = tuple(toSqr)
        self.fromSqr = tuple(fromSqr)
        self.promotion = promotion
        if promotion is not None:
            self.promotion = promotion.lower()
        self.capturedPiece = None

    def uci(self):
        uci = util.asSANSqr(self.fromSqr) + util.asSANSqr(self.toSqr)
        if self.promotion is not None:
            uci += self.promotion
        return uci

    @staticmethod
    def fromUCI(uci):
        if len(uci) != 4 and len(uci) != 5:
            return None
        fromSqr = util.asCoord(uci[0:2])
        toSqr = util.asCoord(uci[2:4])
        promotion = None
        if len(uci) == 5:
            promotion = uci[4]
        return Move(fromSqr=fromSqr, toSqr=toSqr, promotion=promotion)


def initPresets():
    for i in range(64):
        setMask[i] = 1 << i
        clearMask[i] = ~setMask[i]
        kingAttack = setMask[i] | util.right(setMask[i]) | util.left(setMask[i])
        kingAttack |= util.up(kingAttack) | util.down(kingAttack)
        kingAttacks[i] = kingAttack & clearMask[i]

        l1 = util.left(setMask[i])
        l2 = util.left(setMask[i], 2)
        r1 = util.right(setMask[i])
        r2 = util.right(setMask[i], 2)

        h1 = l2 | r2
        h2 = l1 | r1

        knightAttacks[i] = util.up(h1) | util.down(h1) | util.up(h2, 2) | util.down(h2, 2)
