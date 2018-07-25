from level import LEVEL
from database import DatabaseHandler


class Game(DatabaseHandler):
    def __init__(self):
        # self.LoginUser = LoginUser
        # self.AllRoom = AllRoom
        # self.Fight = Fight
        # self.connfd = self.LoginUser[user_name].connfd
        self.gobang_map = []    # 创建游戏map存储棋盘信息，二维列表
        self.steps = []         # 存储记录落子信息，顺序，[(x,y,c),()]
        # self.player_black = []  # 创建玩家列表存储下棋坐标点，黑棋
        # self.player_white = []  # 创建玩家列表存储下棋坐标点，白棋
        self.wins = []          # 创建赢法列表，存储赢法信息
        self.count_wins()       # 统计赢法数组
        self.blackwins = []     # 存储黑棋赢法
        self.whitewins = []     # 存储白棋赢法
        self.game_init()        # 游戏初始化

    def game_init(self):
        # 初始化棋盘信息
        self.gobang_map = [[0 for x in range(15)] for y in range(15)]
        # 初始化落子记录
        self.steps = []
        # 初始化黑棋和白棋赢法计数数组
        self.blackwins = [0 for x in range(572)]
        self.whitewins = [0 for x in range(572)]
        pass

    def count_wins(self):
        self.winCount = 0
        # 棋盘计数(15　*　15)(0空  1:玩家１  2:玩家２)
        # 初始化赢法数组(15*15*572)
        self.wins = [[[False for i in range(572)]
                     for x in range(15)] for y in range(15)]
        # 统计赢法数组
        for x in range(15):  # 行
            for j in range(11):
                for k in range(5):
                    # print(x, j + k, winCount)
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

        # print("赢法已经统计完毕")
        # return self.wins

    # def init_Fight(self, roomid):
    #     # 初始化棋盘信息
    #     # go_type = [[0 for x in range(15)] for y in range(15)]  #count
    #     # 上边先初始化为数字0，如果初始化为'.',当传到客户端时分割时可能在
    #     # 字符与字符之间会出现多个空格，而字符与数字之间好像只有一个空格，可用正则分割
    #     dic = {}
    #     # 获得赢法数组
    #     m = self.count_wins()
    #     dic['Wins'] = m
    #     dic['go_type'] = [[0 for x in range(15)] for y in range(15)]
    #     dic['black'] = []
    #     dic['white'] = []

    #     # 获得赢法数组
    #     # m = get_method()
    #     # enemy = self.LoginUser[user_name].enemy
    #     dic['start_undo'] = []  # 表示使赢法失效的列表
    #     for x in range(572):
    #         dic_undo = {}
    #         dic_undo['positon'] = ''
    #         dic_undo['blacktrue'] = 0  # 失效前的所占某一层赢法True的个数
    #         dic_undo['whitetrue'] = 0
    #         dic['start_undo'].append(dic_undo)

    #     dic['blackwins'] = []
    #     dic['whitewins'] = []
    #     # print(len(dic[self.user_name]))
    #     # 初始化玩家和电脑赢法数组
    #     for x in range(572):
    #         # dic['start_undo'].append(0)
    #         dic['blackwins'].append(0)
    #         dic['whitewins'].append(0)
    #     # print(len(dic[self.user_name]))
    #     # prs
    #     self.Fight[roomid] = dic

    # def update_winstatus(self, user_name, roomid):
    #     # 更新房间
    #     self.AllRoom[roomid].first_hand = ''
    #     self.AllRoom[roomid].start_status = 0
    #     # self.table_left = ''
    #     # self.table_right = ''
    #     self.AllRoom[roomid].who_choice = ''
    #     # self.audience = []
    #     self.AllRoom[roomid].do_alarm = 0
    #     self.AllRoom[roomid].winner = ''
    #     self.AllRoom[roomid].atie = 0
    #     self.AllRoom[roomid].winner = ''

    #     enemy = self.LoginUser[user_name].enemy
    #     # 更新玩家信息
    #     self.LoginUser[user_name].user_status = 1
    #     self.LoginUser[user_name].total_time = 0
    #     self.LoginUser[enemy].user_status = 1
    #     self.LoginUser[enemy].total_time = 0
    #     self.LoginUser[user_name].level_up = 0
    #     # 跟新Fight
    #     # {roomid:{'go_type':[],'black':[],'white':[],user_name:[],
    #     # another_name:[],'Wins':Wins},roomid:{}}
    #     # self.Fight[roomid]['go_type'] = [
    #     #     [0 for x in range(15)] for y in range(15)]
    #     self.Fight[roomid]['blackwins'] = []
    #     self.Fight[roomid]['whitewins'] = []
    #     for x in range(572):
    #         self.Fight[roomid]['blackwins'].append(0)
    #         self.Fight[roomid]['whitewins'].append(0)

    #     self.Fight[roomid]['black'] = []
    #     self.Fight[roomid]['white'] = []

    def game_do(self, x, y, c):
        ''' 此处书写game逻辑代码 '''

        # 0代表无落子，１代表黑棋，2代表白棋
        if self.gobang_map[x][y] != 0:
            return
        if c == 'B':
            self.gobang_map[x][y] = 1
            for k in range(572):
                if self.wins[x][y][k]:
                    self.blackwins[k] += 1
                    self.whitewins[k] += 10
        elif c == 'W':
            self.gobang_map[x][y] = 2
            for k in range(572):
                if self.wins[x][y][k]:
                    self.whitewins[k] += 1
                    self.blackwins[k] += 10
        else:
            return
        # 记录游戏步数
        self.steps.append((x, y, c))
        # print('游戏内部：', self.steps, self.whitewins, self.blackwins)
        # 判断输赢
        for k in range(572):
            if self.blackwins[k] == 5:
                # 此种赢法成立
                print('B', k)
                return 'B'
            if self.whitewins[k] == 5:
                # 此种赢法成立
                print('W', k)
                return 'W'
        # 判断是否和棋
        for k in range(572):
            if self.blackwins[k] < 5 or self.whitewins[k] < 5:
                return
        else:
            return 'A'

    def game_undo(self, c):
        # 参数c为悔棋棋子颜色
        # 判断如果落子记录中最后一个棋子的颜色是否相同
        if self.steps[-1][2] == c:
            # 相同，则说明，在悔棋时，对方没有下棋
            # 删除一个最后一个棋子即可
            self.game_delete()
        else:
            # 否则，则说明，在悔棋时，对方已经下棋
            # 则需要删除最后两个棋子
            self.game_delete()
            self.game_delete()

    def game_delete(self):
        '''删除最后一个棋子函数'''
        if not self.steps:
            return
        x, y, c = self.steps[-1]
        # 修改赢法计数列表
        if c == 'B':
            # 遍历赢法计数列表
            for k in range(572):
                # 判断是否存在此赢法
                if self.wins[x][y][k]:
                    # 判断此赢法
                    self.blackwins[k] -= 1
                    self.whitewins[k] -= 10
        elif c == 'W':
            for k in range(572):
                if self.wins[x][y][k]:
                    self.whitewins[k] -= 1
                    self.blackwins[k] -= 10
        # 删除步数记录列表最后一个元素
        self.steps.pop()
        # 修改地图棋子信息
        self.gobang_map[x][y] = 0

    def save_game_data(self, user, count):
        # 从数据库获取用户信息
        user_info = self.get_user_info(user.user_name)
        addlevel = 0
        if user_info:
            if user_info['GameScore'] + count > LEVEL[user_info['GameLevel']]:
                addlevel = 1
        if count:
            self.save_game_info(user.user_name, count, addlevel, 1, 1)
        else:
            self.save_game_info(user.user_name, 0, 0, 1, 0)
        # 更新用户信息
        self.update_user_info(user)
        # 返回游戏是否升级
        if addlevel:
            return True
        return False

    def update_user_info(self, user):
        # 从数据库获取更新信息，更新user对象
        user_info = self.get_user_info(user.user_name)
        user.game_integral = user_info['GameScore']
        user.game_level = user_info['GameLevel']
        user.win_num = user_info['WinRound']
        user.total_num = user_info['TotalRound']
