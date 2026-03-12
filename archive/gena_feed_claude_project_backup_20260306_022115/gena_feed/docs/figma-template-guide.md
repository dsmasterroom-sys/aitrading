# Figma Template Guide
# GenArchive 캐러셀 제작 템플릿 시스템

## 📋 개요

본 문서는 GenArchive 캐러셀 자동 생성을 위한 Figma 템플릿 구조 설계를 정의합니다.
디자이너급 퀄리티의 비주얼을 API 기반으로 자동 생성하기 위한 Component 시스템입니다.

**핵심 원칙:**
- 템플릿 재사용성: 17개 레이아웃 패턴을 Component화
- 데이터 분리: 디자인과 콘텐츠의 완전한 분리
- 브랜드 일관성: GenArchive 톤앤매너 유지
- 확장성: 새로운 레이아웃 패턴 추가 용이

---

## 🏗️ Figma 파일 구조

### 1. 파일 계층 구조

```
📁 GenArchive Carousel System (Figma File)
├── 📄 Cover (설명 페이지)
├── 🎨 Design System
│   ├── Color Styles
│   ├── Text Styles
│   ├── Effect Styles (Shadows, Blurs)
│   └── Grid/Layout Styles
├── 🧩 Components
│   ├── Atoms (기본 요소)
│   ├── Molecules (조합 요소)
│   └── Templates (17개 레이아웃)
└── 🖼️ Slides (실제 슬라이드 인스턴스)
    ├── Slide-01
    ├── Slide-02
    └── ...
```

### 2. Page 구성

#### **📄 Cover Page**
- 프로젝트 개요, 사용 가이드, 버전 정보
- Quick Start 링크

#### **🎨 Design System Page**
- 모든 Color, Text, Effect Styles 정의
- 브랜드 컬러 시스템 (GenArchive 톤앤매너)
- 타이포그래피 시스템

#### **🧩 Components Page**
- 재사용 가능한 모든 컴포넌트
- Variants로 상태/타입 관리
- Auto Layout 적극 활용

#### **🖼️ Slides Page**
- 실제 캐러셀 슬라이드 프레임
- Component Instance 배치
- API로 업데이트할 대상

---

## 🎨 Design System 정의

### Color Styles

#### Primary Colors (GenArchive 브랜드)
```
Primary/Brand-900     #1A1A2E (Deep Navy)
Primary/Brand-700     #2D2D44 
Primary/Brand-500     #4A4A6A (Main Brand)
Primary/Brand-300     #8B8BAA
Primary/Brand-100     #E8E8F0

Accent/Archive-Gold   #D4AF37 (Gold Accent)
Accent/Archive-Blue   #4A90E2 (Info Blue)
Accent/Archive-Green  #27AE60 (Success Green)
```

#### Semantic Colors
```
Background/Canvas     #FAFAFA
Background/Card       #FFFFFF
Background/Overlay    rgba(26, 26, 46, 0.85)

Text/Primary          #1A1A2E
Text/Secondary        #4A4A6A
Text/Tertiary         #8B8BAA
Text/Inverse          #FFFFFF

Border/Default        #E8E8F0
Border/Strong         #D0D0E0

State/Info            #4A90E2
State/Success         #27AE60
State/Warning         #F39C12
State/Error           #E74C3C
```

#### Gradient Styles
```
Gradient/Hero         linear(135°, #4A4A6A → #1A1A2E)
Gradient/Accent       linear(135°, #D4AF37 → #B8941F)
Gradient/Overlay      linear(180°, transparent → rgba(26,26,46,0.7))
```

### Text Styles

#### Headings
```
Display/Large         Font: Pretendard Bold, 72px, -2% LS
Display/Medium        Font: Pretendard Bold, 56px, -1.5% LS
Heading/H1            Font: Pretendard Bold, 48px, -1% LS, 1.2 LH
Heading/H2            Font: Pretendard SemiBold, 36px, -0.5% LS, 1.3 LH
Heading/H3            Font: Pretendard SemiBold, 28px, 0% LS, 1.4 LH
Heading/H4            Font: Pretendard Medium, 24px, 0% LS, 1.4 LH
```

