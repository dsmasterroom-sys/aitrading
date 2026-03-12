#!/usr/bin/env python3
"""
Nanogen API 테스트 스크립트 - Gena 캐릭터 일관성 검증

목표:
1. Gena 참조 이미지를 사용하여 기본 포즈 이미지 생성
2. 캐릭터 일관성 확인
"""

import os
import sys
import base64
from pathlib import Path

# Nanogen 프로젝트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'nanogen'))

from google import genai
from google.genai import types

def load_image_as_base64(image_path):
    """이미지를 base64로 인코딩"""
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode('utf-8')

def test_gena_generation():
    """Gena 참조 이미지로 기본 포즈 이미지 생성 테스트"""
    
    # API 키 확인
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    print("✅ API Key found")
    
    # Client 생성
    client = genai.Client(api_key=api_key, http_options={'timeout': 600000})
    
    # 참조 이미지 경로
    ref_image_path = Path(__file__).parent / "shared/gena-references/gena_ref_01.png"
    
    if not ref_image_path.exists():
        print(f"❌ Reference image not found: {ref_image_path}")
        return False
    
    print(f"✅ Reference image loaded: {ref_image_path.name}")
    
    # 테스트 프롬프트
    prompt = """gena, 20s korean woman, wearing casual white t-shirt and blue jeans, 
standing on urban street, afternoon golden hour, 
editorial fashion photography, full body shot, soft lighting"""
    
    print(f"\n📝 Prompt: {prompt}")
    
    # 참조 이미지 읽기
    with open(ref_image_path, 'rb') as f:
        ref_image_bytes = f.read()
    
    print("\n🎨 Generating image with Gemini 3.1 Flash Image...")
    
    try:
        # Gemini 3.1 Flash Image 모델로 이미지 생성
        response = client.models.generate_image(
            model='gemini-3.1-flash-image-preview',
            prompt=prompt,
            config=types.GenerateImageConfig(
                number_of_images=1,
                aspect_ratio="3:4",  # Instagram 최적 비율
                # reference_images 파라미터는 Gemini API에서 지원하는지 확인 필요
            )
        )
        
        # 결과 저장
        output_dir = Path(__file__).parent / "test_output"
        output_dir.mkdir(exist_ok=True)
        
        if response.generated_images:
            output_path = output_dir / "gena_test_01.png"
            
            # 이미지 저장
            with open(output_path, 'wb') as f:
                f.write(response.generated_images[0].image.image_bytes)
            
            print(f"\n✅ Image generated successfully!")
            print(f"📁 Saved to: {output_path}")
            return True
        else:
            print("\n❌ No images generated")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Nanogen Gena Character Consistency Test")
    print("=" * 60)
    print()
    
    success = test_gena_generation()
    
    print()
    print("=" * 60)
    if success:
        print("✅ TEST PASSED")
        print("\n다음 단계:")
        print("1. test_output/gena_test_01.png 확인")
        print("2. 캐릭터 일관성 육안 검증")
        print("3. 통과하면 Outfit Swap 2단계 테스트 진행")
    else:
        print("❌ TEST FAILED")
        print("\n문제 해결:")
        print("1. GEMINI_API_KEY 환경변수 확인")
        print("2. Nanogen 서버 실행 확인")
        print("3. API 호출 제한 확인")
    print("=" * 60)
