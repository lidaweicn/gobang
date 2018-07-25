from json import dumps
from struct import pack, unpack


class DataTransfer(object):
    """数据传输类"""

    # def __init__(self, sockfd):
    #     self.sockfd = sockfd
    #     self.headerSize = 4

    def msg_recv(self):
        # while True:
        #     try:
        #         recv_data = self.sockfd.recv(2048).decode()
        #         if recv_data:
        #         # 把数据存入缓冲区，类似于push数据
        #         dataBuffer += recv_data





        # print(dataBuffer)
        # headPack = unpack('!I', dataBuffer[:self.headerSize])
        # bodySize = headPack[0]
        # print(headPack, bodySize)

        # # 分包情况处理，跳出函数继续接收数据
        # # if len(dataBuffer) < self.headerSize + bodySize:
        # #     print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" %
        # #           (len(dataBuffer), self.headerSize + bodySize))
        # #     break
        # # 读取消息正文的内容
        # body = dataBuffer[self.headerSize:
        #                   self.headerSize + bodySize]
        # print(body)
        return

    def msg_send(self, head, content):
        # 封装数据到消息体
        msg_body = head + dumps(content)    # 将数据内容字典转换为json字符串
        print(msg_body)
        # 获取消息体数据长度
        header = msg_body.__len__()
        # 定义报文头，包含消息体数据长度
        head_pack = pack("!I", header)
        # 消息报文，消息头+消息体
        send_data = head_pack + msg_body.encode()
        print(send_data)
        # 发送登录数据到服务器
        self.sockfd.send(send_data)
        # self.msg_recv(send_data + b'sssss')
        pass


def main():
    dt = DataTransfer('sockfd')
    # 将发送的数据封装在head和content变量中
    head = "LOGIN / \r\n"      # 命令行参数
    # 发送的数据内容，封装为字典
    content = {
        'UserName': 'aaaaaaaaaaa',
        'Password': 'bbbbbbbbbbbbb',
    }
    dt.msg_send(head, content)
    pass


if __name__ == '__main__':
    main()