#### Body
```
Body/Large            Font: Pretendard Regular, 18px, 0% LS, 1.6 LH
Body/Medium           Font: Pretendard Regular, 16px, 0% LS, 1.6 LH
Body/Small            Font: Pretendard Regular, 14px, 0% LS, 1.5 LH
Body/Caption          Font: Pretendard Regular, 12px, 0% LS, 1.4 LH
```

#### Special
```
Label/Bold            Font: Pretendard Bold, 14px, 5% LS (uppercase)
Label/Medium          Font: Pretendard Medium, 14px, 0% LS
Number/Display        Font: Pretendard ExtraBold, 64px, -2% LS
Number/Metric         Font: Pretendard Bold, 48px, -1% LS
```

### Effect Styles

#### Shadows
```
Shadow/Card           0px 2px 8px rgba(26,26,46,0.08)
Shadow/Card-Hover     0px 8px 24px rgba(26,26,46,0.12)
Shadow/Floating       0px 12px 40px rgba(26,26,46,0.16)
Shadow/Text           0px 2px 4px rgba(0,0,0,0.25)
```

#### Blurs
```
Blur/Background       blur(20px)
Blur/Glass            blur(40px) + opacity 85%
```

---

## 🧩 Component 시스템

### Atoms (기본 요소)

#### 1. **Text/Dynamic-Text**
- Properties:
  - `content` (text): 동적으로 바뀔 텍스트
  - `style` (variant): Display/Heading/Body/Label
  - `color` (variant): Primary/Secondary/Inverse
- Auto Layout: Hug contents

#### 2. **Image/Dynamic-Image**
- Properties:
  - `placeholder` (fill): 기본 이미지
  - `aspect-ratio` (variant): 16:9 / 4:3 / 1:1 / Custom
- Constraints: Fill container

#### 3. **Icon/Archive-Icon**
- Properties:
  - `icon` (variant): 100+ 아이콘 세트
  - `size` (variant): 16/24/32/48/64
  - `color` (fill): Linked to color styles
- Vector-based, scalable

#### 4. **Shape/Background**
- Properties:
  - `type` (variant): Solid/Gradient/Image/Glass
  - `color` (fill): Linked to color styles
- Corner radius: Variable

### Molecules (조합 요소)

#### 1. **Badge/Info-Badge**
- Composition: Icon + Text
- Variants:
  - Type: Default/Success/Warning/Error/Info
  - Size: Small/Medium/Large
- Auto Layout: 8px gap, 12px padding

#### 2. **Card/Content-Card**
- Composition: Background + Image + Title + Description
- Variants:
  - Style: Default/Elevated/Outlined
  - Alignment: Left/Center
- Auto Layout: 24px inner padding

#### 3. **List/Bullet-Item**
- Composition: Bullet Icon + Text
- Auto Layout: 12px gap
- Supports multi-line text

#### 4. **CTA/Button**
- Composition: Background + Text + Arrow Icon
- Variants:
  - Type: Primary/Secondary/Outline/Ghost
  - Size: Small/Medium/Large
- Interactive states: Default/Hover/Active

#### 5. **Step/Procedure-Step**
- Composition: Number Badge + Title + Description
- Auto Layout: Vertical, 16px gap
- Number circle with brand gradient

---

## 📐 17개 레이아웃 패턴 템플릿 설계

### 캔버스 규격
- **Size:** 1080 × 1920px (Instagram Stories/Reels 최적화)
- **Safe Zone:** 상하 120px, 좌우 80px 여백
- **Grid:** 12-column grid, 16px gutter

---

### **H-1: Hero Statement (히어로 강조)**

```
구조:
┌─────────────────────────────────┐
│ [Gradient Overlay Background]  │
│                                 │
│         [Large Number]          │
│      "핵심 메트릭 숫자"           │
│                                 │
│      [Headline Text]            │
│     "강조하고 싶은 메시지"         │
│                                 │
│      [Sub Text]                 │
│                                 │
│         [Logo]                  │
└─────────────────────────────────┘
```

