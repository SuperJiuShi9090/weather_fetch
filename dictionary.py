WEA = {
    "cloud": "当前云量",
    "dew": "露点温度",
    "feelsLike": "体感温度",
    "fxDate": "预报日期",
    "fxTime": "预报时间",
    "humidity": "相对湿度",
    "moonPhase": "月相",
    "moonrise": "月出时间",
    "moonset": "月落时间",
    "obsTime": "观测时间",
    "pop": "降水概率",
    "precip": "降水量",
    "pressure": "站点气压",
    "sunrise": "日出时间",
    "sunset": "日落时间",
    "temp": "当前气温",
    "text": "当前天气",
    "tempMax": "最高温",
    "tempMin": "最低温",
    "textDay": "白天",
    "textNight": "夜晚",
    "uvIndex": "紫外线指数",
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
    "moonPhase": "",
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
    "1": "实时天气",
    "2": "逐小时天气",
    "3": "每日天气",
    "4": "实时空气质量",
    "5": "逐小时空气质量",
    "6": "每日空气质量",
    "7": "实时预警"
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


def wea_dict(data: dict, data_key: str, default="") -> str:
    reason = (
        f"{WEA.get(data_key, '')}："
        f"{data.get(data_key) or default}"
        f"{WEA_unit.get(data_key, '')}"
    )
    return reason
