"""
此文件存放各种API的json解析的函数
"""
from pathlib import Path
from LOG import *
from image_creater.pic_create import pic_create
from api import aqi, war, wea, rain
from dictionary import *
from tools import h_m_time_diff
from datetime import datetime as dt

logger = logging.getLogger(__name__)

SVG = Path(__file__).resolve().parent / "QWeather-Icons-1.8.0" / "icons"
LICE = "=" * 20 + "\n数据来源：和风天气API"


async def war_json_loader(
        js: dict,
        concise: bool = False
) -> list[str | bytes] | None:
    """
    实时预警json解析
    :param js: 和风天气API返回的实时预警json数据
    :param concise: 是否只返回预警提示图片，默认否。（建议不要单独使用）
    """
    if js.get("error"):
        if concise:
            return None

        err = "error"
        error_msg = js.get(err, {})
        status = error_msg.get("status")

        if status == 400:
            return [f"此地的数据暂时不可用呢，这里超出支持的范围啦！换个地方再试试叭"]

        msg = f"意外地天气预警查询失败在获取预警信息时，错误码：{status}"
        detail = f"{msg}\n详细信息：{error_msg.get('detail')}"

        logger.error(detail)

        return [msg + "（已上报）"]

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
            with open(SVG / f"{line['icon']}.svg", "r") as f:
                svg = f.read()

            color = line["color"]
            svg_color = [color['red'], color['green'], color['blue']]
            svg_char_1 = line["eventType"]["name"]
            svg_char_2 = WAR["color_text"].get(line["color"]['code'], "未知")
            svg_char_3 = color['code']

            pic = await pic_create(svg, svg_char_1, svg_char_2, svg_char_3, atrb, svg_color)

            title = "标题：" + line["headline"] + WAR["color"].get(svg_char_3, "")

            if concise:
                result += [title[3:], pic]
            else:
                sender = ("预报机构：" + (line.get("senderName") or "未知")) if a else None
                urgc = WAR["urgency"].get(line["urgency"])
                svrt = WAR["severity"].get(line["severity"])
                cett = WAR["certainty"].get(line["certainty"])

                if urgc and cett is not None:
                    cett += urgc
                elif cett is None and urgc is not None:
                    cett = urgc

                details = "详细信息：" + line["description"]
                # 修复2：instruction 可能为 None
                istt = "防御指南：" + (line.get("instruction") or "暂无")

                # 关键修复3：把单个预警的所有信息拼接成一个字符串
                # 而不是 append 一个列表（之前是 war_info.append([...])）
                msg = "\n".join([
                    title,
                    sender or "",
                    details,
                    svrt or "",
                    cett or "",
                    istt,
                    atrb or ""
                ])
                result += [msg, pic, LICE]

        return result if len(result) > 1 or concise else result[0]
    else:
        if concise:
            return None
        return ["暂时还没有预警信息哦～"]


def _half_day_js(daytime: dict, time: str = "日") -> list[str]:
    forecast_time = (
        f"预报时间：{iso_format_time(daytime['forecastStartTime'], '%H:%M')}"
        f"-{iso_format_time(daytime['forecastEndTime'], '%H:%M')}"
    )
    text = f"{time}天气：" + daytime['condition']['text'] + icon.get(daytime['condition']['code'], '')
    temp = f"{time}气温：{value_unit(daytime, 'Min')}~{value_unit(daytime, 'Max')}："
    humidity = f"{time}平均相对湿度：{daytime['humidity'] * 100}%"
    wind = (
        f"{time}风力风向：{wind_direction(daytime['wind']['direction']['compass'])}"
        f"{daytime['wind']['scale']}级（{daytime['wind']['speed']['value']}"
        f"{daytime['wind']['speed']['unit']}）"
    )
    precip = daytime['precipitation']['amount']
    precip = f"{time}降水量：{precip['value']}{precip['unit']}"
    precipitation = f"{time}降水概率：{daytime['precipitation']['amount']['value'] * 100}%"
    cloud = f"{time}云量：{daytime['cloudCover'] * 100}%"
    return [forecast_time, text, temp, humidity, wind, precip, precipitation, cloud]


