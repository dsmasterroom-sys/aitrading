# @gena_feed 인스타그램 콘텐츠 자동화 프로젝트

**OpenClaw 기반 완전 자동화 파이프라인**

---

## 🎯 프로젝트 개요

- **목표**: 주간 릴스 5개 + 캐러셀 1개 + 스토리 5회 자동 생성
- **핵심 기술**: Nanogen API, OpenClaw 서브에이전트, Gena 캐릭터 일관성
- **자동화율 목표**: 90%+ (기획 → 생성 → QA → 발행)

---

## 📂 프로젝트 구조

```
instagram-automation/
├── README.md                          # 이 파일
├── MODEL_STRATEGY.md                  # 모델 할당 전략
├── gena_claudecode_design_v2.docx     # 원본 기획서
│
├── agents/                            # 9개 에이전트 (추후 생성)
│   ├── orchestrator.md                # claude-opus-4-6
│   ├── prompt-engineer.md             # claude-opus-4-6
│   ├── researcher.md                  # claude-sonnet-4-6
│   ├── item-researcher.md             # claude-sonnet-4-6
│   ├── contents-marketer.md           # openai/gpt-5.2
│   ├── designer.md                    # openai/gpt-5-mini
│   ├── video-agent.md                 # claude-sonnet-4-6
│   ├── developer.md                   # claude-sonnet-4-6
│   ├── qa-reviewer.md                 # openai/gpt-5-mini
│   └── scheduler.md                   # openai/gpt-5-mini
│
├── skills/                            # 15개 스킬 파일 (추후 생성)
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
├── shared/                            # 공유 리소스
│   ├── design-system/
│   │   ├── design-tokens.css          # 색상/폰트/간격 CSS 변수
│   │   ├── patterns/                  # 29개 레이아웃 패턴 (추후)
│   │   └── validate_slide.py          # 자동 QA 스크립트
│   └── gena-master-prompt.md          # Gena 캐릭터 절대 기준 (8개 참조 이미지)
│
├── workflows/                         # 콘텐츠 유형별 워크플로우
│   ├── reels-workflow.md
│   ├── carousel-workflow.md
│   └── story-workflow.md
│
└── content/                           # 실제 콘텐츠 작업 폴더
    └── {YYYYMMDD}_{series_name}/
        ├── research.md
        ├── items.json
        ├── prompts.json
        ├── plan.md
        ├── copy.md
        ├── assets/
        ├── slides/
        ├── reels/
        ├── stories/
        └── qa-report.md
```

---

## 🚀 30일 구축 로드맵

### Week 1: 기반 인프라 ✅ **현재**
- [x] 프로젝트 폴더 생성
- [x] 모델 전략 문서화
- [ ] Gena 참조 이미지 8장 준비
- [ ] Nanogen API 연결 테스트
- [ ] gena-master-prompt.md 작성

### Week 2: 캐러셀 파이프라인
- [ ] researcher + item-researcher 에이전트 작성
- [ ] prompt-engineer 작성 (10개 체크리스트)
- [ ] designer + developer 작성
- [ ] 첫 캐러셀 완성 (수동 발행)

### Week 3: 릴스 파이프라인
- [ ] video-agent 작성
- [ ] ffmpeg 자동화
- [ ] 첫 릴스 완성

### Week 4: 스케줄러 + 통합
- [ ] scheduler 에이전트 (Meta API 연동)
- [ ] cron 자동화
- [ ] 전체 파이프라인 통합 테스트

---

## 🔧 기술 스택

| 영역 | 기술 |
|---|---|
| **오케스트레이션** | OpenClaw sessions_spawn |
| **이미지 생성** | Nanogen 나노바나나2/Pro, Outfit Swap |
| **영상 생성** | Nanogen Kling v3.0, Veo |
| **웹 크롤링** | browser tool (무신사/지그재그) |
| **HTML → PNG** | Puppeteer (developer 에이전트) |
| **영상 편집** | ffmpeg |
| **발행** | Instagram Graph API |
| **스케줄링** | OpenClaw cron |

---

## 📊 시스템 핵심 3대 원칙

### 1️⃣ Gena 캐릭터 일관성 = 최우선
- 8개 헤어스타일 참조 이미지
- Nanogen 참조 이미지 → 인물 그대로 유지
- 2단계 파이프라인 (기본 포즈 → Outfit Swap)

