#!/usr/bin/env python3
"""
one-bag-multi-look 시리즈 이미지 v3.

변경점 (v2 → v3):
- 6섹션 구조 프롬프트 적용 (마스터 템플릿 기반)
- 레퍼런스 순서: 페르소나 먼저 → 제품 뒤에
- identity swap 제거 — base 이미지를 최종본으로 사용
- slide_03 추가: 나일론 소재 매크로 클로즈업
"""

import base64
import os
import sys
import requests

BASE_DIR = "/Users/master/.openclaw/workspace/projects/gena_feed"
OUTPUT_DIR = os.path.join(BASE_DIR, "series/one-bag-multi-look/generated")

PERSONA_PATHS = {
    "gena_straight": os.path.join(BASE_DIR, "shared/persona/gena_ref_03_basic_straight.png"),
    "gena_braid": os.path.join(BASE_DIR, "shared/persona/gena_ref_08_double_down_braid.png"),
    "gena_hippie": os.path.join(BASE_DIR, "shared/persona/gena_ref_09_long_hippie.png"),
}

PRODUCT_DIR = os.path.join(BASE_DIR, "shared/products/genarchive_crossbag")
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def get_product_images() -> list[str]:
    """제품 폴더 내 모든 이미지 경로를 반환"""
    paths = []
    for f in sorted(os.listdir(PRODUCT_DIR)):
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
            paths.append(os.path.join(PRODUCT_DIR, f))
    return paths

API_URL = "http://localhost:8000/api/generate"
TIMEOUT = 600
DEFAULT_CONFIG = {"aspectRatio": "4:5", "resolution": "1080x1350"}


