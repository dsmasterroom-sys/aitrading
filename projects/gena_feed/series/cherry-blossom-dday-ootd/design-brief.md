# cherry-blossom-dday-ootd — 비주얼 기획서

## 조명 조건 (전체 통일)

**[Golden Hour]** — 웜톤 3500-4500K, 긴 그림자, 골든 림라이트+쿨 섀도우

선택 근거: 벚꽃 + 봄 OOTD의 페미닌/감성 무드에 최적. 핑크 벚꽃과 골든 웜톤의 색감 시너지. Kodak Portra 400 에뮬레이션과 자연스럽게 결합.

---

## 배경 색상 리듬 (10장)

| 순서 | 역할 | 배경 토큰 |
|------|------|----------|
| 01 | Cover | var(--surface-dark) |
| 02 | Empathy | var(--surface-cream) |
| 03 | Transition | var(--surface-cool) |
| 04 | Info 1 | var(--surface-cream) |
| 05 | Info 2 | var(--surface-mid) |
| 06 | Info 3 | var(--surface-dark) |
| 07 | Evidence 1 | var(--surface-accent) |
| 08 | Evidence 2 | var(--surface-dark) |
| 09 | Action | var(--surface-cream) |
| 10 | CTA | var(--surface-dark) |

---

## 슬라이드별 비주얼 기획

### slide-01 | 표지 / 훅

- **구조**: overlay-bottom (참조: editorial/EDI-08)
- **주인공 시각 요소**: 만개 직전 벚꽃 가로수길 풀블리드 사진. 소프트 핑크 보케. 하단에 "D-20" 대형 디스플레이 타이포(--fs-display, 72px+) 오버레이. 카운트다운 숫자에 var(--accent) 적용하여 긴박감 부여
- **배경 색상 토큰**: var(--surface-dark) — 이미지 위 반투명 다크 그라데이션 오버레이
- **텍스트 색상 토큰**: 헤드라인 var(--text-light), "D-20" 강조 var(--accent)
- **조명 조건**: [Golden Hour] — 벚꽃잎에 골든 림라이트, 가로수 그림자 길게
- **나노젠 이미지 생성**: Yes — 벚꽃 가로수길 풍경 (인물 없음)
- **영상 생성**: No

---

### slide-02 | 공감

- **구조**: quote-hero (참조: editorial/EDI-15)
- **주인공 시각 요소**: 크림 배경 위 메모카드/포스트잇 스타일 카드 2-3개. 손글씨 느낌 타이포. 벚꽃잎 일러스트 포인트(CSS로 구현). "옷 고르다 만개 놓치고" / "결국 패딩에 운동화" / "사진 속 나만 계절 무시" 각각 카드로 분리
- **배경 색상 토큰**: var(--surface-cream)
- **텍스트 색상 토큰**: 헤드라인 var(--text-dark), 본문 var(--text-mid)
- **조명 조건**: N/A (타이포/일러스트 슬라이드)
- **나노젠 이미지 생성**: No
- **영상 생성**: No

---

### slide-03 | 전환

- **구조**: hero-center (참조: blackwhite/BW-05)
- **주인공 시각 요소**: 중앙 정렬 대형 타이포. "3~8일 빠르다"를 --fs-display 크기로 강조. 상단에 "올해 개화, 평년보다" 서브텍스트. 하단에 캘린더 아이콘 CSS 요소. 미니멀 쿨톤 배경
- **배경 색상 토큰**: var(--surface-cool)
- **텍스트 색상 토큰**: 강조 "3~8일 빠르다" var(--accent), 서브텍스트 var(--text-dark)
- **조명 조건**: N/A (타이포 중심 슬라이드)
- **나노젠 이미지 생성**: No
- **영상 생성**: No

---

### slide-04 | 정보 — 개화 일정

