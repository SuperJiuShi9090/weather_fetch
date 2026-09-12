"""利用对应API获取天气信息json"""
from LOG import *
from config import Config
from tools import fetch_json

logger = logging.getLogger(__name__)
Host = Config.host

async def aqi(
        latitude: float | int,
        longitude: float | int,
        ans: str ="4",
        host: str | None = Host,
        timeout: int = 5
) -> dict:
    """
    返回空气质量json
    :param latitude: 被查询地点的纬度。十进制，最多支持两位小数
    :param longitude: 被查询地点的经度。十进制，最多支持两位小数
    :param ans: 查询类型。程序内部交流，自动处理，不用管
    :param host: 请求头，从和风天气控制台获取
    :param timeout: 尝试连接时间
    """
    latitude = round(float(latitude), 2)
    longitude = round(float(longitude), 2)

    path = "current/"
    if ans == "5":
        path = "hourly/"
    elif ans == "6":
        path = "daily/"

    url = f"{host}airquality/v1/{path}{latitude}/{longitude}?lang=zh"

    logger.info("开始查询空气质量")
    json_data = await fetch_json(url, timeout=timeout)

    return json_data


async def wea(
        city: str,
        ans: str = "1",
        host: str | None = Host,
        timeout: int = 5
) -> dict:
    """
    返回天气预报json
    :param city: 查询的城市ID
    :param ans: 查询类型。程序内部交流，自动处理，不用管
    :param host: 请求头，从和风天气控制台获取
    :param timeout: 尝试连接时间
    """
    day = "now"
    if ans == "2":
        day = "24h"  # 可选值：24h,72h,168h
    elif ans == "3":
        day = "7d"  # 可选值：3d,7d,10d,15d,30d

    url = f"{host}v7/weather/{day}?location={city}&lang=zh"

    logger.info(f"开始获取{city}天气")
    json_data = await fetch_json(url, timeout=timeout)

    return json_data


async def war(
        latitude: float | int,
        longitude: float | int,
        host: str | None = Host,
        timeout: int = 5
) -> dict:
    """
    返回实时预警json
    :param latitude: 被查询地点的纬度。十进制，最多支持两位小数
    :param longitude: 被查询地点的经度。十进制，最多支持两位小数
    :param host: 请求头，从和风天气控制台获取
    :param timeout: 尝试连接时间
    """
    latitude = round(float(latitude), 2)
    longitude = round(float(longitude), 2)
    url = f"{host}weatheralert/v1/current/{latitude}/{longitude}?lang=zh"

    logger.info("开始获取实时预警")
    json_data = await fetch_json(url, timeout=timeout)

    return json_data
