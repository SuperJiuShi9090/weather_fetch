"""获取location ID、经纬度以及所查询地点的官方名称"""
from LOG import *
from config import *
from tools import fetch_json

logger = logging.getLogger(__name__)

#返回查询地点的官名，locationID和经纬度
async def geo(city: str, host=Host(), timeout=5) -> list:
    url = f"{host}geo/v2/city/lookup?location={city}&lang=zh"

    logger.info("开始获取城市：%s 的信息",city)
    js = await fetch_json(url=url, timeout=timeout)

    if not js:
        logger.error("城市信息获取失败！")
        return []

    if js.get("code") != "200" or not js.get("location"):
        logger.exception(f"GEOAPI 错误：{js}")
    item = js["location"][0]

    # adm1: 省/直辖市/自治区  adm2: 地级市/区
    province = item.get("adm1", "")
    prefecture = item.get("adm2", "")

    # 拼接成「xx省xx市」形式，避免重复
    parts = [p for p in (province, prefecture) if p and p not in item["name"]]
    full_name = "".join(parts) + item["name"] if parts else item["name"]

    return [full_name,item["id"],item["lat"],item["lon"]]


if __name__ == "__main__":
    city = input("请输入城市名（如南京市）：")
    logger.info("GEOAPI调试")
    if geo(city):
        name,ID,lat,lon = geo(city)
        print(f"{name} 的信息 = {id,lat,lon}")
        logger.info("GEOAPI返回正常！")
