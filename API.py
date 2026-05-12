"""利用对应API获取天气信息json"""
from config import *
from GEO_API import geo
from LOG import *
from tools import fetch_json

logger = logging.getLogger(__name__)


#返回空气质量json
async def aqi(lat: float, lon: float, ans="4", host=Host(), timeout=5) -> dict:
    lat, lon = round(float(lat), 2), round(float(lon), 2)
    path = "daily/"
    if ans == "4":
        path = "current/"
    elif ans == "5":
        path = "hourly/"
    url = f"{host}airquality/v1/{path}{lat}/{lon}?lang=zh"

    logger.info("开始查询空气质量")
    json_data = await fetch_json(url, timeout=timeout)

    return json_data or {"获取空气质量失败！"}


#返回天气预报json
async def wea(city: str, ans="1", host=Host(), timeout=5):
    path = "7d"  # 可选值：3d,7d,10d,15d,30d
    if ans == "2":
        path = "24h"  # 可选值：24h,72h,168h
    elif ans == "1":
        path = "now"
    url = f"{host}v7/weather/{path}?location={city}&lang=zh"

    logger.info("开始获取%s天气", city)
    json_data = await fetch_json(url, timeout=timeout)

    return json_data or {f"{city}天气获取失败！"}


#返回实时预警json
async def war(lat: float, lon: float, host=Host(), timeout=5):
    lat, lon = round(float(lat), 2), round(float(lon), 2)
    url = f"{host}weatheralert/v1/current/{lat}/{lon}?lang=zh"

    logger.info("开始获取实时预警")
    json_data = await fetch_json(url, timeout=timeout)

    return json_data or {"预警获取失败！"}


if __name__ == "__main__":
    city = input("请输入要查询空气质量的城市名：")
    name, ID, lat, lon = geo(city=city)
    lat, lon = round(float(lat), 2), round(float(lon), 2)
    print(lat, lon)
    print(aqi(lat, lon, ans="4"))
    """
    logger.info("天气预报API调试")
    name,ID,lat,lon = geo("南京玄武湖")
    print(wea(ID, "3"))
    
    name,id,lat,lon = geo("南京")
    lat,lon = round(float(lat),2),round(float(lon),2)
    print(lat, lon)
    content=war(lat, lon)
    print(content)
    with open(f"{name}实时预警.txt","w") as file:
        file.write(str(content))
    """
