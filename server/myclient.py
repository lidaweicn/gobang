# TCP客户端
from socket import *
from sys import argv


# 1、创建套接字
soc = socket(AF_INET, SOCK_STREAM, 0)
# 2、绑定IP和端口号
# soc.bind(('172.60.12.33', 12120))

ip = argv[1]
port = int(argv[2])
# 3、让套接字具有监听功能
soc.connect((ip, port))
print("服务器连接中... ...")


# 4、消息的收发
while True:
    msg = input('发消息：')
    n = soc.send(msg.encode())
    if not msg:
        break
    # 接受消息
    bf = 1024
    s = soc.recv(bf)
    print('收消息：%s' % s.decode())

# 5、关闭套接字
soc.close()
