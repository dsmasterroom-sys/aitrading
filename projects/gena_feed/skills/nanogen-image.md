---
name: designer (나노젠 이미지 프롬프트)
description: "design-brief 기반으로 나노젠 이미지 생성 프롬프트 작성. 레퍼런스 예제 구조를 따라 작성. API 호출은 developer 담당."
---

# nanogen-image SKILL

## 입력
- `series/{시리즈명}/design-brief.md`
- 참조: shared/brand-identity.md, shared/persona/, shared/products/

## 출력
- `series/{시리즈명}/nanogen-prompts/image_slide_XX.md`
- Prompt (영문) + Negative prompt + config + referenceImages 경로

---

## 핵심 원칙

> **에디토리얼 촬영 세트처럼 생각하라.**
> 같은 카메라·같은 조명에서 로케이션만 옮기며 찍는다.
> [CAMERA SETTINGS], [LIGHTING], [KEY TECHNICAL CHARACTERISTICS]는 시리즈 전체 동일.
> 슬라이드마다 바뀌는 것은 [INDICATIONS], [STYLE], [SCENE & ACTION]뿐이다.

### 변수
- `@model` — 젠아 페르소나 (레퍼런스 이미지로 전달)
- `@outfit` — 해당 슬라이드의 의상 조합 (소재·컬러·디테일까지 명시)
- `@object` — 협찬 제품 또는 핵심 소품 (브랜드명·소재·무게·특징 포함)

---

## 레퍼런스 예제 (구조 가이드 — 이 수준으로 작성)

> **아래 4개 예제가 프롬프트 품질의 기준이다.**
> 새 프롬프트는 이 구조와 디테일 수준을 따르되, 내용은 시리즈에 맞게 새로 작성한다.
> 예제를 그대로 복사하지 않는다.

### Reference 1 — UGC Style
```
[INDICATIONS] A Korean Beautiful real influencer @model. Wearing a trendy and hip casual style @outfit, and the @object. The atmosphere should feel like UGC content: spontaneous, natural, and intimate.
[STYLE] Clean but well-crafted UGC look. Natural reflections on the @object, aesthetic close to a high-quality smartphone video. Friendly and spontaneous energy. Subtle handheld camera shake.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Slight depth of field, natural and soft bokeh. Sharpness on @object details and skin.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light from an overcast day, enhanced with a cool cinematic grading creating a clean, elegant urban atmosphere. Low-key, soft, cool neutral tones, and controlled contrast highlighting the @outfit and @object.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light: No harsh shadows, no glare, wrapped in skylight. Cool temperature: 5500K–6500K leaning bluish; skin tones clean and neutral without yellow hues. Low-to-medium contrast: Soft, three-dimensional look. Desaturated color palette: Environmental colors desaturated by -15%; @object colors remain cinematic. Dominant tones: Urban greys, soft blues, cement green, wet stone.
[SCENE & ACTION] Red brick cafe alley in Seongsu-dong, a trendy hot place in Seoul. Medium close-up. @model takes two steps towards the camera, pauses, naturally adjusts the @object strap, and smiles slightly.
```

### Reference 2 — Cinematic Mood
```
[INDICATIONS] A Korean Beautiful real influencer @model. Wearing a trendy and hip casual style @outfit, and the @object.
[STYLE] Cinematic moody street photography. The mood is genuine and human, letting the silhouette and texture of the @object become part of the visual identity. Smooth movement without heavy handheld shake.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Shallow depth of field to isolate the subject.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light from an overcast day, enhanced with a cool cinematic grading creating a clean, elegant urban atmosphere. Low-key, soft, cool neutral tones, and controlled contrast highlighting the @outfit and @object.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light: No harsh shadows, no glare, wrapped in skylight. Cool temperature: 5500K–6500K leaning bluish; skin tones clean and neutral without yellow hues. Low-to-medium contrast: Soft, three-dimensional look. Desaturated color palette: Environmental colors desaturated by -15%; @object colors remain cinematic. Dominant tones: Urban greys, soft blues, cement green, wet stone.
[SCENE & ACTION] Vintage industrial neon-lit alley in Euljiro, a trendy hot place in Seoul. Wide establishing shot, slow dolly-in. @model stands confidently looking at the neon signs, then turns her profile to the camera to highlight the silhouette of the @object.
```

