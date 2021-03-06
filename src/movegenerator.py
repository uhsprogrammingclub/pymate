'''
Created on Mar 29, 2016

@author: Nate
'''
import util
import board

# Logical Shift for bits


def rshift(val, n): 
    return val >> n if val >= 0 else (val + 0x100000000) >> n

kingAttacks = [0] * 64
knightAttacks = [0] * 64
pawnAttacks = [[0] * 64, [0] * 64]
LONG_MASK = 0xFFFFFFFFFFFFFFFF
INT_MASK = 0xFFFFFFFF
magicNumberRook = [
    0xa180022080400230, 0x40100040022000, 0x80088020001002, 0x80080280841000, 0x4200042010460008, 0x4800a0003040080, 0x400110082041008, 0x8000a041000880, 0x10138001a080c010, 0x804008200480, 0x10011012000c0, 0x22004128102200, 0x200081201200c, 0x202a001048460004, 0x81000100420004, 0x4000800380004500, 0x208002904001, 0x90004040026008, 0x208808010002001, 0x2002020020704940, 0x8048010008110005, 0x6820808004002200, 0xa80040008023011, 0xb1460000811044, 0x4204400080008ea0, 0xb002400180200184, 0x2020200080100380, 0x10080080100080, 0x2204080080800400, 0xa40080360080, 0x2040604002810b1, 0x8c218600004104, 0x8180004000402000, 0x488c402000401001, 0x4018a00080801004, 0x1230002105001008, 0x8904800800800400, 0x42000c42003810, 0x8408110400b012, 0x18086182000401, 0x2240088020c28000, 0x1001201040c004, 0xa02008010420020, 0x10003009010060, 0x4008008008014, 0x80020004008080, 0x282020001008080, 0x50000181204a0004, 0x102042111804200, 0x40002010004001c0, 0x19220045508200, 0x20030010060a900, 0x8018028040080, 0x88240002008080, 0x10301802830400, 0x332a4081140200, 0x8080010a601241, 0x1008010400021, 0x4082001007241, 0x211009001200509, 0x8015001002441801, 0x801000804000603, 0xc0900220024a401, 0x1000200608243L
]
magicNumberBishop = [
    0x2910054208004104, 0x2100630a7020180, 0x5822022042000000, 0x2ca804a100200020, 0x204042200000900, 0x2002121024000002, 0x80404104202000e8, 0x812a020205010840, 0x8005181184080048, 0x1001c20208010101, 0x1001080204002100, 0x1810080489021800, 0x62040420010a00, 0x5028043004300020, 0xc0080a4402605002, 0x8a00a0104220200, 0x940000410821212, 0x1808024a280210, 0x40c0422080a0598, 0x4228020082004050, 0x200800400e00100, 0x20b001230021040, 0x90a0201900c00, 0x4940120a0a0108, 0x20208050a42180, 0x1004804b280200, 0x2048020024040010, 0x102c04004010200, 0x20408204c002010, 0x2411100020080c1, 0x102a008084042100, 0x941030000a09846, 0x244100800400200, 0x4000901010080696, 0x280404180020, 0x800042008240100, 0x220008400088020, 0x4020182000904c9, 0x23010400020600, 0x41040020110302, 0x412101004020818, 0x8022080a09404208, 0x1401210240484800, 0x22244208010080, 0x1105040104000210, 0x2040088800c40081, 0x8184810252000400, 0x4004610041002200, 0x40201a444400810, 0x4611010802020008, 0x80000b0401040402, 0x20004821880a00, 0x8200002022440100, 0x9431801010068, 0x1040c20806108040, 0x804901403022a40, 0x2400202602104000, 0x208520209440204, 0x40c000022013020, 0x2000104000420600, 0x400000260142410, 0x800633408100500, 0x2404080a1410, 0x138200122002900L
]

occupancyMaskRook = [
    0x101010101017e, 0x202020202027c, 0x404040404047a, 0x8080808080876, 0x1010101010106e, 0x2020202020205e, 0x4040404040403e, 0x8080808080807e, 0x1010101017e00, 0x2020202027c00, 0x4040404047a00, 0x8080808087600, 0x10101010106e00, 0x20202020205e00, 0x40404040403e00, 0x80808080807e00, 0x10101017e0100, 0x20202027c0200, 0x40404047a0400, 0x8080808760800, 0x101010106e1000, 0x202020205e2000, 0x404040403e4000, 0x808080807e8000, 0x101017e010100, 0x202027c020200, 0x404047a040400, 0x8080876080800, 0x1010106e101000, 0x2020205e202000, 0x4040403e404000, 0x8080807e808000, 0x1017e01010100, 0x2027c02020200, 0x4047a04040400, 0x8087608080800, 0x10106e10101000, 0x20205e20202000, 0x40403e40404000, 0x80807e80808000, 0x17e0101010100, 0x27c0202020200, 0x47a0404040400, 0x8760808080800, 0x106e1010101000, 0x205e2020202000, 0x403e4040404000, 0x807e8080808000, 0x7e010101010100, 0x7c020202020200, 0x7a040404040400, 0x76080808080800, 0x6e101010101000, 0x5e202020202000, 0x3e404040404000, 0x7e808080808000, 0x7e01010101010100, 0x7c02020202020200, 0x7a04040404040400, 0x7608080808080800, 0x6e10101010101000, 0x5e20202020202000, 0x3e40404040404000, 0x7e80808080808000L
]

