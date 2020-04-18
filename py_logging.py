import logging
import sys
from logging.handlers import RotatingFileHandler

import psutil as psutil
from py_config import ConfigFactory


class LoggerFactory():
    def __init__(self, config):
        self.config = config

    def getLogger(self):
        # 设置日志格式
        formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y%b%d-%H:%M:%S")
        # 文件日志循环
        fileHandlerDict = dict(self.config.items('logger'))
        fileHandlerDict['maxBytes'] = int(fileHandlerDict['maxBytes'])
        fileHandlerDict['backupCount'] = int(fileHandlerDict['backupCount'])
        fileHandler = RotatingFileHandler(**fileHandlerDict)
        fileHandler.setFormatter(formatter)
        #  控制台日志
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(formatter)
        # 加入日志处理句柄
        logger = logging.getLogger()
        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)
        # 设置日志等级
        logger.setLevel(config.getint('default', 'logger_level'))
        return logger


if __name__ == '__main__':
    config = ConfigFactory(config='py_lims.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    logger.debug('Hello world!')
    for i in range(100):
        cpuper = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        line = f'cpu:{cpuper}% mem:{mem} '
        logger.info(line)
