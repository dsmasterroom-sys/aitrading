#!/usr/bin/env python3
"""
FFmpeg 릴스 자막 오버레이 + 씬 결합

목표:
- 각 씬에 자막 추가
- 씬 결합 (5초 릴스)
- 9:16 비율 확인
- 1080×1920px 해상도

사용법:
    python scripts/ffmpeg_assemble_reels.py \
        --content-path content/20260306_spring_reels
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_json(file_path):
    """JSON 파일 로드"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_subtitle_to_scene(
    input_video, 
    output_video, 
    subtitle_text, 
    font_size=60, 
    font_color="white", 
    font_file=None,
    position="bottom"
):
    """
    단일 씬에 자막 추가
    
    Args:
        input_video: 입력 비디오 경로
        output_video: 출력 비디오 경로
        subtitle_text: 자막 텍스트
        font_size: 폰트 크기
        font_color: 폰트 색상
        font_file: 폰트 파일 (예: /System/Library/Fonts/Supplemental/Arial.ttf)
        position: 자막 위치 (top, center, bottom)
    
    Returns:
        bool: 성공 여부
    """
    
    print(f"  자막 추가 중: {subtitle_text[:30]}...")
    
    # 자막 위치 계산
    if position == "top":
        y_position = "100"
    elif position == "center":
        y_position = "(h-text_h)/2"
    else:  # bottom
        y_position = "h-150"
    
    # FFmpeg drawtext 필터
    drawtext_filter = (
        f"drawtext="
        f"text='{subtitle_text}':"
        f"fontsize={font_size}:"
        f"fontcolor={font_color}:"
        f"x=(w-text_w)/2:"  # 가로 중앙
        f"y={y_position}:"
        f"borderw=3:"  # 텍스트 아웃라인
        f"bordercolor=black"
    )
    
    # 폰트 파일 지정 (옵션)
    if font_file:
        drawtext_filter += f":fontfile='{font_file}'"
    
    # FFmpeg 명령어 실행
    cmd = [
        "ffmpeg",
        "-i", str(input_video),
        "-vf", drawtext_filter,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "copy",  # 오디오 복사 (있으면)
        "-y",  # 덮어쓰기
        str(output_video)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"  ✅ 자막 추가 완료: {output_video}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ FFmpeg 오류: {e.stderr}")
        return False


def concatenate_scenes(scene_videos, output_video, resolution="1080x1920"):
    """
    여러 씬 비디오 결합
    
    Args:
        scene_videos: 씬 비디오 경로 리스트 (순서대로)
        output_video: 출력 비디오 경로
        resolution: 최종 해상도 (WxH)
    
    Returns:
        bool: 성공 여부
    """
    
    print(f"\n📹 {len(scene_videos)}개 씬 결합 중...")
    
    # concat 필터 입력 파일 리스트 생성
    filelist_path = output_video.parent / "filelist.txt"
    
    with open(filelist_path, 'w') as f:
        for video in scene_videos:
            f.write(f"file '{video.resolve()}'\n")
    
    print(f"  Filelist: {filelist_path}")
    
    # FFmpeg concat 명령어
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(filelist_path),
        "-vf", f"scale={resolution}",  # 해상도 강제
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",  # 오디오 인코딩 (있으면)
        "-y",
        str(output_video)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ 씬 결합 완료: {output_video}")
        
        # filelist.txt 삭제
        filelist_path.unlink()
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg 오류: {e.stderr}")
        return False


