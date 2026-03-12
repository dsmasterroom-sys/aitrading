# Figma Workflow Integration
# GenArchive 캐러셀 제작 워크플로우 통합 방안

## 📋 개요

본 문서는 기존 HTML 기반 캐러셀 제작 워크플로우를 Figma 기반으로 전환하는 통합 방안을 정의합니다.
디자이너, 콘텐츠 마케터, 개발자 간의 협업 프로세스를 최적화하고 디자이너급 퀄리티를 자동화합니다.

**핵심 목표:**
- 디자인 퀄리티 향상 (웹 폰트 → 프로 디자인 툴)
- 협업 효율성 증대 (실시간 피드백, 버전 관리)
- 자동화 수준 향상 (API 기반 생성)
- 유연성 확보 (템플릿 수정 용이)

---

## 🔄 워크플로우 비교

### 현재 워크플로우 (HTML 기반)

```
┌─────────────────────────────────────────────────────────────┐
│ Week 1-2: 콘텐츠 기획 & 작성                                 │
└─────────────────────────────────────────────────────────────┘
    ↓
[Contents Marketer]
  • weekly/copy.md 작성 (콘텐츠, 메시지)
  • 레이아웃 패턴 선택 (H-1, I-2, etc.)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Week 3: 디자인 초안                                          │
└─────────────────────────────────────────────────────────────┘
    ↓
[Designer]
  • Figma/Sketch에서 참고 디자인 작성 (선택적)
  • 브랜드 컬러, 폰트 지정
  • 이미지 에셋 준비
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Week 3-4: 개발 & 생성                                        │
└─────────────────────────────────────────────────────────────┘
    ↓
[Developer]
  • HTML 템플릿 수정 (templates/*.html)
  • CSS 스타일 조정 (shared/design-tokens.css)
  • python scripts/compose_carousel.py 실행
  • Puppeteer → PNG 추출
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 문제점                                                       │
└─────────────────────────────────────────────────────────────┘
  ✗ 디자인 제약: 웹 폰트, CSS 레이아웃 한계
  ✗ 피드백 루프: 디자이너가 직접 수정 불가, 개발자 의존
  ✗ 디자인 품질: 평범한 비주얼, 차별화 어려움
  ✗ 유지보수: HTML/CSS 코드 수정 필요
```

### 개선 워크플로우 (Figma 기반)

```
┌─────────────────────────────────────────────────────────────┐
│ Week 1-2: 콘텐츠 기획 & 작성                                 │
└─────────────────────────────────────────────────────────────┘
    ↓
[Contents Marketer]
  • weekly/copy.md 작성 (콘텐츠, 메시지)
  • 레이아웃 패턴 선택 (H-1, I-2, etc.)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Week 2-3: 디자인 작업 (Figma)                                │
└─────────────────────────────────────────────────────────────┘
    ↓
[Designer]
  • Figma에서 직접 템플릿 디자인
  • Components, Variants 활용
  • 실제 콘텐츠로 미리보기
  • 피드백 반영 (실시간 수정)
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Week 3: 자동 생성 (API)                                      │
└─────────────────────────────────────────────────────────────┘
    ↓
[Developer / Automation]
  • python scripts/figma_export.py --all --update --data weekly/copy.md
  • Figma Plugin이 템플릿 업데이트
  • Figma API로 PNG Export
  • 자동 최적화 & 메타데이터 삽입
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 개선 효과                                                    │
└─────────────────────────────────────────────────────────────┘
  ✓ 디자인 자유도: 전문 디자인 툴의 모든 기능
  ✓ 빠른 피드백: 디자이너가 Figma에서 직접 수정
  ✓ 디자인 품질: 디자이너급 비주얼
  ✓ 유지보수 용이: Figma 컴포넌트만 수정
  ✓ 협업 강화: Figma 댓글, 버전 히스토리
```

---

## 👥 역할별 워크플로우

### 1️⃣ Contents Marketer

**책임:**
- 콘텐츠 기획 및 작성
- 메시지 전달력 최적화
- 레이아웃 패턴 선택

