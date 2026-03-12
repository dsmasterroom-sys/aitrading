# 캐러셀 제작 워크플로

## 실행 순서 (2-Gate)

```
[자동 구간 1]
1. researcher        → skills/research.md
                     → 출력: series/{시리즈명}/research.md

2. contents-marketer → skills/plan-content.md
                     → 출력: series/{시리즈명}/plan.md

3. contents-marketer → skills/write-copy.md
                     → 출력: series/{시리즈명}/copy.md

4. designer          → skills/design-brief.md
                     → 출력: series/{시리즈명}/design-brief.md

5. designer          → skills/nanogen-image.md
                     → 출력: series/{시리즈명}/nanogen-prompts/image_slide_XX.md

→ [Gate A] 사용자 중간 확인: 리서치 요약 + 기획 핵심 + 비주얼 방향

[자동 구간 2]
6. developer         → skills/nanogen-workflow.md  (API 호출·이미지 생성)
                     → 출력: series/{시리즈명}/generated/

7. developer         → skills/build-html.md  (HTML 구현·PNG 추출)
                     → 출력: output/{시리즈명}/slide_XX.png

8. qa-reviewer       → skills/qa-check.md
                     → 출력: series/{시리즈명}/qa-report.md
                     → HIGH+MID=0 될 때까지 6→7→8 자동 반복

→ [Gate B] 사용자 최종 확인: 완성 PNG + QA 리포트
```

## 기본 설정
- 슬라이드 수: 8-10장
- 캔버스: 1080×1350px
- 나노젠 기본 모드: Text-to-Image
