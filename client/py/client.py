from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QSize, Qt, QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from threading import Thread
from py.common import *
from py.gobang import GoBangGame
from ui.ui_hall import Room
from json import dumps, loads
from hashlib import md5
from re import match
from random import randint
import struct
from py.datatransfer import DataTransfer


class ClientThread(QObject, Thread):
    '''客户端线程，只用于从服务器接收数据'''

    # 创建信号，用于将接收到的数据发送到图形界面
    sign_thread_to_game = pyqtSignal(str, str, str)
    sign_thread_to_login = pyqtSignal(str, str, str)
    sign_thread_to_register = pyqtSignal(str, str, str)

    def __init__(self, sockfd=None):
        QObject.__init__(self)
        Thread.__init__(self)
        self.sockfd = sockfd
        self.headerSize = 4
        self.isstop = False

    def stop(self, mode, content):
        if mode == 0:
            self.isstop = True
            # self.sockfd.timeout(1)
        pass

    def run(self):
        '''调用start, 运行run'''

        print('子线程运行，接收数据')
        dataBuffer = b''
        while True:
            if self.isstop:
                print('子线程结束')
                break
            try:
                recv_data = self.sockfd.recv(2048)
                if recv_data:
                    # 把数据存入缓冲区，类似于push数据
                    dataBuffer += recv_data
                    print(dataBuffer)

                    while True:
                        if len(dataBuffer) < self.headerSize:
                            print("数据包（%s Byte）小于消息头部长度，跳出小循环" %
                                  len(dataBuffer))
                            break
                        else:
                            print('0000000000000', dataBuffer)

                        # 读取包头
                        # struct中:!代表Network order，3I代表3个unsigned int数据
                        headPack = struct.unpack(
                            '!I', dataBuffer[:self.headerSize])
                        bodySize = headPack[0]
                        print('size111111111', headPack)

                        # 分包情况处理，跳出函数继续接收数据
                        if len(dataBuffer) < self.headerSize + bodySize:
                            print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" %
                                  (len(dataBuffer),
                                      self.headerSize + bodySize))
                            break
                        # 读取消息正文的内容
                        print('消息长度', len(dataBuffer))
                        bodyraw = dataBuffer[self.headerSize:
                                             self.headerSize + bodySize]
                        # print(body)

                        print('正文信息：', bodyraw)
                        body = bodyraw.decode()
                        print('正文信息：', body)
                        # 数据处理
                        # dataHandle(headPack, body)

                        # 粘包情况的处理
                        # 获取下一个数据包，类似于把数据pop出
                        dataBuffer = dataBuffer[self.headerSize + bodySize:]

                        # 用\r\n切割信息，分为命令行和内容
                        try:
                            data = body.split('\r\n')
                        except Exception as e:
                            print('数据命令切分错误', e)
                        # print('最后数据：', data)
                        # 命令行内容存储在head变量里
                        head = data[0]
                        # 内容存储在content变量里
                        content = data[1]
                        # 切割命令行信息，分解为主命令和副命令
                        heads = head.split()
                        # 主命令
                        action = heads[0]
                        # 副命令
                        action_vice = heads[1]
                        # 分发数据
                        if action == "LOGIN":
                            # 提交信号，将数据发送到登录窗口
                            self.sign_thread_to_login.emit(
                                action, action_vice, content)
                        elif action == "REGISTER":
                            # 提交信号，将数据发送到注册窗口
                            self.sign_thread_to_register.emit(
                                action, action_vice, content)
                        else:
                            # 提交信号，将数据发送到主窗口
                            self.sign_thread_to_game.emit(
                                action, action_vice, content)

            except KeyboardInterrupt:
                raise
            except BrokenPipeError:
                print("服务器断开连接")
            except Exception as e:
                print(e)
                break
                # continue
            pass
        pass


