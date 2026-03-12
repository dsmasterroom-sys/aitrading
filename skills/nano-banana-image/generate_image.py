#!/usr/bin/env python3
"""
Nano Banana Image Generation Script
Google Imagen 4.0 API를 사용한 이미지 생성 (새 SDK 사용)
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai 라이브러리가 필요합니다.")
    print("설치: pip3 install google-genai")
    sys.exit(1)


def setup_client():
    """API 클라이언트 설정"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY 또는 GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("\n설정 방법:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        print("\nAPI 키 발급:")
        print("  - Google AI Studio: https://aistudio.google.com/")
        print("  - Google Cloud Console: https://console.cloud.google.com/")
        sys.exit(1)
    
    return genai.Client(api_key=api_key)


def generate_image(
    prompt: str,
    number_of_images: int = 1,
    aspect_ratio: str = "1:1",
    negative_prompt: str = "",
    output_dir: str = "./output",
    model: str = "gemini-3.1-flash-image-preview"
):
    """
    이미지 생성 및 저장
    
    Args:
        prompt: 이미지 설명 프롬프트
        number_of_images: 생성할 이미지 수 (1-4)
        aspect_ratio: 가로세로 비율 (1:1, 16:9, 4:3 등)
        negative_prompt: 제외할 요소
        output_dir: 출력 디렉토리
        model: 사용할 모델
    
    Returns:
        생성된 이미지 파일 경로 리스트
    """
    client = setup_client()
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🎨 이미지 생성 중...")
    print(f"   프롬프트: {prompt}")
    print(f"   개수: {number_of_images}")
    print(f"   비율: {aspect_ratio}")
    print(f"   모델: {model}")
    
    try:
        # Imagen 4.0 사용
        config_kwargs = {
            "number_of_images": number_of_images,
            "aspect_ratio": aspect_ratio,
            "output_mime_type": "image/png",
        }
        
        if negative_prompt:
            config_kwargs["negative_prompt"] = negative_prompt
            print(f"   제외: {negative_prompt}")
        
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(**config_kwargs),
        )
        
        # 결과 처리
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if response.generated_images:
            for idx, generated_image in enumerate(response.generated_images):
                # 파일명 생성
                filename = f"image_{timestamp}_{idx+1}.png"
                filepath = output_path / filename
                
                # 이미지 저장
                generated_image.image.save(filepath)
                saved_files.append(str(filepath))
                
                # 메타데이터 출력
                print(f"\n✅ 생성 완료: {filename}")
                if hasattr(generated_image, 'rai_filtered_reason') and generated_image.rai_filtered_reason:
                    print(f"   ⚠️  필터링: {generated_image.rai_filtered_reason}")
            
            # 메타데이터 JSON 저장
            metadata = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "aspect_ratio": aspect_ratio,
                "number_of_images": number_of_images,
                "model": model,
                "timestamp": timestamp,
                "images": [
                    {
                        "filename": Path(f).name,
                    }
                    for f in saved_files
                ]
            }
            
            metadata_file = output_path / f"metadata_{timestamp}.json"
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"\n📋 메타데이터 저장: {metadata_file}")
            
            return saved_files
        else:
            print("❌ 이미지가 생성되지 않았습니다.")
            return []
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Imagen 4.0 이미지 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s "A cute cat wearing a hat"
  %(prog)s "Futuristic city" --aspect-ratio 16:9 --number 2
  %(prog)s "Portrait" --negative-prompt "blurry, ugly"
        """
    )
    
    parser.add_argument(
        "prompt",
        help="이미지 생성 프롬프트"
    )
    
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="생성할 이미지 수 (기본: 1)"
    )
    
    parser.add_argument(
        "-a", "--aspect-ratio",
        default="1:1",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        help="가로세로 비율 (기본: 1:1)"
    )
    
    parser.add_argument(
        "-np", "--negative-prompt",
        default="",
        help="제외할 요소 (예: 'blurry, low quality')"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="./output",
        help="출력 디렉토리 (기본: ./output)"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="imagen-4.0-generate-001",
        help="사용할 모델 (기본: imagen-4.0-generate-001)"
    )
    
    args = parser.parse_args()
    
    # 이미지 생성
    files = generate_image(
        prompt=args.prompt,
        number_of_images=args.number,
        aspect_ratio=args.aspect_ratio,
        negative_prompt=args.negative_prompt,
        output_dir=args.output_dir,
        model=args.model
    )
    
    if files:
        print(f"\n🎉 총 {len(files)}개 이미지 생성 완료!")
        print(f"📁 저장 위치: {args.output_dir}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
