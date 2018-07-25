from PyQt5.QtWidgets import QFrame, QLCDNumber, QPushButton, QLabel
from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject, Qt


class UiGameFrame(QFrame):
    def __init__(self, parent):
        super(UiGameFrame, self).__init__(parent)
        self.setupUi()

    def setupUi(self):

        # 游戏界面
        self.setGeometry(QRect(10, 10, 671, 711))
        # self.setStyleSheet("background-image: url(./img/bg.bmp);")
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(2)
        self.setObjectName("uiGameFrame")

        # 房间信息
        self.game_info = QLabel(self)
        self.game_info.setGeometry(QRect(20, 5, 631, 40))
        self.game_info.setObjectName("gameInfo")
        self.game_info.setScaledContents(True)
        self.game_info.setStyleSheet(
            'font-size:20px;font-weight:bold;')
        self.game_info.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # 游戏画面
        self.game_frame = QFrame(self)
        self.game_frame.setGeometry(QRect(80, 145, 504, 504))
        # self.game_frame.setStyleSheet("background-image: url(./img/game.bmp);")
        self.game_frame.setFrameShape(QFrame.Box)
        self.game_frame.setFrameShadow(QFrame.Plain)
        self.game_frame.setObjectName("gameFrame")

        # 对战
        self.vs_frame = QFrame(self)
        self.vs_frame.setGeometry(QRect(50, 55, 270, 80))
        self.vs_frame.setFrameShape(QFrame.StyledPanel)
        self.vs_frame.setFrameShadow(QFrame.Raised)
        self.vs_frame.setObjectName("vsFrame")
        # self.vs_frame.setStyleSheet("border:1px solid;")

        self.vs_user_image = QLabel(self.vs_frame)
        self.vs_user_image.setGeometry(QRect(5, 5, 70, 70))
        self.vs_user_image.setObjectName("vsUserImage")
        self.vs_user_image.setScaledContents(True)

        self.vs_user_info = QLabel(self.vs_frame)
        self.vs_user_info.setGeometry(QRect(80, 5, 120, 70))
        self.vs_user_info.setObjectName("vsUserInfo")

        self.lcdNumber_l = QLCDNumber(self.vs_frame)
        self.lcdNumber_l.setGeometry(QRect(205, 5, 60, 70))
        self.lcdNumber_l.setLineWidth(0)
        self.lcdNumber_l.setDigitCount(2)
        self.lcdNumber_l.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_l.setProperty("intValue", 20)
        self.lcdNumber_l.setObjectName("lcdNumber_2")

        self.vs_frame_r = QFrame(self)
        self.vs_frame_r.setGeometry(QRect(350, 55, 270, 80))
        self.vs_frame_r.setFrameShape(QFrame.StyledPanel)
        self.vs_frame_r.setFrameShadow(QFrame.Raised)
        self.vs_frame_r.setObjectName("vsFrameR")
        # self.vs_frame_r.setStyleSheet("border:1px solid;")

        self.lcdNumber_r = QLCDNumber(self.vs_frame_r)
        self.lcdNumber_r.setGeometry(QRect(5, 5, 60, 70))
        self.lcdNumber_r.setLineWidth(0)
        self.lcdNumber_r.setDigitCount(2)
        self.lcdNumber_r.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber_r.setProperty("intValue", 20)
        self.lcdNumber_r.setObjectName("lcdNumber_3")

        self.vs_user_image_r = QLabel(self.vs_frame_r)
        self.vs_user_image_r.setGeometry(QRect(70, 5, 70, 70))
        self.vs_user_image_r.setObjectName("vsUserImageR")
        self.vs_user_image_r.setScaledContents(True)

        self.vs_user_info_r = QLabel(self.vs_frame_r)
        self.vs_user_info_r.setGeometry(QRect(145, 5, 120, 70))
        self.vs_user_info_r.setObjectName("vsUserInfoR")

        # 按钮区域
        self.cmd_frame = QFrame(self)
        self.cmd_frame.setGeometry(QRect(55, 655, 560, 47))
        self.cmd_frame.setFrameShape(QFrame.StyledPanel)
        self.cmd_frame.setFrameShadow(QFrame.Raised)
        self.cmd_frame.setObjectName("cmdFrame")
        # 开始按钮
        self.gameStartBtn = QPushButton(self.cmd_frame)
        self.gameStartBtn.setGeometry(QRect(10, 10, 100, 27))
        self.gameStartBtn.setObjectName("gameStartBtn")

        # 悔棋按钮
        self.gameUndoBtn = QPushButton(self.cmd_frame)
        self.gameUndoBtn.setGeometry(QRect(120, 10, 100, 27))
        self.gameUndoBtn.setObjectName("gameUndoBtn")

        # 认输按钮
        self.gameGiveupBtn = QPushButton(self.cmd_frame)
        self.gameGiveupBtn.setGeometry(QRect(230, 10, 100, 27))
        self.gameGiveupBtn.setObjectName("gameGiveupBtn")

        # 返回大厅
        self.gameReHallBtn = QPushButton(self.cmd_frame)
        self.gameReHallBtn.setGeometry(QRect(340, 10, 100, 27))
        self.gameReHallBtn.setObjectName("gameReHallBtn")

        # 设置
        self.gameSetBtn = QPushButton(self.cmd_frame)
        self.gameSetBtn.setGeometry(QRect(450, 10, 100, 27))
        self.gameSetBtn.setObjectName("gameSetBtn")

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.gameStartBtn.setText(_translate("MainWindow", "开始游戏"))
        self.gameUndoBtn.setText(_translate("MainWindow", "悔棋"))
        self.gameGiveupBtn.setText(_translate("MainWindow", "认输"))
        self.gameReHallBtn.setText(_translate("MainWindow", "返回大厅"))
        self.gameSetBtn.setText(_translate("MainWindow", "设置"))
