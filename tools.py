"""发起网络请求并返回JSON内容，解析失败返回空字典"""
import httpx

from config import *
from LOG import *

logger = logging.getLogger(__name__)


async def fetch_json(url: str, headers=Headers, timeout=5) -> dict:
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
