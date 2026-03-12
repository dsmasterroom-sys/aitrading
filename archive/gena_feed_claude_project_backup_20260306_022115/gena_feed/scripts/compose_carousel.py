#!/usr/bin/env python3
"""Compose final carousel PNGs.

1) Render slide HTML(1080x1440) via Puppeteer
2) Composite generated images with Pillow
3) Save 9 final slide PNGs to output/slides/
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Tuple

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SLIDES_DIR = ROOT / "output" / "slides"
GENERATED_DIR = ROOT / "assets" / "output"
RENDER_DIR = SLIDES_DIR / ".rendered"

CANVAS_SIZE = (1080, 1440)


def log(msg: str) -> None:
    print(f"[compose_carousel] {msg}")


def check_required_assets() -> None:
    required = [ROOT / "assets" / "gena-base.png", ROOT / "assets" / "slant-product.png"]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("필수 에셋 누락: " + ", ".join(missing))


def ensure_puppeteer() -> None:
    cmd = ["node", "-e", "require('puppeteer'); console.log('ok')"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(
            "puppeteer 모듈을 찾을 수 없습니다.\n"
            "실행 예시: npm i puppeteer\n"
            f"stderr: {r.stderr.strip()}"
        )


def render_htmls() -> None:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    node_script = f"""
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {{
  const slidesDir = {json.dumps(str(SLIDES_DIR))};
  const renderDir = {json.dumps(str(RENDER_DIR))};
  const files = fs.readdirSync(slidesDir)
    .filter(f => /^slide-\\d{{2}}\\.html$/.test(f))
    .sort();

  const launchOptions = {{
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  }};
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (fs.existsSync(chromePath)) {{
    launchOptions.executablePath = chromePath;
  }}
  const browser = await puppeteer.launch(launchOptions);
  const page = await browser.newPage();
  await page.setViewport({{ width: 1080, height: 1440, deviceScaleFactor: 1 }});

  for (const file of files) {{
    const htmlPath = path.join(slidesDir, file);
    const url = 'file://' + htmlPath;
    await page.goto(url, {{ waitUntil: 'networkidle0' }});
    const outPng = path.join(renderDir, file.replace('.html', '.png'));
    await page.screenshot({{ path: outPng, type: 'png' }});
    console.log('rendered', file);
  }}

  await browser.close();
}})().catch((e) => {{
  console.error(e);
  process.exit(1);
}});
"""

    result = subprocess.run(["node", "-e", node_script], capture_output=True, text=True)
    if result.returncode == 0:
        if result.stdout.strip():
            log(result.stdout.strip())
        return

    log("Puppeteer 렌더 실패. 텍스트 기반 fallback 렌더로 전환합니다.")
    if result.stderr.strip():
        log(result.stderr.strip())
    render_htmls_fallback()


def _load_korean_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def _extract_text_lines(html: str) -> list[str]:
    # Keep only visible-ish text: remove style/script/comments/tags and trim blanks.
    cleaned = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    cleaned = re.sub(r"<style.*?>.*?</style>", "", cleaned, flags=re.S | re.I)
    cleaned = re.sub(r"<script.*?>.*?</script>", "", cleaned, flags=re.S | re.I)
    cleaned = re.sub(r"<br\\s*/?>", "\n", cleaned, flags=re.I)
    cleaned = re.sub(r"<[^>]+>", "\n", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    lines = [ln.strip() for ln in cleaned.splitlines() if ln.strip()]
    return lines


def render_htmls_fallback() -> None:
    files = sorted(SLIDES_DIR.glob("slide-*.html"))
    title_font = _load_korean_font(54)
    body_font = _load_korean_font(34)

    for html_path in files:
        lines = _extract_text_lines(html_path.read_text(encoding="utf-8"))
        canvas = Image.new("RGB", CANVAS_SIZE, "#F5F3EF")
        draw = ImageDraw.Draw(canvas)

        draw.rectangle([(0, 0), (CANVAS_SIZE[0], 110)], fill="#1A1A2E")
        draw.text((54, 28), f"{html_path.stem}", fill="#C8A96E", font=_load_korean_font(32))

        y = 160
        for idx, ln in enumerate(lines[:18]):
            font = title_font if idx < 3 else body_font
            draw.text((70, y), ln, fill="#1A1A2E", font=font)
            y += 72 if idx < 3 else 54
            if y > CANVAS_SIZE[1] - 120:
                break

        out_png = RENDER_DIR / f"{html_path.stem}.png"
        canvas.save(out_png, format="PNG")
        log(f"fallback rendered {html_path.name}")


def fit_cover(img: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
    tw, th = target_size
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def paste_with_opacity(base: Image.Image, overlay: Image.Image, box: Tuple[int, int, int, int], opacity: float = 1.0) -> None:
    x, y, w, h = box
    ov = fit_cover(overlay.convert("RGBA"), (w, h))
    if opacity < 1.0:
        alpha = ov.getchannel("A")
        alpha = alpha.point(lambda p: int(p * opacity))
        ov.putalpha(alpha)
    base.alpha_composite(ov, (x, y))


def compose_one(slide_num: int) -> None:
    name = f"slide-{slide_num:02d}"
    rendered = RENDER_DIR / f"{name}.png"
    if not rendered.exists():
        raise RuntimeError(f"렌더링 파일 없음: {rendered}")

    canvas = Image.open(rendered).convert("RGBA")

    # Generated image placement map (optional if files exist)
    overlays: Dict[str, Tuple[Tuple[int, int, int, int], float]] = {}

    if slide_num == 6:
        overlays["slide06-styleshot"] = ((0, 0, 648, 1380), 1.0)
    elif slide_num == 7:
        overlays["slide07-outfitswap"] = ((0, 0, 1080, 1440), 1.0)
    elif slide_num == 1:
        overlays["slide01-bg"] = ((0, 0, 1080, 1440), 0.18)
    elif slide_num == 2:
        overlays["slide02-bg"] = ((560, 520, 460, 760), 0.10)

    for key, (box, opacity) in overlays.items():
        img_path = GENERATED_DIR / f"{key}.png"
        if not img_path.exists():
            log(f"{name}: generated image 없음, 스킵 -> {img_path.name}")
            continue
        overlay = Image.open(img_path)
        paste_with_opacity(canvas, overlay, box, opacity)

    out = SLIDES_DIR / f"{name}.png"
    canvas.convert("RGB").save(out, format="PNG")
    log(f"완료: {out}")


def main() -> int:
    check_required_assets()
    ensure_puppeteer()

    if RENDER_DIR.exists():
        shutil.rmtree(RENDER_DIR)

    render_htmls()

    for i in range(1, 10):
        compose_one(i)

    log("총 9장 출력 완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