- **구조**: split-50 (참조: editorial/EDI-22)
- **주인공 시각 요소**: 좌측 — 세로 타임라인 인포그래픽 (제주 3/20~25 → 부산 3/23~25 → 서울 개화 3/30~4/2 → 서울 만개 4/6~13). 타임라인 라인에 핑크 그라데이션. "서울 만개 4/6~13"에 var(--accent) 배지. 우측 — 소프트 포커스 벚꽃 나무 클로즈업 이미지
- **배경 색상 토큰**: var(--surface-cream)
- **텍스트 색상 토큰**: 헤드라인 var(--text-dark), 날짜 var(--text-mid), 서울 만개 강조 var(--accent)
- **조명 조건**: [Golden Hour] — 우측 이미지에 적용, 웜톤 벚꽃 클로즈업
- **나노젠 이미지 생성**: Yes — 벚꽃 나무 클로즈업 (인물 없음, 소프트 포커스)
- **영상 생성**: No

---

### slide-05 | 정보 — 룩1 시어 레이어링

- **구조**: overlay-bottom (참조: editorial/EDI-03)
- **주인공 시각 요소**: 벚꽃 가로수 아래 걷는 젠아 전신 착장컷 풀블리드. 시어 톱 레이어링 디테일 보이도록 자연광 역광. gen archive 크로스백 숄더 착용 자연 노출. 하단 반투명 오버레이에 "룩1. 시어 레이어링" 텍스트
- **배경 색상 토큰**: var(--surface-mid) — 이미지 하단 오버레이 베이스
- **텍스트 색상 토큰**: 헤드라인 var(--text-light), "딥그린" 강조 var(--text-light)
- **조명 조건**: [Golden Hour] — 역광 골든 림라이트, 시어 소재 투과광 강조
- **나노젠 이미지 생성**: Yes — Phase 1(flat-lay) + Phase 2(composition) + Phase 3(final scene)
- **영상 생성**: No
- **협찬 제품 노출**: gen archive 슬런트 크로스백 / 숄더 착용 / UGC 자연 노출 / shared/products/genarchive_crossbag/

---

### slide-06 | 정보 — 룩2 트렌치코트 재해석

- **구조**: grid-2x2 (참조: bentoretro/BEN-12)
- **주인공 시각 요소**: 3분할 그리드 — (1) 메인: 트렌치 착장 반신컷, 블랙 베이스 톤 (2) 서브 좌하: 크로스백 매트 블랙 나일론 질감 매크로 클로즈업 (3) 서브 우하: 웨이스트백 착용 디테일컷. 다크 배경에 차분한 그레이-블랙 톤 통일
- **배경 색상 토큰**: var(--surface-dark)
- **텍스트 색상 토큰**: 헤드라인 var(--text-light), "3way" 강조 var(--accent)
- **조명 조건**: [Golden Hour] — 낮은 각도 사이드라이트, 트렌치 소재 질감 강조
- **나노젠 이미지 생성**: Yes — Phase 1(flat-lay) + Phase 2(composition) + Phase 3(final scene) x3컷 (반신, 매크로, 디테일)
- **영상 생성**: No
- **협찬 제품 노출**: gen archive 슬런트 크로스백 / 웨이스트백 착용 / UGC 자연 노출 / shared/products/genarchive_crossbag/

---

### slide-07 | 증거 — 룩3 + 데이터

- **구조**: product-card (참조: editorial/EDI-18)
- **주인공 시각 요소**: 상단 1/3 — 데이터 카드: "200%↑" 대형 타이포(--fs-display) + var(--accent) 컬러. "에이블리 기준, 계절 모티프 의류 거래액" 서브텍스트. 하단 2/3 — 카페 테라스에서 커피 들고 있는 젠아 반신 착장컷, 딥올리브 니트 포인트, 크로스백 숄더 착용
- **배경 색상 토큰**: var(--surface-accent) — 상단 데이터 카드 영역, 하단은 이미지
- **텍스트 색상 토큰**: "200%↑" var(--text-light) on accent, 서브텍스트 var(--text-light)
- **조명 조건**: [Golden Hour] — 카페 테라스 자연광, 커피잔에 골든 리플렉션
- **나노젠 이미지 생성**: Yes — Phase 1(flat-lay) + Phase 2(composition) + Phase 3(final scene)
- **영상 생성**: No
- **협찬 제품 노출**: gen archive 슬런트 크로스백 / 숄더 착용 / UGC 자연 노출 / shared/products/genarchive_crossbag/