occupancyMaskBishop = [
    0x40201008040200, 0x402010080400, 0x4020100a00, 0x40221400, 0x2442800, 0x204085000, 0x20408102000, 0x2040810204000, 0x20100804020000, 0x40201008040000, 0x4020100a0000, 0x4022140000, 0x244280000, 0x20408500000, 0x2040810200000, 0x4081020400000, 0x10080402000200, 0x20100804000400, 0x4020100a000a00, 0x402214001400, 0x24428002800, 0x2040850005000, 0x4081020002000, 0x8102040004000, 0x8040200020400, 0x10080400040800, 0x20100a000a1000, 0x40221400142200, 0x2442800284400, 0x4085000500800, 0x8102000201000, 0x10204000402000, 0x4020002040800, 0x8040004081000, 0x100a000a102000, 0x22140014224000, 0x44280028440200, 0x8500050080400, 0x10200020100800, 0x20400040201000, 0x2000204081000, 0x4000408102000, 0xa000a10204000, 0x14001422400000, 0x28002844020000, 0x50005008040200, 0x20002010080400, 0x40004020100800, 0x20408102000, 0x40810204000, 0xa1020400000, 0x142240000000, 0x284402000000, 0x500804020000, 0x201008040200, 0x402010080400, 0x2040810204000, 0x4081020400000, 0xa102040000000, 0x14224000000000, 0x28440200000000, 0x50080402000000, 0x20100804020000, 0x40201008040200L
]

magicNumberShiftsRook = [
    52, 53, 53, 53, 53, 53, 53, 52, 53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53, 53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53, 53, 54, 54, 54, 54, 54, 54, 53,
    53, 54, 54, 54, 54, 54, 54, 53, 52, 53, 53, 53, 53, 53, 53, 52
]

magicNumberShiftsBishop = [
    58, 59, 59, 59, 59, 59, 59, 58, 59, 59, 59, 59, 59, 59, 59, 59,
    59, 59, 57, 57, 57, 57, 59, 59, 59, 59, 57, 55, 55, 57, 59, 59,
    59, 59, 57, 55, 55, 57, 59, 59, 59, 59, 57, 57, 57, 57, 59, 59,
    59, 59, 59, 59, 59, 59, 59, 59, 58, 59, 59, 59, 59, 59, 59, 58
]

magicMovesRook = [[0 for i in range(4096)] for j in range(64)]
magicMovesBishop = [[0 for i in range(4096)] for j in range(64)]
occupancyVariation = [[0 for i in range(4096)] for j in range(64)]