**Component Mapping:**
- Background: `Shape/Background` (type=Gradient, Gradient/Hero)
- Number: `Text/Dynamic-Text` (style=Number/Display, color=Accent/Gold)
- Headline: `Text/Dynamic-Text` (style=Display/Medium, color=Inverse)
- Sub: `Text/Dynamic-Text` (style=Body/Large, color=Inverse)

**Variables:**
- `hero_number` → Number Text
- `hero_headline` → Headline Text
- `hero_subtext` → Sub Text
- `bg_gradient_start` → Gradient color 1
- `bg_gradient_end` → Gradient color 2

---

### **H-2: Visual Impact (이미지 강조)**

```
구조:
┌─────────────────────────────────┐
│                                 │
│    [Full Bleed Background]      │
│         Image + Overlay         │
│                                 │
│    [Bottom Text Block]          │
│    ┌─────────────────────┐     │
│    │  [Headline]         │     │
│    │  [Description]      │     │
│    │  [Badge]            │     │
│    └─────────────────────┘     │
└─────────────────────────────────┘
```

**Component Mapping:**
- Background: `Image/Dynamic-Image` (aspect=16:9)
- Overlay: `Shape/Background` (type=Gradient, Gradient/Overlay)
- Text Block: `Card/Content-Card` (style=Glass, alignment=Left)
- Badge: `Badge/Info-Badge` (type=Info)

**Variables:**
- `bg_image` → Background Image
- `headline` → Headline Text
- `description` → Description Text
- `badge_text` → Badge label

---

### **H-3: Split Hero (분할 강조)**

```
구조:
┌─────────────────────────────────┐
│ [Top Half - Solid Color]        │
│     [Icon]                      │
│     [Headline]                  │
├─────────────────────────────────┤
│ [Bottom Half - Image/Gradient]  │
│     [Description]               │
│     [CTA Button]                │
└─────────────────────────────────┘
```

**Component Mapping:**
- Top Section: `Shape/Background` (type=Solid, Brand-700)
- Icon: `Icon/Archive-Icon` (size=64, color=Gold)
- Bottom Section: `Shape/Background` (type=Image)
- CTA: `CTA/Button` (type=Primary, size=Large)

**Variables:**
- `icon_name` → Icon variant
- `headline` → Headline Text
- `description` → Description Text
- `cta_text` → Button text
- `bottom_image` → Bottom background image

---

### **I-1: Data Grid (정보 그리드)**

```
구조:
┌─────────────────────────────────┐
│ [Header]                        │
│ "제목"                          │
├─────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐        │
│ │ [Card]  │ │ [Card]  │        │
│ │ Number  │ │ Number  │        │
│ │ Label   │ │ Label   │        │
│ └─────────┘ └─────────┘        │
│ ┌─────────┐ ┌─────────┐        │
│ │ [Card]  │ │ [Card]  │        │
│ │ Number  │ │ Number  │        │
│ │ Label   │ │ Label   │        │
│ └─────────┘ └─────────┘        │
└─────────────────────────────────┘
```

**Component Mapping:**
- Header: `Text/Dynamic-Text` (style=Heading/H2)
- Cards: `Card/Content-Card` (4 instances)
- Numbers: `Text/Dynamic-Text` (style=Number/Metric)
- Labels: `Text/Dynamic-Text` (style=Body/Small)

**Variables:**
- `title` → Header text
- `data_1_value`, `data_1_label` → Card 1
- `data_2_value`, `data_2_label` → Card 2
- `data_3_value`, `data_3_label` → Card 3
- `data_4_value`, `data_4_label` → Card 4

---

