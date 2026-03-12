---
name: build-html
agent: developer
description: "HTML·Nanogen API·PNG·MP4 제작 전담. 기획·카피·QA 금지."
input: "weekly/copy.md + weekly/design-brief.md + weekly/image-prompts.json + weekly/scene-plan.json"
output: "output/slides/ PNG · output/reels/ MP4 · output/story/ PNG"
---

# build-html SKILL

## 공통 환경 변수

```python
import os, requests, base64
from pathlib import Path

NANOGEN_BASE = os.getenv("NANOGEN_BASE_URL", "http://localhost:8000")
IMAGE_EP     = f"{NANOGEN_BASE}/api/generate-image"
VIDEO_EP     = f"{NANOGEN_BASE}/api/generate-video"
```

---

## TRACK 1: 캐러셀 HTML → PNG

### HTML 기본 구조

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  /* shared/design-tokens.css 인라인 삽입 */
  :root {
    --accent:#C8A96E; --dark:#1A1A2E; --bg:#F5F3EF;
    --text:#3D3D3D;   --white:#FFFFFF;
    --fs-title:64px;  --fs-body:36px; --fs-tag:28px;
    --pad:72px;       --radius:16px;
  }
  .canvas {
    width:1080px; height:1440px;
    overflow:hidden; position:relative;
    background:var(--bg); font-family:'Pretendard',sans-serif;
  }
  * { word-break:keep-all; box-sizing:border-box; }
  .bottom-bar {
    position:absolute; bottom:0; width:100%;
    height:60px; background:var(--dark);
    display:flex; align-items:center; padding:0 var(--pad);
    color:var(--accent); font-size:var(--fs-tag);
  }
</style>
</head>
<body>
  <div class="canvas">
    <!-- 슬라이드 콘텐츠 -->
    <div class="bottom-bar">@gena_feed</div>
  </div>
</body>
</html>
```

**원칙**: standalone HTML (CDN·외부 URL 금지) · 이미지 base64 인라인 · CSS 변수만 사용

### PNG 추출 (Puppeteer)

```javascript
const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1440 });
await page.goto(`file://${path.resolve(htmlFile)}`);
await page.screenshot({ path: pngFile, fullPage: false });
await browser.close();
```

### 캐러셀 완료 후 자산 복사

```python
import shutil
shutil.copy("output/slides/slide-01.png", "assets/thumb/slide-01.png")
# 오케스트레이터에 완료 보고
```

---

## TRACK 2: 릴스 — Nanogen API 파이프라인

### Step 1. 씬 이미지 생성

```python
def generate_scene_image(prompt: str) -> str:
    """Returns base64 string"""
    res = requests.post(IMAGE_EP, json={
        "prompt": prompt,
        "config": {"aspectRatio": "9:16", "resolution": "1080x1920"},
        "referenceImages": []
    }, timeout=120)
    res.raise_for_status()
    return res.json()["base64"]
```

### Step 2. Outfit Swap (S4·S6)

```python
def outfit_swap(gena_path: str, slant_path: str, prompt: str) -> str:
    """Returns base64 string"""
    gena_b64  = base64.b64encode(Path(gena_path).read_bytes()).decode()
    slant_b64 = base64.b64encode(Path(slant_path).read_bytes()).decode()
    res = requests.post(IMAGE_EP, json={
        "prompt": prompt,
        "config": {"mode": "composition"},
        "referenceImages": [gena_b64, slant_b64]
    }, timeout=180)
    res.raise_for_status()
    return res.json()["base64"]
```

### Step 3. 이미지 → 동영상 변환 (I2V)

```python
def generate_scene_video(img_b64: str, prompt: str,
                          camera: str, duration: int,
                          model: str = "kling-v3",
                          mode: str = "pro") -> str:
    """Returns .mp4 URL (Nanogen handles polling internally)"""
    res = requests.post(VIDEO_EP, json={
        "prompt": prompt,
        "config": {
            "modelId": model,
            "durationSeconds": duration,
            "klingMode": mode,
            "cameraMovement": camera
        },
        "referenceImages": [img_b64]
    }, timeout=300)   # Nanogen 폴링 포함 최대 3분
    res.raise_for_status()
    return res.json()["videoUrl"]
