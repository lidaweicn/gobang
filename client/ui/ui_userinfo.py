# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userinfo.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt


class Ui_DialogUserInfo(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("DialogUserInfo")
        Dialog.resize(436, 321)
        Dialog.setFixedSize(Dialog.width(), Dialog.height())

        self.userImage = QtWidgets.QLabel(Dialog)
        self.userImage.setGeometry(QtCore.QRect(60, 20, 90, 90))
        self.userImage.setFrameShape(QtWidgets.QFrame.Box)
        self.userImage.setObjectName("userImage")
        self.userImage.setAlignment(Qt.AlignCenter)
        self.userImage.setScaledContents(True)
        self.userInfo = QtWidgets.QLabel(Dialog)
        self.userInfo.setGeometry(QtCore.QRect(190, 10, 211, 101))
        self.userInfo.setObjectName("userInfo")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(70, 170, 51, 27))
        self.label_3.setObjectName("label_3")
        self.userNick = QtWidgets.QLineEdit(Dialog)
        self.userNick.setGeometry(QtCore.QRect(130, 170, 151, 27))
        self.userNick.setObjectName("userNick")
        self.userNick.setClearButtonEnabled(True)
        self.userNickBtn = QtWidgets.QPushButton(Dialog)
        self.userNickBtn.setGeometry(QtCore.QRect(310, 170, 91, 27))
        self.userNickBtn.setObjectName("userNickBtn")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(60, 210, 61, 27))
        self.label_4.setObjectName("label_4")
        self.oldPasswd = QtWidgets.QLineEdit(Dialog)
        self.oldPasswd.setGeometry(QtCore.QRect(130, 210, 151, 27))
        self.oldPasswd.setObjectName("oldPasswd")
        self.oldPasswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.oldPasswd.setClearButtonEnabled(True)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(60, 240, 67, 27))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 270, 91, 27))
        self.label_6.setObjectName("label_6")
        self.userImageList = QtWidgets.QComboBox(Dialog)
        self.userImageList.setGeometry(QtCore.QRect(40, 120, 131, 27))
        self.userImageList.setObjectName("userImageList")
        self.newPasswd = QtWidgets.QLineEdit(Dialog)
        self.newPasswd.setGeometry(QtCore.QRect(130, 240, 151, 27))
        self.newPasswd.setObjectName("newPasswd")
        self.newPasswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPasswd.setClearButtonEnabled(True)
        self.newPasswdCfm = QtWidgets.QLineEdit(Dialog)
        self.newPasswdCfm.setGeometry(QtCore.QRect(130, 270, 151, 27))
        self.newPasswdCfm.setObjectName("newPasswdCfm")
        self.newPasswdCfm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPasswdCfm.setClearButtonEnabled(True)
        self.passwdChange = QtWidgets.QPushButton(Dialog)
        self.passwdChange.setGeometry(QtCore.QRect(310, 240, 91, 27))
        self.passwdChange.setObjectName("passwdChange")
        self.userImageChange = QtWidgets.QPushButton(Dialog)
        self.userImageChange.setGeometry(QtCore.QRect(190, 120, 91, 27))
        self.userImageChange.setObjectName("userImageChange")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "用户信息"))
        self.userImage.setText(_translate("Dialog", "头像"))
        self.userInfo.setText(_translate("Dialog", "<html><head/><body><span>用户名：aaaa</span><br><span>昵称：嘎嘎</span><br><span>等级：5级 积分：4000</span><br><span>场次：30 胜率：50%</span></body></html>"))
        self.label_3.setText(_translate("Dialog", "昵称："))
        self.userNickBtn.setText(_translate("Dialog", "修改昵称"))
        self.label_4.setText(_translate("Dialog", "原密码："))
        self.label_5.setText(_translate("Dialog", "新密码："))
        self.label_6.setText(_translate("Dialog", "确认新密码："))
        self.passwdChange.setText(_translate("Dialog", "修改密码"))
        self.userImageChange.setText(_translate("Dialog", "修改头像"))
