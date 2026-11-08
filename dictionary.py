from tools import iso_format_time

WEA = {
    "astronomicalDawn": "天文晨光开始时间",
    "astronomicalDusk": "天文暮光结束时间",
    "civilDawn": "民用晨光开始时间",
    "civilDusk": "民用暮光结束时间",
    "cloud": "当前云量",
    "dew": "露点温度",
    "feelsLike": "体感温度",
    "fxDate": "预报日期",
    "fxTime": "预报时间",
    "humidity": "相对湿度",
    "moonPhase": "今日月相",
    "moonrise": "月出时间",
    "moonset": "月落时间",
    "moonTransit": "月亮上中天时间",
    "moonUnderfoot": "月亮下中天时间",
    "nauticalDawn": "航海晨光开始时间",
    "nauticalDusk": "航海暮光结束时间",
    "obsTime": "观测时间",
    "pop": "降水概率",
    "precip": "降水量",
    "pressure": "站点气压",
    "solarMidnight": "太阳子夜时间",
    "solarNoon": "太阳正午时间",
    "sunrise": "日出时间",
    "sunset": "日落时间",
    "temp": "当前气温",
    "text": "当前天气",
    "tempMax": "最高温",
    "tempMin": "最低温",
    "textDay": "白天",
    "textNight": "夜晚",
    "uvIndex": "紫外线指数",
    "uvIndexMax": "当日最大紫外线指数",
    "vis": "能见度",
    "windDir": "风向",
    "windDirDay": "日风向",
    "windDirNight": "夜风向",
    "windScale": "风级",
    "windScaleDay": "日风级",
    "windScaleNight": "夜风级",
    "windSpeed": "风速",
    "windSpeedDay": "日风速",
    "windSpeedNight": "夜风速",
    "count_day": {
        -3: "大前天",
        -2: "前天",
        -1: "昨天",
        0: "今天",
        1: "明天",
        2: "后天",
        3: "大后天"
    },
}
WEA_unit = {
    "cloud": "%",
    "dew": "℃",
    "feelsLike": "℃",
    "fxDate": "",
    "fxTime": "",
    "humidity": "%",
    "moonrise": "",
    "moonset": "",
    "moonPhase": {
        "new-moon": "新月",
        "waxing-crescent": "蛾眉月",
        "first-quarter": "上弦月",
        "waxing-gibbous": "盈凸月",
        "full-moon": "满月",
        "waning-gibbous": "亏凸月",
        "last-quarter": "下弦月",
        "waning-crescent": "残月"
    },
    "obsTime": "",
    "pop": "%",
    "precip": "mm",
    "pressure": "HPa",
    "sunrise": "",
    "sunset": "",
    "temp": "℃",
    "tempMax": "℃",
    "tempMin": "℃",
    "text": "",
    "textDay": "",
    "textNight": "",
    "uvIndex": "",
    "vis": "km",
    "windDir": "",
    "windDirDay": "",
    "windDirNight": "",
    "windScale": "级",
    "windScaleDay": "级",
    "windScaleNight": "级",
    "windSpeed": "km/h",
    "windSpeedDay": "km/h",
    "windSpeedNight": "km/h",
}
AQI = {
    "indexes": {
        "aqi": "空气指数",
        "level": "指数等级",
        "category": "指数情况",
        "primaryPollutant": {
            "name": "首要污染物"
        },
        "health": {
            "effect": "影响",
            "advice": {
                "generalPopulation": "对普通人群的建议",
                "sensitivePopulation": "对敏感人群的建议"
            },
        },
    },
    "pollutants": {
        "name": "污染物",
        "concentration": {
            "value": "浓度值"
        },
    },
    "station": "监测站"
}
mod = {
    1: "实时天气",
    2: "逐小时天气",
    3: "每日天气",
    4: "实时空气质量",
    5: "逐小时空气质量",
    6: "每日空气质量",
    7: "实时预警"
}
icon = {
    "9999": "⚠️",
    "2551": "💨",
    "2552": "❄️",
    "2553": "⚡️",
    "2029": "⚡️",
    "2123": "🌪",
    "807": "🌘",
    "806": "🌗",
    "805": "🌖",
    "804": "🌕",
    "803": "🌔",
    "802": "🌓",
    "801": "🌒",
    "800": "🌑",
    "307": "🌨",
    "306": "🌧",
    "305": "🌨",
    "302": "⛈",
    "303": "⛈",
    "100": "☀️",
    "101": "🌥",
    "102": "⛅️",
    "103": "🌤",
    "104": "☁️",
    "150": "🌙",
    "300": "🌦",
    "301": "🌦",
}
WAR = {
    "urgency": {
        "immediate": "必须立刻采取行动！",
        "expected": "应尽快采取行动（通常在1小时内）",
        "future": "应在近期采取行动",
        "past": "事件已不再发生",
        "unknown": "紧急性未知！"
    },
    "severity": {
        "unknown": "提示：严重性未知！",
        "minor": "提示：对生命或财产构成的威胁极小或没有已知威胁",
        "moderate": "提示：对生命或财产可能构成威胁！",
        "severe": "提示：对生命或财产构成的重大威胁",
        "extreme": "提示：对生命或财产构成的严重威胁"
    },
    "certainty": {
        "observed": "可能性：事件已经发生或正在发生",
        "likely": "可能性；发生概率大于约50%",
        "unlikely": "可能性：预计不会发生（概率接近0）",
        "unknown": "可能性：确定性未知！"
    },
    "color": {
        "white": "⚪",
        "gray": "🩶",
        "green": "🟢",
        "blue": "🔵",
        "yellow": "🟡",
        "amber": "（琥珀色）",
        "orange": "🟠",
        "red": "🔴",
        "purple": "🟣",
        "black": "⚫"
    },
    "color_text": {
        "white": "白",
        "gray": "灰",
        "green": "绿",
        "blue": "蓝",
        "yellow": "黄",
        "amber": "琥珀",
        "orange": "橙",
        "red": "红",
        "purple": "紫",
        "black": "黑"
    }
}
_WIND_DIRECTIONS = {
    "n":   ("北风",         "North"),
    "nne": ("东北偏北风",   "North-Northeast"),
    "ne":  ("东北风",       "Northeast"),
    "ene": ("东北偏东风",   "East-Northeast"),
    "e":   ("东风",         "East"),
    "ese": ("东南偏东风",   "East-Southeast"),
    "se":  ("东南风",       "Southeast"),
    "sse": ("东南偏南风",   "South-Southeast"),
    "s":   ("南风",         "South"),
    "ssw": ("西南偏南风",   "South-Southwest"),
    "sw":  ("西南风",       "Southwest"),
    "wsw": ("西南偏西风",   "West-Southwest"),
    "w":   ("西风",         "West"),
    "wnw": ("西北偏西风",   "West-Northwest"),
    "nw":  ("西北风",       "Northwest"),
    "nnw": ("西北偏北风",   "North-Northwest"),
    "none": ("静风（无风）", "Calm"),
    "vrb": ("风向不定",      "Variable"),
}


