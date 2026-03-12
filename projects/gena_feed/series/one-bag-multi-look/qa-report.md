# QA Report — one-bag-multi-look

## 검증 일시: 2026-03-10

---

## Step 1 — 기술 검증

| 항목 | 결과 |
|------|------|
| 캔버스 크기 (1080×1350) | PASS — 8장 모두 1080×1350px 확인 |
| 텍스트 캔버스 밖 이탈 | PASS — 이탈 없음 |
| 최소 폰트 28px | PASS — var(--fs-caption) = 28px 최소값 |
| 외부 URL 참조 | **FAIL** — Google Fonts CDN @import 8건 |
| overflow: hidden | PASS |
| word-break: keep-all | PASS |
| 텍스트 오버레이 얼굴 가림 | PASS — slide_04, slide_06 하단 배치 수정 완료 |

## Step 2 — 콘텐츠 검증

### 카피 대조 (copy.md ↔ 슬라이드)

| 슬라이드 | 헤드라인 | 본문 | 강조 | 결과 |
|---------|---------|------|------|------|
| 01 | 가방 하나로 3가지 룩, 가능할까? | — | 3가지 룩 (빨간색) | PASS |
| 02 | 아침마다 이 고민, 나만 하는 거 아니지? | 옷은 골랐는데 가방이 안 맞아서 다시 처음부터. | — | PASS |
| 03 | 답은 소재에 있었어 | 매트 나일론 하나면 캐쥬얼부터 스트릿까지 전부 커버. | 소재 (빨간색) | PASS |
| 04 | LOOK 1 캐쥬얼 | 가디건 + 와이드 데님에 크로스백으로 가볍게. | — | PASS |
| 05 | LOOK 2 미니멀 | 블레이저 + 슬랙스에 숄더백으로 깔끔하게. | — | PASS |
| 06 | LOOK 3 스트릿 | 레더 재킷 + 스커트에 힙색으로 포인트. | — | PASS |
| 07 | 왜 이 가방이냐면 | 매트 나일론 · YKK 지퍼 · 조절 버클 스트랩 / 작지만 다 들어가. | 작지만 다 들어가 (bold) | PASS |
| 08 | 저장해두고 내일 바로 써먹어 | @gena_feed 팔로우하면 다음 주 원백 멀티룩 릴스도 볼 수 있어. | 원백 멀티룩 릴스 (빨간색) | PASS |

### 브랜드 톤
- 금지 표현 사용: 없음 — PASS
- 강조 슬라이드당 2개 이내: PASS
- 이모지: 0건 — PASS

## Step 3 — 나노젠 이미지 검증

| 항목 | 결과 |
|------|------|
| [HIGH] 인물: 젠아 레퍼런스 사용 | PASS — 3-phase pipeline으로 페르소나 적용 |
| [HIGH] 협찬 제품: 색상·형태 일치 | PASS — genarchive crossbag 블랙, 형태 일관 |
| @gena_feed 무드 (Korean aesthetic, muted tones) | PASS — 쿨톤 Overcast 조명 통일 |
| Garment Swap: 모델 정체성·배경 보존 | PASS |

## Step 4 — 이슈 리포트

### HIGH (즉시 수정 — developer에게 전달)
- 없음

### MID (수정 필요)
- [전체] Google Fonts CDN `@import url(...)` 8건 → 외부 URL 참조 금지 규칙 위반. 단, PNG 추출 시 puppeteer가 네트워크 접근하므로 렌더링에는 정상 반영됨. 오프라인 환경이나 향후 재빌드 시 폰트 누락 가능.
  → **수정 지시**: `@import` 제거하고 시스템 폰트 fallback 사용 또는 로컬 폰트 파일 인라인

### LOW (기록 후 다음 회차 반영)
- [slide_08] 하단 여백이 넓음 — CTA 버튼과 @gena_feed 사이 공간 많음. 레이아웃 조밀하게 조정 검토.
- [slide_05] 인물 헤어스타일(더블 다운 브레이드)이 미니멀/오피스룩과 약간 불일치 — 다음 회차 시 straight 헤어 고려.

---

**HIGH + MID 합산: MID 1건 (Google Fonts CDN)**

→ MID 이슈 수정 후 QA 통과 가능