**주요 작업:**

#### A. 콘텐츠 작성 (`weekly/copy.md`)

```markdown
---
title: "GenArchive 2월 3주차 캐러셀"
date: 2026-02-15
theme: "아카이브 성장 스토리"
---

## Slide 1: Hero (H-1)
**메시지:** GenArchive의 성장을 숫자로 보여줍니다
**패턴:** H-1 (Hero Statement)

```yaml
hero_number: "2,500+"
hero_headline: "GenArchive에서 만난 아카이브"
hero_subtext: "국내 최대 아카이브 커뮤니티"
bg_gradient_start: "#4A4A6A"
bg_gradient_end: "#1A1A2E"
```

## Slide 2: Timeline (I-2)
**메시지:** 주요 이정표를 시간순으로
**패턴:** I-2 (Timeline)

```yaml
title: "GenArchive 성장 히스토리"
events:
  - date: "2024.01"
    title: "서비스 런칭"
    desc: "베타 서비스 시작"
  - date: "2024.06"
    title: "1,000명 돌파"
    desc: "커뮤니티 성장"
  - date: "2025.12"
    title: "2,500명 달성"
    desc: "국내 최대 규모"
```

## Slide 3: CTA (CTA-1)
**메시지:** 지금 바로 가입하세요
**패턴:** CTA-1 (Primary CTA)

```yaml
icon_name: "rocket"
headline: "지금 바로 시작하세요"
subtext: "무료로 아카이브를 시작할 수 있습니다"
cta_text: "무료 가입하기"
small_print: "이메일만으로 간편 가입"
```
```

#### B. 레이아웃 선택 가이드

| 목적 | 추천 패턴 | 설명 |
|------|----------|------|
| 임팩트 강조 | H-1, H-2, H-3 | 숫자, 이미지, 헤드라인 중심 |
| 정보 전달 | I-1, I-2, I-3, I-4, I-5 | 데이터, 타임라인, 리스트 |
| 절차 설명 | P-1, P-2, P-3 | 단계, 비교, 흐름도 |
| 비교 분석 | C-1, C-2 | 좌우 비교, 장단점 |
| 아이템 소개 | M-1, M-2 | 제품, 컬렉션 |
| 행동 유도 | CTA-1, CTA-2 | 전환, 긴급성 |

#### C. 콘텐츠 체크리스트

- [ ] 각 슬라이드의 핵심 메시지가 명확한가?
- [ ] 레이아웃 패턴이 메시지와 일치하는가?
- [ ] 텍스트 길이가 적절한가? (제목 40자 이내, 본문 100자 이내)
- [ ] 이미지 에셋이 준비되었는가?
- [ ] 브랜드 톤앤매너와 일치하는가?

---

### 2️⃣ Designer

**책임:**
- Figma 템플릿 디자인 및 유지보수
- 브랜드 아이덴티티 반영
- 컴포넌트 시스템 관리

**주요 작업:**

#### A. 초기 설정 (한 번만)

1. **Figma 파일 생성**
   ```
   File → New Design File
   Name: "GenArchive Carousel System"
   ```

2. **Design System 구축**
   - Color Styles 생성 (`figma-template-guide.md` 참조)
   - Text Styles 생성
   - Effect Styles 생성 (Shadow, Blur)
   - Component Library 구축

3. **템플릿 17개 제작**
   - 각 패턴별 Component 생성
   - Variants 설정 (크기, 상태, 스타일)
   - Auto Layout 적용
   - Naming Convention 준수

4. **Node Mapping JSON 생성**
   ```
   Figma Plugin 실행 → "Export Node Mappings"
   → figma_mappings.json 다운로드
   ```

#### B. 콘텐츠 작업 (매주)

1. **콘텐츠 리뷰**
   - `weekly/copy.md` 읽기
   - 각 슬라이드의 메시지 이해

2. **Figma에서 미리보기**
   - Slides 페이지로 이동
   - Component 인스턴스 배치
   - 실제 콘텐츠로 텍스트 교체 (임시)
   - 레이아웃 검토, 조정

