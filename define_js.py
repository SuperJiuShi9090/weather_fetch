"""
此文件存放各种API的json解析的函数
"""
from LOG import *
from dictionary import *
from tools import iso_format_time

logger = logging.getLogger(__name__)

LICE = "=" * 20 + "\n数据来源：和风天气API"


def warjs(js: dict,) -> list | str | None:
    """
    实时预警json解析
    :param js: 和风天气API返回的实时预警json数据
    """
    if js.get("error"):
        err = "error"
        error_msg = js.get(err, {})
        status = error_msg.get("status")

        if status == 400:
            return "此地的数据暂时不可用呢，这里超出支持的范围啦！换个地方再试试叭"

        msg = f"意外地天气预警查询失败在获取预警信息时，错误码：{status}"
        detail = f"{msg}\n详细信息：{error_msg.get('detail')}"

        logger.error(detail)
        return [err, msg]

    data = js["metadata"]
    attribute = data.get("attributions", None)

    a = ""
    if attribute is not None:
        for line in attribute:
            a += line + "\n"
    atrb = "声明：数据来自" + a if a else ""

    if not data["zeroResult"]:
        result = []
        for line in js['alerts']:
            color = line["color"]['code']
            title = "标题：" + line["headline"] + WAR["color"].get(color, "")
            sender = ("预报机构：" + (line.get("senderName") or "未知")) if a else None
            urgc = WAR["urgency"].get(line["urgency"])
            svrt = WAR["severity"].get(line["severity"])
            cett = WAR["certainty"].get(line["certainty"])

            if urgc and cett is not None:
                cett += urgc
            elif cett is None and urgc is not None:
                cett = urgc

            details = "详细信息：" + line["description"]
            istt = "防御指南：" + (line.get("instruction") or "暂无")

            msg = "\n".join([
                title,
                sender or "",
                details,
                svrt or "",
                cett or "",
                istt,
                atrb or ""
            ])
            result.append(msg + LICE)

        return result
    return "暂时还没有预警信息哦～"


def weajs(js, *args) ->list | str:
    """
    天气预报解析，每小时/天各返回一个 MessageSegment.text
    天气行格式：天气：🌤多云
    :param js: 和风天气API返回的json
    """
    if js.get("error"):
        return [str(js)]

    msg = ["\n".join(args).strip()] if args else []
    if js.get("now"):
        data = js["now"]

        time = "观测时间：" + iso_format_time(data['obsTime'], "%Y年%m月%d日 %H:%M")
        temp = wea_dict(data, "temp") + (
            f"（体感{data['feelsLike']}℃）" if data['feelsLike'] else ""
        )
        text = wea_dict(data, "text") + icon.get(data['icon'], "")
        wind = (
            f"风力风向：{data['windDir']}{data['windScale']}"
            f"{WEA_unit.get('windScale')}（{data['windSpeed']}"
            f"{WEA_unit.get('windSpeed')}）"
        )
        humidity = wea_dict(data, "humidity")
        precip = wea_dict(data, "precip")
        pressure = wea_dict(data, "pressure")
        cloud = wea_dict(data, "cloud")
        dew = wea_dict(data, "dew")
        vis = wea_dict(data, "vis")

        result = [
            time, temp, text, wind, humidity,
            precip, pressure, cloud, dew, vis, LICE
        ]
        msg = "\n".join(args) + "\n".join(result)
    elif js.get("daily"):
        datas = js["daily"]
        for data in datas:
            time = "预报时间：" + iso_format_time(data['fxDate'], "%Y年%m月%d日 %H:%M")

            sunrise = data["sunrise"]
            sunset = data["sunset"]
            if sunrise and sunset:
                sun = f"日出时间：{data['sunrise']}-{data['sunset']}"
            elif sunrise and not sunset:
                sun = wea_dict(data, "sunrise")
            else:
                sun = wea_dict(data, "sunset")

            temp = (
                f"当日气温：{data['tempMin']}{WEA_unit.get('tempMin')}"
                f"~{data['tempMax']}{WEA_unit.get('tempMax')}"
            )
            text = (
                f"昼夜天气：{data['textDay'] + icon.get(data['iconDay'], '')}"
                f" / {data['textNight'] + icon.get(data['iconNight'], '')}"
            )

            wind = (
                f"昼夜风况：{data['windDirDay']}{data['windScaleDay']}"
                f"{WEA_unit.get('windScaleDay')}（{data['windSpeedDay']}"
                f"{WEA_unit.get('windSpeedDay')}） / {data['windDirNight']}"
                f"{data['windScaleNight']}{WEA_unit.get('windScaleNight')}"
                f"（{data['windSpeedNight']}{WEA_unit.get('windSpeedNight')}）"
            )
            humidity = wea_dict(data, "humidity")
            precip = wea_dict(data, "precip")
            pressure = wea_dict(data, "pressure")
            uv_index = wea_dict(data, "uvIndex")
            vis = wea_dict(data, "vis")
            cloud = wea_dict(data, "cloud")

            result = [
                time, sun, temp, text, wind, humidity,
                precip, pressure, uv_index, vis, cloud, LICE
            ]
            msg.append(f"\n".join(result))
    else:
        datas = js['hourly']
        for data in datas:
            time = "预报时间：" + iso_format_time(data['fxTime'], "%Y年%m月%d日 %H:%M")
            temp = wea_dict(data, "temp")
            text = wea_dict(data, "text") + icon.get(data['icon'], '')
            wind = (
            f"风力风向：{data['windDir']}{data['windScale']}"
            f"{WEA_unit.get('windScale')}（{data['windSpeed']}"
            f"{WEA_unit.get('windSpeed')}）"
            )
            humidity = wea_dict(data, "humidity")
            precip = wea_dict(data, "precip")
            pressure = wea_dict(data, "pressure")
            cloud = wea_dict(data, "cloud")
            dew = wea_dict(data, "dew")
            pop = wea_dict(data, "pop", 0)

            result = [
                time, temp, text, wind, humidity,
                precip, pressure, cloud, dew, pop, LICE
            ]
            msg.append(f"\n".join(result))
    return msg