### **I-2: Timeline (시간순 정보)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
├─────────────────────────────────┤
│ ● [Date] ────────               │
│   [Event Title]                 │
│   [Description]                 │
│                                 │
│ ● [Date] ────────               │
│   [Event Title]                 │
│   [Description]                 │
│                                 │
│ ● [Date] ────────               │
│   [Event Title]                 │
│   [Description]                 │
└─────────────────────────────────┘
```

**Component Mapping:**
- Timeline Item: Custom component (Dot + Line + Text block)
- Date: `Text/Dynamic-Text` (style=Label/Bold, color=Gold)
- Event Title: `Text/Dynamic-Text` (style=Heading/H4)
- Description: `Text/Dynamic-Text` (style=Body/Medium)

**Variables:**
- `title` → Main title
- `event_1_date`, `event_1_title`, `event_1_desc` → Event 1
- `event_2_date`, `event_2_title`, `event_2_desc` → Event 2
- `event_3_date`, `event_3_title`, `event_3_desc` → Event 3

---

### **I-3: Stat Comparison (통계 비교)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
├─────────────────────────────────┤
│ [Category A]                    │
│ ████████████░░░░░░░░ 65%       │
│                                 │
│ [Category B]                    │
│ ██████████░░░░░░░░░░ 50%       │
│                                 │
│ [Category C]                    │
│ ███████████████░░░░░ 75%       │
│                                 │
│ [Source/Note]                   │
└─────────────────────────────────┘
```

**Component Mapping:**
- Progress Bar: Custom component (Background + Fill + Label)
- Category: `Text/Dynamic-Text` (style=Body/Medium)
- Percentage: `Text/Dynamic-Text` (style=Number/Metric)
- Note: `Text/Dynamic-Text` (style=Body/Caption)

**Variables:**
- `title` → Main title
- `stat_1_label`, `stat_1_value` → Stat 1
- `stat_2_label`, `stat_2_value` → Stat 2
- `stat_3_label`, `stat_3_value` → Stat 3
- `note` → Footer note

---

### **I-4: Feature List (특징 나열)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
│ "주요 특징"                     │
├─────────────────────────────────┤
│ ✓ [Feature 1]                   │
│   [Description]                 │
│                                 │
│ ✓ [Feature 2]                   │
│   [Description]                 │
│                                 │
│ ✓ [Feature 3]                   │
│   [Description]                 │
│                                 │
│ ✓ [Feature 4]                   │
│   [Description]                 │
└─────────────────────────────────┘
```

**Component Mapping:**
- List Item: `List/Bullet-Item` (4 instances)
- Icon: Checkmark icon from `Icon/Archive-Icon`

**Variables:**
- `title` → Main title
- `feature_1_title`, `feature_1_desc` → Feature 1
- `feature_2_title`, `feature_2_desc` → Feature 2
- `feature_3_title`, `feature_3_desc` → Feature 3
- `feature_4_title`, `feature_4_desc` → Feature 4

---

### **I-5: Quote + Source (인용형)**

```
구조:
┌─────────────────────────────────┐
│                                 │
│         "                       │
│                                 │
│    [Large Quote Text]           │
│    인용문 내용                   │
│                                 │
│         "                       │
│                                 │
│    ─────                        │
│    [Author Name]                │
│    [Source/Title]               │
└─────────────────────────────────┘
```

**Component Mapping:**
- Quote marks: `Icon/Archive-Icon` (size=48, color=Gold, opacity=30%)
- Quote: `Text/Dynamic-Text` (style=Display/Medium, alignment=Center)
- Author: `Text/Dynamic-Text` (style=Body/Large, color=Secondary)
- Source: `Text/Dynamic-Text` (style=Body/Small, color=Tertiary)

**Variables:**
- `quote_text` → Quote content
- `author_name` → Author
- `source` → Source/Title

---

### **P-1: Step-by-Step (단계형)**

```
구조:
┌─────────────────────────────────┐
│ [Title] "3단계로 시작하기"       │
├─────────────────────────────────┤
│ ┌───┐                           │
│ │ 1 │ [Step Title]              │
│ └───┘ [Description]             │
│                                 │
│ ┌───┐                           │
│ │ 2 │ [Step Title]              │
│ └───┘ [Description]             │
│                                 │
│ ┌───┐                           │
│ │ 3 │ [Step Title]              │
│ └───┘ [Description]             │
└─────────────────────────────────┘
```

**Component Mapping:**
- Step Item: `Step/Procedure-Step` (3 instances)
- Number badge: Circular, gradient fill

**Variables:**
- `title` → Main title
- `step_1_title`, `step_1_desc` → Step 1
- `step_2_title`, `step_2_desc` → Step 2
- `step_3_title`, `step_3_desc` → Step 3

---

### **P-2: Before/After (전후 비교)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
├─────────────────────────────────┤
│ BEFORE                          │
│ ┌─────────────────────┐         │
│ │ [Image/Content]     │         │
│ └─────────────────────┘         │
│                                 │
│        ↓ ↓ ↓                    │
│                                 │
│ AFTER                           │
│ ┌─────────────────────┐         │
│ │ [Image/Content]     │         │
│ └─────────────────────┘         │
└─────────────────────────────────┘
```

