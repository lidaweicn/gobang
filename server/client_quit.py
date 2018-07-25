from common import get_time


class ExceptQuit:
    ''' 此模块用来处理异常退出重置相应状态'''

    def deal_quit(self, user, room):
        print("进入处理异常函数")
        if user.user_name == '':  # 未登录的人退出，初始化时为空
            print("未登录的人退出")
            return

        if not user.e_quit:
            return

        if room.room_id not in (0, 999):
            room.return_hall(user)
        del self.LoginUser[user.user_name]
        user.e_quit = False
        self.send_hallinfo_toall()
        self.send_loginlist()
        self.send_roominfo(room)
