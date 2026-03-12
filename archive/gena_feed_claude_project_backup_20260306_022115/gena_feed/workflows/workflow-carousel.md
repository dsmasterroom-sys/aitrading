# workflow-carousel.md — 캐러셀 제작

trigger: "캐러셀 만들어줘" / "카드뉴스" / weekly에서 캐러셀 포맷 확정 시

---

## 실행 흐름

```
STEP 1. spawn: contents-marketer (plan-content)
  스킬: skills/plan-content.md
  입력: weekly/research.md (확정 주제)
  출력: weekly/content-plan.md (9장 감정 곡선 + 레이아웃 힌트)

STEP 2. spawn: contents-marketer (write-copy + monetize)
  스킬: skills/write-copy.md + skills/monetize.md
  입력: weekly/content-plan.md
  출력: weekly/copy.md (슬라이드별 카피 완성본)

STEP 3. spawn: designer
  스킬: skills/design-visual.md
  입력: weekly/copy.md + weekly/content-plan.md
  출력: weekly/design-brief.md (슬라이드별 패턴 코드 + 이미지 프롬프트)

STEP 4. [G2 게이팅] 사용자 확인
  전달 내용:
    - 슬라이드 카피 요약 (1장·7장·9장 하이라이트)
    - 레이아웃 패턴 목록
    - monetize 태그 + 광고 표기 방식
  대기: 사용자 승인

STEP 5. spawn: developer (HTML→PNG)
  스킬: skills/build-html.md (TRACK 1)
  출력: output/slides/slide-01.png ~ slide-09.png
  완료 즉시: slide-01.png → assets/thumb/slide-01.png 복사

STEP 6. spawn: qa-reviewer
  스킬: skills/qa-check.md (캐러셀 항목)
  출력: weekly/qa-report.md

STEP 7. QA 루프
  고·중 이슈 0건까지: developer 재수정 → qa-reviewer 재검증

STEP 8. [G3 게이팅] 발행 최종 확인
  체크: QA 0건 · slant 7장 링크바이오 · 광고 표기
  통과 후: Buffer/Later 수요일 12:00 예약
```