---

### slide-08 | 증거 — 룩4 + 제철코어

- **구조**: split-50 (참조: editorial/EDI-10)
- **주인공 시각 요소**: 좌측 — "제철코어" 키워드 대형 타이포(--fs-title) + 해설 본문. 벚꽃잎 흩날리는 CSS 그래픽 요소. 우측 — 공원 벤치에 앉은 젠아 릴랙스 포즈 전신컷. 와이드 카고 + 크롭 후디, 크로스백 크로스 착용. 자연광 소프트 톤
- **배경 색상 토큰**: var(--surface-dark)
- **텍스트 색상 토큰**: "제철코어" 강조 var(--accent), 본문 var(--text-light)
- **조명 조건**: [Golden Hour] — 낮은 사이드라이트, 공원 나무 사이로 들어오는 골든 빔
- **나노젠 이미지 생성**: Yes — Phase 1(flat-lay) + Phase 2(composition) + Phase 3(final scene)
- **영상 생성**: No
- **협찬 제품 노출**: gen archive 슬런트 크로스백 / 크로스 착용 / UGC 자연 노출 / shared/products/genarchive_crossbag/

---

### slide-09 | 실천 — 체크리스트

- **구조**: checklist (참조: editorial/EDI-25)
- **주인공 시각 요소**: 체크박스 4항목 수직 나열. 각 항목에 미니 아이콘(CSS). 하단에 벚꽃잎 일러스트 장식. 심플하고 저장 욕구를 자극하는 정돈된 레이아웃. "캘린더 저장" 항목에 var(--accent) 하이라이트
- **배경 색상 토큰**: var(--surface-cream)
- **텍스트 색상 토큰**: 헤드라인 var(--text-dark), 체크항목 var(--text-mid), "캘린더 저장" var(--accent)
- **조명 조건**: N/A (타이포/일러스트 슬라이드)
- **나노젠 이미지 생성**: No
- **영상 생성**: No

---

### slide-10 | CTA

- **구조**: cta-centered (참조: editorial/EDI-30)
- **주인공 시각 요소**: 만개 벚꽃 터널 풍경 풀블리드. 소프트 핑크 톤. 중앙에 "저장 한 번이면 OOTD 끝" CTA 문구. 저장 아이콘 CSS 그래픽. slide-01과 시각적 대칭(bookend). 반투명 다크 오버레이로 텍스트 가독성 확보
- **배경 색상 토큰**: var(--surface-dark) — 오버레이
- **텍스트 색상 토큰**: CTA "저장" 강조 var(--accent), 나머지 var(--text-light)
- **조명 조건**: [Golden Hour] — 터널 끝에서 들어오는 골든 역광
- **나노젠 이미지 생성**: Yes — 만개 벚꽃 터널 풍경 (인물 없음)
- **영상 생성**: No

---

## 젠아 헤어 파일 지정

| 슬라이드 | 룩 | 무드 | 헤어 파일 |
|---------|-----|------|----------|
| slide-05 | 룩1 시어 레이어링 | 페미닌/감성 | `gena_ref_07_long_halfupdown_wave.png` |
| slide-06 | 룩2 트렌치코트 | 시크/모던 | `gena_ref_02_medium_straight.png` |
| slide-07 | 룩3 미니멀 캐주얼 | 캐주얼/시크 | `gena_ref_03_basic_straight.png` |
| slide-08 | 룩4 스트릿 캐주얼 | 캐주얼/힙 | `gena_ref_08_double_down_braid.png` |

---

## 룩별 의상 디테일

### 룩1 — 시어 레이어링 (slide-05)

