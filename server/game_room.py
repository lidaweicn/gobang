from game import Game
from time import sleep
from send_data import SendData
from client_quit import ExceptQuit
from common import get_time


class Room(ExceptQuit, Game, SendData):
    def __init__(self, room_id, LoginUser, AllRoom, Log):
        self.room_id = room_id
        self.LoginUser = LoginUser
        self.AllRoom = AllRoom
        self.Log = Log
        # self.Fight = Fight

        # self.table_left = ''
        # self.table_right = ''
        # self.audience = []
        # self.do_alarm = 0

        self.start_status = False   # 游戏开始状态
        self.first_hand = None      # 游戏先手
        self.who_choice = None      # 当前下棋者
        self.atie = False           # 是否出现和棋
        self.player_left = None     # 房间左边玩家
        self.player_right = None    # 房间右边玩家

        self.undo_status = False    # 是否悔棋
        self.winner = None          # 赢棋者
        self.loster = None          # 输棋者
        self.giveup_player = None   # 认输者
        self.fast_num = 3           # 开始时房间为空，快速进入房间优先级为3
        Game.__init__(self)

    def room_init(self):
        self.winner = None
        self.giveup_player = None
        self.undo_status = False
        pass

    def room_reset(self):
        '''重置游戏，游戏结束时执行（winner，和棋，认输）'''
        self.start_status = False   # 游戏开始状态
        self.first_hand = None      # 游戏先手
        self.who_choice = None      # 当前下棋者
        self.atie = False           # 是否出现和棋
        self.room_init()
        # 初始化玩家游戏状态，时间，是否升级
        if self.player_left:
            self.player_left.game_status = 1
            self.player_left.total_time = 0
            self.player_left.level_up = False
        if self.player_right:
            self.player_right.game_status = 1
            self.player_right.total_time = 0
            self.player_right.level_up = False
        pass

    def ready(self, user):
        self.room_init()
        self.game_init()
        # print("进入ready")
        self.first_hand = user  # 设置先手
        self.who_choice = user  # 设置该谁下棋
        # print("先手为:", user.user_name)
        head = 'GAME /start \r\n'
        # content = {'GameStatus': 'ready'}
        content = {'GameStatus': 11}
        self.send_data(head, content, user)
        sleep(0.1)
        # 发送房间对战数据，将自己（房间对象）传入参数
        self.send_roominfo(self)

    def start(self, user):
        # 游戏开始后让悔棋状态变为0
        self.room_init()
        self.game_init()
        self.start_status = True
        print("游戏开始")
        self.send_roominfo(self)

    def get_enemy(self, user):
        '''获取对手，返回对象'''
        if user.user_status == 1:
            return self.player_right
        elif user.user_status == 2:
            return self.player_left
        else:
            return
        return

    def game(self, user, content):
        if not self.start_status:  # 游戏开始才能进行棋盘信息输入
            return
        x, y = content['GamePos']
        time_gap = content["UseTime"]
        # 判断下棋者是否该轮到自己
        if self.who_choice is user:
            self.who_choice = self.get_enemy(user)
            user.total_time += time_gap
            if user.game_status == 13:
                c = 'B'     # 黑棋black
            elif user.game_status == 12:
                c = 'W'     # 白棋white
            else:
                return
            # 执行落子，存储坐标和棋子颜色，有人赢棋返回棋子颜色，或和棋
            winner = self.game_do(x, y, c)
            if winner:
                count = 3   # 赢棋加3分
                if winner == 'A':       # 和棋
                    self.atie = True
                    count = 1   # 和棋时间少者加1分
                    if self.player_left.total_time > \
                            self.player_right.total_time:
                        self.winner = self.player_right
                    else:
                        self.winner = self.player_left
                elif winner == 'B':     # 黑棋赢
                    if self.player_left.game_status == 13:
                        self.winner = self.player_left
                    elif self.player_right.game_status == 13:
                        self.winner = self.player_right
                    else:
                        return
                elif winner == 'W':     # 白棋赢
                    if self.player_left.game_status == 12:
                        self.winner = self.player_left
                    elif self.player_right.game_status == 12:
                        self.winner = self.player_right
                    else:
                        return
                else:
                    return
                # 游戏结束处理
                self.over(count)
            else:
                self.send_roominfo(self)

    def over(self, count, exceptdeal=False):
        '''游戏结束处理函数'''

        # 保存积分等级等游戏数据
        if self.save_game_data(self.winner, count):
            print('赢者升级')
            self.winner.level_up = True
        if exceptdeal:
            self.save_game_data(self.user, 0)
        else:
            self.save_game_data(self.get_enemy(self.winner), 0)
        # 发送更新数据到客户端
        self.send_roominfo(self)
        self.send_loginlist()
        self.room_reset()       # 出现赢棋和棋，重置游戏状态

    def undo(self, user, content):
        # 游戏没开始，返回
        if not self.start_status:
            return
        undo_status = content['UndoStatus']
        enemy = self.get_enemy(user)
        if undo_status == 'request':
            # 设置房间悔棋状态
            self.undo_status = True
            head = 'GAME /undo \r\n'
            self.send_data(head, content, enemy)

        elif undo_status == 'yes':
            # 判断自己棋子颜色，如果为13黑棋，则白棋请求悔棋，否则，黑棋请求悔棋
            if user.game_status == 13:
                c = 'W'
            elif user.game_status == 12:
                c = 'B'
            else:
                return
            # 调用悔棋函数，传入悔棋棋子颜色
            self.game_undo(c)
            # 设置下棋者为请求者
            self.who_choice = enemy
            # 增加请求者时间20秒，作为惩罚
            enemy.total_time += 20
            # 设置房间悔棋状态
            self.undo_status = False
            # 发送房间游戏数据
            self.send_roominfo(self)

        elif undo_status == "no":
            head = 'GAME /undo \r\n'
            content = {'UndoStatus': 'no'}
            # 设置房间悔棋状态
            self.undo_status = False
            self.send_data(head, content, enemy)

    def giveup(self, user):
        if user.user_status not in (1, 2):
            return
        if user.game_status not in (12, 13):
            return
        self.winner = self.get_enemy(user)
        self.giveup_player = user
        head = 'GAME /giveup \r\n'
        content = {'GiveupPlayer': user.nickname}
        self.send_data(head, content, user)
        self.send_data(head, content, self.winner)
        # 初始化玩家状态
        user.game_status = 1
        user.total_time = 0
        user.level_up = False
        self.winner.game_status = 1
        self.winner.total_time = 0
        self.winner.level_up = False
        if user.e_quit:
            # 游戏结束处理，赢者增加积分3分
            self.over(3, exceptdeal=True)
        else:
            self.over(3)

    def except_deal(self, user):
        self.Log.append(get_time() + '用户退出' + user.user_name)
        self.deal_quit(user, self)
        pass

    def return_hall(self, user):
        print("退出房间函数")
        if user.user_status == 1:       # 左边玩家
            self.player_left = None
            if user.game_status in (12, 13):    # 游戏中
                self.giveup(user)
        elif user.user_status == 2:     # 右边玩家
            self.player_right = None
            if user.game_status in (12, 13):
                self.giveup(user)
        # 初始化玩家状态
        user.room_id = 0
        user.user_status = 0
        user.game_status = 1
        user.total_time = 0
        user.level_up = False