### 2️⃣ 실제 아이템 매칭
- items.json 구조화
- 제품 이미지 URL → Nanogen Outfit Swap 직접 투입
- QA에서 아이템 시각 일치 검증

### 3️⃣ 에이전트 단일 책임
- 한 에이전트 = 한 가지 역할
- Write 권한 최소화
- QA는 검수만 (수정 금지)

---

## 💰 예상 비용 (월간)

- API 호출: 약 1,000~1,200회
- Nanogen 이미지: 주 25~30장 → 월 100~120장
- Nanogen 영상: 주 5개 → 월 20개
- Instagram API: 무료 (비즈니스 계정)

**총 예상**: 측정 중 (Week 2 이후 업데이트)

---

## 📝 현재 상태

**Phase**: Week 1 완료 / Week 2 시작  
**최종 업데이트**: 2026-03-06 05:07  
**진행률**: Week 1 (100%) / 전체 (15%)

### ✅ Session 1-2 완료 (프로젝트 기반)
- [x] 프로젝트 폴더 정리
- [x] 9개 에이전트 파일
- [x] 15개 스킬 파일
- [x] Gena Master Prompt (248줄)
- [x] validate_slide.py (자동 QA)

### ✅ Session 3 완료 (Nanogen 연동)
- [x] nanogen_image.py (이미지 자동 생성)
- [x] nanogen_video.py (영상 자동 생성)
- [x] 3개 Workflow 파일 (carousel, reels, story)
- [x] 3개 HTML 패턴 (hero, split, product)

### ✅ Session 4-5 완료 (첫 캐러셀 테스트)
- [x] 첫 이미지 생성 성공 (Nanogen Outfit Swap)
- [x] 3개 슬라이드 자동 생성
- [x] HTML → PNG 렌더링 (Puppeteer)
- [x] 다양한 레이아웃 패턴 적용
- [x] **End-to-End 파이프라인 검증 완료!** 🎉

### ✅ Session 6 완료 (QA + 패턴 확장)
- [x] QA 자동화 테스트 (3개 슬라이드 통과)
- [x] 3개 HTML 패턴 추가 (quote, grid-4, cta)
- [x] 문서 정리

### 📊 생성된 콘텐츠
- **이미지**: 3장 (각 25초 소요)
- **HTML 패턴**: 6개 (hero, split, product, quote, grid-4, cta)
- **최종 슬라이드**: 3장 (2160×2880px Retina)
- **QA 리포트**: 1건 (전체 통과)

### ✅ Session 7 완료 (2026-03-06, 8시간 스프린트)

**Phase 1: Meta API 연동** ✅ (24분)
- instagram_api.py (캐러셀/릴스 발행, 성과 조회)
- imgur_uploader.py (이미지 호스팅)
- scheduler.md (발행 에이전트)
- meta-api-setup.md (설정 가이드)

**Phase 2: 릴스 파이프라인** ✅ (15분)
- ffmpeg_assemble_reels.py (자막 + 씬 결합)
- video-agent.md (비디오 생성 에이전트)

**Phase 3: 스케줄러 자동화** ✅ (10분)
- setup_cron_jobs.py (주간 자동 생성 일정)

**Phase 4: 문서화** ✅ (10분)
- INTEGRATION_GUIDE.md (통합 설정 가이드)
- TROUBLESHOOTING.md (문제 해결 가이드)
- requirements.txt (Python 의존성)

**Phase 5: Story + HTML 패턴** ✅ (19분)
- orchestrate-story.SKILL.md (스토리 워크플로우)
- HTML 패턴 12개 (네오브루탈리즘 디자인)

### 📋 다음 단계 (Session 8)
- [ ] Meta API 토큰 발급 (마보스님)
- [ ] Imgur Client ID 발급 (마보스님)
- [ ] 첫 캐러셀 E2E 자동 생성 테스트
- [ ] 1주일 프로덕션 운영 테스트
- [ ] 성과 데이터 수집 및 개선

**담당**: 자비스 (OpenClaw orchestrator)

---

**프로젝트 시작일**: 2026-03-06  
**목표 완료일**: 2026-04-06 (30일)  
**Week 1 완료**: 2026-03-06 ✅  
**Session 7 완료**: 2026-03-06 ✅ (8시간, 5 Phases)  
**전체 진행률**: 약 50% ⚡ (기반 인프라 완성, 실전 테스트만 남음)
