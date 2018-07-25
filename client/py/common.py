'''
全局常量，配置函数类
'''
from PyQt5.QtCore import QSettings
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QIcon
from time import localtime

# HOST = '172.60.12.69'
# PORT = 8886
# HOST = '127.0.0.1'
# PORT = 8888
# ADDR = (HOST, PORT)
# 用户所在位置，大厅或房间
HALL = 0
ROOM1, ROOM2, ROOM3, ROOM4, ROOM5, ROOM6 = range(1, 7)
# 玩家状态，棋手1，棋手2，观战
SINGLE = 0      # 单机游戏
PLAYER1 = 1     # 对战玩家1，左
PLAYER2 = 2     # 对战玩家2，右
WATCHING = 3    # 观战
NETSINGLE = 4   # 联网，与电脑对战
# 游戏状态
OVER = 10
READY = 11
WHITE = 12
BLACK = 13
START = 14
WATCH = 15
# 网络连接状态，
CONNECTED = 1       # 网络已连接
DISCONNECT = 0      # 网络未连接


class Config(object):
    def load_config(self):
        # 读取配置文件
        self.setting = QSettings('./setting.ini', QSettings.IniFormat)
        # self.setting.setIniCodec("UTF8")
        # 加载落子音效
        self.sound_piece = QSound("sound/move.wav")
        self.background_music = QSound("sound/bgm.wav")
        self.background_music.setLoops(-1)
        # 加载配置
        self.config = {}
        self.setting.beginGroup("setting")
        ck = self.setting.childKeys()
        for k in ck:
            self.config[k] = self.setting.value(k)
        self.setting.endGroup()
        # print('配置字典', self.config)
        # 读取样式文件
        # print('qss/', type(self.config['qss']))

        style_file = self.setting.value('qss/' + self.config['qss'])

        # print("common:49", style_file)
        self.QSS = self.read_qss(style_file)
        # 设置程序图标
        icon = QIcon('img/logo.png')
        self.setWindowIcon(icon)

    @staticmethod
    def read_qss(style_file):
        with open(style_file, 'r') as f:
            return f.read()

    @staticmethod
    def get_time():
        tm = "{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}"\
            .format(*localtime()[:6])
        return tm
        pass
