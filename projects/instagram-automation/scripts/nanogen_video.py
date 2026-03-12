#!/usr/bin/env python3
"""
Nanogen 비디오 생성 자동화 (Video Agent 전용)

목표:
- prompts.json의 video_prompts 읽기
- Kling v3.0 / Veo API 호출
- 폴링 대기 → reels/ 폴더에 자동 저장

사용법:
    python scripts/nanogen_video.py \
        --content-path content/20260306_spring_reels \
        --scene-id scene_01

또는 전체 씬 일괄 생성:
    python scripts/nanogen_video.py \
        --content-path content/20260306_spring_reels \
        --all
"""

import argparse
import base64
import json
import sys
import time
import requests
from pathlib import Path


def load_json(file_path):
    """JSON 파일 로드"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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


def generate_video_scene(
    content_path,
    scene_id,
    video_prompts_data,
    nanogen_url="http://localhost:8000",
    model_id="kling-v3",
    kling_mode="standard",
    duration_seconds=5,
    camera_movement=None,
    poll_timeout=300,
    poll_interval=5
):
    """
    단일 비디오 씬 생성
    
    Args:
        content_path: 콘텐츠 작업 폴더 (예: content/20260306_spring_reels)
        scene_id: 씬 ID (예: scene_01)
        video_prompts_data: prompts.json의 video_prompts 섹션
        nanogen_url: Nanogen 서버 URL
        model_id: 비디오 모델 (kling-v3, veo 등)
        kling_mode: Kling 모드 (standard, pro)
        duration_seconds: 영상 길이 (초)
        camera_movement: 카메라 무브먼트 (pan_right, zoom_in 등)
        poll_timeout: 폴링 타임아웃 (초)
        poll_interval: 폴링 간격 (초)
    
    Returns:
        dict: 생성 결과
    """
    
    content_path = Path(content_path)
    
    print(f"\n{'='*70}")
    print(f"🎬 비디오 씬 생성: {scene_id}")
    print(f"{'='*70}")
    
    # 1. prompts.json에서 씬 정보 읽기
    if scene_id not in video_prompts_data:
        print(f"❌ {scene_id}가 video_prompts에 없습니다")
        return {'success': False, 'error': f'{scene_id} not found'}
    
    scene_data = video_prompts_data[scene_id]
    video_prompt = scene_data.get('video_prompt')
    reference_frame = scene_data.get('reference_frame')  # 예: assets/reel_frame_01.png
    
    if not video_prompt:
        print(f"❌ {scene_id}에 video_prompt가 없습니다")
        return {'success': False, 'error': 'No video_prompt'}
    
    print(f"  프롬프트: {video_prompt[:80]}...")
    print(f"  참조 프레임: {reference_frame}")
    print(f"  모델: {model_id} ({kling_mode if model_id == 'kling-v3' else 'N/A'})")
    print(f"  길이: {duration_seconds}초")
    
    # 2. 참조 프레임 로드 (옵션)
    reference_image_b64 = None
    if reference_frame:
        reference_frame_path = content_path / reference_frame
        if reference_frame_path.exists():
            try:
                reference_image_b64 = load_image_as_base64(reference_frame_path)
                print(f"  ✅ 참조 프레임 로드 완료")
            except Exception as e:
                print(f"  ⚠️  참조 프레임 로드 실패: {e}")
        else:
            print(f"  ⚠️  참조 프레임 없음: {reference_frame_path}")
    
    # 3. API 요청 데이터 구성
    request_data = {
        "prompt": video_prompt,
        "config": {
            "modelId": model_id,
            "durationSeconds": duration_seconds
        }
    }
    
    # Kling 전용 옵션
    if model_id == "kling-v3":
        request_data["config"]["klingMode"] = kling_mode
        if camera_movement:
            request_data["config"]["cameraMovement"] = camera_movement
    
    # 참조 이미지 추가
    if reference_image_b64:
        request_data["referenceImages"] = [reference_image_b64]
    
    # 4. Nanogen Video API 호출
    print("\n📡 Nanogen Video API 호출 중...")
    try:
        response = requests.post(
            f"{nanogen_url}/api/generate-video",
            json=request_data,
            timeout=30  # 초기 요청 타임아웃
        )
        response.raise_for_status()
        result = response.json()
        
        job_id = result.get('jobId')
        if not job_id:
            print("❌ jobId가 없습니다")
            return {'success': False, 'error': 'No jobId in response'}
        
        print(f"✅ 비디오 생성 작업 시작됨 (jobId: {job_id})")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return {'success': False, 'error': str(e)}
    
    # 5. 폴링 대기 (생성 완료까지)
    print(f"\n⏳ 비디오 생성 대기 중... (최대 {poll_timeout}초)")
    elapsed = 0
    
    while elapsed < poll_timeout:
        try:
            status_response = requests.get(
                f"{nanogen_url}/api/video-status/{job_id}",
                timeout=10
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data.get('status')
            progress = status_data.get('progress', 0)
            
            print(f"  [{elapsed:3d}s] 상태: {status} ({progress}%)", end='\r')
            
            if status == 'completed':
                video_url = status_data.get('url')
                if not video_url:
                    print(f"\n❌ 비디오 URL이 없습니다")
                    return {'success': False, 'error': 'No video URL'}
                
                print(f"\n✅ 비디오 생성 완료! ({elapsed}초 소요)")
                
                # 6. 결과 저장
                reels_dir = content_path / "reels" / "scenes"
                reels_dir.mkdir(parents=True, exist_ok=True)
                
                output_filename = f"{scene_id}.mp4"
                output_path = reels_dir / output_filename
                
                # 비디오 다운로드
                print(f"📥 비디오 다운로드 중...")
                video_response = requests.get(video_url, timeout=60)
                video_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(video_response.content)
                
                file_size = len(video_response.content) / 1024 / 1024
                print(f"✅ 저장 완료: {output_path}")
                print(f"📊 파일 크기: {file_size:.1f} MB")
                
                return {
                    'success': True,
                    'output_path': str(output_path),
                    'video_url': video_url,
                    'duration': elapsed,
                    'file_size_mb': file_size
                }
            
            elif status == 'failed':
                error_msg = status_data.get('error', 'Unknown error')
                print(f"\n❌ 비디오 생성 실패: {error_msg}")
                return {'success': False, 'error': error_msg}
            
            # 다음 폴링까지 대기
            time.sleep(poll_interval)
            elapsed += poll_interval
            
        except requests.exceptions.RequestException as e:
            print(f"\n❌ 폴링 요청 실패: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            print(f"\n❌ 예상치 못한 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    # 타임아웃
    print(f"\n❌ 타임아웃: {poll_timeout}초 내에 완료되지 않음")
    return {'success': False, 'error': f'Timeout after {poll_timeout}s'}


def generate_all_scenes(
    content_path,
    nanogen_url="http://localhost:8000",
    model_id="kling-v3",
    kling_mode="standard",
    duration_seconds=5,
    poll_timeout=300,
    poll_interval=5
):
    """
    prompts.json의 모든 비디오 씬 생성
    
    Args:
        content_path: 콘텐츠 작업 폴더
        nanogen_url: Nanogen 서버 URL
        model_id: 비디오 모델
        kling_mode: Kling 모드
        duration_seconds: 영상 길이
        poll_timeout: 폴링 타임아웃
        poll_interval: 폴링 간격
    
    Returns:
        dict: 전체 생성 결과 요약
    """
    
    content_path = Path(content_path)
    
    print(f"\n{'='*70}")
    print(f"🚀 전체 비디오 씬 생성 시작")
    print(f"{'='*70}")
    print(f"  콘텐츠 폴더: {content_path}")
    print(f"  모델: {model_id} ({kling_mode if model_id == 'kling-v3' else 'N/A'})")
    print(f"  길이: {duration_seconds}초")
    print()
    
    # 1. prompts.json 로드
    try:
        prompts_path = content_path / "prompts.json"
        
        if not prompts_path.exists():
            print(f"❌ prompts.json이 없습니다: {prompts_path}")
            return {'success': False, 'error': 'prompts.json not found'}
        
        prompts_data = load_json(prompts_path)
        video_prompts_data = prompts_data.get('video_prompts', {})
        
        if not video_prompts_data:
            print(f"❌ prompts.json에 video_prompts가 없습니다")
            return {'success': False, 'error': 'No video_prompts'}
        
        print(f"✅ prompts.json 로드 완료 ({len(video_prompts_data)}개 씬)")
        
    except Exception as e:
        print(f"❌ JSON 로드 실패: {e}")
        return {'success': False, 'error': str(e)}
    
    # 2. 씬별 생성
    results = {}
    success_count = 0
    fail_count = 0
    total_duration = 0
    total_size_mb = 0
    
    for scene_id in video_prompts_data.keys():
        result = generate_video_scene(
            content_path=content_path,
            scene_id=scene_id,
            video_prompts_data=video_prompts_data,
            nanogen_url=nanogen_url,
            model_id=model_id,
            kling_mode=kling_mode,
            duration_seconds=duration_seconds,
            poll_timeout=poll_timeout,
            poll_interval=poll_interval
        )
        
        results[scene_id] = result
        
        if result['success']:
            success_count += 1
            total_duration += result.get('duration', 0)
            total_size_mb += result.get('file_size_mb', 0)
        else:
            fail_count += 1
    
    # 3. 결과 요약
    print(f"\n{'='*70}")
    print(f"📊 전체 비디오 생성 완료")
    print(f"{'='*70}")
    print(f"  성공: {success_count}개")
    print(f"  실패: {fail_count}개")
    print(f"  총 {len(results)}개 씬")
    print(f"  총 생성 시간: {total_duration}초")
    print(f"  총 파일 크기: {total_size_mb:.1f} MB")
    print()
    
    if fail_count > 0:
        print("❌ 실패한 씬:")
        for scene_id, result in results.items():
            if not result['success']:
                print(f"  - {scene_id}: {result.get('error', 'Unknown')}")
    
    return {
        'success': fail_count == 0,
        'total': len(results),
        'success_count': success_count,
        'fail_count': fail_count,
        'total_duration': total_duration,
        'total_size_mb': total_size_mb,
        'details': results
    }


def main():
    parser = argparse.ArgumentParser(description='Nanogen 비디오 생성 자동화')
    parser.add_argument('--content-path', required=True, help='콘텐츠 작업 폴더 (예: content/20260306_spring_reels)')
    parser.add_argument('--scene-id', help='생성할 씬 ID (예: scene_01)')
    parser.add_argument('--all', action='store_true', help='모든 씬 생성')
    parser.add_argument('--nanogen-url', default='http://localhost:8000', help='Nanogen 서버 URL')
    parser.add_argument('--model-id', default='kling-v3', help='비디오 모델 (kling-v3, veo 등)')
    parser.add_argument('--kling-mode', default='standard', help='Kling 모드 (standard, pro)')
    parser.add_argument('--duration', type=int, default=5, help='영상 길이 (초)')
    parser.add_argument('--poll-timeout', type=int, default=300, help='폴링 타임아웃 (초)')
    parser.add_argument('--poll-interval', type=int, default=5, help='폴링 간격 (초)')
    
    args = parser.parse_args()
    
    if not args.scene_id and not args.all:
        print("❌ --scene-id 또는 --all 중 하나를 지정해야 합니다")
        return 1
    
    print("=" * 70)
    print("🤖 Nanogen 비디오 생성 자동화 (Video Agent)")
    print("=" * 70)
    print()
    
    if args.all:
        # 전체 씬 생성
        result = generate_all_scenes(
            content_path=args.content_path,
            nanogen_url=args.nanogen_url,
            model_id=args.model_id,
            kling_mode=args.kling_mode,
            duration_seconds=args.duration,
            poll_timeout=args.poll_timeout,
            poll_interval=args.poll_interval
        )
    else:
        # 단일 씬 생성
        content_path = Path(args.content_path)
        
        try:
            prompts_data = load_json(content_path / "prompts.json")
            video_prompts_data = prompts_data.get('video_prompts', {})
        except Exception as e:
            print(f"❌ JSON 로드 실패: {e}")
            return 1
        
        result = generate_video_scene(
            content_path=content_path,
            scene_id=args.scene_id,
            video_prompts_data=video_prompts_data,
            nanogen_url=args.nanogen_url,
            model_id=args.model_id,
            kling_mode=args.kling_mode,
            duration_seconds=args.duration,
            poll_timeout=args.poll_timeout,
            poll_interval=args.poll_interval
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
