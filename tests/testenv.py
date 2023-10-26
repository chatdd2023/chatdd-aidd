import os
# 在另一个文件中
from aidd.config.env import *  # 导入 os 模块，其中包含了环境变量

# 使用环境变量的值进行操作
database_host = os.getenv('DB_DATABASE')
print(database_host)



