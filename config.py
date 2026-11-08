"""获取配置，包括AKI key等"""
import os

from dotenv import load_dotenv
from LOG import *


load_dotenv()
logger = logging.getLogger(__name__)

class Config:
    key: str = os.getenv("QWEATHER_APIKEY")
    kid: str = os.getenv("QWEATHER_APIKID")
    host: str = os.getenv("QWEATHER_APIHOST")

    headers: dict = {
    'X-QW-Api-Key': key,
    'kid':kid
    }

if not Config.host or not Config.key or not Config.kid:
    logger.exception("缺少配置，请检查环境变量配置是否正确！")
    raise EnvironmentError("缺少配置，请检查环境变量配置是否正确！")

if not Config.host.startswith("https://") or not Config.host.endswith("/"):
    logger.exception("API host格式错误，请按照和风天气官方文档获取正确的API host！")
    raise EnvironmentError("API host格式错误，请按照和风天气官方文档获取正确的API host！")
