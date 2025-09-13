# src/utils/logger_config.py
import logging


def setup_logging():
    """
    统一配置日志格式
    """
    # 检查是否已经配置过根日志记录器
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(threadName)s] %(levelname).1s %(name)s:%(funcName)s-%(lineno)d - %(message)s',
            handlers=[
                logging.StreamHandler(),  # 输出到控制台
                # 如果需要输出到文件可以添加:
                # logging.FileHandler('app.log', encoding='utf-8')
            ]
        )


def get_logger(name):
    """
    获取指定名称的日志记录器
    """
    setup_logging()
    return logging.getLogger(name)