def generatePseudoMoves(state):
    """
    Takes input of a board object and returns a list of potential moves
    """
    moves = []
    side = state.pieceBitBoards[board.WHITE] if state.sideToMove == board.Side.W else state.pieceBitBoards[board.BLACK]

    # King Moves
    kingIndex = util.lastSetBit(side & state.pieceBitBoards[board.KINGS])
    kingMoves = util.getSetBits(kingAttacks[kingIndex] & ~side)
    kingMoves = map(lambda x: (util.asCoord(kingIndex), util.asCoord(x)), kingMoves)
    moves.extend(map(lambda x: board.Move(fromSqr=x[0], toSqr=x[1]), kingMoves))

    # Castling Moves
    if state.canCastle(state.sideToMove, True):
        moves.append(board.Move(fromSqr=util.asCoord(kingIndex), toSqr=util.asCoord(kingIndex + 2)))
    if state.canCastle(state.sideToMove, False):
        moves.append(board.Move(fromSqr=util.asCoord(kingIndex), toSqr=util.asCoord(kingIndex - 2)))

    # Knight Moves
    knightSquares = util.getSetBits(side & state.pieceBitBoards[board.KNIGHTS])

    for index in knightSquares:
        knightMoves = util.getSetBits(knightAttacks[index] & ~side)
        knightMoves = map(lambda x: (util.asCoord(index), util.asCoord(x)), knightMoves)
        moves.extend(map(lambda x: board.Move(fromSqr=x[0], toSqr=x[1]), knightMoves))

    # Pawn Moves
    pawnSquares = util.getSetBits(side & state.pieceBitBoards[board.PAWNS])
    for index in pawnSquares:
        pawnMoves = util.getSetBits(pawnPush(util.asBit(index), state.sideToMove, state))
        pawnMoves.extend(util.getSetBits(pawnAttack(index, state.sideToMove, state)))
        pawnMoves = map(lambda x: (util.asCoord(index), util.asCoord(x)), pawnMoves)
        for x in pawnMoves:
            if x[1][1] != 0 and x[1][1] != 7:
                moves.append(board.Move(fromSqr=x[0], toSqr=x[1]))
            else:
                moves.append(board.Move(fromSqr=x[0], toSqr=x[1], promotion='q'))
                moves.append(board.Move(fromSqr=x[0], toSqr=x[1], promotion='n'))
                moves.append(board.Move(fromSqr=x[0], toSqr=x[1], promotion='r'))
                moves.append(board.Move(fromSqr=x[0], toSqr=x[1], promotion='b'))

    # Rook Moves
    rookSquares = util.getSetBits(side & state.pieceBitBoards[board.ROOKS])

    for index in rookSquares:
        rookMoves = util.getSetBits(rookAttacks(index, state) & ~side)
        rookMoves = map(lambda x: (util.asCoord(index), util.asCoord(x)), rookMoves)
        moves.extend(map(lambda x: board.Move(fromSqr=x[0], toSqr=x[1]), rookMoves))

    # Bishop Moves
    bishopSquares = util.getSetBits(side & state.pieceBitBoards[board.BISHOPS])

    for index in bishopSquares:
        bishopMoves = util.getSetBits(bishopAttacks(index, state) & ~side)
        bishopMoves = map(lambda x: (util.asCoord(index), util.asCoord(x)), bishopMoves)
        moves.extend(map(lambda x: board.Move(fromSqr=x[0], toSqr=x[1]), bishopMoves))

    # Queen Moves
    queenSquares = util.getSetBits(side & state.pieceBitBoards[board.QUEENS])

    for index in queenSquares:
        queenMoves = util.getSetBits((bishopAttacks(index, state) | rookAttacks(index, state)) & ~side)
        queenMoves = map(lambda x: (util.asCoord(index), util.asCoord(x)), queenMoves)
        moves.extend(map(lambda x: board.Move(fromSqr=x[0], toSqr=x[1]), queenMoves))

    return moves


def rookAttacks(index, state=None, consideredPieces=None):
    if consideredPieces is None:
        consideredPieces = state.allPieces()
    bbBlockers = consideredPieces & occupancyMaskRook[index]
    # print "bbBlockers\n", util.bbAsString(bbBlockers)
    databaseIndex = rshift((bbBlockers * magicNumberRook[index]) & LONG_MASK, magicNumberShiftsRook[index])
    # print "magicMovesRook", databaseIndex, "\n", util.bbAsString(magicMovesRook[index][databaseIndex])
    return magicMovesRook[index][databaseIndex]


def bishopAttacks(index, state=None, consideredPieces=None):
    if consideredPieces is None:
        consideredPieces = state.allPieces()
    bbBlockers = consideredPieces & occupancyMaskBishop[index]
    databaseIndex = rshift((bbBlockers * magicNumberBishop[index]) & LONG_MASK, magicNumberShiftsBishop[index])
    return magicMovesBishop[index][databaseIndex]


def pawnPush(bb, pawnSide, state):
    moves = 0
    action = util.up if pawnSide == board.Side.W else util.down
    rank4 = board.RANK_BB[3] if pawnSide == board.Side.W else board.RANK_BB[4]
    pawns = action(bb) & ~state.allPieces()
    moves |= pawns
    pawns = action(pawns)
    moves |= pawns & ~state.allPieces() & rank4  # only add double push moves if the destination is on rank 4

    return moves


def pawnAttack(index, pawnSide, state):
    EPTarget = 0
    attack = 0
    if state.EPTarget is not None:
        EPTarget = util.asBit(state.EPTarget)
    if (pawnSide == board.Side.W):
        enemy = state.pieceBitBoards[board.BLACK]
        attack = pawnAttacks[0][index]
        EPTarget = util.up(EPTarget)
    else:
        enemy = state.pieceBitBoards[board.WHITE]
        attack = pawnAttacks[1][index]
        EPTarget = util.down(EPTarget)
    enemy |= EPTarget

    return attack & enemy


