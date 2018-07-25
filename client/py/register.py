from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from hashlib import md5
from json import dumps, loads
from re import match
from py.datatransfer import DataTransfer


class RegisterFunction(DataTransfer):
    @pyqtSlot()
    def on_regRegBtn_clicked(self):
        print('注册')
        user_name = self.regUserName.text()
        if not user_name:
            self.regInfo.setText('请输入用户名！')
            return
        user_pwd = self.regUserPwd.text()
        if not user_pwd:
            self.regInfo.setText('请输入密码！')
            return
        user_pwd_cfm = self.regUserPwdCfm.text()
        if user_pwd != user_pwd_cfm:
            self.regInfo.setText('两次输入的密码不相同！')
            return
        user_nick_name = self.regUserNick.text()
        if not user_nick_name:
            self.regInfo.setText('请输入昵称！')
            return
        user_birth_date = self.regUserBirth.text()
        regex = '^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
        birth_test = match(regex, user_birth_date)
        print(birth_test)
        try:
            birth_date = birth_test.group()
            print(birth_date)
        except Exception:
            self.regInfo.setText('出生日期格式不对！')
            return
            pass

        # 密码进行加密
        user_pwd_md5 = md5(user_pwd.encode()).hexdigest()

        # 将发送的数据封装在head和content变量中
        head = "REGISTER / \r\n"      # 命令行参数
        # 发送的数据内容，封装为字典
        content = {
            'UserName': user_name,
            'Password': user_pwd_md5,
            'NickName': user_nick_name,
            'Birthdate': user_birth_date,
        }
        print(head, content)
        # # 将命令行数据和内容数据连接成发送数据的字符串
        # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
        # print(msg_send)
        # # 发送登录数据到服务器
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    def register_response(self, action, action_vice, content):
        msg = loads(content)
        if action_vice == '/ok':
            QMessageBox.information(self,
                                    "用户注册",
                                    "{}".format(msg['OkMsg']),
                                    QMessageBox.Yes)
            print('注册成功')
        if action_vice == '/fail':
            QMessageBox.information(self,
                                    "用户注册",
                                    "{}".format(msg['ErrorMsg']),
                                    QMessageBox.Yes)
            print('注册失败')
        else:
            pass
        pass
