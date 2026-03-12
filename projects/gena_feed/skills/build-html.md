---
name: developer (HTML 빌드)
description: "나노젠 생성 이미지·카피를 HTML 슬라이드로 구현하고 PNG 추출."
---

# build-html SKILL

## 입력
- `series/{시리즈명}/copy.md` (확정 카피)
- `series/{시리즈명}/design-brief.md` (레이아웃·색상)
- `series/{시리즈명}/generated/` (나노젠 생성 이미지 base64)
- 참조: shared/design-tokens.css, series/{시리즈명}/theme/theme.md (있을 경우)
- 참조: `shared/references/*.html` (레이아웃 패턴 카탈로그)

## 출력
- `series/{시리즈명}/slides/slide_XX.html` (슬라이드별)
- `output/{시리즈명}/slide_XX.png` (최종 PNG)

---

## 실행 흐름

### Step 1 — HTML 기본 구조 (절대 규칙)
```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080">
<link rel="stylesheet" href="../../../shared/design-tokens.css">
<style>
  /* ★ :root 변수·@font-face를 슬라이드에 복사하지 않는다 — design-tokens.css에서 로딩됨 */
  /* 시리즈 오버라이드 있으면 theme.md 값을 :root에 추가 선언 (덮어쓰기) */

  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body {
    width: var(--canvas-carousel-w);   /* 1080px */
    height: var(--canvas-carousel-h);  /* 1350px */
    overflow: hidden;
    word-break: keep-all;
    font-family: var(--ff-primary);
    -webkit-font-smoothing: antialiased;
  }
  .slide {
    width: var(--canvas-carousel-w);
    height: var(--canvas-carousel-h);
    overflow: hidden;
    position: relative;
  }
  /* 헤드라인에는 var(--ff-accent) 사용 */
</style>
</head>
```
> **주의**: HTTP 서버는 프로젝트 루트에서 실행해야 상대경로(`../../../shared/`)가 작동한다.
> `cd /path/to/gena_feed && python3 -m http.server 8888`

### Step 2 — 이미지 삽입 규칙
- 외부 URL 직접 참조 금지
- generated/ 파일을 base64로 읽어 인라인 삽입:
```html
<img src="data:image/png;base64,[base64_data]" />
```

### Step 3 — 레이아웃 패턴 카탈로그 활용 (필수 참조)

**3a. 카탈로그 분석 (매 시리즈 시작 시 1회)**
`shared/references/*.html` 파일들을 읽고, design-brief의 무드에 맞는 패턴 3~5개를 미리 선정한다.
- editorial.html (~30 패턴): 클린·미니멀·그리드 기반
- bentoretro.html (~30 패턴): 벤토 그리드·레트로·컬러 블록
- blackwhite.html (~17 패턴): 모노크롬·하이콘트라스트·타이포 중심
- neonbold2.html (~17 패턴): 네온·볼드·그래디언트
- neonblack.html (~17 패턴): 다크모드·네온 액센트

각 패턴에서 참조할 것: **그리드 구조, 오버레이 방식, 텍스트 배치 전략, 네거티브 스페이스 활용법**
각 패턴에서 참조하지 않을 것: 컬러값, 폰트명, 간격 수치 (모두 토큰으로 치환)

**3b. 패턴 적용 규칙**
1. design-brief에서 `참조: editorial/MIX-03` 등으로 지정된 경우 해당 패턴 구조를 기반으로 구현
2. **컬러·폰트·간격은 카탈로그 값을 절대 사용하지 않는다** — 반드시 시리즈 토큰(`var(--)`)으로 치환
3. 구조를 그대로 복사하지 않고, 시리즈 맥락에 맞게 변형·조합한다
4. 10장 슬라이드 중 **최소 3가지 다른 레이아웃 패턴** 사용

```
❌ color: #05fe04           (카탈로그 하드코딩)
✅ color: var(--accent)     (시리즈 토큰)

❌ font-family: 'Anton'     (카탈로그 폰트)
✅ font-family: var(--ff-display) 또는 시리즈 지정 폰트
```

