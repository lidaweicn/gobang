from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QRect


class Ui_DialogEmoji(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(250, 100)
        # self.move(930, 550)
        self.setWindowOpacity(0.9)

        self.setWindowFlags(Qt.SplashScreen)
        # self.setWindowFlags(Qt.CustomizeWindowHint)  # 无标题
        self.setWindowModality(Qt.NonModal)    # 不阻塞
        # self.setWindowModality(Qt.ApplicationModal)      # 阻塞整个应用程序
        self.emoji_layout = QGridLayout(self)
        self.emoji_layout.setSpacing(0)
        # self.emoji_layout.setGeometry(QtCore.QRect(0, 0, 300, 200))
        self.emoji_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.emoji_layout)

        emoji = [['😀', '😁', '😂', '😄', '😅', '😆', '😉', '😊', '😋', '😎'],
                 ['😍', '😘', '😚', '🙂', '🤗', '🤔', '🙄', '😏', '😣', '😥'],
                 ['🤐', '😯', '😪', '😫', '😴', '😌', '😛', '😜', '😝', '😒'],
                 ['😓', '🤑', '😲', '🙁', '😖', '😞', '😟', '😤', '😢', '😭'],
                 ['😧', '😨', '😩', '😬', '😰', '😱', '😳', '😵', '😡', '😠'],
                 ['😷', '🤒', '🤕', '😇', '🤓', '💀',  '👽', '💩']]
        self.btn_emoji = {}
        for row, em in enumerate(emoji):
            for col, e in enumerate(em):
                btn_key = 'btn' + str(row) + str(col)
                self.btn_emoji[btn_key] = QPushButton(e, self)
                self.btn_emoji[btn_key].setObjectName(e)
                self.btn_emoji[btn_key].setFixedSize(25, 25)
                self.btn_emoji[btn_key].setFlat(True)
                self.btn_emoji[btn_key].clicked.connect(self.get_emoji)
                # print(self.btn_emoji)
                self.emoji_layout.addWidget(self.btn_emoji[btn_key], row, col, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "emoji"))

    def get_emoji(self):
        sender = self.sender()
        print(sender)
        print(sender.text())
        self.emoji = sender.text()
        self.close()
        pass