def attacksTo(pos, state, defendingSide, consideredPieces=None):
    if consideredPieces is None:
        consideredPieces = state.allPieces()
    enemyBB = state.pieceBitBoards[board.WHITE] if defendingSide == board.Side.B else state.pieceBitBoards[board.BLACK]
    enemyBB &= consideredPieces
    knights = knightAttacks[pos] & state.pieceBitBoards[board.KNIGHTS]
    kings = kingAttacks[pos] & state.pieceBitBoards[board.KINGS]
    bishopsQueens = bishopAttacks(pos, state, consideredPieces) & (state.pieceBitBoards[board.BISHOPS] | state.pieceBitBoards[board.QUEENS])
    rooksQueens = rookAttacks(pos, state, consideredPieces) & (state.pieceBitBoards[board.ROOKS] | state.pieceBitBoards[board.QUEENS])
    pawns = pawnAttack(pos, defendingSide, state) & state.pieceBitBoards[board.PAWNS]

    return (knights | kings | bishopsQueens | rooksQueens | pawns) & enemyBB

# Generate occupancy variations


def generateOccupancyVariations(isRook):

    bitCount = []

    for bitRef in range(64):
        mask = occupancyMaskRook[bitRef] if isRook else occupancyMaskBishop[bitRef]

        setBitsInMask = util.getSetBits(mask)
        bitCount = util.countSetBits(mask)
        variationCount = util.asBit(bitCount)

        for i in xrange(variationCount):
            occupancyVariation[bitRef][i] = 0

            # find bits set in index "i" and map them to bits in the 64 bit "occupancyVariation"

            setBitsInIndex = util.getSetBits(i)  # an array of integers showing which bits are set

            for j in range(len(setBitsInIndex)):
                occupancyVariation[bitRef][i] |= util.asBit(setBitsInMask[setBitsInIndex[j]])


def generateMoveDatabase(isRook):
    for bitRef in range(64):
        bitCount = util.countSetBits(occupancyMaskRook[bitRef]) if isRook else util.countSetBits(occupancyMaskBishop[bitRef])
        variations = util.asBit(bitCount)

        for i in xrange(variations):
            validMoves = 0
            if (isRook):

                magicIndex = rshift((occupancyVariation[bitRef][i] * magicNumberRook[bitRef]) & LONG_MASK, magicNumberShiftsRook[bitRef])
                # add Moves up
                for j in range(bitRef + 8, 64, 8):
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                # add Moves down
                for j in range(bitRef - 8, -1, -8):
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                # add Moves right
                for j in range(bitRef + 1, 64):
                    if j % 8 == 0:
                        break
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                # add moves left
                for j in range(bitRef - 1, -1, -1):
                    if j % 8 == 7:
                        break
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                magicMovesRook[bitRef][magicIndex] = validMoves

                # if magicIndex == 1785:
                    # print "occupancyVariation[", bitRef, "][", i, "]:\n", util.bbAsString(occupancyVariation[bitRef][i])
                    # print "magicMovesRook[", bitRef, "][", magicIndex, "]:\n", util.bbAsString(magicMovesRook[bitRef][magicIndex])

            else:
                magicIndex = rshift((occupancyVariation[bitRef][i] * magicNumberBishop[bitRef]) & LONG_MASK, magicNumberShiftsBishop[bitRef])

                # add moves up right
                for j in range(bitRef + 9, 64, 9):
                    if j % 8 == 0 or j > 63:
                        break
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                # add moves down left
                for j in range(bitRef - 9, -1, -9):
                    if j % 8 == 7 or j < 0:
                        break
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                # add moves up left
                for j in range(bitRef + 7, 64, 7):
                    if j % 8 == 7 or j > 63:
                        break
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                # add moves down right
                for j in range(bitRef - 7, -1, -7):
                    if j % 8 == 0 or j < 0:
                        break
                    validMoves |= util.asBit(j)
                    if (occupancyVariation[bitRef][i] & util.asBit(j)) != 0:
                        break

                magicMovesBishop[bitRef][magicIndex] = validMoves


def initPresets():
    """
    Loads initial presets
    """
    for i in range(64):
        util.setMask[i] = 1 << i
        bit = util.setMask[i]
        util.clearMask[i] = ~bit
        kingAttack = bit | util.right(bit) | util.left(bit)
        kingAttack |= util.up(kingAttack) | util.down(kingAttack)
        kingAttacks[i] = kingAttack & util.clearMask[i]

        l1 = util.left(bit)
        l2 = util.left(bit, 2)
        r1 = util.right(bit)
        r2 = util.right(bit, 2)

        h1 = l2 | r2
        h2 = l1 | r1

        knightAttacks[i] = util.up(h1) | util.down(h1) | util.up(h2, 2) | util.down(h2, 2)

        # pawn attacks
        wRightAttack = util.upRight(bit)
        wLeftAttack = util.upLeft(bit)
        bRightAttack = util.downRight(bit)
        bLeftAttack = util.downLeft(bit)
        pawnAttacks[0][i] = (wRightAttack | wLeftAttack)
        pawnAttacks[1][i] = (bRightAttack | bLeftAttack)

    generateOccupancyVariations(True)
    generateMoveDatabase(True)
    generateOccupancyVariations(False)
    generateMoveDatabase(False)

if __name__ == '__main__':
    pass