### Step 3.5 — 비주얼 컴포지션 원칙

**텍스트-이미지 배치 전략** (인물 슬라이드 필수):
| 이미지 구도 | 텍스트 위치 | 기법 |
|------------|-----------|------|
| 인물 중앙 | 상단 or 하단 밴드 | 반투명 그라데이션 오버레이 |
| 인물 좌측 | 우측 여백 | 세로 텍스트 블록 or 사이드바 |
| 인물 하단 | 상단 2/3 | 이미지 위 직접 타이포 |
| 풀블리드 이미지 | 하단 바 | 솔리드 컬러 바 + 텍스트 |

**타이포그래피 계층** (슬라이드당 최대 3단계):
1. **헤드라인**: `--fs-display` ~ `--fs-title` / weight 700-900 / 시선 첫 도달점
2. **서브헤드/강조**: `--fs-body` / weight 500-600 / accent 컬러 가능
3. **본문/캡션**: `--fs-body` ~ `--fs-caption` / weight 400 / secondary 컬러

**시각적 리듬 규칙**:
- 텍스트 중심 → 이미지 중심 → 텍스트 중심 교대 배치 (3연속 동일 비율 금지)
- 전체 슬라이드의 텍스트/이미지 비율: 텍스트 온리 최대 2장, 이미지 풀블리드 최대 3장
- 숫자/통계 슬라이드: 히어로 숫자는 `--fs-display` 이상, 강렬한 시각적 무게감

### Step 4 — 카피 적용
- copy.md의 헤드라인·본문·강조를 HTML 요소에 매핑
- 강조: `<strong>` 또는 color 토큰으로만, 중첩 금지
- 폰트: CSS 변수만 사용 (하드코딩 금지)

### Step 5 — PNG 추출 + 시각 검수

**5a. PNG 추출** (Puppeteer)
```javascript
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1350, deviceScaleFactor: 1 });
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
await page.screenshot({ path: pngPath, type: 'png' });
```
스토리인 경우: width 1080, height 1920

**5b. Playwright MCP 시각 검수** (가능한 경우)
추출된 PNG를 Playwright MCP로 브라우저에서 열어 시각적으로 검증한다:
- 텍스트가 이미지 위에서 가독성이 있는지
- 레이아웃이 캔버스를 벗어나지 않는지
- 10장 연속 스와이프했을 때 시각적 리듬감이 있는지

---

## 자기검증 체크리스트

### HIGH (고위험 — 반드시 확인)
- [ ] **텍스트 오버레이가 인물 얼굴을 가리지 않는가?** — 이미지 구도를 확인하고 오버레이 위치(top/bottom)와 그라데이션 강도를 조정할 것
- [ ] 외부 CDN·URL 참조가 0건인가?
- [ ] 모든 이미지가 base64 인라인인가?

### MID (중위험)
- [ ] overflow: hidden이 설정되었는가?
- [ ] word-break: keep-all이 설정되었는가?
- [ ] 최소 폰트가 28px(var(--fs-caption)) 이상인가?
- [ ] CSS 하드코딩 값(색상·폰트 직접 기재)이 없는가? — 카탈로그 참조 시 원본 값이 남아있지 않은지 특히 주의
- [ ] PNG 추출 해상도가 캔버스 크기와 일치하는가?

### DESIGN (디자인 품질)
- [ ] 레퍼런스 카탈로그에서 최소 3가지 패턴을 참조했는가?
- [ ] 텍스트-이미지 배치가 인물 구도에 맞게 조정되었는가?
- [ ] 타이포그래피가 최대 3단계 계층을 준수하는가?
- [ ] 텍스트 중심/이미지 중심이 3연속 동일 비율이 아닌가?
- [ ] 히어로 숫자/통계가 충분한 시각적 무게감을 가지는가?
