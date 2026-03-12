# PROJECT.md - 인스타그램 자동화 프로젝트

**프로젝트**: @gena_feed 인스타그램 콘텐츠 자동화  
**목표**: 완전 자동화된 콘텐츠 제작 → 발행 → 운영 → 분석 → 개선 사이클

---

## 👥 역할 분담 (2026-03-06 확정)

### 🔨 클로드 코드 (Claude Code) - 제작자
**담당**: 콘텐츠 생성 전체
- 콘텐츠 기획 (트렌드 조사, 주제 선정)
- 콘텐츠 제작 (이미지, 영상, 카피)
- 콘텐츠 생성 (HTML, 슬라이드, 릴스)
- QA (품질 검증, 오류 수정)

**도구**: 
- 파일 시스템 (Read, Write, Edit)
- 개발 환경 (exec, process)
- 9개 에이전트 (researcher ~ qa-reviewer)
- 15개 스킬
- 디자인 시스템

**산출물**:
- research.md, items.json
- prompts.json
- plan.md, copy.md
- assets/*.png
- slides/*.html, *.png
- qa-report.md

---

### 🎯 자비스 (Jarvis) - 운영자 & 전략가
**담당**: 콘텐츠 운영 및 전략
- **콘텐츠 게시** (Instagram API, 스케줄링)
- **팔로워 관리 및 chat 운영**:
  - 캡션 관리 (해시태그 최적화)
  - 댓글 관리 (응답, 모니터링)
  - DM 관리 (고객 응대)
- **KPI 분석 및 평가**:
  - 조회수, 좋아요, 저장, 공유
  - 팔로워 증가율
  - 참여율 (Engagement Rate)
- **목표 조정 및 콘텐츠 방향 설정**:
  - 성과 분석 → 인사이트 도출
  - 다음 주제 제안
  - 전략 보고서 작성
- **보고서 → 클로드 코드 전달**

**도구**:
- Instagram Graph API
- 메시징 (Telegram, message tool)
- 데이터 분석
- 크론 작업
- sessions_send (클로드 코드와 통신)

**산출물**:
- 발행 완료 확인
- 주간/월간 성과 리포트
- 전략 제안서
- 다음 주제 브리프

---

## 🎯 핵심 원칙

**역할 분리**: 제작 vs 운영. 각자 전문성 집중.  
**한 에이전트 = 한 가지 일**. 컨텍스트 오염 방지.

---

## 🏗️ 3레이어 구조

```
L1: 오케스트레이터 (PROJECT.md) → 라우팅, 게이팅, 사용자 컨펌
L2: 9개 에이전트 (agents/*.md) → 각자 단일 역할
L3: 15개 스킬 (skills/*.SKILL.md) → 150줄 이내 실행 명세
```

---

## 📊 9개 에이전트 맵

| 에이전트 | 모델 | 역할 | 허용 도구 | 금지 |
|---|---|---|---|---|
| researcher | sonnet-4-6 | 트렌드 리서치 | WebSearch, Read | Write, Edit |
| item-researcher | sonnet-4-6 | 아이템 리서치 | WebSearch, WebFetch, Read | Write, Edit |
| prompt-engineer | opus-4-6 | 프롬프트 생성 | Read, Write | WebSearch, Edit |
| contents-marketer | gpt-5.2 | 기획/카피 | Read, Write | WebSearch, HTML |
| designer | gpt-5-mini | 이미지 생성 | Read, Write, Nanogen API | HTML, QA |
| video-agent | sonnet-4-6 | 영상 생성 | Read, Write, Nanogen API, ffmpeg | 기획, QA |
| developer | sonnet-4-6 | HTML 구현 | Read, Write, Edit, Bash | 기획, QA |
| qa-reviewer | gpt-5-mini | 검수 전담 | Read, validate_slide.py | Write, Edit |
| scheduler | gpt-5-mini | 발행/성과 | Read, Write, Meta API, Bash | 콘텐츠 생성 |

---

## 🔄 데이터 흐름

### 캐러셀 제작 파이프라인

```
트렌드 주제 입력
    ↓
[researcher + item-researcher] 병렬 실행
    ↓
prompt-engineer
    ↓
[contents-marketer + designer] 병렬 실행
    ↓
developer (⚠️ 패턴 매핑 필수)
    ↓
qa-reviewer
    ↓
[고/중 이슈] → developer 수정 루프 (최대 3회)
    ↓
QA 통과 → scheduler → 발행
```

### Phase 4: Developer 패턴 매핑 규칙 (필수)

**Orchestrator가 Phase 4 실행 시 반드시 패턴 지정**:

```javascript
// 슬라이드 타입 분석 (prompts.json 기반)
const pattern_mapping = {
  1: "01-hero.html",        // 훅/히어로
  2: "11-overlay.html",     // 문제 제기 (오버레이)
  3: "02-split.html",       // 솔루션 (분할)
  4: "03-product.html",     // 제품 1
  5: "03-product.html",     // 제품 2
  6: "03-product.html",     // 제품 3
  7: "03-product.html",     // 제품 4
  8: "03-product.html",     // 제품 5
  9: "05-grid-4.html",      // 라인업 (그리드)
  10: "06-cta.html"         // CTA
}

// developer에게 전달
sessions_spawn({
  agentId: "developer",
  task: `
각 슬라이드에 지정된 패턴 사용 (새로운 CSS 작성 절대 금지):

패턴 매핑: ${JSON.stringify(pattern_mapping, null, 2)}

작업 단계:
1. 각 슬라이드 번호에 해당하는 patterns/*.html 파일 읽기
2. {{PLACEHOLDER}} 부분만 copy.md 내용으로 교체
3. 이미지는 base64로 인라인 삽입
4. CSS 변수 그대로 유지 (하드코딩 금지)
5. slides/ 폴더에 HTML + PNG 저장

필수 준수 사항:
- design-system/patterns/ 에서만 선택
- 레이아웃 구조 변경 금지
- 새로운 CSS 규칙 추가 금지
- CSS 변수만 참조
  `
})
```

### 패턴 선택 가이드

| 슬라이드 타입 | 사용 패턴 | 특징 |
|---|---|---|
| 훅/히어로 | 01-hero.html | 전체 이미지 + 하단 텍스트 |
| 분할 레이아웃 | 02-split.html | 좌우 분할 |
| 제품 소개 | 03-product.html | 중앙 이미지 + 정보 박스 |
| 인용/강조 | 04-quote.html | 큰 인용문 |
| 그리드 (4개) | 05-grid-4.html | 2×2 그리드 |
| CTA | 06-cta.html | 행동 유도 버튼 |
| 전체 화면 | 07-fullscreen.html | 풀스크린 이미지 |
| 텍스트 중심 | 08-text-heavy.html | 긴 텍스트 |
| 미니멀 | 09-minimal.html | 최소 요소 |
| 볼드 타이포 | 10-bold-typo.html | 큰 글씨 강조 |
| 오버레이 | 11-overlay.html | 이미지 위 그라데이션 |
| 비교 | 12-comparison.html | 좌우 비교 |

### 릴스 제작 파이프라인

```
트렌드 주제 입력
    ↓
[researcher + item-researcher] 병렬
    ↓
contents-marketer (씬 기획)
    ↓
prompt-engineer (씬별 프롬프트)
    ↓
[designer + video-agent] 병렬
    ↓
developer (자막 오버레이)
    ↓
qa-reviewer → scheduler
```

---

## 🚦 게이팅 규칙

### G1: 토픽 확정 게이트
**위치**: researcher 완료 후  
**조건**: research.md 작성 완료  
**사용자 확인**: 추천 토픽 6개 → 마보스님 선택  
**통과**: 선택된 토픽으로 item-researcher 스폰

### G2: 프롬프트 검증 게이트
**위치**: prompt-engineer 완료 후  
**조건**: prompts.json 10개 체크리스트 통과  
**자동 검증**: prompt-quality-check.SKILL.md  
**실패 시**: prompt-engineer 재생성

### G3: QA 통과 게이트
**위치**: qa-reviewer 완료 후  
**조건**: qa-report.md 고/중 이슈 0건  
**루프**: 이슈 발견 → developer 수정 (최대 3회)  
**에스컬레이션**: 3회 실패 시 오케스트레이터 개입

### G4: 발행 승인 게이트
**위치**: scheduler 발행 직전  
**조건**: 최종 슬라이드/영상 확인  
**사용자 확인**: 마보스님 최종 승인 (선택)  
**자동 발행**: QA 통과 시 자동 (설정 가능)

---

## 🎛️ 라우팅 규칙

### 사용자 요청 → 에이전트 매핑

**"트렌드 조사해줘"** → researcher  
**"아이템 찾아줘"** → item-researcher  
**"프롬프트 만들어줘"** → prompt-engineer  
**"캐러셀 기획해줘"** → contents-marketer  
**"이미지 생성해줘"** → designer  
**"릴스 만들어줘"** → video-agent  
**"슬라이드 HTML 만들어줘"** → developer  
**"QA 해줘"** → qa-reviewer  
**"발행 예약해줘"** → scheduler

### 병렬 실행 포인트

**트렌드 + 아이템**:
```
sessions_spawn(researcher)
sessions_spawn(item-researcher)
```

**기획 + 이미지**:
```
sessions_spawn(contents-marketer)
sessions_spawn(designer)
```

---

## 📁 파일 구조

```
gena_feed/
├── PROJECT.md (이 파일, 오케스트레이터)
├── README.md (사람용 프로젝트 개요)
├── .env (API 키)
│
├── agents/ (9개 에이전트)
│   ├── researcher.md
│   ├── item-researcher.md
│   ├── prompt-engineer.md
│   ├── contents-marketer.md
│   ├── designer.md
│   ├── video-agent.md
│   ├── developer.md
│   ├── qa-reviewer.md
│   └── scheduler.md
│
├── skills/ (15개 스킬, 각 150줄 이내)
│   ├── research-trend.SKILL.md
│   ├── research-hashtag.SKILL.md
│   ├── item-research.SKILL.md
│   ├── item-visual-desc.SKILL.md
│   ├── prompt-image.SKILL.md
│   ├── prompt-video.SKILL.md
│   ├── plan-content.SKILL.md
│   ├── write-copy.SKILL.md
│   ├── design-visual.SKILL.md
│   ├── html-slide.SKILL.md
│   ├── video-nanogen-call.SKILL.md
│   ├── video-ffmpeg-assemble.SKILL.md
│   ├── qa-visual.SKILL.md
│   ├── qa-factcheck.SKILL.md
│   └── schedule-post.SKILL.md
│
├── shared/
│   ├── design-system/
│   │   ├── design-tokens.css
│   │   ├── patterns/ (29개 HTML 패턴)
│   │   └── validate_slide.py
│   └── gena-master-prompt.md
│
├── workflows/
│   ├── reels-workflow.md
│   ├── carousel-workflow.md
│   └── story-workflow.md
│
├── scripts/
│   ├── nanogen_outfit_swap.py
│   ├── nanogen_image.py
│   ├── nanogen_video.py
│   └── ffmpeg_assemble.py
│
└── content/ (콘텐츠별 작업 폴더)
    └── {YYYYMMDD}_{series_name}/
        ├── research.md
        ├── items.json
        ├── prompts.json
        ├── plan.md
        ├── copy.md
        ├── assets/
        ├── slides/
        ├── reels/
        └── qa-report.md
```

---

## 🔐 Write 권한 관리

**오케스트레이터만**:
- research.md 저장 (researcher → 오케스트레이터)
- items.json 저장 (item-researcher → 오케스트레이터)

**에이전트별**:
- prompt-engineer: prompts.json (Write)
- contents-marketer: plan.md, copy.md (Write)
- designer: assets/ (Write)
- video-agent: reels/ (Write)
- developer: slides/ (Write, Edit)
- qa-reviewer: qa-report.md (Write) - **산출물 수정 금지**
- scheduler: schedule.json, performance_log.json (Write)

---

## 🧪 자기 성장 시스템

**실패 학습 루프**:
1. 에이전트 작업 중 실패 발견
2. 오케스트레이터가 실패 원인 분석
3. 해당 SKILL.md에 규칙 추가
4. 다음 실행부터 같은 실수 방지

**예시**:
- designer가 캐릭터 불일치 이미지 생성 → design-visual.SKILL.md에 체크리스트 추가
- developer가 overflow 발생 → html-slide.SKILL.md에 max-width 규칙 추가

---

## 📊 성과 피드백 루프 (주 1회)

```
scheduler: 성과 수집 (performance_log.json)
    ↓
오케스트레이터: 상위 20% 콘텐츠 패턴 분석
    ↓
researcher: 다음 주 기획에 반영
    ↓
contents-marketer: 성공 패턴 우선 적용
```

---

## ⚠️ 에러 핸들링

### 에이전트 실패 시
1. 재시도 (최대 2회)
2. 오케스트레이터 개입 (원인 분석)
3. SKILL.md 규칙 업데이트
4. 사용자 에스컬레이션 (심각한 경우)

### QA 루프 무한 방지
- 최대 3회 수정 루프
- 3회 실패 시 → 마보스님 수동 확인 요청

---

## 🎯 우선순위 원칙

**절대 우선순위**:
1. **Gena 캐릭터 일관성** (최우선)
2. 아이템 시각 정확성
3. 팩트 정확성 (가격, 브랜드)
4. 레이아웃 품질

**타협 가능**:
- 미세한 색감 차이
- 텍스트 여백 조정
- 배경 디테일

---

**최종 업데이트**: 2026-03-06 03:37  
**프로젝트**: @gena_feed Instagram 자동화  
**담당**: 자비스 (OpenClaw orchestrator)