3. **피드백 반영**
   - Figma 댓글로 소통
   - 디자인 수정 (Colors, Fonts, Spacing)
   - 버전 저장 (Save Version History)

4. **최종 승인**
   - 슬라이드 구성 확정
   - API 실행 준비 완료 신호

#### C. 템플릿 업데이트 프로세스

```
┌─────────────────────────────────────┐
│ 1. 기존 템플릿 복제                  │
│    Component → Duplicate             │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 2. 디자인 수정                       │
│    Colors, Fonts, Layout             │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 3. 테스트 슬라이드 생성              │
│    실제 콘텐츠로 검증                │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 4. Component 업데이트                │
│    Main Component 교체               │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 5. 버전 저장                         │
│    File → Save Version               │
│    "Updated H-1 template"            │
└─────────────────────────────────────┘
```

#### D. 디자이너 팁

**효율적인 작업:**
- Component Variants 활용으로 여러 스타일 한 번에 관리
- Auto Layout으로 반응형 디자인
- Styles로 일관성 유지
- Team Library로 컴포넌트 공유

**피해야 할 것:**
- Absolute positioning (Auto Layout 사용)
- Hardcoded colors (Color Styles 연결)
- 복잡한 그룹 구조 (Flatten 사용)
- Node 이름 변경 (API 연동 깨짐)

---

### 3️⃣ Developer

**책임:**
- Figma API 연동 및 자동화
- 스크립트 유지보수
- 에러 핸들링 및 Fallback

**주요 작업:**

#### A. 초기 설정

1. **환경 변수 설정**
   ```bash
   cp .env.example .env
   vim .env
   
   # FIGMA_ACCESS_TOKEN, FIGMA_FILE_ID 입력
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   
   # requirements.txt
   # requests==2.31.0
   # python-dotenv==1.0.0
   # Pillow==10.0.0  # PNG 최적화
   # PyYAML==6.0     # copy.md 파싱
   ```

3. **Figma 연결 테스트**
   ```bash
   python scripts/figma_export.py --test
   ```

4. **Node Mappings 설정**
   - 디자이너로부터 `figma_mappings.json` 받기
   - 프로젝트 루트에 배치

#### B. 캐러셀 생성 (매주)

**Manual 방식 (추천):**

```bash
# 1. 콘텐츠 파일 확인
cat weekly/copy.md

# 2. Figma Plugin 실행 (Figma 앱에서)
#    Plugin: "GenArchive Updater"
#    Load: weekly/copy.md
#    Apply Updates

# 3. Export 실행
python scripts/figma_export.py --all --optimize

# 4. 결과 확인
ls output/
# → slide_01.png, slide_02.png, ...
```

**Automated 방식 (고급):**

```bash
# One-command generation
python scripts/figma_export.py \
  --all \
  --update \
  --data weekly/copy.md \
  --optimize \
  --fallback
```

#### C. 트러블슈팅

**문제: Figma API 인증 실패**
```
✗ 401 Unauthorized

해결:
1. .env의 FIGMA_ACCESS_TOKEN 확인
2. Figma Settings에서 토큰 재발급
3. 토큰 권한 확인 (File content: Read)
```

**문제: Node ID 찾을 수 없음**
```
✗ Node not found: 123:456

해결:
1. Figma 파일에서 노드 존재 확인
2. figma_mappings.json 재생성
3. Figma File ID 확인
```

**문제: 이미지 Export 실패**
```
✗ Export failed: 500 Internal Server Error

해결:
1. Figma API 상태 확인 (status.figma.com)
2. Rate limit 대기 (429 에러 시)
3. Fallback 사용: --fallback 플래그
```

#### D. 자동화 (Cron / CI/CD)

**GitHub Actions 예시:**

