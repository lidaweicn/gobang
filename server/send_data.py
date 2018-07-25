from json import dumps
from struct import pack
import log


class SendData:
    def send_data(self, head, content, user=None):
        # 将命令行和数据内容（字典转json字符串）封装为消息体
        msg_body = head + dumps(content)
        # 消息头，包含消息体数据长度
        header = msg_body.__len__()
        headPack = pack("!I", header)
        # 数据包，消息头+消息体
        sendData = headPack + msg_body.encode('utf8')
        try:
            user = user if user else self.user
        except Exception as e:
            try:
                user = user if user else self
            except Exception as e:
                print(e)
                log.logging.error(e)
            print(e)
            log.logging.error(e)
        # print(user, self.user)
        try:
            user.connfd.send(sendData)
        except BrokenPipeError:
            print("客户端断开产生异常")
            if not user.e_quit:
                self.except_deal(user)

    def send_userinfo(self, content):
        # 登录时发送自己的相关信息
        head = "LOGIN /ok \r\n"
        self.send_data(head, content)

    def send_hallinfo(self):
        # 客户端登录发送大厅信息
        content = self.get_roomsinfo()
        head = "HALL / \r\n"
        self.send_data(head, content)

    def send_hallinfo_toall(self):
        # 发送大厅信息给所有人
        content = self.get_roomsinfo()
        head = "HALL / \r\n"
        # 给所有人发送
        users = self.LoginUser.copy()
        print(users)
        for key, user in users.items():
            if user.room_id == 0:
                self.send_data(head, content, user)

    def get_roomsinfo(self):
        '''获取所有房间信息（对战双方昵称和头像），用于显示大厅'''
        rooms = {}
        for room in self.AllRoom.values():
            if room.room_id in (0, 999):
                continue
            if room.player_left:
                left_player_image = room.player_left.user_img
                left_player = room.player_left.nickname
            else:
                left_player_image = ''
                left_player = ''

            if room.player_right:
                right_player_image = room.player_right.user_img
                right_player = room.player_right.nickname
            else:
                right_player_image = ''
                right_player = ''

            room_info = {
                'RoomId': room.room_id,
                'LeftPlayer': left_player,
                'RightPlayer': right_player,
                'LeftPlayerImage': left_player_image,
                'RightPlayerImage': right_player_image,
            }
            rooms[room.room_id] = room_info
        return rooms

    def get_userlist(self):
        get_users = {}
        users = self.LoginUser.copy()
        for user in users.values():
            user_info = {
                'UserName': user.user_name,
                'NickName': user.nickname,
                'GameLevel': user.game_level,
                'GameScore': user.game_integral,
                'UserImage': user.user_img,
                'RoomId': user.room_id,
                'UserStatus': user.user_status,
                'TotalRound': user.total_num,
                'WinRound': user.game_integral,
            }
            get_users[user.user_name] = user_info
        return get_users

    def send_loginlist(self):
        # 发送已登录的成员列表，用于刷新大厅列表，发给所有客户端
        head = "LIST / \r\n"
        content = self.get_userlist()
        # 给所有人发送
        users = self.LoginUser.copy()
        for user in users.values():
            self.send_data(head, content, user)

    def send_roominfo(self, room):
        # 提取用户信息
        if room.player_left:
            left_player = room.player_left.user_name
            left_player_nickname = room.player_left.nickname
            left_player_image = room.player_left.user_img
            left_player_status = room.player_left.game_status
            total_time_left = room.player_left.total_time
            level_up_left = room.player_left.level_up
        else:
            left_player = ''
            left_player_nickname = ''
            left_player_image = ''
            left_player_status = 0
            total_time_left = 0
            level_up_left = False

        if room.player_right:
            right_player = room.player_right.user_name
            right_player_nickname = room.player_right.nickname
            right_player_image = room.player_right.user_img
            right_player_status = room.player_right.game_status
            total_time_right = room.player_right.total_time
            level_up_right = room.player_right.level_up
        else:
            right_player = ''
            right_player_nickname = ''
            right_player_image = ''
            right_player_status = 0
            total_time_right = 0
            level_up_right = False
        if room.who_choice:
            who_choice = room.who_choice.user_name
        else:
            who_choice = ''
        if room.winner:
            winner = room.winner.nickname
        else:
            winner = ''
        if room.giveup_player:
            giveup_player = room.giveup_player.nickname
        else:
            giveup_player = ''
        # 封装房间游戏信息
        room_info = {
            'Room': room.room_id,
            'LeftPlayer': left_player,
            'RightPlayer': right_player,
            'LeftPlayerNick': left_player_nickname,
            'RightPlayerNick': right_player_nickname,
            'LeftPlayerImage': left_player_image,
            'RightPlayerImage': right_player_image,
            'GogangInfo': room.gobang_map,
            'LeftPlayerStatus': left_player_status,
            'RightPlayerStatus': right_player_status,
            'Winner': winner,
            'GiveupPlayer': giveup_player,
            'TotalTimeLeft': total_time_left,
            'TotalTimeRight': total_time_right,
            'TimerStart': who_choice,
            'ATie': room.atie,
            'LevelUpLeft': level_up_left,
            'LevelUpRight': level_up_right,
        }

        head = 'GAME /info \r\n'

        users = self.LoginUser.copy()
        for user in users.values():
            if user.room_id == room.room_id:
                self.send_data(head, room_info, user)





    # def send_myinfo(self, database):
    #     content = {
    #         'UserName': self.client_name,
    #         # 'Password': passwd,
    #         'UserImage': database[0][6],
    #         'NickName': database[0][2],
    #         'GameLevel': database[0][5],
    #         'GameScore': database[0][4],
    #         'WinRound': database[0][8],
    #         'TotalRound': database[0][7],
    #         # 'CheckMassage':''
    #     }
    #     self.send_userinfo(content)




    # def send_roominfo2(self):
    #     # 给自己发送房间信息
    #     head = "HALL / \r\n"
    #     room_dic = {}
    #     # print(AllRoom)

    #     for room in self.AllRoom.values():
    #         if room.table_left == '':
    #             left_player_image = ''
    #             left_player = ''
    #         else:
    #             left_player_image = self.LoginUser[room.table_left].user_img
    #             left_player = self.LoginUser[room.table_left].nickname

    #         if room.table_right == '':
    #             right_player_image = ''
    #             right_player = ''

    #         else:
    #             right_player_image = self.LoginUser[room.table_right].user_img
    #             right_player = self.LoginUser[room.table_right].nickname

    #         room_info = {
    #             'Room': room.room_id,
    #             'LeftPlayer': left_player,
    #             'RightPlayer': right_player,
    #             'LeftPlayerImage': left_player_image,
    #             'RightPlayerImage': right_player_image,

    #         }
    #         room_dic[room.room_id] = room_info

    #     msg = head + dumps(room_dic)
    #     # print("发送的房间信息:",msg)
    #     # connfd.send(msg.encode())
    #     self.send_msg(self.client_name, self.LoginUser, msg)
    #     # try:
    #     #     self.connfd.send(msg.encode())
    #     # except BrokenPipeError:
    #     #     self.deal_quit(self.client_name)

    # def send_roominfo_toall(self):
    #     # 给已登录的所有人发送房间信息,用来刷新大厅房间信息
    #     head = "HALL / \r\n"
    #     room_dic = {}
    #     # print(AllRoom)
    #     for room in self.AllRoom.values():
    #         # print(room.table_left)
    #         if room.table_left == '':
    #             left_player_image = ''
    #             left_player = ''
    #         else:
    #             left_player_image = self.LoginUser[room.table_left].user_img
    #             left_player = self.LoginUser[room.table_left].nickname

    #         if room.table_right == '':
    #             right_player_image = ''
    #             right_player = ''

    #         else:
    #             right_player_image = self.LoginUser[room.table_right].user_img
    #             right_player = self.LoginUser[room.table_right].nickname

    #         room_info = {
    #             'Room': room.room_id,
    #             'LeftPlayer': left_player,
    #             'RightPlayer': right_player,
    #             'LeftPlayerImage': left_player_image,
    #             'RightPlayerImage': right_player_image,

    #         }
    #         room_dic[room.room_id] = room_info

    #     msg = head + dumps(room_dic)
    #     # for key, user in self.LoginUser.items():
    #     #     if user.e_quit == 1:
    #     #         del self.LoginUser[key]
    #     # if self.LoginUser[user_name].e_quit == 1:
    #     #     del self.LoginUser[user_name]

    #     users = self.LoginUser.copy()
    #     for key, user in users.items():
    #         self.send_msg(key, self.LoginUser, msg)
    #         # if user.user_name != client_name:
    #         # try:
    #         #     user.connfd.send(msg.encode())
    #         # except BrokenPipeError:
    #         #     if user.e_quit == 1:
    #         #         continue
    #         #     else:
    #         #         self.deal_quit(key)
    #         # deal_exceptquit(user.user_name,self.LoginUser)
    #         # db.update_userinfo(user.user_name,self.LoginUser)
    #         # del self.LoginUser[key]
    #         # print(key,"用户非正常退出")

    # def init_loginfo(self, database):
    #     # 初始化登录的用户信息
    #     user_info = {
    #         'UserName': database[0][0],
    #         'Password': database[0][1],
    #         'NickName': database[0][2],
    #         'Birthdate': database[0][3],
    #         'GameScore': database[0][4],
    #         'GameLevel': database[0][5],
    #         'UserImage': database[0][6],
    #         'TotalRound': database[0][7],
    #         'WinRound': database[0][8],
    #     }
    #     user_name = database[0][0]
    #     user = User(user_info, self.connfd)
    #     self.LoginUser[user_name] = user

    # def send_loginlist(self):
    #     # 发送已登录的成员列表，用于刷新大厅列表
    #     head = "LIST / \r\n"
    #     dic = {}

    #     users = self.LoginUser.copy()
    #     for user in users.values():
    #         if user.e_quit == 1:
    #             continue
    #         user_info = {
    #             'UserName': user.user_name,
    #             # 'Password': user.password,
    #             'NickName': user.nickname,
    #             # 'Birthdate': database[0][3],
    #             'GameLevel': user.game_level,
    #             'GameScore': user.game_integral,
    #             'UserImage': user.user_img,
    #             'RoomId': user.room_id,
    #             'UserStatus': user.user_status,
    #             'TotalRound': user.total_num,
    #             'WinRound': user.game_integral,
    #         }
    #         dic[user.user_name] = user_info

    #     msg_all = head + dumps(dic)
    #     print(msg_all)

    #     for key, user in users.items():
    #         # if user.user_name != client_name:
    #         self.send_msg(key, self.LoginUser, msg_all)
    #         # try:
    #         #     user.connfd.send(msg_all.encode())
    #         # except BrokenPipeError:
    #         #     if user.e_quit == 1:  # 是异常退出时调用该函数,e_quit==1表示正在调用过deal_quit
    #         #         continue
    #         #     else:
    #         #         self.deal_quit(key)

    # def sendtoruser_roominfo(self, roomid):
    #     if self.AllRoom[roomid].table_left == '':
    #         left_player = ''
    #         left_player_nickname = ''
    #         left_player_image = ''
    #         # go_type = [[0 for x in range(15)] for y in range(15)]
    #         left_player_status = 0
    #         total_time_left = 0
    #         level_up_left = 0

    #     else:
    #         name = self.AllRoom[roomid].table_left
    #         left_player = name
    #         left_player_nickname = self.LoginUser[name].nickname
    #         left_player_image = self.LoginUser[name].user_img
    #         left_player_status = self.LoginUser[name].user_status
    #         total_time_left = self.LoginUser[name].total_time
    #         level_up_left = self.LoginUser[name].level_up

    #     if self.AllRoom[roomid].table_right == '':
    #         right_player = ''
    #         right_player_nickname = ''
    #         right_player_image = ''
    #         # go_type = [[0 for x in range(15)] for y in range(15)]
    #         right_player_status = 0
    #         total_time_right = 0
    #         level_up_right = 0
    #     else:
    #         name = self.AllRoom[roomid].table_right
    #         right_player = name
    #         right_player_nickname = self.LoginUser[name].nickname
    #         right_player_image = self.LoginUser[name].user_img
    #         right_player_status = self.LoginUser[name].user_status
    #         total_time_right = self.LoginUser[name].total_time
    #         level_up_right = self.LoginUser[name].level_up

    #     room_info = {
    #         'Room': self.AllRoom[roomid].room_id,
    #         'LeftPlayer': left_player,
    #         'RightPlayer': right_player,
    #         'LeftPlayerNick': left_player_nickname,
    #         'RightPlayerNick': right_player_nickname,
    #         'LeftPlayerImage': left_player_image,
    #         'RightPlayerImage': right_player_image,
    #         'GogangInfo': self.Fight[roomid]['go_type'],
    #         'LeftPlayerStatus': left_player_status,
    #         'RightPlayerStatus': right_player_status,
    #         'Winner': self.AllRoom[roomid].winner,
    #         'GiveupPlayer': self.AllRoom[roomid].giveup_player,
    #         'TotalTimeLeft': total_time_left,
    #         'TotalTimeRight': total_time_right,
    #         'TimerStart': self.AllRoom[roomid].who_choice,
    #         'ATie': self.AllRoom[roomid].atie,
    #         'LevelUpLeft': level_up_left,
    #         'LevelUpRight': level_up_right,
    #     }

    #     head = 'GAME /info \r\n'

    #     msg = head + dumps(room_info)
    #     # roomid = self.LoginUser[self.client_name].room_id
    #     user = [self.AllRoom[roomid].table_left, self.AllRoom[roomid].table_right] \
    #         + self.AllRoom[roomid].audience
    #     print("观众:", self.AllRoom[roomid].audience)
    #     for x in user:
    #         if x != '':
    #             self.send_msg(x, self.LoginUser, msg)
    #             # 下边进行是否是从观众席进入对战席的判断
    #             # if (x in self.AllRoom[roomid].audience) and (x not in self.LoginUser):
    #             #     self.AllRoom[roomid].audience.remove(x)
                    
    #             #     print("删除后观众:", self.AllRoom[roomid].audience)
    #             #     continue
    #             # try:
    #             #     self.LoginUser[x].connfd.send(msg.encode())
    #             # except BrokenPipeError:
    #             #     if self.LoginUser[x].e_quit == 1:
    #             #         continue
    #             #     else:
    #             #         self.deal_quit(x)
