---
name: plan-content
agent: contents-marketer
description: "감정 곡선 설계 + 슬라이드/씬별 역할 명세. 실제 카피 작성 금지 (write-copy 담당)."
input: "weekly/research.md (확정 주제 1개 + 메타데이터), 포맷 (릴스/캐러셀/스토리)"
output: "weekly/content-plan.md 또는 weekly/scene-plan.json"
---

# plan-content SKILL

## 캐러셀 (9장) 기획

감정 곡선 원칙: 공감 → 전환 → 증거/팁 → 실천/CTA

| 장 | 역할 | 감정 온도 | 레이아웃 힌트 |
|----|------|----------|--------------|
| 1 | 훅 (숫자 or 질문 제목) | ●○○○○ | 강조형 H-1~3 |
| 2 | 공감 (문제 상황) | ●●○○○ | 감정형 I-2 |
| 3~6 | 팁 1~4 | ●●●○○ | 정보형 I-1~5 / 절차형 P |
| 7 | 아이템 자연 연결 (monetize) | ●●●○○ | 아이템형 M-1~2 |
| 8 | 요약 | ●●○○○ | 정리형 I-4 |
| 9 | CTA | ●○○○○ | CTA형 CTA-1~2 |

**규칙**: 같은 레이아웃 패턴 2연속 금지 · 같은 감정 온도 3장 연속 금지

## 릴스 (30초) 씬 기획

출력 형식: `weekly/scene-plan.json`

```json
{
  "scenes": [
    {
      "scene_id": "S1",
      "duration_sec": 5,
      "role": "훅 — 멈추게 만드는 질문/충격",
      "image_direction": "강렬한 클로즈업 or 텍스트 중심",
      "caption_max_chars": 10,
      "camera_movement": "zoom_in",
      "model_hint": "kling-v3 pro",
      "outfit_swap": false
    },
    {
      "scene_id": "S2", "duration_sec": 5, "role": "문제 제기",
      "image_direction": "공감 상황 묘사", "caption_max_chars": 15,
      "camera_movement": "pan_left", "model_hint": "kling-v2.6 standard", "outfit_swap": false
    },
    {
      "scene_id": "S3", "duration_sec": 6, "role": "팁/해결 1",
      "image_direction": "제품 or 행동 시연", "caption_max_chars": 20,
      "camera_movement": "tilt_up", "model_hint": "kling-v2.6 standard", "outfit_swap": false
    },
    {
      "scene_id": "S4", "duration_sec": 6, "role": "팁/해결 2 (slant 착용 씬)",
      "image_direction": "전체 룩 공개 — Outfit Swap", "caption_max_chars": 20,
      "camera_movement": "zoom_out", "model_hint": "kling-v3 pro", "outfit_swap": true
    },
    {
      "scene_id": "S5", "duration_sec": 6, "role": "반전/결론",
      "image_direction": "before→after or 완성 이미지", "caption_max_chars": 15,
      "camera_movement": "pan_right", "model_hint": "kling-v3 pro", "outfit_swap": false
    },
    {
      "scene_id": "S6", "duration_sec": 5, "role": "CTA — slant 링크바이오",
      "image_direction": "slant 클로즈업", "caption_max_chars": 10,
      "camera_movement": "zoom_in", "model_hint": "kling-v3 pro", "outfit_swap": true
    }
  ]
}
```

## 스토리 (3일 시퀀스) 기획

| 시점 | 역할 | 배경 소스 | 인터랙션 |
|------|------|----------|---------|
| D-1 (화) | 궁금증 유발 | assets/thumb/slide-01.png | 투표 스티커 |
| D+0 (수) | 캐러셀 공유 | assets/thumb/slide-01.png | 게시물 링크 |
| D+3 (토) | 반응 공유 + slant CTA | assets/reels/scene-05.png | 링크 스티커 |

## 자기검증 체크리스트

- [ ] 실제 카피 한 줄도 쓰지 않았는가 (역할/방향만 명세)
- [ ] 캐러셀: 감정 온도 3장 연속 동일 없음
- [ ] 캐러셀: 같은 레이아웃 패턴 2연속 없음
- [ ] 캐러셀: 7장에 monetize 아이템 배치 확인
- [ ] 릴스: scene-plan.json에 6개 씬 전부 포함
- [ ] 릴스: S4·S6 outfit_swap: true 설정 확인
