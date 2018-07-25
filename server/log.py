import logging
import os
from common import get_time

# 初始化日志默认配置
LOG_PATH = '/log'
path = os.getcwd() + LOG_PATH + '/{}'.format(get_time()[:10])
if not os.path.exists(path):
    os.mkdir(path)
fmt = '%(asctime)s %(levelname)s Line:%(lineno)s==>%(message)s'
logging.basicConfig(filename=path + '/game.log',    # 日志输出文件
                    level=logging.DEBUG,            # 日志写入级别
                    datefmt='%Y-%m-%d %H:%M:%S',    # 时间格式
                    format=fmt)   # 日志写入格式
