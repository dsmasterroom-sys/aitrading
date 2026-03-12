# QA Report — napoleon-jacket carousel
Date: 2026-03-11

## Summary
- HIGH issues: 2
- MID issues: 3
- LOW issues: 3
- PASS: 14

## Issues

### [HIGH] slide-08 레이아웃: design-brief와 구현 불일치
- Slide: 08
- Category: DESIGN
- Description: design-brief에서 slide-08은 `split-50 (좌: 이미지 / 우: 텍스트)` 구조로 기획되었으나, 실제 HTML 구현은 `overlay-bottom` (풀블리드 이미지 + 하단 그라데이션 오버레이) 구조로 되어 있다. plan.md에서도 "분할 50/50 — 좌: 전신 이미지 / 우: 아이템 리스트 + 스타일 팁"으로 명시했으나 미반영.
- Fix: slide_08.html을 split-50 레이아웃으로 재구현. 좌측 50%에 이미지, 우측 50%에 var(--surface-cream) 배경 + 아이템 리스트 텍스트 배치. slide-05와 같은 구조 참조.

### [HIGH] slide-09 협찬 제품 불일치 — @genarchive.kr 미니크로스백이 아닌 토트백 노출
- Slide: 09
- Category: BRAND
- Description: design-brief에서 slide-09는 "@genarchive.kr 미니크로스백, UGC 자연 착용"으로 기획되었고, copy.md의 slide-08에서 "@genarchive.kr 크로스백"을 언급한다. 그러나 slide-09의 생성 이미지에서 모델이 들고 있는 가방은 블랙 우븐 토트백으로 보이며, 미니크로스백과 형태가 다르다. 협찬 제품 고증 원칙(brand-identity.md: "제품 색상·형태·로고 임의 생성 절대 금지") 위반.
- Fix: slide-09 이미지를 shared/products/genarchive_crossbag/ 레퍼런스를 참조하여 재생성. 미니크로스백 형태(크로스바디 스트랩 + 소형 박스형)가 정확히 반영되어야 함.

### [MID] slide-05 하드코딩된 font-size 값 (CSS 변수 미사용)
- Slide: 05
- Category: DESIGN
- Description: slide_05.html에서 `.slide-05 .headline`에 `font-size: 44px`, `.slide-05 .item-text`에 `font-size: 30px`를 직접 하드코딩했다. design-tokens.css 규칙("슬라이드 HTML에서 하드코딩 금지")에 위반된다. 30px는 --fs-caption(28px)보다 크므로 최소 크기 위반은 아니나, 토큰 시스템 일관성을 해친다.
- Fix: `.slide-05 .headline`의 font-size를 `var(--fs-title)` (56px)로 변경하거나, 공간이 부족하다면 별도 커스텀 변수를 :root에 추가. `.slide-05 .item-text`는 `var(--fs-caption)` (28px) 또는 `var(--fs-body)` (36px)로 변경.

### [MID] slide-08 협찬 제품 이미지 — 크로스백 색상 불일치
- Slide: 08
- Category: BRAND
- Description: copy.md의 slide-08에서 "@genarchive.kr 크로스백"을 언급하며, design-brief에서 포인트 컬러로 "Muskmelon(#E8A87C) 토트백"을 지정했다. 그러나 생성 이미지에서 모델이 착용한 크로스백은 그레이/다크 컬러로 Muskmelon 톤이 아니다. 또한 design-brief에 명시된 "와이드 데님 + 화이트 스니커즈"가 아닌 진한 데님에 스니커즈가 잘 보이지 않는 구도이다.
- Fix: slide-08 이미지 재생성 시 (1) 크로스백을 genarchive 제품 레퍼런스와 일치시키고, (2) 전신 구도에서 화이트 스니커즈와 와이드 데님이 보이도록 구도 조정.

### [MID] slide-04 하단 여백 과다 — 그리드가 상단에 치우침
- Slide: 04
- Category: DESIGN
- Description: slide-04의 PNG 출력에서 셀럽 3인 그리드가 캔버스 상단~중앙에 위치하고, 하단 약 1/3이 빈 공간으로 남아있다. 정보 밀도 HIGH 슬라이드로서 공간 활용이 비효율적이다.
- Fix: `.slide-04 .grid`의 flex 정렬을 조정하여 그리드를 수직 중앙으로 배치하거나, 카드 높이를 키워서 캔버스를 채움. 또는 하단에 서브텍스트(예: "같은 아이템, 다른 연출")를 추가.

### [LOW] overlay 그라데이션에 rgba 하드코딩
- Slide: 01, 07, 08, 09
- Category: TECHNICAL
- Description: overlay 그라데이션에 `rgba(26,26,26,0.92)`, `rgba(26,26,26,0.6)` 등의 값이 하드코딩되어 있다. 이 값들은 var(--surface-dark)의 rgba 변형으로, CSS 변수로는 직접 알파 조절이 불가하므로 불가피한 부분이 있다.
- Fix: 다음 회차부터 `--overlay-dense: rgba(26,26,26,0.92)`, `--overlay-light: rgba(26,26,26,0.6)` 등을 design-tokens.css에 추가하여 통일. 이번 시리즈는 현 상태 유지 가능.

