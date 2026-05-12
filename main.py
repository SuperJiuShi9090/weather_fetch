"""
__version__=1.5.0
主程序入口，使用define_js.py的函数解析和风天气返回的内容
此为示例代码
"""
import asyncio

from define_js import *
from dictionary import *
from GEO_API import geo
from LOG import *

logger = logging.getLogger(__name__)
Name = '和风天气API'


async def main():
    while True:  #天气查询类别选择
        print(
            f"{Name:=^40}\n"
            "查询内容:\n  1.实时天气预报"
            "\n  2.逐小时天气预报\n  3.每日天气预报"
            "\n  4.实时空气质量\n  5.逐小时空气质量（暂未更新）"
            "\n  6.每日空气质量（暂未更新）\n  7.实时天气预警"
        )
        ans = input("选择一项上述查询内容的相应序号:")

        if ans not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("答案不在选项中，请重新输入！")
            continue
        break

    while True:  #查询指定地点
        print(f"{Name:=^40}")
        b = input("请输入查询地点（如南京市）：")
        b = b.replace(" ", "")

        if len(b) < 2:
            print("最少输入两个有效字符！")
            continue

        name, ID, lat, lon = await geo(b)

        if ans in ["1", "2", "3"]:
            data = await wea(ID, ans)
        elif ans in ["4", "5", "6"]:
            data = await aqi(lat, lon, ans)
        else:
            data = await war(lat, lon)
        break

    reason = ""
    if True:  #留个判断口，后面json解析
        logger.info("%s请求成功!", mod.get(ans, "和风天气API"))

        if ans in ["1", "2", "3"]:  #天气预报处理
            cnt = weajs(data, ans)
            for i in cnt:
                reason += i + "\n"
        elif ans == "4":  #空气质量处理
            cnt = ctaqijs(data)
            for i in cnt:
                if i is not None:
                    reason += i + "\n"
        elif ans in ["5", "6"]:
            reason = data
        elif ans == "7":  #实时预警处理
            cnt = warjs(data)
            reason = ""
            if cnt[0] is not None:
                for i in cnt:
                    if i is not None:
                        reason += i + "\n"
                reason = reason[:-1]
            else:
                reason = name + "暂时还没有预警信息哦～"
            logger.info("实时预警请求完毕！")

        print(reason)
    #    with open(f"{name + mod[ans]}预报.txt", "w") as file:
    #        file.write(f"地点:{name}\n")
    #        file.write(reason)

if __name__ == "__main__":
    from API import aqi, war, wea
    asyncio.run(main())