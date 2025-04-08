import logging
import os

# 创建日志目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志记录器
test_logger = logging.getLogger('yaml_to_test')
test_logger.setLevel(logging.INFO)

# 创建文件处理器
file_handler = logging.FileHandler(os.path.join(log_dir, 'yaml_to_test.log'), encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器到日志记录器
test_logger.addHandler(file_handler)
test_logger.addHandler(console_handler) 