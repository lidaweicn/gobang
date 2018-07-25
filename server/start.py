from threading import Thread
from socket import *
from random import *
from client_handler import ClientHandler
from config import *
from game_room import Room
from common import get_time
from time import sleep
import os
import log

LoginUser = {}  # 用来保存用户状态 是存储正在线上的用户的状态
AllRoom = {}    # 用来存储游戏房间
Log = []        # 用来存储日志
GameLog = []    # 用来存储游戏日志

# 初始化游戏房间,初始创建6张桌子，可动态添加
# 游戏房间号为1到6，0为大厅，999为电脑对战
for i in range(7):
    AllRoom[i] = Room(i, LoginUser, AllRoom, GameLog)
AllRoom[999] = Room(999, LoginUser, AllRoom, GameLog)


def handler2(connfd):
    '''客户端处理函数'''

    # 引入全局变量
    global LoginUser
    global AllRoom
    global Log

    addr = connfd.getpeername()
    print("客户端连接", addr)
    # Log.append(get_time() + '客户端连接' + str(addr))
    # 写日志
    log.logging.info('客户端连接{}'.format(addr))
    handler = ClientHandler(connfd, LoginUser, AllRoom, Log)
    handler.data_recv()


# 自定义写日志函数，取消不用
def loghandler():
    '''日志处理函数'''

    global Log
    global GameLog

    print('服务器日志启动')
    while True:
        sleep(10)   # 间隔多长时间记录一次
        path = os.getcwd() + LOG_PATH + '/{}'\
            .format(get_time()[:10])
        if not os.path.exists(path):
            os.mkdir(path)
        if Log:
            print(Log)
            with open(path + '/log.txt', 'a') as f:
                logwrite = Log
                Log = Log[len(logwrite):]
                for line in logwrite:
                    f.write(line + '\n')
        if GameLog:
            print(GameLog)
            with open(path + '/gamelog.txt', 'a') as f2:
                gamelogwrite = GameLog
                GameLog = []
                for line in gamelogwrite:
                    f2.write(line + '\n')


def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print("服务器启动")
    print("服务器地址:{}:{}".format(HOST, PORT))
    log.logging.info('服务器启动')
    # Log.append(get_time() + "服务器启动")
    # t1 = Thread(target=loghandler)
    # t1.setDaemon(True)  # 主线程结束之后，自动处理回收，并子线程结束
    # t1.start()
    while True:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e)
            # continue
        print(type(c))
        t2 = Thread(target=handler2, args=(c,))
        t2.setDaemon(True)  # 主线程结束之后，自动处理回收，并子线程结束
        t2.start()


if __name__ == '__main__':
    main()
