# from database import DatabaseHandler
# from send_data import SendData
# # from time import sleep
# import log


class User:
    def __init__(self):
        self.user_name = ''
        self.room_id = 0
        self.e_quit = False
        pass

    def init(self, content):
        self.user_name = content['UserName']
        self.nickname = content['NickName']
        self.game_level = content['GameLevel']
        self.game_integral = content['GameScore']
        self.user_img = content['UserImage']
        self.total_num = content['TotalRound']
        self.win_num = content['WinRound']

        self.user_status = 0    # 用户状态，对战1左,2右，观战3
        self.game_status = 0    # 游戏状态，11准备，12白棋，13黑棋
        self.total_time = 0
        self.level_up = False

    # def register(self, data):
    #     uid = data['UserName']
    #     nick = data['NickName']
    #     # 检测用户和昵称是否存在，返回元组(状态码,信息)
    #     status, msg = self.check_user_register(uid, nick)
    #     head = "REGISTER /fail \r\n"
    #     # 判断注册，并发送消息
    #     if status == 'error':
    #         content = {'ErrorMsg': msg}
    #         self.send_data(head, content)
    #     elif status == 'ok':
    #         status, msg = self.user_register(**data)
    #         if status == 'error':
    #             content = {'ErrorMsg': msg}
    #         elif status == 'ok':
    #             head = "REGISTER /ok \r\n"
    #             content = {'OkMsg': msg}
    #             # self.Log.append(get_time() + '用户注册' + uid + nick)
    #             log.logging.info('用户注册:' + uid + '-' + nick)
    #         self.send_data(head, content)
    #     else:
    #         pass

    # def login(self, data):
    #     uid = data['UserName']
    #     passwd = data['Password']

    #     # 数据库查询用户
    #     query_user = self.check_user_login(uid)     # 成功返回数据为元组
    #     if not query_user:  # 用户名不存在
    #         head = "LOGIN /fail \r\n"
    #         content = {'ErrorMsg': '用户名不存在'}
    #         self.send_data(head, content)
    #         return False
    #     else:
    #         user, pwd = query_user
    #         if pwd != passwd:   # 密码错误
    #             head = "LOGIN /fail \r\n"
    #             content = {'ErrorMsg': '密码错误'}
    #             self.send_data(head, content)
    #             return False
    #         else:
    #             # 给client_name赋值
    #             # self.client_name = uid
    #             # 将用户根据数据库内容进行初始化
    #             # self.user.init(user)
    #             # # 保存用户对象到在线用户
    #             # self.LoginUser[user['UserName']] = self.user

                
    #             # self.Log.append(get_time() + '用户登录' + uid)
    #             log.logging.info('用户登录:' + uid)
    #             return True

    # def modify_image(self, content):
    #     user_name = content["UserName"]
    #     image = content["UserImage"]
    #     # 调用数据库函数修改信息
    #     status, msg = self.modify_userinfo('userimg', user_name, image)
    #     if status == 'ok':
    #         # 调用数据库函数获取修改后的用户信息
    #         user_info = self.get_user_info(user_name)
    #         # 发送个人信息到客户端
    #         self.send_userinfo(user_info)
    #         # 更新user对象
    #         self.user.user_img = image
    #         log.logging.info('用户修改头像:' + user_name)
    #     # 发送信息
    #     head = 'MODIFY /image \r\n'
    #     content = {'CheckMassage': msg}
    #     self.send_data(head, content)

    # def modify_nickname(self, content):
    #     user_name = content["UserName"]
    #     nickname = content["NickName"]
    #     # 调用数据库函数修改信息
    #     status, msg = self.modify_userinfo('username', user_name, nickname)
    #     if status == 'ok':
    #         # 调用数据库函数获取修改后的用户信息
    #         user_info = self.get_user_info(user_name)
    #         # 发送个人信息到客户端
    #         self.send_userinfo(user_info)
    #         # 更新user对象
    #         self.user.nickname = nickname
    #         log.logging.info('用户修改昵称:' + user_name + '-' + nickname)
    #     # 发送信息
    #     head = 'MODIFY /nick \r\n'
    #     content = {'CheckMassage': msg}
    #     self.send_data(head, content)

    # def modify_password(self, content):
    #     user_name = content["UserName"]
    #     old_password = content['OldPassword']
    #     new_password = content['NewPassword']
    #     status, msg = self.modify_userinfo('passwd', user_name, new_password,
    #                                        passwd=old_password)
    #     # 发送信息
    #     head = 'MODIFY /password \r\n'
    #     content = {'CheckMassage': msg}
    #     self.send_data(head, content)
    #     log.logging.info('用户修改密码:' + user_name)
