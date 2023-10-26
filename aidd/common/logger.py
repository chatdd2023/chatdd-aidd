import logging

'''
  功能：简易版 日志打印
  author:boge
  date:2023-10-27
'''
class Logger:
    def __init__(self, log_file):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.log_file = log_file
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    def debug(self, message):
        self.logger.debug(message)
    def info(self, message):
        self.logger.info(message)
    def warning(self, message):
        self.logger.warning(message)
    def error(self, message):
        self.logger.error(message)

logger = Logger('mylog.log')
errorlogger = Logger('mylogerror.log')

if __name__ == '__main__':
    logger = Logger('mylog.log')
    logger.info('Info message')
    errorlogger = Logger('mylogerror.log')
    errorlogger.error('Error message')
