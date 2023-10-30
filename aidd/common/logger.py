import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from aidd.config.env import *
import os
'''
   功能：日志管理类
   日期：2023.10.10
   作者: boge
'''
def init_logger(logger_name):
    if logger_name not in Logger.manager.loggerDict:
        #读取配置文件
        info_log_path = os.getenv("ALL_LOG_PATH")
        error_log_path = os.getenv("ERROR_LOG_PATH")

        logger1 = logging.getLogger(logger_name)
        logger1.setLevel(logging.INFO)  # 设置最低级别
        df = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: %(name)s %(levelname)s %(message)s'
        formatter = logging.Formatter(format_str, df)
        try:
            handler1 = TimedRotatingFileHandler(info_log_path, when='D', interval=1, backupCount=7,encoding='utf-8')
        except Exception:
            handler1 = TimedRotatingFileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)),"all.log"), when='D', interval=1, backupCount=7,encoding='utf-8')
        handler1.setFormatter(formatter)
        if os.getenv("LOG_LEVEL")=="info":
            handler1.setLevel(logging.INFO)
        else:
            handler1.setLevel(logging.DEBUG)
        logger1.addHandler(handler1)
        # handler error
        try:
            handler2 = TimedRotatingFileHandler(error_log_path, when='D', interval=1, backupCount=7,encoding='utf-8')
        except Exception:
            handler2 = TimedRotatingFileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)),"error.log"), when='D', interval=1, backupCount=7,encoding='utf-8')
        handler2.setFormatter(formatter)
        handler2.setLevel(logging.ERROR)
        logger1.addHandler(handler2)

        # console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # 设置日志打印格式
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        logger1.addHandler(console)

    logger1 = logging.getLogger(logger_name)
    return logger1

logger = init_logger('runtime-log')

def logger_ouput_INFO( request_id: str, class_name, function_name, detail_message):
    logger.info(
        f"request_id:{request_id} Class:{class_name} Function:{function_name} detail_message:{detail_message}")
def logger_ouput_Error( request_id: str, class_name, function_name, detail_message):
    logger.error(
        f"request_id:{request_id} Class:{class_name} Function:{function_name} detail_message:{detail_message}")


if __name__ == '__main__':
    logger_ouput_INFO("request_id","类名", "DTI tooling starting ",
                      "执行 dti tolling 工具")