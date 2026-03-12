# Carousel Workflow

**용도**: 캐러셀 콘텐츠 제작 전체 흐름  
**목표**: 트렌드 주제 → 10슬라이드 캐러셀 완성 → QA → 발행  
**자동화율**: 90%+

---

## 📊 전체 프로세스

```
1. 트렌드 리서치 (researcher)
   ↓
2. 아이템 리서치 (item-researcher) [병렬]
   ↓
[게이트 G1: 토픽 확정]
   ↓
3. 프롬프트 생성 (prompt-engineer)
   ↓
[게이트 G2: 프롬프트 검증]
   ↓
4. 콘텐츠 기획 (contents-marketer) [병렬]
5. 이미지 생성 (designer) [병렬]
   ↓
6. HTML 슬라이드 생성 (developer)
   ↓
7. QA 검수 (qa-reviewer)
   ↓
[게이트 G3: QA 통과]
   ↓
8. 스케줄링 (scheduler)
   ↓
[게이트 G4: 발행 승인]
   ↓
9. 발행 (Meta API)
```

---

## 🚀 Phase별 상세 실행

### Phase 1: 트렌드 리서치 (30분)

**담당**: researcher (sonnet-4-6)  
**스킬**: research-trend.SKILL.md, research-hashtag.SKILL.md

**입력**:
- 사용자 요청 (예: "봄 패션 트렌드")

**실행**:
```python
# Orchestrator → researcher 스폰
sessions_spawn(
    agentId="researcher",
    task="봄 패션 트렌드 조사 (인스타그램 중심, 2026년 3월)",
    model="claude-sonnet-4-6"
)
```

**출력**:
- `research.md` (6개 추천 토픽, 각 토픽당 해시태그 20개)

**게이트 G1: 토픽 확정**
- Orchestrator → 마보스님께 6개 토픽 제시
- 선택된 토픽으로 다음 단계 진행

---

### Phase 2: 아이템 리서치 (30분)

**담당**: item-researcher (sonnet-4-6)  
**스킬**: item-research.SKILL.md, item-visual-desc.SKILL.md

**입력**:
- 선택된 토픽 (예: "오버사이즈 니트 코디")

**실행**:
```python
# Orchestrator → item-researcher 스폰
sessions_spawn(
    agentId="item-researcher",
    task="오버사이즈 니트 코디 아이템 10개 수집 (무신사/지그재그)",
    model="claude-sonnet-4-6"
)
```

**출력**:
- `items.json` (10개 아이템, 각 아이템당 ref_image_url, visual_desc, price, brand)

---

### Phase 3: 프롬프트 생성 (20분)

**담당**: prompt-engineer (opus-4-6)  
**스킬**: prompt-image.SKILL.md

**입력**:
- `research.md` (토픽 정보)
- `items.json` (아이템 정보)
- `shared/gena-master-prompt.md` (Gena 캐릭터 기준)

**실행**:
```python
# Orchestrator → prompt-engineer 스폰
sessions_spawn(
    agentId="prompt-engineer",
    task="캐러셀 10슬라이드 프롬프트 생성 (Gena 착장)",
    model="claude-opus-4-6"
)
```

**출력**:
- `prompts.json` (10개 슬라이드 프롬프트, 각 슬라이드당 image_prompt, reference_images)

**게이트 G2: 프롬프트 검증**
- 자동 검증: prompt-quality-check.SKILL.md
- 10개 체크리스트 통과 여부
- 실패 시 prompt-engineer 재생성

---

### Phase 4: 콘텐츠 기획 (20분)

**담당**: contents-marketer (gpt-5.2)  
**스킬**: plan-content.SKILL.md, write-copy.SKILL.md

**입력**:
- `prompts.json`
- `items.json`

**실행**:
```python
# Orchestrator → contents-marketer 스폰
sessions_spawn(
    agentId="contents-marketer",
    task="캐러셀 기획 및 카피 작성 (슬라이드별 문구)",
    model="openai/gpt-5.2"
)
```

**출력**:
- `plan.md` (전체 기획 의도, 타겟 오디언스, 시리즈명)
- `copy.md` (슬라이드별 제목, 본문, CTA)

---

### Phase 5: 이미지 생성 (60분)

**담당**: designer (gpt-5-mini)  
**스킬**: design-visual.SKILL.md

**입력**:
- `prompts.json`
- `items.json`
- `shared/gena-master-prompt.md`
- `shared/gena-references/*.png`

**실행**:
```python
# Orchestrator → designer 스폰
sessions_spawn(
    agentId="designer",
    task="캐러셀 10슬라이드 이미지 생성 (Nanogen Outfit Swap)",
    model="openai/gpt-5-mini"
)
```

**내부 실행**:
```bash
# designer 에이전트 내부에서 실행
python scripts/nanogen_image.py \
    --content-path content/20260306_spring_outfits \
    --all \
    --aspect-ratio 3:4 \
    --resolution 2K
```

**출력**:
- `assets/carousel_slide_01.png` ~ `carousel_slide_10.png` (1080×1440px)

**자기검증**:
- design-visual.SKILL.md의 10개 체크리스트
- 캐릭터 일관성 (최우선)
- 아이템 정확성
- 재생성 규칙 적용

---

### Phase 6: HTML 슬라이드 생성 (30분)

**담당**: developer (sonnet-4-6)  
**스킬**: html-slide.SKILL.md

**입력**:
- `assets/*.png` (이미지)
- `copy.md` (문구)
- `shared/design-system/design-tokens.css`
- `shared/design-system/patterns/*.html` (29개 레이아웃 패턴)

