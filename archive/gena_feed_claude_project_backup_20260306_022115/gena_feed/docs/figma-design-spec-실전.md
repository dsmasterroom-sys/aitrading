# Figma 템플릿 디자인 스펙 (실전 버전)
# @gena_feed 캐러셀 시스템

> 기존 HTML 캐러셀 샘플 분석 기반
> 실제 Figma 제작에 바로 사용 가능한 상세 스펙

---

## 📐 캔버스 규격

```
크기: 1080 × 1920px (Instagram Stories/Reels)
Export: @2x (2160 × 3840px)
Safe Zone: 
  - 상단: 120px
  - 하단: 160px (브랜드 영역 포함)
  - 좌우: 80px
Grid: 8px 기반
```

---

## 🎨 Design System

### Color Palette

**Primary Colors (베이지 톤)**
```
Light Beige Background    #F5F1E8
Medium Beige             #E8DEC8
Warm Beige               #D4C4A8
```

**Accent Colors (금색)**
```
Gold Primary             #C9A961
Gold Dark               #B89850
Gold Light              #D8B976
```

**Dark Colors**
```
Deep Navy               #1A1D2E
Charcoal                #2D2F3E
Dark Gray               #4A4D5E
```

**Text Colors**
```
Primary Text (Dark)      #1A1D2E
Secondary Text (Gray)    #6B6E7E
Light Text (White)       #FFFFFF
Muted Text              #9B9EA8
```

**Semantic Colors**
```
Background Canvas        #F5F1E8 (light) / #1A1D2E (dark)
Card Background         #FFFFFF (light) / #2D2F3E (dark)
Border                  #E0DDD5 (light) / #4A4D5E (dark)
```

### Typography

**폰트 패밀리**
```
Primary: Pretendard (Variable Font 권장)
Fallback: -apple-system, "Malgun Gothic", sans-serif

다운로드: https://github.com/orioncactus/pretendard
Figma: Pretendard Variable 설치 필수
```

**Type Scale**

| 용도 | 크기 | 굵기 | 행간 | 자간 |
|------|------|------|------|------|
| Display Large | 72px | Bold (700) | 1.1 (79px) | -2% |
| Display Medium | 56px | Bold (700) | 1.15 (64px) | -1.5% |
| Heading H1 | 48px | Bold (700) | 1.2 (58px) | -1% |
| Heading H2 | 36px | SemiBold (600) | 1.3 (47px) | -0.5% |
| Heading H3 | 28px | SemiBold (600) | 1.4 (39px) | 0% |
| Heading H4 | 24px | Medium (500) | 1.4 (34px) | 0% |
| Body Large | 20px | Regular (400) | 1.6 (32px) | 0% |
| Body Medium | 18px | Regular (400) | 1.6 (29px) | 0% |
| Body Small | 16px | Regular (400) | 1.5 (24px) | 0% |
| Caption | 14px | Regular (400) | 1.4 (20px) | 0% |
| Label Bold | 14px | Bold (700) | 1.3 (18px) | 5% uppercase |
| Number Display | 64px | ExtraBold (800) | 1.0 (64px) | -2% |
| Page Number | 18px | Regular (400) | 1.0 (18px) | 0% |

**실제 예시 (기존 샘플 분석)**
```
"이것만 기억해" → H1 (48px Bold)
"기울기 대각선으로" → Body Large (20px SemiBold)
"08 / 09" → Page Number (18px Regular)
"@gena_feed" → Caption (14px Regular)
```

### Spacing System (8px Grid)

```
4px   - Micro spacing (icon + text gap)
8px   - Tiny (inline elements)
12px  - Small (list items)
16px  - Medium (paragraph margins)
24px  - Large (section gaps)
32px  - XLarge (major sections)
48px  - XXLarge (slide padding top/bottom)
64px  - Huge (hero spacing)
80px  - Safe zone horizontal
120px - Safe zone top
160px - Safe zone bottom (브랜드 영역 포함)
```

### Effects

**Shadows**
```css
Card Shadow:
  0px 2px 8px rgba(26, 29, 46, 0.08)

Card Hover:
  0px 8px 24px rgba(26, 29, 46, 0.12)

Floating:
  0px 12px 40px rgba(26, 29, 46, 0.16)

Text Shadow (헤드라인 강조용):
  0px 2px 4px rgba(0, 0, 0, 0.25)
```

