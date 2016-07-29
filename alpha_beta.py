from copy import deepcopy
from BoardSquare import *


def gen_board_list(brd):
    """

    :rtype: list
    """
    cbrd = deepcopy(brd)
    brd_list = []
    mov_list = brd.get_moves4player()
    for mov in mov_list:
        cbrd.apply_move(mov)
        #        print(brd)  #------------------------------------------------------
        brd_list.append(cbrd)
        cbrd = deepcopy(brd)
    return brd_list


def print_data(alpha, beta, v, mov):
    print("move - ", str(mov))
    print("alpha= " + str(alpha) + " beta= " + str(beta) + " value= " + str(v))
    print("\n\n")


def alphabeta(lbrd, alpha, beta, depth, max_player):
    val, mov = lbrd.value, lbrd.move
    #    turn = 1
    if depth == 0:
        Board.values_list.append([alpha, lbrd.value, lbrd.move])
        # mov = max(lbrd.valList)[1]
        return [lbrd.value, lbrd.move]

    cbrd = deepcopy(lbrd)

    if max_player:
        ab_value = alpha
        max_list = gen_board_list(cbrd)
        for max_brd in max_list:
            val, mov = alphabeta(max_brd, alpha, beta, depth - 1, -lbrd.player)
            ab_value = max(ab_value, val)
            if (ab_value >= beta): return ab_value, mov
            alpha = max(alpha, ab_value)
        return ab_value, mov

    else:
        ab_value = beta
        min_list = gen_board_list(cbrd)
        for min_brd in min_list:
            val, mov = alphabeta(min_brd, alpha, beta, depth - 1, -lbrd.player)
            #            print (minbrd)
            ab_value = min(ab_value, val)
            if (ab_value <= alpha): return ab_value, mov
            beta = min(beta, ab_value)

        return ab_value, mov


def call_a_b_1(brd):
    val, move = alphabeta(brd, -infinity, +infinity, depth, -brd.player)
    if move == -1:
        brd.set_player(-brd.player)
        return
    brd.applyMove(move)
    brd.update_moves()
    # redraw(ot_game)
    print(brd)
    brd.moves_list.append(deepcopy(brd))
    brd.set_player(-brd.player)