**Component Mapping:**
- Label: `Text/Dynamic-Text` (style=Label/Bold)
- Image: `Image/Dynamic-Image` (2 instances)
- Arrow: `Icon/Archive-Icon` (down arrows, color=Gold)

**Variables:**
- `title` → Main title
- `before_image` → Before image
- `before_caption` → Before caption
- `after_image` → After image
- `after_caption` → After caption

---

### **P-3: Process Flow (흐름도)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
├─────────────────────────────────┤
│ ┌─────────┐                     │
│ │ Step A  │ ──→                 │
│ └─────────┘                     │
│      ↓                          │
│ ┌─────────┐                     │
│ │ Step B  │ ──→                 │
│ └─────────┘                     │
│      ↓                          │
│ ┌─────────┐                     │
│ │ Result  │                     │
│ └─────────┘                     │
└─────────────────────────────────┘
```

**Component Mapping:**
- Process Box: `Card/Content-Card` (style=Outlined)
- Arrows: `Icon/Archive-Icon` (right/down arrows)

**Variables:**
- `title` → Main title
- `process_1_title`, `process_1_desc` → Process 1
- `process_2_title`, `process_2_desc` → Process 2
- `process_3_title`, `process_3_desc` → Result

---

### **C-1: Side-by-Side (좌우 비교)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
├────────────────┬────────────────┤
│ [Option A]     │ [Option B]     │
│                │                │
│ ✓ Feature 1    │ ✗ Feature 1    │
│ ✓ Feature 2    │ ✓ Feature 2    │
│ ✗ Feature 3    │ ✓ Feature 3    │
│ ✓ Feature 4    │ ✓ Feature 4    │
│                │                │
│ [Price/CTA]    │ [Price/CTA]    │
└────────────────┴────────────────┘
```

**Component Mapping:**
- Column: `Card/Content-Card` (2 instances)
- Check/X: `Icon/Archive-Icon` (checkmark/x-mark)
- CTA: `CTA/Button`

**Variables:**
- `title` → Main title
- `option_a_name`, `option_b_name` → Option names
- `option_a_features[]`, `option_b_features[]` → Feature lists
- `option_a_cta`, `option_b_cta` → CTA text

---

### **C-2: Pros/Cons (장단점)**

```
구조:
┌─────────────────────────────────┐
│ [Title]                         │
├─────────────────────────────────┤
│ 👍 장점                         │
│ ✓ [Pro 1]                       │
│ ✓ [Pro 2]                       │
│ ✓ [Pro 3]                       │
│                                 │
│ 👎 단점                         │
│ ✗ [Con 1]                       │
│ ✗ [Con 2]                       │
└─────────────────────────────────┘
```

**Component Mapping:**
- Section: `Card/Content-Card`
- List items: `List/Bullet-Item`
- Icons: Thumbs up/down + check/x marks

**Variables:**
- `title` → Main title
- `pros[]` → List of pros
- `cons[]` → List of cons

---

### **M-1: Product Showcase (아이템 소개)**

