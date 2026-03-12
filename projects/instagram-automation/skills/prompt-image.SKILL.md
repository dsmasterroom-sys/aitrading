# prompt-image.SKILL.md

**용도**: 이미지 생성 프롬프트 작성 규칙  
**사용 에이전트**: prompt-engineer  
**버전**: 1.0

---

## 📥 입력

- research.md (트렌드, 해시태그)
- items.json (아이템 정보)
- shared/gena-master-prompt.md (Gena 기준)
- plan.md (콘텐츠 기획)

---

## 📤 출력

prompts.json:
```json
{
  "content_type": "carousel",
  "slide_02": {
    "image_prompt": "gena, 20s korean woman, wearing...",
    "negative_prompt": "different face, wrong outfit",
    "reference_images": ["gena_ref_04.png", "items.json > item_id"],
    "nanogen_config": {
      "modelId": "gemini-3.1-flash-image-preview",
      "aspectRatio": "3:4",
      "resolution": "2K"
    }
  }
}
```

---

## 🔧 실행 흐름

### 1단계: Gena 참조 이미지 선택

**헤어스타일 → 콘텐츠 무드 매핑**:
- gena_ref_01: 긴 스트레이트 → 포멀/출근룩
- gena_ref_02: 웨이브 하프업 → 데이트룩
- gena_ref_03: 단발 → 캐주얼/스트릿
- gena_ref_04: 포니테일 → 스포티/액티브
- gena_ref_05~08: 기타 스타일

**선택 규칙**:
- plan.md의 무드 키워드 확인
- "화보/세련" → ref_01 or ref_04
- "캐주얼/스트릿" → ref_03
- "데이트/여성스러운" → ref_02

### 2단계: 프롬프트 구조 조립

**구조**:
```
[캐릭터] + [나이/국적] + [착용 아이템] + [포즈] + [배경] + [조명] + [스타일] + [카메라]
```

**예시**:
```
gena, 20s korean woman,
wearing 무신사 스탠다드 오버사이즈 셔츠 [loose fit, 7-button front, 3/4 sleeve],
black wide-leg pants,
casual walking pose,
urban street in Seoul with modern buildings,
afternoon golden hour,
editorial fashion photography,
full body shot,
high quality, professional photography
```

### 3단계: visual_desc 삽입

items.json의 visual_desc를 `[...]` 안에 삽입:

```json
{
  "visual_desc": "오버사이즈 핏, 앞단추 7개, 7부 소매"
}
```
↓
```
wearing 무신사 오버사이즈 셔츠 [오버사이즈 핏, 앞단추 7개, 7부 소매]
```

### 4단계: negative_prompt 작성

**필수 포함**:
- "different face"
- "different person"
- "wrong outfit"

**추가 권장**:
- "cartoon, anime, 3d render"
- "accessory inconsistency"

### 5단계: nanogen_config 설정

**Instagram 최적**:
- 피드: `"aspectRatio": "3:4"`, `"resolution": "2K"`
- 릴스: `"aspectRatio": "9:16"`, `"resolution": "2K"`
- 정사각: `"aspectRatio": "1:1"`, `"resolution": "1K"`

---

## ✅ 자기검증 체크리스트 (10개)

프롬프트 작성 완료 후 **모두 체크**:

### [ ] 1. Gena 캐릭터 토큰
- "gena, 20s korean woman" 첫 위치 포함

### [ ] 2. 참조 이미지 선택
- gena_ref_01~08 중 1개 선택
- 선택 이유 명시

### [ ] 3. visual_desc 삽입
- items.json의 visual_desc를 [...] 안에 포함
- 최소 3가지 특징 포함

### [ ] 4. negative_prompt
- "different face, wrong outfit" 필수 포함

### [ ] 5. 배경 구체화
- 추상적 표현 금지
- 구체적 장소 명시 (예: "성수동 brick alley")

### [ ] 6. 조명 명시
- "golden hour" / "soft diffused light" 등

### [ ] 7. 카메라 앵글
- "full body shot" / "half body shot" / "close-up" 중 선택

### [ ] 8. 감정 온도 일치
- plan.md의 해당 슬라이드 감정 온도와 일치

### [ ] 9. nanogen_config 유효
- modelId, aspectRatio가 Nanogen 지원 범위

### [ ] 10. 중복 배제
- 같은 시리즈 내 동일 배경/포즈 2연속 금지

---

## 🚫 금지 키워드

**절대 사용 금지**:
- ❌ "beautiful face", "pretty eyes" (외모 묘사)
- ❌ "sexy", "hot", "attractive" (외모 평가)
- ❌ "AI", "generated", "digital art" (메타 언급)
- ❌ "perfect", "flawless" (과장)

---

## 📋 템플릿

### 캐주얼 데일리
```
gena, 20s korean woman,
wearing [아이템 visual_desc],
casual pose,
cozy cafe interior with wooden furniture,
morning natural light,
lifestyle photography,
half body shot,
high quality
```

### 화보 스타일
```
gena, 20s korean woman,
wearing [아이템 visual_desc],
confident standing pose,
minimalist studio with white background,
professional studio lights,
fashion lookbook photography,
full body shot,
high quality, professional photography, 8K
```

---

**최종 업데이트**: 2026-03-06 03:51
