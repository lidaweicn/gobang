# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtGui


class Ui_DialogR(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setFixedSize(Dialog.width(), Dialog.height())

        self.regInfo = QtWidgets.QLabel(Dialog)
        self.regInfo.setGeometry(QtCore.QRect(70, 5, 267, 27))
        self.regInfo.setObjectName("regInfo")
        self.regInfo.setAlignment(QtCore.Qt.AlignCenter)
        # self.regInfo.setStyleSheet("border:1px solid;")
        self.regInfo.setStyleSheet('color:red;')

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 40, 67, 27))
        self.label.setObjectName("label")
        self.regUserName = QtWidgets.QLineEdit(Dialog)
        self.regUserName.setGeometry(QtCore.QRect(140, 40, 191, 27))
        self.regUserName.setObjectName("regUserName")
        self.regUserName.setMaxLength(8)

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 80, 31, 27))
        self.label_2.setObjectName("label_2")
        self.regUserPwd = QtWidgets.QLineEdit(Dialog)
        self.regUserPwd.setGeometry(QtCore.QRect(140, 80, 191, 27))
        self.regUserPwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.regUserPwd.setObjectName("regUserPwd")
        self.regUserPwd.setMaxLength(8)

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 120, 61, 27))
        self.label_3.setObjectName("label_3")
        self.regUserPwdCfm = QtWidgets.QLineEdit(Dialog)
        self.regUserPwdCfm.setGeometry(QtCore.QRect(140, 120, 191, 27))
        self.regUserPwdCfm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.regUserPwdCfm.setObjectName("regUserPwdCfm")
        self.regUserPwdCfm.setMaxLength(8)

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(90, 160, 51, 27))
        self.label_4.setObjectName("label_4")
        self.regUserNick = QtWidgets.QLineEdit(Dialog)
        self.regUserNick.setGeometry(QtCore.QRect(140, 160, 191, 27))
        self.regUserNick.setObjectName("regUserNick")
        self.regUserNick.setMaxLength(8)

        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(60, 200, 67, 27))
        self.label_5.setObjectName("label_5")
        self.regUserBirth = QtWidgets.QLineEdit(Dialog)
        self.regUserBirth.setGeometry(QtCore.QRect(140, 200, 191, 27))
        self.regUserBirth.setObjectName("regUserBirth")
        # regExpStr = '^[1-2]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
        # regExp = QtCore.QRegExp(regExpStr)
        # # regExp = QtCore.QIntValidator()
        # self.regUserBirth.setValidator(QtGui.QRegExpValidator(regExp, self))
        # self.regUserBirth.setInputMask("0000-00-00")
        # self.regUserBirth.setCursorPosition(0)

        self.regRegBtn = QtWidgets.QPushButton(Dialog)
        self.regRegBtn.setGeometry(QtCore.QRect(80, 245, 99, 27))
        self.regRegBtn.setObjectName("regRegBtn")
        self.regResetBtn = QtWidgets.QPushButton(Dialog)
        self.regResetBtn.setGeometry(QtCore.QRect(230, 245, 99, 27))
        self.regResetBtn.setObjectName("regResetBtn")

        self.retranslateUi(Dialog)
        self.regResetBtn.clicked.connect(self.regUserName.clear)
        self.regResetBtn.clicked.connect(self.regUserPwd.clear)
        self.regResetBtn.clicked.connect(self.regUserPwdCfm.clear)
        self.regResetBtn.clicked.connect(self.regUserNick.clear)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "用户注册"))
        self.regUserName.setPlaceholderText(_translate("Dialog", "10字符以内"))
        self.regUserPwd.setPlaceholderText(_translate("Dialog", "6-12位密码"))
        self.label_2.setText(_translate("Dialog", "密码"))
        self.label.setText(_translate("Dialog", "用户名"))
        self.regUserPwdCfm.setPlaceholderText(_translate("Dialog", "6-12位密码"))
        self.label_3.setText(_translate("Dialog", "确认密码"))
        self.label_4.setText(_translate("Dialog", "昵称"))
        self.regUserNick.setPlaceholderText(_translate("Dialog",
                                                       "8字符或4中文以内"))
        self.regUserBirth.setText(_translate("Dialog", "1970-01-01"))
        self.label_5.setText(_translate("Dialog", "出生日期"))
        self.regRegBtn.setText(_translate("Dialog", "注册"))
        self.regResetBtn.setText(_translate("Dialog", "重填"))