```
구조:
┌─────────────────────────────────┐
│      [Product Image]            │
│   ┌─────────────────┐           │
│   │                 │           │
│   │    [Image]      │           │
│   │                 │           │
│   └─────────────────┘           │
│                                 │
│   [Product Name]                │
│   [Category Badge]              │
│   [Description]                 │
│   [Price/CTA]                   │
└─────────────────────────────────┘
```

**Component Mapping:**
- Image: `Image/Dynamic-Image` (aspect=4:3)
- Name: `Text/Dynamic-Text` (style=Heading/H2)
- Badge: `Badge/Info-Badge`
- Description: `Text/Dynamic-Text` (style=Body/Medium)
- CTA: `CTA/Button`

**Variables:**
- `product_image` → Product image
- `product_name` → Name
- `category` → Badge text
- `description` → Description
- `price` → Price text
- `cta_text` → CTA button text

---

### **M-2: Collection Grid (컬렉션 그리드)**

```
구구조:
┌─────────────────────────────────┐
│ [Title] "이번 주 추천"           │
├─────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐        │
│ │ IMG │ │ IMG │ │ IMG │        │
│ └─────┘ └─────┘ └─────┘        │
│  Name    Name    Name           │
│                                 │
│ ┌─────┐ ┌─────┐ ┌─────┐        │
│ │ IMG │ │ IMG │ │ IMG │        │
│ └─────┘ └─────┘ └─────┘        │
│  Name    Name    Name           │
└─────────────────────────────────┘
```

**Component Mapping:**
- Grid: Auto Layout, 3 columns, 16px gap
- Item: `Card/Content-Card` (6 instances)
- Image: `Image/Dynamic-Image` (aspect=1:1)
- Name: `Text/Dynamic-Text` (style=Body/Small)

**Variables:**
- `title` → Main title
- `item_1_image`, `item_1_name` → Item 1
- `item_2_image`, `item_2_name` → Item 2
- ... (6 items total)

---

### **CTA-1: Primary CTA (주요 행동 유도)**

```
구조:
┌─────────────────────────────────┐
│                                 │
│      [Icon/Illustration]        │
│                                 │
│      [Headline]                 │
│   "지금 바로 시작하세요"         │
│                                 │
│      [Sub Text]                 │
│   "간단한 설명"                  │
│                                 │
│   ┌─────────────────┐           │
│   │  [CTA Button]   │           │
│   └─────────────────┘           │
│                                 │
│      [Small Print]              │
└─────────────────────────────────┘
```

**Component Mapping:**
- Icon: `Icon/Archive-Icon` (size=64)
- Headline: `Text/Dynamic-Text` (style=Display/Medium)
- Sub: `Text/Dynamic-Text` (style=Body/Large)
- CTA: `CTA/Button` (type=Primary, size=Large)
- Small print: `Text/Dynamic-Text` (style=Body/Caption)

**Variables:**
- `icon_name` → Icon variant
- `headline` → Headline text
- `subtext` → Sub text
- `cta_text` → Button text
- `small_print` → Footer text

---

### **CTA-2: Urgency CTA (긴급 행동 유도)**

```
구조:
┌─────────────────────────────────┐
│ [Urgent Banner]                 │
│ "⏰ 48시간 남음!"               │
├─────────────────────────────────┤
│                                 │
│      [Offer Headline]           │
│   "특별 할인 진행중"             │
│                                 │
│      [Large Discount]           │
│         50% OFF                 │
│                                 │
│   ┌─────────────────┐           │
│   │  [CTA Button]   │           │
│   │  "지금 신청"     │           │
│   └─────────────────┘           │
│                                 │
│   [Countdown/Deadline]          │
└─────────────────────────────────┘
```

**Component Mapping:**
- Urgent banner: `Badge/Info-Badge` (type=Warning, full-width)
- Headline: `Text/Dynamic-Text` (style=Heading/H2)
- Discount: `Text/Dynamic-Text` (style=Number/Display, color=Error)
- CTA: `CTA/Button` (type=Primary, size=Large)
- Countdown: `Text/Dynamic-Text` (style=Body/Medium, color=Warning)

