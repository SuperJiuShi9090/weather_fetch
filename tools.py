"""发起网络请求并返回JSON内容，解析失败返回空字典"""
from datetime import datetime

import httpx
import pytz

from config import *
from LOG import *

logger = logging.getLogger(__name__)


async def fetch_json(url: str, headers=Headers, timeout: int =5) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as client:
        for i in range(1, 4):
            try:
                r = await client.get(url, headers=headers, timeout=timeout)
                logger.debug(r)
                logger.debug(r.text)
            except httpx.TimeoutException:
                logger.warning('服务器请求超时！第%d次尝试', i)
                continue
            except httpx.HTTPError as e:
                logger.error("HTTP错误：%s", e)
                return {}

            if not r.text:
                logger.error("服务器未返回任何数据！")
                return {}

            try:
                data = r.json()
                logger.debug(data)
                logger.info("服务器请求成功！")
                return data
            except ValueError:
                logger.error("未返回合法JSON！%s", r)
                return {}
        else:
            logger.error("请求失败，请求次数耗尽！")
            return {}

def iso_format_time(time: str, time_format: str ="%Y-%m-%d %H:%M:%S"):
    """将 ISO 时间转换为指定格式的 GMT+8 时间

    Args:
        time (_type_): ISO 时间
        time_format (_type_): 输出的时间格式
    """
    # 解析为datetime对象
    dt = datetime.fromisoformat(time)

    # 设置时区
    tz = pytz.timezone('Asia/Shanghai')
    dt_gmt8 = dt.astimezone(tz)
    formatted_time = dt_gmt8.strftime(time_format)
    return formatted_time
