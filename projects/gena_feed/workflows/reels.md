# 릴스 제작 워크플로

## 실행 순서 (2-Gate)

```
[자동 구간 1]
1. researcher        → skills/research.md

2. contents-marketer → skills/plan-content.md + skills/write-copy.md
                     → 출력: 릴스 스크립트 (보이스오버 + 자막)

3. designer          → skills/design-brief.md (장면별 비주얼 기획)
4. designer          → skills/nanogen-image.md (썸네일·스틸컷 프롬프트)
5. designer          → skills/nanogen-video.md (영상 프롬프트·모델 선택)

→ [Gate A] 사용자 중간 확인: 리서치 요약 + 스크립트 + 비주얼 방향

[자동 구간 2]
6. developer         → skills/nanogen-workflow.md  (영상 생성 API 호출)
                     → Kling I2V: task_id 폴링 → MP4 URL 수령

7. qa-reviewer       → skills/qa-check.md

→ [Gate B] 사용자 최종 확인: 완성 MP4 + QA 리포트
```

## 기본 설정
- 기본 모델: Kling v3.0 Pro
- 기본 길이: 10초 (4·5·8·10초 선택 가능)
- 캔버스: 1080×1920px (9:16)
