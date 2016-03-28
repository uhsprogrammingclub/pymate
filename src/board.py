# encoding=utf8
'''
Created on Mar 22, 2016

@author: Stiven
'''
import util

setMask = []
clearMask = []
kingAttacks = []
knightAttacks = []

RANK_1 = 0x00000000000000FF
RANK_8 = 0xFF00000000000000
FILE_A = 0x0101010101010101
FILE_H = 0x8080808080808080
LEFT_HALF = 0xF0F0F0F0F0F0F0F0

WHITE, BLACK, PAWNS, KNIGHTS, BISHOPS, ROOKS, QUEENS, KINGS = 0, 1, 2, 3, 4, 5, 6, 7
pieceStringMap = {PAWNS: 'p', KNIGHTS: 'n', BISHOPS: 'b', ROOKS: 'r', QUEENS: 'q', KINGS: 'k'}
pieceBoardMap = {'p': PAWNS, 'n': KNIGHTS, 'b': BISHOPS, 'r': ROOKS, 'q': QUEENS, 'k': KINGS}

WKCA, WQCA, BKCA, BQCA = 1, 2, 4, 8

UNICODE_PIECES = {'r': u'♜', 'n': u'♞', 'b': u'♝', 'q': u'♛', 'k': u'♚', 'p': u'♟', 'R': u'♖', 'N': u'♘', 'B': u'♗', 'Q': u'♕', 'K': u'♔', 'P': u'♙', None: u'⌧'}


class Side:
    W, B, NONE, BOTH = range(4)


class Board:
    def __init__(self):
        self.pieceBitBoards = [0] * 8
        self.castleRights = 0
        self.WCastled = False
        self.BCastled = False
        self.EPTarget = None
        self.halfMoveClock = 0
        self.fullMoveCounter = 0
        self.sideToMove = Side.NONE

    def __str__(self):
        pieceList = self.asList()
        string = ''
        for i in reversed(range(64)):
            string += "|" + UNICODE_PIECES[pieceList[i]]
            if i % 8 == 0:
                string += "|\n"
        return string.encode('utf-8')

    def asList(self):
        pieceList = [None] * 64
        for i in range(64):
            bit = util.indexToBit(i)
            if self.pieceBitBoards[WHITE] & bit != 0 or self.pieceBitBoards[BLACK] & bit != 0:
                for piece in range(PAWNS, 8):
                    if self.pieceBitBoards[piece] & bit != 0:
                        pieceList[i] = pieceStringMap[piece]
                if self.pieceBitBoards[WHITE] & bit != 0:
                    pieceList[i] = pieceList[i].upper()
        return pieceList