```

### Step 4. 씬별 실행 루프

```python
import json

scene_plan  = json.load(open("weekly/scene-plan.json"))
img_prompts = json.load(open("weekly/image-prompts.json"))
clip_urls   = {}

for scene in scene_plan["scenes"]:
    sid = scene["scene_id"]
    prompt_cfg = img_prompts[sid]

    if scene["outfit_swap"]:
        img_b64 = outfit_swap(
            "assets/gena-base.png",
            "assets/slant-product.png",
            prompt_cfg["image_prompt"]
        )
    else:
        img_b64 = generate_scene_image(prompt_cfg["image_prompt"])

    video_url = generate_scene_video(
        img_b64,
        prompt_cfg["video_prompt"],
        scene["camera_movement"],
        scene["duration_sec"],
        model=scene.get("model_override", "kling-v3"),
        mode=scene.get("mode_override", "pro")
    )
    clip_urls[sid] = video_url
    print(f"{sid} 완료: {video_url}")
```

### Step 5. ffmpeg 후처리

```bash
# 1. 클립 다운로드 및 이어붙이기
for s in S1 S2 S3 S4 S5 S6; do
  wget -O output/reels/${s}.mp4 "${CLIP_URL[$s]}"
done
ffmpeg -f concat -safe 0 -i clips.txt -c copy output/reels/merged.mp4

# 2. 자막 합성 (ASS 포맷)
ffmpeg -i output/reels/merged.mp4 \
       -vf "ass=weekly/captions.ass" \
       output/reels/with_captions.mp4

# 3. BGM 합성 (-15dB)
ffmpeg -i output/reels/with_captions.mp4 \
       -i assets/bgm.mp3 \
       -filter_complex "[1:a]volume=-15dB[bgm];[0:a][bgm]amix=inputs=2" \
       output/reels/final.mp4
```

릴스 완료 후 자산 복사:
```python
shutil.copy("output/reels/scene-05.png", "assets/reels/scene-05.png")
```

---

## TRACK 3: 스토리 PNG 합성

```python
from PIL import Image, ImageDraw, ImageFont

def make_story(bg_path: str, text: str, out_path: str):
    bg = Image.open(bg_path).resize((1080, 1920), Image.LANCZOS)
    # 반투명 다크 오버레이
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 120))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("assets/Pretendard-Bold.ttf", 64)
    draw.text((540, 300), text, fill="#FFFFFF", font=font, anchor="mt")
    bg.save(out_path)

make_story("assets/thumb/slide-01.png", "선크림 순서 맞게 바르고 있어요?",
           "output/story/story-d1.png")
make_story("assets/thumb/slide-01.png", "오늘 이거 올렸어요 →",
           "output/story/story-d0.png")
make_story("assets/reels/scene-05.png", "링크바이오에서 바로 볼 수 있어요 🔗",
           "output/story/story-d3.png")
```

---

## QA 이슈 수정 프로세스

1. qa-reviewer에서 이슈 수신 (`weekly/qa-report.md`)
2. 고·중 이슈 즉시 수정
3. 해당 산출물 재생성 (PNG 재추출 or MP4 재생성)
4. qa-reviewer에 재검증 요청
5. 고·중 이슈 0건 확인까지 반복

## 자기검증 체크리스트

- [ ] 캐러셀: 1080×1440px / overflow:hidden / CDN 없음 / word-break:keep-all
- [ ] 캐러셀: 하단 바 @gena_feed 존재 / 폰트 28px 미만 없음
- [ ] 릴스: Nanogen 서버 연결 확인 (localhost:8000 ping)
- [ ] 릴스: 6씬 MP4 전부 생성 / final.mp4 30초 이내
- [ ] 스토리: 1080×1920px / 텍스트 가독성
- [ ] 자산 복사: slide-01.png → assets/thumb/ / scene-05.png → assets/reels/
- [ ] 기획·카피·QA 작업 금지