### Reference 3 — Dynamic Fashion Reel
```
[INDICATIONS] A Korean Beautiful real influencer @model. Wearing a trendy and hip casual style @outfit, and the @object.
[STYLE] Dynamic high-end fashion reel. Clean but well-crafted UGC look with a highly professional edge.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Deep focus to show both subject and the bustling environment.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light from an overcast day, enhanced with a cool cinematic grading creating a clean, elegant urban atmosphere. Low-key, soft, cool neutral tones, and controlled contrast highlighting the @outfit and @object.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light: No harsh shadows, no glare, wrapped in skylight. Cool temperature: 5500K–6500K leaning bluish; skin tones clean and neutral without yellow hues. Low-to-medium contrast: Soft, three-dimensional look. Desaturated color palette: Environmental colors desaturated by -15%; @object colors remain cinematic. Dominant tones: Urban greys, soft blues, cement green, wet stone.
[SCENE & ACTION] Bustling street corner in Hongdae, a trendy hot place in Seoul. Eye-level tracking shot moving left to right. @model takes three quick steps, stops abruptly, poses with hands in pockets, letting the @object take center stage.
```

### Reference 4 — Cinematic Narrative
```
[INDICATIONS] A Korean Beautiful real influencer @model. Wearing a trendy and hip casual style @outfit, and the @object.
[STYLE] Cinematic narrative. The mood is genuine and human, creating a moment of authentic lifestyle.
[CAMERA SETTINGS] Kodak Portra 400 emulation, 35mm equivalent, f/2.0, 1/120s, ISO 200. Natural and soft bokeh.
[LIGHTING: SOFT NATURAL DAYLIGHT] Natural light from an overcast day, enhanced with a cool cinematic grading creating a clean, elegant urban atmosphere. Low-key, soft, cool neutral tones, and controlled contrast highlighting the @outfit and @object.
[KEY TECHNICAL CHARACTERISTICS] Soft, diffused light: No harsh shadows, no glare, wrapped in skylight. Cool temperature: 5500K–6500K leaning bluish; skin tones clean and neutral without yellow hues. Low-to-medium contrast: Soft, three-dimensional look. Desaturated color palette: Environmental colors desaturated by -15%; @object colors remain cinematic. Dominant tones: Urban greys, soft blues, cement green, wet stone.
[SCENE & ACTION] Dongdaemun Design Plaza (DDP), a trendy hot place in Seoul, featuring curved metallic architecture. Over-the-shoulder shot transitioning to a medium close-up. @model checks her phone, then looks up directly into the lens.
```

---

## 프롬프트 작성 규칙

### [INDICATIONS] — 슬라이드마다 변경
- 첫 문장: **"A Korean Beautiful real influencer @model"** (필수)
- @outfit: 소재, 컬러, 디테일(버튼·지퍼·칼라), 실루엣 구체적으로
- @object: 브랜드명, 소재, 무게, 착용 방식 구체적으로
- "No overlay, no text, no logo." 포함

### [STYLE] — 슬라이드마다 변경 가능
레퍼런스 예제의 4가지 스타일 중 선택하거나 아래 추가 변형 활용:
- **에디토리얼**: "Editorial lookbook. Clean, composed framing. Polished minimalist tones. Strong silhouette emphasis, intentional negative space."
- **스트릿 다큐**: "Street documentary style. Raw, unposed, mid-motion capture. Slight motion blur on limbs, sharp focus on @object."
- **제품 히어로**: "Studio product photography. Clean backdrop. Even soft diffusion. Macro-level detail on material texture, stitching, hardware."

### [CAMERA SETTINGS] — 시리즈 고정
레퍼런스 예제의 카메라 블록을 기본으로 사용. 렌즈·조리개만 슬라이드별 미세 조정 가능.
필름 에뮬레이션과 ISO는 바꾸지 않는다.

### [LIGHTING] — 시리즈 고정
기본값: **SOFT NATURAL DAYLIGHT** (레퍼런스 예제와 동일).
시리즈 전체에서 하나의 라이팅만 사용. 혼용 금지.

대체 프리셋 (필요 시):
- **BRIGHT SUNNY**: 5500K, high-key, fresh, direct sunlight
- **GOLDEN HOUR**: 3500-4500K, low-angle, dramatic rim light, cinematic warmth

### [KEY TECHNICAL CHARACTERISTICS] — 시리즈 고정
레퍼런스 예제의 블록을 기본으로 사용.
**도미넌트 톤만** 시리즈 주제에 맞게 조정:
- 기본: "Urban greys, soft blues, cement green, wet stone."
- 벚꽃: "Urban greys, soft blues, muted cherry pink, wet stone."
- 가을: "Warm taupe, burnt sienna, dry leaves, slate grey."

### [SCENE & ACTION] — 핵심. 슬라이드마다 고유.
**6요소 필수:**
1. **구체적 장소** — 특정 지명 + 건축/환경 디테일 (서울에 한정하지 않음. "a trendy hot place in Seoul" 패턴 활용)
2. **카메라 앵글/구도** — 앵글 프리셋에서 선택
3. **마이크로 액션 1-2개** — "걷는다" ✗ → "두 발짝 걷고 멈추고 가방 스트랩을 조정한다" ✓
4. **표정/감정** — "웃는다" ✗ → "뭔가 재미있는 걸 본 듯 입꼬리가 올라간다" ✓
5. **소품 인터랙션** — @object 또는 소품과의 자연스러운 접촉
6. **환경 디테일** — 배경의 구체적 요소 (네온, 행인, 식물, 건축물 등)

