from json import loads
from user import User
from time import sleep
from config import *
from send_data import SendData
from database import DatabaseHandler
from hall import Hall
from client_quit import ExceptQuit
import struct
import log


class ClientHandler(ExceptQuit, Hall, SendData, DatabaseHandler):

    def __init__(self, connfd, LoginUser, AllRoom, Log):
        self.connfd = connfd
        self.client_name = ""
        self.user = User()
        self.user.connfd = connfd
        self.LoginUser = LoginUser  # 用大驼峰表示登录的用户
        self.AllRoom = AllRoom
        self.Log = Log
        # self.Fight = Fight

        # MysqlDeal.__init__(self, DATABASE)

    def data_recv(self):
        dataBuffer = bytes()
        headerSize = 4

        while True:
            try:
                data = self.connfd.recv(1024)
                print("收到消息:", data)  # 用于测试
            except ConnectionResetError:
                self.user.e_quit = True
                self.except_deal(self.user)
                print("客户端退出")
                break

            if not data:
                self.user.e_quit = True
                self.except_deal(self.user)
                return

            if data:
                # 把数据存入缓冲区，类似于push数据
                dataBuffer += data
                while True:
                    if len(dataBuffer) < headerSize:
                        print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                        break

                    # 读取包头
                    # struct中:!代表Network order，3I代表3个unsigned int数据
                    headPack = struct.unpack('!I', dataBuffer[:headerSize])
                    bodySize = headPack[0]

                    # 分包情况处理，跳出函数继续接收数据
                    if len(dataBuffer) < headerSize + bodySize:
                        print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" %
                              (len(dataBuffer), headerSize + bodySize))
                        break
                    # 读取消息正文的内容
                    body = dataBuffer[headerSize:headerSize + bodySize]

                    # 数据处理
                    # self.dataHandle(headPack, body)
                    self.dataHandle(body)

                    # 粘包情况的处理
                    # 获取下一个数据包，类似于把数据pop出
                    dataBuffer = dataBuffer[headerSize + bodySize:]

    # --------------------------------------------------------
    def dataHandle(self, body):
        '''数据分发函数'''
        data = body.decode()
        order_data = data.split('\r\n')
        head = order_data[0]
        heads = head.split()
        action = heads[0]
        action_vice = heads[1]
        content = order_data[1]
        content_dict = loads(content)
        user_info = loads(content)

        if action == "CHAT":
            if action_vice == '/hall':
                room_id = 0
            else:
                room_id = int(action_vice[1:])
            self.chat_handler(room_id, head, content_dict)
        elif action == "LOGIN":
            self.login(content_dict)
        elif action == "REGISTER":
            self.register(content_dict)
        elif action == 'GOROOM':
            # print("roomid:", self.LoginUser[self.client_name].room_id)
            # print("进入６６６６６６")
            if action_vice == '/fast':
                self.fast_game(content_dict)
            elif action_vice == '/inroom':
                # self.fightin(content)
                self.room_in(content_dict)
            elif action_vice == '/challenge':
                self.challenge(content_dict)
            else:
                self.room_in(content_dict)  # 用来初始化进入房间后的状态

        elif action == 'MODIFY':
            print("进入modify")
            if action_vice == '/image':
                self.modify_image(user_info)
                pass
            elif action_vice == '/nick':
                self.modify_nickname(user_info)
                pass
            elif action_vice == '/password':
                self.modify_password(user_info)
        elif action == "GAME":
            self.game_handler(action_vice, content_dict)
        elif action == "HALL":
            if action_vice == '/create':
                self.create_room()

        elif action == "LIST":
            # 接收用户信息列表，分发到界面
            print('用户列表')
            pass
        else:
            print('接收数据错误')
            pass

    def game_handler(self, action_vice, content):
        # 获取用户所在的房间对象
        room = self.AllRoom[self.user.room_id]
        # 判断副命令
        if action_vice == "/ready":
            pass
        elif action_vice == "/start":
            if self.user.user_status == 1:  # player1
                if room.player_right:
                    room.fast_num = 9   # 设置优先级最低
                    if room.player_right.game_status == 11:
                        self.user.game_status = 12
                        room.player_right.game_status = 13
                        room.start(self.user)
                        return
                else:
                    room.fast_num = 1   # 设置优先级最高
                self.user.game_status = 11
                room.ready(self.user)
            elif self.user.user_status == 2:    # player2
                if room.player_left:
                    room.fast_num = 9   # 设置优先级最低
                    if room.player_left.game_status == 11:
                        self.user.game_status = 12
                        room.player_left.game_status = 13
                        room.start(self.user)
                        return
                else:
                    room.fast_num = 1   # 设置优先级最高
                self.user.game_status = 11
                room.ready(self.user)
            else:
                pass
        elif action_vice == "/game":
            if self.user.user_status in (1, 2) and not room.undo_status:
                room.game(self.user, content)
        elif action_vice == "/undo":
            if self.user.user_status in (1, 2):
                room.undo(self.user, content)
        elif action_vice == "/giveup":
            if self.user.user_status in (1, 2):
                room.giveup(self.user)
        elif action_vice == 'fightin':  # 观众进入对战席
            self.fightin(self.user, content)
        elif action_vice == '/returnhall':
            if self.user.room_id == 999:
                self.user.room_id = 0
                self.user.user_status = 0
                self.send_hallinfo()    # 发送大厅给客户端
            else:
                room.return_hall(self.user)
                self.send_roominfo(room)
                self.send_hallinfo_toall()    # 发送大厅给大厅的人
            sleep(0.1)
            self.send_loginlist()   # 发送登录列表给所有人
        else:
            print('接收数据错误')
            log.logging.error('数据接收错误')
        pass

    def chat_handler(self, roomid, head, data):
        message = data['Message']
        head = head + '\r\n'
        print(head)
        if not message:
            return
        if message[0] == '@':
            message_list = message.split()
            atname = message_list[0][1:]
            print(atname)
            for key, user in self.LoginUser.items():
                if user.nickname == atname:
                    print(user.nickname)
                    self.send_data(head, data, user)
                    return

        for key, user in self.LoginUser.items():
            if user.room_id == roomid and user is not self.user:
                self.send_data(head, data, user)

    def register(self, data):
        uid = data['UserName']
        nick = data['NickName']
        # 检测用户和昵称是否存在，返回元组(状态码,信息)
        status, msg = self.check_user_register(uid, nick)
        head = "REGISTER /fail \r\n"
        # 判断注册，并发送消息
        if status == 'error':
            content = {'ErrorMsg': msg}
            self.send_data(head, content)
        elif status == 'ok':
            status, msg = self.user_register(**data)
            if status == 'error':
                content = {'ErrorMsg': msg}
            elif status == 'ok':
                head = "REGISTER /ok \r\n"
                content = {'OkMsg': msg}
                # self.Log.append(get_time() + '用户注册' + uid + nick)
                log.logging.info('用户注册:' + uid + '-' + nick)
            self.send_data(head, content)
        else:
            pass

    def login(self, data):
        uid = data['UserName']
        passwd = data['Password']
        # 检测是否已经登录
        for username in self.LoginUser:
            if username == uid:
                head = "LOGIN /fail \r\n"
                content = {'ErrorMsg': '用户已登录'}
                self.send_data(head, content)
                return
        # 数据库查询用户
        query_user = self.check_user_login(uid)     # 成功返回数据为元组
        if not query_user:  # 用户名不存在
            head = "LOGIN /fail \r\n"
            content = {'ErrorMsg': '用户名不存在'}
            self.send_data(head, content)
            return False
        else:
            user, pwd = query_user
            if pwd != passwd:   # 密码错误
                head = "LOGIN /fail \r\n"
                content = {'ErrorMsg': '密码错误'}
                self.send_data(head, content)
                return False
            else:
                # 给client_name赋值
                # self.client_name = uid
                # 将用户根据数据库内容进行初始化
                self.user.init(user)
                # 保存用户对象到在线用户
                self.LoginUser[user['UserName']] = self.user

                # 发送用户相关信息给客户端
                self.send_userinfo(user)
                sleep(0.1)
                # 发送大厅信息给客户端
                self.send_hallinfo()
                sleep(0.1)
                # 发送已登录的成员列表给所有人
                self.send_loginlist()
                sleep(0.1)
                # self.Log.append(get_time() + '用户登录' + uid)
                log.logging.info('用户登录:' + uid)
                return True

    def except_deal(self, user):
        # self.Log.append(get_time() + '用户退出' + user.user_name)
        log.logging.info('用户退出:' + user.user_name)
        room = self.AllRoom[user.room_id]
        self.deal_quit(user, room)
        pass

    def modify_image(self, content):
        user_name = content["UserName"]
        image = content["UserImage"]
        # 调用数据库函数修改信息
        status, msg = self.modify_userinfo('userimg', user_name, image)
        if status == 'ok':
            # 调用数据库函数获取修改后的用户信息
            user_info = self.get_user_info(user_name)
            # 发送个人信息到客户端
            self.send_userinfo(user_info)
            # 更新user对象
            self.user.user_img = image
            log.logging.info('用户修改头像:' + user_name)
        # 发送信息
        head = 'MODIFY /image \r\n'
        content = {'CheckMassage': msg}
        self.send_data(head, content)

    def modify_nickname(self, content):
        user_name = content["UserName"]
        nickname = content["NickName"]
        # 调用数据库函数修改信息
        status, msg = self.modify_userinfo('username', user_name, nickname)
        if status == 'ok':
            # 调用数据库函数获取修改后的用户信息
            user_info = self.get_user_info(user_name)
            # 发送个人信息到客户端
            self.send_userinfo(user_info)
            # 发送已登录的成员列表给所有人
            self.send_loginlist()
            # 更新user对象
            self.user.nickname = nickname
            log.logging.info('用户修改昵称:' + user_name + '-' + nickname)
        # 发送信息
        head = 'MODIFY /nick \r\n'
        content = {'CheckMassage': msg}
        self.send_data(head, content)
       

    def modify_password(self, content):
        user_name = content["UserName"]
        old_password = content['OldPassword']
        new_password = content['NewPassword']
        status, msg = self.modify_userinfo('passwd', user_name, new_password,
                                           passwd=old_password)
        # 发送信息
        head = 'MODIFY /password \r\n'
        content = {'CheckMassage': msg}
        self.send_data(head, content)
        log.logging.info('用户修改密码:' + user_name)