def load_b64(path: str) -> str:
    """이미지를 data URI 형식으로 반환 (data:image/png;base64,...)"""
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def call_api(prompt: str, config: dict, ref_images_b64: list[str]) -> bytes:
    payload = {
        "prompt": prompt,
        "config": config,
        "referenceImages": ref_images_b64,
    }
    resp = requests.post(API_URL, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()["url"]
    prefix = "data:image/png;base64,"
    if data.startswith(prefix):
        data = data[len(prefix):]
    return base64.b64decode(data)


def generate_slide(name: str, filename: str, prompt: str,
                    persona_key: str | None = None, use_product: bool = False):
    """persona 먼저, product 전체 뒤에 — 순서 보장"""
    print(f"\n{'='*60}")
    print(f"생성 중: {filename} ({name})")

    refs = []

    # 1) 페르소나 (항상 첫 번째)
    if persona_key:
        path = PERSONA_PATHS[persona_key]
        print(f"  페르소나: {os.path.basename(path)} ({os.path.getsize(path) / 1024 / 1024:.1f}MB)")
        refs.append(load_b64(path))

    # 2) 제품 폴더 내 모든 이미지
    if use_product:
        for path in get_product_images():
            print(f"  제품: {os.path.basename(path)} ({os.path.getsize(path) / 1024 / 1024:.1f}MB)")
            refs.append(load_b64(path))

    print(f"  총 레퍼런스: {len(refs)}장")

    print("  API 호출 중...")
    try:
        img_bytes = call_api(prompt, DEFAULT_CONFIG, refs)
    except requests.exceptions.Timeout:
        print(f"  [ERROR] API 응답 타임아웃 ({TIMEOUT}초)")
        return False
    except requests.exceptions.ConnectionError:
        print("  [ERROR] 서버 연결 실패")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False

    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    print(f"  저장 완료: {output_path} ({os.path.getsize(output_path) / 1024:.1f}KB)")
    return True


# ============================================================
# 6섹션 프롬프트 정의
# ============================================================

SLIDE_02_PROMPT = """[INDICATIONS] A Korean Beautiful real influencer @model who looks exactly like a real person in the image. With straight black hair loosely tied. Wearing an oversized grey cotton t-shirt and black leggings — a relaxed morning home outfit. She stands in front of a full-length mirror in her bedroom, 5-6 different stylish bags scattered on the white bed behind her: a leather tote, a canvas crossbody, a quilted shoulder bag, a small clutch, and a nylon backpack. She's contemplating which bag to carry today. The atmosphere is intimate and relatable, a real morning routine moment. No overlay, no text, no logo.
[STYLE] Clean but well-crafted UGC look. Warm, natural light from a large window, with an aesthetic close to a high-quality smartphone photo. Simple framing, friendly and spontaneous energy. The mood is genuine and human — a candid morning-routine moment. @model looks at her reflection with a slightly indecisive expression, one hand reaching toward the bags on the bed.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field with soft bokeh on the bags. Sharpness focused on @model's face in the mirror reflection and the variety of bags on the bed.
[LIGHTING: SOFT NATURAL DAYLIGHT] Soft morning light from a large bedroom window. Overcast sky providing diffused, even illumination. Cool cinematic grading (5500K) creating a clean, calm atmosphere. No harsh shadows. Gentle wrap-around light.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light. No harsh shadows. Natural and realistic appearance. Cool temperature: slightly cooler white balance (5500K). Skin tones clean and neutral. Low contrast, soft three-dimensional look. Environmental colors slightly desaturated. Dominant tones: Warm white bedding, soft grey t-shirt, assorted bag colors as visual variety, wooden floor warmth.
[SCENE & ACTION] A bright, minimalist bedroom with white walls and a wooden floor. A full-length mirror with a thin black frame stands against the wall. @model stands barefoot in front of the mirror, looking at her reflection. On the white bed behind her, 5-6 bags of different styles and colors are laid out. She tilts her head slightly, one hand on her hip, the other reaching toward a black crossbody bag. The scene captures the universal moment of choosing the right bag before heading out."""

SLIDE_03_PROMPT = """[INDICATIONS] Extreme macro close-up of matte black ballistic nylon fabric from a mini crossbag. Visible tight weave pattern showing individual nylon fibers crossing over each other. A metal YKK zipper partially open, with teeth in sharp focus. The adjustable black buckle hardware of the strap enters the frame from the edge. No person, no full bag — only material and hardware details filling the entire frame. No overlay, no text, no logo.
[STYLE] Studio product photography. Clean, controlled environment. The aesthetic is tactile and editorial — the viewer should feel the texture. Minimal composition with the fabric weave as the hero element.
[CAMERA SETTINGS] Kodak Ektar 100 emulation, 90mm macro equivalent, f/4.0, 1/60s, ISO 100. Extremely shallow depth of field. Razor-sharp focus on the nylon weave at center, with zipper teeth softly falling off into bokeh. Light film grain, high clarity.
[LIGHTING: CONTROLLED STUDIO] Soft overhead studio light, 6000K daylight balanced. Even diffusion from a large softbox positioned slightly above and to the left. Subtle specular highlight on the metal zipper teeth. No harsh shadows. Clean, clinical illumination that reveals every fiber of the nylon weave.
[KEY TECHNICAL CHARACTERISTICS] High clarity, controlled contrast. No color cast. Neutral temperature (6000K). Fabric texture rendered with extreme detail — individual fibers visible. Metal hardware shows subtle reflective highlights without blowout. Background is the fabric itself, no separate backdrop. Dominant tones: Matte black nylon, gunmetal zipper, dark charcoal buckle.
[SCENE & ACTION] The camera is positioned inches away from the surface of a matte black nylon mini crossbag. The frame is filled entirely with the ballistic nylon weave — a tight, grid-like pattern of thick nylon threads. In the upper-right portion, a metal zipper with silver teeth catches a subtle glint of light. The lower-left shows the edge of a plastic buckle where the adjustable strap connects. A single finger gently presses into the nylon surface, creating a slight depression that reveals the fabric's density and resistance."""

SLIDE_04_PROMPT = """[INDICATIONS] A Korean Beautiful real influencer @model who looks exactly like a real person in the image. With straight black hair, slightly wind-blown. Wearing a trendy gorpcore outfit: charcoal windbreaker layered over a mocha mousse warm brown hoodie, black cargo pants, and black trail shoes. A matte black nylon mini crossbag worn diagonally across the torso — the rectangular silhouette sits at hip level. The atmosphere should feel like UGC content: spontaneous, natural, and intimate. @model is walking confidently through an urban setting. The silhouette and texture of the crossbag become part of the visual identity. Details like real skin texture, natural hair movement, micro-imperfections, and natural light reflections on the bag's nylon material are emphasized. No overlay, no text, no logo.
[STYLE] Clean but well-crafted UGC look. Cool, desaturated urban tones with soft reflections on the surface of the nylon crossbag. Aesthetic close to a high-quality smartphone video. Simple framing, friendly and spontaneous energy. The mood is genuine and human — @model taking in the surroundings with a relaxed, confident expression. Subtle handheld camera energy.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field, natural and soft bokeh on the background. Sharpness focused on the crossbag strap and buckle detail, and @model's face. Light film texture, warm and realistic colors.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light from an overcast day, enhanced with cool cinematic grading creating a clean, elegant urban atmosphere. Low-key, soft, with cool neutral tones and controlled contrast. Strongly highlights the gorpcore outfit layers and the matte black crossbag. 5500-6500K color temperature.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light. No harsh shadows. No glare. Natural and realistic appearance. Cool temperature (5500K-6500K, grading leaning bluish). Skin tones cleaner and more neutral, without yellow hues. Low-to-medium contrast: soft, three-dimensional look. Environmental colors desaturated by -15%. Dominant tones: Concrete grey, mocha mousse brown, charcoal, matte black nylon.
[SCENE & ACTION] A clean concrete sidewalk alongside a minimalist grey building wall in Seongsu-dong. @model walks toward the camera with a confident, relaxed stride. Her charcoal windbreaker is unzipped, revealing the mocha mousse hoodie underneath. The black crossbag bounces slightly against her hip as she moves. She glances slightly to the side with a natural half-smile, one hand in her cargo pants pocket. The wind catches her straight black hair gently."""

SLIDE_05_PROMPT = """[INDICATIONS] A Korean Beautiful real influencer @model who looks exactly like a real person in the image. With double braids (two braids down each side). Wearing a clean techwear outfit: black shell jacket over a deep lavender future dusk crop zip-up, grey wide jogger pants, and black chunky sneakers. A matte black nylon mini bag worn as a shoulder bag on one shoulder with a short strap — the rectangular form rests under the arm. The atmosphere should feel like UGC content: spontaneous, natural, and intimate. The silhouette and texture of the shoulder bag become part of the visual identity. Details like real skin texture, natural braided hair texture, and light reflections on the bag's nylon surface are emphasized. No overlay, no text, no logo.
[STYLE] Clean but well-crafted UGC look. Cool, desaturated urban tones. Aesthetic close to a high-quality smartphone video. The mood is genuine and human — @model pauses mid-walk, looking slightly spaced-out, lost in thought. Subtle handheld camera energy creating an authentic atmosphere.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field with the concrete pillars falling into soft bokeh. Sharpness focused on the shoulder bag form and @model's face. Light film texture with cool, realistic tones.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light filtering into a parking structure from open sides. Overcast sky providing soft, diffused illumination. Cool cinematic grading (6000K) emphasizing concrete greys and the lavender accent of the zip-up. No harsh shadows. Ambient bounce light from concrete surfaces.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light. No harsh shadows. Cool temperature (6000K, grading leaning bluish). Skin tones clean and neutral. Low-to-medium contrast: soft, three-dimensional look. Environmental colors desaturated by -15%. The deep lavender zip-up provides the only color accent against the monochrome palette. Dominant tones: Concrete grey, matte black, deep lavender accent, cool neutral skin.
[SCENE & ACTION] An empty parking structure with clean concrete pillars and geometric lines. Diffused daylight enters from the open sides. @model stands in a contrapposto pose between two pillars, one hand adjusting the shoulder bag strap. Her double braids fall over the front of her black shell jacket. She looks off to the side with a contemplative, slightly dreamy expression. The deep lavender zip-up peeks out from under the open jacket, providing a subtle pop of color against the grey concrete environment."""

SLIDE_06_PROMPT = """[INDICATIONS] A Korean Beautiful real influencer @model who looks exactly like a real person in the image. With long hippie-style wavy hair flowing past the shoulders. Wearing a street layered outfit: black oversized hoodie with an aqua glaze mint blue mesh vest layered on top, black jogger pants, and black trail shoes. A matte black nylon mini bag worn as a waist bag (fanny pack style) at the front hip — the rectangular form sits flat against the body. The atmosphere should feel like UGC content: spontaneous, natural, and intimate. The texture of the mesh vest and the nylon waist bag create visual interest. No overlay, no text, no logo.
[STYLE] Clean but well-crafted UGC look. Cool, desaturated urban tones with the aqua mint vest as a color accent. Aesthetic close to a high-quality smartphone video. Friendly and spontaneous energy. @model leans against a wall with relaxed confidence, naturally adjusting the waist bag. Subtle handheld camera energy.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field, natural bokeh on the stairway behind. Sharpness focused on the waist bag and the mesh vest texture, and @model's face. Light film texture, cool realistic tones.
[LIGHTING: SOFT NATURAL DAYLIGHT] Ambient light in a semi-covered urban stairway. Overcast sky providing soft, diffused light from above. Cool cinematic grading (5500K) emphasizing the cool desaturated atmosphere. No harsh shadows. Soft ambient bounce from concrete surfaces.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light. No harsh shadows. Cool temperature (5500K, desaturated grading). Skin tones clean and neutral without warmth. Low-to-medium contrast: soft, three-dimensional look. Environmental colors desaturated by -15%. The aqua glaze mint blue mesh vest provides the primary color accent. Dominant tones: Matte black, urban concrete grey, aqua mint accent, cool neutral skin.
[SCENE & ACTION] A minimalist urban stairway with clean concrete walls and metal handrails in Mangwon-dong. @model leans against the concrete wall at a slight angle, one foot resting on a lower step. Her long hippie-style wavy hair drapes over the aqua mint mesh vest. She looks directly at the camera with a relaxed, slightly playful expression, one hand resting on the waist bag at her hip. The layered outfit creates visual depth — the black hoodie base, the semi-transparent mint mesh vest, and the compact black waist bag at center."""

SLIDE_07_PROMPT = """[INDICATIONS] A matte black nylon mini crossbag — product hero shot. The bag is the sole subject, displayed at a slight three-quarter angle to show both the front face and the side depth. Visible details: tight ballistic nylon weave texture, metal YKK zipper with a minimal pull tab, adjustable black buckle strap, compact rectangular form. The strap is artfully draped to one side. No person, no hand. No overlay, no text, no logo.
[STYLE] Editorial product photography. Clean, minimal composition. The bag sits on a subtle matte surface (light grey concrete or pale stone). Negative space surrounds the product, giving it room to breathe. The aesthetic is high-end e-commerce meets fashion editorial.
[CAMERA SETTINGS] Kodak Ektar 100 emulation, 85mm equivalent, f/4.0, 1/60s, ISO 100. Shallow depth of field — front buckle sharp, rear strap softly out of focus. High clarity, minimal grain. Color accuracy prioritized.
[LIGHTING: CONTROLLED STUDIO] Soft overhead key light from a large softbox (6000K daylight balanced). Fill card on the opposite side to gently open the shadows. Subtle rim light from behind to separate the bag from the background. Even, controlled illumination revealing nylon weave texture without hotspots.
[KEY TECHNICAL CHARACTERISTICS] Medium contrast — enough to show the three-dimensional form of the bag without crushing blacks. No color cast. Neutral temperature (6000K). Nylon texture rendered with high detail — weave pattern visible. Metal hardware shows controlled specular highlights. Dominant tones: Matte black nylon, gunmetal zipper, soft grey background surface.
[SCENE & ACTION] The matte black nylon mini crossbag sits centered on a light grey matte concrete surface. The bag is positioned at a slight angle, front zipper facing the camera. The adjustable strap extends to the right, its black buckle catching a subtle glint of light. The tight nylon weave texture is clearly visible across the front panel. Behind the bag, the background fades to a clean, soft gradient of light grey. The composition is minimal and confident — the product speaks for itself."""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for key, path in PERSONA_PATHS.items():
        if not os.path.exists(path):
            print(f"[ERROR] 페르소나 이미지 없음: {path}")
            sys.exit(1)
        print(f"  [OK] {key}: {os.path.getsize(path)/1024/1024:.1f}MB")

    product_imgs = get_product_images()
    print(f"\n  제품 이미지 ({len(product_imgs)}장):")
    for p in product_imgs:
        print(f"  [OK] {os.path.basename(p)}: {os.path.getsize(p)/1024/1024:.1f}MB")

    # 페르소나 먼저, 제품 폴더 전체 자동 참조
    slides = [
        {"name": "공감 — 거울 앞 고민", "filename": "slide_02.png",
         "prompt": SLIDE_02_PROMPT, "persona_key": "gena_straight", "use_product": False},
        {"name": "소재 — 나일론 매크로", "filename": "slide_03.png",
         "prompt": SLIDE_03_PROMPT, "persona_key": None, "use_product": True},
        {"name": "LOOK 1 크로스백 고프코어", "filename": "slide_04.png",
         "prompt": SLIDE_04_PROMPT, "persona_key": "gena_straight", "use_product": True},
        {"name": "LOOK 2 숄더백 테크웨어", "filename": "slide_05.png",
         "prompt": SLIDE_05_PROMPT, "persona_key": "gena_braid", "use_product": True},
        {"name": "LOOK 3 힙색 스트릿", "filename": "slide_06.png",
         "prompt": SLIDE_06_PROMPT, "persona_key": "gena_hippie", "use_product": True},
        {"name": "제품 클로즈업", "filename": "slide_07.png",
         "prompt": SLIDE_07_PROMPT, "persona_key": None, "use_product": True},
    ]

    results = []
    for slide in slides:
        ok = generate_slide(
            name=slide["name"],
            filename=slide["filename"],
            prompt=slide["prompt"],
            persona_key=slide["persona_key"],
            use_product=slide["use_product"],
        )
        results.append((slide["filename"], ok))

    # 최종 결과
    print(f"\n{'='*60}")
    print("최종 결과:")
    print(f"{'='*60}")
    for filename, success in results:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if success and os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  [OK] {filepath} ({size / 1024:.1f}KB)")
        else:
            print(f"  [FAIL] {filename}")

    success_count = sum(1 for _, s in results if s)
    print(f"\n성공: {success_count}/{len(slides)}")
    if success_count < len(slides):
        sys.exit(1)


if __name__ == "__main__":
    main()