```yaml
# .github/workflows/generate-carousel.yml

name: Generate Weekly Carousel

on:
  schedule:
    - cron: '0 9 * * MON'  # 매주 월요일 오전 9시
  workflow_dispatch:  # 수동 실행 가능

jobs:
  generate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate carousel
        env:
          FIGMA_ACCESS_TOKEN: ${{ secrets.FIGMA_ACCESS_TOKEN }}
          FIGMA_FILE_ID: ${{ secrets.FIGMA_FILE_ID }}
        run: |
          python scripts/figma_export.py --all --optimize --fallback
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: carousel-images
          path: output/*.png
      
      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add output/
          git commit -m "Generate carousel for $(date +%Y-%m-%d)"
          git push
```

---

## 🔄 통합 워크플로우 (전체 프로세스)

### Timeline (4주 사이클)

```
┌──────────┬──────────┬──────────┬──────────┐
│  Week 1  │  Week 2  │  Week 3  │  Week 4  │
└──────────┴──────────┴──────────┴──────────┘

Week 1: 기획 & 콘텐츠
├─ Day 1-2: 주제 선정, 메시지 정의
├─ Day 3-5: copy.md 작성, 레이아웃 선택
└─ Day 6-7: 내부 리뷰, 피드백

Week 2: 디자인 & 에셋
├─ Day 1-2: Figma 템플릿 선택/조정
├─ Day 3-4: 실제 콘텐츠로 미리보기
├─ Day 5-6: 디자인 피드백 반영
└─ Day 7: 이미지 에셋 준비 완료

Week 3: 생성 & 검증
├─ Day 1: Figma Plugin으로 업데이트
├─ Day 2: API Export 실행
├─ Day 3-4: QA (텍스트, 이미지, 색상)
├─ Day 5-6: 수정 및 재생성
└─ Day 7: 최종 승인

Week 4: 발행 & 분석
├─ Day 1: Instagram, LinkedIn 포스팅
├─ Day 2-7: 반응 모니터링, 데이터 수집
└─ 다음 사이클 피드백
```

### 실시간 협업 프로세스

```
[Contents Marketer] ──────────────────────────────┐
   │                                              │
   │ 1. copy.md 작성                              │
   │                                              │
   ↓                                              │
[Figma File]                                      │
   │                                              │
   │ 2. 댓글로 메시지 전달                         │
   │    "@Designer 이번 주 테마는..."             │
   │                                              │
   ↓                                              │
[Designer] ───────────────────────────────────────┤
   │                                              │
   │ 3. 템플릿 수정                                │
   │    색상, 레이아웃 조정                        │
   │                                              │
   │ 4. 댓글로 피드백 요청                         │
   │    "@Marketer 이렇게 하면 어떨까요?"          │
   │                                              │
   ↓                                              │
[Contents Marketer]                               │
   │                                              │
   │ 5. Figma에서 확인                             │
   │    "좋아요! 승인합니다" ✓                    │
   │                                              │
   ↓                                              │
[Developer] ──────────────────────────────────────┤
   │                                              │
   │ 6. 스크립트 실행                              │
   │    python figma_export.py --all              │
   │                                              │
   ↓                                              │
[Output: PNG files]                               │
   │                                              │
   │ 7. 최종 QA                                   │
   │                                              │
   ↓                                              │
[✓ Ready to Publish] ─────────────────────────────┘
```

---

## 📊 성능 비교

### 작업 시간

| 작업 단계 | HTML 방식 | Figma 방식 | 개선 |
|----------|----------|-----------|------|
| 템플릿 수정 | 2시간 (HTML/CSS 코딩) | 30분 (Figma 디자인) | **-75%** |
| 피드백 반영 | 1시간 (코드 재수정) | 10분 (Figma 수정) | **-83%** |
| PNG 생성 | 30분 (Puppeteer 실행) | 5분 (API Export) | **-83%** |
| **전체** | **3.5시간** | **45분** | **-79%** |

### 디자인 퀄리티

| 항목 | HTML 방식 | Figma 방식 |
|------|----------|-----------|
| 폰트 렌더링 | 웹 폰트 (제한적) | 프로 폰트 (무제한) |
| 그래픽 효과 | CSS만 가능 | 모든 디자인 툴 기능 |
| 커스텀 에셋 | 외부 준비 필요 | Figma에서 직접 제작 |
| 일관성 | CSS 변수 의존 | Design System 기반 |
| **종합 평가** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 협업 효율성

