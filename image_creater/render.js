function fitText(element, minSize, maxSize, isVertical) {
    if (!element) return;

    const text = element.dataset.text || element.textContent || "";
    if (!text.trim()) {
        element.textContent = "";
        return;
    }

    const parent = element.parentElement;
    if (!parent) return;

    const style = window.getComputedStyle(element);
    const padLeft = parseFloat(style.paddingLeft) || 0;
    const padRight = parseFloat(style.paddingRight) || 0;
    const padTop = parseFloat(style.paddingTop) || 0;
    const padBottom = parseFloat(style.paddingBottom) || 0;

    let availableWidth, availableHeight;
    if (isVertical) {
        availableWidth = parent.clientHeight - padTop - padBottom;
        availableHeight = parent.clientWidth - padLeft - padRight;
    } else {
        availableWidth = parent.clientWidth - padLeft - padRight;
        availableHeight = parent.clientHeight - padTop - padBottom;
    }

    let low = minSize;
    let high = maxSize;
    let best = minSize;

    const measurer = document.createElement('span');
    measurer.style.cssText =
        'position:absolute;visibility:hidden;white-space:nowrap;' +
        'font-family:inherit;font-weight:inherit;line-height:1;';
    if (isVertical) {
        measurer.style.writingMode = 'vertical-lr';
        measurer.style.textOrientation = 'upright';
    }
    element.appendChild(measurer);

    while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        measurer.style.fontSize = mid + 'px';
        measurer.textContent = text;

        const rect = measurer.getBoundingClientRect();
        let textWidth, textHeight;
        if (isVertical) {
            textWidth = rect.height;
            textHeight = rect.width;
        } else {
            textWidth = rect.width;
            textHeight = rect.height;
        }

        if (textWidth <= availableWidth - 1 && textHeight <= availableHeight - 1) {
            best = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    element.removeChild(measurer);
    element.style.fontSize = best + 'px';
}


function fitSVG() {
    const container = document.querySelector(".svg-container");
    const svg = container.querySelector("svg");
    if (!svg) return;

    const viewBox = svg.getAttribute("viewBox");
    if (!viewBox) {
        const width = parseFloat(svg.getAttribute("width"));
        const height = parseFloat(svg.getAttribute("height"));
        if (Number.isFinite(width) && Number.isFinite(height)) {
            svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
        }
    }

    svg.style.maxWidth = "100%";
    svg.style.maxHeight = "100%";
    svg.style.width = "auto";
    svg.style.height = "auto";

    if (svg.getAttribute("viewBox")) {
        const vb = svg.getAttribute("viewBox").trim().split(/[ ,]+/).map(Number);
        if (vb.length === 4) {
            const vw = Math.abs(vb[2]);
            const vh = Math.abs(vb[3]);
            const cw = container.clientWidth;
            const ch = container.clientHeight;
            if (vw > 0 && vh > 0) {
                const scale = Math.min(cw / vw, ch / vh);
                svg.style.width = Math.floor(vw * scale) + "px";
                svg.style.height = Math.floor(vh * scale) + "px";
            }
        }
    }
}


function fitGridText() {
    const gridContainer = document.querySelector('.grid-text-container');
    if (!gridContainer) return;

    const gridLayout = gridContainer.querySelector('.grid-layout');
    if (!gridLayout) return;

    const cells = gridLayout.querySelectorAll('.grid-cell');
    if (cells.length === 0) return;

    const cols = parseInt(gridContainer.dataset.cols) || 1;
    const rows = parseInt(gridContainer.dataset.rows) || 1;

    const containerStyle = window.getComputedStyle(gridContainer);
    const padLeft = parseFloat(containerStyle.paddingLeft) || 0;
    const padRight = parseFloat(containerStyle.paddingRight) || 0;
    const padTop = parseFloat(containerStyle.paddingTop) || 0;
    const padBottom = parseFloat(containerStyle.paddingBottom) || 0;

    const availableWidth = gridContainer.clientWidth - padLeft - padRight;
    const availableHeight = gridContainer.clientHeight - padTop - padBottom;

    const gap = 1; // 与 CSS 中的 gap 保持一致
    const cellW = (availableWidth - gap * (cols - 1)) / cols;
    const cellH = (availableHeight - gap * (rows - 1)) / rows;

    let maxText = "";
    cells.forEach(cell => {
        const text = cell.textContent || "";
        if (text.length > maxText.length) maxText = text;
    });

    if (!maxText.trim()) return;

    let low = 8;
    let high = Math.min(cellW, cellH);
    let best = 8;

    const measurer = document.createElement('span');
    measurer.style.cssText =
        'position:absolute;visibility:hidden;white-space:nowrap;' +
        'font-family:inherit;font-weight:900;line-height:1;';
    gridContainer.appendChild(measurer);


    while (low <= high) {
        const mid = Math.floor((low + high) / 2);
        measurer.style.fontSize = mid + 'px';
        measurer.textContent = maxText;

        const rect = measurer.getBoundingClientRect();
        if (rect.width <= cellW - 2 && rect.height <= cellH - 2) {
            best = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    gridContainer.removeChild(measurer);

    cells.forEach(cell => {
        cell.style.fontSize = best + 'px';
    });
}


async function renderUI() {
    if (document.fonts) await document.fonts.ready;
    await new Promise(r => setTimeout(r, 50));

    const CANVAS_SIZE      = 256;
    const FOOTER_BOTTOM    = 5;    // 与 CSS bottom 一致
    const FOOTER_GAP       = 4;    // footer 顶边与上方面板底边的间距
    const PANEL_TOP        = 176;  // panel-char2/3 的 top
    const PANEL_MIN_H      = 30;   // 上方面板允许压缩到的最小高度
    const PANEL_ORIG_BOTTOM = 231; // 176 + 55

    const footer = document.getElementById("footer");
    const panel2 = document.querySelector(".panel-char2");
    const panel3 = document.querySelector(".panel-char3");

    // ---- 1. 动态 footer 高度 + 压缩上方面板 ----
    if (footer.textContent.trim()) {
        footer.style.height    = "auto";
        footer.style.maxHeight = "none";
        footer.style.overflow  = "visible";

        let footerH = footer.getBoundingClientRect().height;

        // 上限：不能把 panel-char2/3 压到 < PANEL_MIN_H
        const maxFooterH = CANVAS_SIZE - FOOTER_BOTTOM
                         - (PANEL_TOP + PANEL_MIN_H) - FOOTER_GAP; // = 41
        if (footerH > maxFooterH) {
            footerH = maxFooterH;
            footer.style.height   = footerH + "px";
            footer.style.overflow = "hidden";   // 超出部分裁掉，字号不变
        }

        const footerTop   = CANVAS_SIZE - FOOTER_BOTTOM - footerH;
        const panelBottom = Math.min(PANEL_ORIG_BOTTOM, footerTop - FOOTER_GAP);
        const panelH      = Math.max(PANEL_MIN_H, panelBottom - PANEL_TOP);

        panel2.style.height = panelH + "px";
        panel3.style.height = panelH + "px";
    } else {
        footer.style.display = "none";
    }

    // ---- 2. 再做文字自适应（此时面板高度已是最终值）----
    fitSVG();

    const char1 = document.getElementById("char1");
    if (char1 && char1.classList.contains("auto-text-vertical")) {
        fitText(char1, 8, 150, true);
    } else if (char1 && char1.classList.contains("grid-text-container")) {
        fitGridText();
    }

    fitText(document.getElementById("char2"), 8, 55, false);
    fitText(document.getElementById("char3"), 8, 55, false);
}
