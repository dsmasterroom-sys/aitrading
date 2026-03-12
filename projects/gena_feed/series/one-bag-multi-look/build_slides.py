#!/usr/bin/env python3
"""
원백 멀티룩 캐러셀 — 8장 HTML 슬라이드 빌드 + PNG 추출.
이미지는 base64 인라인 삽입. 디자인 토큰은 CSS 변수로만 사용.
"""

import base64
import os
import subprocess

BASE_DIR = "/Users/master/.openclaw/workspace/projects/gena_feed"
SERIES_DIR = os.path.join(BASE_DIR, "series/one-bag-multi-look")
GEN_DIR = os.path.join(SERIES_DIR, "generated")
SLIDES_DIR = os.path.join(SERIES_DIR, "slides")
OUTPUT_DIR = os.path.join(BASE_DIR, "output/one-bag-multi-look")

os.makedirs(SLIDES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def img_to_b64(filename: str) -> str:
    path = os.path.join(GEN_DIR, filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# 디자인 토큰 (인라인 복사)
TOKENS = """
:root {
  --primary: #1A1A1A;
  --secondary: #6B6B6B;
  --accent: #D93025;
  --surface-dark: #1A1A1A;
  --surface-cream: #F2EDE8;
  --surface-cool: #E2DEDA;
  --surface-mid: #D0CBC6;
  --surface-accent: #D93025;
  --text-dark: #1A1A1A;
  --text-mid: #555555;
  --text-light: #F2EDE8;
  --fs-display: 72px;
  --fs-title: 56px;
  --fs-body: 36px;
  --fs-caption: 28px;
  --lh-display: 1.1;
  --lh-heading: 1.2;
  --lh-body: 1.6;
  --ls-heading: -0.02em;
  --ls-body: 0em;
  --pad: 80px;
  --gap: 40px;
  --gap-sm: 24px;
  --canvas-carousel-w: 1080px;
  --canvas-carousel-h: 1350px;
}
"""

BASE_STYLE = """
* { margin: 0; padding: 0; box-sizing: border-box; }
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
body { font-family: 'Noto Sans KR', sans-serif; }
.canvas {
  width: var(--canvas-carousel-w);
  height: var(--canvas-carousel-h);
  overflow: hidden;
  word-break: keep-all;
  position: relative;
}
.canvas img.bg {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}
.overlay {
  position: absolute; left: 0; right: 0;
  padding: var(--pad);
  z-index: 2;
}
.overlay-bottom {
  bottom: 0;
  background: linear-gradient(transparent, rgba(26,26,26,0.85) 40%);
  padding-top: 120px;
}
.overlay-top {
  top: 0;
  background: linear-gradient(rgba(26,26,26,0.7) 60%, transparent);
  padding-bottom: 120px;
}
.overlay-minimal {
  bottom: 0;
  background: linear-gradient(transparent, rgba(26,26,26,0.6) 50%);
  padding-top: 80px;
}
h1 {
  font-size: var(--fs-display);
  font-weight: 900;
  line-height: var(--lh-display);
  letter-spacing: var(--ls-heading);
}
h2 {
  font-size: var(--fs-title);
  font-weight: 700;
  line-height: var(--lh-heading);
  letter-spacing: var(--ls-heading);
}
p {
  font-size: var(--fs-body);
  font-weight: 400;
  line-height: var(--lh-body);
  letter-spacing: var(--ls-body);
  margin-top: var(--gap-sm);
}
.accent { color: var(--accent); }
.label {
  display: inline-block;
  font-size: var(--fs-caption);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 8px 20px;
  border: 2px solid currentColor;
  margin-bottom: var(--gap-sm);
}
"""


def wrap_html(body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
{TOKENS}
{BASE_STYLE}
</style>
</head>
<body>
{body}
</body>
</html>"""


# ============================================================
# 슬라이드 정의
# ============================================================

def slide_01():
    return wrap_html("""
<div class="canvas" style="background: var(--surface-dark); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: var(--pad);">
  <div style="margin-bottom: var(--gap);">
    <span class="label" style="color: var(--text-light);">ONE BAG, MULTI LOOK</span>
  </div>
  <h1 style="color: var(--text-light);">가방 하나로<br><span class="accent">3가지 룩,</span><br>가능할까?</h1>
  <p style="color: var(--secondary); margin-top: var(--gap);">@gena_feed</p>
</div>""")


def slide_02():
    b64 = img_to_b64("slide_02.png")
    return wrap_html(f"""
<div class="canvas">
  <img class="bg" src="data:image/png;base64,{b64}" />
  <div class="overlay overlay-bottom">
    <h2 style="color: var(--text-light);">아침마다 이 고민,<br>나만 하는 거 아니지?</h2>
    <p style="color: var(--surface-cream);">옷은 골랐는데 가방이 안 맞아서<br>다시 처음부터.</p>
  </div>
</div>""")


def slide_03():
    b64 = img_to_b64("slide_03.png")
    return wrap_html(f"""
<div class="canvas">
  <img class="bg" src="data:image/png;base64,{b64}" />
  <div class="overlay overlay-minimal">
    <h2 style="color: var(--text-light);">답은 <span class="accent">소재</span>에 있었어</h2>
    <p style="color: var(--surface-cream);">매트 나일론 하나면<br>캐쥬얼부터 스트릿까지 전부 커버.</p>
  </div>
</div>""")


def slide_04():
    b64 = img_to_b64("slide_04.png")
    return wrap_html(f"""
<div class="canvas">
  <img class="bg" src="data:image/png;base64,{b64}" />
  <div class="overlay overlay-bottom">
    <span class="label" style="color: var(--text-light);">LOOK 1</span>
    <h2 style="color: var(--text-light);">캐쥬얼</h2>
    <p style="color: var(--surface-cream);">가디건 + 와이드 데님에<br>크로스백으로 가볍게.</p>
  </div>
</div>""")


def slide_05():
    b64 = img_to_b64("slide_05.png")
    return wrap_html(f"""
<div class="canvas">
  <img class="bg" src="data:image/png;base64,{b64}" />
  <div class="overlay overlay-bottom">
    <span class="label" style="color: var(--text-light);">LOOK 2</span>
    <h2 style="color: var(--text-light);">미니멀</h2>
    <p style="color: var(--surface-cream);">블레이저 + 슬랙스에<br>숄더백으로 깔끔하게.</p>
  </div>
</div>""")


def slide_06():
    b64 = img_to_b64("slide_06.png")
    return wrap_html(f"""
<div class="canvas">
  <img class="bg" src="data:image/png;base64,{b64}" />
  <div class="overlay overlay-minimal" style="padding: var(--pad); padding-top: 60px;">
    <span class="label" style="color: var(--text-light);">LOOK 3</span>
    <h2 style="color: var(--text-light);">스트릿</h2>
    <p style="color: var(--surface-cream);">레더 재킷 + 스커트에<br>힙색으로 포인트.</p>
  </div>
</div>""")


def slide_07():
    b64 = img_to_b64("slide_07.png")
    return wrap_html(f"""
<div class="canvas">
  <img class="bg" src="data:image/png;base64,{b64}" />
  <div class="overlay overlay-bottom">
    <h2 style="color: var(--text-light);">왜 이 가방이냐면</h2>
    <p style="color: var(--surface-cream);">매트 나일론 · YKK 지퍼 · 조절 버클 스트랩<br><strong style="color: var(--text-light);">작지만 다 들어가.</strong></p>
  </div>
</div>""")


def slide_08():
    return wrap_html("""
<div class="canvas" style="background: var(--surface-dark); display: flex; flex-direction: column; justify-content: center; padding: var(--pad);">
  <h2 style="color: var(--text-light); margin-bottom: var(--gap);">저장해두고<br>내일 바로 써먹어</h2>
  <p style="color: var(--surface-cream);">@gena_feed 팔로우하면<br>다음 주 <strong style="color: var(--accent);">원백 멀티룩 릴스</strong>도 볼 수 있어.</p>
  <div style="margin-top: 80px; display: flex; gap: var(--gap-sm); flex-wrap: wrap;">
    <span style="color: var(--secondary); font-size: var(--fs-caption); border: 1px solid var(--secondary); padding: 10px 24px; border-radius: 100px;">저장하기</span>
    <span style="color: var(--secondary); font-size: var(--fs-caption); border: 1px solid var(--secondary); padding: 10px 24px; border-radius: 100px;">팔로우</span>
    <span style="color: var(--secondary); font-size: var(--fs-caption); border: 1px solid var(--secondary); padding: 10px 24px; border-radius: 100px;">다음 편 보기</span>
  </div>
  <p style="color: var(--secondary); margin-top: auto; font-size: var(--fs-caption);">@gena_feed</p>
</div>""")


def main():
    builders = [
        ("slide_01.html", slide_01),
        ("slide_02.html", slide_02),
        ("slide_03.html", slide_03),
        ("slide_04.html", slide_04),
        ("slide_05.html", slide_05),
        ("slide_06.html", slide_06),
        ("slide_07.html", slide_07),
        ("slide_08.html", slide_08),
    ]

    for filename, builder in builders:
        print(f"빌드 중: {filename}")
        html = builder()
        path = os.path.join(SLIDES_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        size_kb = os.path.getsize(path) / 1024
        print(f"  → {path} ({size_kb:.0f}KB)")

    print(f"\nHTML 빌드 완료: {len(builders)}장")

    # PNG 추출
    print("\nPNG 추출 중...")
    for filename, _ in builders:
        html_path = os.path.join(SLIDES_DIR, filename)
        png_name = filename.replace(".html", ".png")
        png_path = os.path.join(OUTPUT_DIR, png_name)

        try:
            result = subprocess.run(
                ["npx", "puppeteer", "screenshot", html_path,
                 "--width", "1080", "--height", "1350",
                 "--output", png_path],
                capture_output=True, text=True, timeout=30,
                cwd=BASE_DIR,
            )
            if os.path.exists(png_path):
                print(f"  [OK] {png_path} ({os.path.getsize(png_path)/1024:.0f}KB)")
            else:
                # puppeteer CLI가 없으면 다른 방법 시도
                print(f"  [SKIP] puppeteer CLI 미설치 — HTML만 생성됨")
                break
        except FileNotFoundError:
            print(f"  [SKIP] npx/puppeteer 미설치 — HTML만 생성됨")
            break
        except subprocess.TimeoutExpired:
            print(f"  [TIMEOUT] {png_name}")

    print("\n완료!")


if __name__ == "__main__":
    main()
