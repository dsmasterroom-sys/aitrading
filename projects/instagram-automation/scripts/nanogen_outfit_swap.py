#!/usr/bin/env python3
"""
Nanogen Outfit Swap 자동화 스크립트

목표:
- Gena 참조 이미지 + 의상 이미지 → Outfit Swap 자동 실행
- Phase 1 검증에서 확인된 2단계 파이프라인 자동화

사용법:
    python scripts/nanogen_outfit_swap.py \
        --gena-ref shared/gena-references/gena_ref_01.png \
        --garment-image test_output/garment_sample.png \
        --output test_output/outfit_swap_result.png

API:
    POST http://localhost:8000/api/generate
    {
        "prompt": "의상교체",
        "config": {
            "modelId": "gemini-3.1-flash-image-preview",
            "aspectRatio": "1:1",
            "resolution": "1K"
        },
        "referenceImages": [
            "data:image/png;base64,...",  # Gena reference
            "data:image/jpeg;base64,..."  # Garment image
        ]
    }
"""

import argparse
import base64
import json
import requests
from pathlib import Path


def load_image_as_base64(image_path):
    """이미지를 base64 data URI로 변환"""
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # 파일 확장자로 MIME 타입 결정
    ext = image_path.suffix.lower()
    mime_type = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp'
    }.get(ext, 'image/png')
    
    return f"data:{mime_type};base64,{b64}"


