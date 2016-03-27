'''
Created on Mar 22, 2016

@author: Stiven
'''


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

WKCA, WQCA, BKCA, BQCA = 1, 2, 4, 8

class Side:
    W, B, NONE, BOTH = range(4)

class Board:
    def __init__(self):
        self.pieceBitBoards = []
        self.castleRights = 0
        self.WCastled = False
        self.BCastled = False
        self.EPTarget = None
        self.halfMoveClock = 0
        self.fullMoveCounter = 0
        self.sideToMove = Side.NONE
