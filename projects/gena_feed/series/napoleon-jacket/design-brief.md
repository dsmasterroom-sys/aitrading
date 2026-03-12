# design-brief — 나폴레옹 자켓 캐러셀

> 시리즈: napoleon-jacket | 슬라이드: 10장 | 캔버스: 1080×1350px
> 작성일: 2026-03-11

## 1. 시리즈 조명 결정

**전체 조명: [Overcast] — 시크/모던 통일**
- 5500-6500K, 낮은 대비, desaturated -15%
- 자켓의 구조적 라인과 골드 버튼 디테일을 쿨톤에서 부각
- 전 슬라이드 동일 적용 (예외 없음)

## 2. 서피스 리듬

| # | 서피스 | 텍스트 컬러 |
|---|--------|-----------|
| 01 | 이미지 풀블리드 (오버캐스트) | var(--text-light) |
| 02 | var(--surface-cream) | var(--text-dark) |
| 03 | var(--surface-cool) | var(--text-dark) |
| 04 | var(--surface-dark) | var(--text-light) |
| 05 | 이미지 + var(--surface-cream) | var(--text-dark) |
| 06 | var(--surface-cool) | var(--text-dark) |
| 07 | 이미지 풀블리드 (오버캐스트) | var(--text-light) |
| 08 | 이미지 + var(--surface-cream) | var(--text-dark) |
| 09 | 이미지 풀블리드 (오버캐스트) | var(--text-light) |
| 10 | var(--surface-dark) | var(--text-light) + var(--surface-accent) |

## 3. 슬라이드별 비주얼 기획서

### slide-01 (표지/훅)
| 항목 | 사양 |
|------|------|
| 구조 | overlay-bottom |
| 주인공 시각 요소 | 젠아 사이드 프로필, 나폴레옹 자켓 골드 버튼 강조, 도심 거리 배경 |
| 색상 토큰 | 이미지 위 그라데이션 → var(--text-light), var(--surface-accent) "같은 자켓" 강조 |
| 조명 조건 | [Overcast] 5500-6500K |
| 나노젠 이미지 생성 | **Yes** |
| 헤어 | gena_ref_02_medium_straight.png |
| 의상 | 차콜-블랙 나폴레옹 자켓 (골드 더블 브레스트 버튼), 블랙 슬림 팬츠, 앵클부츠 |

### slide-02 (공감)
| 항목 | 사양 |
|------|------|
| 구조 | quote-hero |
| 주인공 시각 요소 | 대형 타이포 "피드에 계속 뜨는 이 자켓" |
| 색상 토큰 | 배경 var(--surface-cream), 텍스트 var(--text-dark), 강조 var(--text-mid) |
| 나노젠 이미지 생성 | **No** |

### slide-03 (전환)
| 항목 | 사양 |
|------|------|
| 구조 | grid-2x2 변형 (키워드 카드 3개 + 서브텍스트) |
| 주인공 시각 요소 | "밀리터리 x 페미닌", "구조적 x 부드러움", "미코노미" 키워드 |
| 색상 토큰 | 배경 var(--surface-cool), 카드 var(--surface-cream), 텍스트 var(--text-dark) |
| 나노젠 이미지 생성 | **No** |

### slide-04 (셀럽 비교)
| 항목 | 사양 |
|------|------|
| 구조 | grid-2x2 변형 → 3×1 세로 그리드 |
| 주인공 시각 요소 | 셀럽 3인 영역 (타이포+아이콘) + 무드 키워드 |
| 색상 토큰 | 배경 var(--surface-dark), 텍스트 var(--text-light), 무드 키워드 var(--surface-accent) |
| 나노젠 이미지 생성 | **No** |

### slide-05 (디테일 해부)
| 항목 | 사양 |
|------|------|
| 구조 | split-50 (좌: 이미지 / 우: 텍스트) |
| 주인공 시각 요소 | 좌: 나폴레옹 자켓 매크로 클로즈업 / 우: 디테일 3가지 넘버링 |
| 색상 토큰 | 우 var(--surface-cream), 넘버 var(--surface-accent) |
| 조명 조건 | [Overcast] 소프트 디퓨즈드 |
| 나노젠 이미지 생성 | **Yes** |
| 의상 | 나폴레옹 자켓 단독 (다크 네이비/차콜, 골드 버튼, 스탠드칼라) |