**Blurs**
```css
Background Blur:
  blur(20px)

Glass Effect:
  blur(40px) + opacity 85%
```

### 브랜드 요소

**고정 요소 (모든 슬라이드)**

1. **페이지 번호** (우상단)
   ```
   위치: 우상단 80px, 80px
   폰트: 18px Regular, #9B9EA8
   형식: "08 / 09"
   ```

2. **브랜드 로고** (하단)
   ```
   위치: 하단 중앙, 바닥에서 40px
   폰트: 14px Regular, 컬러는 배경에 따라
   텍스트: "@gena_feed"
   배경: 24px 높이 바 (dark: #1A1D2E, light: #F5F1E8)
   ```

3. **금색 악센트 라인**
   ```
   사용처: 헤드라인 언더라인, 리스트 아이콘
   색상: #C9A961
   두께: 4px (헤드라인), 2px (리스트)
   길이: 64px~120px (헤드라인 너비의 40% 정도)
   ```

---

## 📱 17개 템플릿 패턴 상세 스펙

### H-1: Hero Statement (숫자 강조)

**레이아웃:**
```
1080 × 1920px

Safe Zone: 80px left/right, 120px top, 160px bottom

┌─────────────────────────────────────────┐
│                                    08/09 │  ← 페이지 번호
│                                         │
│                                         │
│              [큰 숫자]                    │  ← Number Display (64px)
│             2,500+                      │
│                                         │
│          [헤드라인]                      │  ← H1 (48px Bold)
│       GenArchive에서                     │
│       만난 아카이브                       │
│          ─────                          │  ← 금색 라인
│                                         │
│       [서브 텍스트]                      │  ← Body Large (20px)
│    국내 최대 아카이브 커뮤니티             │
│                                         │
│                                         │
│                                         │
│              @gena_feed                 │  ← 브랜드
└─────────────────────────────────────────┘
```

**Component 구조:**
```
Frame: H1-Hero-Statement (1080×1920)
├─ Background (Fill: Gradient)
│  └─ Gradient: #4A4D5E → #1A1D2E (135°)
├─ Text/page_number (18px Regular, #9B9EA8)
├─ Text/hero_number (64px ExtraBold, #C9A961)
├─ Text/hero_headline (48px Bold, #FFFFFF)
├─ Shape/accent_line (4×80px, #C9A961)
├─ Text/hero_subtext (20px Regular, #E8DEC8)
└─ Footer
   ├─ Rectangle (1080×80px, #1A1D2E)
   └─ Text/brand_logo (14px Regular, #FFFFFF)
```

**변수 노드:**
```
Text/hero_number      → "2,500+"
Text/hero_headline    → "GenArchive에서\n만난 아카이브"
Text/hero_subtext     → "국내 최대 아카이브 커뮤니티"
Text/page_number      → "01 / 09"
Color/bg_gradient_start → #4A4D5E
Color/bg_gradient_end   → #1A1D2E
```

**Auto Layout 설정:**
- Container: Vertical, Center aligned
- Gap: 24px (숫자 ↔ 헤드라인), 16px (헤드라인 ↔ 서브)
- Padding: 80px left/right, 120px top, 160px bottom

---

### H-2: Visual Impact (이미지 강조)

**레이아웃:**
```
┌─────────────────────────────────────────┐
│                                    08/09 │
│                                         │
│   [Full Bleed Background Image]         │
│   + Gradient Overlay                    │
│                                         │
│                                         │
│   ┌───────────────────────────┐         │
│   │ [텍스트 카드]                │         │
│   │                           │         │
│   │  [헤드라인]                 │         │
│   │  슬링백 공급하면             │         │
│   │  링크바이오에 있어요.         │         │
│   │                           │         │
│   │  [Badge] 제품 정보          │         │
│   └───────────────────────────┘         │
│                                         │
│              @gena_feed                 │
└─────────────────────────────────────────┘
```