**실행**:
```python
# Orchestrator → developer 스폰
sessions_spawn(
    agentId="developer",
    task="캐러셀 HTML 슬라이드 생성 (디자인 시스템 기반)",
    model="claude-sonnet-4-6"
)
```

**출력**:
- `slides/slide_01.html` ~ `slide_10.html`
- `slides/slide_01.png` ~ `slide_10.png` (Puppeteer 렌더링)

**기술 요구사항**:
- CSS Grid 레이아웃
- 반응형 (1080×1440px 기준)
- 오버플로우 방지
- 디자인 토큰 준수

---

### Phase 7: QA 검수 (15분)

**담당**: qa-reviewer (gpt-5-mini)  
**스킬**: qa-visual.SKILL.md, qa-factcheck.SKILL.md

**입력**:
- `slides/*.png` (최종 슬라이드)
- `items.json` (팩트 체크용)
- `shared/design-system/validate_slide.py`

**실행**:
```python
# Orchestrator → qa-reviewer 스폰
sessions_spawn(
    agentId="qa-reviewer",
    task="캐러셀 QA 검수 (시각/팩트/레이아웃)",
    model="openai/gpt-5-mini"
)
```

**내부 실행**:
```bash
# qa-reviewer 에이전트 내부에서 실행
python shared/design-system/validate_slide.py \
    --slides-dir content/20260306_spring_outfits/slides \
    --output-report qa-report.md
```

**출력**:
- `qa-report.md` (이슈 리스트: 고/중/저)

**게이트 G3: QA 통과**
- 고/중 이슈 0건 → 통과
- 고/중 이슈 발견 → developer 수정 루프 (최대 3회)
- 3회 실패 → Orchestrator 개입

---

### Phase 8: 스케줄링 (10분)

**담당**: scheduler (gpt-5-mini)  
**스킬**: schedule-post.SKILL.md

**입력**:
- `slides/*.png` (최종 슬라이드)
- `copy.md` (캡션)
- `research.md` (해시태그)

**실행**:
```python
# Orchestrator → scheduler 스폰
sessions_spawn(
    agentId="scheduler",
    task="캐러셀 발행 준비 (Meta API 업로드)",
    model="openai/gpt-5-mini"
)
```

**출력**:
- `schedule.json` (발행 예약 정보)

**게이트 G4: 발행 승인**
- Orchestrator → 마보스님께 최종 슬라이드 제시
- 승인 → 발행 실행
- 수정 요청 → 해당 Phase로 복귀

---

### Phase 9: 발행 (5분)

**담당**: scheduler (자동)

**실행**:
```python
# Meta Graph API 호출
POST /me/media
{
    "image_url": "...",
    "caption": "...",
    "children": [...]  # 캐러셀 슬라이드
}
```

**출력**:
- Instagram 발행 완료
- `performance_log.json` 업데이트 (발행 시간, 예상 노출수)

---

## ⏱️ 전체 소요 시간

| Phase | 소요 시간 |
|---|---|
| 트렌드 리서치 | 30분 |
| 아이템 리서치 | 30분 |
| 프롬프트 생성 | 20분 |
| 콘텐츠 기획 | 20분 |
| 이미지 생성 | 60분 |
| HTML 슬라이드 | 30분 |
| QA 검수 | 15분 |
| 스케줄링 | 10분 |
| 발행 | 5분 |
| **총 소요 시간** | **약 3.5시간** |

*(병렬 실행으로 약 2.5시간으로 단축 가능)*

---

## 🔧 병렬 실행 최적화

### 1차 병렬 (Phase 1-2)
```python
# researcher + item-researcher 동시 실행
researcher_session = sessions_spawn(agentId="researcher", ...)
item_researcher_session = sessions_spawn(agentId="item-researcher", ...)

# 두 세션 완료 대기
wait_for_completion([researcher_session, item_researcher_session])
```

### 2차 병렬 (Phase 4-5)
```python
# contents-marketer + designer 동시 실행
marketer_session = sessions_spawn(agentId="contents-marketer", ...)
designer_session = sessions_spawn(agentId="designer", ...)

wait_for_completion([marketer_session, designer_session])
```

---

## 📂 최종 산출물 구조

```
content/20260306_spring_outfits/
├── research.md               # researcher 산출물
├── items.json                # item-researcher 산출물
├── prompts.json              # prompt-engineer 산출물
├── plan.md                   # contents-marketer 산출물
├── copy.md                   # contents-marketer 산출물
├── assets/
│   ├── carousel_slide_01.png
│   └── ... (10개)
├── slides/
│   ├── slide_01.html
│   ├── slide_01.png
│   └── ... (10개)
├── qa-report.md              # qa-reviewer 산출물
├── schedule.json             # scheduler 산출물
└── performance_log.json      # 발행 후 성과 기록
```

---

## 🚨 실패 복구 시나리오

### 이미지 생성 실패
- designer 재실행 (최대 3회)
- 3회 실패 → 다른 Gena 참조 이미지 시도
- 여전히 실패 → Orchestrator 개입

### QA 루프 무한 방지
- developer 수정 최대 3회
- 3회 실패 → Orchestrator → 마보스님 수동 확인

### Meta API 오류
- 재시도 (최대 2회)
- 실패 시 로컬 저장 → 수동 발행

---

**최종 업데이트**: 2026-03-06 04:15  
**프로젝트**: @gena_feed Instagram 자동화  
**담당**: 자비스 (OpenClaw orchestrator)
