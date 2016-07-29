from alpha_beta import *

def main():
    MAXINT = 32500
    depth = 4
    val_list = []
    infinity = 32000
    brd = Board(1)
    print(brd)

    while brd.moves_list:
        val, move = alphabeta(brd, -infinity, +infinity, depth, brd.player)
        brd.apply_move(move)
        brd.switch_player()
        brd.moves_list = brd.get_moves4player()
        print(brd)

        move = int(input('Enter a move'))
        while brd.moves_list and move not in brd.moves_list:
            move = int(input('Enter a move'))
        brd.apply_move(move)
        brd.moves_list = brd.get_moves4player()
        print(brd)


    print(brd.value)


#        brd.switch_player()

if __name__ == '__main__':
    main()