**Component 구조:**
```
Frame: H2-Visual-Impact (1080×1920)
├─ Image/bg_image (1080×1920, Fill)
├─ Rectangle/overlay (Gradient: transparent → #1A1D2E 70%)
├─ Text/page_number
├─ Card/text_block (Auto Layout)
│  ├─ Background (Glass: #FFFFFF 15%, blur 40px)
│  ├─ Text/headline (28px SemiBold, #FFFFFF)
│  ├─ Text/description (18px Regular, #E8DEC8)
│  └─ Badge/info (Auto Layout)
│     ├─ Icon (16px)
│     └─ Text (14px Medium)
└─ Footer/brand
```

**변수 노드:**
```
Image/bg_image        → [제품 착용 이미지]
Text/headline         → "슬링백 공급하면\n링크바이오에 있어요."
Text/description      → "간단한 설명 텍스트"
Text/badge_text       → "제품 정보"
```

---

### I-2: Timeline (시간순 정보)

**레이아웃:**
```
┌─────────────────────────────────────────┐
│                                    08/09 │
│                                         │
│       [제목]                             │
│    이것만 기억해                          │
│       ─────                             │
│                                         │
│  ① 기울기                                │
│     대각선으로                            │
│                                         │
│  ② 끝 길이                               │
│     짧게                                 │
│                                         │
│  ③ 드는 위치                             │
│     체형마다 달라                         │
│                                         │
│  ④ 표지선                                │
│     특마다 다름                           │
│                                         │
│        사랑어요. 진짜예요.                 │
│                                         │
│              @gena_feed                 │
└─────────────────────────────────────────┘
```

**Component 구조:**
```
Frame: I2-Timeline (1080×1920)
├─ Background (#F5F1E8)
├─ Text/page_number
├─ Header
│  ├─ Text/title (36px SemiBold, #1A1D2E)
│  └─ Shape/accent_line (4×100px, #C9A961)
├─ List (Auto Layout, Vertical, 32px gap)
│  ├─ Item-1
│  │  ├─ Circle/number (48×48px, #C9A961)
│  │  │  └─ Text "①" (20px Bold, #FFFFFF)
│  │  └─ Content (Auto Layout, 12px gap)
│  │     ├─ Text/item_1_title (20px SemiBold, #C9A961)
│  │     └─ Text/item_1_desc (18px Regular, #1A1D2E)
│  ├─ Item-2 (동일 구조)
│  ├─ Item-3 (동일 구조)
│  └─ Item-4 (동일 구조)
├─ Text/closing_remark (18px Italic, #6B6E7E)
└─ Footer/brand
```

**변수 노드:**
```
Text/title            → "이것만 기억해"
Text/item_1_title     → "기울기"
Text/item_1_desc      → "대각선으로"
Text/item_2_title     → "끝 길이"
Text/item_2_desc      → "짧게"
Text/item_3_title     → "드는 위치"
Text/item_3_desc      → "체형마다 달라"
Text/item_4_title     → "표지선"
Text/item_4_desc      → "특마다 다름"
Text/closing_remark   → "사랑어요. 진짜예요."
```

---

### CTA-1: Primary CTA (링크바이오 유도)

**레이아웃:**
```
┌─────────────────────────────────────────┐
│                                    09/09 │
│                                         │
│                                         │
│         [아이콘]                          │
│          📝                              │
│                                         │
│      [헤드라인]                           │
│     저장해두고                             │
│     나중에 써봐요                          │
│          ─────                          │
│                                         │
│      [서브 텍스트]                        │
│    슬링백 궁금하면                         │
│    링크바이오에 있어요.                     │
│                                         │
│   ┌───────────────────────┐              │
│   │  🔗 링크바이오          │              │
│   └───────────────────────┘              │
│                                         │
│              @gena_feed                 │
└─────────────────────────────────────────┘
```

**Component 구조:**
```
Frame: CTA1-Primary (1080×1920)
├─ Background (Radial gradient center)
│  └─ Colors: #2D2F3E (center) → #1A1D2E (edge)
├─ Text/page_number
├─ Icon/emoji (64px) or Image/icon_illustration
├─ Header
│  ├─ Text/headline (48px Bold, #FFFFFF)
│  └─ Shape/accent_line (4×100px, #C9A961)
├─ Text/subtext (20px Regular, #E8DEC8)
├─ Button/cta (Auto Layout)
│  ├─ Background (#C9A961, 8px corner radius)
│  ├─ Padding (24px H, 16px V)
│  ├─ Icon/link (20px, #FFFFFF)
│  └─ Text/cta_text (18px Bold, #FFFFFF)
└─ Footer/brand
```

