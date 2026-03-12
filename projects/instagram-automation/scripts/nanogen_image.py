#!/usr/bin/env python3 -u
"""
Nanogen 이미지 생성 자동화 (Designer Agent 전용)

-u flag: unbuffered output (로그 즉시 출력)

목표:
- prompts.json + items.json 읽기
- Gena 참조 이미지 + 아이템 이미지 → Outfit Swap
- assets/ 폴더에 자동 저장

사용법:
    python scripts/nanogen_image.py \
        --content-path content/20260306_spring_outfits \
        --slide-id slide_02

또는 전체 슬라이드 일괄 생성:
    python scripts/nanogen_image.py \
        --content-path content/20260306_spring_outfits \
        --all
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Unbuffered stdout
sys.stdout.reconfigure(line_buffering=True)

# 스크립트 디렉토리를 sys.path에 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from nanogen_outfit_swap import nanogen_outfit_swap, load_image_as_base64


def load_json(file_path):
    """JSON 파일 로드"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_slide_image(
    content_path,
    slide_id,
    prompts_data,
    items_data,
    nanogen_url="http://localhost:8000",
    aspect_ratio="3:4",
    resolution="2K",
    max_retries=3
):
    """
    단일 슬라이드 이미지 생성
    
    Args:
        content_path: 콘텐츠 작업 폴더 (예: content/20260306_spring_outfits)
        slide_id: 슬라이드 ID (예: slide_02)
        prompts_data: prompts.json 데이터
        items_data: items.json 데이터
        nanogen_url: Nanogen 서버 URL
        aspect_ratio: 이미지 비율 (3:4 기본)
        resolution: 이미지 해상도 (2K 기본)
        max_retries: 최대 재시도 횟수
    
    Returns:
        dict: 생성 결과
    """
    
    content_path = Path(content_path)
    
    print(f"\n{'='*70}")
    print(f"🎨 슬라이드 이미지 생성: {slide_id}")
    print(f"{'='*70}")
    
    # 1. prompts.json에서 슬라이드 정보 읽기
    if slide_id not in prompts_data:
        print(f"❌ {slide_id}가 prompts.json에 없습니다")
        return {'success': False, 'error': f'{slide_id} not found'}
    
    slide_data = prompts_data[slide_id]
    reference_images = slide_data.get('reference_images', [])
    
    if len(reference_images) < 2:
        print(f"❌ reference_images가 부족합니다 (필요: 2개, 현재: {len(reference_images)}개)")
        return {'success': False, 'error': 'Insufficient reference images'}
    
    gena_ref_filename = reference_images[0]  # 예: gena_ref_04.png
    item_id = reference_images[1]            # 예: top_001
    
    print(f"  Gena 참조: {gena_ref_filename}")
    print(f"  아이템 ID: {item_id}")
    
    # 2. items.json에서 아이템 정보 읽기
    if item_id not in items_data:
        print(f"❌ {item_id}가 items.json에 없습니다")
        return {'success': False, 'error': f'{item_id} not found in items.json'}
    
    item_data = items_data[item_id]
    garment_url = item_data.get('ref_image_url')
    
    if not garment_url:
        print(f"❌ {item_id}에 ref_image_url이 없습니다")
        return {'success': False, 'error': 'No ref_image_url'}
    
    print(f"  아이템 이미지: {garment_url}")
    
    # 3. 파일 경로 설정
    gena_ref_path = content_path.parent.parent / "shared" / "gena-references" / gena_ref_filename
    
    # 아이템 이미지 다운로드 (또는 로컬 경로)
    # TODO: URL인 경우 다운로드 로직 추가
    # 지금은 로컬 파일 가정
    if garment_url.startswith('http'):
        print(f"⚠️  URL 다운로드는 아직 미구현입니다: {garment_url}")
        print(f"   로컬 테스트를 위해 garment_sample.png 사용")
        garment_path = content_path.parent.parent / "test_output" / "garment_sample.png"
    else:
        garment_path = Path(garment_url)
    
    # 출력 경로
    assets_dir = content_path / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    content_type = slide_data.get('content_type', 'carousel')
    output_filename = f"{content_type}_{slide_id}.png"
    output_path = assets_dir / output_filename
    
    # 4. Nanogen Outfit Swap 실행 (재시도 로직 포함)
    retry_count = 0
    last_error = None
    
    while retry_count < max_retries:
        if retry_count > 0:
            print(f"\n🔄 재시도 {retry_count}/{max_retries}...")
            time.sleep(2)  # 재시도 전 대기
        
        result = nanogen_outfit_swap(
            gena_ref_path=str(gena_ref_path),
            garment_path=str(garment_path),
            output_path=str(output_path),
            nanogen_url=nanogen_url,
            prompt=slide_data.get('image_prompt', '의상교체'),
            aspect_ratio=aspect_ratio,
            resolution=resolution
        )
        
        if result['success']:
            print(f"\n✅ 슬라이드 {slide_id} 생성 완료!")
            print(f"📁 저장 위치: {output_path}")
            return result
        
        last_error = result.get('error', 'Unknown error')
        retry_count += 1
    
    # 최대 재시도 초과
    print(f"\n❌ 슬라이드 {slide_id} 생성 실패 (재시도 {max_retries}회 초과)")
    print(f"   마지막 오류: {last_error}")
    return {'success': False, 'error': last_error, 'retries': max_retries}