| 항목 | HTML 방식 | Figma 방식 |
|------|----------|-----------|
| 실시간 미리보기 | ✗ (로컬 빌드 필요) | ✓ (Figma 실시간 동기화) |
| 댓글/피드백 | 외부 툴 사용 | Figma 내장 |
| 버전 관리 | Git (코드 diff 어려움) | Figma History (비주얼) |
| 권한 관리 | 레포 접근 제어 | Figma 세밀한 권한 |
| **종합 평가** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚧 마이그레이션 가이드

### 기존 HTML 시스템 → Figma 시스템

#### Phase 1: 병행 운영 (1개월)

```
Week 1-2: Figma 시스템 구축
  - Figma 파일 생성
  - 템플릿 17개 디자인
  - Node mappings 생성

Week 3-4: 파일럿 테스트
  - 1~2개 슬라이드를 Figma로 생성
  - HTML 방식과 비교
  - 문제점 파악 및 개선
```

#### Phase 2: 전환 (1개월)

```
Week 5-6: Figma 주, HTML 보조
  - 대부분 슬라이드를 Figma로 생성
  - 복잡한 케이스만 HTML 사용
  - Fallback 메커니즘 테스트

Week 7-8: Figma 완전 전환
  - 모든 슬라이드를 Figma로 생성
  - HTML 방식은 Fallback으로만 유지
  - 프로세스 문서화
```

#### Phase 3: 최적화 (지속)

```
- 템플릿 개선 (사용자 피드백 반영)
- 자동화 고도화 (CI/CD 통합)
- 성능 튜닝 (캐싱, 배치 처리)
- 새로운 패턴 추가
```

### 마이그레이션 체크리스트

**준비 단계:**
- [ ] Figma 계정 생성 (팀 플랜 권장)
- [ ] Access Token 발급
- [ ] 기존 디자인 에셋 정리 (폰트, 이미지, 컬러)
- [ ] 팀원 교육 (Figma 사용법, 새 워크플로우)

**구축 단계:**
- [ ] Design System 구축 (Colors, Text, Effects)
- [ ] Component Library 제작 (17개 템플릿)
- [ ] Node Mappings JSON 생성
- [ ] Python 스크립트 설치 및 테스트

**테스트 단계:**
- [ ] 파일럿 슬라이드 생성 (1~2개)
- [ ] 품질 비교 (HTML vs Figma)
- [ ] 성능 측정 (생성 시간, 파일 크기)
- [ ] 팀 피드백 수집

**전환 단계:**
- [ ] 모든 슬라이드를 Figma로 전환
- [ ] Fallback 메커니즘 검증
- [ ] 문서화 완료
- [ ] HTML 방식 아카이브 (삭제하지 않음)

---

## 🎯 성공 지표 (KPI)

### 정량적 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 디자인 작업 시간 | -70% 이상 | 작업 시간 로그 |
| 피드백 사이클 | 1일 이내 | 댓글 타임스탬프 |
| 생성 에러율 | 5% 이하 | 로그 분석 |
| 이미지 품질 점수 | 4.5/5 이상 | 팀 평가 |

### 정성적 지표

- **디자이너 만족도:** Figma에서 자유롭게 디자인 가능
- **마케터 만족도:** 빠른 피드백, 높은 완성도
- **개발자 만족도:** 자동화로 반복 작업 감소
- **최종 사용자 반응:** 인스타그램 engagement 증가

### 모니터링 대시보드

```python
# monitoring/dashboard.py

def generate_weekly_report():
    """
    주간 리포트 생성
    
    포함 내용:
    - 생성된 슬라이드 수
    - Figma API 호출 횟수
    - 에러 발생 횟수
    - 평균 생성 시간
    - Fallback 사용 횟수
    """
    report = {
        "week": "2026-W10",
        "slides_generated": 8,
        "figma_api_calls": 24,
        "errors": 0,
        "avg_time_seconds": 47,
        "fallback_used": 0,
        "quality_score": 4.7
    }
    
    return report
```

