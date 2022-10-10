import copy


class Solver:

    def __init__(self, original):
        self.isTry = False
        # key: num         value: coord set of num
        self.num_coord_list = {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        # key: block(3x3)   value: coord set of box in this block
        self.block_box_list = {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        # key: num         value: ser of all block that num in
        self.num_block_list = {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        # coord set of empty box
        self.box_list = set()
        # num[1-9]
        self.all_num_set = set(range(1, 10))
        # when should try the value will be gave in `run_2`, structure: [coord, numSetCanPutInThisCoord]
        self.try_start = None
        # before you make a try, you should make a snapshot
        self.snapshot = list()
        # init board
        self.board = [[0] * 9 for i in range(9)]
        # check question and apply it
        original = [i.strip() for i in original.split(',')]
        if len(original) != 9:
            raise Exception('Error input! Please check row number.')
        for row in range(9):
            row_data = original[row]
            if len(row_data) != 9:
                raise Exception('Error input! Please check row[{}].'.format(row+1))
            for col in range(9):
                try:
                    n = int(row_data[col])
                except:
                    raise Exception('Error input! It\'s not a number in coord:({}, {}), please check.'.format(row+1, col+1))
                if n:
                    # check row
                    if n in self.board[row]:
                        raise Exception('Error input! There are more than one number[{}] in row[{}]. Please check.'
                                        .format(n, row+1))
                    # check col
                    for i in self.board:
                        if i[col] == n:
                            raise Exception('Error input! There are more than one number[{}] in colume[{}] Please check.'
                                            .format(n, col+1))
                    # check block
                    block_seq = self.get_block_seq((row, col))
                    if block_seq in self.num_block_list[n]:
                        raise Exception('Error input! There are more than one number[{}] in block[{}] Please check.'
                                        .format(n, block_seq))
                self.board[row][col] = n
                if n:
                    self.num_coord_list[n].add((row, col))
                    self.num_block_list[n].add(self.get_block_seq((row, col)))
                else:
                    self.box_list.add((row, col))
                    self.block_box_list[self.get_block_seq((row, col))].add((row, col))

    def run_1(self):
        flag = False
        for n in range(1, 10):
            for z in self.all_num_set - self.num_block_list[n]:
                res = []
                for i in self.block_box_list[z]:
                    tmp_list = self.num_coord_list[n]
                    if i[0] not in [j[0] for j in tmp_list] and i[1] not in [j[1] for j in tmp_list]:
                        res.append(i)
                if len(res) == 1:
                    self.put(res[0][0], res[0][1], n, z)
                    flag = True
        return flag

    def run_2(self):
        coord = (None, None)
        try_set = None
        shot = 9
        mark = False
        for coo in copy.deepcopy(self.box_list):
            can_put = self.get_can_put_num(coo)
            can_put_length = len(can_put)
            if can_put_length == 1:
                n = can_put.pop()
                z = self.get_block_seq(coo)
                self.put(*coo, n, z)
                mark = True
                continue
            if can_put_length < shot:
                shot = can_put_length
                coord = coo
                try_set = can_put
        if not mark:
            self.try_start = [coord, try_set]
        return mark

    def try_put(self, coord, try_set):
        self.isTry = True
        x, y = coord
        n = try_set.pop()
        z = self.get_block_seq(coord)
        self.create_shot(coord, try_set)
        self.put(x, y, n, z)

    def create_shot(self, coord, try_set):
        '''
        self.snapshot.append((coord, try_set, copy.deepcopy(self.board), copy.deepcopy(self.num_coord_list),
                              copy.deepcopy(self.block_box_list), copy.deepcopy(self.num_block_list),
                              copy.deepcopy(self.box_list)))'''
        self.snapshot.append((coord, try_set, copy.deepcopy(self.board)))

    def restore(self):
        while not self.snapshot[-1][1]:
            self.snapshot.pop()
            if not self.snapshot:
                break
        data = self.snapshot[-1]
        self.board = data[2]
        # init properties before restore
        self.num_coord_list = {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        self.block_box_list = {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        self.num_block_list = {1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(), 8: set(), 9: set()}
        self.box_list = set()
        # restore properties
        for row in range(9):
            for col in range(9):
                n = self.board[row][col]
                if n:
                    self.num_coord_list[n].add((row, col))
                    self.num_block_list[n].add(self.get_block_seq((row, col)))
                else:
                    self.box_list.add((row, col))
                    self.block_box_list[self.get_block_seq((row, col))].add((row, col))
        #self.num_coord_list = data[3]
        #self.block_box_list = data[4]
        #self.num_block_list = data[5]
        #self.box_list = data[6]
        x, y = data[0]
        n = data[1].pop()
        self.put(x, y, n, self.get_block_seq(data[0]))

    def check(self, x, y, z):
        related_coords = set()
        for coo in self.box_list:
            if coo[0] == x or coo[1] == y:
                related_coords.add(coo)
        related_coords = related_coords | self.block_box_list[z]
        for c in related_coords:
            if not len(self.get_can_put_num(c)):
                self.restore()

    def get_can_put_num(self, coord):
        x, y = coord
        block_set = set([self.board[row][col] for row in range(x//3*3, x//3*3+3) for col in range(y//3*3, y//3*3+3)])
        return self.all_num_set - (set(self.get_row(x)) | set(self.get_col(y)) | block_set)

    @staticmethod
    def get_block_seq(coord):
        return coord[0]//3*3+coord[1]//3+1

    def get_row(self, row):
        return self.board[row]

    def get_col(self, col):
        return [i[col] for i in self.board]

    def put(self, x, y, n, z):
        self.board[x][y] = n
        self.num_coord_list[n].add((x, y))
        self.block_box_list[z] -= {(x, y)}
        self.num_block_list[n].add(z)
        self.box_list -= {(x, y)}
        if self.isTry:
            self.check(x, y, z)

    def show_board(self):
        [print(i) for i in self.board]

    def start(self):
        while self.box_list:
            while self.run_1() or self.run_2():
                pass
            if not self.box_list:
                break
            self.try_put(*self.try_start)


if __name__ == '__main__':
    q1 = '000007020, 806000100, 000000000, 390002000, 000085006, 000000400, 000060000, 020000070, 010040000'
    q2 = '000670080, 060000447, 705800000, 020041000, 080520004, 907000102, 030005260, 000008470, 602090000'

    tmp = Solver(q2)
    tmp.start()
    tmp.show_board()
