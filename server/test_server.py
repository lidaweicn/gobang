from threading import Thread
from socket import *


def handler2(ADDR):
    '''客户端处理函数'''

    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print("服务器启动")

    while True:
        try:
            c, addr = s.accept()
            print(addr)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e)
            # continue


def main():
    addr1 = ('0.0.0.0', 8888)
    addr2 = ('0.0.0.0', 8889)
    t1 = Thread(target=handler2, args=(addr1,))
    t1.setDaemon(True)  # 主线程结束之后，自动处理回收，并子线程结束
    t1.start()

    t2 = Thread(target=handler2, args=(addr2,))
    t2.setDaemon(True)  # 主线程结束之后，自动处理回收，并子线程结束
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
