# workflow-weekly.md — 주간 콘텐츠 발굴

trigger: "주제 찾아줘" / "이번 주 콘텐츠" / 매주 월요일 시작

---

## 실행 흐름

```
STEP 1. spawn: researcher
  스킬: skills/research-trend.md
  입력: 현재 시즌 (월/시즌) + 계정 목표 (유입/전환/신뢰)
  출력: 주제 후보 12개 + 메타데이터

STEP 2. 오케스트레이터: researcher 결과 저장
  저장 위치: weekly/research.md
  형식: AGENT.md의 "researcher 결과 저장 방법" 참조

STEP 3. [G1 게이팅] 사용자에게 전달
  내용: 주제 후보 12개 전체 (profit_type·monetize·trend_score 포함)
  질문: "이번 주 우선순위가 유입 확대 / 전환·매출 / 신뢰 구축 중 어느 쪽인가요?"
  대기: 사용자 6개 선택 완료까지

STEP 4. 오케스트레이터: 확정 주제 6개 weekly/research.md에 기입

STEP 5. 포맷별 워크플로 트리거
  각 주제에 대해 format_hint에 따라:
  → 릴스: workflow-reels.md
  → 캐러셀: workflow-carousel.md
  → 스토리: workflow-story.md (캐러셀/릴스 완료 후)
```
