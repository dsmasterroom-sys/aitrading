#!/usr/bin/env python3
"""
나노젠 API를 사용하여 one-bag-multi-look 시리즈 이미지 5장을 생성하는 스크립트.
"""

import base64
import json
import os
import sys
import requests

# 경로 설정
BASE_DIR = "/Users/master/.openclaw/workspace/projects/gena_feed"
OUTPUT_DIR = os.path.join(BASE_DIR, "series/one-bag-multi-look/generated")

# 레퍼런스 이미지 경로
REF_IMAGES = {
    "gena_straight": os.path.join(BASE_DIR, "shared/persona/gena_ref_03_basic_straight.png"),
    "gena_braid": os.path.join(BASE_DIR, "shared/persona/gena_ref_08_double_down_braid.png"),
    "gena_hippie": os.path.join(BASE_DIR, "shared/persona/gena_ref_09_long_hippie.png"),
    "product_4view": os.path.join(BASE_DIR, "shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png"),
    "product_fit": os.path.join(BASE_DIR, "shared/products/genarchive_crossbag/genarchive_crossbag_fit.png"),
}

API_URL = "http://localhost:8000/api/generate"


def load_image_base64(path: str) -> str:
    """이미지 파일을 base64 문자열로 인코딩"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_and_save(filename: str, prompt: str, config: dict, ref_keys: list[str]):
    """나노젠 API를 호출하고 결과 이미지를 저장"""
    print(f"\n{'='*60}")
    print(f"생성 중: {filename}")
    print(f"레퍼런스: {', '.join(ref_keys)}")

    # 레퍼런스 이미지 base64 인코딩
    reference_images = []
    for key in ref_keys:
        path = REF_IMAGES[key]
        print(f"  로딩: {os.path.basename(path)} ({os.path.getsize(path) / 1024 / 1024:.1f}MB)")
        reference_images.append(load_image_base64(path))

    # API 요청 구성
    payload = {
        "prompt": prompt,
        "config": config,
        "referenceImages": reference_images,
    }

    print(f"  API 호출 중...")
    try:
        response = requests.post(API_URL, json=payload, timeout=300)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] 나노젠 서버 연결 실패 (localhost:8000). 서버가 실행 중인지 확인하세요.")
        return False
    except requests.exceptions.Timeout:
        print(f"  [ERROR] API 응답 타임아웃 (300초)")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"  [ERROR] API HTTP 에러: {e}")
        print(f"  응답: {response.text[:500]}")
        return False

    # 응답에서 이미지 데이터 추출
    result = response.json()
    image_data = result.get("url", "")

    # data:image/png;base64, 프리픽스 제거
    prefix = "data:image/png;base64,"
    if image_data.startswith(prefix):
        image_data = image_data[len(prefix):]

    # base64 디코딩 후 파일 저장
    output_path = os.path.join(OUTPUT_DIR, filename)
    image_bytes = base64.b64decode(image_data)
    with open(output_path, "wb") as f:
        f.write(image_bytes)

    file_size = os.path.getsize(output_path)
    print(f"  저장 완료: {output_path}")
    print(f"  파일 크기: {file_size / 1024:.1f}KB")
    return True


def main():
    # 출력 디렉토리 확인
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 레퍼런스 이미지 존재 확인
    for key, path in REF_IMAGES.items():
        if not os.path.exists(path):
            print(f"[ERROR] 레퍼런스 이미지 없음: {path}")
            sys.exit(1)

    # 생성할 이미지 정의
    slides = [
        {
            "filename": "slide_02.png",
            "prompt": "young Korean woman standing in front of full-length mirror, bedroom interior, multiple bags scattered on bed, contemplating expression looking at reflection, oversized grey t-shirt and black leggings, overcast daylight from window 5500K cool tone, hyperrealistic skin texture, visible pores, micro-expression detail, soft Korean lifestyle",
            "config": {"aspectRatio": "4:5", "resolution": "1080x1350"},
            "ref_keys": ["gena_straight"],
        },
        {
            "filename": "slide_04.png",
            "prompt": "young Korean woman full-body street style, charcoal windbreaker layered over mocha mousse brown hoodie, black cargo pants, matte black nylon mini crossbag worn diagonally across torso, urban concrete alley background, overcast natural light 5500-6500K low contrast, dynamic stride pose, streetwear inspired, hyperrealistic skin texture, peach fuzz glow, tone-on-tone outfit",
            "config": {"aspectRatio": "4:5", "resolution": "1080x1350"},
            "ref_keys": ["gena_straight", "product_fit", "product_4view"],
        },
        {
            "filename": "slide_05.png",
            "prompt": "young Korean woman full-body techwear outfit, black shell jacket over deep lavender future dusk crop zip-up, grey wide jogger pants, matte black nylon mini bag worn as shoulder bag on one shoulder with short strap, urban sidewalk parking lot concrete background, overcast diffused light 6000K cool tone low contrast, contrapposto stance, mid-motion capture, high-fashion editorial, hyperrealistic skin texture, subtle eye bags, oversized proportions",
            "config": {"aspectRatio": "4:5", "resolution": "1080x1350"},
            "ref_keys": ["gena_braid", "product_fit", "product_4view"],
        },
        {
            "filename": "slide_06.png",
            "prompt": "young Korean woman full-body street layered look, black oversized hoodie with aqua glaze mint blue mesh vest layered on top, black trail shoes, matte black nylon mini bag worn as waist bag at front hip, urban stairway underpass background, overcast ambient light 5500K cool desaturated tones, leaning against wall pose, streetwear inspired, hyperrealistic skin texture, peach fuzz glow, micro-expression detail, oversized proportions",
            "config": {"aspectRatio": "4:5", "resolution": "1080x1350"},
            "ref_keys": ["gena_hippie", "product_fit", "product_4view"],
        },
        {
            "filename": "slide_07.png",
            "prompt": "matte black nylon mini crossbag product close-up macro shot, visible nylon weave texture, metal zipper detail, adjustable buckle strap, minimalist compact rectangular form, overcast studio light 6000K even diffusion no harsh shadow, tailored minimalism, hyperrealistic fabric texture",
            "config": {"aspectRatio": "4:5", "resolution": "1080x1350"},
            "ref_keys": ["product_4view", "product_fit"],
        },
    ]

    results = []
    for slide in slides:
        success = generate_and_save(
            filename=slide["filename"],
            prompt=slide["prompt"],
            config=slide["config"],
            ref_keys=slide["ref_keys"],
        )
        results.append((slide["filename"], success))

    # 최종 결과 보고
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
    print(f"\n성공: {success_count}/5")

    if success_count < 5:
        sys.exit(1)


if __name__ == "__main__":
    main()