**변수 노드:**
```
Text/headline         → "저장해두고\n나중에 써봐요"
Text/subtext          → "슬링백 궁금하면\n링크바이오에 있어요."
Text/cta_text         → "링크바이오"
Icon/emoji            → "📝" or image path
```

**Interactive State (Figma Prototype):**
```
Default → Hover: Scale 102%, Shadow increase
Click: Link to external URL (prototype용)
```

---

## 🔧 Figma 제작 실전 가이드

### Step 1: 파일 설정

1. **새 파일 생성**
   ```
   File → New Design File
   Name: GenArchive Carousel System v2
   ```

2. **Pages 구성**
   ```
   ├─ 📄 Cover (설명)
   ├─ 🎨 Design System (Color/Text/Effect Styles)
   ├─ 🧩 Components (17개 템플릿)
   └─ 🖼️ Slides (실제 슬라이드 작업)
   ```

3. **Canvas 설정**
   ```
   각 프레임: 1080 × 1920px
   Background: None (투명)
   ```

### Step 2: Design System 구축

**Color Styles 생성**

```
이름 패턴: Category/Name/Variant

Primary/Beige/Light       #F5F1E8
Primary/Beige/Medium      #E8DEC8
Accent/Gold/Primary       #C9A961
Accent/Gold/Dark         #B89850
Text/Primary/Dark        #1A1D2E
Text/Secondary/Gray      #6B6E7E
Background/Canvas/Light  #F5F1E8
Background/Canvas/Dark   #1A1D2E
```

**Text Styles 생성**

```
이름 패턴: Category/Size/Weight

Display/Large/Bold       Pretendard 72px Bold
Heading/H1/Bold          Pretendard 48px Bold
Heading/H2/SemiBold      Pretendard 36px SemiBold
Body/Large/Regular       Pretendard 20px Regular
Body/Medium/Regular      Pretendard 18px Regular
Label/Bold/Uppercase     Pretendard 14px Bold, uppercase
```

**Effect Styles 생성**

```
Shadow/Card              0 2 8 rgba(26,29,46,0.08)
Shadow/Floating          0 12 40 rgba(26,29,46,0.16)
Blur/Background          blur 20
```

### Step 3: Component 제작 (예시: H-1)

**1) 기본 프레임 생성**

```
Frame 도구 (F) → 1080 × 1920px
Name: H1-Hero-Statement
Fill: Linear Gradient (#4A4D5E → #1A1D2E, 135°)
```

**2) 페이지 번호 추가**

```
Text 도구 (T)
Content: "08 / 09"
Position: X:920, Y:80 (우상단)
Style: Page Number (18px Regular, #9B9EA8)
Layer name: Text/page_number
```

**3) 콘텐츠 그룹 (Auto Layout)**

```
Frame 도구 (F)
Name: Content-Container
Auto Layout: Vertical, Center aligned
Gap: 24px
Padding: 80px (left/right), 400px (top), 160px (bottom)

Children:
  1. Text/hero_number
     Content: "2,500+"
     Style: Number Display (64px ExtraBold, #C9A961)
  
  2. Text/hero_headline
     Content: "GenArchive에서\n만난 아카이브"
     Style: Heading H1 (48px Bold, #FFFFFF)
     
  3. Shape/accent_line
     Rectangle: 80×4px, Fill #C9A961
     Corner radius: 2px
     
  4. Text/hero_subtext
     Content: "국내 최대 아카이브 커뮤니티"
     Style: Body Large (20px Regular, #E8DEC8)
```

**4) 브랜드 푸터**

```
Frame 도구 (F)
Name: Footer
Position: bottom, full width
Size: 1080×80px
Fill: #1A1D2E
Auto Layout: Horizontal, Center

Children:
  Text/brand_logo
  Content: "@gena_feed"
  Style: Caption (14px Regular, #FFFFFF)
```

**5) Component 생성**

```
전체 선택 → Create Component (Cmd+Opt+K)
Name: H-1 / Hero Statement
Description: 숫자 강조 히어로 슬라이드
```

**6) Variants 설정 (선택)**

```
Properties:
  - Theme: Light / Dark
  - Size: Default / Compact

각 Variant마다 색상만 변경
```

