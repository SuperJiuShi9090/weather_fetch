"""获取配置，包括AKI key等"""
import os

from dotenv import load_dotenv
from LOG import *


load_dotenv()
logger = logging.getLogger(__name__)

key = os.getenv("API_KEY")
kid = os.getenv("API_KID")
host = os.getenv("API_HOST")

if not host or not key or not kid:
    logger.exception("缺少配置，请检查环境变量配置是否正确！")
    raise EnvironmentError("缺少配置，请检查环境变量配置是否正确！")

if not host.startswith("https://") or not host.endswith("/"):
    logger.exception("API host格式错误，请按照和风天气官方文档获取正确的API host！")
    raise EnvironmentError("API host格式错误，请按照和风天气官方文档获取正确的API host！")

Headers = {
    'X-QW-Api-Key': key,
    'kid': kid
}

def Host():
    return host

if __name__ == "__main__":
    print(Headers)
    print(Host())
