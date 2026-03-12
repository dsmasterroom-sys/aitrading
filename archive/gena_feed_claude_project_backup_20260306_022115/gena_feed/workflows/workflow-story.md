# workflow-story.md — 스토리 제작

trigger: "스토리 만들어줘" / 캐러셀 또는 릴스 완료 후 자동 연계

---

## 사전 확인 (오케스트레이터)

```
assets/thumb/slide-01.png 존재 여부 확인
  → 없으면: "캐러셀을 먼저 제작해야 스토리 배경을 만들 수 있습니다.
             캐러셀 제작을 먼저 진행할까요?" 사용자에게 질문
```

---

## 실행 흐름

```
STEP 1. spawn: contents-marketer (write-copy)
  스킬: skills/write-copy.md (스토리 텍스트 섹션)
  입력: weekly/research.md (확정 주제) + weekly/copy.md (캐러셀 제목 참조)
  출력: weekly/story-copy.md
    - D-1: 질문 텍스트 + 투표 선택지 2개
    - D+0: 공유 텍스트 + 게시물 링크 안내
    - D+3: 반응 공유 텍스트 + slant 링크바이오 CTA

STEP 2. spawn: developer (Pillow 합성)
  스킬: skills/build-html.md (TRACK 3)
  입력:
    D-1 배경: assets/thumb/slide-01.png
    D+0 배경: assets/thumb/slide-01.png
    D+3 배경: assets/reels/scene-05.png (없으면 slide-01.png 대체)
  출력:
    output/story/story-d1.png
    output/story/story-d0.png
    output/story/story-d3.png

STEP 3. spawn: qa-reviewer
  스킬: skills/qa-check.md (스토리 항목)
  출력: weekly/qa-report.md (스토리 섹션)

STEP 4. QA 루프
  고·중 이슈 0건까지: developer 재수정 → qa-reviewer 재검증

STEP 5. [G3 게이팅] 발행 확인
  발행 스케줄:
    D-1: 화요일 19:00
    D+0: 캐러셀 발행 직후
    D+3: 토요일 10:00
  주의: 투표·질문 스티커는 인스타 앱에서 직접 추가
```
