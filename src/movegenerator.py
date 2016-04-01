'''
Created on Mar 29, 2016

@author: Nate
'''
from board import *
from util import *

kingAttacks = [0] * 64
knightAttacks = [0] * 64


def generatePsuedoMoves(state):
    """
    Takes input of a board object and returns a list of potential moves
    """
    moves = []
    side = state.pieceBitBoards[WHITE] if state.sideToMove == Side.W else state.pieceBitBoards[BLACK]

    # King Moves
    kingSquare = asCoord(kingAttacks[side & state.pieceBitBoards[KINGS]])
    kingMoves = getSetBits(kingAttacks[side & state.pieceBitBoards[KINGS]] & ~side)
    filter(lambda x: (kingSquare, asCoord(x)), kingMoves)
    moves.extend(kingMoves)

    # Knight Moves
    knightSquares = getSetBits(side & state.pieceBitBoards[KNIGHTS])

    for index in knightSquares:
        knightMoves = getSetBits(knightAttacks[index] & ~side)
        filter(lambda x: (asCoord(index), asCoord(x)), knightMoves)
        moves.extend(knightMoves)


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
