from pymysql import connect
from random import choice
from config import DATABASE
import log


class DatabaseHandler(object):
    def open(self):
        self.conn = connect(charset="utf8", **DATABASE)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query_data(self, sql):
        self.open()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.close()
        return data

    def update_data(self, sql):
        self.open()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            raise Exception(e)
            print('数据库更新错误：', e)
        self.close()

    def check_user_login(self, uid):

        sql = "select * from userinfo where userid='%s';" % uid
        data = self.query_data(sql)
        if not data:
            return False
        print(data)     # data数据为元祖
        # (('aaa', '47bce5c74f589f4867dbd57e9ca9f808',
        # '哈哈哈', '1970-01-01', 0, 0,
        # './img/user/hawkeye.png', 0, 0),)
        # self.conn.commit()
        # self.close()
        print("ok,已从数据库中取出")
        user = {
            'UserName': data[0][0],
            'NickName': data[0][2],
            'GameScore': data[0][4],
            'GameLevel': data[0][5],
            'UserImage': data[0][6],
            'TotalRound': data[0][7],
            'WinRound': data[0][8],
        }
        passwd = data[0][1]
        return user, passwd

    def check_user_register(self, uid, nick):
        # 查询用户名
        sql = "select * from userinfo where userid='%s';" % uid
        data = self.query_data(sql)
        if data:
            return 'error', '用户名已存在'
        # 查询昵称
        sql = "select * from userinfo where username='%s';" % nick
        data = self.query_data(sql)
        if data:
            return 'error', '昵称已存在'
        return 'ok', '注册查询成功'

    def user_register(self, **user):
        user_image = choice(['img/user/boy.png', 'img/user/girl.png'])

        sql = "insert into userinfo(userid,passwd,username,birthday,userimg)\
            values('%s','%s','%s','%s','%s');"\
            % (user['UserName'],
               user['Password'],
               user['NickName'],
               user['Birthdate'],
               user_image)
        try:
            self.update_data(sql)
            return 'ok', '注册成功'
        except Exception as e:
            return 'error', e

    def get_user_info(self, uid):
        sql = "select * from userinfo where userid='%s';" % uid
        data = self.query_data(sql)
        if not data:
            return False
        user = {
            'UserName': data[0][0],
            'NickName': data[0][2],
            'GameScore': data[0][4],
            'GameLevel': data[0][5],
            'UserImage': data[0][6],
            'TotalRound': data[0][7],
            'WinRound': data[0][8],
        }
        return user

    def save_game_info(self, uid, integral, rank, total, winround):
        sql = "update userinfo set integral=integral+%d,\
            rank=rank+%d,total=total+%d,winround=winround+%d \
            where userid='%s'" % (integral, rank, total, winround, uid)
        try:
            self.update_data(sql)
            log_str = '保存游戏数据:' + '-'.join(
                (uid, str(integral), str(rank), str(total), str(winround)))
            log.logging.info(log_str)
        except Exception as e:
            log.logging.error(e)
            return 'error', e

    def modify_userinfo(self, field, uid, content, passwd=''):
        if field == 'passwd' and not passwd:
            sql = 'select userid from userinfo where \
                   uid="{}" and passwd="{}"'.format(uid, passwd)
            if not self.query_data(sql):
                return 'error', '原密码不正确'
        sql = 'update userinfo set {}="{}" where userid="{}"'\
            .format(field, content, uid)

        try:
            self.update_data(sql)
            log_str = '修改用户数据:' + '-'.join(
                (field, uid, content, passwd))
            log.logging.info(log_str)
            return 'ok', '修改成功'
        except Exception as e:
            log.logging.error(e)
            # print(e)
            return 'error', e
        pass









    # def update_to_mysql(self, sql):
    #     self.open()
    #     self.cursor.execute(sql)
    #     self.conn.commit()
    #     self.close()
    #     print("ok,已存入数据库")

    # def save_to_mysql(self, sql):
    #     self.open()
    #     self.cursor.execute(sql)
    #     self.conn.commit()
    #     self.close()
    #     print("ok,已存入数据库")

    # def get_from_mysql(self, sql):
    #     # order1 = "select * from userinfo"
    #     self.open()
    #     self.cursor.execute(sql)
    #     data = self.cursor.fetchall()
    #     self.conn.commit()
    #     self.close()
    #     print("ok,已从数据库中取出")
    #     return data

    # def getone_from_mysql(self, one, flag):
    #     if flag == 2:
    #         order = "select * from userinfo where username='%s';" % one
    #     elif flag == 1:
    #         order = "select * from userinfo where userid='%s';" % one
    #     self.open()
    #     self.cursor.execute(order)
    #     data = self.cursor.fetchall()
    #     self.conn.commit()
    #     self.close()
    #     print("ok,已从数据库中取出")
    #     return data

    # def getall_from_mysql(self, one):
    #     # if type(one) == str:
    #     #     order = "select * from userinfo where username='%s';" % one
    #     # elif type(one) == int:
    #     order = "select * from userinfo where userid='%s';" % one
    #     self.open()
    #     self.cursor.execute(order)
    #     data = self.cursor.fetchall()
    #     self.conn.commit()
    #     self.close()
    #     print("ok,已从数据库中取出")
    #     return data

    # def saveall_to_mysql(self, uid, passwd, name, birthday):
    #     self.open()
    #     order = "insert into userinfo(userid,passwd,username,birthday) \
    #     values('%s','%s','%s','%s');" % (uid, passwd, name, birthday)
    #     self.cursor.execute(order)
    #     self.conn.commit()
    #     self.close()
    #     print("ok,已存入数据库")

    # def updateone_to_mysql(self, one, one_value, user_name):
    #     order = "update userinfo set %s='%s' where userid='%s'" % (
    #         one, one_value, user_name)
    #     self.open()
    #     self.cursor.execute(order)
    #     self.conn.commit()
    #     self.close()

    # # def update_rankinteg(self):
    # #     order = "update userinfo set %s=%d,%s=%d where userid='%s'" % (one,one_value,user_name)
    # #     self.open()
    # #     self.cursor.execute(order)
    # #     self.conn.commit()
    # #     self.close()

    # def update_userinfo(self, user_name, LoginUser):
    #     # name = LoginUser[user_name]
    #     user_info = (user_name, LoginUser[user_name].password, LoginUser[user_name].nickname,
    #                  LoginUser[user_name].birthday, LoginUser[user_name].game_integral,
    #                  LoginUser[user_name].game_level, LoginUser[user_name].user_img, user_name)
    #     order = "update userinfo set userid='%s',passwd='%s',username='%s',\
    #             birthday='%s',integral=%d,rank=%d,userimg='%s' where userid='%s';" % user_info
    #     self.open()
    #     self.cursor.execute(order)
    #     self.conn.commit()
    #     self.close()
    #     print("数据已更新完毕")
