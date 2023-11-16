from aidd.db.redishelper import RedisHelper
from aidd.db.mysqlhelper import MySqLHelper
import aidd.common.logger

'''
redis 测试
'''
redis=RedisHelper()
redis.set("bobo","badao")
print(redis.get("bobo"))
print(redis.search_float("*++1001R_ASFK5"))

'''
mysql 测试
'''
#mysqlhelper=MySqLHelper()
#result = mysqlhelper.insertone(
#    "insert into pharmolix_chat_history(user_id, chat_session_id, content, role, type) values( % s, %s, %s, %s, %s)",
#    ("1008", "2008", "人民最幸福", "user", "text"))
#print("result====",result)