### slide-06 (체형별 가이드)
| 항목 | 사양 |
|------|------|
| 구조 | step-flow (체형 3유형 수직 배열) |
| 주인공 시각 요소 | 체형 유형 아이콘 + 추천 디자인 키워드 |
| 색상 토큰 | 배경 var(--surface-cool), 카드 var(--surface-cream), 포인트 var(--surface-accent) |
| 나노젠 이미지 생성 | **No** |

### slide-07 (룩1 — 출근)
| 항목 | 사양 |
|------|------|
| 구조 | overlay-bottom |
| 주인공 시각 요소 | 젠아 출근 룩 전신, 오피스 빌딩 로비/계단, 로우앵글 워킹 |
| 색상 토큰 | var(--text-light), 아이템 라벨 var(--surface-cream) 배지 |
| 조명 조건 | [Overcast] 5500-6500K |
| 나노젠 이미지 생성 | **Yes** |
| 헤어 | gena_ref_03_basic_straight.png |
| 의상 | 차콜 나폴레옹 자켓 + 와이드 슬랙스 + 블랙 로퍼 + Burnished Lilac 스카프 |

### slide-08 (룩2 — 주말)
| 항목 | 사양 |
|------|------|
| 구조 | split-50 (좌: 이미지 / 우: 텍스트) |
| 주인공 시각 요소 | 좌: POV 셀피, 성수 골목 배경 / 우: 아이템 리스트 |
| 색상 토큰 | 우 var(--surface-cream), Muskmelon(#E8A87C) 포인트 |
| 조명 조건 | [Overcast] 디퓨즈드 라이트 |
| 나노젠 이미지 생성 | **Yes** |
| 헤어 | gena_ref_08_double_down_braid.png |
| 의상 | 블랙 나폴레옹 자켓 + 와이드 데님 + 화이트 스니커즈 + Muskmelon 토트백 |

### slide-09 (룩3 — 데이트 + 협찬)
| 항목 | 사양 |
|------|------|
| 구조 | overlay-bottom |
| 주인공 시각 요소 | 젠아 뒷모습/3/4 앵글, 한남동 거리, 크로스백 자연 착용 |
| 색상 토큰 | var(--text-light), 협찬 라벨 var(--surface-cream) 배지 |
| 조명 조건 | [Overcast] 5500-6500K |
| 나노젠 이미지 생성 | **Yes** |
| 헤어 | gena_ref_07_long_halfupdown_wave.png |
| 의상 | 그레이 나폴레옹 자켓 + 아이보리 새틴 미디스커트 + 누드 힐 + 베이비 핑크 캐미솔 |
| 협찬 | @genarchive.kr 미니크로스백, UGC 자연 착용 |
| 협찬 이미지 | shared/products/genarchive_crossbag/ (fit + 4-view) |

### slide-10 (CTA)
| 항목 | 사양 |
|------|------|
| 구조 | cta-centered |
| 주인공 시각 요소 | 대형 타이포 + 저장/팔로우 CTA |
| 색상 토큰 | 배경 var(--surface-dark), 헤드라인 var(--text-light), "트렌치코트" var(--surface-accent) |
| 나노젠 이미지 생성 | **No** |

## 4. 다양성 검증

| 검증 항목 | 결과 |
|----------|------|
| 앵글 | 5종 (사이드/매크로/로우앵글/POV셀피/뒷모습3/4) |
| 스타일 변형 | 4종 (시네마틱/스트릿다큐/UGC캔디드/제품히어로) |
| 장소 카테고리 | 3종 (도심스트릿/인테리어/혼합) |
| 헤어 | 4종 모두 다름 (02/03/08/07) |
| 서피스 2연속 | 없음 |
| 앵글 2연속 | 없음 |

## 5. 룩별 의상 레퍼런스

| 룩 | 의상 | 레퍼런스 출처 | 헤어 |
|----|------|-------------|------|
| 표지 (01) | 다크 나폴레옹 자켓 + 블랙 슬림팬츠 + 앵클부츠 | flat-lay 생성 | gena_ref_02 |
| 출근 (07) | 차콜 자켓 + 와이드 슬랙스 + 로퍼 + 라일락 스카프 | flat-lay 생성 | gena_ref_03 |
| 주말 (08) | 블랙 자켓 + 와이드 데님 + 스니커즈 + 머스크멜론 토트 | flat-lay 생성 | gena_ref_08 |
| 데이트 (09) | 그레이 자켓 + 새틴 스커트 + 힐 + 핑크 캐미 + 크로스백 | flat-lay 생성 | gena_ref_07 |