def value_unit(data, data_type):
    _data = data[
        f'temperature{data_type}' if data_type in {'Max', 'Min', ''} else data_type
    ]
    return str(_data.get('value')) + _data.get('unit')

def wea_dict(
        data: dict,
        data_key: str,
        unit_key: str  = "",
        data_is_time: str = "",
        default: str = ""
) -> str:
    """
    根据字典按照 [名称：值&单位] 的格式解析字典
    :param data: 需要解析的内容
    :param data_key: 字典索引
    :param unit_key: 单位索引
    :param data_is_time: 传入内容时认为获得的值是时间，并且按照此内容格式化值
    :param default: 无内容时的默认返回值
    """
    reason = f"{WEA.get(data_key, '')}："
    if unit_key and not data_is_time:
        reason += value_unit(data, unit_key)
    else:
        reason += (((
            str(data.get(data_key, '')) if not data_is_time else iso_format_time(
                data.get(data_key, ''), data_is_time
            )) or default) + (
            data.get(unit_key, '') if unit_key else str(
                WEA_unit.get(data_key, '')
            )
        ))
    return reason


def sun_moon(data, data_type="日", default=""):
    _name = {"日": "sun", "月": "moon"}.get(data_type)

    rise = data[f"{_name}rise"]
    set = data[f"{_name}set"]
    if rise and set:
        astro = (
            f"{data_type}出时间：{iso_format_time(data[f'{_name}rise'], '%H:%M')}"
            f"-{iso_format_time(data[f'{_name}set'], '%H:%M')}"
        )
    elif rise and not set:
        astro = wea_dict(data, f"{_name}rise", data_is_time="%H:%M")
    elif set and not rise:
        astro = wea_dict(data, f"{_name}set", data_is_time="%H:%M")
    else:
        astro = default

    return astro


def wind_direction(code: str | None, lang: str = "zh", default: str | None = None) -> str:
    """
    将风向方位码转换为用户友好的风向文本。
    :param code:    风向方位码，如 "nne"、"VRB"，大小写/首尾空格均可容忍
    :param lang:    "zh" 返回中文，"en" 返回英文
    :param default: 无法识别时的返回值；为 None 时返回原始输入
    :return:        风向描述文本
    """
    if code is None:
        return default if default is not None else ""

    key = str(code).strip().lower()
    item = _WIND_DIRECTIONS.get(key)
    if item is None:
        return default if default is not None else str(code)

    return item[0] if lang == "zh" else item[1]