def nanogen_outfit_swap(
    gena_ref_path,
    garment_path,
    output_path=None,
    nanogen_url="http://localhost:8000",
    prompt=None,
    aspect_ratio="1:1",
    resolution="1K"
):
    """
    Nanogen Outfit Swap 실행
    
    Args:
        gena_ref_path: Gena 참조 이미지 경로
        garment_path: 의상 이미지 경로
        output_path: 결과 저장 경로 (None이면 자동 생성)
        nanogen_url: Nanogen 서버 URL
        prompt: 생성 프롬프트 (기본: "의상교체")
        aspect_ratio: 이미지 비율 (1:1, 3:4, 16:9 등)
        resolution: 이미지 해상도 (1K, 2K)
    
    Returns:
        dict: {
            'success': bool,
            'output_path': str,
            'saved_image_url': str (Nanogen DB에 저장된 URL)
        }
    """
    
    # Generate default detailed prompt if not provided
    if prompt is None:
        prompt = """[STRICT OUTFIT SWAP TASK]

Reference Image 1: Korean fashion model with specific pose and styling
Reference Image 2: Product image (bag/garment/accessory)

CRITICAL REQUIREMENTS:
1. PRESERVE from Reference Image 1:
   - EXACT same person identity and face features
   - EXACT same pose and body position
   - EXACT same lighting, shadows, and atmosphere
   - EXACT same background and environment
   - EXACT same hair style and makeup

2. SWAP from Reference Image 2:
   - Replace ONLY the bag/garment/accessory shown in Reference 2
   - Product must appear natural on the model's body
   - Product details (color, texture, design) must be ACCURATE and CLEARLY VISIBLE
   - Product placement must match the model's pose naturally

3. TECHNICAL QUALITY:
   - Professional commercial photography quality
   - Seamless integration between model and product
   - Natural lighting consistency
   - Sharp focus on both face and product
   - High-resolution output suitable for Instagram

DO NOT:
- Change the model's face, identity, or any facial features
- Alter the pose, body position, or background
- Add or remove other accessories not specified
- Change lighting or color grading

ONLY swap the specified product while keeping everything else identical."""
    
    print(f"🎨 Nanogen Outfit Swap 시작...")
    print(f"  Gena 참조: {gena_ref_path}")
    print(f"  의상 이미지: {garment_path}")
    print(f"  프롬프트 길이: {len(prompt)} chars")
    print(f"  해상도: {aspect_ratio} @ {resolution}")
    print()
    
    # 1. 이미지 로드
    try:
        gena_ref_b64 = load_image_as_base64(gena_ref_path)
        garment_b64 = load_image_as_base64(garment_path)
        print("✅ 이미지 로드 완료")
    except Exception as e:
        print(f"❌ 이미지 로드 실패: {e}")
        return {'success': False, 'error': str(e)}
    
    # 2. API 요청 데이터 구성
    request_data = {
        "prompt": prompt,
        "config": {
            "modelId": "gemini-3.1-flash-image-preview",
            "aspectRatio": aspect_ratio,
            "resolution": resolution,
            "useGrounding": False
        },
        "referenceImages": [
            gena_ref_b64,   # 첫 번째: 인물(Gena)
            garment_b64     # 두 번째: 의상
        ]
    }
    
    # 3. Nanogen API 호출
    print("📡 Nanogen API 호출 중...")
    try:
        response = requests.post(
            f"{nanogen_url}/api/generate",
            json=request_data,
            timeout=120  # 2분 타임아웃
        )
        response.raise_for_status()
        result = response.json()
        print("✅ 생성 완료")
    except requests.exceptions.Timeout:
        print("❌ 타임아웃: Nanogen 응답이 없습니다 (2분 초과)")
        return {'success': False, 'error': 'Timeout'}
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return {'success': False, 'error': str(e)}
    
    # 4. 결과 저장
    try:
        image_url = result.get('url')
        saved_image = result.get('saved_image', {})
        
        if not image_url:
            print("❌ 결과 URL이 없습니다")
            return {'success': False, 'error': 'No image URL in response'}
        
        # base64 디코딩
        if image_url.startswith('data:'):
            header, data = image_url.split(',', 1)
            image_bytes = base64.b64decode(data)
            
            # 출력 경로 결정
            if output_path is None:
                output_dir = Path(__file__).parent.parent / "test_output"
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / f"outfit_swap_{Path(gena_ref_path).stem}_{Path(garment_path).stem}.png"
            else:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 파일 저장
            with open(output_path, 'wb') as f:
                f.write(image_bytes)
            
            print(f"✅ 저장 완료: {output_path}")
            print(f"📊 파일 크기: {len(image_bytes) / 1024:.1f} KB")
            
            if saved_image.get('url'):
                print(f"🔗 Nanogen DB URL: {nanogen_url}{saved_image['url']}")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'saved_image_url': saved_image.get('url'),
                'saved_image_id': saved_image.get('id')
            }
        else:
            print("❌ 예상치 못한 응답 형식")
            return {'success': False, 'error': 'Unexpected response format'}
            
    except Exception as e:
        print(f"❌ 결과 저장 실패: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}


def main():
    parser = argparse.ArgumentParser(description='Nanogen Outfit Swap 자동화')
    parser.add_argument('--gena-ref', required=True, help='Gena 참조 이미지 경로')
    parser.add_argument('--garment', required=True, help='의상 이미지 경로')
    parser.add_argument('--output', help='결과 저장 경로 (선택, 기본: test_output/)')
    parser.add_argument('--nanogen-url', default='http://localhost:8000', help='Nanogen 서버 URL')
    parser.add_argument('--prompt', default=None, help='생성 프롬프트 (기본: 자세한 outfit swap 지시문)')
    parser.add_argument('--aspect-ratio', default='1:1', help='이미지 비율 (1:1, 3:4, 16:9)')
    parser.add_argument('--resolution', default='1K', help='이미지 해상도 (1K, 2K)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🤖 Nanogen Outfit Swap 자동화")
    print("=" * 70)
    print()
    
    result = nanogen_outfit_swap(
        gena_ref_path=args.gena_ref,
        garment_path=args.garment,
        output_path=args.output,
        nanogen_url=args.nanogen_url,
        prompt=args.prompt,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution
    )
    
    print()
    print("=" * 70)
    if result['success']:
        print("✅ SUCCESS")
        print(f"\n📁 Output: {result['output_path']}")
        if result.get('saved_image_url'):
            print(f"🔗 Nanogen DB: {args.nanogen_url}{result['saved_image_url']}")
    else:
        print("❌ FAILED")
        print(f"\n❗ Error: {result.get('error', 'Unknown error')}")
    print("=" * 70)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    exit(main())