def _day_js(data):
    msg = []
    for day in data:
        time = f"{iso_format_time(day['forecastStartTime'], '%Y年%m月%d日'):=^21}"

        astro = day['astro']    # 太阳和月亮天文事件
        sun = sun_moon(astro, "日")
        moon = sun_moon(astro, "月")
        moon_prase = WEA['moonPhase'] + "：" + WEA_unit['moonPhase'].get(astro['moonPhase'])
        astronomical_dawn = wea_dict(astro, 'astronomicalDawn', data_is_time='%H:%M')
        astronomical_dusk = wea_dict(astro,  'astronomicalDusk', data_is_time='%H:%M')
        nautical_dawn = wea_dict(astro, 'nauticalDawn', data_is_time='%H:%M')
        nautical_dusk = wea_dict(astro, 'nauticalDusk', data_is_time='%H:%M')
        civil_dawn = wea_dict(astro, 'civilDawn', data_is_time='%H:%M')
        civil_dusk = wea_dict(astro, 'civilDusk', data_is_time='%H:%M')
        solar_noon = wea_dict(astro, "solarNoon", data_is_time="%H:%M")
        solar_midnight = wea_dict(astro, "solarMidnight", data_is_time="%H:%M")
        moon_transit = wea_dict(astro, "moonTransit", data_is_time="%H:%M")
        moon_underfoot = wea_dict(astro, "moonUnderfoot", data_is_time="%H:%M")
        temp = f"当日气温：{value_unit(day, 'Min')}~{value_unit(day, 'Max')}"
        uv_index_max = wea_dict(day, "uvIndexMax")

        daytime = day['daytime']    # 白天预报
        day_info = _half_day_js(daytime, "日")

        nighttime = day['nighttime']    # 夜间预报
        night_info = _half_day_js(nighttime, "夜")

        result = {
            "other": [
                time, sun, moon, moon_prase,temp, uv_index_max
            ],
            "day": day_info,
            "night": night_info,
            "infrequent": [
                astronomical_dawn, astronomical_dusk, nautical_dawn, nautical_dusk,
                civil_dawn, civil_dusk, solar_noon, solar_midnight, moon_transit,
                moon_underfoot
            ]
        }
        msg += [
            "\n".join(result.get("other", "")) +
            "\n======日天气预报======\n├" +
            "\n├".join(result.get("day", "")) +
            "\n======夜天气预报======\n├" +
            "\n├".join(result.get("night", "")) +
            "\n====不常用天气预报=====\n├" +
            "\n├".join(result.get("infrequent", "")) +
            "\n" + LICE
        ]
    return msg


def _now_o_hour_js(data: dict, concise: bool = False) -> list[str]:
    time = data.get('forecastTime', '')
    time = "预报时间" + iso_format_time(time, "%H:%M") if time else ""
    text = wea_dict(data['condition'], 'text') + icon.get(data['condition']['code'], '')
    temp = (
        f"当前气温：{value_unit(data, '')}"
        f"（体感：{value_unit(data, 'feelsLike')}）"
    )
    humidity = f"相对湿度：{data['humidity'] * 100}%"
    wind = (
        f"风向风力：{wind_direction(data['wind']['direction']['compass'])}"
        f"{data['wind']['scale']}级（{value_unit(data['wind'], 'speed')}）"
    )

    probability = data['precipitation'].get('probability')
    if concise:
        precip = (
            f"降水情况：{value_unit(data['precipitation'], 'amount')}"
            f"（{value_unit(data['precipitation'], 'intensity')}）"
        )
        return [text, temp, humidity, precip]

    precip = (
        (f"降水概率：{probability * 100}%\n" if probability else "") +
        f"累计降水量：{value_unit(data['precipitation'], 'amount')}"
        f"\n降水强度：{value_unit(data['precipitation'], 'intensity')}"
    )
    pressure = "当前气压：" + value_unit(data, 'pressure')
    visibility = "能见度：" + value_unit(data, 'visibility')
    dew = "露点温度：" + value_unit(data, 'dewPoint')
    cloud = f"当前云量：{data['cloudCover']}%"
    uv = f"紫外线指数：{data['uvIndex']}"
    return [
        time, text, temp, humidity, wind, precip, pressure,
        visibility, dew, cloud, uv
    ]


