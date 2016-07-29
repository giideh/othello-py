from tkinter import *
from alpha_beta import *
from BoardSquare import *


def redraw():
    for i in range(NO_SQRS):
        ot_game[i].config(image=None)
        if brd.board[i].status == 1:
            ot_game[i].config(image=ibd, width=60, height=60, text='1')
        elif brd.board[i].status == -1:
            ot_game[i].config(image=ird, width=60, height=60, text='-1')
        else:
            ot_game[i].config(text='0')

    return brd

def print_data(a, b, v, mov):
    print ("move - ", str(mov))
    print ("alpha= " + str(a) + " beta= " + str(b) + " value= " + str(v))
    print ("\n\n")

def on_click(move):
    if brd.move_ok(move):
        brd.apply_move(move)
        # brd.update_moves()
        redraw()
        print(brd)
        # brd.moves_list.append(move)
        brd.switch_player()
        brd.moves_list = brd.get_moves4player()
        val, move = alphabeta(brd, -infinity, +infinity, depth, -brd.player)
        if move == -1:
            brd.switch_player()
            return
        brd.apply_move(move)
        # brd.update_moves()
        redraw()
        print(brd)
        # brd.moves_list.append(deepcopy(brd))
        brd.switch_player()
        brd.moves_list = brd.get_moves4player()


def undo():
    mv_lst = brd.moves_list
    mv_lst.pop()
    mv_lst.pop()
#    print(mv_lst[len(Board.moves)-1])
    brd = mv_lst[-1]
    redraw()
    print(brd)

def no_move():
    brd.switch_player()
    call_a_b(brd)

def close_window ():
    root.destroy()

def call_a_b(brd):
    MAXINT = 32500;
    depth = 3;
    val_list =[]
    infinity = 32000
    val, move = alphabeta(brd, -infinity, +infinity, depth, -brd.player)
    if move == -1:
        brd.set_player(-brd.player)
        return
    brd.apply_move(move)
    #brd.update_moves()
    redraw()
    print(brd)
    brd.moves_list.append(deepcopy(brd))
    brd.switch_player()


depth = 2
value_list = []
infinity = MAXINT

root = Tk()
root.title("Othello")
root.geometry("700x900")

##rd=PhotoImage(file='C:/Users/gabi/Google Drive/CODE/pyfiles/Othello/images/rd.gif')
##bd=PhotoImage(file='C:/Users/gabi/Google Drive/CODE/pyfiles/Othello/images/bd.gif')

ird = PhotoImage(file='C:/Users/gabi\PycharmProjects/Othello-py/srd.gif')
ibd = PhotoImage(file='C:/Users/gabi\PycharmProjects/Othello-py/sbd.gif')

brd = Board(1)
# brd.switch_player()
print(brd)

ot_game = [Button(root, width=8, height=4, justify=LEFT) for r in range(Board.ROWS) for c in range(Board.COLS)]
for i in range(Board.ROWS * Board.COLS):
    ot_game[i]["text"] = 'x'
    ot_game[i].grid(row=brd.row(i), column=brd.col(i))
    ot_game[i]["command"] = lambda i=i: on_click(i)

i += 9
undo_btn = Button(root, width=8, height=2, justify=LEFT, text="Undo", command=undo)
undo_btn.grid(row=brd.row(i + 1), column=brd.col(i + 1))

i += 2
redraw_btn = Button(root, width=8, height=2, justify=LEFT, text="Redraw", command=redraw)
redraw_btn.grid(row=brd.row(i), column=brd.col(i + 1))
i += 1
exit_btn = Button(root, width=8, height=2, justify=LEFT, text="Exit", command=close_window)
exit_btn.grid(row=brd.row(i), column=brd.col(i + 1))
i += 2
nomove_btn = Button(root, width=8, height=2, justify=LEFT, text="No Move", command=no_move)
nomove_btn.grid(row=brd.row(i), column=brd.col(i + 1))

for i in (27, 36):
    brd.board[i].status = 1
    ot_game[i].config(image=ibd, width=60, height=60)
for i in (28, 35):
    brd.board[i].status = -1
    ot_game[i].config(image=ird, width=60, height=60)

val, move = alphabeta(brd, -infinity, +infinity, depth, brd.player)
brd.apply_move(move)
# brd.update_moves()
redraw()
print(brd)
# brd.moves_list.append(deepcopy(brd))
brd.switch_player()
brd.moves_list = brd.get_moves4player()
root.mainloop()