---

## 앵글 프리셋

| 앵글 | 키워드 | 용도 |
|------|--------|------|
| 광각샷 | wide-angle shot, 16mm lens, expansive environment | 장소감 강조 |
| 항공샷 | aerial top-down view, bird's-eye perspective | 플랫레이, OOTD |
| MZ셀카 | POV selfie angle, slightly above eye-level | 친근감 |
| 발샷 | low-angle ground shot, focus on shoes and pavement | 신발/하의 |
| 뒷모습 | rear view, walking away from camera | 미스터리 |
| 횡단보도 | wide side profile, full street scene | 스트릿 무드 |
| 거울샷 | mirror reflection | MZ 필수 |
| 프레임인프레임 | framed through doorway/window/arch | 깊이감 |
| 클로즈업 | extreme close-up, macro lens 100mm | 제품 디테일 |
| 모션블러 | 1/30s shutter, intentional motion blur | 역동성 |
| 실루엣 | backlit silhouette, rim light only | 드라마틱 |
| 오버숄더 | over-the-shoulder from behind | 스토리텔링 |

> 시리즈(10컷) 내 최소 5가지 앵글. 같은 앵글 2연속 금지.

---

## 3단계 파이프라인 (인물+의상 슬라이드)

**Phase 1: 의상 flat-lay**
- [STYLE]: "Clean editorial flat-lay photography. Overhead bird's-eye view."
- [CAMERA SETTINGS]: Kodak Ektar 100, 50mm, f/5.6
- referenceImages: 없음

**Phase 2: Composition** (고정 프롬프트 — 수정하지 않는다)
```
"Change only the main clothing garments to strictly match the design,
texture, and details of the provided clothing reference image.
Replicate the attached outfit exactly. Crucially, preserve all
original accessories intact. Keep the original model's face, pose,
hair, background, and lighting exactly the same.
Seamless integration, photorealistic, 8k resolution."
```
referenceImages: [페르소나 이미지, 의상 flat-lay] (순서: 페르소나 FIRST)

> **비율 왜곡 주의**: Phase 2에서 비율이 틀어지면 건너뛰고 persona ref만으로 Phase 3 직행.

**Phase 3: 최종 슬라이드**
- 6섹션 구조로 작성 (레퍼런스 예제 수준)
- referenceImages: [composition 결과 또는 persona, 제품 폴더 전체]

---

## 협찬 제품 참조

제품 폴더 내 **모든 이미지를 복수 참조**. 이미지가 많을수록 디테일 정확.
```
referenceImages: [
  shared/persona/{헤어 파일},
  shared/products/{폴더}/img_01.png,
  shared/products/{폴더}/img_02.png,
  ...
]
```

제품 배치 구체적으로:
- ✓ "@object (gen archive matte black nylon slant crossbag, 196g) worn DIAGONALLY ACROSS torso, compact bag body resting at right hip"
- ✗ "@object worn as crossbody bag"

---

## 네거티브 프롬프트 (전 슬라이드 고정)

```
oversaturated, western aesthetic, heavy filter, text overlay,
cluttered background, artificial glamour, unnatural skin, plastic look,
stiff pose, mannequin-like, stock photo feel, generic smile,
bad anatomy, extra fingers, deformed hands, blurry face,
watermark, signature, logo, frame border, collage layout,
readable text, signage, store names, Korean text, Japanese text,
Chinese characters, kanji, hangeul, extra accessories not described
in prompt, backpack, clutch, AI-generated artifact, synthetic appearance,
disproportionate body, large head, short arms
```

---

## 자기검증 체크리스트

### 시리즈 레벨:
- [ ] [CAMERA], [LIGHTING], [KEY TECH] 고정 블록이 전 슬라이드 동일?
- [ ] 라이팅 프리셋 1개만 사용?
- [ ] 네거티브 프롬프트 강화 버전 적용?

### 슬라이드 레벨:
- [ ] [INDICATIONS]에 의상·제품 디테일이 레퍼런스 예제 수준으로 구체적?
- [ ] [SCENE & ACTION]에 6요소 모두 포함?
- [ ] 장소에 구체적 지명 + 환경 디테일 포함?
- [ ] 마이크로 액션이 구체적 동작 비트?

### 다양성 레벨:
- [ ] 앵글 최소 5가지, 2연속 동일 없음?
- [ ] 장소 최소 3개 카테고리, 2연속 동일 없음?
- [ ] 스타일 최소 2가지 혼용?
- [ ] 같은 마이크로 액션 반복 없음?
