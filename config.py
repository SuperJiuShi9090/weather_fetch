"""获取配置，包括AKI key等"""
import os

from dotenv import load_dotenv
from LOG import *


load_dotenv()
logger = logging.getLogger(__name__)

class Config:
    key: str = os.getenv("API_KEY")
    kid: str = os.getenv("API_KID")
    host: str = os.getenv("API_HOST")

if not Config.host or not Config.key or not Config.kid:
    logger.exception("缺少配置，请检查环境变量配置是否正确！")
    raise EnvironmentError("缺少配置，请检查环境变量配置是否正确！")

if not Config.host.startswith("https://") or not Config.host.endswith("/"):
    logger.exception("API host格式错误，请按照和风天气官方文档获取正确的API host！")
    raise EnvironmentError("API host格式错误，请按照和风天气官方文档获取正确的API host！")

Headers = {
    'X-QW-Api-Key': Config.key,
    'kid': Config.kid
}
