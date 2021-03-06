# encoding=utf8
'''
Created on Mar 22, 2016

@author: Nate and Stiven
'''
import util
import movegenerator


RANK_BB = [0x00000000000000FF, 0x000000000000FF00, 0x0000000000FF0000, 0x00000000FF000000, 0x000000FF00000000, 0x0000FF0000000000, 0x00FF000000000000, 0xFF00000000000000]
FULL_BOARD = 0xFFFFFFFFFFFFFFFF
FILE_BB = [0x0101010101010101, 0x0202020202020202, 0x0404040404040404, 0x0808080808080808, 0x1010101010101010, 0x2020202020202020, 0x4040404040404040, 0x8080808080808080]
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
        self.pieceList = [None] * 64
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
        return self.pieceList

    def getPieceAtIndex(self, index):
        index = util.asIndex(index)
        return self.pieceList[index]

    def makeMove(self, move):
        undo = Undo(move=move, board=self)
        self.history.append(undo)
        self.halfMoveClock += 1
        move.movingPiece = self.getPieceAtIndex(move.fromSqr)
        move.capturedPiece = self.getPieceAtIndex(move.toSqr)
        self.movePiece(move.fromSqr, move.toSqr)
        if move.promotion is not None:
            if self.sideToMove == Side.W:
                self.addPiece(move.promotion.upper(), move.toSqr)
            else:
                self.addPiece(move.promotion, move.toSqr)

        if move.capturedPiece is not None:
            self.halfMoveClock = 0

        if move.movingPiece.lower() == "p":
            self.halfMoveClock = 0
            # Handle en passant
            if move.fromSqr[0] != move.toSqr[0] and move.capturedPiece is None:
                self.clearSquare(self.EPTarget)
                move.EPMove = True
            if abs(move.fromSqr[1] - move.toSqr[1]) > 1:
                self.EPTarget = move.toSqr
            else:
                self.EPTarget = None
        else:
            self.EPTarget = None

        # handle castling
        if move.movingPiece.lower() == "k":
            self.castleRights &= ~(WKCA | WQCA) if self.sideToMove == WHITE else ~(BKCA | BQCA)
            for y in [0, 7]:
                if move.fromSqr == (4, y):
                    if move.toSqr == (6, y):
                        self.movePiece((7, y), (5, y))
                        move.castling = True
                    elif move.toSqr == (2, y):
                        self.movePiece((0, y), (3, y))
                        move.castling = True

        if move.movingPiece == "R":
            if move.fromSqr == (0, 0):
                self.castleRights &= ~WQCA
            elif move.fromSqr == (7, 0):
                self.castleRights &= ~WKCA
        elif move.movingPiece == "r":
            if move.fromSqr == (0, 7):
                self.castleRights &= ~BQCA
            elif move.fromSqr == (7, 7):
                self.castleRights &= ~BKCA

        if move.capturedPiece == "R":
            if move.toSqr == (0, 0):
                self.castleRights &= ~WQCA
            elif move.toSqr == (7, 0):
                self.castleRights &= ~WKCA
        elif move.capturedPiece == "r":
            if move.toSqr == (0, 7):
                self.castleRights &= ~BQCA
            elif move.toSqr == (7, 7):
                self.castleRights &= ~BKCA

        self.sideToMove = Side.other(self.sideToMove)

    def takeMove(self):
        if len(self.history) == 0:
            return
        undo = self.history.pop()
        move = undo.move
        self.halfMoveClock = undo.halfMoveClock
        self.EPTarget = undo.EPTarget
        self.castleRights = undo.castleRights
        self.sideToMove = Side.other(self.sideToMove)

        self.movePiece(move.toSqr, move.fromSqr)

        if move.promotion is not None:
            if self.sideToMove == Side.W:
                self.addPiece("P", move.fromSqr)
            else:
                self.addPiece("p", move.fromSqr)
        if move.capturedPiece is not None:
            self.addPiece(move.capturedPiece, move.toSqr)
        if move.EPMove:
            if self.sideToMove == Side.W:
                self.addPiece("p", self.EPTarget)
            else:
                self.addPiece("P", self.EPTarget)
        if move.castling:
            for y in [0, 7]:
                if move.fromSqr == (4, y):
                    if move.toSqr == (6, y):
                        self.movePiece((5, y), (7, y))
                    elif move.toSqr == (2, y):
                        self.movePiece((3, y), (0, y))

    def clearSquare(self, coord):
        coord = util.asIndex(coord)
        piece = self.getPieceAtIndex(coord)
        if piece is not None:
            pieceLower = piece.lower()
            self.pieceBitBoards[pieceBoardMap[pieceLower]] = util.clearBit(self.pieceBitBoards[pieceBoardMap[pieceLower]], coord)
            if piece == pieceLower:
                self.pieceBitBoards[BLACK] = util.clearBit(self.pieceBitBoards[BLACK], coord)
            else:
                self.pieceBitBoards[WHITE] = util.clearBit(self.pieceBitBoards[WHITE], coord)
            self.pieceList[coord] = None

    def addPiece(self, piece, coord):
        bit = util.asBit(coord)
        self.clearSquare(coord)
        pieceLower = piece.lower()
        self.pieceBitBoards[pieceBoardMap[pieceLower]] |= bit
        if pieceLower == piece:
            self.pieceBitBoards[BLACK] |= bit
        else:
            self.pieceBitBoards[WHITE] |= bit
        self.pieceList[util.asIndex(coord)] = piece

    def movePiece(self, coordFrom, coordTo):
        coordFrom = util.asIndex(coordFrom)
        coordTo = util.asIndex(coordTo)

        piece = self.getPieceAtIndex(coordFrom)
        self.clearSquare(coordFrom)
        self.addPiece(piece, coordTo)

    def allPieces(self):
        return self.pieceBitBoards[WHITE] | self.pieceBitBoards[BLACK]

    def kingPos(self, side):
        friendlyBB = self.pieceBitBoards[WHITE] if side == Side.W else self.pieceBitBoards[BLACK]
        return util.lastSetBit(friendlyBB & self.pieceBitBoards[KINGS])

    def canCastle(self, side, kSide):
        if self.isInCheck(side):
            return False

        allBB = self.allPieces()

        if side == Side.W and (self.castleRights & WKCA) != 0 and kSide:
            if (allBB & 0x60) != 0 or movegenerator.attacksTo(5, self, side) != 0 or movegenerator.attacksTo(6, self, side) != 0:
                return False
            return True
        elif side == Side.B and (self.castleRights & BKCA) != 0 and kSide:
            if (allBB & 0x6000000000000000) != 0 or movegenerator.attacksTo(61, self, side) != 0 or movegenerator.attacksTo(62, self, side) != 0:
                return False
            return True
        elif side == Side.W and (self.castleRights & WQCA) != 0 and not kSide:
            if (allBB & 0xE) != 0 or movegenerator.attacksTo(3, self, side) != 0 or movegenerator.attacksTo(2, self, side) != 0:
                return False
            return True
        elif side == Side.B and (self.castleRights & BQCA) != 0 and not kSide:
            if (allBB & 0xE00000000000000) != 0 or movegenerator.attacksTo(59, self, side) != 0 or movegenerator.attacksTo(58, self, side) != 0:
                return False
            return True

    def isInCheck(self, side):
        if movegenerator.attacksTo(self.kingPos(side), self, side) == 0:
            return False
        else:
            return True

    def isPositionLegal(self):
        if self.isInCheck(Side.other(self.sideToMove)):
            return False
        else:
            return True

    def lazyIsLegalMove(self, move):
        sideToMove = self.sideToMove
        self.makeMove(move)
        inCheck = self.isInCheck(sideToMove)
        self.takeMove()
        if inCheck:
            return False
        else:
            return True

    # def isLegalMove(self, move):
    #     sideToMove = self.sideToMove
    #     fromPos = util.asIndex(move.fromSqr)
    #     toPos = util.asIndex(move.toSqr)
    #     kingPos = self.kingPos(sideToMove)

    # if the king is moving check if the to square is under attack
    #     if fromPos == kingPos:
    #         if movegenerator.attacksTo(toPos, self, sideToMove, self.allPieces() ^ util.asBit(kingPos)) == 0:
    #             return True
    #         else:
    #             return False

    #     else:

    #         if self.isInCheck(sideToMove):

    # If double check, only the king can move
    #             attacksToKing = movegenerator.attacksTo(kingPos, self, sideToMove)
    #             if util.countSetBits(attacksToKing) > 1:
    #                 return False
    #             attackingPos = util.lastSetBit(attacksToKing)

    # If its a capture move and the capturing piece is not absolutely pinned, move is legal
    #             if attackingPos == toPos and not self.isAbsolutePin(fromPos, sideToMove):
    #                 return True

    # if a knight is attacking, then king has to move
    #             if self.pieceBitBoards[KNIGHTS] & util.asBit(attackingPos) != 0:
    #                 return False

    # try the move to see if the move will block the check
    #             self.makeMove(move)
    #             inCheck = self.isInCheck(sideToMove)
    #             self.takeMove()
    #             if inCheck:
    #                 return False
    #             else:
    #                 return True

    #         else:
    # check that the moving piece is not absolutely pinned
    #             if not self.isAbsolutePin(fromPos, sideToMove):
    #                 EPMove = False
    #                 if util.getPieceAtIndex(self, move.fromSqr).lower() == "p":
    #                     if move.fromSqr[0] != move.toSqr[0] and util.getPieceAtIndex(self, move.toSqr) is None:
    #                         EPMove = True
    #                 if EPMove is False:
    #                     return True

    # if piece is pinned, try the move and see if it results in the king being in check
    #             self.makeMove(move)
    #             inCheck = self.isInCheck(sideToMove)
    #             self.takeMove()
    #             if inCheck:
    #                 return False
    #             else:
    #                 return True

    def isAbsolutePin(self, pinnedPiece, side):
        pinnedPiece = util.asIndex(pinnedPiece)
        numOfAttacksWithPin = util.countSetBits(movegenerator.attacksTo(self.kingPos(side), self, side))
        bbWithoutPin = self.allPieces() & ~util.asBit(pinnedPiece)
        numOfAttacksWithoutPin = util.countSetBits(movegenerator.attacksTo(self.kingPos(side), self, side, bbWithoutPin))
        if numOfAttacksWithPin < numOfAttacksWithoutPin:
            return True
        else:
            return False


class Undo:
    def __init__(self, move=None, castleRights=None, EPTarget=None, halfMoveClock=None, board=None):
        self.move = move
        if board is None:
            self.castleRights = castleRights
            self.EPTarget = EPTarget
            self.halfMoveClock = halfMoveClock
        else:
            self.castleRights = board.castleRights
            self.EPTarget = board.EPTarget
            self.halfMoveClock = board.halfMoveClock


class Move:
    def __init__(self, fromSqr=(0, 0), toSqr=(0, 0), promotion=None):
        self.toSqr = tuple(toSqr)
        self.fromSqr = tuple(fromSqr)
        self.promotion = promotion
        if promotion is not None:
            self.promotion = promotion.lower()
        self.capturedPiece = None
        self.castling = False
        self.EPMove = False

    def uci(self):
        uci = util.asSANSqr(self.fromSqr) + util.asSANSqr(self.toSqr)
        if self.promotion is not None:
            uci += self.promotion
        return uci

    def __repr__(self):
        return self.uci()

    def __str__(self):
        return self.uci()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.fromSqr != other.fromSqr:
                return False
            elif self.toSqr != other.toSqr:
                return False
            elif self.promotion != other.promotion:
                return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

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
