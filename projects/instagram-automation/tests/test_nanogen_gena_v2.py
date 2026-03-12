#!/usr/bin/env python3
"""
Nanogen API 테스트 스크립트 v2 - Gena 캐릭터 일관성 검증

목표:
1. Gena 참조 이미지를 사용하여 기본 포즈 이미지 생성
2. 캐릭터 일관성 확인
"""

import os
import sys
import base64
from pathlib import Path

# 환경 변수 설정
os.environ['GEMINI_API_KEY'] = 'AIzaSyCIXMIBcdF1Nb0dJYkkFpVBxwSHg7qNNNc'
os.environ['IMAGE_MODEL_ID'] = 'gemini-3.1-flash-image-preview'

# Nanogen 프로젝트 경로 추가
nanogen_path = Path(__file__).parent.parent.parent / 'nanogen'
sys.path.insert(0, str(nanogen_path))

# Nanogen services import
from nanogen.services import generate_image_with_gemini

def load_image_as_data_uri(image_path):
    """이미지를 data URI로 변환"""
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/png;base64,{b64}"

def test_gena_generation():
    """Gena 참조 이미지로 기본 포즈 이미지 생성 테스트"""
    
    print("✅ Environment variables set")
    
    # 참조 이미지 경로
    ref_image_path = Path(__file__).parent / "shared/gena-references/gena_ref_01.png"
    
    if not ref_image_path.exists():
        print(f"❌ Reference image not found: {ref_image_path}")
        return False
    
    print(f"✅ Reference image loaded: {ref_image_path.name}")
    
    # 테스트 프롬프트
    prompt = """gena, 20s korean woman, wearing casual white t-shirt and blue jeans, 
standing on urban street in Seoul, afternoon golden hour, 
editorial fashion photography, full body shot, soft lighting, 
high quality, professional photography"""
    
    print(f"\n📝 Prompt:\n{prompt}")
    
    # 참조 이미지를 data URI로 변환
    ref_image_data_uri = load_image_as_data_uri(ref_image_path)
    
    print(f"\n✅ Reference image converted to data URI (length: {len(ref_image_data_uri)} chars)")
    
    # Config 설정
    config = {
        'modelId': 'gemini-3.1-flash-image-preview',
        'aspectRatio': '3:4',  # Instagram 최적 비율
        'resolution': '2K',
        'useGrounding': False
    }
    
    print(f"\n⚙️  Config: {config}")
    print("\n🎨 Generating image with Nanogen...")
    
    try:
        # Nanogen generate_image_with_gemini 함수 호출
        result = generate_image_with_gemini(
            prompt=prompt,
            config=config,
            reference_images=[ref_image_data_uri],
            mask_image=None
        )
        
        # 결과 저장
        output_dir = Path(__file__).parent / "test_output"
        output_dir.mkdir(exist_ok=True)
        
        if result and 'image_url' in result:
            output_path = output_dir / "gena_test_v2_01.png"
            
            # base64 디코딩하여 이미지 저장
            if result['image_url'].startswith('data:'):
                header, data = result['image_url'].split(',', 1)
                image_bytes = base64.b64decode(data)
                
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)
                
                print(f"\n✅ Image generated successfully!")
                print(f"📁 Saved to: {output_path}")
                print(f"📊 Image size: {len(image_bytes) / 1024:.1f} KB")
                return True
        else:
            print(f"\n❌ Unexpected result format: {result}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 Nanogen Gena Character Consistency Test v2")
    print("=" * 70)
    print()
    
    success = test_gena_generation()
    
    print()
    print("=" * 70)
    if success:
        print("✅ TEST PASSED")
        print("\n다음 단계:")
        print("1. test_output/gena_test_v2_01.png 확인")
        print("2. 참조 이미지(gena_ref_01.png)와 생성 이미지 비교")
        print("3. 캐릭터 일관성 육안 검증:")
        print("   - 얼굴 특징 일치 여부")
        print("   - 피부톤 일치 여부")
        print("   - 전체적인 인물 동일성")
        print("4. 통과하면 다른 참조 이미지(02~08)도 테스트")
        print("5. 모두 통과하면 Outfit Swap 2단계 테스트 진행")
    else:
        print("❌ TEST FAILED")
        print("\n문제 해결:")
        print("1. Nanogen 프로젝트 경로 확인")
        print("2. GEMINI_API_KEY 유효성 확인")
        print("3. API 할당량 확인")
        print("4. 참조 이미지 파일 확인")
    print("=" * 70)