def wea_json_loader(
        data: dict,
        *args,
        concise: bool = False,
) -> list[str]:
    """
    天气预报解析，每小时/天各返回一个 MessageSegment.text
    :param data: 和风天气API返回的json
    :param concise: 简介模式：只返回最常用信息。默认不开启
    """
    if data.get("error"):
        if concise:
            return ["天气信息获取失败"]
        return [str(data)]

    a = data['metadata']['attributions'] or ''
    attribution = "声明：数据来自" + "，".join(i for i in a if i.strip())

    msg = ["\n".join(args) + attribution]
    if data.get("days"):
        data = data['days']
        result = msg + _day_js(data)
    elif data.get("hours"):
        data = data['hours']
        result = [*msg]
        for hour in data:
            result += ["\n".join(_now_o_hour_js(hour) + [LICE])]
    else:
        if concise:
            result = _now_o_hour_js(data, True)
        else:
            result = [
                "\n".join(args) + "\n".join(_now_o_hour_js(data) + ['\n', LICE])
            ]
    return result


def _aqijs(
        data: dict,
        attributions: str = "",
        concise: bool = False
) -> list[str] | str:
    time = "预报时间：" + iso_format_time(
        data['forecastTime'], "%Y年%m月%d日 %H:%M"
    ) if data.get('forecastTime') else (
        "预报有效范围："
        f"{iso_format_time(data['forcastStartTime'], '%Y年%m月%d日 %H:%M')}"
        f"至{iso_format_time(data['forcastEndTime'], '%Y年%m月%d日 %H:%M')}"
    ) if data.get('forcastStartTime') else ""
    index = data['indexes'][0]
    _aqi = f"{index['name']}：{index['aqiDisplay']}"
    if concise:
        return _aqi + f"（{index['category']}）"

    leve = f"等级类别：{index['level']}（{index['category']}）"
    pollutant = "首要污染：" + (index['primaryPollutant'] or {}).get('name', "无")

    health = index['health']
    effect = f"影响：{health['effect']}" if health['effect'] else ""

    health = health['advice']
    normal = health.get('generalPopulation', '')
    special = health.get('sensitivePopulation', '')
    if normal == special:
        advice = normal
    elif normal and special:
        advice = (
            f"对于一般人群来说，{normal} \n"
            f"对于敏感人群来说，{special}"
        )
    else:
        advice = ""

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

    return [time, _aqi, leve, pollutant, effect, advice, sender, attributions, LICE]


def aqi_json_loader(
        data: dict,
        *args,
        concise: bool = False
) -> str | list[str] | None:
    if data.get("error"):
        if concise:
            return None
        return [str(data)]

    logger.debug(data)
    #tag   = js["metadata"]["tag"]
    attributions = "，".join(i for i in data['metadata']['attributions'])

    if concise:
        return _aqijs(data, concise=concise)

    if data.get('indexes'):
        result = [*args, *_aqijs(data, "声明：数据来源" + attributions)]
        msg = ["\n".join(i for i in result if i.strip())]
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


