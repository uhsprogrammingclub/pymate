'''
Created on Mar 29, 2016

@author: Nate
'''
from board import *
from util import *

kingAttacks = [0] * 64
knightAttacks = [0] * 64


def generatePseudoMoves(state):
    """
    Takes input of a board object and returns a list of potential moves
    """
    moves = []
    side = state.pieceBitBoards[WHITE] if state.sideToMove == Side.W else state.pieceBitBoards[BLACK]

    # King Moves
    kingIndex = lastSetBit(side & state.pieceBitBoards[KINGS])
    kingMoves = getSetBits(kingAttacks[kingIndex] & ~side)
    kingMoves = map(lambda x: (asCoord(kingIndex), asCoord(x)), kingMoves)
    moves.extend(map(lambda x: Move(fromSqr=x[0], toSqr=x[1]), kingMoves))

    # Knight Moves
    knightSquares = getSetBits(side & state.pieceBitBoards[KNIGHTS])

    for index in knightSquares:
        knightMoves = getSetBits(knightAttacks[index] & ~side)
        knightMoves = map(lambda x: (asCoord(index), asCoord(x)), knightMoves)
        moves.extend(map(lambda x: Move(fromSqr=x[0], toSqr=x[1]), knightMoves))

    # Pawn Moves
    pawnSquares = getSetBits(side & state.pieceBitBoards[PAWNS])
    for index in pawnSquares:
        pawnMoves = getSetBits(pawnPush(asBit(index), state))
        pawnMoves.extend(getSetBits(pawnAttack(asBit(index), state)))
        pawnMoves = map(lambda x: (asCoord(index), asCoord(x)), pawnMoves)
        for x in pawnMoves:
            if x[1][1] != 0 and x[1][1] != 7:
                moves.append(Move(fromSqr=x[0], toSqr=x[1]))
            else:
                moves.append(Move(fromSqr=x[0], toSqr=x[1], promotion='q'))
                moves.append(Move(fromSqr=x[0], toSqr=x[1], promotion='n'))
                moves.append(Move(fromSqr=x[0], toSqr=x[1], promotion='r'))
                moves.append(Move(fromSqr=x[0], toSqr=x[1], promotion='b'))

    return moves


def pawnPush(bb, state):
    moves = 0
    action = up if state.sideToMove == Side.W else down
    rank4 = action(RANK_1, 3) if state.sideToMove == Side.W else action(RANK_8, 3)
    pawns = action(bb) & ~state.allPieces()
    moves |= pawns
    pawns = action(pawns)
    moves |= pawns & ~state.allPieces() & rank4  # only add double push moves if the destination is on rank 4

    return moves


def pawnAttack(bb, state):
    rightAttack = 0
    leftAttack = 0
    EPTarget = 0
    if state.EPTarget is not None:
        EPTarget = asBit(state.EPTarget)
    if (state.sideToMove == Side.W):
        enemy = state.pieceBitBoards[BLACK]
        rightAttack = upRight(bb)
        leftAttack = upLeft(bb)
        EPTarget = up(EPTarget)
    else:
        enemy = state.pieceBitBoards[WHITE]
        rightAttack = downRight(bb)
        leftAttack = downLeft(bb)
        EPTarget = down(EPTarget)
    enemy |= EPTarget

    return (rightAttack | leftAttack) & enemy


def initPresets():
    """
    Loads initial presets
    """
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

if __name__ == '__main__':
    pass
