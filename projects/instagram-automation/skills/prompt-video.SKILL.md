# prompt-video.SKILL.md

**용도**: 영상 생성 프롬프트 작성 규칙  
**사용 에이전트**: prompt-engineer  
**버전**: 1.0

---

## 📥 입력

- reel-plan.md (씬 기획)
- items.json
- shared/gena-master-prompt.md

---

## 📤 출력

prompts.json (video_prompts):
```json
{
  "scene_01_hook": {
    "video_prompt": "gena korean woman in white shirt, turning to camera with smile, slow pan right, urban street, golden hour, cinematic",
    "reference_images": ["gena_ref_04.png"],
    "nanogen_config": {
      "modelId": "kling-v3",
      "durationSeconds": 5,
      "cameraMovement": "pan_right"
    }
  }
}
```

---

## 🔧 프롬프트 구조

```
[씬 설명] + [주인공] + [아이템] + [동작] + [카메라] + [배경] + [무드] + [스타일]
```

**예시**:
```
gena korean woman wearing white oversized shirt and black pants,
walking confidently toward camera,
slow pan right,
urban street in Seoul with modern buildings,
afternoon golden hour,
cinematic fashion video,
professional quality
```

---

## 🎬 카메라 무브먼트 (Nanogen 지원)

- `pan_left` / `pan_right`: 좌우 패닝
- `tilt_up` / `tilt_down`: 상하 틸트
- `zoom_in` / `zoom_out`: 줌
- `static`: 고정

---

## 📋 씬별 추천

### 훅 씬 (0~3초)
- 카메라: zoom_in
- 동작: 얼굴 클로즈업, 시선 처리
- 무드: 강렬한 비주얼

### 바디 씬 (3~15초)
- 카메라: pan_right, tilt_up
- 동작: 워킹, 포즈 변화
- 무드: 아이템 쇼케이스

### CTA 씬 (15~20초)
- 카메라: static
- 동작: 정면 포즈
- 무드: 저장 유도

---

## ✅ 검증

### [ ] Gena 토큰 포함
### [ ] 카메라 무브먼트 명시
### [ ] 동작 구체적
### [ ] durationSeconds: 5초

---

**최종 업데이트**: 2026-03-06 03:58
