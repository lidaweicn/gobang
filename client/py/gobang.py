'''
五子棋游戏逻辑(客户端单机)
'''


class GoBangGame(object):
    def __init__(self):
        # 初始化赢法数组(15*15*572), 并赋值False
        self.wins = [[[False for i in range(572)]
                      for x in range(15)] for y in range(15)]
        self.winCount = 0       # 赢法统计数组，用于统计一共有多少种赢法
        # self.myWin = []         # 玩家的赢法统计
        # self.computerWin = []   # 电脑的赢法统计
        # self.me = True          # 棋手标记,True为玩家下棋，False为电脑下棋
        # self.cp = 'w'           # 电脑为白棋
        # self.pp = 'b'           # 玩家为黑棋
        self.over = True       # 对局是否结束标记
        # self.winner = ''        # 存储赢者
        self.__initializa()     # 初始化游戏
        self.game_reset()
        pass

    def __initializa(self):
        '''变量初始化函数'''

        # 统计赢法数组
        for x in range(15):  # 行
            for j in range(11):
                for k in range(5):
                    self.wins[x][j + k][self.winCount] = True
                self.winCount += 1

        for x in range(15):  # 列
            for j in range(11):
                for k in range(5):
                    self.wins[j + k][x][self.winCount] = True
                self.winCount += 1

        for x in range(11):  # 斜
            for j in range(11):
                for k in range(5):
                    self.wins[x + k][j + k][self.winCount] = True
                self.winCount += 1

        for x in range(11):  # 反斜
            for j in range(14, 3, -1):
                for k in range(5):
                    self.wins[x + k][j - k][self.winCount] = True
                self.winCount += 1

    def game_reset(self):
        if not self.over:
            return
        self.myWin = []         # 玩家的赢法统计
        self.computerWin = []   # 电脑的赢法统计
        self.me = True          # 棋手标记,True为玩家下棋，False为电脑下棋
        self.cp = 'w'           # 电脑为白棋
        self.pp = 'b'           # 玩家为黑棋
        self.over = False       # 对局是否结束标记
        self.winner = ''        # 存储赢者

        # 棋盘计数，用于存储棋盘上各个点是否有棋子，且落子属于谁的(0空1玩家2电脑)chessboard
        self.count = [[0 for x in range(15)] for y in range(15)]
        # 初始化玩家和电脑赢法数组
        for x in range(self.winCount):
            self.myWin.append(0)
            self.computerWin.append(0)
        pass

    def __computerAI(self):
        '''电脑AI算法
        查找最佳游戏点, 返回游戏坐标'''

        # 初始化加权分数
        self.my_score = [[0 for x in range(15)] for y in range(15)]
        self.computer_score = [[0 for x in range(15)] for y in range(15)]
        # 初始化最高加权分变量和最佳游戏坐标
        max_score = 0
        u = 0
        v = 0
        # 查找游戏最佳点
        for x in range(15):
            for j in range(15):
                if self.count[x][j] == 0:
                    for k in range(self.winCount):
                        if self.wins[x][j][k]:
                            if self.myWin[k] == 1:
                                self.my_score[x][j] += 200
                            elif self.myWin[k] == 2:
                                self.my_score[x][j] += 400
                            elif self.myWin[k] == 3:
                                self.my_score[x][j] += 2000
                            elif self.myWin[k] == 4:
                                self.my_score[x][j] += 10000

                            if self.computerWin[k] == 1:
                                self.computer_score[x][j] += 220
                            elif self.computerWin[k] == 2:
                                self.computer_score[x][j] += 420
                            elif self.computerWin[k] == 3:
                                self.computer_score[x][j] += 2100
                            elif self.computerWin[k] == 4:
                                self.computer_score[x][j] += 20000

                    if self.my_score[x][j] > max_score:
                        max_score = self.my_score[x][j]
                        u = x
                        v = j
                    elif self.my_score[x][j] == max_score:
                        if self.computer_score[x][j] >\
                                self.computer_score[u][v]:
                            u = x
                            v = j

                    if self.computer_score[x][j] > max_score:
                        max_score = self.computer_score[x][j]
                        u = x
                        v = j
                    elif self.computer_score[x][j] == max_score:
                        if self.my_score[x][j] > self.my_score[u][v]:
                            u = x
                            v = j

        self.count[u][v] = 2
        for k in range(self.winCount):
            if self.wins[u][v][k]:
                self.computerWin[k] += 1
                self.myWin[k] = 99
            if self.computerWin[k] == 5:
                self.winner = '电脑'
                self.over = True

        return u, v, 'w'

    def do_game(self, x, y):
        '''执行游戏函数'''

        # 判断游戏是否结束
        if self.over:
            print(self.winner, '赢了')
            return

        # 执行落子判断
        if self.count[x][y] != 0:
            return
        # 执行落子
        self.count[x][y] = 1
        for k in range(self.winCount):
            if self.wins[x][y][k]:
                self.myWin[k] += 1
                self.computerWin[k] = 99
                if self.myWin[k] == 5:
                    self.winner = '你'
                    self.over = True
        self.me = not self.me
        return self.__computerAI()

    # 判断坐标点是否有棋子
    def is_null(self, x, y):
        if self.count[x][y]:
            return True
        return False
        pass


def main():
    '''main函数,只用于测试'''
    gbg = GoBangGame()
    x, y, z = gbg.do_game(5, 6)
    print(x, y, z)


if __name__ == '__main__':
    main()
