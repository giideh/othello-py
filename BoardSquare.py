from copy import deepcopy

MAXINT = 320000
MAX_PLAYER = 1
MACHINE = -1
ROWS = 8
COLS = 8
LENGTH = 8

FADI = 0
NO_SQRS = LENGTH * LENGTH

NORTH = -ROWS
SOUTH = ROWS

EAST = 1
WEST = -1

N_EAST = NORTH + EAST
N_WEST = NORTH + WEST
S_EAST = SOUTH + EAST
S_WEST = SOUTH + WEST

CORNER_UL = 0
CORNER_UR = LENGTH - 1
CORNER_BL = NO_SQRS - LENGTH
CORNER_BR = NO_SQRS - 1
MARK = LENGTH / 2 * (LENGTH - 1) - 1
DIR = [NORTH, N_EAST, EAST, S_EAST, SOUTH, S_WEST, WEST, N_WEST]

topEdge = (0, 1, 2, 3, 4, 5, 6, 7)
botEdge = (56, 57, 58, 59, 60, 61, 62, 63)
leftEdge = (0, 8, 16, 24, 32, 40, 48, 56)
rightEdge = (7, 15, 23, 31, 39, 47, 55, 63)
edge = list(set(topEdge + botEdge + leftEdge + rightEdge))
corners = (0, 7, 56, 63)
corner1 = (1, 8, 9, 6, 14, 15, 48, 49, 57, 54, 55, 62)
corner2 = (2, 10, 16, 17, 18, 5, 13, 21, 22, 23, 40, 41, 42, 50, 58, 45, 46, 47, 53, 61)


class Square():
    def __init__(self, r=-1, c=-1, value=0, status=0, owner='x'):
        self.r = r
        self.c = c
        self.value = value
        self.status = status
        # owner i, 0=empty, 1 = you, -1 = oppnent
        self.owner = owner

    def __str__(self):
        sqr_str = 'Row = {0}  Col = {1}\n'.format(str(self.r), str(self.c))
        sqr_str = '{0} Status = {1}  Value = {2}\n'.format(sqr_str, str(self.status), str(self.value))
        return sqr_str

    @property
    def empty(self):
        # return self.status in ['x', '.']
        return self.status == 0

    def set_status(self, status: int):
        """

        :type status: int
        """
        self.status = status

    def get_status(self):
        return self.status

    def set_owner(self, owner):
        """

        :param owner: string
        """
        self.owner = owner

    def get_owner(self):
        return self.owner

    def set_status_owner(self, sta):
        """

        :param sta: string
        """
        self.status = sta
        self.owner = '+' if sta == 1 else 'o'

    @property
    def get_status_owner(self):
        return self.status, self.owner

    def set_value(self, value):
        """

        :param value: int
        """
        self.value = value

    @property
    def get_value(self):
        return self.value

    @property
    def on_click(self):
        return self.r, self.c


