"""获取location ID、经纬度以及所查询地点的官方名称"""
from LOG import logging
from config import Config
from tools import fetch_json

logger = logging.getLogger(__name__)

Host = Config.host

#返回查询地点的官名，locationID和经纬度
async def geo(
        city: str,
        host: str | None = Host,
        number: int = 10,
        timeout: int = 5
) -> dict | list:
    """
    返回查询地点的官名，locationID和经纬度
    :param city: 城市名称
    :param host: 请求头，从和风天气控制台获取
    :param number: 返回的结果数量，默认10条。范围：1~20
    :param timeout: 连接超时的判定时间
    :return: 返回列表（包含国家到城市拼接的完整名称、城市ID、城市精度和城市纬度或错误信息）
    或原json
    """
    url = f"{host}geo/v2/city/lookup?location={city}&lang=zh&number={number}"

    logger.info(f"开始获取城市：{city} 的信息")
    data: dict = await fetch_json(url=url, timeout=timeout)

    if data.get("code") != "200" or not data.get("location"):
        err = "error"
        error_msg = data.get(err, {})

        if error_msg:
            if error_msg.get("status"):
                if error_msg.get("status") == 400:
                    logger.warning(f"未找到城市：{city}")
                    return [err,f"找不到城市：{city}！"]

                msg = error_msg.get("detail", "无")
                logger.error(
                    f"城市：{city} 信息查询失败，错误码："
                    f"{error_msg.get('status')}\n详细信息：{msg}"
                )
                return [err, msg]
        msg = str(data)
        logger.error(f"城市：{city} 信息查询失败，详细信息：{msg}")
        return [err, msg]

    item = data["location"][0]
    city = item['name']

    # adm1: 省/直辖市/自治区  adm2: 地级市/区
    country = item['country']
    province = item.get("adm1", "")
    prefecture = item.get("adm2", "")

    # 拼接成「xx省xx市」形式，避免重复
    full_name = country + province + prefecture + (
        city if prefecture != city else ""
    )

    logger.debug(
        f"城市：{city} 的信息获取完毕，返回："
        f"[{full_name},{item['id']},{item['lat']},{item['lon']}]"
    )
    return [full_name, item["id"], item["lat"], item["lon"]]
