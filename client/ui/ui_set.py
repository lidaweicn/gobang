# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_DialogSet(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, DialogSet):
        DialogSet.setObjectName("DialogSet")
        DialogSet.resize(400, 300)
        DialogSet.setFixedSize(DialogSet.width(), DialogSet.height())

        self.label = QtWidgets.QLabel(DialogSet)
        self.label.setGeometry(QtCore.QRect(50, 30, 67, 27))
        self.label.setObjectName("label")
        self.setWindowStyle = QtWidgets.QComboBox(DialogSet)
        self.setWindowStyle.setGeometry(QtCore.QRect(140, 30, 121, 27))
        self.setWindowStyle.setObjectName("setWindowStyle")
        self.setWindowStyleLb = QtWidgets.QLabel(DialogSet)
        self.setWindowStyleLb.setGeometry(QtCore.QRect(280, 30, 67, 27))
        self.setWindowStyleLb.setObjectName("setWindowStyleLb")
        self.label_3 = QtWidgets.QLabel(DialogSet)
        self.label_3.setGeometry(QtCore.QRect(50, 65, 71, 27))
        self.label_3.setObjectName("label_3")
        self.setBoardStyle = QtWidgets.QComboBox(DialogSet)
        self.setBoardStyle.setGeometry(QtCore.QRect(140, 65, 121, 27))
        self.setBoardStyle.setObjectName("setBoardStyle")
        self.setBoardStyleLb = QtWidgets.QLabel(DialogSet)
        self.setBoardStyleLb.setGeometry(QtCore.QRect(280, 65, 67, 27))
        self.setBoardStyleLb.setObjectName("setBoardStyleLb")
        self.label_7 = QtWidgets.QLabel(DialogSet)
        self.label_7.setGeometry(QtCore.QRect(50, 100, 71, 27))
        self.label_7.setObjectName("label_7")
        self.setPieceStyle = QtWidgets.QComboBox(DialogSet)
        self.setPieceStyle.setGeometry(QtCore.QRect(140, 100, 121, 27))
        self.setPieceStyle.setObjectName("setPieceStyle")
        self.setPieceStyleLb = QtWidgets.QLabel(DialogSet)
        self.setPieceStyleLb.setGeometry(QtCore.QRect(280, 100, 67, 27))
        self.setPieceStyleLb.setObjectName("setPieceStyleLb")
        self.label_6 = QtWidgets.QLabel(DialogSet)
        self.label_6.setGeometry(QtCore.QRect(50, 135, 81, 27))
        self.label_6.setObjectName("label_6")
        self.setMusic = QtWidgets.QCheckBox(DialogSet)
        self.setMusic.setGeometry(QtCore.QRect(140, 135, 86, 27))
        self.setMusic.setObjectName("setMusic")
        self.setSound = QtWidgets.QCheckBox(DialogSet)
        self.setSound.setGeometry(QtCore.QRect(250, 135, 91, 27))
        self.setSound.setObjectName("setSound")
        self.label_8 = QtWidgets.QLabel(DialogSet)
        self.label_8.setGeometry(QtCore.QRect(50, 170, 71, 27))
        self.label_8.setObjectName("label_8")
        self.setIP = QtWidgets.QLineEdit(DialogSet)
        self.setIP.setGeometry(QtCore.QRect(140, 170, 201, 27))
        self.setIP.setObjectName("setIP")
        self.label_9 = QtWidgets.QLabel(DialogSet)
        self.label_9.setGeometry(QtCore.QRect(50, 205, 71, 27))
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setObjectName("label_9")
        self.setPort = QtWidgets.QLineEdit(DialogSet)
        self.setPort.setGeometry(QtCore.QRect(140, 205, 71, 27))
        self.setPort.setObjectName("setPort")
        self.setSave = QtWidgets.QPushButton(DialogSet)
        self.setSave.setGeometry(QtCore.QRect(100, 250, 92, 33))
        self.setSave.setObjectName("setSave")
        self.setReset = QtWidgets.QPushButton(DialogSet)
        self.setReset.setGeometry(QtCore.QRect(220, 250, 91, 33))
        self.setReset.setObjectName("setReset")

        self.retranslateUi(DialogSet)
        QtCore.QMetaObject.connectSlotsByName(DialogSet)

    def retranslateUi(self, DialogSet):
        _translate = QtCore.QCoreApplication.translate
        DialogSet.setWindowTitle(_translate("DialogSet", "设置"))
        self.label.setText(_translate("DialogSet", "界面风格："))
        self.setWindowStyleLb.setText(_translate("DialogSet", "当前风格"))
        self.label_3.setText(_translate("DialogSet", "棋盘样式："))
        self.setBoardStyleLb.setText(_translate("DialogSet", "当前风格"))
        self.label_7.setText(_translate("DialogSet", "棋子样式："))
        self.setPieceStyleLb.setText(_translate("DialogSet", "当前风格"))
        self.label_6.setText(_translate("DialogSet", "声音设置："))
        self.setMusic.setText(_translate("DialogSet", "背景音乐"))
        self.setSound.setText(_translate("DialogSet", "游戏音效"))
        self.label_8.setText(_translate("DialogSet", "服务器IP："))
        self.label_9.setText(_translate("DialogSet", "端口："))
        self.setSave.setText(_translate("DialogSet", "保存设置"))
        self.setReset.setText(_translate("DialogSet", "恢复默认"))