class ClientFunction(Config, DataTransfer):
    """客户端功能函数"""

    def init_function(self):
        '''初始化一些参数'''

        self.font_family = 'Ubuntu'
        self.font_point_size = 11
        self.font_bold = False
        self.font_italic = False
        self.font_weight = 50
        self.font_color = "#000000"

        self.chat_font = QtGui.QFont()
        # self.helper = CommonHelper()
        self.room_count = 0

    def message_box(self, title, msg):
        '''弹出框函数'''

        QMessageBox.information(self, title, msg,
                                QMessageBox.Ok,
                                QMessageBox.Ok)
        pass

    def readResponse(self, action, action_vice, content):
        '''槽函数，用于从线程接收数据，进行处理，显示到界面元素上'''

        # 分发数据
        if action == "CHAT":
            self.show_textbrowser(content)
            # self.ucf.textBrowser.append(content)   # 将文本添加到textBrowser
        elif action == "GOROOM":
            self.select_room_response(action, action_vice, content)
            pass
        elif action == "MODIFY":
            msg = loads(content)
            self.message_box("修改信息", msg['CheckMassage'])
            pass
        elif action == "HALL":
            if action_vice == "/fail":
                self.message_box("创建房间", "有空房间存在，不允许创建！")
                return
            self.show_hall(action, action_vice, content)
        elif action == "GAME":
            self.game_data_response(action, action_vice, content)
            pass
        elif action == "LIST":
            # 接收用户信息列表，分发到界面
            # print('用户列表')
            self.show_user_list(action, action_vice, content)
            pass
        else:
            print('接收数据错误')
        pass

    def show_hall(self, action, action_vice, content):
        # print('收到创建房间数据')
        halls = loads(content)

        top = 0
        for idx, room in halls.items():
            # print(idx, room)
            if int(idx) % 2 == 1:
                col = 0
                row = (int(idx) + 1) // 2
                y = row * 230 + 40
                top = y if y > top else top
                # print("创建房间位置", row, y)
            else:
                col = 1
                row = int(idx) // 2
                y = row * 230 + 40
                top = y if y > top else top
                # print("创建房间位置", row, y)
                pass
            try:
                rm = self.uhf.rooms[idx]
            except Exception as e:
                print(e)
                rm = Room(self.uhf.hall_widgetContents,
                          self.user, roomName="房间{}".format(idx))
                if not rm.sign_isconnect:
                    # print('连接房间信号')
                    rm.room_sign_btn.connect(self.send_select_room_data)
                    rm.sign_isconnect = True
                self.uhf.lay.addWidget(rm, row, col)
                self.uhf.rooms[idx] = rm

            self.uhf.rooms[idx].roomVSLabelL.setText(room['LeftPlayer'])
            if room['LeftPlayerImage']:
                self.uhf.rooms[idx].roomVSLeft.setText('')
            else:
                self.uhf.rooms[idx].roomVSLeft.setText('对战')
            self.uhf.rooms[idx].roomVSLeft.setStyleSheet(
                "border-image: url({});".format(room['LeftPlayerImage']))
            self.uhf.rooms[idx].roomVSLabelR.setText(room['RightPlayer'])
            if room['RightPlayerImage']:
                self.uhf.rooms[idx].roomVSRight.setText('')
            else:
                self.uhf.rooms[idx].roomVSRight.setText('对战')
            self.uhf.rooms[idx].roomVSRight.setStyleSheet(
                "border-image: url({});".format(room['RightPlayerImage']))

            self.uhf.hall_widgetContents.setMinimumSize(QSize(400, top))

        pass

    def pushbutton_click(self):
        # 用户信息头, 仅用于本地显示自己的聊天信息
        texth_head = "{} {}".format('我', self.get_time())
        # 信息内容
        text = self.ucf.lineEdit.text()     # 获取输入框文本
        if not text:
            return
        # 格式化聊天信息
        text_format = """<div style="text-align:right;{}">{}</div>"""\
            .format(self.get_font_style(), text)
        # print(text_format)

        self.ucf.textBrowser.append(texth_head)   # 将文本添加到textBrowser
        self.ucf.textBrowser.append(text_format)   # 将文本添加到textBrowser
        # 单机模式不发送数据
        # print('网络状态', self.net_status)
        if self.net_status == DISCONNECT:
            # print('单机模式，不发送聊天数据')
            self.ucf.lineEdit.clear()
            return

        action_vice = self.user.user_site
        print("发送聊天数据", action_vice)
        if action_vice == HALL:
            action_vice_str = 'hall'
        else:
            action_vice_str = str(action_vice)
        head = "CHAT /{} \r\n".format(action_vice_str)
        content = {
            'UserName': self.user.user_name,
            'NickName': self.user.user_nick,
            'FontStyle': self.get_font_style(),
            'Message': text,
            'SendTime': self.get_time(),
        }
        # msg = head + dumps(content)
        # try:
        #     self.sockfd.send(msg.encode())
        # except BrokenPipeError:
        #     print('网络连接断开')
        self.msg_send(head, content)

        self.ucf.lineEdit.clear()
        pass

    def set_time_show(self):
        '''用于单机游戏和电脑对战'''

        self.ugf.vs_user_info.setText(
            "<font style='font-size:14px;'>玩家：{}<br>棋子：黑棋<br>用时：{}s</font>"
            .format(self.user_l.user_nick, self.user_l.game_time))
        self.ugf.vs_user_info_r.setText(
            "<font style='font-size:14px;'>玩家：电脑<br>棋子：白棋<br>用时：{}s</font>"
            .format(self.user_r.game_time))
        pass

    def set_vs(self, content, mode=None):
        if mode == SINGLE:
            # print("单机设置用户")
            # 显示用户头像
            pix = QtGui.QPixmap(self.user.user_image)
            self.user.user_pix = pix
            self.ugf.vs_user_image.setPixmap(pix)
            pixr = QtGui.QPixmap(self.user_r.user_image)
            self.ugf.vs_user_image_r.setPixmap(pixr)
            self.user_l.user_nick = '单机玩家'
            self.set_time_show()
            pass
        elif mode == NETSINGLE:
            # 显示用户头像
            pix = QtGui.QPixmap(self.user_l.user_image)
            self.user_l.user_pix = pix
            self.ugf.vs_user_image.setPixmap(pix)
            userinfo = '玩家：{}<br>棋子：黑棋<br>用时：0s'.format(self.user_l.user_nick)
            self.ugf.vs_user_info.setText(
                "<font style='font-size:14px;'>{}</font>".format(userinfo))

            pixr = QtGui.QPixmap(self.user_r.user_image)
            self.ugf.vs_user_image_r.setPixmap(pixr)
            self.ugf.vs_user_info_r.setText(
                "<font style='font-size:14px;'>玩家：电脑<br>棋子：白棋<br>用时：0s</font>")
            pass
        else:
            # 显示用户头像
            pix = QtGui.QPixmap(self.user_l.user_image)
            self.user_l.user_pix = pix
            self.ugf.vs_user_image.setPixmap(pix)
            self.ugf.vs_user_info.setText(
                "<font style='font-size:14px;'>{}</font>".format(
                    self.user_l.show_info))

            pixr = QtGui.QPixmap(self.user_r.user_image)
            self.ugf.vs_user_image_r.setPixmap(pixr)
            self.ugf.vs_user_info_r.setText(
                "<font style='font-size:14px;'>{}</font>".format(
                    self.user_r.show_info))
            if self.user.user_status == WATCHING:
                if (self.user_l.user_name == '' or
                        self.user_r.user_name == ''):
                    self.ugf.gameStartBtn.setText('加入对战')
                    self.ugf.gameStartBtn.setEnabled(True)
                else:
                    self.ugf.gameStartBtn.setText('观战中')
                    self.ugf.gameStartBtn.setEnabled(False)
            pass
        pass

    def set_user(self, content, mode=WATCHING):
        # print('存储登录用户')
        # print(content)

        if mode == WATCHING:
            user_dict = loads(content)
            self.user.user_name = user_dict['UserName']
            self.user.user_nick = user_dict['NickName']
            self.user.user_image = user_dict['UserImage']
            self.user.user_level = user_dict['GameLevel']
            self.user.user_score = user_dict['GameScore']
            self.user.total_round = user_dict['TotalRound']
            self.user.win_round = user_dict['WinRound']
            self.show_user_info()

        elif mode == SINGLE:
            self.user_l.user_nick = '单机玩家'
            self.uusf.user_info.setText(
                "<font style='font-size:30px;'> 单机游戏</font>")
        else:
            print("错误数据")
        # 显示用户头像
        pix = QtGui.QPixmap(self.user.user_image)
        self.user.user_pix = pix
        self.uusf.user_image.setPixmap(pix)
        pass

    def show_user_info(self):
        # 显示用户信息
        user_info_name = "用户名：" + self.user.user_name
        user_inof_nick = "昵　称：" + self.user.user_nick
        user_info_level = "等　级：" + str(self.user.user_level)
        user_info_score = "积　分：" + str(self.user.user_score)
        # print(user_info_name)
        # print(user_info_level)
        # print(user_info_score)

        self.uusf.user_info.setText(user_info_name + "\n" +
                                    user_inof_nick + "\n" +
                                    user_info_level + "\n" +
                                    user_info_score)
        pass

    def set_style(self):
        # 更新界面样式
        self.setStyleSheet(self.QSS)
        self.set_dialog.setWindowStyleLb.setText(self.config['qss'])
        # 更新棋盘样式
        game_background = self.setting.value('board/' + self.config['board'])
        self.set_dialog.setBoardStyleLb.setText(self.config['board'])
        self.ugf.game_frame.setStyleSheet("background-image: url({});"
                                          .format(game_background))
        # 更新棋子样式
        game_piece_style = self.setting.value('piece/' + self.config['piece'])
        self.set_dialog.setPieceStyleLb.setText(self.config['piece'])
        self.piece_black = game_piece_style[0]
        self.piece_white = game_piece_style[1]
        # 设置聊天输入框颜色为字体颜色
        self.ucf.lineEdit.setStyleSheet("color:{}".format(self.font_color))
        # 处理背景音乐
        if eval(self.config['music']):
            print('播放背景音乐')
            self.background_music.play()
        else:
            self.background_music.stop()
        pass

    def show_user_list(self, action, action_vice, content):
        user_lst = loads(content)
        status = {
            '0': '无',
            '1': '对战',
            '2': '对战',
            '3': '观战',
            '4': '电脑',
            '11': '对战',
            '12': '对战',
            '13': '对战',
        }

        self.model = QStandardItemModel(len(user_lst), 8, self.uulf.tableView)
        self.model.setHorizontalHeaderLabels(
            ['昵称', '等级', '房间', '状态', '用户名', '积分', '场次', '胜场'])

        for row, usr in enumerate(user_lst.values()):
            self.model.setItem(row, 0, QStandardItem(usr['NickName']))
            self.model.setItem(
                row, 1, QStandardItem(str(usr['GameLevel']) + '级'))
            if usr['RoomId'] == 0:
                roomstr = '大厅'
            else:
                roomstr = '房间' + str(usr['RoomId'])
            self.model.setItem(
                row, 2, QStandardItem(roomstr))
            self.model.setItem(
                row, 3, QStandardItem(status[str(usr['UserStatus'])]))
            self.model.setItem(row, 4, QStandardItem(usr['UserName']))
            self.model.setItem(row, 5, QStandardItem(str(usr['GameScore'])))
            self.model.setItem(row, 6, QStandardItem(str(usr['TotalRound'])))
            self.model.setItem(row, 7, QStandardItem(str(usr['WinRound'])))
            # 设置字体居中
            for i in range(8):
                self.model.item(row, i).setTextAlignment(QtCore.Qt.AlignCenter)
            if usr['UserName'] == self.user.user_name:
                self.user.user_level = usr['GameLevel']
                self.user.user_score = usr['GameScore']
                self.user.total_round = usr['TotalRound']
                self.user.win_round = usr['WinRound']
                self.user.user_site = usr['RoomId']
                self.show_user_info()

        self.uulf.tableView.setModel(self.model)
        # 设置列宽
        if len(user_lst) >= 10:
            self.uulf.tableView.setColumnWidth(0, 88)
        elif len(user_lst) >= 7:
            self.uulf.tableView.setColumnWidth(0, 97)
        else:
            self.uulf.tableView.setColumnWidth(0, 100)
        self.uulf.tableView.setColumnWidth(1, 51)
        self.uulf.tableView.setColumnWidth(2, 51)
        self.uulf.tableView.setColumnWidth(3, 51)
        self.uulf.tableView.setColumnWidth(4, 51)
        self.uulf.tableView.setColumnWidth(5, 51)
        self.uulf.tableView.setColumnWidth(6, 51)
        self.uulf.tableView.setColumnWidth(7, 51)
        # 隐藏不需要的列
        self.uulf.tableView.hideColumn(4)
        self.uulf.tableView.hideColumn(5)
        self.uulf.tableView.hideColumn(6)
        self.uulf.tableView.hideColumn(7)
        pass

    def show_textbrowser(self, msg):
        content = loads(msg)
        show_user_msg = content['NickName'] + ' '
        show_user_msg += content['SendTime']
        show_msg = """<p style='{}'>{}</p>"""\
            .format(content['FontStyle'], content['Message'])
        # print(show_msg)
        self.ucf.textBrowser.append(show_user_msg)
        self.ucf.textBrowser.append(show_msg)
        pass

    def get_font_style(self):
        '''设置字体样式，并返回'''

        font_style = 'font-family:{};font-size:{}px;color:{};'\
            .format(self.font_family,
                    self.font_point_size + 5,
                    self.font_color)
        if self.font_bold:
            font_style += 'font-weight:bold;'
        else:
            font_style += 'font-weight:{};'.format(self.font_weight)
        if self.font_italic:
            font_style += 'font-style:italic;'
        return font_style
        pass

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        self.pushbutton_click()
        pass

    @QtCore.pyqtSlot()
    def on_toolButton_clicked(self):
        '''设置字体'''
        font, ok = QtWidgets.QFontDialog.getFont()

        self.font_family = font.family()            # 字体
        self.font_point_size = int(font.pointSize())    # 大小
        self.font_weight = font.weight()            # 粗细
        self.font_overline = font.overline()        # 上划线
        self.font_underline = font.underline()      # 下划线
        self.font_strike_out = font.strikeOut()     # 删除线
        self.font_bold = font.bold()                # 粗体
        self.font_italic = font.italic()
        self.chat_font = font

        if ok:
            self.ucf.lineEdit.setFont(font)
        pass

    @QtCore.pyqtSlot()
    def on_toolButton2_clicked(self):
        '''设置粗体'''

        if self.font_bold:
            self.font_bold = False
        else:
            self.font_bold = True
        # self.font = QtGui.QFont()
        self.chat_font.setBold(self.font_bold)
        self.ucf.lineEdit.setFont(self.chat_font)
        pass

    @QtCore.pyqtSlot()
    def on_toolButton3_clicked(self):
        '''设置斜体'''

        if self.font_italic:
            self.font_italic = False
        else:
            self.font_italic = True
        # self.font = QtGui.QFont()
        self.chat_font.setItalic(self.font_italic)
        self.ucf.lineEdit.setFont(self.chat_font)

    @QtCore.pyqtSlot()
    def on_toolButton4_clicked(self):
        '''设置颜色'''
        col = QColorDialog.getColor()
        if col.isValid():
            self.font_color = col.name()
            print(r'{}'.format(self.font_color))
            self.ucf.lineEdit.setStyleSheet("color:{}".format(col.name()))

    @QtCore.pyqtSlot()
    def on_toolButton5_clicked(self):
        '''emoji'''

        print('emoji')

        # self.emoji_dialog = Ui_DialogE(self)
        self.emoji_dialog.setGeometry(self.pos().x() + 750,
                                      self.pos().y() + 520, 250, 100)
        self.emoji_dialog.exec_()
        print(self.emoji_dialog.emoji)
        # show_emoji = self.emoji_dialog.emoji
        # text = self.ucf.lineEdit.text()
        self.ucf.lineEdit.setText(
            self.ucf.lineEdit.text() + self.emoji_dialog.emoji)

    @QtCore.pyqtSlot('QString')
    def on_comboBox_activated(self, text):
        '''快速发言下拉菜单'''

        # print('c', text)
        show_text = self.ucf.lineEdit.text() + text
        self.ucf.lineEdit.setText(show_text)
        pass

    def mousePressEvent(self, event):
        '''鼠标点击事件，用于点击棋盘操作'''

        # print(event.x(), event.y())
        if not self.isstart:
            return
        # 获取点击坐标
        click_x = event.x()
        click_y = event.y()
        # 限定坐标点击范围，即棋盘范围
        if (click_x < 130 or
            click_x > 574 or
            click_y < 197 or
                click_y > 641):
            return
        print(click_x, click_y)
        # 修正坐标原点
        modify_x = click_x - 130
        modify_y = click_y - 197
        print(modify_x, modify_y)
        # 将鼠标点击坐标转换为游戏坐标
        game_x = modify_x // 30
        game_y = modify_y // 30
        print(game_x, game_y)

        if (self.user.user_status == SINGLE or
                self.user.user_status == NETSINGLE):
            self.single_game(game_x, game_y)
        elif self.user.user_status == PLAYER1:
            if self.user.user_site == HALL:
                return
            self.send_game_data(game_x, game_y)
            pass
        elif self.user.user_status == PLAYER2:
            if self.user.user_site == HALL:
                return
            self.send_game_data(game_x, game_y)
            pass
        elif self.user.user_status == WATCHING:
            pass
        pass

    def send_game_data(self, x, y):
        '''发送游戏数据'''

        print("发送game数据")
        if self.user.user_status == PLAYER1:
            use_time = 20 - self.time_l
            self.time_l = 20
        elif self.user.user_status == PLAYER2:
            use_time = 20 - self.time_r
            self.time_r = 20
        head = "GAME /game \r\n"
        content = {
            'UserName': self.user.user_name,
            'GamePos': (x, y),
            'RoomId': self.user.user_site,
            'UseTime': use_time,
        }
        # msg = head + dumps(content)
        # self.sockfd.send(msg.encode())
        self.msg_send(head, content)
        pass

    def game_data_response(self, action, action_vice, content):
        '''接收游戏数据，进行处理函数'''

        content_dict = loads(content)

        # 判断副命令
        if action_vice == "/ready":
            # 对方发送就绪信息，或直接显示到对战信息区域
            print('对方就绪')
        elif action_vice == "/game":
            # 接收对方发送的游戏坐标到界面
            print('游戏')
        elif action_vice == "/start":
            # 接收对方点击游戏开始
            print('开始')
            self.user.game_status = content_dict['GameStatus']
        elif action_vice == "/undo":
            # 对方发送悔棋请求，或对方回复悔棋请求
            print('悔棋')
            if content_dict['UndoStatus'] == 'request':
                reply = QMessageBox.question(self,
                                             "游戏信息", "对方请求悔棋，您是否同意？",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                print('是否同意悔棋：', reply)
                if reply == QMessageBox.Yes:
                    response = 'yes'
                else:
                    response = 'no'
                    pass

                head = "GAME /undo \r\n"
                content = {
                    'UserName': self.user.user_name,
                    'UndoStatus': response
                }
                # 将命令行数据和内容数据连接成发送数据的字符串
                # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
                # self.sockfd.send(msg_send.encode())
                self.msg_send(head, content)
                print(msg_send)
            elif content_dict['UndoStatus'] == 'yes':
                self.message_box('游戏信息', '悔棋成功')
            elif content_dict['UndoStatus'] == 'no':
                self.message_box('游戏信息', '悔棋失败，对方不同意悔棋')
        elif action_vice == "/giveup":
            # 对方认输
            print('对方认输')
            self.user.game_status = OVER
            self.ugf.gameStartBtn.setText('开始游戏')
            self.ugf.gameStartBtn.setEnabled(True)
            if self.user.user_nick == content_dict['GiveupPlayer']:
                self.message_box('游戏信息', '很遗憾，您认输了！')
            else:
                self.message_box('游戏信息', '对方认输，您赢了')

        elif action_vice == '/info':
            self.user_l.user_name = content_dict['LeftPlayer']
            self.user_l.user_nick = content_dict['LeftPlayerNick']
            self.user_l.user_image = content_dict['LeftPlayerImage']
            self.user_l.game_status = content_dict['LeftPlayerStatus']
            self.user_r.user_name = content_dict['RightPlayer']
            self.user_r.user_nick = content_dict['RightPlayerNick']
            self.user_r.user_image = content_dict['RightPlayerImage']
            self.user_r.game_status = content_dict['RightPlayerStatus']

            if self.user.game_status != START:
                if self.user.user_status == PLAYER1:
                    self.user.game_status = content_dict['LeftPlayerStatus']
                elif self.user.user_status == PLAYER2:
                    self.user.game_status = content_dict['RightPlayerStatus']
                elif self.user.user_status == WATCHING:
                    self.user.game_status = WATCH
                    if (self.user_l.user_name == '' or
                            self.user_r.user_name == ''):
                        self.ugf.gameStartBtn.setText('加入对战')
                        pass
                    else:
                        self.ugf.gameStartBtn.setText('观战中')
                        self.ugf.gameStartBtn.setEnabled(False)
                        self.ugf.gameUndoBtn.setEnabled(False)
                        self.ugf.gameGiveupBtn.setEnabled(False)
                        pass
                else:
                    pass

            status_lst = {
                '11': '已准备',
                '1': '未准备',
                '12': '白棋',
                '13': '黑棋',
                '0': '未准备'
            }
            self.user_l.show_info = '玩家：{}<br>状态：{}<br>用时：{}s<br>'.format(
                self.user_l.user_nick, status_lst[
                    str(content_dict['LeftPlayerStatus'])],
                content_dict['TotalTimeLeft'])
            self.user_r.show_info = '玩家：{}<br>状态：{}<br>用时：{}s<br>'.format(
                self.user_r.user_nick, status_lst[
                    str(content_dict['RightPlayerStatus'])],
                content_dict['TotalTimeRight'])

            # print('下棋用户', content_dict['TimerStart'])
            # print('左边用户名', self.user_l.user_name)
            # print('右边用户名', self.user_r.user_name)
            # 处理时钟
            if self.isstart:
                if content_dict['TimerStart'] == self.user_l.user_name:
                    # print('左边定时器开始')
                    self.time_l = 20
                    self.timer_r.stop()
                    self.timer_l.start()
                elif content_dict['TimerStart'] == self.user_r.user_name:
                    # print('右边定时器开始')
                    self.time_r = 20
                    self.timer_l.stop()
                    self.timer_r.start()

            self.set_vs('content')
            self.board_info = content_dict['GogangInfo']
            self.update_board(self.board_info)
            if self.user.game_status == WHITE:
                self.user.game_status = START
                self.isstart = True
                self.ugf.gameStartBtn.setText('游戏中')
                self.message_box('游戏信息', '您使用的是白棋，请等待对方先落子')
            elif self.user.game_status == BLACK:
                self.user.game_status = START
                self.isstart = True
                self.ugf.gameStartBtn.setText('游戏中')
                self.message_box('游戏信息', '您使用的是黑棋，请您先落子')
            elif self.user.game_status == WATCH:
                if ((self.user_l.game_status in [WHITE, BLACK]) and
                        (self.user_r.game_status in [WHITE, BLACK])):
                    self.isstart = True
            elif self.user.game_status == START:
                if not self.isstart:
                    self.isstart = True
            else:
                pass

            if content_dict['Winner']:
                if content_dict['ATie']:
                    gameinfo = '游戏结束，和棋，{}总用时短赢了'\
                        .format(content_dict['Winner'])
                    self.ucf.textBrowser.append(
                        '<p style="color:red">系统信息：{}</p>'.format(gameinfo))
                    self.isstart = False
                else:
                    gameinfo = '游戏结束，{}赢了'.format(content_dict['Winner'])
                    self.ucf.textBrowser.append(
                        '<p style="color:red">系统信息：{}</p>'.format(gameinfo))
                    self.isstart = False
                # 玩家弹框
                if self.user.user_status == PLAYER1:
                    if content_dict['Winner'] == self.user.user_nick:
                        msgbox_info = '游戏结束，你赢了'
                        if content_dict['LevelUpLeft']:
                            msgbox_info += '\n恭喜您升级了'
                    else:
                        msgbox_info = '游戏结束，你输了'
                    self.user.game_status = OVER
                    self.timer_l.stop()
                    self.timer_r.stop()
                    self.ugf.gameStartBtn.setText('开始游戏')
                    self.ugf.gameStartBtn.setEnabled(True)
                    self.message_box('游戏信息', msgbox_info)

                elif self.user.user_status == PLAYER2:
                    if content_dict['Winner'] == self.user.user_nick:
                        msgbox_info = '游戏结束，你赢了'
                        if content_dict['LevelUpRight']:
                            msgbox_info += '\n恭喜您升级了'
                    else:
                        msgbox_info = '游戏结束，你输了'
                    self.user.game_status = OVER
                    self.timer_l.stop()
                    self.timer_r.stop()
                    self.ugf.gameStartBtn.setText('开始游戏')
                    self.ugf.gameStartBtn.setEnabled(True)
                    self.message_box('游戏信息', msgbox_info)

            if content_dict['GiveupPlayer']:
                self.timer_l.stop()
                self.timer_r.stop()
                gameinfo = '游戏结束，{}认输了'.format(content_dict['GiveupPlayer'])
                self.ucf.textBrowser.append(
                    '<p style="color:red">系统信息：{}</p>'.format(gameinfo))
                self.isstart = False
        else:
            print('接收数据错误')

    def update_board(self, gobanginfo):
        # print('开始清空棋盘')
        # self.init_board()
        # 播放落子声音
        if eval(self.config['sound']):
            self.sound_piece.play()

        # print('开始画棋子')
        for x in range(15):
            for y in range(15):
                s = str(x) + 'x' + str(y)
                if gobanginfo[x][y] == 1:
                    # pix = QtGui.QPixmap('game.bmp')
                    pix = QtGui.QPixmap(self.piece_black)
                    self.label[s].setPixmap(pix)
                elif gobanginfo[x][y] == 2:
                    # pix = QtGui.QPixmap('game.bmp')
                    pix = QtGui.QPixmap(self.piece_white)
                    self.label[s].setPixmap(pix)
                else:
                    # pix = QtGui.QPixmap("")
                    # pix = QtGui.QPixmap('./img/none.png')
                    self.label[s].clear()
        # print('画完棋子')
        pass

    def single_game(self, x, y):
        '''单机游戏'''

        if self.gbg.over:
            self.message_box("游戏", "{}赢了".format(self.gbg.winner))
            return
        # 判断坐标点是否有棋子
        if self.gbg.is_null(x, y):
            return False
        # 播放落子声音
        if eval(self.config['sound']):
            self.sound_piece.play()
        # 调用方法画棋子
        self.draw_gobang(x, y, 'b')
        self.user_l.game_time += 20 - self.time_l
        self.time_l = 20
        self.timer_l.stop()
        self.timer_r.start()
        self.set_time_show()
        # 调用电脑画棋子
        self.draw_gobang(*self.gbg.do_game(x, y))
        self.user_r.game_time += 20 - self.time_r
        self.time_r = 20
        self.timer_r.stop()
        self.timer_l.start()
        self.set_time_show()
        if self.gbg.over:
            self.time_l = 20
            self.time_r = 20
            self.timer_l.stop()
            self.timer_r.stop()
            self.isstart = False
            self.message_box("游戏", "{}赢了".format(self.gbg.winner))
        return True
        pass

    def init_game(self):
        '''初始化游戏'''
        self.label = {}
        self.me = True
        self.isstart = False
        self.game_pieces = set()
        self.game_pieces_p1 = set()
        self.game_pieces_p2 = set()
        self.game_pieces = self.game_pieces_p1 | self.game_pieces_p2
        self.gbg = GoBangGame()

        # 新建一个QTimer对象
        self.timer_l = QtCore.QTimer()
        self.timer_l.setInterval(1000)
        # self.timer_l.start()
        self.timer_r = QtCore.QTimer()
        self.timer_r.setInterval(1000)
        # self.timer_r.start()
        # 计时器初始化时间
        self.time_l = 20
        self.time_r = 20

        # 信号连接到槽
        self.timer_l.timeout.connect(self.onTimerOutL)
        self.timer_r.timeout.connect(self.onTimerOutR)

        self.layout = QtWidgets.QWidget(self.ugf.game_frame)
        self.layout.setGeometry(QtCore.QRect(28, 28, 473, 473))
        self.layout.setObjectName("layout")
        self.gridLayout = QtWidgets.QGridLayout(self.layout)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.layout.setStyleSheet("background-image: url(./img/none.png);")

        self.init_board()
        pass

    def init_board(self):
        '''初始化棋盘'''

        for x in range(16):     # 棋盘行列个加一空行和列，处理最右边和最底部棋子被遮挡问题
            for y in range(16):
                s = str(x) + 'x' + str(y)
                # print(s)
                self.label[s] = QLabel(self.layout)
                self.label[s].setFixedSize(30, 30)
                self.label[s].setContentsMargins(0, 0, 0, 0)
                self.gridLayout.addWidget(self.label[s], y, x, 1, 1)
                self.label[s].setScaledContents(True)
                # self.label[s].setPixmap(QtGui.QPixmap(''))
                self.label[s].setStyleSheet(
                    "background-image: url(./img/none.png);")
        pass

    def onTimerOutL(self):
        '''左边玩家时钟处理函数'''

        self.ugf.lcdNumber_l.display(self.time_l)
        if self.time_l > 0:
            self.time_l -= 1
        else:
            self.timer_l.stop()
            # self.time_l = 20
            self.time_out(status=PLAYER1)
        pass

    def onTimerOutR(self):
        '''右边玩家时钟处理函数'''

        self.ugf.lcdNumber_r.display(self.time_r)
        if self.time_r > 0:
            self.time_r -= 1
        else:
            self.timer_r.stop()
            # self.time_r = 20
            self.time_out(status=PLAYER2)
        pass

    def time_out(self, status=SINGLE):
        '''时间到未做操作处理函数'''

        print('时间到函数')
        if status == SINGLE:
            while True:
                x = randint(0, 14)
                y = randint(0, 14)
                if self.single_game(x, y):
                    break
                pass
        else:
            print('时间到')
            if self.user.user_status == status:
                while True:
                    x = randint(0, 14)
                    y = randint(0, 14)
                    if not self.board_info[x][y]:
                        break
                self.send_game_data(x, y)
                print('时间到发送游戏数据', x, y)
        pass

    def game_reset(self):
        self.gbg.game_reset()
        self.me = True
        self.game_pieces = set()
        self.game_pieces_p1 = set()
        self.game_pieces_p2 = set()
        self.game_pieces = self.game_pieces_p1 | self.game_pieces_p2
        self.time_l = 20
        self.time_r = 20
        self.timer_l.stop()
        self.timer_r.stop()
        self.ugf.lcdNumber_l.display(self.time_l)
        self.ugf.lcdNumber_r.display(self.time_r)
        self.user_l.game_time = 0
        self.user_r.game_time = 0
        self.set_time_show()
        for k in self.label:
            self.label[k].setPixmap(QtGui.QPixmap(''))
        pass

    def draw_gobang(self, x, y, bw):

        # 处理none.png
        # img = QtGui.QImage()
        # img.load("light_black.png")
        # img.save("light_black1.png")

        s = str(x) + 'x' + str(y)
        if s in self.game_pieces:
            print('存在')
            return

        # print(self.game_pieces)
        # print(self.game_pieces_p1)

        self.game_pieces_p1.add(s)
        self.game_pieces = self.game_pieces_p1 | self.game_pieces_p2

        if bw == 'b':
            # pix = QtGui.QPixmap('game.bmp')
            pix = QtGui.QPixmap(self.piece_black)
        else:
            # pix = QtGui.QPixmap('game.bmp')
            pix = QtGui.QPixmap(self.piece_white)
        self.me = not self.me
        self.label[s].setPixmap(pix)
        pass

    def send_select_room_data(self, room, position):
        print('点击对战按钮数据', room, position)
        room_id = int(room[2:])
        # print('room_id:----------------', room_id)
        head = "GOROOM / \r\n"
        content = {
            'UserName': self.user.user_name,
            'RoomId': room_id,
            'Position': position,
        }
        # 将命令行数据和内容数据连接成发送数据的字符串
        # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
        # print(msg_send)
        # 发送登录数据到服务器
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    def select_room_response(self, action, action_vice, content):
        room_dict = loads(content)
        # print("选择房间返回信息", room_dict)
        if action_vice == "/ok":
            self.user.user_status = room_dict['Position']
            self.user.user_site = room_dict['RoomId']
            self.ugf.gameStartBtn.setText('开始游戏')
            self.ugf.gameStartBtn.setEnabled(True)
            self.ugf.gameUndoBtn.setEnabled(True)
            self.ugf.gameGiveupBtn.setEnabled(True)
            self.isstart = False
            self.set_vs('content')
            roominfo = "《==人人对战房间{}==》".format(room_dict['RoomId'])
            self.ugf.game_info.setText(roominfo)
            self.stackedWidget.setCurrentIndex(1)
            pass
        elif action_vice == '/info':
            self.user_l.user_nick = room_dict['LeftPlayer']
            self.user_l.user_image = room_dict['LeftPlayerImage']
            self.user_r.user_nick = room_dict['RightPlayer']
            self.user_r.user_image = room_dict['RightPlayerImage']
            status_lst = {
                '11': '已准备',
                '1': '未准备',
                '12': '白棋',
                '0': '未准备',
                '13': '黑棋',
            }
            self.user_l.show_info = '玩家：{}<br>状态：{}<br>用时：0s<br>'.format(
                self.user_l.user_nick, status_lst[
                    str(room_dict['LeftPlayerStatus'])])
            self.user_r.show_info = '玩家：{}<br>状态：{}<br>用时：0s<br>'.format(
                self.user_r.user_nick, status_lst[
                    str(room_dict['RightPlayerStatus'])])

            self.set_vs('content')
            pass
        elif action_vice == '/challenge':
            if room_dict['ChallengeStatus'] == 'no':
                self.message_box('游戏信息', '对方不同意与你对战')
            elif room_dict['ChallengeStatus'] == 'request':
                reply = QMessageBox.question(self,
                                             "游戏信息", "{}请求与你对战，您是否同意？".format(
                                                 room_dict['UserNick']),
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                print('是否同意悔棋：', reply)
                if reply == QMessageBox.Yes:
                    response = 'yes'
                else:
                    response = 'no'
                head = 'GOROOM /challenge \r\n'
                content = {
                    'UserName': room_dict['UserName'],
                    'EnemyName': room_dict['EnemyName'],
                    'ChallengeStatus': response
                }
                self.msg_send(head, content)
            pass
        elif action_vice == '/fail':
            self.message_box('游戏信息', room_dict['FailMsg'])
            pass
        else:
            pass
        pass

    # ##################################################################################
    # ####                        游戏或大厅界面底部按钮
    # ##################################################################################
    @QtCore.pyqtSlot()
    def on_gameStartBtn_clicked(self):
        '''开始按钮'''

        print('点击开始按钮')
        if self.isstart:
            return
        print('点击开始按钮2', self.isstart,
              self.user.user_status, self.user.user_site)

        if (self.user.user_status == SINGLE or
                self.user.user_status == NETSINGLE):
            if not self.isstart:
                self.isstart = True
                self.ugf.gameStartBtn.setText('重新开始')

            if not self.gbg.over:
                return

            self.game_reset()
        elif (self.user.user_status == PLAYER1 or
                self.user.user_status == PLAYER2):
            head = 'GAME /start \r\n'
            content = {
                'UserName': self.user.user_name,
            }
            # msg_send = head + dumps(content) + "\r\n"
            # self.sockfd.send(msg_send.encode())
            self.msg_send(head, content)
            self.ugf.gameStartBtn.setText('等待对方')
            self.ugf.gameStartBtn.setEnabled(False)
            pass
        elif self.user.user_status == WATCHING:
            print('加入对战')
            if self.user_l.user_name == '':
                position = PLAYER1
            elif self.user_r.user_name == '':
                position = PLAYER2
            else:
                position = WATCHING
            head = "GOROOM /inroom \r\n"
            content = {
                'UserName': self.user.user_name,
                'RoomId': self.user.user_site,
                'Position': position,
            }
            # 将命令行数据和内容数据连接成发送数据的字符串
            # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
            # print(msg_send)
            # 发送登录数据到服务器
            # self.sockfd.send(msg_send.encode())
            self.msg_send(head, content)
            pass
        pass

    @QtCore.pyqtSlot()
    def on_gameUndoBtn_clicked(self):
        '''悔棋按钮'''

        print('悔棋')
        if (self.user.user_status == PLAYER1 or
                self.user.user_status == PLAYER2):
            head = "GAME /undo \r\n"
            content = {
                'UserName': self.user.user_name,
                'UndoStatus': 'request'
                # 'RoomId': rooms[room],
                # 'Position': position,
            }
            # 将命令行数据和内容数据连接成发送数据的字符串
            # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
            # self.sockfd.send(msg_send.encode())
            # print(msg_send)
            self.msg_send(head, content)
        pass

    @QtCore.pyqtSlot()
    def on_gameGiveupBtn_clicked(self):
        '''认输按钮'''

        print('认输')
        if not self.isstart:
            return
        if (self.user.user_status == PLAYER1 or
                self.user.user_status == PLAYER2):
            head = "GAME /giveup \r\n"
            content = {
                'UserName': self.user.user_name,
            }
            # 将命令行数据和内容数据连接成发送数据的字符串
            # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
            # self.sockfd.send(msg_send.encode())
            # print(msg_send)
            self.msg_send(head, content)
        pass

    @QtCore.pyqtSlot()
    def on_gameReHallBtn_clicked(self):
        '''返回大厅'''

        print('返回大厅')

        if self.user.user_status == NETSINGLE:
            self.isstart = False
            self.game_reset()
            self.ugf.gameStartBtn.setText('开始游戏')
        else:
            if (self.user.game_status == START):
                reply = QMessageBox.question(self,
                                             "游戏信息",
                                             "您正在对战中，如果返回大厅自动认输，您是否确认返回大厅？",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.Yes)
                if reply == QMessageBox.No:
                    return
            self.on_gameGiveupBtn_clicked()

        head = "GAME /returnhall \r\n"
        content = {
            'UserName': self.user.user_name,
            # 'RoomId': rooms[room],
            # 'Position': position,
        }
        # 将命令行数据和内容数据连接成发送数据的字符串
        # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
        # self.sockfd.send(msg_send.encode())
        # print(msg_send)
        self.msg_send(head, content)
        self.user.user_status = SINGLE
        self.user.user_site = HALL
        self.stackedWidget.setCurrentIndex(0)

    @QtCore.pyqtSlot()
    def on_gameSetBtn_clicked(self):
        '''游戏界面设置按钮'''

        self.window_set()
        pass

    @QtCore.pyqtSlot()
    def on_hallSetBtn_clicked(self):
        ''''大厅界面设置按钮'''

        self.window_set()

    def window_set(self):
        # 加载配置文件各项，显示到设置界面上
        self.setting.beginGroup("qss")
        ck = self.setting.childKeys()
        self.set_dialog.setWindowStyle.clear()
        for k in ck:
            self.set_dialog.setWindowStyle.addItem(k)
        self.setting.endGroup()
        self.setting.beginGroup('board')
        ck = self.setting.childKeys()
        self.set_dialog.setBoardStyle.clear()
        for k in ck:
            self.set_dialog.setBoardStyle.addItem(k)
        self.setting.endGroup()
        self.setting.beginGroup('piece')
        ck = self.setting.childKeys()
        self.set_dialog.setPieceStyle.clear()
        for k in ck:
            self.set_dialog.setPieceStyle.addItem(k)
        self.setting.endGroup()
        music = self.setting.value('setting/music')
        self.set_dialog.setMusic.setChecked(eval(music))
        sound = self.setting.value('setting/sound')
        self.set_dialog.setSound.setChecked(eval(sound))
        ip = self.setting.value('setting/server')
        self.set_dialog.setIP.setText(ip)
        port = self.setting.value('setting/port')
        self.set_dialog.setPort.setText(str(port))
        self.set_dialog.exec_()
        pass

    @QtCore.pyqtSlot('QString')
    def on_setWindowStyle_activated(self, text):
        print('设置界面风格', text)
        self.setting.setValue('setting/qss', text)
        self.setting.sync()
        self.load_config()
        self.set_style()
        pass

    @QtCore.pyqtSlot('QString')
    def on_setBoardStyle_activated(self, text):
        print('设置棋盘样式', text)
        self.setting.setValue('setting/board', text)
        self.setting.sync()
        self.load_config()
        self.set_style()
        pass

    @QtCore.pyqtSlot('QString')
    def on_setPieceStyle_activated(self, text):
        print('设置棋子样式', text)
        self.setting.setValue('setting/piece', text)
        self.setting.sync()
        self.load_config()
        self.set_style()
        pass

    @QtCore.pyqtSlot()
    def on_setMusic_clicked(self):
        music = self.set_dialog.setMusic.isChecked()
        self.setting.setValue('setting/music', str(music))
        self.setting.sync()
        self.load_config()
        self.set_style()
        pass

    @QtCore.pyqtSlot()
    def on_setSound_clicked(self):
        sound = self.set_dialog.setSound.isChecked()
        self.setting.setValue('setting/sound', str(sound))
        self.setting.sync()
        self.load_config()
        self.set_style()
        pass

    @QtCore.pyqtSlot()
    def on_setSave_clicked(self):
        print("保存设置")
        # 正则表达式匹配IP地址和网址
        ip_regex = '^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$'
        url_regex = '^(gobang.\w+(.com|.cn|.com.cn))$'
        ip = self.set_dialog.setIP.text()

        ip_test = match(ip_regex, ip)
        url_test = match(url_regex, ip)
        server = ''
        try:
            server = ip_test.group()
            server = ip
        except Exception:
            pass
        try:
            server = url_test.group()
            server = ip
        except Exception:
            pass
        if not server:
            # print('ip fail')
            self.message_box("设置", "服务器地址错误，请重新输入")
            return
        try:
            port = int(self.set_dialog.setPort.text())
        except Exception:
            port = 10101
        self.setting.setValue('setting/server', server)
        if port > 65535:
            self.message_box("设置", "端口错误！，请重新输入")
            return
        self.setting.setValue('setting/port', port)
        self.setting.sync()
        self.set_dialog.close()
        pass

    @QtCore.pyqtSlot()
    def on_setReset_clicked(self):
        print("恢复默认")
        self.setting.setValue('setting/qss', 'style0')
        self.setting.setValue('setting/board', 'board0')
        self.setting.setValue('setting/piece', 'piece0')
        self.setting.setValue('setting/music', 'True')
        self.setting.setValue('setting/sound', 'True')
        self.setting.sync()
        self.load_config()
        self.set_style()
        self.setStyleSheet(self.QSS)
        pass

    @QtCore.pyqtSlot()
    def on_hallFastJoin_clicked(self):
        print('快速游戏')
        # self.stackedWidget.setCurrentIndex(1)
        head = "GOROOM /fast \r\n"
        content = {'UserName': self.user.user_name}
        # msg_send = head + dumps(content) + "\r\n"
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    @QtCore.pyqtSlot()
    def on_hallUserInfo_clicked(self):
        print('用户信息')
        # 计算胜率
        if self.user.total_round:
            win_rate = int(self.user.win_round) * \
                100 // int(self.user.total_round)
        else:
            win_rate = '0'
        self.setting.beginGroup("image")
        ck = self.setting.childKeys()
        self.userinfo_dialog.userImageList.clear()
        for k in ck:
            self.userinfo_dialog.userImageList.addItem(k)
        self.setting.endGroup()
        userinfo = "<span>用户名：{}</span><br>".format(self.user.user_name) +\
            "<span>昵称：{}</span><br>".format(self.user.user_nick) +\
            "<span>等级：{}级 积分：{}</span><br>".format(
                str(self.user.user_level), str(self.user.user_score)) +\
            "<span>场次：{} 胜率：{}%</span>".format(self.user.total_round, win_rate)
        self.userinfo_dialog.userInfo.setText(userinfo)
        # 加载头像
        pix = QtGui.QPixmap(self.user.user_image)
        self.userinfo_dialog.userImage.setPixmap(pix)
        self.userinfo_dialog.exec_()
        pass

    @QtCore.pyqtSlot('QString')
    def on_userImageList_activated(self, text):
        print('用户头像', text)
        self.set_image_temp = self.setting.value('image/' + text)
        # print(image)
        pix = QtGui.QPixmap(self.set_image_temp)
        self.userinfo_dialog.userImage.setPixmap(pix)
        pass

    @QtCore.pyqtSlot()
    def on_hallConsoleGame_clicked(self):
        print('与电脑对战')
        self.user_l = self.user
        self.user_l.user_status = NETSINGLE
        self.game_status = OVER
        self.ugf.gameUndoBtn.setEnabled(False)
        self.ugf.gameGiveupBtn.setEnabled(False)
        self.user_r.user_image = 'img/user/robot.png'
        self.set_vs('content', NETSINGLE)

        head = "GOROOM / \r\n"
        content = {
            'UserName': self.user.user_name,
            'RoomId': '999',
            'Position': NETSINGLE,
        }
        # 将命令行数据和内容数据连接成发送数据的字符串
        # msg_send = head + dumps(content)    # 将数据内容字典转换为json字符串
        # print(msg_send)
        # 发送登录数据到服务器
        # try:
        #     self.sockfd.send(msg_send.encode())
        # except Exception as e:
        #     print(e)
        self.msg_send(head, content)

        roominfo = "《==电脑对战房间==》"
        print(roominfo)
        self.game_reset()
        self.ugf.game_info.setText(roominfo)
        self.stackedWidget.setCurrentIndex(1)
        pass

    @QtCore.pyqtSlot()
    def on_hallCreateRoom_clicked(self):
        print('创建房间')
        head = "HALL /create \r\n"
        content = {"NoData": None}
        # msg_send = head + dumps(content) + "\r\n"
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    @QtCore.pyqtSlot()
    def on_userImageChange_clicked(self):
        print('修改用户头像')
        head = "MODIFY /image \r\n"
        content = {
            "UserName": self.user.user_name,
            "UserImage": self.set_image_temp,
        }
        # print("937:", content)
        # msg_send = head + dumps(content) + "\r\n"
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    @QtCore.pyqtSlot()
    def on_userNickBtn_clicked(self):
        print('修改用户昵称')
        head = "MODIFY /nick \r\n"
        content = {
            "UserName": self.user.user_name,
            "NickName": self.userinfo_dialog.userNick.text(),
        }
        # msg_send = head + dumps(content) + "\r\n"
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    @QtCore.pyqtSlot()
    def on_passwdChange_clicked(self):
        print('修改用户密码')
        new_passwd = self.userinfo_dialog.newPasswd.text()
        new_passwdcfm = self.userinfo_dialog.newPasswdCfm.text()
        if new_passwd != new_passwdcfm:
            self.message_box("修改信息", "两次输入的新密码不一致")
            return
        head = "MODIFY /password \r\n"
        old_passwd = self.userinfo_dialog.oldPasswd.text()
        content = {
            "UserName": self.user.user_name,
            "OldPassword": md5(old_passwd.encode()).hexdigest(),
            "NewPassword": md5(new_passwd.encode()).hexdigest(),
        }
        # msg_send = head + dumps(content) + "\r\n"
        # self.sockfd.send(msg_send.encode())
        self.msg_send(head, content)
        pass

    def custom_menu(self, action, row):
        '''用户列表右键菜单处理函数'''
        # nick = self.model.record(row).value(0).toString()
        nick = self.model.item(row, 0).text()

        print(action, row, nick)
        if action == 'show':
            total_round = int(self.model.item(row, 6).text())
            win_round = int(self.model.item(row, 7).text())
            print(total_round, win_round)
            if total_round:
                win_rate = str(win_round * 100 // total_round)
            else:
                win_rate = '0'

            user_info = (
                self.model.item(row, 0).text(),
                self.model.item(row, 1).text(),
                self.model.item(row, 5).text(),
                self.model.item(row, 6).text(),
                win_rate,
            )
            msg_show = '昵称：{}\n等级：{}\n积分：{}分\n场次：{} 胜率：{}%'.format(*user_info)
            self.message_box('显示用户信息', msg_show)
            pass
        elif action == 'message':
            self.ucf.lineEdit.clear()
            self.ucf.lineEdit.setText('@' + nick + ' ')
            pass
        elif action == 'fight':
            if self.model.item(row, 4).text() == self.user.user_name:
                return
            head = 'GOROOM /challenge \r\n'
            content = {
                'UserName': self.user.user_name,
                'EnemyName': self.model.item(row, 4).text(),
                'UserNick': self.user.user_nick,
                'ChallengeStatus': 'request'
            }
            self.msg_send(head, content)
            pass
        else:
            pass
