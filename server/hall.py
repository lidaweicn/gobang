from time import sleep
from random import choice


class Hall:
    def fightin(self, content):
        self.room_id(content)
        pass

    def room_in(self, data):
        '''客户端点击对战进入房间'''

        print("此为进入房间函数")
        # 获取房间号
        roomid = int(data['RoomId'])
        room = self.AllRoom[roomid]
        user = self.LoginUser[data['UserName']]
        # 提取进入房间位置
        position = data['Position']
        print(data)

        if position == 4:   # 电脑对战
            user.user_status = 4
            user.room_id = roomid
        else:
            if position == 1:   # player1
                if room.player_left:
                    return
                user.user_status = 1
                user.room_id = roomid
                room.player_left = user
                # 发送进入房间所需数据
                # head = 'GOROOM /ok \r\n'
                # self.send_data(head, data)

            elif position == 2:
                if room.player_right:
                    return
                user.user_status = 2
                user.room_id = roomid
                room.player_right = user
                # 发送进入房间所需数据
                # head = 'GOROOM /ok \r\n'
                # self.send_data(head, data)
            elif position == 3:  # 区分观众进入正在对战中的房间
                user.user_status = 3
                user.room_id = roomid

            head = 'GOROOM /ok \r\n'
            self.send_data(head, data, user)

            self.send_hallinfo_toall()
            sleep(0.1)

            self.send_loginlist()
            sleep(0.1)
            # 发送房间信息给房间的人，传入房间对象
            self.send_roominfo(room)

    def challenge(self, content):
        chall_states = content['ChallengeStatus']
        user_name = content['UserName']
        enemy_name = content['EnemyName']
        # 获取对手user对象
        enemy = self.LoginUser[enemy_name]

        if chall_states == 'request':
            head = 'GOROOM /challenge \r\n'
            # 给对手发送对战消息
            self.send_data(head, content, enemy)

        elif chall_states == 'yes':
            if self.user.game_status not in [12, 13] and \
                    enemy.game_status not in [12, 13]:
                for roomid, room in self.AllRoom.items():
                    if roomid in (0, 999):
                        continue
                    if not room.player_left and not room.player_right:

                        myposition, enemyposition = choice([(1, 2), (2, 1)])
                        mycontent = {
                            'Position': myposition,
                            'UserName': user_name,
                            'RoomId': roomid,
                        }
                        enemycontent = {
                            'Position': enemyposition,
                            'UserName': enemy_name,
                            'RoomId': roomid,
                        }
                        self.room_in(mycontent)
                        self.room_in(enemycontent)
                        return
                else:
                    # 无空房间，创建新房间进入
                    pass

        elif chall_states == 'no':
            head = 'GOROOM /challenge \r\n'
            content['ChallengeStatus'] = 'no'
            # 给请求者返回拒绝消息
            self.send_data(head, content, enemy)

    def create_room(self):
        # 检查有没有全空的房间
        for room in self.AllRoom.values():
            if room.room_id in (0, 999):
                continue
            if not room.player_left and not room.player_right:
                head = "HALL /fail \r\n"
                content = {'ErrorMsg': '有空房间'}
                self.send_data(head, content)
                return
        else:
            n = len(self.AllRoom) - 1
            self.AllRoom[n] = Room(n, self.LoginUser, self.AllRoom, self.Log)
            self.send_hallinfo_toall()

    def fast_game(self, content):
        # print("进入fast_game")
        user_name = content['UserName']
        flag = 1
        for key, room in self.AllRoom.items():
            if key in (0, 999):
                continue
            if room.fast_num == 1:
                # print("优先级1")
                roomid = key
                if not room.player_left:
                    position = 1
                else:
                    position = 2
                break
        else:
            for key, room in self.AllRoom.items():
                if key in (0, 999):
                    continue
                if room.fast_num == 2:
                    # print("优先级2")
                    roomid = key
                    if not room.player_left:
                        position = 1
                    else:
                        position = 2
                    break
            else:
                for key, room in self.AllRoom.items():
                    if key in (0, 999):
                        continue
                    if room.fast_num == 3:
                        # print("优先级3")
                        roomid = key
                        if not room.player_left:
                            position = 1
                        else:
                            position = 2
                        break
                else:
                    flag = 0
                    # print("没有合适的房间")
        if flag == 1:
            # roomid = int(data['RoomId'])
            # user_name = data['UserName']  # 不用发用户昵称，该服务员只能接收到固定客户端的信息
            # position = data['Position']
            content = {
                'RoomId': roomid,
                'UserName': user_name,
                'Position': position,
            }
            # print("进入room之前", content)
            self.room_in(content)
        else:
            # print("没有合适的房间")
            head = 'GOROOM /fail \r\n'
            content = {
                'FailMsg': '没有符合条件的房间，请创建房间后再试'
            }
            # 给请求者返回拒绝消息
            self.send_data(head, content, self.user)