| 아이템 | 디테일 |
|--------|--------|
| 상의(이너) | 차콜 슬리브리스 탱크탑, 리브 니트 소재 |
| 상의(아우터) | 딥그린 시어 롱슬리브 톱, 메시 소재, 루즈핏 |
| 하의 | 차콜 와이드 슬랙스, 하이웨이스트 |
| 신발 | 블랙 로퍼 (미니멀) |
| 가방 | gen archive 슬런트 크로스백 — 숄더 착용 |

- 의상 레퍼런스: 나노젠 Phase 1 flat-lay 생성
- 페르소나 헤어: `gena_ref_07_long_halfupdown_wave.png`

### 룩2 — 트렌치코트 재해석 (slide-06)

| 아이템 | 디테일 |
|--------|--------|
| 아우터 | 블랙 오버사이즈 트렌치코트, 벨트 루즈하게 묶음 |
| 상의 | 블랙 크루넥 티, 슬림핏 |
| 하의 | 블랙 스트레이트 진 |
| 신발 | 블랙 첼시부츠 |
| 가방 | gen archive 슬런트 크로스백 — 웨이스트백 착용 |

- 의상 레퍼런스: 나노젠 Phase 1 flat-lay 생성
- 페르소나 헤어: `gena_ref_02_medium_straight.png`

### 룩3 — 미니멀 캐주얼 (slide-07)

| 아이템 | 디테일 |
|--------|--------|
| 상의 | 딥올리브 크루넥 니트, 미디엄 게이지 |
| 하의 | 라이트 그레이 와이드 슬랙스 |
| 신발 | 화이트 캔버스 스니커즈 |
| 레이어 | 그레이 라이트 가디건 (어깨에 걸침) |
| 가방 | gen archive 슬런트 크로스백 — 숄더 착용 |

- 의상 레퍼런스: 나노젠 Phase 1 flat-lay 생성
- 페르소나 헤어: `gena_ref_03_basic_straight.png`

### 룩4 — 스트릿 캐주얼 (slide-08)

| 아이템 | 디테일 |
|--------|--------|
| 상의 | 딥포레스트그린 크롭 후디, 드로스트링 |
| 하의 | 카키 와이드 카고팬츠, 멀티포켓 |
| 신발 | 블랙 청키 스니커즈 |
| 가방 | gen archive 슬런트 크로스백 — 크로스 착용 |
| 액세서리 | 실버 링 1개 |

- 의상 레퍼런스: 나노젠 Phase 1 flat-lay 생성
- 페르소나 헤어: `gena_ref_08_double_down_braid.png`

---

## 협찬 제품 노출 정리

| 슬라이드 | 착용 방식 | 노출 방식 | 제품 경로 |
|---------|----------|----------|----------|
| slide-05 | 숄더 | UGC 자연 노출 | shared/products/genarchive_crossbag/ |
| slide-06 | 웨이스트백 | UGC 자연 노출 (3way 디테일) | shared/products/genarchive_crossbag/ |
| slide-07 | 숄더 | UGC 자연 노출 | shared/products/genarchive_crossbag/ |
| slide-08 | 크로스 | UGC 자연 노출 | shared/products/genarchive_crossbag/ |

---

## 나노젠 이미지 생성 요약

| 슬라이드 | 생성 대상 | Phase |
|---------|----------|-------|
| 01 | 벚꽃 가로수길 풍경 (인물X) | Phase 3 only |
| 04 | 벚꽃 나무 클로즈업 (인물X) | Phase 3 only |
| 05 | 룩1 착장 전신컷 | Phase 1 → 2 → 3 |
| 06 | 룩2 반신컷 + 매크로 + 디테일 (3컷) | Phase 1 → 2 → 3 x3 |
| 07 | 룩3 반신 착장컷 | Phase 1 → 2 → 3 |
| 08 | 룩4 전신 착장컷 | Phase 1 → 2 → 3 |
| 10 | 벚꽃 터널 풍경 (인물X) | Phase 3 only |

총 이미지 생성: 약 9컷