class Board():
    DIR = [-9, -8, -7, 1, 9, 8, 7, -1]
    ROWS = 8
    COLS = 8
    values_list = []

    def __init__(self, player=0):
        """

        :rtype: Board
        """
        self.player = player
        self.board = [Square() for r in range(Board.ROWS) for c in range(Board.COLS)]
        self.set_sqr_values()

        self.frontier = [18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45]
        self.update_frontier_txt()

        self.explored = [27, 28, 35, 36]

        #        you is '+, 1' opponent is 'o, -1'
        self.board[27].set_status_owner(1)
        self.board[36].set_status_owner(1)

        self.board[28].set_status_owner(-1)
        self.board[35].set_status_owner(-1)

        self.move = 0
        self.prevMove = 0
        self.value = 0
        self.prevValue = 0

        self.moves_list = self.get_moves4player()

    def update_frontier_txt(self):
        for sqNo in self.frontier: self.board[sqNo].set_owner('.')

    def __str__(self):
        brd_str = ""
        brd_str += 'Player ' + str(self.player) + '\n'
        for i in range(Board.ROWS):
            for j in range(Board.COLS):
                brd_str = brd_str + str(self.board[Board.ROWS * i + j].owner) + " "
            brd_str += "\n"

        brd_str += "Move " + str(self.move) + "  Value " + str(self.value) + "\n"
        brd_str += "Previous Move " + str(self.prevMove) + " Previous Value " + str(self.prevValue) + "\n"
        brd_str += "Frontier Moves " + str(self.frontier) + "\n"
        brd_str += "Possible Moves " + str(self.moves_list) + "\n"
        brd_str += '\n\n'
        return brd_str

    def clone(self):
        lbrd = deepcopy(self)
        lbrd.maxList = []
        lbrd.minList = []
        return lbrd

    def sq_num(self, row, col):
        return row * Board.ROWS + col

    def row(self, index):
        return index // Board.ROWS

    def col(self, index):
        return index % Board.COLS

    def top(self, index):
        return self.row(index) == 0

    def bottom(self, index):
        return self.row(index) == Board.ROWS - 1

    def l_edge(self, index):
        return self.col(index) == 0

    def r_edge(self, index):
        return self.col(index) == Board.COLS - 1

    def edge(self, index):
        return self.top(index) or self.bottom(index) or self.l_edge(index) or self.r_edge(index)

    def corner(self, index):
        return index == 0 or index == Board.COLS - 1 or index == Board.ROWS - 1 * Board.COLS or index == Board.ROWS * Board.COLS - 1

    def update_frontier(self, m):
        if m in self.frontier: self.frontier.remove(m)
        ml_dir = [m + l_dir for l_dir in Board.DIR if
                  (not self.off_board(m, l_dir) and self.board[m + l_dir].empty and m + l_dir not in self.frontier)]
        self.frontier += ml_dir
        self.update_frontier_txt()

    def update_explored(self, sq_no):
        self.explored.append(sq_no)
        self.board[sq_no].set_status_owner(self.player)

    def evaluate(self, sq_no):
        val = self.board[sq_no].value
        for s in self.explored:
            if self.board[s].status == self.player:
                val += 2
        return val

    def switch_player(self):
        self.player = -self.player

    def flip_direction(self, sq_no, l_dir):
        end_point = sq_no + l_dir
        while self.board[end_point].get_status() == -self.player:
            self.board[end_point].set_status_owner(self.player)
            end_point += l_dir

    def flip_stones_1(self, sq_no):
        for l_dir in Board.DIR:
            if self.is_move_legal(sq_no, l_dir):
                self.flip_direction(sq_no, l_dir)

    def flip_stones(self, sq_no):
        dirs = [l_dir for l_dir in Board.DIR if self.is_move_legal(sq_no, l_dir)]
        for l_dir in dirs:
            self.flip_direction(sq_no, l_dir)

    def apply_move(self, sq_no):
        self.flip_stones(sq_no)
        self.board[sq_no].set_status_owner(self.player)

        self.prevValue = self.value
        self.value = self.evaluate(sq_no)
        self.prevMove = self.move
        self.move = sq_no

        self.update_explored(sq_no)
        self.update_frontier(sq_no)

    def off_board(self, sq_no, l_dir):
        return ((self.top(sq_no) and (l_dir == NORTH or l_dir == N_EAST or l_dir == N_WEST)) or
                (self.bottom(sq_no) and (l_dir == SOUTH or l_dir == S_EAST or l_dir == S_WEST)) or
                (self.l_edge(sq_no) and (l_dir == WEST or l_dir == N_WEST or l_dir == S_WEST)) or
                (self.r_edge(sq_no) and (l_dir == EAST or l_dir == N_EAST or l_dir == S_EAST)) or
                sq_no + l_dir > 63 or sq_no + l_dir < 0)

    def is_move_legal(self, sq_no, l_dir):
        if not self.board[sq_no].empty: return False
        # look at Next position
        sq_no += l_dir
        if self.off_board(sq_no, l_dir): return False
        if self.board[sq_no].get_status() == -self.player:
            while self.board[sq_no].get_status() == -self.player:  # and not self.off_board(sqNo, ldir):
                sq_no += l_dir
                if self.off_board(sq_no, l_dir): return False
            if self.board[sq_no].get_status() == self.player: return True
        return False

    def move_ok(self, sq_no):
        dirs = [sq_no, [l_dir for l_dir in Board.DIR if self.is_move_legal(sq_no, l_dir)]]
        return True if dirs[1] else False

    def get_moves4player(self):
        if self.player == 0:
            self.moves_list = []
        self.moves_list = [m for m in self.frontier if self.move_ok(m)]
        return self.moves_list

    def set_sqr_values(self):
        for s in range(NO_SQRS):
            if s in edge:
                self.board[s].value = 10
            elif s in corner2:
                self.board[s].value = 15
            elif s in corner1:
                self.board[s].value = -30
            elif s in corners:
                self.board[s].value = 50
            else:
                self.board[s].value = 12
