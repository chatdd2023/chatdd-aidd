from dbutils.pooled_db import PooledDB
import pymysql
from aidd.config.env import *
'''
  description:：mysql数据库连接池操作
  author:boge
  date: 2023-10-18
'''
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# 数据库连接编码
DB_CHARSET = "utf8mb4"
# mincached : 启动时开启的闲置连接数量(缺省值 0 开始时不创建连接)
DB_MIN_CACHED = 10
# maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
DB_MAX_CACHED = 10
# maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
DB_MAX_SHARED = 20
# maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
DB_MAX_CONNECYIONS = 100
# blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......> 其他代表阻塞直到连接数减少,连接被分配)
DB_BLOCKING = True
# maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
DB_MAX_USAGE = 0
# setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
DB_SET_SESSION = None
# creator : 使用连接数据库的模块
DB_CREATOR = pymysql

class MyConnectionPool(object):

    __pool = None

    # 创建数据库连接conn和游标cursor
    def __enter__(self):
        self.conn = self.__getconn()
        self.cursor = self.conn.cursor()

    # 创建数据库连接池
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=DB_CREATOR,
                mincached=DB_MIN_CACHED,
                maxcached=DB_MAX_CACHED,
                maxshared=DB_MAX_SHARED,
                maxconnections=DB_MAX_CONNECYIONS,
                blocking=DB_BLOCKING,
                maxusage=DB_MAX_USAGE,
                setsession=DB_SET_SESSION,
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USERNAME,
                passwd=DB_PASSWORD,
                db=DB_DATABASE,
                use_unicode=False,
                charset=DB_CHARSET
            )
        return self.__pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn


class MySqLHelper(object):
    def __init__(self):
        self.db = MyConnectionPool()  # 从数据池中获取连接

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):  # 单例
            cls.inst = super(MySqLHelper, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 封装执行命令
    def execute(self, sql, param=None, autoclose=False):
        """
        【主要判断是否有参数和是否执行完就释放连接】
        :param sql: 字符串类型，sql语句
        :param param: sql语句中要替换的参数"select %s from tab where id=%s" 其中的%s就是参数
        :param autoclose: 是否关闭连接
        :return: 返回连接conn和游标cursor
        """
        cursor, conn = self.db.getconn()  # 从连接池获取连接
        count = 0
        try:
            # count : 为改变的数据条数
            if param:
                count = cursor.execute(sql, param)
            else:
                count = cursor.execute(sql)
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            print(e)
            pass
        return cursor, conn, count


    # 释放连接
    def close(self, cursor, conn):
        """释放连接归还给连接池"""
        cursor.close()
        conn.close()

    # 查询所有
    def selectall(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print(e)
            self.close(cursor, conn)
            return count

    # 查询单条
    def selectone(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print("error_msg:", e.args)
            self.close(cursor, conn)
            return count

    # 增加
    def insertone(self, sql, param):
        try:
            cursor, conn, count = self.execute(sql, param)
            # 最后插入行的主键id
            last_id=cursor.lastrowid
            conn.commit()
            self.close(cursor, conn)
            return last_id
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return 0

    # 增加多行
    def insertmany(self, sql, param):
        """
        :param sql:
        :param param: 必须是元组或列表[(),()]或（（），（））
        :return:
        """
        cursor, conn, count = self.db.getconn()
        try:
            cursor.executemany(sql, param)
            conn.commit()
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return 0

    # 删除
    def delete(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return 0

    # 更新
    def update(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            return count
        except Exception as e:
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return 0



if __name__ == '__main__':
    db = MySqLHelper()
    result=db.insertone("insert into pharmolix_chat_history(user_id, chat_session_id, content, role, type) values( % s, %s, %s, %s, %s)",("1008","2008","你好 世界呀","user","text"))
    print("result===="+str(result))