### [LOW] slide-02 텍스트 수직 위치 — 하단 여백 과다
- Slide: 02
- Category: DESIGN
- Description: slide-02의 PNG에서 텍스트 블록이 캔버스 중앙보다 약간 위에 위치하고, 하단에 큰 빈 공간이 남아있다. 타이포 중심 슬라이드로서 시각적 무게 중심이 상단에 쏠려 있다.
- Fix: `justify-content: center`가 적용되어 있으나, 텍스트 양이 적어서 하단이 비어 보임. 필수 수정은 아니나, body 텍스트 아래에 장식 요소(예: 화살표, 슬라이드 넘김 유도)를 추가하면 개선 가능.

### [LOW] slide-03 카드 3번 텍스트 글자 깨짐 의심
- Slide: 03
- Category: COPY
- Description: slide-03 PNG에서 카드 3번의 텍스트가 "이모순이 포인트"로 보인다. copy.md 원문은 "이 **모순이 포인트**"인데, HTML에서 `이 <span class="accent-text">모순이 포인트</span>`로 구현되어 "이"와 "모순이" 사이에 시각적 공백이 충분하지 않아 "이모순이"처럼 읽힐 수 있다.
- Fix: "이" 뒤에 명확한 공백 또는 줄바꿈을 넣어 "이 모순이 포인트"가 명확히 읽히도록 수정. 예: `이 <span>` 사이 `&nbsp;` 추가 또는 "이" 제거 후 "모순이 포인트"만 강조.

## Pass Items

1. **캔버스 크기**: 전 슬라이드 1080x1350px 정확 (PASS)
2. **overflow hidden**: 전 슬라이드 `.slide` 클래스에 `overflow: hidden` 적용 (PASS)
3. **외부 URL 없음**: 전 슬라이드 외부 URL 참조 없음, 모든 이미지 base64 인라인 (PASS)
4. **최소 폰트 크기**: 전 슬라이드 최소 28px 이상 (slide-05의 30px 포함) (PASS)
5. **CSS 토큰 색상**: :root 외부에 hex 색상 하드코딩 없음, 전체 var(--) 사용 (PASS)
6. **카피 일치**: 전 슬라이드 텍스트가 copy.md 원문과 일치 (PASS)
7. **이모지 규칙**: 슬라이드당 이모지 2개 이하 — slide-04(아이콘용 3개)는 UI 요소로 허용, slide-10(1개) (PASS)
8. **CTA 존재**: slide-10에 "저장 + 팔로우" CTA 명확히 배치 (PASS)
9. **해시태그 포맷**: slide-10에 #gena_봄아우터도감 포함 (PASS)
10. **협찬 disclosure**: slide-08에 "협찬" 라벨 표시 존재 (PASS)
11. **금지 표현 없음**: "정말/너무/완전" 남발, 근거 없는 최상급 표현 없음 (PASS)
12. **강조 규칙**: 전 슬라이드 강조(accent/bold) 2개 이내, strong 1개 이내 (PASS)
13. **레이아웃 다양성**: 5종 이상 사용 (overlay-bottom, quote-hero, card, grid, split-50, step-flow, cta-centered) — 같은 레이아웃 2연속 없음 (PASS)
14. **앵글 다양성**: 사이드 프로필(01), 매크로(05), 로우앵글 워킹(07), POV셀피(08), 뒷모습 3/4(09) — 전부 다른 앵글 (PASS)
15. **서피스 리듬**: 같은 서피스 2연속 없음 — 이미지/cream/cool/dark/이미지+cream/cool/이미지/이미지/이미지/dark (PASS)
16. **브랜드 톤**: 친근하고 공감 가는 MZ 말투, 정보 기반 전달 유지 (PASS)
17. **감정 곡선**: plan.md 감정 온도 패턴과 실제 슬라이드 강도 흐름 일치 (PASS)
18. **다음편 예고**: slide-10에 "트렌치코트" 예고 포함, 시리즈 연결 (PASS)

## DESIGN (디자인 품질)

### [MID] slide-07~08~09 연속 풀블리드 이미지 — 시리즈 리듬 단조
- Slide: 07, 08, 09
- Category: DESIGN
- Description: slide-07, 08, 09가 모두 풀블리드 이미지 + 하단 오버레이 구조로, 3장 연속 같은 레이아웃 패턴이다. slide-08이 design-brief대로 split-50으로 구현되었다면 해결되었을 문제이나, 현재는 3연속 동일 구조로 시각적 단조로움이 발생한다.
- Fix: slide-08을 design-brief 원안대로 split-50 레이아웃으로 변경하면 자연스럽게 해결됨. (HIGH 이슈 #1과 동일 수정으로 해결)

---

## 최종 판정

**HIGH 2건 + MID 3건 + DESIGN MID 1건 = 총 6건 수정 필요**

> QA 미통과 — developer에게 HIGH/MID 이슈 전달 후 수정 필요

### 수정 우선순위
1. [HIGH] slide-08 레이아웃을 split-50으로 재구현 (이 수정으로 DESIGN MID 리듬 이슈도 동시 해결)
2. [HIGH] slide-09 이미지 재생성 — genarchive 미니크로스백 레퍼런스 반영
3. [MID] slide-08 이미지 재생성 — 크로스백 형태/색상 + 전신 구도 수정
4. [MID] slide-05 하드코딩 font-size를 CSS 변수로 교체
5. [MID] slide-04 그리드 수직 정렬 개선