---

## 🔮 미래 확장 계획

### Short-term (3개월)

- **A/B 테스트:** 같은 슬라이드의 여러 변형 자동 생성
- **다국어 지원:** 텍스트 자동 번역 후 Export
- **동영상 생성:** Figma → Video (Prototype + Lottie)

### Mid-term (6개월)

- **AI 추천:** 콘텐츠 분석 후 최적 레이아웃 자동 제안
- **자동 스케줄링:** 생성 → 승인 → 포스팅 완전 자동화
- **Analytics 통합:** 성과 데이터 기반 템플릿 최적화

### Long-term (1년)

- **GenArchive Design System:** 다른 프로젝트에도 재사용
- **Figma Plugin Marketplace 배포:** 오픈소스로 공개
- **템플릿 마켓플레이스:** 커뮤니티 기여 템플릿

---

## 📚 참고 문서

### 내부 문서
- `figma-template-guide.md` - 템플릿 구조 설계
- `figma-api-design.md` - API 연동 설계
- `gena_feed/skills/design-visual.md` - 기존 레이아웃 패턴

### 외부 자료
- Figma for Teams: https://www.figma.com/teams/
- Figma Best Practices: https://www.figma.com/best-practices/
- Design Systems with Figma: https://www.designsystems.com/

### 교육 자료
- Figma 기초 (30분): https://help.figma.com/hc/en-us/articles/360040450213
- Auto Layout 마스터 (1시간): https://www.youtube.com/watch?v=...
- Components & Variants (45분): https://www.youtube.com/watch?v=...

---

## ❓ FAQ

### Q1: HTML 방식은 완전히 제거하나요?
**A:** 아니요. Fallback으로 유지합니다. Figma API 장애 시 자동으로 HTML 방식으로 전환됩니다.

### Q2: Figma 유료 플랜이 필요한가요?
**A:** 개인 프로젝트는 무료 플랜으로도 가능하지만, 팀 협업을 위해서는 Professional 플랜(월 $12/인)을 권장합니다.

### Q3: 디자이너가 없으면 어떻게 하나요?
**A:** 초기 템플릿만 한 번 설정하면, 이후에는 콘텐츠만 바꿔서 자동 생성됩니다. 외부 디자이너 초기 작업 위탁 가능.

### Q4: 기존 HTML 템플릿을 Figma로 변환할 수 있나요?
**A:** 네. HTML2Figma 도구(Figma Plugin)를 사용하거나, 디자이너가 수동으로 재제작합니다. 재제작을 권장합니다 (더 나은 결과).

### Q5: Figma API Rate Limit은?
**A:** 개인: 분당 60회, 팀: 분당 300회. 일반적인 사용에는 충분합니다. 캐싱으로 호출 최소화.

### Q6: 여러 사람이 동시에 Figma 파일을 수정하면?
**A:** Figma는 실시간 동기화를 지원합니다. Google Docs처럼 여러 명이 동시 작업 가능.

### Q7: 버전 관리는 어떻게 하나요?
**A:** Figma의 Version History 기능 사용. 언제든지 이전 버전으로 복원 가능. (Pro 플랜: 무제한 히스토리)

### Q8: 로컬에서도 작업 가능한가요?
**A:** Figma는 웹 기반이지만, Desktop App도 제공합니다. Offline 모드는 제한적이므로 인터넷 연결 권장.

---

## 📞 지원 및 문의

**기술 지원:**
- Slack: #genarchive-design
- Email: dev@genarchive.com
- 이슈 트래킹: GitHub Issues

**디자인 문의:**
- Figma 댓글 기능 활용
- Design Review 미팅: 매주 수요일 오후 2시

**긴급 상황:**
- Figma API 장애 시: Fallback 자동 실행
- Figma 파일 손상 시: Version History에서 복구
- 담당자 연락 불가 시: dev@genarchive.com

---

**문서 버전:** 1.0  
**작성일:** 2026-03-01  
**작성자:** GenArchive Team  
**다음 업데이트:** 2026-04-01 (파일럿 테스트 결과 반영)
