---
name: developer (나노젠 워크플로)
description: "나노젠 Workflow Studio 파이프라인 실행. 시리즈 콘텐츠 자동화 체인 담당."
---

# nanogen-workflow SKILL

## 입력
- `series/{시리즈명}/nanogen-prompts/` (image_slide_XX.md 전체)
- 나노젠 서버 주소 및 .env 설정 확인

## 출력
- `series/{시리즈명}/generated/` 폴더에 생성된 이미지·영상 파일
- 각 파일은 base64 변환 완료 상태로 저장

---

## 실행 흐름 — 3단계 이미지 파이프라인

인물+의상 슬라이드는 반드시 아래 3단계를 순서대로 실행한다.
제품 전용 슬라이드(매크로, 히어로샷)는 Phase 3만 실행.

### Phase 1 — 의상 이미지 생성 (Flat-lay)
각 룩의 의상 조합을 flat-lay(바닥 배치) 이미지로 생성한다.
의상 레퍼런스가 이미 있으면(스크래핑/사용자 제공) 이 단계 생략.
```
POST http://localhost:8000/api/generate
{
  "prompt": "[6섹션 flat-lay 프롬프트]",
  "config": { "aspectRatio": "4:5", "resolution": "1080x1350" },
  "referenceImages": []  ← 참조 없이 프롬프트만으로 생성
}
저장: generated/outfits/look{N}_{style}.png
```

### Phase 2 — Composition (의상 교체)
젠아 페르소나에 Phase 1의 의상을 입힌다.
```
POST http://localhost:8000/api/generate
{
  "prompt": "Change only the main clothing garments to strictly match
    the design, texture, and details of the provided clothing reference
    image. Replicate the attached outfit exactly. Crucially, preserve
    all original accessories intact. Keep the original model's face,
    pose, hair, background, and lighting exactly the same.
    Seamless integration, photorealistic, 8k resolution.",
  "config": { "aspectRatio": "4:5", "resolution": "1080x1350" },
  "referenceImages": [
    "data:...모델(페르소나) 이미지",   ← 첫 번째: 모델
    "data:...의상(flat-lay) 이미지"    ← 두 번째: 의상
  ]
}
저장: generated/compositions/comp_look{N}_{style}.png
```

### Phase 3 — 최종 슬라이드 생성
composition 결과 + 제품 참조로 최종 장면을 생성한다.
```
POST http://localhost:8000/api/generate
{
  "prompt": "[6섹션 슬라이드 프롬프트]",
  "config": { "aspectRatio": "4:5", "resolution": "1080x1350" },
  "referenceImages": [
    "data:...composition 결과",        ← 첫 번째: 의상 입은 젠아
    "data:...제품 이미지 1",           ← 제품 폴더 내 전체
    "data:...제품 이미지 2",
    ...
  ]
}
반환값: { "url": "data:image/png;base64,..." }
저장: generated/slide_XX.png
```

> **⚠ 필수: referenceImages는 반드시 data URI 형식으로 전송**
> `data:{mime};base64,{data}` 프리픽스가 없으면 백엔드의
> `process_reference_image()`가 `None`을 반환하여 참조 이미지가
> 전부 무시된다. raw base64만 보내면 안 된다.

### Step 4 — 영상 생성 API 호출 (릴스)
```
POST http://localhost:8000/api/generate-video
{
  "prompt": "...",
  "config": { "modelId": "kling-v3", "durationSeconds": 10,
              "klingMode": "pro", "cameraMovement": "zoom_in" },
  "referenceImages": ["data:...base64_source"]
}
→ Kling AI: task_id 수령 → 폴링 → 최종 MP4 URL 수령
```

### Step 5 — 반환값 처리 및 저장
- URL 반환 시: fetch → ArrayBuffer → base64 변환
- base64 직접 반환 시: 그대로 사용
- 저장 위치: `series/{시리즈명}/generated/slide_XX.png`

---

## 자기검증 체크리스트
- [ ] .env 3가지 키가 모두 설정되어 있는가?
- [ ] 모든 referenceImages가 data URI 형식(data:{mime};base64,...)인가?
- [ ] 인물 슬라이드: Phase 1→2→3 순서를 지켰는가?
- [ ] Phase 2 composition: [모델, 의상] 순서인가?
- [ ] Phase 3: composition 결과가 referenceImages 첫 번째인가?
- [ ] 제품 참조: 해당 폴더 내 모든 이미지를 복수 참조했는가?
- [ ] Kling I2V: 폴링 완료 후 MP4 URL을 수령했는가?
- [ ] 생성된 파일이 generated/ 폴더에 저장되었는가?
- [ ] 외부 URL을 HTML에 직접 삽입하지 않았는가?
