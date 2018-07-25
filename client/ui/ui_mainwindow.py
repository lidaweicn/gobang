# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uitest4.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from ui.ui_chat import UiChatFrame
from ui.ui_game import UiGameFrame
from ui.ui_hall import UiHallFrame
from ui.ui_user import UiUserShowFrame, UiUserListFrame
from ui.ui_set import Ui_DialogSet
from ui.ui_emoji import Ui_DialogEmoji
from ui.ui_userinfo import Ui_DialogUserInfo


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.init_function()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1024, 768)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        MainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint |
                                  QtCore.Qt.WindowCloseButtonHint |
                                  QtCore.Qt.WindowMinimizeButtonHint)

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 游戏主框架
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 10, 691, 731))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.uhf = UiHallFrame(self.page, self.user)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.ugf = UiGameFrame(self.page_2)
        self.stackedWidget.addWidget(self.page_2)
        # 聊天框架
        self.ucf = UiChatFrame(self.centralwidget)
        # UiChatFrame.__init__(self.centralwidget)
        # 用户信息框架
        self.uusf = UiUserShowFrame(self.centralwidget)
        # 用户列表框架
        self.uulf = UiUserListFrame(self.centralwidget)
        self.uulf.sign_userlist_to_menu.connect(self.custom_menu)
        # 创建设置窗口
        self.set_dialog = Ui_DialogSet(self)
        # 创建emoji窗口
        self.emoji_dialog = Ui_DialogEmoji(self)
        # 创建用户信息窗口
        self.userinfo_dialog = Ui_DialogUserInfo(self)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.init_game()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "网络五子棋"))
        MainWindow.setStatusTip(_translate("MainWindow", "网络已连接"))
        self.ucf.pushButton.setText(_translate("MainWindow", "发送"))
        self.ucf.pushButton.setShortcut(_translate("MainWindow", "Return"))
        self.ucf.toolButton.setText(_translate("MainWindow", "A"))
        self.ucf.toolButton2.setText(_translate("MainWindow", "B"))
        self.ucf.toolButton3.setText(_translate("MainWindow", "I"))
        self.ucf.toolButton4.setText(_translate("MainWindow", "C"))
        self.ucf.toolButton5.setText(_translate("MainWindow", "😊"))
