#!/usr/bin/env python3
"""
one-bag-multi-look 3단계 파이프라인:
  Phase 1: flat-lay 의상 이미지 생성 (3 looks)
  Phase 2: composition — 젠아 + 의상 합성 (3 looks)
  Phase 3: 최종 슬라이드 이미지 생성 (6 slides)
"""

import base64
import os
import sys
import requests

BASE_DIR = "/Users/master/.openclaw/workspace/projects/gena_feed"
OUTPUT_DIR = os.path.join(BASE_DIR, "series/one-bag-multi-look/generated")
OUTFIT_DIR = os.path.join(OUTPUT_DIR, "outfits")
COMP_DIR = os.path.join(OUTPUT_DIR, "compositions")

PERSONA_PATHS = {
    "gena_straight": os.path.join(BASE_DIR, "shared/persona/gena_ref_03_basic_straight.png"),
    "gena_medium": os.path.join(BASE_DIR, "shared/persona/gena_ref_02_medium_straight.png"),
    "gena_braid": os.path.join(BASE_DIR, "shared/persona/gena_ref_08_double_down_braid.png"),
    "gena_hippie": os.path.join(BASE_DIR, "shared/persona/gena_ref_09_long_hippie.png"),
}

PRODUCT_DIR = os.path.join(BASE_DIR, "shared/products/genarchive_crossbag")
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

API_URL = "http://localhost:8000/api/generate"
TIMEOUT = 600
DEFAULT_CONFIG = {"aspectRatio": "4:5", "resolution": "1080x1350"}


