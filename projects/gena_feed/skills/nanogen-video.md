---
name: designer (나노젠 영상 프롬프트)
description: "릴스용 Veo 3.1 마스터 프롬프트 구조로 영상 프롬프트 작성. 서울 씬 기반 UGC/시네마틱 스타일."
---

# nanogen-video SKILL

## 입력
- `series/{시리즈명}/design-brief.md` (릴스 기획)
- 영상 스타일, 장소, 길이 요구사항
- 참조: shared/brand-identity.md, shared/persona/, shared/products/

## 출력
- `series/{시리즈명}/nanogen-prompts/video_reel.md`
- Veo 3.1 7블록 완성 프롬프트 + config

---

## 실행 흐름

### Step 1 — 영상 스타일 선택

| 스타일 | 특징 | 적합 콘텐츠 |
|--------|------|------------|
| UGC Style | 핸드헬드 흔들림, 스폰테니어스, 스마트폰 느낌 | 협찬 자연 노출, 일상 브이로그 |
| Cinematic Mood | 부드러운 카메라, 실루엣 강조, 무드 중심 | 감성 릴스, 브랜드 무드필름 |
| Dynamic Fashion | 트래킹샷, 스톱-앤-포즈, 하이엔드 엣지 | 패션 룩북, 스타일링 쇼케이스 |
| Cinematic Narrative | 타임코드 분할, 스토리텔링 | 시리즈 오프닝, 스토리 있는 릴스 |

### Step 2 — 모델 선택
- `kling-v3 Pro`: 메인 릴스, 최고 퀄리티
- `kling-v2.6 Standard`: 빠른 프리뷰, A/B 테스트
- `veo`: 시네마틱 자연광, 내레이티브 무드

### Step 3 — Veo 3.1 7블록 프롬프트 구조 (이 순서 고정)
```
[INDICATIONS]  인물(@model), 의상(@outfit), 제품(@object), 전체 바이브
[STYLE]        에스테틱, 필름 포맷, 무드, 카메라 움직임 로직
[CAMERA SETTINGS] 렌즈, 심도, 셔터, ISO, 보케
[LIGHTING]     조명 조건 (아래 3종에서 선택)
[KEY TECHNICAL CHARACTERISTICS] 대비·색온도·팔레트 앵커
[SCENE & ACTION] 서울 장소 + 타이밍 + 액션 비트 (숏당 1-2개만)
[DIALOGUE & AUDIO] 한국어 대사 + 오디오 텍스처
```

### Step 4 — 조명 조건 (3종 중 선택)
```
[Overcast]     Natural light from an overcast day, cool cinematic grading,
               5500K-6500K, low-to-medium contrast, urban greys + soft blues
[Bright Sunny] Direct sunlight, crisp clean grading, 5500K pure daylight,
               medium-to-high contrast, clear sky blues + sunlit concrete
[Golden Hour]  Low-angle golden light, 3500K-4500K warm, long shadows,
               golden rim light, golden yellows + cool shadow blues
```

### Step 5 — 서울 씬 × 스타일 조합 템플릿

**성수동 UGC (협찬 자연 노출)**
```
[SCENE & ACTION] Red brick cafe alley in Seongsu-dong, Seoul.
  Medium close-up. @model takes two steps toward camera,
  pauses, naturally adjusts @object strap, smiles slightly.
[DIALOGUE & AUDIO] @model whispers fast in Korean: "야, 오늘 코디 어때?"
  Raw iPhone mic, uneven reception, cafe chatter + soft footsteps.
```

**을지로 Cinematic Mood**
```
[SCENE & ACTION] Vintage neon-lit alley in Euljiro, Seoul.
  Wide establishing shot, slow dolly-in. @model stands confidently,
  then turns profile to highlight @object silhouette.
[DIALOGUE & AUDIO] @model speaks fast in Korean: "여기 분위기 진짜 미쳤지?"
  Low-quality iPhone, patchy reception, faint neon hum + traffic hiss.
```

**홍대 Dynamic Fashion**
```
[SCENE & ACTION] Bustling street corner in Hongdae, Seoul.
  Eye-level tracking shot left to right. @model takes three quick steps,
  stops abruptly, poses hands in pockets, @object takes center stage.
[DIALOGUE & AUDIO] @model whispers: "대박, 방금 봤어?"
  Glitchy cell mic, heavy signal dropouts + street ambiance.
```

**DDP Narrative (타임코드 분할)**
```
[SCENE & ACTION] Dongdaemun Design Plaza, curved metallic architecture.
  Over-the-shoulder → medium close-up transition.
  [00:00-00:02] @model checks phone.
  [00:02-00:04] @model looks up directly into lens.
[DIALOGUE & AUDIO] Fast casual Korean: "서울 구경, 준비됐어? 빨리 와."
  Raw iPhone mic, slight muffled wind + subtle footsteps.
```

### Step 6 — config 작성
```
config:
  modelId: "kling-v3" | "kling-v2.6" | "veo"
  durationSeconds: 4 | 5 | 8 | 10   (Kling 지원값)
  klingMode: "pro" | "standard"
  cameraMovement: "zoom_in" | "zoom_out" | "pan_right" | "pan_left" | "tilt_up"
referenceImages:
  - shared/persona/{헤어 파일}      (인물 등장 시 필수)
  - shared/products/{폴더}/ref_01   (제품 등장 시 필수)
```

---

## 자기검증 체크리스트
- [ ] 7블록 구조가 순서대로 완성되었는가?
- [ ] 서울 실제 장소가 명시되었는가?
- [ ] 대사가 한국어이고 "빠른 일상어 or 속삭임"으로 지정되었는가?
- [ ] 오디오에 "raw iPhone mic, uneven reception" 텍스처가 포함되었는가?
- [ ] 액션 비트가 숏당 1-2개로 제한되었는가?
- [ ] 인물/제품 등장 시 referenceImages가 포함되었는가?
- [ ] durationSeconds가 Kling 지원값(4·5·8·10)인가?
