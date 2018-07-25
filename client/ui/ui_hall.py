from PyQt5.QtWidgets import QFrame, QWidget, QPushButton, QScrollArea, QLabel, QGridLayout
from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject, QSize, pyqtSignal, Qt
from PyQt5 import QtCore, QtGui
from py.common import *


class Room(QFrame):
    # 点击对战和观战按钮发送信号，数据类型为字典，
    room_sign_btn = pyqtSignal(str, int)

    def __init__(self, parent, user, roomName="房间1"):
        super(Room, self).__init__(parent)
        self.user = user
        self.roomName = roomName
        self.player_left = ''
        self.player_right = ''
        self.sign_isconnect = False
        self.setupUi()

    def setupUi(self):
        # self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.setObjectName("Room")
        # self.setGeometry(QRect(30, 40, 221, 121))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet(
            "/*background-image: url(./img/bg.bmp);*/border:none;")
        self.roomTop = QLabel(self)
        self.roomTop.setGeometry(QRect(80, 10, 110, 20))
        self.roomTop.setObjectName("roomTop")
        self.roomTop.setStyleSheet("text-align:center;")
        self.roomTop.setAlignment(Qt.AlignCenter)

        self.roomVSLeft = QPushButton(self)
        self.roomVSLeft.setGeometry(QRect(10, 70, 60, 60))
        self.roomVSLeft.setObjectName("roomVSLeft")
        self.roomVSLabelL = QLabel(self)
        self.roomVSLabelL.setGeometry(QRect(0, 130, 80, 20))
        self.roomVSLabelL.setObjectName("label")
        self.roomVSLabelL.setScaledContents(True)
        self.roomVSLabelL.setAlignment(Qt.AlignCenter)
        # self.roomVSLeft.setScaledContents(True)
        self.roomVSRight = QPushButton(self)
        self.roomVSRight.setGeometry(QRect(200, 70, 60, 60))
        self.roomVSRight.setObjectName("roomVSRight")
        self.roomVSLabelR = QLabel(self)
        self.roomVSLabelR.setGeometry(QRect(190, 130, 80, 20))
        self.roomVSLabelR.setObjectName("label")
        self.roomVSLabelR.setScaledContents(True)
        self.roomVSLabelR.setAlignment(Qt.AlignCenter)
        self.label = QLabel(self)
        self.label.setGeometry(QRect(80, 40, 110, 110))
        self.label.setObjectName("label")
        self.label.setScaledContents(True)
        # self.label.setStyleSheet("border:1px solid;")

        self.roomWatch = QPushButton(self)
        self.roomWatch.setGeometry(QRect(105, 160, 60, 30))
        self.roomWatch.setObjectName("roomWatch")

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.roomVSLeft.setText(_translate("Room", "对战"))
        self.roomVSLabelL.setText(_translate("Room", ""))
        self.roomVSRight.setText(_translate("Room", "对战"))
        self.roomVSLabelR.setText(_translate("Room", ""))
        self.label.setText(_translate("Room", "房间1"))
        pix = QtGui.QPixmap('img/desktop.png')
        self.label.setPixmap(pix)
        self.roomTop.setText(_translate("Room", self.roomName))
        self.roomWatch.setText(_translate("Room", "观战"))

    @QtCore.pyqtSlot()
    def on_roomVSLeft_clicked(self):
        print('房间对战按钮', self)
        # print(self.roomTop.text())

        self.room_sign_btn.emit(self.roomTop.text(), PLAYER1)

        # self.roomVSLabelL.setText(self.user.user_nick)
        # self.roomVSLeft.setStyleSheet("border-image: url({});"
        #                               .format(self.user.user_image))

        # print(self.roomVSLeft.text())
        pass

    @QtCore.pyqtSlot()
    def on_roomVSRight_clicked(self):
        print('房间对战按钮', self)
        # print(self.roomTop.text())

        self.room_sign_btn.emit(self.roomTop.text(), PLAYER2)

        # self.roomVSLabelR.setText(self.user.user_nick)
        # self.roomVSRight.setStyleSheet(
        #     "border-image: url({});".format(self.user.user_image))
        # self.label.setPixmap(self.user.user_pix)
        # print(self.roomVSRight.text())
        pass

    @QtCore.pyqtSlot()
    def on_roomWatch_clicked(self):
        print('房间观战按钮', self)
        # print(self.roomTop.text())

        self.room_sign_btn.emit(self.roomTop.text(), WATCHING)

        # print(self.roomVSRight.text())
        pass