def process_reels(
    content_path,
    font_size=60,
    font_color="white",
    font_file=None,
    subtitle_position="bottom",
    resolution="1080x1920"
):
    """
    릴스 전체 처리 (자막 + 결합)
    
    Args:
        content_path: 콘텐츠 작업 폴더
        font_size: 폰트 크기
        font_color: 폰트 색상
        font_file: 폰트 파일
        subtitle_position: 자막 위치
        resolution: 최종 해상도
    
    Returns:
        dict: 처리 결과
    """
    
    content_path = Path(content_path)
    
    print(f"\n{'='*70}")
    print(f"🎬 릴스 자막 오버레이 + 씬 결합")
    print(f"{'='*70}")
    print(f"  콘텐츠 폴더: {content_path}")
    print()
    
    # 1. copy.md 로드 (자막 텍스트)
    copy_path = content_path / "copy.md"
    
    if not copy_path.exists():
        print(f"❌ copy.md가 없습니다: {copy_path}")
        return {'success': False, 'error': 'copy.md not found'}
    
    try:
        copy_content = copy_path.read_text(encoding='utf-8')
        print(f"✅ copy.md 로드 완료")
    except Exception as e:
        print(f"❌ copy.md 로드 실패: {e}")
        return {'success': False, 'error': str(e)}
    
    # 2. scenes.json 로드 (씬 정보)
    scenes_path = content_path / "scenes.json"
    
    if not scenes_path.exists():
        print(f"❌ scenes.json이 없습니다: {scenes_path}")
        return {'success': False, 'error': 'scenes.json not found'}
    
    try:
        scenes_data = load_json(scenes_path)
        print(f"✅ scenes.json 로드 완료 ({len(scenes_data)}개 씬)")
    except Exception as e:
        print(f"❌ scenes.json 로드 실패: {e}")
        return {'success': False, 'error': str(e)}
    
    # 3. 씬 비디오 경로 확인
    scenes_dir = content_path / "reels" / "scenes"
    
    if not scenes_dir.exists():
        print(f"❌ 씬 폴더가 없습니다: {scenes_dir}")
        return {'success': False, 'error': 'Scenes folder not found'}
    
    scene_videos = sorted(scenes_dir.glob("scene_*.mp4"))
    
    if not scene_videos:
        print(f"❌ 씬 비디오가 없습니다: {scenes_dir}")
        return {'success': False, 'error': 'No scene videos'}
    
    print(f"✅ {len(scene_videos)}개 씬 비디오 발견")
    print()
    
    # 4. 각 씬에 자막 추가
    print(f"📝 자막 추가 중...")
    
    subtitled_dir = scenes_dir.parent / "subtitled"
    subtitled_dir.mkdir(exist_ok=True)
    
    subtitled_videos = []
    
    # copy.md에서 씬별 자막 추출 (간단히 줄바꿈으로 분리)
    # 실제로는 scenes.json에 자막 정보가 있으면 더 좋음
    subtitle_lines = [line.strip() for line in copy_content.split('\n') if line.strip()]
    
    for i, scene_video in enumerate(scene_videos):
        scene_id = scene_video.stem  # 예: scene_01
        
        # 자막 텍스트 (copy.md의 해당 줄, 없으면 빈 문자열)
        subtitle_text = subtitle_lines[i] if i < len(subtitle_lines) else ""
        
        if not subtitle_text:
            # 자막 없으면 원본 그대로 복사
            subtitled_video = subtitled_dir / f"{scene_id}_subtitled.mp4"
            import shutil
            shutil.copy(scene_video, subtitled_video)
            subtitled_videos.append(subtitled_video)
            print(f"  [{i+1}/{len(scene_videos)}] {scene_id}: 자막 없음 (원본 복사)")
            continue
        
        subtitled_video = subtitled_dir / f"{scene_id}_subtitled.mp4"
        
        print(f"  [{i+1}/{len(scene_videos)}] {scene_id}")
        
        success = add_subtitle_to_scene(
            input_video=scene_video,
            output_video=subtitled_video,
            subtitle_text=subtitle_text,
            font_size=font_size,
            font_color=font_color,
            font_file=font_file,
            position=subtitle_position
        )
        
        if success:
            subtitled_videos.append(subtitled_video)
        else:
            print(f"  ⚠️  자막 추가 실패, 원본 사용")
            subtitled_videos.append(scene_video)
    
    # 5. 씬 결합
    final_output = content_path / "reels" / "final_reel.mp4"
    
    success = concatenate_scenes(
        scene_videos=subtitled_videos,
        output_video=final_output,
        resolution=resolution
    )
    
    if not success:
        return {'success': False, 'error': 'Concatenation failed'}
    
    # 6. 결과 확인
    file_size_mb = final_output.stat().st_size / 1024 / 1024
    
    print()
    print(f"{'='*70}")
    print(f"✅ 릴스 처리 완료!")
    print(f"{'='*70}")
    print(f"  출력: {final_output}")
    print(f"  크기: {file_size_mb:.1f} MB")
    print()
    
    return {
        'success': True,
        'output_path': str(final_output),
        'file_size_mb': file_size_mb,
        'scene_count': len(subtitled_videos)
    }


def main():
    parser = argparse.ArgumentParser(description='FFmpeg 릴스 자막 오버레이 + 씬 결합')
    parser.add_argument('--content-path', required=True, help='콘텐츠 작업 폴더 (예: content/20260306_spring_reels)')
    parser.add_argument('--font-size', type=int, default=60, help='폰트 크기 (기본: 60)')
    parser.add_argument('--font-color', default='white', help='폰트 색상 (기본: white)')
    parser.add_argument('--font-file', help='폰트 파일 경로 (옵션)')
    parser.add_argument('--subtitle-position', default='bottom', help='자막 위치 (top, center, bottom)')
    parser.add_argument('--resolution', default='1080x1920', help='최종 해상도 (기본: 1080x1920)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🤖 FFmpeg 릴스 자막 오버레이 + 씬 결합")
    print("=" * 70)
    print()
    
    result = process_reels(
        content_path=args.content_path,
        font_size=args.font_size,
        font_color=args.font_color,
        font_file=args.font_file,
        subtitle_position=args.subtitle_position,
        resolution=args.resolution
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
