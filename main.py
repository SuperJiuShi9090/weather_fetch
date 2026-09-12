"""
__version__=1.6.0
主程序入口，使用define_js.py的函数解析和风天气返回的内容
"""
import asyncio
import traceback

from define_js import *
from GEO_API import geo
from LOG import *

logger = logging.getLogger(__name__)
Name = "天气查询"


async def main():
    while True:  # 天气查询类别选择
        print(
            f"{Name:=^40}\n"
            "查询内容:\n  1.实时天气预报"
            "\n  2.逐小时天气预报\n  3.每日天气预报"
            "\n  4.实时空气质量\n  5.逐小时空气质量"
             "\n  6.每日空气质量\n  7.实时天气预警"
        )
        ans = input("选择一项上述查询内容的相应序号:")

        if ans not in {"1", "2", "3", "4", "5", "6", "7"}:
            print("答案不在选项中，请重新输入！")
            continue
        break

    data = {}
    name, city_id, lat, lon = "", "", 0, 0
    while True:  # 查询指定地点
        print(f"{Name:=^40}")
        city = input("请输入查询地点（如南京市）：").strip()

        if len(city) < 2:
            print("最少输入两个有效字符！")
            continue

        try:
            geo_info = await geo(city)
            if geo_info[0] != "error":
                name, city_id, lat, lon = geo_info
            else:
                print(f"城市：{city} 信息查询失败！错误信息：{geo_info[1]}")
                return
        except Exception as e:
            tb = traceback.format_exc()
            msg = f"意外的天气预报查询失败在获取geo信息时！错误信息：{type(e).__name__}: {e}"
            print(msg)
            logger.error(msg + tb)
            return
        break

    loc_info = f"查询地点：{name}\n"
    reason = ""
    if True:  # 留个判断口，后面json解析
        logger.info("%s请求成功!", mod.get(ans, "和风天气API"))
        logger.debug(data)

        if ans in {"1", "2", "3"}:
            data = await wea(city_id, ans)
            reason = weajs(data, loc_info)
        elif ans in {"4", "5", "6"}:
            data = await aqi(lat, lon, ans)
            reason = aqijs(data, loc_info)
        elif ans == "7":
            war_data = await war(lat, lon)
            reason = warjs(war_data)

        print("\n".join(reason) if isinstance(reason, list) else reason)
    #    with open(f"{name + mod[ans]}预报.txt", "w") as file:
    #        file.write(f"地点:{name}\n")
    #        file.write(reason)


if __name__ == "__main__":
    from api import aqi, war, wea

    asyncio.run(main())
