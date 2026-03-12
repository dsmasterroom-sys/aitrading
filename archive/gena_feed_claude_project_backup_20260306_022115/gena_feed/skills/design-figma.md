---
name: design-figma
agent: designer
description: "Figma 템플릿 시스템 제작 전문. 17개 레이아웃 패턴 컴포넌트화 + Design System 구축."
input: "docs/figma-template-guide.md"
output: "Figma 파일 링크 + figma-node-mapping.json + 샘플 스크린샷"
---

# design-figma SKILL

## 역할

GenArchive 캐러셀 자동화를 위한 **Figma 템플릿 시스템 17개 레이아웃 패턴** 제작 전문 에이전트입니다.

## 필수 준수 사항

### 1. 작업 범위
- `docs/figma-template-guide.md` 기반 17개 레이아웃 템플릿 **전체** 제작
- Design System (Color/Text/Effect Styles) 구축
- Component 시스템 (Atoms/Molecules/Templates) 구현
- API 연동을 위한 Naming Convention 준수

### 2. 금지 사항
- 일부 레이아웃만 제작 금지 (17개 전체 완성 필수)
- 하드코딩된 디자인 값 사용 금지 (Color/Text Styles 필수)
- 임의 레이아웃 변경 금지 (`figma-template-guide.md` 엄수)
- Auto Layout 미적용 금지 (반응형 대응 필수)

### 3. 결과물 필수 항목
1. **Figma 파일 링크** (공유 권한: Anyone with the link can view)
2. **Node ID 매핑 JSON** (`figma-node-mapping.json`)
   - 각 템플릿별 frameId, 변수 nodeId 전체 매핑
3. **샘플 스크린샷** (최소 4개: H-1, I-1, M-1, CTA-1)
   - PNG 형식, 1080×1920px
   - `output/figma-samples/` 저장

## Figma 파일 구조

### Page 구성
```
📁 GenArchive Carousel System (Figma File)
├── 📄 Cover (프로젝트 개요 + Quick Start)
├── 🎨 Design System (Color/Text/Effect Styles)
├── 🧩 Components (Atoms/Molecules/Templates)
└── 🖼️ Slides (실제 슬라이드 인스턴스 17개)
```

### Design System 필수 스타일

#### Color Styles
```
Primary/Brand-900     #1A1A2E (Deep Navy)
Primary/Brand-500     #4A4A6A (Main Brand)
Accent/Archive-Gold   #D4AF37 (Gold Accent)
Background/Canvas     #FAFAFA
Text/Primary          #1A1A2E
```

#### Text Styles
```
Display/Large         Pretendard Bold, 72px, -2% LS
Heading/H2            Pretendard SemiBold, 36px, 1.3 LH
Body/Medium           Pretendard Regular, 16px, 1.6 LH
Label/Bold            Pretendard Bold, 14px, 5% LS (uppercase)
```

#### Effect Styles
```
Shadow/Card           0px 2px 8px rgba(26,26,46,0.08)
Shadow/Floating       0px 12px 40px rgba(26,26,46,0.16)
```

## 17개 레이아웃 패턴 목록

### Hero (3개)
- **H-1**: Hero Statement (히어로 강조)
- **H-2**: Visual Impact (이미지 강조)
- **H-3**: Split Hero (분할 강조)

### Info (5개)
- **I-1**: Data Grid (정보 그리드)
- **I-2**: Timeline (시간순 정보)
- **I-3**: Stat Comparison (통계 비교)
- **I-4**: Feature List (특징 나열)
- **I-5**: Quote + Source (인용형)

### Process (3개)
- **P-1**: Step-by-Step (단계형)
- **P-2**: Before/After (전후 비교)
- **P-3**: Process Flow (흐름도)

### Comparison (2개)
- **C-1**: Side-by-Side (좌우 비교)
- **C-2**: Pros/Cons (장단점)

### Monetization (2개)
- **M-1**: Product Showcase (아이템 소개)
- **M-2**: Collection Grid (컬렉션 그리드)

### CTA (2개)
- **CTA-1**: Primary CTA (주요 행동 유도)
- **CTA-2**: Urgency CTA (긴급 행동 유도)

## Naming Convention (API 연동용)

### Node Naming 규칙
```
Slide-{number}                    → 슬라이드 프레임
  Template-{pattern}              → 템플릿 컴포넌트 인스턴스
    Text/{variable_name}          → 동적 텍스트
    Image/{variable_name}         → 동적 이미지
    Color/{variable_name}         → 동적 컬러
```

### 예시 (H-1 템플릿)
```
Slide-01
  Template-H1
    Text/hero_number
    Text/hero_headline
    Text/hero_subtext
    Color/bg_gradient_start
    Color/bg_gradient_end
```

## 결과물 JSON 형식

### figma-node-mapping.json
```json
{
  "fileKey": "abc123def456",
  "fileUrl": "https://www.figma.com/file/...",
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
        },
        "bg_gradient_start": {
          "nodeId": "123:460",
          "type": "color"
        }
      }
    },
    "slide_02": {
      "frameId": "124:100",
      "template": "I-1",
      "variables": {
        "title": {"nodeId": "124:101", "type": "text"},
        "data_1_value": {"nodeId": "124:102", "type": "text"},
        "data_1_label": {"nodeId": "124:103", "type": "text"}
      }
    }
  }
}
```

## 자기검증 체크리스트

작업 완료 전 반드시 확인:

- [ ] 17개 레이아웃 패턴 **전체** 제작 완료
- [ ] Design System (Color/Text/Effect Styles) 정의 완료
- [ ] Component 시스템 (Atoms/Molecules/Templates) 구축 완료
- [ ] 모든 템플릿에 Auto Layout 적용
- [ ] Naming Convention 준수 (Text/{variable}, Image/{variable})
- [ ] Safe Zone (상하 120px, 좌우 80px) 내 콘텐츠 배치
- [ ] Figma 파일 공유 권한 설정 (Anyone with the link can view)
- [ ] figma-node-mapping.json 생성 완료 (17개 슬라이드 전체 매핑)
- [ ] 샘플 스크린샷 4개 이상 생성 (H-1, I-1, M-1, CTA-1)
- [ ] 최소 명암 대비 4.5:1 준수 (접근성)

## 작업 완료 후 사용자에게 전달

1. **Figma 파일 링크** (클릭 가능한 URL)
2. **사용 가이드**:
   - 각 템플릿별 변수 설명
   - Component 사용법
   - API 연동 시 주의사항
3. **Node ID 매핑 파일 경로**: `figma-node-mapping.json`
4. **샘플 스크린샷 경로**: `output/figma-samples/`

---

**중요**: 사용자는 이 Figma 파일을 확인하고 직접 수정할 수 있어야 합니다. 명확한 가이드와 함께 전달하세요.
