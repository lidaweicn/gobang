from PyQt5.QtWidgets import QFrame, QTextBrowser, QLabel
from PyQt5.QtWidgets import QTableView, QHeaderView, QMenu, QAbstractItemView
from PyQt5.QtCore import QRect, Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class UiUserShowFrame(QFrame):
    def __init__(self, parent):
        super(UiUserShowFrame, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # 用户信息
        self.setGeometry(QRect(710, 10, 301, 111))
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(2)
        self.setObjectName("uiUserShowFrame")
        self.user_image = QLabel(self)
        self.user_image.setGeometry(QRect(10, 10, 90, 90))
        self.user_image.setObjectName("userImage")
        # self.user_image.setStyleSheet("background-image: url(./img/game.bmp);")
        self.user_image.setScaledContents(True)

        # self.user_info = QTextBrowser(self)
        self.user_info = QLabel(self)
        self.user_info.setGeometry(QRect(120, 10, 171, 91))
        self.user_info.setObjectName("userInfo")


class UiUserListFrame(QFrame):
    # 用户列表右键菜单事件信号
    sign_userlist_to_menu = pyqtSignal(str, int)

    def __init__(self, parent):
        super(UiUserListFrame, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # 用户列表框架
        self.setGeometry(QRect(710, 130, 301, 231))
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(2)
        self.setObjectName("uiUserListFrame")

        # 用户列表
        self.tableView = QTableView(self)
        self.tableView.setGeometry(QRect(10, 10, 281, 212))
        self.tableView.setObjectName("tableView")
        # self.tableView.setContextMenuPolicy(3)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested[QPoint].connect(
            self.generateMenu)

    def generateMenu(self, pos):
        menu = QMenu()
        item1 = menu.addAction(u"查看信息")
        item2 = menu.addAction(u"发送消息")
        item3 = menu.addAction(u"发起对战")
        action = menu.exec_(self.tableView.mapToGlobal(pos))
        row_num = self.tableView.currentIndex().row()
        print(row_num)
        # text = self.tableView.indexAt(QPoint(row_num, 0)).data()
        if action == item1:
            self.sign_userlist_to_menu.emit('show', row_num)
            # print('查看信息', )
        elif action == item2:
            self.sign_userlist_to_menu.emit('message', row_num)
            # print('发送消息', self.tableView.indexAt(QPoint(row_num, 0)).data())
        elif action == item3:
            # print('发起对战', self.tableView.indexAt(QPoint(row_num, 0)).data())
            self.sign_userlist_to_menu.emit('fight', row_num)
        else:
            return