**Variables:**
- `urgency_text` → Urgent banner text
- `headline` → Offer headline
- `discount` → Discount amount
- `cta_text` → Button text
- `deadline` → Countdown text

---

## 🔧 동적 요소 정의

### Text Variables

Figma API를 통해 업데이트할 텍스트 노드:

```javascript
{
  "textVariables": {
    // H-1
    "hero_number": "string",
    "hero_headline": "string",
    "hero_subtext": "string",
    
    // I-1 (Data Grid)
    "data_1_value": "string",
    "data_1_label": "string",
    // ... etc
    
    // Common
    "title": "string",
    "description": "string",
    "cta_text": "string"
  }
}
```

### Image Variables

Figma API를 통해 교체할 이미지 노드:

```javascript
{
  "imageVariables": {
    "bg_image": "https://...",
    "product_image": "https://...",
    "item_1_image": "https://...",
    // ... etc
  }
}
```

### Color Variables

Figma Variables 기능 활용:

```javascript
{
  "colorVariables": {
    "primary_color": "#4A4A6A",
    "accent_color": "#D4AF37",
    "bg_gradient_start": "#4A4A6A",
    "bg_gradient_end": "#1A1A2E"
  }
}
```

---

## 📦 Component Variants 시스템

### 예시: CTA/Button Component

**Properties:**
- `type`: Primary / Secondary / Outline / Ghost
- `size`: Small / Medium / Large
- `state`: Default / Hover / Active / Disabled

**Auto Layout:**
- Padding: 16px (S) / 20px (M) / 24px (L)
- Gap: 8px (icon + text)
- Horizontal resizing: Hug contents
- Vertical resizing: Fixed

**Interactive:**
- Hover effect: Shadow/Card-Hover
- Active effect: Scale 98%
- Prototype: Interactive component

---

## 🎯 API 연동을 위한 Naming Convention

### Node Naming

```
Slide-{number}                    → 슬라이드 프레임
  Template-{pattern}              → 템플릿 컴포넌트 인스턴스
    Text/{variable_name}          → 동적 텍스트
    Image/{variable_name}         → 동적 이미지
    Color/{variable_name}         → 동적 컬러
```

**예시:**
```
Slide-01
  Template-H1
    Text/hero_number
    Text/hero_headline
    Text/hero_subtext
    Color/bg_gradient_start
    Color/bg_gradient_end
```

### Layer ID 관리

Figma API는 Node ID를 사용하므로:

1. **Template 인스턴스 ID**: 변경 불가 (Figma 자동 생성)
2. **Variable 노드 ID**: JSON으로 매핑 저장

```json
{
  "slides": {
    "slide_01": {
      "frameId": "123:456",
      "template": "H-1",
      "variables": {
        "hero_number": {
          "nodeId": "123:457",
          "type": "text"
        },
        "hero_headline": {
          "nodeId": "123:458",
          "type": "text"
        }
      }
    }
  }
}
```

---

## ✅ 템플릿 체크리스트

각 템플릿 컴포넌트는 다음을 충족해야 합니다:

- [ ] Auto Layout 적용 (반응형 대응)
- [ ] 명확한 Naming Convention 준수
- [ ] Text/Image/Color Styles 연결
- [ ] Component Variants 정의
- [ ] 동적 변수 노드 식별 가능
- [ ] Safe Zone 내 콘텐츠 배치
- [ ] Constraints 설정 (화면 크기 변화 대응)
- [ ] 접근성 고려 (최소 명암 대비 4.5:1)
- [ ] 브랜드 가이드 준수

---

## 📚 참고 자료

- Figma Component Best Practices: https://www.figma.com/best-practices/components-styles-and-shared-libraries/
- Figma Auto Layout: https://help.figma.com/hc/en-us/articles/360040451373
- Figma Variables: https://help.figma.com/hc/en-us/articles/15339657135383
- GenArchive 브랜드 가이드: (내부 문서)

---

**문서 버전:** 1.0  
**작성일:** 2026-03-01  
**작성자:** GenArchive Design System Team
