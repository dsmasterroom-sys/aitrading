# HTML 템플릿 디자인 수정 가이드

> GenArchive 캐러셀 HTML 템플릿 커스터마이징 방법

---

## 📁 파일 구조

```
gena_feed/
├── templates/              ← HTML 템플릿 파일
│   ├── H-1-hero.html
│   ├── H-2-hero-dual.html
│   ├── I-1-info-grid.html
│   ├── I-2-info-list.html
│   ├── CTA-1-final.html
│   └── ...
├── shared/
│   ├── design-tokens.css   ← 🎨 색상/폰트 중앙 관리
│   └── base.css
└── scripts/
    └── compose_carousel.py ← 캐러셀 생성 스크립트
```

---

## 🎨 1. 색상 변경

### 파일: `shared/design-tokens.css`

```css
/* 주요 색상 */
:root {
  /* 브랜드 컬러 */
  --color-primary: #C9A961;      /* 금색 악센트 */
  --color-secondary: #8B7355;    /* 서브 컬러 */
  
  /* 배경색 */
  --color-bg-primary: #F5F1E8;   /* 베이지 배경 */
  --color-bg-secondary: #FFFFFF; /* 화이트 배경 */
  --color-bg-dark: #1A1D2E;      /* 다크 배경 */
  
  /* 텍스트 */
  --color-text-primary: #1A1D2E;   /* 진한 텍스트 */
  --color-text-secondary: #5A5D6E; /* 보조 텍스트 */
  --color-text-light: #F5F1E8;     /* 밝은 텍스트 (다크 배경용) */
  
  /* 악센트 라인 */
  --color-accent-line: #C9A961;  /* 금색 구분선 */
}
```

### 예시: 브랜드 컬러 변경

**기존 (금색):**
```css
--color-primary: #C9A961;
```

**변경 (로즈골드):**
```css
--color-primary: #B76E79;
```

---

## 🔤 2. 폰트 변경

### 파일: `shared/design-tokens.css`

```css
/* 타이포그래피 */
:root {
  /* 폰트 패밀리 */
  --font-family-base: 'Pretendard Variable', -apple-system, sans-serif;
  --font-family-display: 'Pretendard Variable', sans-serif;
  
  /* 폰트 크기 */
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */
  
  /* 폰트 두께 */
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

### 예시: 헤딩 크기 키우기

**기존:**
```css
--font-size-4xl: 2.25rem;  /* 36px */
```

**변경:**
```css
--font-size-4xl: 3rem;  /* 48px */
```

---

## 📐 3. 레이아웃 수정

### Safe Zone 조정

**파일:** 개별 템플릿 (예: `templates/H-1-hero.html`)

```html
<style>
  .safe-zone {
    padding-top: 120px;    /* 상단 여백 */
    padding-bottom: 160px; /* 하단 여백 */
    padding-left: 80px;    /* 좌측 여백 */
    padding-right: 80px;   /* 우측 여백 */
  }
</style>
```

### 간격 조정

**파일:** `shared/design-tokens.css`

```css
/* 간격 */
:root {
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */
  --spacing-3xl: 4rem;     /* 64px */
}
```

---

## 🖼️ 4. 개별 템플릿 수정

### H-1 Hero 템플릿 예시

**파일:** `templates/H-1-hero.html`

```html
<div class="hero-section">
  <h1 class="hero-title">GenArchive</h1>
  <p class="hero-subtitle">Minimal Design Philosophy</p>
  
  <style>
    .hero-title {
      font-size: var(--font-size-4xl);
      font-weight: var(--font-weight-bold);
      color: var(--color-text-primary);
      margin-bottom: var(--spacing-md);
    }
    
    .hero-subtitle {
      font-size: var(--font-size-lg);
      color: var(--color-text-secondary);
    }
  </style>
</div>
```

**수정 예시:**
- 제목 크기: `--font-size-4xl` → `--font-size-5xl`
- 색상: `--color-text-primary` → `--color-primary`
- 간격: `--spacing-md` → `--spacing-lg`

---

## 🎯 5. 금색 악센트 라인 수정

### CTA 템플릿 예시

**파일:** `templates/CTA-1-final.html`

```html
<div class="accent-line"></div>

<style>
  .accent-line {
    width: 80px;
    height: 4px;
    background: var(--color-accent-line);
    margin: var(--spacing-lg) auto;
  }
</style>
```

**수정:**
- 길이: `width: 120px;`
- 두께: `height: 6px;`
- 색상: `background: var(--color-primary);`

---

## 📱 6. 페이지 번호 스타일

### 공통 요소

```html
<div class="page-number">08/09</div>

<style>
  .page-number {
    position: absolute;
    top: 40px;
    right: 80px;
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    font-weight: var(--font-weight-medium);
  }
</style>
```

---

## 🔧 7. 실전 커스터마이징 워크플로우

### Step 1: 디자인 토큰 수정
```bash
# 1. 색상/폰트 중앙 설정
vi shared/design-tokens.css
```

### Step 2: 개별 템플릿 수정
```bash
# 2. 특정 템플릿 레이아웃 조정
vi templates/H-1-hero.html
```

### Step 3: 미리보기
```bash
# 3. 캐러셀 생성 및 확인
cd /Users/master/.openclaw/workspace/gena_feed_claude_project/gena_feed
python scripts/compose_carousel.py
```

### Step 4: 결과 확인
```bash
# 생성된 이미지 확인
open output/slides/
```

---

## ✅ 빠른 시작 체크리스트

- [ ] `shared/design-tokens.css` 열기
- [ ] 브랜드 컬러 확인/수정 (`--color-primary`)
- [ ] 배경색 확인/수정 (`--color-bg-primary`)
- [ ] 폰트 크기 확인/수정 (`--font-size-*`)
- [ ] `python scripts/compose_carousel.py` 실행
- [ ] `output/slides/` 폴더에서 결과 확인
- [ ] 만족할 때까지 반복

---

## 🎨 디자인 팁

### 1. 색상 조합 예시

**모던 골드** (현재):
```css
--color-primary: #C9A961;
--color-bg-primary: #F5F1E8;
```

**로즈 골드**:
```css
--color-primary: #B76E79;
--color-bg-primary: #FFF5F7;
```

**네이비 골드**:
```css
--color-primary: #D4AF37;
--color-bg-primary: #F8F9FA;
--color-bg-dark: #0A1929;
```

### 2. 타이포그래피 조합

**클래식** (현재):
```css
--font-weight-bold: 700;
--font-size-4xl: 2.25rem;
```

**모던 라이트**:
```css
--font-weight-bold: 500;
--font-size-4xl: 3rem;
```

**강렬한 임팩트**:
```css
--font-weight-bold: 800;
--font-size-4xl: 3.5rem;
```

---

## 🚨 주의사항

1. **CSS 변수 우선 사용**: 하드코딩 대신 `var(--color-primary)` 형식 사용
2. **Safe Zone 준수**: 상단 120px, 하단 160px, 좌우 80px 여백 유지
3. **캔버스 크기**: 1080×1920px (Instagram Stories/Reels 표준)
4. **Export 크기**: @2x 스케일 (2160×3840px)
5. **폰트 로딩**: Pretendard 웹폰트 로딩 확인

---

## 📚 참고 문서

- **Figma 디자인 스펙**: `docs/figma-design-spec-실전.md`
- **템플릿 가이드**: `docs/figma-template-guide.md`
- **브랜드 가이드**: GenArchive 브랜드북 (별도)

---

**마지막 업데이트:** 2026-03-03  
**작성자:** 자비스
