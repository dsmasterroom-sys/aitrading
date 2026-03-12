# CLAUDE.md — @gena_feed 공통 참조

모든 에이전트는 이 파일을 먼저 읽습니다.

---

## 프로젝트 개요

- **계정**: @gena_feed (인스타그램 AI 자동화)
- **모계정**: @genarchive.kr
- **판매 제품**: slant 미니 슬링백
- **발행**: 릴스(금 19:00) · 캐러셀(수 12:00) · 스토리(화/수/토)

---

## gena 말투 원칙 (필수)

- 가볍고 친근하게, 딱딱한 존댓말 금지
- 문장당 15자 이내, 짧고 끊어서
- 이모지 슬라이드당 최대 2개
- 엣지 있는 감각

**좋은 예**: "이거 몰랐으면 진짜 억울했을 뻔"
**나쁜 예**: "꼭 알아야 할 중요한 정보입니다"

---

## 에이전트 구조

| 에이전트 | 스킬 파일 | Write 권한 | 담당 |
|----------|-----------|-----------|------|
| researcher | research-trend.md | ❌ | 트렌드 리서치 |
| contents-marketer | plan-content.md, write-copy.md | ✅ | 기획·카피 |
| designer | design-visual.md | ✅ | 비주얼 기획 |
| developer | build-html.md | ✅ | HTML·Nanogen |
| qa-reviewer | qa-check.md | ❌ | 검수 전담 |
| orchestrator | AGENT.md | 제한적 | 라우팅·게이팅 |

**단일 책임 원칙 - 역할 침범 절대 금지**

---

## 파일 구조

```
gena_feed/
├── STATUS.md          ← 현재 상태 (세션 재시작 시 필독)
├── CLAUDE.md          ← 이 파일
├── AGENT.md           ← 오케스트레이터
├── skills/            ← 에이전트 스킬
├── workflows/         ← 워크플로우
├── scripts/           ← 실행 스크립트
├── assets/            ← 공용 자산
├── weekly/            ← 주간 작업
└── output/            ← 산출물
```

---

## 환경변수 (.env)

```
NANOGEN_BASE_URL=http://localhost:8000
BUFFER_API_KEY=your_buffer_api_key
```

**절대 Git 커밋 금지**

---

## Nanogen 통합

```
서버:    http://localhost:8000
이미지:  POST /api/generate-image
동영상:  POST /api/generate-video
Outfit Swap: config.mode = "composition"
```

### 공용 자산
- `assets/gena-base.png` - Outfit Swap 베이스
- `assets/slant-product.png` - 제품 이미지
- `assets/outfit/` - Outfit Grid Reference

---

## 수익 연동

- **slant CTA**: 캐러셀 7장 + 스토리 D+3 + 릴스 S6
- **링크바이오 안내 필수**
- **광고 표기**: L3 협찬 시 `#ad` 또는 `[브랜드명] 협찬`

---

## 절대 금지

1. 광고 표기 누락
2. 게이팅(G1·G2·G3) 없이 다음 단계 진행
3. 에이전트 역할 침범
4. `.env` Git 커밋
5. 스킬 파일 150줄 초과

---

**상세 규칙**: `AGENT.md`, `skills/*.md` 참조
