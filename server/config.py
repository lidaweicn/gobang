HOST = '0.0.0.0'
PORT = 10102
# PORT = randint(8000,9000)
ADDR = (HOST, PORT)
DATABASE = {
    'host': "localhost",
    'user': "root",
    'passwd': "123456",
    'db': "dbuser",
}

# 玩家状态，棋手1，棋手2，观战
SINGLE = 0      # 单机游戏
PLAYER1 = 1     # 对战玩家1，左
PLAYER2 = 2     # 对战玩家2，右
WATCHING = 3    # 观战
NETSINGLE = 4   # 联网，与电脑对战
# 游戏状态
OVER = 10
READY = 11
WHITE = 12
BLACK = 13
START = 14
WATCH = 15
