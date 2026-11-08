import asyncio
import html
import io
import math
import re
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

# -------------- 路径配置 ------------------ #
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates.html"
STYLE_PATH = BASE_DIR / "style.css"
SCRIPT_PATH = BASE_DIR / "render.js"


# --------------- 文本排版工具 --------------- #
def calc_grid(text: str):
    """
    根据文字长度计算网格布局，目标比例横 2 : 纵 3
    阅读顺序：从左往右，再从上往下（行优先）
    返回 (cols, rows, grid)
    """
    length = len(text)
    if length == 0:
        return 1, 1, [[""]]

    best_cols, best_rows = 1, length
    best_diff = float("inf")

    for rows in range(1, length + 1):
        cols = math.ceil(length / rows)
        if rows > 0:
            ratio = cols / rows
            target = 2 / 3
            diff = abs(ratio - target)
            score = diff * 1000 + (cols * rows - length)
            if score < best_diff:
                best_diff = score
                best_cols, best_rows = cols, rows

    grid = [["" for _ in range(best_cols)] for _ in range(best_rows)]
    idx = 0
    for row in range(best_rows):
        for col in range(best_cols):
            if idx < length:
                grid[row][col] = text[idx]
                idx += 1

    return best_cols, best_rows, grid


def build_char1_html(text: str) -> str:
    """
    构建 char_1 的 HTML 内容：
    - 字数 <= 2：纯竖排
    - 字数 > 2：按横 2 : 纵 3 比例网格排版（行优先）
    """
    text = "" if text is None else str(text)
    length = len(text)

    if length <= 2:
        escaped = html.escape(text)
        return (
            f'<div id="char1" class="auto-text-vertical" data-text="{escaped}">'
            f'{escaped}'
            f'</div>'
        )

    cols, rows, grid = calc_grid(text)

    cells_html = ""
    for row_idx in range(rows):
        for col_idx in range(cols):
            ch = html.escape(grid[row_idx][col_idx])
            if not ch:
                ch = "&nbsp;"
            cells_html += (
                f'<div class="grid-cell" data-row="{row_idx}" '
                f'data-col="{col_idx}">{ch}</div>'
            )

    return (
        f'<div id="char1" class="grid-text-container" '
        f'data-text="{html.escape(text)}" '
        f'data-cols="{cols}" data-rows="{rows}">'
        f'<div class="grid-layout" '
        f'style="grid-template-columns: repeat({cols}, 1fr); '
        f'grid-template-rows: repeat({rows}, 1fr);">'
        f'{cells_html}'
        f'</div>'
        f'</div>'
    )


def wrap_text_every_n(text: str, n: int = 33) -> str:
    """每 n 个字符插入一个 <br>，实现 HTML 中的自动换行。"""
    if not text:
        return ""
    parts = [html.escape(text[i:i + n]) for i in range(0, len(text), n)]
    return "<br>".join(parts)


# ---------------- 模板装配 -------------------- #
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _build_html(
    *,
    svg: str,
    char1_html: str,
    char2: str,
    char3: str,
    char4_wrapped: str,
    bg_color: str,
    frame_color: str,
    svg_color: str,
) -> str:
    template = _read(TEMPLATE_PATH)
    style = _read(STYLE_PATH)
    script = _read(SCRIPT_PATH)

    # 先替换 CSS 里的变量占位符
    style = (
        style
        .replace("__BG_COLOR__", bg_color)
        .replace("__FRAME_COLOR__", frame_color)
        .replace("__SVG_COLOR__", svg_color)
    )

    # 再装配整体 HTML
    return (
        template
        .replace("__STYLE__", style)
        .replace("__SCRIPT__", script)
        .replace("__SVG__", svg)
        .replace("__CHAR1_HTML__", char1_html)
        .replace("__CHAR2__", char2)
        .replace("__CHAR3__", char3)
        .replace("__CHAR4_WRAPPED__", char4_wrapped)
    )


# ------------------ 主渲染函数 ------------------- #
async def pic_create(
    svg: str,
    char_1: str,
    char_2: str,
    char_3: str,
    char_4: str,
    color: list[int],
    pic_size: int = 256,
):
    """
    UI 图片生成：返回 PNG 的 bytes。

    :param svg:        左上角 SVG 图片代码
    :param char_1:     右上角文字（<=2 竖排，>2 网格排版）
    :param char_2:     左下角文字
    :param char_3:     右下角英文
    :param char_4:     图片底部小字
    :param color:      RGB 列表，例如 [255, 0, 0]
    :param pic_size:   输出图片边长，默认 256
    """
    if not isinstance(color, list) or len(color) != 3:
        raise ValueError("color 必须是类似 [255, 165, 0] 的 RGB 列表")

    r, g, b = [max(min(255, x), 0) for x in color]
    bg_color = f"rgb({r}, {g}, {b})"
    frame_color = "#777985"
    svg_color = bg_color

    if not isinstance(svg, str):
        raise ValueError("svg 必须是字符串")

    svg = svg.strip()
    if not svg:
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"></svg>'

    match = re.search(r"<svg\b[\s\S]*?</svg>", svg, re.IGNORECASE)
    if match:
        svg = match.group(0)

    svg = re.sub(
        r"<svg\b",
        '<svg style="width:100%;height:100%;"',
        svg,
        count=1,
        flags=re.IGNORECASE,
    )

    char_1 = str(char_1 or "")
    char_2 = html.escape(str(char_2 or ""))
    char_3 = html.escape(str(char_3 or ""))
    char_4 = html.escape(str(char_4 or ""))

    char1_html = build_char1_html(char_1)

    html_code = _build_html(
        svg=svg,
        char1_html=char1_html,
        char2=char_2,
        char3=char_3,
        char4_wrapped=char_4,
        bg_color=bg_color,
        frame_color=frame_color,
        svg_color=svg_color,
    )


    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={"width": 256, "height": 256},  # type: ignore
            device_scale_factor=1,
        )

        await page.set_content(html_code, wait_until="load")
        await page.wait_for_timeout(200)
        await page.evaluate(
            """
            async () => {
                if (document.fonts) {
                    await document.fonts.ready;
                }
                if (typeof renderUI === 'function') {
                    await renderUI();
                }
            }
            """
        )

        png_bytes = await page.locator("#canvas").screenshot(
            type="png",
            omit_background=True,
        )
        await browser.close()

    if pic_size != 256:
        pic_size = max(64, int(pic_size))

        image = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        image = image.resize((pic_size, pic_size), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        image.save(output, format="PNG")
        png_bytes = output.getvalue()

    return png_bytes


if __name__ == "__main__":
    with open("../QWeather-Icons-1.8.0/icons/qweather.svg", "r", encoding="utf-8") as f:
        SVG = f.read()

    pic = asyncio.run(
        pic_create(
            SVG,
            "测试",
            "壹",
            "Test",
            "•注：这是测试",
            [255, 0, 0]
        )
    )
    with open("test_pic.png", "wb") as f:
        f.write(pic)
