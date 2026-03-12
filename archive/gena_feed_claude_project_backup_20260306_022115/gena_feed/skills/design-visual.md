---
name: design-visual
agent: designer
description: "비주얼 기획 + 이미지 프롬프트 생성. 카피 작성·HTML·QA 금지."
input: "weekly/copy.md + weekly/content-plan.md or scene-plan.json"
output: "weekly/design-brief.md + weekly/image-prompts.json"
---

# design-visual SKILL

## 디자인 토큰 참조

모든 디자인 값은 `shared/design-tokens.css`의 CSS 변수만 사용합니다.
슬라이드 HTML에 직접 값 하드코딩 금지.

주요 토큰:
- `--accent: #C8A96E` (골드 포인트)
- `--dark: #1A1A2E` (딥 네이비)
- `--bg: #F5F3EF` (오프화이트)
- `--text: #3D3D3D` (본문)
- `--fs-title: 64px` / `--fs-body: 36px` / `--fs-tag: 28px` (최솟값)

## 캐러셀 레이아웃 패턴 (17개)

| 코드 | 유형 | 적합 장면 |
|------|------|----------|
| H-1 | 강조형: 풀블리드 다크 + 센터 타이틀 + 골드 언더라인 | 1장 훅 |
| H-2 | 강조형: 오프화이트 + 좌정렬 타이틀 + 골드 바 | 1장 훅 (부드러운) |
| H-3 | 강조형: 그라디언트 (dark→accent) | 1장 강렬 |
| I-1 | 정보형: 번호 배지 + 타이틀 + 본문 2줄 | 팁 3~6장 |
| I-2 | 정보형: 아이콘 + 타이틀 + 본문 좌정렬 | 감성 정보 |
| I-3 | 정보형: bg에 white 카드 인셋 | 고급스러운 팁 |
| I-4 | 정보형: 번호 리스트 (3항목 이내) | 요약·체크리스트 |
| I-5 | 정보형: 이미지 하프 + 텍스트 하프 | 아이템 설명 |
| P-1 | 절차형: 상→하 스텝 플로우 | 메이크업 순서 |
| P-2 | 절차형: 원형 배지 + 각 단계 | 3~4단계 |
| P-3 | 절차형: Before/After 2분할 | 전후 비교 |
| C-1 | 비교형: 좌우 2분할 A vs B | 제품 비교 |
| C-2 | 비교형: 상하 2분할 전/후 | 스타일 전후 |
| M-1 | 아이템형: 제품 풀블리드 + 하단 텍스트 | 7장 slant 메인 |
| M-2 | 아이템형: 제품 우측 60% + 좌측 텍스트 | 7장 파트너스 |
| CTA-1 | CTA형: 다크 배경 + 저장 아이콘 | 9장 구매 유도 |
| CTA-2 | CTA형: 오프화이트 + 골드 버튼 | 9장 저장+팔로우 |

**필수 규칙**: 7장 → M-1 or M-2 / 9장 → CTA-1 or CTA-2 / 같은 패턴 2연속 금지

## 릴스 이미지 프롬프트 원칙

캐러셀과 다른 기준:
- **해상도**: 1080×1920px (9:16 세로형)
- **씬 일관성**: 동일 시리즈 조명·색감·무드 통일
- **텍스트 금지**: 이미지 내 텍스트 없음 (자막은 별도 레이어)
- **모션 여백**: 피사체 센터 + 가장자리 15% 여백

프롬프트 공식:
```
[피사체] + [구도] + [무드/조명] + [색감] + [금지어]
스타일: editorial fashion, clean minimal, soft natural light
색상: muted tones, off-white, gold accents
금지: no text, no watermark, no oversaturated colors
비율: --ar 9:16
```

Outfit Swap 씬 (S4·S6):
```
[gena 착용 씬 설명], sling bag visible,
lifestyle editorial, golden hour or soft indoor light,
face not fully visible (side or back), --ar 9:16
```

## 자기검증 체크리스트

- [ ] 캐러셀: 같은 패턴 2연속 없음
- [ ] 캐러셀: 7장 M-1 or M-2, 9장 CTA-1 or CTA-2
- [ ] 모든 디자인 값 CSS 변수 참조 (하드코딩 금지)
- [ ] 릴스: 해상도 힌트 1080×1920 명시
- [ ] 릴스: 이미지 내 텍스트 없음
- [ ] S4·S6 Outfit Swap 프롬프트 별도 작성
- [ ] 카피 작성·HTML·QA 금지