def generate_all_slides(
    content_path,
    nanogen_url="http://localhost:8000",
    aspect_ratio="3:4",
    resolution="2K",
    max_retries=3
):
    """
    prompts.json의 모든 슬라이드 이미지 생성
    
    Args:
        content_path: 콘텐츠 작업 폴더
        nanogen_url: Nanogen 서버 URL
        aspect_ratio: 이미지 비율
        resolution: 이미지 해상도
        max_retries: 슬라이드당 최대 재시도 횟수
    
    Returns:
        dict: 전체 생성 결과 요약
    """
    
    content_path = Path(content_path)
    
    print(f"\n{'='*70}")
    print(f"🚀 전체 슬라이드 이미지 생성 시작")
    print(f"{'='*70}")
    print(f"  콘텐츠 폴더: {content_path}")
    print(f"  해상도: {aspect_ratio} @ {resolution}")
    print()
    
    # 1. JSON 파일 로드
    try:
        prompts_path = content_path / "prompts.json"
        items_path = content_path / "items.json"
        
        if not prompts_path.exists():
            print(f"❌ prompts.json이 없습니다: {prompts_path}")
            return {'success': False, 'error': 'prompts.json not found'}
        
        if not items_path.exists():
            print(f"❌ items.json이 없습니다: {items_path}")
            return {'success': False, 'error': 'items.json not found'}
        
        prompts_data = load_json(prompts_path)
        items_data = load_json(items_path)
        
        print(f"✅ prompts.json 로드 완료 ({len(prompts_data)}개 슬라이드)")
        print(f"✅ items.json 로드 완료 ({len(items_data)}개 아이템)")
        
    except Exception as e:
        print(f"❌ JSON 로드 실패: {e}")
        return {'success': False, 'error': str(e)}
    
    # 2. 슬라이드별 생성
    results = {}
    success_count = 0
    fail_count = 0
    
    for slide_id in prompts_data.keys():
        result = generate_slide_image(
            content_path=content_path,
            slide_id=slide_id,
            prompts_data=prompts_data,
            items_data=items_data,
            nanogen_url=nanogen_url,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            max_retries=max_retries
        )
        
        results[slide_id] = result
        
        if result['success']:
            success_count += 1
        else:
            fail_count += 1
    
    # 3. 결과 요약
    print(f"\n{'='*70}")
    print(f"📊 전체 생성 완료")
    print(f"{'='*70}")
    print(f"  성공: {success_count}개")
    print(f"  실패: {fail_count}개")
    print(f"  총 {len(results)}개 슬라이드")
    print()
    
    if fail_count > 0:
        print("❌ 실패한 슬라이드:")
        for slide_id, result in results.items():
            if not result['success']:
                print(f"  - {slide_id}: {result.get('error', 'Unknown')}")
    
    return {
        'success': fail_count == 0,
        'total': len(results),
        'success_count': success_count,
        'fail_count': fail_count,
        'details': results
    }


def main():
    parser = argparse.ArgumentParser(description='Nanogen 이미지 생성 자동화')
    parser.add_argument('--content-path', required=True, help='콘텐츠 작업 폴더 (예: content/20260306_spring_outfits)')
    parser.add_argument('--slide-id', help='생성할 슬라이드 ID (예: slide_02)')
    parser.add_argument('--all', action='store_true', help='모든 슬라이드 생성')
    parser.add_argument('--nanogen-url', default='http://localhost:8000', help='Nanogen 서버 URL')
    parser.add_argument('--aspect-ratio', default='3:4', help='이미지 비율 (3:4 기본)')
    parser.add_argument('--resolution', default='2K', help='이미지 해상도 (2K 기본)')
    parser.add_argument('--max-retries', type=int, default=3, help='최대 재시도 횟수')
    
    args = parser.parse_args()
    
    if not args.slide_id and not args.all:
        print("❌ --slide-id 또는 --all 중 하나를 지정해야 합니다")
        return 1
    
    print("=" * 70)
    print("🤖 Nanogen 이미지 생성 자동화 (Designer Agent)")
    print("=" * 70)
    print()
    
    if args.all:
        # 전체 슬라이드 생성
        result = generate_all_slides(
            content_path=args.content_path,
            nanogen_url=args.nanogen_url,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            max_retries=args.max_retries
        )
    else:
        # 단일 슬라이드 생성
        content_path = Path(args.content_path)
        
        try:
            prompts_data = load_json(content_path / "prompts.json")
            items_data = load_json(content_path / "items.json")
        except Exception as e:
            print(f"❌ JSON 로드 실패: {e}")
            return 1
        
        result = generate_slide_image(
            content_path=content_path,
            slide_id=args.slide_id,
            prompts_data=prompts_data,
            items_data=items_data,
            nanogen_url=args.nanogen_url,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            max_retries=args.max_retries
        )
    
    print()
    print("=" * 70)
    if result['success']:
        print("✅ SUCCESS")
    else:
        print("❌ FAILED")
        print(f"\n❗ Error: {result.get('error', 'Unknown error')}")
    print("=" * 70)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
