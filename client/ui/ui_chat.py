from PyQt5.QtWidgets import QFrame, QTextBrowser, QToolButton
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton
from PyQt5.QtCore import QRect


class UiChatFrame(QFrame):
    def __init__(self, parent):
        super(UiChatFrame, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        # 聊天界面
        self.setGeometry(QRect(710, 370, 301, 371))
        # self.setStyleSheet("border-color: rgb(0, 255, 255);")
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(2)
        self.setObjectName("uiChatFrame")
        # 聊天显示框
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setGeometry(QRect(10, 10, 281, 281))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setOpenExternalLinks(True)     # 打开外部链接
        # 字体设置按钮
        self.toolButton = QToolButton(self)
        self.toolButton.setGeometry(QRect(10, 300, 24, 25))
        self.toolButton.setObjectName("toolButton")
        # 字体设置按钮
        self.toolButton2 = QToolButton(self)
        self.toolButton2.setGeometry(QRect(40, 300, 24, 25))
        self.toolButton2.setObjectName("toolButton2")
        # 字体设置按钮
        self.toolButton3 = QToolButton(self)
        self.toolButton3.setGeometry(QRect(70, 300, 24, 25))
        self.toolButton3.setObjectName("toolButton3")
        # 字体设置按钮
        self.toolButton4 = QToolButton(self)
        self.toolButton4.setGeometry(QRect(100, 300, 24, 25))
        self.toolButton4.setObjectName("toolButton4")
        # 字体设置按钮
        self.toolButton5 = QToolButton(self)
        self.toolButton5.setGeometry(QRect(130, 300, 24, 25))
        self.toolButton5.setObjectName("toolButton5")
        # 下拉列表
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(QRect(160, 300, 131, 27))
        # self.comboBox.setInsertPolicy(QComboBox.InsertAtBottom)
        # self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.setObjectName("comboBox")
        # self.comboBox.addItem("请选择...")
        self.comboBox.addItem("你在干嘛！！")
        self.comboBox.addItem("快点时间到了")
        self.comboBox.addItem("你要输了！！")
        self.comboBox.addItem("快点认输吧！！")
        self.comboBox.addItem("我要赢了！！！")
        # self.comboBox.setCurrentText("请选择...")
        # 聊天输入框
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(10, 335, 221, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("输入聊天信息")
        self.lineEdit.setClearButtonEnabled(True)
        # 发送按钮
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(240, 335, 50, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setShortcut('Return')  # shortcut key
        # self.pushButton.clicked.connect(self.pushbutton_click)
