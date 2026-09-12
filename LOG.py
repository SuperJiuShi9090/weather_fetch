"""全局日志配置"""
import logging

logging.basicConfig(
    level=logging.INFO, # 把级别调到 DEBUG，就能看到更详细的信息
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('run.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
