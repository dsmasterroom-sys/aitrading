#!/usr/bin/env python3
"""
one-bag-multi-look 시리즈 이미지 v2 — 2단계 프로세스 적용.

변경점:
- 인물 이미지: 1단계 generation (프롬프트 개선) → 2단계 identity_swap (젠아 얼굴 적용)
- 제품 이미지: 제품 레퍼런스 강참조 1단계만
- 프롬프트: 클린 에디토리얼 스타일로 전면 수정
"""

import base64
import json
import os
import sys
import time
import requests

# 경로 설정
BASE_DIR = "/Users/master/.openclaw/workspace/projects/gena_feed"
OUTPUT_DIR = os.path.join(BASE_DIR, "series/one-bag-multi-look/generated")

# 레퍼런스 이미지 경로
REF_PATHS = {
    "gena_straight": os.path.join(BASE_DIR, "shared/persona/gena_ref_03_basic_straight.png"),
    "gena_braid": os.path.join(BASE_DIR, "shared/persona/gena_ref_08_double_down_braid.png"),
    "gena_hippie": os.path.join(BASE_DIR, "shared/persona/gena_ref_09_long_hippie.png"),
    "product_4view": os.path.join(BASE_DIR, "shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png"),
    "product_fit": os.path.join(BASE_DIR, "shared/products/genarchive_crossbag/genarchive_crossbag_fit.png"),
}

API_URL = "http://localhost:8000/api/generate"
TIMEOUT = 600

IDENTITY_SWAP_PROMPT = (
    "Perform a seamless identity swap, replacing the original person with the identity "
    "and likeness of the provided attached model. Crucially, the new model must adopt the "
    "exact same pose, body proportions, composition, and placement within the frame as the "
    "original person. The entire background, lighting, shadows, and atmosphere must remain "
    "100% identical to the original image. Photorealistic, high fidelity result."
)

DEFAULT_CONFIG = {"aspectRatio": "4:5", "resolution": "1080x1350"}


