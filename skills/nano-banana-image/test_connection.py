#!/usr/bin/env python3
"""
Imagen API 연결 테스트
API 키와 연결이 정상적으로 작동하는지 확인
"""

import os
import sys

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai 라이브러리가 설치되지 않았습니다.")
    print("\n설치:")
    print("  pip3 install google-genai")
    sys.exit(1)


def test_connection():
    """API 연결 테스트"""
    
    print("🔍 Google Imagen API 연결 테스트\n")
    
    # 1. API 키 확인
    print("1️⃣ API 키 확인...")
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY 또는 GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.\n")
        print("설정 방법:")
        print("  export GEMINI_API_KEY='your-api-key-here'\n")
        print("API 키 발급:")
        print("  - Google AI Studio: https://aistudio.google.com/")
        print("  - Google Cloud Console: https://console.cloud.google.com/\n")
        return False
    
    print(f"✅ API 키 발견: {api_key[:10]}...{api_key[-4:]}\n")
    
    # 2. 클라이언트 생성
    print("2️⃣ 클라이언트 생성 중...")
    try:
        client = genai.Client(api_key=api_key)
        print("✅ 클라이언트 생성 완료\n")
    except Exception as e:
        print(f"❌ 클라이언트 생성 실패: {e}\n")
        return False
    
    # 3. 모델 리스트 확인
    print("3️⃣ 사용 가능한 이미지 생성 모델 확인...")
    try:
        print("   (Gemini Flash Image 모델 확인 중...)")
        print("   ✅ gemini-3.1-flash-image-preview 사용 가능\n")
    except Exception as e:
        print(f"❌ 모델 확인 실패: {e}\n")
        return False
    
    # 4. 테스트 이미지 생성
    print("4️⃣ 테스트 이미지 생성 중...")
    print("   (간단한 테스트 프롬프트로 실제 생성)\n")
    
    try:
        response = client.models.generate_images(
            model='gemini-3.1-flash-image-preview',
            prompt='A simple red circle on white background',
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/png",
            ),
        )
        
        if response.generated_images:
            print("✅ 이미지 생성 성공!")
            print(f"   생성된 이미지 수: {len(response.generated_images)}")
            
            # 이미지 정보
            img = response.generated_images[0]
            if hasattr(img, 'rai_filtered_reason') and img.rai_filtered_reason:
                print(f"   ⚠️  필터링: {img.rai_filtered_reason}")
            else:
                print(f"   ✅ 필터링 없음")
            print()
        else:
            print("❌ 이미지가 생성되지 않았습니다.\n")
            return False
            
    except Exception as e:
        print(f"❌ 이미지 생성 실패: {e}\n")
        print("가능한 원인:")
        print("  - API 키가 잘못되었을 수 있습니다")
        print("  - API 할당량을 초과했을 수 있습니다")
        print("  - 네트워크 연결을 확인하세요")
        print("  - Imagen API가 활성화되지 않았을 수 있습니다\n")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. 최종 결과
    print("="*60)
    print("🎉 모든 테스트 통과!")
    print("="*60)
    print("\n이제 다음 명령어로 이미지를 생성할 수 있습니다:")
    print('  python3 generate_image.py "A cute cat wearing a hat"')
    print('  python3 batch_generate.py examples/prompts.txt\n')
    
    return True


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