async def default_wea_json_loader(
        lat: float | int,
        lon: float | int,
        *args,
) -> list[str]:
    war_data = await war(lat, lon)
    _war = await war_json_loader(war_data, True)
    if _war is None:
        _war = []
    attribution = war_data['metadata'].get('attributions', []) if _war else []

    wea_now = await wea(lat, lon, 1)
    attribution += wea_now['metadata'].get('attributions', [])
    wea_now_data = wea_json_loader(wea_now, concise=True)

    aqi_data = await aqi(lat, lon, 4)
    aqi_now_data = aqi_json_loader(aqi_data, concise=True)

    precip_data = await rain(lat, lon)
    code = precip_data.get("code", "无")

    if code != "200":
        logger.debug(precip_data)
        logger.error(f"分钟降水信息获取失败！错误码：{code}")
    precip = precip_data.get('summary', '')

    wea_daily = await wea(lat, lon, 3)
    wea_daily_data = wea_daily.get("days")
    if wea_daily_data:
        attribution += wea_daily['metadata'].get('attributions', [])
        data_1 = wea_daily_data[0]
        day = data_1['astro']
        now = dt.now().strftime("%H:%M")
        sunrise = iso_format_time(day.get("sunrise", ""), "%H:%M")
        sunset = iso_format_time(day.get("sunset", ""), "%H:%M")
        moonrise = iso_format_time(day.get("moonrise", ""), "%H:%M")
        moonset = iso_format_time(day.get("moonset", ""), "%H:%M")

        sunrise = (
            f"太阳将在{h_m_time_diff(sunrise, now)}后({sunrise})升起"
            if now < sunrise else ""
        ) if sunrise else ""
        sunset = (
            f"将在{h_m_time_diff(sunset, now)}后({sunset})落下"
            if now < sunset else ""
        ) if sunset else ""
        moonrise = (
            f"月亮将在{h_m_time_diff(moonrise, now)}后({moonrise})升起"
            if now < moonrise else ""
        ) if moonrise else ""
        moonset = (
            f"将在{h_m_time_diff(moonset, now)}后({moonset})落下"
            if now < moonset else ""
        ) if moonset else ""

        uv_index = wea_dict(data_1, 'uvIndexMax')
        temp = (
            f"当日气温：{value_unit(data_1, 'Min')}"
            f"~{value_unit(data_1, 'Max')}"
        )
        is_rain = "雨" in data_1['daytime']['condition']['text']

        sun = (
            sunrise + "并" + sunset
            if sunrise and sunset else sunrise or (
                "太阳" + sunset if sunset else ""
            )
        )
        moon = (
            moonrise + "并" + moonset
            if moonrise and moonset else moonrise or (
                "月亮" + moonset if moonset else ""
            )
        )

        count_day = 0
        text_day = "这几天天气无明显变化哦~"
        for day in wea_daily_data[1:]:
            count_day += 1
            if not is_rain:
                day_rain = day['daytime']['condition']['text']
                night_rain = day['nighttime']['condition']['text']
                if "雨" in day_rain:
                    text_day = (
                        f"{WEA['count_day'].get(count_day, f'{count_day}天后')}"
                        f"的白天可能会有{day_rain}哦"
                    )
                    break
                elif "雨" in night_rain:
                    text_day = (
                        f"{WEA['count_day'].get(count_day, f'{count_day}天后')}"
                        f"的晚上可能会有{night_rain}哦"
                    )
            else:
                if not "雨" in day['daytime']['condition']['text']:
                    text_day = (
                        f"{WEA['count_day'].get(count_day, f'{count_day}天后')}"
                        f"的白天可能开始不下雨哦"
                    )
                    break
                elif not "雨" in day['nighttime']['condition']['text']:
                    text_day = (
                        f"{WEA['count_day'].get(count_day, f'{count_day}天后')}"
                        f"的晚上可能开始不下雨哦"
                    )
        else:
            text_day += "，一直是晴天呢" if not is_rain else "，一直在下雨哦"
        wea_daily_data = [temp, uv_index, "-" * 20, precip, text_day, "-" * 25, sun, moon]
    else:
        wea_daily_data = ["天气预报获取失败", precip]

    message = list(args) + [aqi_now_data] + wea_now_data + wea_daily_data + [
        "声明：数据来自" + "，".join(
                i for i in (list(dict.fromkeys(attribution)))
            ) if attribution else ""
        ]

    if _war:
        message.append("\n※=====※ 发现预警 ※=====※\n")
        message += [i for i in _war]
    message += ["\n" + LICE]

    return message
