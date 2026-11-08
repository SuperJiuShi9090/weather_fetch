"""利用对应API获取天气信息json"""
from LOG import *
from config import Config
from tools import fetch_json

logger = logging.getLogger(__name__)
_host = Config.host
_headers = Config.headers

async def aqi(
        latitude: float | int,
        longitude: float | int,
        ans: int =4,
        timeout: int = 5
) -> dict:
    """
    返回空气质量json
    :param latitude: 被查询地点的纬度。十进制，最多支持两位小数
    :param longitude: 被查询地点的经度。十进制，最多支持两位小数
    :param ans: 查询类型。程序内部交流，自动处理，不用管
    :param timeout: 尝试连接时间
    """
    latitude = round(float(latitude), 2)
    longitude = round(float(longitude), 2)

    path = "current/"
    if ans == 5:
        path = "hourly/"
    elif ans == 6:
        path = "daily/"

    url = f"{_host}airquality/v1/{path}{latitude}/{longitude}?lang=zh"

    logger.info("开始查询空气质量")
    json_data = await fetch_json(url, timeout=timeout, headers=_headers)

    logger.debug(json_data)
    return json_data


async def wea(
        latitude: float | int,
        longitude: float | int,
        ans: int = 1,
        timeout: int = 5
):
    """
    返回一公里精度的天气预报数据
    :param latitude: 被查询地点的纬度。十进制，最多支持两位小数
    :param longitude: 被查询地点的经度。十进制，最多支持两位小数
    :param ans: 查询类型。程序内部交流，自动处理，不用管
    :param timeout: 尝试连接时间，超过则返回连接超时错误
    """
    time = "current"
    if ans == 2:
        time = "hourly"
    elif ans == 3:
        time = "daily"
    latitude, longitude = round(float(latitude), 2), round(float(longitude), 2)
    url = f"{_host}weather/v1/{time}/{latitude}/{longitude}?lang=zh"

    logger.info(f"开始获取{time}天气信息")
    json_data = await fetch_json(url, timeout=timeout, headers=_headers)

    logger.debug(json_data)
    return json_data


async def war(
        latitude: float | int,
        longitude: float | int,
        timeout: int = 5
) -> dict:
    """
    返回实时预警json
    :param latitude: 被查询地点的纬度。十进制，最多支持两位小数
    :param longitude: 被查询地点的经度。十进制，最多支持两位小数
    :param timeout: 尝试连接时间
    """
    latitude = round(float(latitude), 2)
    longitude = round(float(longitude), 2)
    url = f"{_host}weatheralert/v1/current/{latitude}/{longitude}?lang=zh"

    logger.info("开始获取实时预警")
    json_data = await fetch_json(url, timeout=timeout, headers=_headers)

    logger.debug(json_data)
    return json_data


async def rain(
        latitude: float | int,
        longitude: float | int,
        timeout: int = 5
) -> dict:
    """
    返回分钟级1公里精度的未来2小时每5分钟降雨预报数据
    :param latitude: 被查询地点的纬度。十进制，最多支持两位小数
    :param longitude: 被查询地点的经度。十进制，最多支持两位小数
    :param host: 请求头，从和风天气控制台获取
    :param timeout: 尝试连接时间
    """
    latitude, longitude = round(float(latitude), 2), round(float(longitude), 2)
    url = f"{_host}v7/minutely/5m?location={longitude},{latitude}&lang=zh"

    logger.info("开始获取分钟降水")
    json_data = await fetch_json(url, timeout=timeout, headers=_headers)

    logger.debug(json_data)
    return json_data


async def indices(
        location: str,
        days: int = 1,
        id_type: int = 0,
        timeout: int = 5
):
    """
    获取中国及全球城市的天气生活指数预报数据
    :param location: 需要查询地区的LocationID（可通过和风天气提供的GEO API获取）或以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）
    :param days: 预报天数，支持最多3天预报，可选值：1、3
    :param id_type: 生活指数的类型id，可一次性获取多个类型的生活指数，多个类型用英文逗号分割，可选值参考文档获取指数类型
    :param timeout: 尝试连接时间
    """
    url = f"{_host}v7/indices/{days}d?type={id_type}&location={location}&lang=zh"

    logger.info("开始获取天气指数")
    json_data = await fetch_json(url, timeout=timeout, headers=_headers)

    logger.debug(json_data)
    return json_data
