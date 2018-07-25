from PyQt5.QtCore import pyqtSlot
from hashlib import md5
from json import dumps, loads
from struct import pack, unpack
from py.common import *
from py.datatransfer import DataTransfer


class LoginFunction(DataTransfer):
    def send_data(self, head, content):
        # 封装数据到消息体
        msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
        print(msg_send)
        # 发送登录数据到服务器
        self.sockfd.send(msg_send.encode())
        pass

    @pyqtSlot()
    def on_loginBtn_clicked(self):
        '''登录按钮点击事件，只执行向服务器发送数据'''

        # 判断是否连接网络
        if self.net_status == DISCONNECT:
            print("网络未连接")
            self.loginInfo.setText('网络错误，无法连接服务器！')
            return

        # 获取界面输入框数据
        self.user_name = self.loginUserName.text()
        if not self.user_name:
            self.loginInfo.setText('请输入用户名！')
            return
        user_pwd = self.loginUserPwd.text()
        if not user_pwd:
            self.loginInfo.setText('请输入密码！')
            return
        # 判断密码框输入的数据是否为记住的密码，如果不是，重新MD5加密
        if self.user_pwd_md5 != user_pwd:
            # 将密码用MD5加密
            self.user_pwd_md5 = md5(user_pwd.encode()).hexdigest()
        print(self.user_pwd_md5)

        print('登录发送数据')
        # 将发送的数据封装在head和content变量中
        head = "LOGIN / \r\n"      # 命令行参数
        # 发送的数据内容，封装为字典
        content = {
            'UserName': self.user_name,
            'Password': self.user_pwd_md5,
            # 以下数据测试用，模拟服务器返回信息
            # 'NickName': "哈哈哈哈",
            # 'UserImage': 'img/user/01.png',
            # 'GameLevel': 5,
            # 'GameScore': 534,
        }
        print(head, content)
        self.msg_send(head, content)
        # 将命令行数据和内容数据连接成发送数据的字符串
        # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
        # print(msg_send)
        # # 发送登录数据到服务器
        # self.sockfd.send(msg_send.encode())

    def login_response(self, action, action_vice, content):
        '''接收登录数据，返回登录验证是否成功'''

        login_info = loads(content)

        if action_vice == "/ok":
            print('登录成功')
            # 如果记住密码，存储密码
            print(self.loginKeepPwd.isChecked())
            if self.loginKeepPwd.isChecked():
                # 将用户名也加密存储
                user_name = md5(self.user_name.encode()).hexdigest()
                self.setting.setValue("user/" + user_name, self.user_pwd_md5)
            self.login_status_data.emit(1, content)   # 提交登录状态信号0单机，1网络
            self.login_sign.emit()      # 提交登录成功信号，用于打开主窗口
            self.close()                # 关闭登录窗口
        elif action_vice == "/forgetpwd":
            print('处理找回密码')
        elif action_vice == "/fail":
            self.loginInfo.setText(login_info['ErrorMsg'])
        else:
            pass
        pass

    @pyqtSlot()
    def on_loginSingleBtn_clicked(self):
        '''单机游戏点击按钮事件，直接关闭登录窗口，打开主窗口'''

        print('单机游戏')
        self.close()
        self.login_status_data.emit(0, "no")   # 提交登录状态信号0单机，1网络
        self.login_sign.emit()
        pass

    @pyqtSlot()
    def on_loginRegBtn_clicked(self):
        '''注册按钮点击事件，打开用户注册界面'''

        # 判断是否连接网络
        if self.net_status == DISCONNECT:
            print("网络未连接")
            self.loginInfo.setText('网络错误，无法连接服务器！')
            return

        self.register_sign.emit()
        pass

    @pyqtSlot('QString')
    def on_loginUserName_textChanged(self):
        '''用户名文本框文本change事件，用于加载记住的密码'''

        # print('loginUserName 文本改变事件')
        user_name = md5(self.loginUserName.text().encode()).hexdigest()
        user_pwd = self.setting.value("user/" + user_name)
        # print('focus', user_pwd)
        if user_pwd:
            self.user_pwd_md5 = user_pwd
            self.loginUserPwd.setText(self.user_pwd_md5)
        else:
            self.user_pwd_md5 = ''
            self.loginUserPwd.clear()

    @pyqtSlot()
    def on_forgetPwd_clicked(self):
        print("忘记密码")
        self.resetpwd_dialog.exec_()
        pass

    @pyqtSlot()
    def on_resetBtn_clicked(self):
        user_name = self.resetpwd_dialog.resetUserName.text()
        user_birth = self.resetpwd_dialog.resetBirthday.text()
        user_passwd = self.resetpwd_dialog.resetPasswd.text()
        user_passwd_cfm = self.resetpwd_dialog.resetPasswdCfm.text()
        if user_passwd != user_passwd_cfm:
            return

        head = 'LOGIN /forgetpwd \r\n'
        content = {
            'UserName': user_name,
            'Birthdate': user_birth,
            'Password': user_passwd,
        }
        # msg_send = head + dumps(content) + '\#\$'   # 将数据内容字典转换为json字符串
        # print(msg_send)
        # # 发送登录数据到服务器
        # self.sockfd.send(msg_send.encode())
        # print('重置密码')
        self.msg_send(head, content)
