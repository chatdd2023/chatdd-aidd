import redis
from aidd.config.env import *

# 缓存服务地址
REDIS_HOST = os.getenv('REDIS_HOST')
# 缓存服务端口
REDIS_PORT = os.getenv('REDIS_PORT')
# 缓存服务密码
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

'''
  功能：封装redis的操作类
  author:boge
  date: 2023-10-26
'''
class RedisHelper:
    def __init__(self):
        # 连接redis
        self.__redis = redis.StrictRedis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT)

    # 设置key-value
    def set(self, key, value):
        self.__redis.set(key, value)

    # 获取key-value
    def get(self, key):
        return self.__redis.get(key).decode()

    # 判断key是否存在
    def is_existsKey(self, key):
        # 返回1存在，0不存在
        return self.__redis.exists(key)

    # 添加集合操作
    def add_set(self, key, value):
        # 集合中存在该元素则返回0,不存在则添加进集合中，并返回1
        # 如果key不存在，则创建key集合，并添加元素进去,返回1
        return self.__redis.sadd(key, value)

    # 判断value是否在key集合中
    def is_Inset(self, key, value):
        '''判断value是否在key集合中，返回布尔值'''
        return self.__redis.sismember(key, value)

    # 关闭连接
    def close(self):
        self.__redis.close()