def load_b64(path: str) -> str:
    """이미지 파일을 base64 문자열로 인코딩"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def bytes_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def call_api(prompt: str, config: dict, ref_images_b64: list[str]) -> bytes:
    """나노젠 API 호출 → 이미지 바이트 반환"""
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


def save_image(data: bytes, filename: str) -> str:
    """이미지 저장 후 경로 반환"""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "wb") as f:
        f.write(data)
    size_kb = os.path.getsize(path) / 1024
    print(f"  저장: {path} ({size_kb:.1f}KB)")
    return path


def generate_person_slide(
    name: str,
    base_filename: str,
    final_filename: str,
    gen_prompt: str,
    product_ref_keys: list[str],
    face_ref_key: str,
):
    """인물 슬라이드: 1단계 generation → 2단계 identity_swap"""
    print(f"\n{'='*60}")
    print(f"[{name}] 1단계: base 이미지 generation")

    # 1단계: 클린 에디토리얼 base 이미지 생성
    product_refs = [load_b64(REF_PATHS[k]) for k in product_ref_keys]
    for k in product_ref_keys:
        print(f"  제품 레퍼런스: {os.path.basename(REF_PATHS[k])}")

    base_bytes = call_api(gen_prompt, DEFAULT_CONFIG, product_refs)
    save_image(base_bytes, base_filename)
    print(f"  1단계 완료")

    # 2단계: identity swap으로 젠아 얼굴 적용
    print(f"[{name}] 2단계: identity swap (face: {face_ref_key})")
    scene_b64 = bytes_to_b64(base_bytes)
    face_b64 = load_b64(REF_PATHS[face_ref_key])
    print(f"  얼굴 레퍼런스: {os.path.basename(REF_PATHS[face_ref_key])}")

    final_bytes = call_api(IDENTITY_SWAP_PROMPT, DEFAULT_CONFIG, [scene_b64, face_b64])
    save_image(final_bytes, final_filename)
    print(f"  2단계 완료 → {final_filename}")
    return True


def generate_product_slide(name: str, filename: str, prompt: str, ref_keys: list[str]):
    """제품 슬라이드: 1단계만 (identity swap 불필요)"""
    print(f"\n{'='*60}")
    print(f"[{name}] 제품 이미지 generation (1단계만)")

    refs = [load_b64(REF_PATHS[k]) for k in ref_keys]
    for k in ref_keys:
        print(f"  제품 레퍼런스: {os.path.basename(REF_PATHS[k])}")

    img_bytes = call_api(prompt, DEFAULT_CONFIG, refs)
    save_image(img_bytes, filename)
    print(f"  완료 → {filename}")
    return True


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 레퍼런스 이미지 존재 확인
    for key, path in REF_PATHS.items():
        if not os.path.exists(path):
            print(f"[ERROR] 레퍼런스 이미지 없음: {path}")
            sys.exit(1)
        print(f"  [OK] {key}: {os.path.getsize(path)/1024/1024:.1f}MB")

    results = []

    # ── slide_02: 공감 — 거울 앞 고민 ──
    try:
        ok = generate_person_slide(
            name="slide_02 (공감 — 거울 앞 고민)",
            base_filename="slide_02_base.png",
            final_filename="slide_02.png",
            gen_prompt=(
                "Korean beautiful fashion influencer standing in front of full-length mirror "
                "in bright clean bedroom, multiple bags on white bed, contemplating which bag to carry, "
                "oversized grey cotton t-shirt and black leggings, polished minimalist interior, "
                "soft overcast daylight from large window 5500K, editorial lifestyle photography, "
                "fashion lookbook quality, well-groomed, hyperrealistic skin texture, micro-expression detail"
            ),
            product_ref_keys=[],  # no product ref for this slide
            face_ref_key="gena_straight",
        )
        results.append(("slide_02.png", ok))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_02.png", False))

    # ── slide_04: LOOK 1 크로스백 — 고프코어 ──
    try:
        ok = generate_person_slide(
            name="slide_04 (LOOK 1 크로스백 — 고프코어)",
            base_filename="slide_04_base.png",
            final_filename="slide_04.png",
            gen_prompt=(
                "Korean beautiful fashion influencer full-body shot, polished clean gorpcore style, "
                "charcoal windbreaker layered over mocha mousse warm brown hoodie, black cargo pants, "
                "matte black nylon mini crossbag worn diagonally across torso, minimalist urban backdrop "
                "with clean concrete wall, overcast natural light 5500-6500K low contrast, editorial fashion "
                "lookbook quality, well-groomed, dynamic stride pose, hyperrealistic skin texture, peach fuzz glow"
            ),
            product_ref_keys=["product_fit", "product_4view"],
            face_ref_key="gena_straight",
        )
        results.append(("slide_04.png", ok))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_04.png", False))

    # ── slide_05: LOOK 2 숄더백 — 테크웨어 ──
    try:
        ok = generate_person_slide(
            name="slide_05 (LOOK 2 숄더백 — 테크웨어)",
            base_filename="slide_05_base.png",
            final_filename="slide_05.png",
            gen_prompt=(
                "Korean beautiful fashion influencer full-body shot, clean techwear editorial style, "
                "black shell jacket over deep lavender future dusk crop zip-up, grey wide jogger pants, "
                "matte black nylon mini bag worn as shoulder bag on one shoulder, minimalist parking structure "
                "backdrop with clean lines, overcast diffused light 6000K cool tone, editorial fashion "
                "lookbook quality, well-groomed, contrapposto stance, hyperrealistic skin texture, subtle eye bags"
            ),
            product_ref_keys=["product_fit", "product_4view"],
            face_ref_key="gena_braid",
        )
        results.append(("slide_05.png", ok))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_05.png", False))

    # ── slide_06: LOOK 3 힙색 — 스트릿 ──
    try:
        ok = generate_person_slide(
            name="slide_06 (LOOK 3 힙색 — 스트릿)",
            base_filename="slide_06_base.png",
            final_filename="slide_06.png",
            gen_prompt=(
                "Korean beautiful fashion influencer full-body shot, clean street layered editorial style, "
                "black oversized hoodie with aqua glaze mint blue mesh vest layered on top, black jogger pants, "
                "black trail shoes, matte black nylon mini bag worn as waist bag at front hip, minimalist urban "
                "stairway with clean architecture, overcast ambient light 5500K cool desaturated tones, "
                "editorial fashion lookbook quality, well-groomed, leaning against wall pose, hyperrealistic "
                "skin texture, peach fuzz glow"
            ),
            product_ref_keys=["product_fit", "product_4view"],
            face_ref_key="gena_hippie",
        )
        results.append(("slide_06.png", ok))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_06.png", False))

    # ── slide_07: 제품 클로즈업 ──
    try:
        ok = generate_product_slide(
            name="slide_07 (제품 클로즈업)",
            filename="slide_07.png",
            prompt=(
                "matte black nylon mini crossbag product hero shot, clean white studio backdrop, "
                "visible nylon weave texture, metal zipper detail, adjustable buckle strap, minimalist "
                "compact rectangular form, studio lighting 6000K even soft diffusion, editorial product "
                "photography, fashion e-commerce quality, hyperrealistic fabric texture"
            ),
            ref_keys=["product_4view", "product_fit"],
        )
        results.append(("slide_07.png", ok))
    except Exception as e:
        print(f"  [ERROR] {e}")
        results.append(("slide_07.png", False))

    # ── 최종 결과 보고 ──
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

    # base 이미지도 보고
    print(f"\nbase 이미지:")
    for base in ["slide_02_base.png", "slide_04_base.png", "slide_05_base.png", "slide_06_base.png"]:
        bp = os.path.join(OUTPUT_DIR, base)
        if os.path.exists(bp):
            print(f"  [OK] {bp} ({os.path.getsize(bp)/1024:.1f}KB)")

    success_count = sum(1 for _, s in results if s)
    print(f"\n성공: {success_count}/5")

    if success_count < 5:
        sys.exit(1)


if __name__ == "__main__":
    main()