def _aqijs(data, attributions: str = ""):
    time = "预报时间：" + iso_format_time(
        data['forecastTime'], "%Y年%m月%d日 %H:%M"
    ) if data.get('forecastTime') else (
        "预报有效范围："
        f"{iso_format_time(data['forcastStartTime'], '%Y年%m月%d日 %H:%M')}"
        f"至{iso_format_time(data['forcastEndTime'], '%Y年%m月%d日 %H:%M')}"
    ) if data.get('forcastStartTime') else ""
    index = data['indexes'][0]
    aqi = f"{index['name']}：{index['aqiDisplay']}"
    leve = f"等级类别：{index['level']}（{index['category']}）"
    pollutant = "首要污染：" + (index['primaryPollutant'] or {}).get('name', "无")

    health = index['health']
    effect = f"影响：{health['effect']}" if health['effect'] else ""

    advice = ""
    if health['advice']:
        normal = health['advice']['generalPopulation']
        special = health['advice']['sensitivePopulation']
        if normal == special:
            advice = normal
        elif normal and special:
            advice = (
                f"对于一般人群来说，{normal} \n"
                f"对于敏感人群来说，{special}"
            )

    """
    for p in polls:
        code  = p['code']                       # pm2p5 / pm10 / no2 ...
        name  = p['name']                       # PM 2.5 / PM 10 / NO2 ...
        value = p['concentration']['value']     # 浓度数值
        unit  = p['concentration']['unit']      # μg/m³ 或 mg/m³
        sub   = p['subIndexes'][0]['aqi']       # 分指数
        print(f"{name:<4} 浓度={value:6.2f}{unit:<6} 分指数={sub}")
    """
    sender = "监测点 :" + "、".join(
        i["name"] for i in data['stations']
    ) if data.get('stations') else ""

    return [time, aqi, leve, pollutant, effect, advice, sender, attributions, LICE]


def aqijs(data: dict, *args) -> str | list:
    if data.get("error"):
        return str(data)

    logger.debug(data)
    #tag   = js["metadata"]["tag"]
    attributions = "，".join(i for i in data['metadata']['attributions'])

    if data.get('indexes'):
        result = [*args, *_aqijs(data, "声明：数据来源" + attributions)]
        msg = "\n".join(i for i in result if i.strip())
    elif data.get("hours"):
        msg = ["\n".join(args) + "声明：以下数据均来源" + attributions]
        for data in data["hours"]:
            result = f"\n".join(i for i in _aqijs(data) if i.strip())
            msg.append(result)
    else:
        msg = ["\n".join(args) + "声明：以下数据均来源" + attributions]
        for data in data["days"]:
            result = f"\n".join(i for i in _aqijs(data) if i.strip())
            msg.append(result)
    return msg