class UiHallFrame(QFrame):
    def __init__(self, parent, user):
        super(UiHallFrame, self).__init__(parent)
        self.user = user
        self.setupUi()

    def setupUi(self):

        # 游戏大厅界面
        self.setGeometry(QRect(10, 10, 671, 711))
        # self.setStyleSheet("background-image: url(./img/bg.bmp);")
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(2)
        self.setObjectName("uiGameFrame")

        self.hallBanner = QLabel(self)
        self.hallBanner.setGeometry(QRect(20, 10, 630, 50))
        self.hallBanner.setObjectName("hallBanner")
        self.hallBanner.setScaledContents(True)
        # self.hallBanner.setStyleSheet("/*border:1px solid;*/background-image: url(./img/banner.png);")
        pix = QtGui.QPixmap('./img/banner.png')
        self.hallBanner.setPixmap(pix)

        self.hall_scrollArea = QScrollArea(self)
        self.hall_scrollArea.setGeometry(QRect(20, 80, 630, 551))
        self.hall_scrollArea.setWidgetResizable(True)
        self.hall_scrollArea.setObjectName("scrollArea")
        self.hall_widgetContents = QWidget()
        self.hall_widgetContents.setGeometry(QRect(0, 0, 629, 549))
        self.hall_widgetContents.setObjectName("widgetContents")
        self.hall_widgetContents.setMinimumSize(QSize(400, 400))
        # self.hall_widgetContents.setStyleSheet('background:rgba(0,0,0,0)')

        # 创建房间列表，用于存储房间
        self.rooms = {}
        self.lay = QGridLayout(self.hall_widgetContents)

        self.hall_scrollArea.setWidget(self.hall_widgetContents)

        # 按钮区域
        self.cmd_frame = QFrame(self)
        self.cmd_frame.setGeometry(QRect(55, 655, 560, 47))
        self.cmd_frame.setFrameShape(QFrame.StyledPanel)
        self.cmd_frame.setFrameShadow(QFrame.Raised)
        self.cmd_frame.setObjectName("cmdFrame")

        # 快速游戏
        self.hallFastJoin = QPushButton(self.cmd_frame)
        self.hallFastJoin.setGeometry(QRect(10, 10, 100, 27))
        self.hallFastJoin.setObjectName("hallFastJoin")

        # 用户信息
        self.hallUserInfo = QPushButton(self.cmd_frame)
        self.hallUserInfo.setGeometry(QRect(120, 10, 100, 27))
        self.hallUserInfo.setObjectName("hallUserInfo")

        # 单机游戏
        self.hallConsoleGame = QPushButton(self.cmd_frame)
        self.hallConsoleGame.setGeometry(QRect(230, 10, 100, 27))
        self.hallConsoleGame.setObjectName("hallConsoleGame")

        # 返回大厅
        self.hallCreateRoom = QPushButton(self.cmd_frame)
        self.hallCreateRoom.setGeometry(QRect(340, 10, 100, 27))
        self.hallCreateRoom.setObjectName("hallCreateRoom")

        # 设置
        self.hallSetBtn = QPushButton(self.cmd_frame)
        self.hallSetBtn.setGeometry(QRect(450, 10, 100, 27))
        self.hallSetBtn.setObjectName("hallSetBtn")

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.hallFastJoin.setText(_translate("uiGameFrame", "快速游戏"))
        self.hallUserInfo.setText(_translate("uiGameFrame", "用户信息"))
        self.hallConsoleGame.setText(_translate("uiGameFrame", "电脑对战"))
        self.hallCreateRoom.setText(_translate("uiGameFrame", "创建房间"))
        self.hallSetBtn.setText(_translate("uiGameFrame", "设置"))