def load_b64(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp"}.get(ext, "image/png")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def bytes_to_data_uri(data: bytes) -> str:
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"


def get_product_images() -> list[str]:
    paths = []
    for f in sorted(os.listdir(PRODUCT_DIR)):
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
            paths.append(os.path.join(PRODUCT_DIR, f))
    return paths


def call_api(prompt: str, config: dict, ref_b64: list[str]) -> bytes:
    payload = {"prompt": prompt, "config": config, "referenceImages": ref_b64}
    resp = requests.post(API_URL, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()["url"]
    prefix = "data:image/png;base64,"
    if data.startswith(prefix):
        data = data[len(prefix):]
    return base64.b64decode(data)


def save(data: bytes, path: str) -> str:
    with open(path, "wb") as f:
        f.write(data)
    print(f"  → 저장: {path} ({os.path.getsize(path)/1024:.0f}KB)")
    return path


# ============================================================
# PHASE 1: Flat-lay 의상 이미지 생성
# ============================================================

OUTFIT_PROMPTS = {
    "look1_casual": """[INDICATIONS] A flat-lay outfit arrangement on a clean white wooden floor. Items neatly laid out from top to bottom: a cream-colored oversized cable-knit cardigan with natural buttons, a plain white crewneck cotton t-shirt folded underneath, light blue washed wide-leg denim jeans, and white minimal leather sneakers placed at the bottom. All items are arranged with intentional spacing, as if styled for an Instagram flat-lay post.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Minimal, organized, aesthetically pleasing arrangement. Each item clearly visible and distinct.
[CAMERA SETTINGS] Kodak Ektar 100 emulation, 50mm equivalent, f/5.6, 1/125s, ISO 100. Even sharpness across entire frame. No depth of field blur — everything in focus.
[LIGHTING] Soft, even studio overhead light, 5500K daylight balanced. Large diffused softbox directly above. No harsh shadows. Clean, bright illumination that accurately renders fabric colors and textures.
[KEY TECHNICAL CHARACTERISTICS] High clarity, neutral color rendering. Cream cardigan warm but not yellow. White tee pure white. Denim shows authentic wash texture. Dominant tones: Cream, white, light blue denim, white leather.
[SCENE & ACTION] A perfectly arranged flat-lay on a white wooden surface. The cream cardigan is spread open at the top, the white tee peeks out from underneath. Below, the wide-leg jeans are folded once at the waist, legs extending downward. White sneakers are placed neatly at the bottom corners. Small negative space between each item. No accessories, no person, no bag — only clothing and shoes.""",

    "look2_minimal": """[INDICATIONS] A flat-lay outfit arrangement on a clean light grey concrete surface. Items neatly laid out: a black oversized structured blazer with subtle shoulder structure, a crisp white cotton button-down shirt folded underneath, black high-waisted wide-leg tailored trousers, and black pointed-toe loafers placed at the bottom. All items are arranged with intentional spacing for an editorial flat-lay.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Monochrome minimal aesthetic. Sharp, precise arrangement with geometric alignment.
[CAMERA SETTINGS] Fuji Pro 400H emulation, 50mm equivalent, f/5.6, 1/125s, ISO 100. Even sharpness across frame. Cool tone rendering.
[LIGHTING] Soft, even studio overhead light, 6000K slightly cool daylight. Large diffused softbox. No shadows. Clean, clinical illumination emphasizing the contrast between black and white garments.
[KEY TECHNICAL CHARACTERISTICS] Medium-high contrast between black and white items. Black fabric shows subtle texture without crushing to pure black. White shirt is clean and bright. Tailored lines and structure clearly visible. Dominant tones: Black, white, light grey concrete surface.
[SCENE & ACTION] A minimalist flat-lay on a light grey concrete surface. The black blazer is spread open at the top, revealing the white button-down shirt beneath. The black wide-leg trousers are folded at the waist below. Black loafers placed at the bottom, toes pointing outward. Precise geometric spacing between all items. No accessories, no person, no bag — only clothing and shoes.""",

    "look3_street": """[INDICATIONS] A flat-lay outfit arrangement on a dark charcoal surface. Items laid out with intentional creative overlap: a black oversized hoodie as the base layer, a sage green mesh utility vest layered on top of it, black wide-leg cargo jogger pants with visible utility pockets and drawstring hem, and black chunky trail sneakers at the bottom. The layering of hoodie and mesh vest shows both items clearly.
[STYLE] Clean editorial flat-lay photography with slight creative styling. Overhead bird's-eye view. Streetwear energy — items slightly more dynamic in arrangement than traditional flat-lay, with the mesh vest draped naturally over the hoodie.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 50mm equivalent, f/5.6, 1/125s, ISO 200. Even sharpness. Slight warm tone in the sage green rendering.
[LIGHTING] Soft studio overhead light, 5500K daylight balanced. Diffused softbox. Minimal shadows. Clean illumination that shows the mesh texture transparency and hoodie fabric weight.
[KEY TECHNICAL CHARACTERISTICS] Low-medium contrast. The sage green mesh vest is semi-transparent, showing the black hoodie underneath. Cargo jogger pockets and drawstring details clearly visible. Dominant tones: Black, sage green, dark charcoal surface.
[SCENE & ACTION] A streetwear flat-lay on a dark charcoal surface. The black oversized hoodie is spread flat as the foundation. The sage green mesh utility vest is draped on top, its semi-transparent weave revealing the hoodie underneath. Below, black cargo joggers are arranged with pockets visible. Black chunky trail sneakers at the bottom. The arrangement has slight creative energy — not perfectly geometric, but intentionally styled with streetwear attitude. No accessories, no person, no bag — only clothing and shoes.""",
}


# ============================================================
# PHASE 2: Composition — 젠아 + 의상 합성
# ============================================================

COMPOSITION_PROMPT = (
    "Change only the main clothing garments to strictly match the design, texture, "
    "and details of the provided clothing reference image. Replicate the attached "
    "outfit exactly. Crucially, preserve all original accessories intact (including "
    "bags, earrings, rings, jewelry, eyewear, etc.). Keep the original model's face, "
    "pose, hair, background, and lighting exactly the same. Seamless integration, "
    "photorealistic, 8k resolution."
)


# ============================================================
# PHASE 3: 최종 슬라이드 프롬프트
# ============================================================

SLIDE_02_PROMPT = """[INDICATIONS] A Korean Beautiful real influencer @model who looks exactly like a real person in the image. With straight black hair loosely tied. Wearing an oversized grey cotton t-shirt and black leggings — a relaxed morning home outfit. She stands in front of a full-length mirror in her bedroom, 5-6 different stylish bags scattered on the white bed behind her: a leather tote, a canvas crossbody, a quilted shoulder bag, a small clutch, and a nylon backpack. She's contemplating which bag to carry today. The atmosphere is intimate and relatable, a real morning routine moment. No overlay, no text, no logo.
[STYLE] Clean but well-crafted UGC look. Warm, natural light from a large window, with an aesthetic close to a high-quality smartphone photo. Simple framing, friendly and spontaneous energy. The mood is genuine and human — a candid morning-routine moment. @model looks at her reflection with a slightly indecisive expression, one hand reaching toward the bags on the bed.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field with soft bokeh on the bags. Sharpness focused on @model's face in the mirror reflection and the variety of bags on the bed.
[LIGHTING: SOFT NATURAL DAYLIGHT] Soft morning light from a large bedroom window. Overcast sky providing diffused, even illumination. Cool cinematic grading (5500K) creating a clean, calm atmosphere. No harsh shadows. Gentle wrap-around light.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light. No harsh shadows. Natural and realistic appearance. Cool temperature: slightly cooler white balance (5500K). Skin tones clean and neutral. Low contrast, soft three-dimensional look. Environmental colors slightly desaturated. Dominant tones: Warm white bedding, soft grey t-shirt, assorted bag colors as visual variety, wooden floor warmth.
[SCENE & ACTION] A bright, minimalist bedroom with white walls and a wooden floor. A full-length mirror with a thin black frame stands against the wall. @model stands barefoot in front of the mirror, looking at her reflection. On the white bed behind her, 5-6 bags of different styles and colors are laid out. She tilts her head slightly, one hand on her hip, the other reaching toward a black crossbody bag. The scene captures the universal moment of choosing the right bag before heading out."""

SLIDE_03_PROMPT = """[INDICATIONS] Extreme macro close-up of matte black ballistic nylon fabric from a mini crossbag. Visible tight weave pattern showing individual nylon fibers crossing over each other. A metal YKK zipper partially open, with teeth in sharp focus. The adjustable black buckle hardware of the strap enters the frame from the edge. No person, no full bag — only material and hardware details filling the entire frame. No overlay, no text, no logo.
[STYLE] Studio product photography. Clean, controlled environment. The aesthetic is tactile and editorial — the viewer should feel the texture. Minimal composition with the fabric weave as the hero element.
[CAMERA SETTINGS] Kodak Ektar 100 emulation, 90mm macro equivalent, f/4.0, 1/60s, ISO 100. Extremely shallow depth of field. Razor-sharp focus on the nylon weave at center, with zipper teeth softly falling off into bokeh.
[LIGHTING: CONTROLLED STUDIO] Soft overhead studio light, 6000K daylight balanced. Even diffusion from a large softbox. Subtle specular highlight on metal zipper teeth. No harsh shadows.
[KEY TECHNICAL CHARACTERISTICS] High clarity, controlled contrast. Neutral temperature (6000K). Fabric texture rendered with extreme detail. Metal hardware shows subtle reflective highlights. Dominant tones: Matte black nylon, gunmetal zipper, dark charcoal buckle.
[SCENE & ACTION] The camera is positioned inches away from the surface of a matte black nylon mini crossbag. The frame is filled with the ballistic nylon weave. In the upper-right, a metal zipper with silver teeth catches a glint of light. The lower-left shows a plastic buckle where the strap connects. A single finger gently presses into the nylon surface, revealing the fabric's density."""

SLIDE_LOOK_TEMPLATE = """[INDICATIONS] A Korean Beautiful real influencer @model who looks exactly like a real person in the image. Wearing {outfit_desc}, and a matte black nylon mini crossbag — {bag_wear_style}. The atmosphere should feel like UGC content: spontaneous, natural, and intimate. @model is {action} in an everyday urban setting. The silhouette and texture of the crossbag become part of the visual identity. Details like real skin texture, natural hair, micro-imperfections, and natural light reflections on the bag's nylon material are emphasized. No overlay, no text, no logo.
[STYLE] Clean but well-crafted UGC look. {style_tone} Aesthetic close to a high-quality smartphone video. Simple framing, friendly and spontaneous energy. The mood is genuine and human. Subtle handheld camera energy.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field, natural and soft bokeh. Sharpness focused on the crossbag and @model's face.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light from an overcast day, enhanced with cool cinematic grading. Low-key, soft, with cool neutral tones and controlled contrast. {lighting_detail}
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light. No harsh shadows. Cool temperature (5500K-6500K). Skin tones clean and neutral. Low-to-medium contrast: soft, three-dimensional look. Environmental colors desaturated by -15%. {dominant_tones}
[SCENE & ACTION] {scene_action}"""

SLIDE_07_PROMPT = """[INDICATIONS] A matte black nylon mini crossbag — product hero shot. The bag is the sole subject, displayed at a slight three-quarter angle. Visible details: tight ballistic nylon weave texture, metal YKK zipper, adjustable black buckle strap, compact rectangular form. Strap artfully draped. No person. No overlay, no text, no logo.
[STYLE] Editorial product photography. Clean, minimal composition. Negative space surrounds the product.
[CAMERA SETTINGS] Kodak Ektar 100 emulation, 85mm equivalent, f/4.0, 1/60s, ISO 100. Shallow depth of field. High clarity.
[LIGHTING: CONTROLLED STUDIO] Soft overhead key light from large softbox (6000K). Fill card on opposite side. Subtle rim light from behind.
[KEY TECHNICAL CHARACTERISTICS] Medium contrast. Neutral temperature (6000K). Nylon texture high detail. Metal hardware controlled specular highlights. Dominant tones: Matte black nylon, gunmetal zipper, soft grey background.
[SCENE & ACTION] The crossbag sits centered on a light grey matte surface at a slight angle, front zipper facing camera. The strap extends to the right, buckle catching light. Nylon weave clearly visible. Background fades to soft grey gradient. Minimal and confident."""


def run_phase1():
    """Phase 1: flat-lay 의상 이미지 생성"""
    print("\n" + "=" * 60)
    print("PHASE 1: Flat-lay 의상 이미지 생성")
    print("=" * 60)
    os.makedirs(OUTFIT_DIR, exist_ok=True)

    results = {}
    for name, prompt in OUTFIT_PROMPTS.items():
        filename = f"{name}.png"
        filepath = os.path.join(OUTFIT_DIR, filename)
        print(f"\n  생성 중: {filename}")
        try:
            img = call_api(prompt, {"aspectRatio": "4:5", "resolution": "1080x1350"}, [])
            save(img, filepath)
            results[name] = filepath
        except Exception as e:
            print(f"  [ERROR] {e}")
            results[name] = None
    return results


def run_phase2(outfit_paths: dict):
    """Phase 2: Composition — 젠아 모델 + 의상 합성"""
    print("\n" + "=" * 60)
    print("PHASE 2: Composition — 젠아 + 의상 합성")
    print("=" * 60)
    os.makedirs(COMP_DIR, exist_ok=True)

    # 각 룩별 페르소나 매핑
    look_persona = {
        "look1_casual": "gena_straight",
        "look2_minimal": "gena_braid",
        "look3_street": "gena_hippie",
    }

    results = {}
    for look_name, persona_key in look_persona.items():
        outfit_path = outfit_paths.get(look_name)
        if not outfit_path:
            print(f"\n  [SKIP] {look_name} — 의상 이미지 없음")
            results[look_name] = None
            continue

        filename = f"comp_{look_name}.png"
        filepath = os.path.join(COMP_DIR, filename)
        print(f"\n  합성 중: {filename}")
        print(f"  모델: {persona_key}")
        print(f"  의상: {os.path.basename(outfit_path)}")

        model_b64 = load_b64(PERSONA_PATHS[persona_key])
        garment_b64 = load_b64(outfit_path)

        try:
            # composition: [model, garment] 순서
            img = call_api(COMPOSITION_PROMPT, DEFAULT_CONFIG, [model_b64, garment_b64])
            save(img, filepath)
            results[look_name] = filepath
        except Exception as e:
            print(f"  [ERROR] {e}")
            results[look_name] = None
    return results


def run_phase3(comp_paths: dict):
    """Phase 3: 최종 슬라이드 이미지 생성"""
    print("\n" + "=" * 60)
    print("PHASE 3: 최종 슬라이드 이미지 생성")
    print("=" * 60)

    product_b64 = [load_b64(p) for p in get_product_images()]
    print(f"  제품 참조: {len(product_b64)}장")

    # 룩별 슬라이드 프롬프트
    look_slides = {
        "look1_casual": {
            "filename": "slide_04.png",
            "prompt": SLIDE_LOOK_TEMPLATE.format(
                outfit_desc="a cream oversized cable-knit cardigan over a white crewneck t-shirt, light blue washed wide-leg denim jeans, and white minimal sneakers",
                bag_wear_style="worn diagonally across the torso, the compact black rectangle sitting at hip level",
                action="walking casually with a relaxed confident stride",
                style_tone="Warm, soft neutral tones with natural light.",
                lighting_detail="5500K neutral daylight highlighting cream and denim textures.",
                dominant_tones="Dominant tones: Cream cardigan, white tee, light blue denim, matte black crossbag, warm concrete.",
                scene_action="A quiet residential street in Yeonnam-dong with low brick buildings and small potted plants along the sidewalk. @model walks toward the camera with a relaxed stride, cream cardigan open and flowing with the movement. The white tee and wide-leg jeans create a clean vertical line. The black crossbag sits at her hip, contrasting with the light outfit. She smiles softly, one hand holding the cardigan lapel, the other swinging naturally. Morning light wraps around the warm-toned buildings.",
            ),
        },
        "look2_minimal": {
            "filename": "slide_05.png",
            "prompt": SLIDE_LOOK_TEMPLATE.format(
                outfit_desc="a black oversized structured blazer over a crisp white button-down shirt, black high-waisted wide-leg tailored trousers, and black pointed-toe loafers",
                bag_wear_style="worn as a shoulder bag on one shoulder with a short strap, the rectangular form tucked under the arm",
                action="pausing mid-stride with a composed, thoughtful expression",
                style_tone="Cool, monochrome minimal tones. Clean and precise.",
                lighting_detail="6000K cool daylight emphasizing the black-white contrast and clean silhouette.",
                dominant_tones="Dominant tones: Black blazer, white shirt, black trousers, matte black crossbag, cool grey concrete.",
                scene_action="A clean, modern building entrance in Gangnam with grey stone walls and glass doors. @model stands in a slight contrapposto pose, one hand in her blazer pocket. The oversized blazer drapes over the white shirt, creating sharp contrast. The black crossbag is tucked under her left arm as a shoulder bag. She looks slightly to the side with a composed, minimal expression. Her double braids add a subtle youthful edge to the tailored monochrome look. The architectural lines of the building echo the clean geometry of the outfit.",
            ),
        },
        "look3_street": {
            "filename": "slide_06.png",
            "prompt": SLIDE_LOOK_TEMPLATE.format(
                outfit_desc="a black oversized hoodie with a sage green mesh utility vest layered on top, black wide-leg cargo jogger pants with utility pockets, and black chunky trail sneakers",
                bag_wear_style="worn as a waist bag (fanny pack) at the front hip, the compact form sitting flat against the body",
                action="leaning against a wall with relaxed street confidence",
                style_tone="Cool, desaturated urban tones with sage green as the color accent.",
                lighting_detail="5500K cool ambient light emphasizing urban greys and the sage green mesh texture.",
                dominant_tones="Dominant tones: Black hoodie, sage green mesh, black cargo jogger, matte black crossbag, concrete grey.",
                scene_action="A minimalist urban underpass stairway in Mangwon-dong with clean concrete walls and metal handrails. @model leans against the concrete wall, one foot on a lower step. Her long hippie-style wavy hair drapes over the sage green mesh vest. She looks directly at the camera with a relaxed, slightly playful expression, one hand adjusting the waist bag at her hip. The layered outfit creates visual depth — black hoodie base, semi-transparent sage mesh vest, and compact black waist bag at center. The cargo jogger pockets add utilitarian detail.",
            ),
        },
    }

    results = []

    # slide_02: 공감 (composition 불필요)
    print(f"\n  생성 중: slide_02.png (공감)")
    try:
        refs = [load_b64(PERSONA_PATHS["gena_straight"])]
        img = call_api(SLIDE_02_PROMPT, DEFAULT_CONFIG, refs)
        save(img, os.path.join(OUTPUT_DIR, "slide_02.png"))
        results.append(("slide_02.png", True))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_02.png", False))

    # slide_03: 소재 매크로 (composition 불필요)
    print(f"\n  생성 중: slide_03.png (소재 매크로)")
    try:
        img = call_api(SLIDE_03_PROMPT, DEFAULT_CONFIG, product_b64)
        save(img, os.path.join(OUTPUT_DIR, "slide_03.png"))
        results.append(("slide_03.png", True))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_03.png", False))

    # slide_04~06: 룩 슬라이드 (composition 결과 + 제품 참조)
    for look_name, slide_info in look_slides.items():
        fname = slide_info["filename"]
        print(f"\n  생성 중: {fname} ({look_name})")

        refs = []
        # composition 결과를 첫 번째 참조로
        comp_path = comp_paths.get(look_name)
        if comp_path and os.path.exists(comp_path):
            print(f"  composition 참조: {os.path.basename(comp_path)}")
            refs.append(load_b64(comp_path))
        # 제품 참조 추가
        refs.extend(product_b64)

        try:
            img = call_api(slide_info["prompt"], DEFAULT_CONFIG, refs)
            save(img, os.path.join(OUTPUT_DIR, fname))
            results.append((fname, True))
        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append((fname, False))

    # slide_07: 제품 클로즈업
    print(f"\n  생성 중: slide_07.png (제품 클로즈업)")
    try:
        img = call_api(SLIDE_07_PROMPT, DEFAULT_CONFIG, product_b64)
        save(img, os.path.join(OUTPUT_DIR, "slide_07.png"))
        results.append(("slide_07.png", True))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_07.png", False))

    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 페르소나 확인
    for key, path in PERSONA_PATHS.items():
        if not os.path.exists(path):
            print(f"[ERROR] 페르소나 없음: {path}")
            sys.exit(1)
        print(f"  [OK] {key}: {os.path.getsize(path)/1024/1024:.1f}MB")

    # 제품 확인
    product_imgs = get_product_images()
    print(f"\n  제품 이미지 ({len(product_imgs)}장):")
    for p in product_imgs:
        print(f"  [OK] {os.path.basename(p)}: {os.path.getsize(p)/1024/1024:.1f}MB")

    # === 3단계 파이프라인 ===
    outfit_paths = run_phase1()
    comp_paths = run_phase2(outfit_paths)
    slide_results = run_phase3(comp_paths)

    # 최종 결과
    print(f"\n{'='*60}")
    print("최종 결과:")
    print(f"{'='*60}")
    for fname, ok in slide_results:
        fpath = os.path.join(OUTPUT_DIR, fname)
        if ok and os.path.exists(fpath):
            print(f"  [OK] {fpath} ({os.path.getsize(fpath)/1024:.0f}KB)")
        else:
            print(f"  [FAIL] {fname}")

    success = sum(1 for _, ok in slide_results if ok)
    print(f"\n성공: {success}/{len(slide_results)}")
    if success < len(slide_results):
        sys.exit(1)


if __name__ == "__main__":
    main()
