from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import pyqtSignal
from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_login import Ui_Dialog
from ui.ui_register import Ui_DialogR
from py.client import ClientThread, ClientFunction
from py.login import LoginFunction
from py.register import RegisterFunction
from socket import socket, AF_INET, SOCK_STREAM
from py.common import *
from random import choice
import sys


class User(object):
    def __init__(self):
        self.user_site = HALL   # 位置
        self.user_status = WATCHING
        self.user_name = ''
        self.user_nick = ''
        self.user_image = choice(['img/user/boy.png', 'img/user/girl.png'])
        self.user_level = 0
        self.user_score = 0
        self.total_round = 0
        self.win_round = 0
        self.show_info = ''
        self.game_status = ''
        self.game_time = 0
        pass
    pass


class MyMainWindow(QMainWindow, Ui_MainWindow, ClientFunction):
    '''主窗口类

    继承主窗口Ui_MainWindow、客户端功能函数类ClientFunction'''

    def __init__(self, parent=None, sockfd=None):
        super(MyMainWindow, self).__init__(parent)
        self.sockfd = sockfd
        self.net_status = ''
        # 创建用户对象
        self.user = User()
        self.user_l = User()
        self.user_r = User()
        Ui_MainWindow.__init__(parent, self.user)   # 用户对象传入窗口
        self.setupUi(self)
        self.load_config()  # 加载配置
        # self.setStyleSheet(self.QSS)

    def set_status(self, status, content):
        self.set_style()
        if status == 0:
            # 单机游戏，断开网络
            if self.net_status == CONNECTED:
                self.sockfd.close()
                self.net_status = DISCONNECT
            # 设置单机游戏参数
            self.user.user_status = SINGLE
            self.game_status = OVER
            # 打开单机界面
            self.stackedWidget.setCurrentIndex(1)
            # 禁用网络对战相关按钮
            self.ugf.gameUndoBtn.setEnabled(False)
            self.ugf.gameGiveupBtn.setEnabled(False)
            self.ugf.gameReHallBtn.setEnabled(False)
            self.setStatusTip('单机模式')
            self.user_r.user_image = 'img/user/robot.png'
            self.set_user(content, mode=SINGLE)
            self.set_vs(content, mode=SINGLE)
        else:
            self.user.user_status = WATCHING
            self.game_status = OVER
            self.stackedWidget.setCurrentIndex(0)
            self.set_user(content)
        pass


class LoginWindow(QDialog, Ui_Dialog, LoginFunction, Config):
    '''登录窗口类

    继承Ui_Dialog图形界面类、LoginFunction登录函数类和Config配置类'''

    login_sign = pyqtSignal()       # 登录成功发送信号打开主窗口
    register_sign = pyqtSignal()    # 点击注册按钮，发送信号打开注册窗口
    login_status_data = pyqtSignal(int, str)  # 发送登录状态到主窗口，网络1或单机0，和登录返回数据

    def __init__(self, parent=None, sockfd=None):
        super(LoginWindow, self).__init__(parent)
        self.sockfd = sockfd
        self.net_status = ''
        self.user_pwd_md5 = ''
        self.setupUi(self)
        self.load_config()  # 加载配置
        self.setStyleSheet(self.QSS)
        pass


class RegisterWindow(QDialog, Ui_DialogR, RegisterFunction, Config):
    '''注册窗口类，继承Ui_DialogR图形界面类'''

    def __init__(self, parent=None, sockfd=None):
        super(RegisterWindow, self).__init__(parent)
        self.sockfd = sockfd
        self.net_status = ''
        self.setupUi(self)
        self.load_config()  # 加载配置
        self.setStyleSheet(self.QSS)
        pass


def main():
    # 创建网络套接字
    sockfd = socket(AF_INET, SOCK_STREAM, 0)

    # 创建图形界面应用
    app = QApplication(sys.argv)
    # 创建主窗口
    myWin = MyMainWindow(sockfd=sockfd)
    # 创建登录窗口
    myLogin = LoginWindow(sockfd=sockfd)
    # 创建注册窗口
    myRegister = RegisterWindow(sockfd=sockfd)

    # 从配置文件读取IP地址和端口
    setting = QSettings('./setting.ini', QSettings.IniFormat)
    IP = setting.value('setting/server')
    PORT = int(setting.value('setting/port'))
    ADDR = (IP, PORT)

    # 连接网络
    try:
        sockfd.connect(ADDR)
        myWin.net_status = CONNECTED
        myLogin.net_status = CONNECTED
        myRegister.net_status = CONNECTED
        # 网络连接成功，启动线程接收数据
        client_thread = ClientThread(sockfd)
        client_thread.setDaemon(True)
        client_thread.start()
        # 客户端线程信号绑定槽函数，用于线程向图形界面发送数据，readResponse函数接收数据
        client_thread.sign_thread_to_game.connect(myWin.readResponse)
        # 线程发送的登录信号，连接到登录窗口login_response函数
        client_thread.sign_thread_to_login.connect(myLogin.login_response)
        # 线程发送的注册信号，连接到注册窗口register_response函数
        client_thread.sign_thread_to_register\
            .connect(myRegister.register_response)
        # 登录窗口发送登录状态到线程，如果为单机，关闭线程
        myLogin.login_status_data.connect(client_thread.stop)
    except (ConnectionRefusedError, OSError):
        print("网络连接错误，")
        myWin.net_status = DISCONNECT
        myLogin.net_status = DISCONNECT
        myRegister.net_status = DISCONNECT
        myWin.setStatusTip('网络未连接')
        pass
    except Exception as e:
        print(e)

    # 显示登录窗口
    myLogin.show()
    # 登录窗口信号绑定函数，用于显示窗口
    myLogin.register_sign.connect(myRegister.show)
    myLogin.login_sign.connect(myWin.show)
    # 登录窗口将登录状态和数据发送到主窗口
    myLogin.login_status_data.connect(myWin.set_status)
    # 图形界面进入事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