### Step 4: 변수 노드 명명 규칙

**중요: API 연동을 위한 정확한 명명**

```
텍스트 노드:
  Text/{variable_name}
  예: Text/hero_number, Text/hero_headline

이미지 노드:
  Image/{variable_name}
  예: Image/bg_image, Image/product_photo

컬러 노드:
  Color/{variable_name}
  예: Color/bg_gradient_start
```

### Step 5: 실제 슬라이드 작성

**Slides 페이지로 이동**

```
1. Component에서 Instance 드래그
2. 변수 노드 내용 실제 콘텐츠로 교체
3. Layer name은 절대 변경하지 말 것!
4. Frame name을 "Slide-01", "Slide-02" 등으로 변경
```

### Step 6: Node Mapping JSON 생성

**프로젝트에서 실행**

```bash
cd gena_feed
python3 scripts/figma_node_mapper.py
```

**결과:**
```
figma-node-mapping.json 생성
→ 모든 Frame의 Node ID 및 변수 노드 매핑
```

---

## 📋 제작 체크리스트

### Design System
- [ ] Color Styles 14개 생성
- [ ] Text Styles 12개 생성
- [ ] Effect Styles 3개 생성
- [ ] Pretendard Variable 폰트 설치

### Components (17개)
- [ ] H-1: Hero Statement
- [ ] H-2: Visual Impact
- [ ] H-3: Split Hero
- [ ] I-1: Data Grid
- [ ] I-2: Timeline
- [ ] I-3: Stat Comparison
- [ ] I-4: Feature List
- [ ] I-5: Quote + Source
- [ ] P-1: Step-by-Step
- [ ] P-2: Before/After
- [ ] P-3: Process Flow
- [ ] C-1: Side-by-Side
- [ ] C-2: Pros/Cons
- [ ] M-1: Product Showcase
- [ ] M-2: Collection Grid
- [ ] CTA-1: Primary CTA
- [ ] CTA-2: Urgency CTA

### 공통 요소
- [ ] 페이지 번호 (우상단, 18px)
- [ ] 브랜드 로고 (하단, @gena_feed)
- [ ] 금색 악센트 라인 (헤드라인 언더라인)

### 명명 규칙
- [ ] 모든 변수 노드: Text/{var}, Image/{var}, Color/{var}
- [ ] Component: {Pattern} / {Description}
- [ ] Frame: Slide-{number:02d}

### 테스트
- [ ] Instance 생성 및 내용 변경 테스트
- [ ] Node Mapping JSON 생성 확인
- [ ] Export 테스트 (python scripts/figma_export.py --all)

---

## 🎯 Quick Start

**최소 작업으로 테스트하기:**

1. **3개 템플릿만 먼저 제작**
   - H-1 (숫자 강조)
   - I-2 (리스트)
   - CTA-1 (링크바이오)

2. **Design System 간소화**
   - Color: 5개만 (Beige/Gold/Dark/Light Text/Dark Text)
   - Text: 4개만 (H1/Body Large/Caption/Number)

3. **실제 슬라이드 3장 작성**
   - Slide-01: H-1 Instance
   - Slide-02: I-2 Instance
   - Slide-03: CTA-1 Instance

4. **테스트**
   ```bash
   python3 scripts/figma_node_mapper.py
   python3 scripts/figma_export.py --all
   ```

5. **검증 후 나머지 14개 확장**

---

## 📚 참고 자료

**Figma 공식 문서:**
- Components: https://help.figma.com/hc/en-us/articles/360038662654
- Auto Layout: https://help.figma.com/hc/en-us/articles/360040451373
- Variants: https://help.figma.com/hc/en-us/articles/360056440594

**Pretendard 폰트:**
- GitHub: https://github.com/orioncactus/pretendard
- Figma 설치: Settings → Font → Upload

**기존 문서:**
- `docs/figma-template-guide.md` - 17개 패턴 전체 명세
- `docs/figma-api-design.md` - API 연동 설계
- `docs/figma-workflow.md` - 워크플로우 통합

---

**문서 버전:** 2.0 (실전)  
**작성일:** 2026-03-03  
**작성자:** 자비스  
**기반:** 기존 HTML 캐러셀 샘플 9장 분석
