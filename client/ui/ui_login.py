# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from ui.ui_resetpwd import Ui_DialogResetPwd


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setFixedSize(Dialog.width(), Dialog.height())
        Dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint |
                              QtCore.Qt.WindowCloseButtonHint |
                              QtCore.Qt.WindowMinimizeButtonHint)
        self.loginInfo = QtWidgets.QLabel(Dialog)
        self.loginInfo.setGeometry(QtCore.QRect(90, 30, 240, 17))
        self.loginInfo.setObjectName("loginInfo")
        self.loginInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.loginInfo.setStyleSheet('color:red;')

        self.loginUserName = QtWidgets.QLineEdit(Dialog)
        self.loginUserName.setGeometry(QtCore.QRect(120, 60, 191, 27))
        self.loginUserName.setObjectName("loginUserName")
        self.loginUserName.setClearButtonEnabled(True)
        self.loginUserPwd = QtWidgets.QLineEdit(Dialog)
        self.loginUserPwd.setGeometry(QtCore.QRect(120, 110, 191, 27))
        self.loginUserPwd.setObjectName("loginUserPwd")
        self.loginUserPwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginUserPwd.setClearButtonEnabled(True)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 60, 67, 27))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(70, 110, 31, 27))
        self.label_2.setObjectName("label_2")
        self.loginKeepPwd = QtWidgets.QCheckBox(Dialog)
        self.loginKeepPwd.setGeometry(QtCore.QRect(100, 160, 140, 17))
        self.loginKeepPwd.setObjectName("loginKeepPwd")
        self.loginBtn = QtWidgets.QPushButton(Dialog)
        self.loginBtn.setGeometry(QtCore.QRect(100, 200, 99, 27))
        self.loginBtn.setObjectName("loginBtn")
        self.loginRegBtn = QtWidgets.QPushButton(Dialog)
        self.loginRegBtn.setGeometry(QtCore.QRect(210, 200, 99, 27))
        self.loginRegBtn.setObjectName("loginRegBtn")
        self.loginSingleBtn = QtWidgets.QPushButton(Dialog)
        self.loginSingleBtn.setGeometry(QtCore.QRect(150, 250, 99, 27))
        self.loginSingleBtn.setObjectName("loginSingleBtn")
        self.forgetPwd = QtWidgets.QPushButton(Dialog)
        self.forgetPwd.setGeometry(QtCore.QRect(250, 158, 67, 20))
        self.forgetPwd.setObjectName("forgetPwd")
        self.forgetPwd.setStyleSheet("border:none;background:")

        # 创建找回密码窗口
        self.resetpwd_dialog = Ui_DialogResetPwd(self)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "用户登录"))
        self.loginInfo.setText(_translate("Dialog", ""))
        self.loginUserName.setPlaceholderText(_translate("Dialog", "请输入用户名"))
        self.loginUserPwd.setPlaceholderText(
            _translate("Dialog", "请输入6-12位密码"))
        self.label.setText(_translate("Dialog", "用户名"))
        self.label_2.setText(_translate("Dialog", "密码"))
        self.loginKeepPwd.setText(_translate("Dialog", "记住密码"))
        self.loginBtn.setText(_translate("Dialog", "登录"))
        self.loginRegBtn.setText(_translate("Dialog", "注册"))
        self.loginSingleBtn.setText(_translate("Dialog", "单机游戏"))
        self.forgetPwd.setText(_translate("Dialog", "忘记密码"))
