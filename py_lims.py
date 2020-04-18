import multiprocessing
import os

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_watchdog import WatchDogObServer

if __name__ == '__main__':
    # 编译时兼容win系统
    if os.sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    # 基本配置
    config = ConfigFactory(config='py_lims.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    # 启动监控程序
    wObserver = WatchDogObServer(config=config, logger=logger)
    wObserver.start()
