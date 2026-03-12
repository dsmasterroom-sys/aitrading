# design-visual.SKILL.md

**용도**: Nanogen 이미지 생성 실행 규칙  
**사용 에이전트**: designer  
**버전**: 1.0

---

## 📥 입력

- prompts.json (prompt-engineer 산출물)
- items.json (제품 이미지 URL)
- shared/gena-master-prompt.md

---

## 📤 출력

- assets/{content_type}_{slide_id}.png
- 해상도: 1080×1440px (3:4) 또는 지정된 비율

---

## 🔧 실행 흐름

### 1단계: 참조 이미지 준비

```python
# prompts.json에서 읽기
gena_ref = prompts["slide_02"]["reference_images"][0]  # gena_ref_04.png
item_id = prompts["slide_02"]["reference_images"][1]   # items.json > top_001

# items.json에서 제품 이미지 URL 가져오기
garment_url = items.json[item_id]["ref_image_url"]
```

### 2단계: Nanogen Outfit Swap 호출

**스크립트 사용**:
```bash
python scripts/nanogen_outfit_swap.py \
  --gena-ref shared/gena-references/{gena_ref} \
  --garment {garment_url 다운로드 경로} \
  --output assets/{output_filename}.png \
  --aspect-ratio 3:4 \
  --resolution 2K
```

**API 직접 호출 (선택)**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate",
    json={
        "prompt": "의상교체",
        "config": {
            "modelId": "gemini-3.1-flash-image-preview",
            "aspectRatio": "3:4",
            "resolution": "2K"
        },
        "referenceImages": [
            gena_ref_base64,
            garment_base64
        ]
    }
)
```

### 3단계: 결과 저장

**파일명 규칙**:
- 캐러셀: `carousel_slide_{번호}.png`
- 릴스: `reel_frame_{번호}.png`
- 스토리: `story_{번호}.png`

**저장 위치**:
```
content/YYYYMMDD_series_name/
  └── assets/
      ├── carousel_slide_01.png
      ├── carousel_slide_02.png
      └── ...
```

---

## ✅ 자기검증 체크리스트

생성 완료 후 **모두 확인**:

### 캐릭터 일관성 (최우선)

#### [ ] 1. 동일인 인식
- 참조 이미지와 명확히 같은 사람으로 보임
- **실패 시**: 즉시 재생성

#### [ ] 2. 피부톤 일치
- 밝은 웜톤 유지
- 색온도 편차 ±10% 이내

#### [ ] 3. 헤어 스타일
- 참조 이미지의 헤어스타일 유지
- 길이/컬/색상 일치

#### [ ] 4. 얼굴 비율
- 타원형 얼굴형
- 눈/코/입 위치 일관성

### 아이템 정확성

#### [ ] 5. 색상 일치
- items.json의 color 필드와 시각적 일치
- RGB 편차 ±15% 이내

#### [ ] 6. 핏/디테일 일치
- visual_desc의 특징 반영
- 예: "오버사이즈" → 실제 루즈핏으로 보임

#### [ ] 7. 제품 동일성
- ref_image_url의 제품과 같은 아이템
- 브랜드/스타일 명확히 일치

### 기술 품질

#### [ ] 8. 해상도
- 1080×1440px (3:4) 또는 지정 비율
- 2K 품질 (약 1.5~2MB)

#### [ ] 9. 노이즈/아티팩트
- 얼굴/손 영역 깨끗
- 왜곡/뭉개짐 없음

#### [ ] 10. 배경 적합성
- plan.md의 배경 설정과 일치
- 불필요한 요소 없음

---

## 🚨 실패 처리 규칙

### 재생성 기준

**즉시 재생성 (고 심각도)**:
- 다른 사람으로 인식
- 캐릭터 인종 변경
- 아이템 색상 완전 불일치

**3회 재시도 (중 심각도)**:
- 미세한 피부톤 차이
- 헤어 길이 약간 다름
- 아이템 디테일 일부 누락

**허용 (저 심각도)**:
- 배경 디테일 차이
- 미세한 조명 차이
- 액세서리 미세 변형

### 재생성 방법

**1회 실패**:
```python
# 동일 파라미터로 재시도
retry_count = 1
nanogen_outfit_swap(same_params)
```

**2회 실패**:
```python
# negative_prompt 강화
negative_prompt += ", facial distortion, color mismatch"
```

**3회 실패**:
```python
# 다른 Gena 참조 이미지로 변경 시도
# 예: gena_ref_04 → gena_ref_03
```

**3회 이상 실패**:
- qa-reviewer에게 보고
- 오케스트레이터 개입 요청

---

## 📊 품질 기준

### 목표 KPI
- 1회 생성 성공률: 80% 이상
- 캐릭터 일관성: 95% 이상
- 아이템 정확도: 90% 이상

### 측정 방법
- QA 통과율로 측정
- 재생성 횟수 기록 (performance_log.json)

---

## 🔧 Nanogen 설정 옵션

### modelId
- `gemini-3.1-flash-image-preview` (기본)
- `nano-banana-2` (고품질, 느림)

### aspectRatio
- `3:4` (Instagram 피드)
- `9:16` (릴스)
- `1:1` (정사각)

### resolution
- `1K` (빠름, 테스트용)
- `2K` (기본, 고품질)

---

**최종 업데이트**: 2026-03-06 03:52
