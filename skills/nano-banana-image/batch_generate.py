#!/usr/bin/env python3
"""
Imagen Batch Image Generation
여러 프롬프트로 이미지를 배치 생성 (새 SDK 사용)
"""

import os
import sys
import argparse
import json
from pathlib import Path
from generate_image import generate_image


def load_prompts(prompt_file):
    """
    프롬프트 파일 로드
    
    지원 형식:
    - TXT: 한 줄에 하나씩
    - JSON: [{"prompt": "...", "negative_prompt": "...", "aspect_ratio": "..."}, ...]
    """
    filepath = Path(prompt_file)
    
    if not filepath.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {prompt_file}")
        sys.exit(1)
    
    # JSON 파일
    if filepath.suffix.lower() == ".json":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        else:
            print("❌ JSON 파일은 배열 형식이어야 합니다.")
            sys.exit(1)
    
    # TXT 파일
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        return [{"prompt": line} for line in lines]


def batch_generate(
    prompt_file: str,
    output_dir: str = "./batch_output",
    aspect_ratio: str = "1:1",
    negative_prompt: str = "",
    model: str = "gemini-3.1-flash-image-preview"
):
    """
    배치 이미지 생성
    
    Args:
        prompt_file: 프롬프트 파일 경로 (TXT 또는 JSON)
        output_dir: 출력 디렉토리
        aspect_ratio: 기본 가로세로 비율
        negative_prompt: 기본 negative prompt
        model: 사용할 모델
    """
    prompts = load_prompts(prompt_file)
    
    print(f"📝 총 {len(prompts)}개 프롬프트 로드")
    print(f"📁 출력 위치: {output_dir}\n")
    
    results = []
    
    for idx, item in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(prompts)}] 생성 중...")
        print(f"{'='*60}")
        
        # 프롬프트 파싱
        if isinstance(item, dict):
            prompt = item.get("prompt", "")
            item_aspect_ratio = item.get("aspect_ratio", aspect_ratio)
            item_negative_prompt = item.get("negative_prompt", negative_prompt)
            item_model = item.get("model", model)
        else:
            prompt = str(item)
            item_aspect_ratio = aspect_ratio
            item_negative_prompt = negative_prompt
            item_model = model
        
        # 개별 출력 디렉토리
        item_output_dir = Path(output_dir) / f"prompt_{idx:03d}"
        
        # 이미지 생성
        files = generate_image(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio=item_aspect_ratio,
            negative_prompt=item_negative_prompt,
            output_dir=str(item_output_dir),
            model=item_model
        )
        
        results.append({
            "index": idx,
            "prompt": prompt,
            "success": len(files) > 0,
            "files": files
        })
    
    # 전체 결과 저장
    summary_file = Path(output_dir) / "batch_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 통계 출력
    success_count = sum(1 for r in results if r["success"])
    
    print(f"\n{'='*60}")
    print(f"🎉 배치 생성 완료!")
    print(f"{'='*60}")
    print(f"✅ 성공: {success_count}/{len(prompts)}")
    print(f"❌ 실패: {len(prompts) - success_count}/{len(prompts)}")
    print(f"📋 요약 파일: {summary_file}")
    

def main():
    parser = argparse.ArgumentParser(
        description="Imagen 배치 이미지 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
프롬프트 파일 형식:

TXT 파일 (prompts.txt):
  A beautiful sunset
  A cute cat
  A modern office
  # 주석도 가능

JSON 파일 (prompts.json):
  [
    {
      "prompt": "A beautiful sunset",
      "aspect_ratio": "16:9",
      "negative_prompt": "blurry"
    },
    {
      "prompt": "A cute cat",
      "model": "imagen-4.0-generate-001"
    }
  ]

예시:
  %(prog)s prompts.txt
  %(prog)s prompts.json --output-dir ./instagram_images
  %(prog)s prompts.txt --aspect-ratio 16:9 --negative-prompt "low quality"
        """
    )
    
    parser.add_argument(
        "prompt_file",
        help="프롬프트 파일 (TXT 또는 JSON)"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="./batch_output",
        help="출력 디렉토리 (기본: ./batch_output)"
    )
    
    parser.add_argument(
        "-a", "--aspect-ratio",
        default="1:1",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        help="기본 가로세로 비율 (기본: 1:1)"
    )
    
    parser.add_argument(
        "-np", "--negative-prompt",
        default="",
        help="기본 negative prompt"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="imagen-4.0-generate-001",
        help="사용할 모델 (기본: imagen-4.0-generate-001)"
    )
    
    args = parser.parse_args()
    
    batch_generate(
        prompt_file=args.prompt_file,
        output_dir=args.output_dir,
        aspect_ratio=args.aspect_ratio,
        negative_prompt=args.negative_prompt,
        model=args.model
    )


if __name__ == "__main__":
    main()
