import os
import sys
from datetime import datetime
from loguru import logger

class TestLogger:
    def __init__(self):
        self.log_path = "logs"
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        
        # 移除默认的处理器
        logger.remove()
        
        # 添加控制台输出处理器
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO"
        )
        
        # 添加文件处理器
        log_file = os.path.join(self.log_path, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG",
            rotation="500 MB",
            retention="10 days"
        )

    @staticmethod
    def info(msg: str, *args, **kwargs):
        """记录信息级别日志"""
        logger.info(msg, *args, **kwargs)

    @staticmethod
    def debug(msg: str, *args, **kwargs):
        """记录调试级别日志"""
        logger.debug(msg, *args, **kwargs)

    @staticmethod
    def warning(msg: str, *args, **kwargs):
        """记录警告级别日志"""
        logger.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg: str, *args, **kwargs):
        """记录错误级别日志"""
        logger.error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg: str, *args, **kwargs):
        """记录异常信息"""
        logger.exception(msg, *args, **kwargs)

# 创建全局日志记录器实例
test_logger = TestLogger() 