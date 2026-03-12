---
name: schedule
agent: orchestrator
description: "주간 루틴 타이밍 + 게이팅 + 발행 체크리스트."
input: "주간 시작 (월요일), 이번 주 시즌/이슈 정보"
output: "주간 스케줄 실행 + 게이팅 관리"
---

# schedule SKILL

## 주간 루틴 타임라인

| 요일/시간 | 캐러셀 트랙 | 릴스 트랙 | 스토리 트랙 | 게이팅 |
|----------|------------|----------|------------|--------|
| 월 오전 | researcher → 주제 12개 | ↑ | ↑ | — |
| 월 오후 | 오케스트레이터 주제 저장 | ↑ | ↑ | ✅ **G1** |
| 화 오전 | plan-content 9장 기획 | plan-content 씬 6개 | plan-content 스토리 텍스트 | — |
| 화 오후 | write-copy + monetize | write-copy 자막 | write-copy 스토리 | ✅ **G2** |
| 화 19:00 | — | — | **스토리 D-1 발행** | — |
| 수 오전 | designer 레이아웃+이미지 | designer 씬 이미지 프롬프트 | — | — |
| 수 오후 | developer HTML→PNG | developer Nanogen I2V | developer Pillow 합성 | — |
| 수 완료 즉시 | slide-01.png → assets/thumb/ 복사 | scene-05.png → assets/reels/ 복사 | — | — |
| 수 12:00 | **캐러셀 발행** | — | **스토리 D+0 발행** | — |
| 목 오전 | qa-reviewer 캐러셀 QA | — | qa-reviewer 스토리 QA | — |
| 목 오후 | — | qa-reviewer 릴스 QA | — | — |
| 금 오전 | Buffer 예약 확인 | Buffer 예약 | — | ✅ **G3** |
| 금 19:00 | — | **릴스 발행** | — | — |
| 토 10:00 | — | — | **스토리 D+3 발행** | — |

## 수요일 병렬 처리 조건

- 캐러셀 HTML 구현 ↔ 릴스 이미지 생성 → 동시 실행 가능
- 릴스 동영상 변환 ↔ 스토리 PNG 합성 → 동시 실행 가능
- **조건**: 캐러셀 slide-01.png 완료 후 스토리 트랙 시작 (의존성)

## 발행 플랫폼

- Buffer 또는 Later로 예약 발행
- 스토리 투표·질문 스티커: 인스타 앱 내 직접 추가 (자동화 불가)

## 오케스트레이터 금지

콘텐츠 기획·카피 수정·HTML 코딩·QA 검증 직접 수행 금지
→ 위임, 라우팅, 게이팅, 자산 복사만 담당
