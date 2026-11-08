"""发起网络请求并返回JSON内容，解析失败返回空字典"""
from datetime import datetime

import httpx
import pytz
import re

from config import *
from LOG import *

from typing import Tuple

logger = logging.getLogger(__name__)

MEANINGLESS_PATTERNS = [
    r"^[\W_]+$",  # 纯符号
    r"^[\d\s\.]+$"  # 纯数字/空格/点
    r'^[\w\s]+$',  # emoji等纯非单词字符
]


def h_m_time_to_minutes(time):
    h, m = time.split(":")
    return int(h) * 60 + int(m)


def h_m_time_diff(time1, time2):
    m1 = h_m_time_to_minutes(time1)
    m2 = h_m_time_to_minutes(time2)
    diff = abs(m2 - m1)
    h = diff // 60 if diff >= 60 else 0
    m = diff - h * 60

    if h or m:
        return (f"{h}h" if h else "") + (f"{m}m" if m else "")
    return "0m"

def dms_to_decimal(deg_str, min_str, sec_str, direction):
    """将度分秒转换为十进制度。"""
    deg = float(deg_str) if deg_str else 0.0
    minute = float(min_str) if min_str else 0.0
    second = float(sec_str) if sec_str else 0.0
    decimal = deg + minute / 60.0 + second / 3600.0
    direction = direction.upper() if direction else ''
    if direction in ('S', 'W'):
        decimal = -decimal
    return decimal, direction


def parse_location(text: str) -> list | str:
    """
    解析包含经纬度信息的文本，返回 [经度, 纬度] 列表（最多两位小数）。
    支持十进制和度分秒（DMS）格式。
    经度在前，纬度在后。北纬/东经为正，南纬/西经为负。

    和风天气 GeoAPI 查询时需转换为字符串 "经度,纬度"。
    """
    if not text:
        return ""

    # 1. 统一全角符号和中文方向词
    text = (
        text.replace('，', ',')
        .replace('东经', 'E').replace('西经', 'W')
        .replace('北纬', 'N').replace('南纬', 'S')
        .replace('东', 'E').replace('西', 'W')
        .replace('北', 'N').replace('南', 'S')
    )

    # 2. 先尝试匹配度分秒（DMS）格式
    #    匹配模式：度 分 秒 方向（方向可在最后或最前）
    dms_pattern = re.compile(
        r'([+-]?\d+(?:\.\d+)?)\s*°?\s*'          # 度
        r'(?:(\d+(?:\.\d+)?)\s*[\'′]?\s*)?'       # 分（可选）
        r'(?:(\d+(?:\.\d+)?)\s*[\"″]?\s*)?'       # 秒（可选）
        r'([EWNSewns]?)'                            # 方向
    )
    dms_matches = dms_pattern.findall(text)

    lon = None
    lat = None

    # 优先使用 DMS 解析结果
    if len(dms_matches) >= 2:
        for deg_str, min_str, sec_str, direction in dms_matches[:4]:
            dec, dir_ = dms_to_decimal(deg_str, min_str, sec_str, direction)
            if dir_ in ('E', 'W') and lon is None:
                lon = dec
            elif dir_ in ('N', 'S') and lat is None:
                lat = dec
            elif lon is None:
                lon = dec
            elif lat is None:
                lat = dec

    # 3. 如果 DMS 解析不完整，回退到简单的十进制解析
    if lon is None or lat is None:
        # 更宽松的十进制匹配，避免误吞度分秒中的数字
        simple_pattern = r'([+-]?\d+(?:\.\d+)?)\s*°?\s*([EWNSewns]?)'
        simple_matches = re.findall(simple_pattern, text)
        # 过滤掉明显是分或秒的短数字（如果前面有度符号）
        filtered = []
        for i, (val, d) in enumerate(simple_matches):
            # 如果这个数字后面紧跟着 ' 或 "，且不是第一个数字，可能是分或秒
            # 简单处理：只取第一个和第二个有方向标记或看起来像度的数字
            filtered.append((val, d))
        # 取前两个有效对
        for val_str, direction in filtered:
            if lon is not None and lat is not None:
                break
            direction = direction.upper() if direction else ''
            try:
                val = float(val_str)
            except ValueError:
                continue
            if direction in ('E', 'W'):
                if lon is None:
                    lon = -val if direction == 'W' else val
            elif direction in ('N', 'S'):
                if lat is None:
                    lat = -val if direction == 'S' else val
            else:
                if lon is None:
                    lon = val
                elif lat is None:
                    lat = val

    # 4. 最终校验
    if lon is None or lat is None:
        return ""
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        return ""

    return [round(lon, 2), round(lat, 2)]


def validate_input(text: str) -> Tuple[bool, str]:
    """
    校验输入内容是否有效
    :param text: 需要检测的字符串
    :return: 是否有效，错误原因
    """
    text = text.strip()
    if not text:
        return False, "请输入要查询的地点名称或坐标！"

    if len(text) < 2:
        return False, "输入内容太短，并没有意义"

    if len(text) > 32:
        return False, "输入内容过长，并没有必要写这么多"

    for pattern in MEANINGLESS_PATTERNS:
        if re.match(pattern, text):
            return False, "请不要输入无意义内容。。。"

    return True, ""


async def fetch_json(url: str, headers: dict | None, timeout: int =5) -> dict:
    async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
        for i in range(1, 4):
            try:
                r = await client.get(url, timeout=timeout)
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

def iso_format_time(time: str, time_format: str ="%Y-%m-%d %H:%M:%S"):
    """将 ISO 时间转换为指定格式的 GMT+8 时间

    Args:
        time (_type_): ISO 时间
        time_format (_type_): 输出的时间格式
    """
    # 解析为datetime对象
    dt = datetime.fromisoformat(time)

    # 设置时区
    tz = pytz.timezone('Asia/Shanghai')
    dt_gmt8 = dt.astimezone(tz)
    formatted_time = dt_gmt8.strftime(time_format)
    return formatted_time
