# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forgetpasswd.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_DialogResetPwd(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def setupUi(self, DialogResetPwd):
        DialogResetPwd.setObjectName("DialogResetPwd")
        DialogResetPwd.resize(300, 200)
        DialogResetPwd.setFixedSize(DialogResetPwd.width(),
                                    DialogResetPwd.height())

        self.label = QtWidgets.QLabel(DialogResetPwd)
        self.label.setGeometry(QtCore.QRect(45, 10, 51, 27))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(DialogResetPwd)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 67, 27))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(DialogResetPwd)
        self.label_3.setGeometry(QtCore.QRect(30, 70, 67, 27))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(DialogResetPwd)
        self.label_4.setGeometry(QtCore.QRect(30, 100, 67, 27))
        self.label_4.setObjectName("label_4")
        self.resetUserName = QtWidgets.QLineEdit(DialogResetPwd)
        self.resetUserName.setGeometry(QtCore.QRect(120, 10, 151, 27))
        self.resetUserName.setObjectName("resetUserName")
        self.resetBirthday = QtWidgets.QLineEdit(DialogResetPwd)
        self.resetBirthday.setGeometry(QtCore.QRect(120, 40, 151, 27))
        self.resetBirthday.setObjectName("resetBirthday")
        self.resetPasswd = QtWidgets.QLineEdit(DialogResetPwd)
        self.resetPasswd.setGeometry(QtCore.QRect(120, 70, 151, 27))
        self.resetPasswd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.resetPasswd.setObjectName("resetPasswd")
        self.resetPasswdCfm = QtWidgets.QLineEdit(DialogResetPwd)
        self.resetPasswdCfm.setGeometry(QtCore.QRect(120, 100, 151, 27))
        self.resetPasswdCfm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.resetPasswdCfm.setObjectName("resetPasswdCfm")
        self.resetBtn = QtWidgets.QPushButton(DialogResetPwd)
        self.resetBtn.setGeometry(QtCore.QRect(120, 150, 99, 27))
        self.resetBtn.setObjectName("resetBtn")

        self.retranslateUi(DialogResetPwd)
        QtCore.QMetaObject.connectSlotsByName(DialogResetPwd)

    def retranslateUi(self, DialogResetPwd):
        _translate = QtCore.QCoreApplication.translate
        DialogResetPwd.setWindowTitle(_translate("DialogResetPwd", "忘记密码"))
        self.label.setText(_translate("DialogResetPwd", "用户名："))
        self.label_2.setText(_translate("DialogResetPwd", "出生日期："))
        self.label_3.setText(_translate("DialogResetPwd", "重置密码："))
        self.label_4.setText(_translate("DialogResetPwd", "确认密码："))
        self.resetBtn.setText(_translate("DialogResetPwd", "重置密码"))
