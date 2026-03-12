---
name: design-nanogen-image
agent: designer
description: "Nanogen API로 AI 이미지 생성. Reference 이미지 필수 첨부 + 체크리스트 검증 + 1장씩 생성 보고."
input: "weekly/image-prompts.json"
output: "assets/output/W##-##-{format}/*.png"
---

# design-nanogen-image SKILL

## 역할

Nanogen API를 사용하여 **인스타그램 게시물 이미지**를 생성하는 Designer 전용 스킬입니다.

**중요**: 이미지 생성 = 과금 발생 → 반드시 체크리스트 검증 + 승인 후 실행

## 필수 전제 조건

### 1. 체크리스트 확인 (IMAGE_GENERATION_CHECKLIST.md)
이미지 생성 전 **반드시** 체크리스트를 먼저 읽고 4단계 검증을 완료해야 합니다.

```bash
# 체크리스트 읽기
cat IMAGE_GENERATION_CHECKLIST.md
```

### 2. 마보스님 최종 승인
- [ ] 생성할 게시물 확정 (1개만!)
- [ ] 총 이미지 개수 확정 (릴스 6장 / 캐러셀 7-9장)
- [ ] 예상 과금 비용 확인
- [ ] **승인 완료** ✅

승인 없이 생성 시작 금지!

## Reference 이미지 자동 포함 규칙

모든 이미지 생성 시 **반드시** Reference를 첨부해야 합니다.

### 필수 Reference (모든 이미지)
```python
reference_images = []

# 1. 인물 일관성 (필수)
gena_refs = [
    "assets/gena_hair (1).png",
    "assets/gena_hair (2).png", 
    "assets/gena_hair (3).png"
]
for ref in gena_refs:
    reference_images.append(load_image_as_base64(ref))
```

### 조건부 Reference

#### 제품 등장 씬 (slant bag)
```python
# 제품 참조 추가
if "slant" in prompt or "sling bag" in prompt:
    product_refs = [
        "assets/slant_4-view.png",
        "assets/slant-produact.png"
    ]
    for ref in product_refs:
        reference_images.append(load_image_as_base64(ref))
```

#### 의상 참조 (outfit grid 사용 시)
```python
# image-prompts.json의 outfit_reference 설정 확인
if config.get("outfit_reference", {}).get("enabled"):
    outfit_mode = config["outfit_reference"]["mode"]
    
    if outfit_mode == "latest":
        count = config["outfit_reference"]["count"]
        outfit_files = get_latest_outfit_files(count)
    elif outfit_mode == "specific":
        outfit_files = config["outfit_reference"]["specific_files"]
    
    for outfit_file in outfit_files:
        reference_images.append(load_image_as_base64(f"assets/outfit/{outfit_file}"))
```

## Nanogen API 호출 형식

### Endpoint
```
POST http://localhost:8000/api/generate
```

### Request Body
```json
{
  "prompt": "프롬프트 텍스트 (image-prompts.json에서 가져옴)",
  "config": {
    "modelId": "gemini-3-pro-image-preview",
    "aspectRatio": "4:5",  // 릴스 6장: "9:16", 캐러셀: "4:5"
    "resolution": "1K"
  },
  "referenceImages": [
    "data:image/png;base64,iVBORw0KGgo...",  // gena_hair (1)
    "data:image/png;base64,iVBORw0KGgo...",  // gena_hair (2)
    "data:image/png;base64,iVBORw0KGgo...",  // gena_hair (3)
    "data:image/png;base64,iVBORw0KGgo..."   // slant (해당 시)
  ]
}
```

### Response
```json
{
  "url": "data:image/png;base64,iVBORw0KGgo...",
  "saved_image": {
    "id": 123,
    "url": "/media/generated_abc123.png"
  }
}
```

## 생성 프로세스 (1장씩)

### 1단계: 준비
```python
import requests
import json
import base64
from datetime import datetime

BASE_URL = "http://localhost:8000"
prompts = load_prompts("weekly/image-prompts.json")
content_id = prompts["slides"][0]["content_id"]  # 예: "W10-01-reels"
output_dir = f"assets/output/{content_id}"
os.makedirs(output_dir, exist_ok=True)
```

### 2단계: 1장씩 생성 + 보고
```python
for slide in prompts["slides"][0]["slides"]:
    slide_num = slide["slide"]
    prompt = slide["prompt"]
    
    # Reference 이미지 준비
    reference_images = prepare_references(slide, prompts)
    
    # 사용자에게 보고
    print(f"\n[Slide {slide_num}] 생성 중...")
    print(f"프롬프트: {prompt[:100]}...")
    print(f"Reference: {len(reference_images)}개")
    
    # API 호출
    response = requests.post(
        f"{BASE_URL}/api/generate",
        json={
            "prompt": prompt,
            "config": {
                "modelId": "gemini-3-pro-image-preview",
                "aspectRatio": "4:5"  # or "9:16" for reels
            },
            "referenceImages": reference_images
        },
        timeout=300
    )
    
    if response.status_code == 200:
        result = response.json()
        url = result.get("url", "")
        
        # Base64 이미지 저장
        if url.startswith("data:image"):
            header, data = url.split(",", 1)
            ext = "png" if "png" in header else "jpg"
            filename = f"{output_dir}/slide-S{slide_num}.{ext}"
            
            with open(filename, "wb") as f:
                f.write(base64.b64decode(data))
            
            print(f"✅ 저장: {filename}")
            
            # 중간 확인 요청 (2-3장마다)
            if slide_num % 2 == 0:
                print(f"\n⏸️  {slide_num}장 생성 완료. 계속 진행할까요?")
                # 오케스트레이터에게 보고 → 마보스님 확인 대기
                return  # 승인 후 재실행
        else:
            print(f"❌ 이미지 생성 실패")
    else:
        print(f"❌ HTTP {response.status_code}")
```

### 3단계: 완료 보고
```python
print(f"\n{'='*50}")
print(f"🎬 {content_id} 이미지 생성 완료!")
print(f"📁 경로: {output_dir}")
print(f"📊 총 {len(slides)}장 생성")
print(f"💰 예상 과금: {len(slides)} 이미지")
print(f"{'='*50}")
```

## 자기검증 체크리스트

생성 실행 전:
- [ ] IMAGE_GENERATION_CHECKLIST.md 4단계 모두 확인
- [ ] 마보스님 최종 승인 받음
- [ ] Reference 이미지 3개 이상 포함 (gena_hair 필수)
- [ ] 제품 등장 씬은 slant 참조 포함
- [ ] 1개 게시물만 생성 (일괄 생성 금지)

생성 중:
- [ ] 1장씩 생성 후 결과 확인
- [ ] 2-3장마다 중간 보고
- [ ] 오류 발생 시 즉시 중단 및 보고

생성 후:
- [ ] 인물 일관성 확인
- [ ] 제품 일관성 확인 (해당 시)
- [ ] 총 과금 개수 리포트
- [ ] output 경로 확인

## 금지 사항

- ❌ 체크리스트 없이 생성 시작
- ❌ Reference 이미지 누락
- ❌ 일괄 생성 (여러 게시물 동시 생성)
- ❌ 승인 없이 계속 진행
- ❌ 과금 개수 보고 누락
- ❌ 카피 작성, HTML 생성, QA 검증 (타 Agent 영역)

## 오케스트레이터 연동

Designer가 이미지 생성 완료 시:
1. 생성 결과 리포트 전달
2. 인물/제품 일관성 체크 요청
3. QA Agent에게 이미지 검증 의뢰

---

**핵심**: Reference 없는 이미지 = 일관성 없음 = 사용 불가 = 과금 낭비
