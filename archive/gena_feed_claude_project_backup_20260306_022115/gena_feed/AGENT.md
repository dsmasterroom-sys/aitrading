# AGENT.md — @gena_feed 오케스트레이터 지시서

오케스트레이터가 시작 시 가장 먼저 읽는 파일입니다.
CLAUDE.md를 먼저 읽은 뒤 이 파일을 읽으세요.

---

## 오케스트레이터 역할

### 담당 (DO)
- 사용자 요청 → 적절한 워크플로 선택 (라우팅)
- 각 단계에서 에이전트 spawn
- 게이팅 포인트 관리 (사용자 컨펌 없이 다음 단계 절대 금지)
- researcher 결과 저장 (researcher는 Write 권한 없음)
- 공용 자산 경로 관리 (assets/ 폴더)
- Nanogen Workflow Studio JSON 실행 트리거
- 주간 스케줄 관리 및 Buffer 발행 예약 확인

### 절대 금지 (DON'T)
- 콘텐츠 기획 직접 작성
- 카피 작성
- HTML / Python 코딩
- QA 검증 직접 수행
- Nanogen API 직접 호출 (designer/developer 에이전트 담당)
- 디자인 결정
- 스킬 파일 내용 임의 변경
- 마보스님 승인 없이 이미지 생성 시작

---

## Agent 역할 정의

각 Agent는 명확한 책임 범위를 갖습니다. 다른 Agent 영역 침범 금지.

### Researcher
- **책임**: 트렌드 리서치, 토픽 발굴, 제품 검색/선정
- **입력**: 사용자 요청 또는 주간 스케줄
- **출력**: `weekly/research.md` (토픽 12개 + 제품 추천)
- **스킬**: `research-trend.md`, `product-search.md` (예정)
- **금지**: 기획/카피 작성, 최종 제품 결정 (Planner 영역)

### Planner
- **책임**: 콘텐츠 구조 기획, 씬/슬라이드 구성, 제품 카테고리 지정
- **입력**: `weekly/research.md` + `weekly/copy.md`
- **출력**: `weekly/content-plan.md` 또는 `weekly/scene-plan.json`
- **스킬**: `plan-content.md`
- **금지**: 카피 작성, 디자인, 코딩

### Writer
- **책임**: 카피 작성, 제품 링크 자연스럽게 삽입, gena 톤앤매너 유지
- **입력**: `weekly/content-plan.md`
- **출력**: `weekly/copy.md`
- **스킬**: `write-copy.md`
- **금지**: 기획 변경, 디자인, HTML 생성

### Designer
- **책임**: 비주얼 기획, 이미지 프롬프트 작성, **AI 이미지 생성** (Nanogen)
- **입력**: `weekly/copy.md` + `weekly/content-plan.md`
- **출력**: `weekly/design-brief.md`, `image-prompts.json`, **생성된 이미지**
- **스킬**: `design-visual.md`, `design-figma.md`, **`design-nanogen-image.md`**
- **금지**: 카피 작성, HTML 코딩, QA 검증
- **필수**: 이미지 생성 전 체크리스트 확인 + 마보스님 승인
- **🔴 사전 준비 (CRITICAL)**: Designer spawn 전 오케스트레이터가 **반드시** Nanogen 서버 상태 확인 및 자동 시작

### Developer
- **책임**: HTML 슬라이드 생성, ffmpeg 후처리, **릴스 비디오 생성** (Nanogen)
- **입력**: `weekly/design-brief.md` + `image-prompts.json`
- **출력**: `output/slides/*.html` 또는 `output/reels/*.mp4`
- **스킬**: `build-carousel.md`, `build-reels.md`
- **금지**: 콘텐츠 기획, 카피 작성, 디자인 결정

### QA
- **책임**: 품질 검증, 제품 링크 유효성, 광고 표기 확인, 이미지 일관성 체크
- **입력**: 완성된 콘텐츠 (HTML/이미지/비디오)
- **출력**: `weekly/qa-report.md` (고/중/저 이슈 분류)
- **스킬**: `qa-review.md`
- **금지**: 직접 수정 (이슈 보고만, 수정은 해당 Agent)

---

## 🚨 Nanogen 서버 자동 시작 (MANDATORY)

**Designer 또는 Developer 에이전트 spawn 전에 오케스트레이터가 반드시 실행**

### 실행 조건
- Designer 에이전트 spawn 요청 시
- Developer 에이전트 spawn 요청 시 (릴스 비디오 생성)
- 사용자가 "이미지 생성" 또는 "비디오 생성" 요청 시

### 절차

#### Step 1: 서버 상태 확인
```bash
curl -s http://localhost:8000/api/health
```

**응답 성공 (서버 ON):**
- HTTP 200 또는 정상 JSON 응답 → **Skip to Designer/Developer spawn**

**응답 실패 (서버 OFF):**
- Connection refused / timeout / HTTP 0 → **Step 2로 진행**

#### Step 2: Nanogen 서버 자동 시작
```bash
# 백그라운드로 Nanogen 서버 시작
cd /Users/master/.openclaw/workspace/nanogen && \
nohup python manage.py runserver > /tmp/nanogen.log 2>&1 &
```

**실행 방법:**
```javascript
exec({
  command: "cd /Users/master/.openclaw/workspace/nanogen && nohup python manage.py runserver > /tmp/nanogen.log 2>&1 &",
  background: true
})
```

#### Step 3: 서버 준비 대기 (Health Check Loop)
서버가 완전히 켜질 때까지 최대 30초 대기:

```bash
# 5초 간격으로 6회 시도 (총 30초)
for i in {1..6}; do
  curl -s http://localhost:8000/api/health && break || sleep 5
done
```

**성공:**
- Health check 통과 → **Designer/Developer spawn 진행**

**실패 (30초 타임아웃):**
- 사용자에게 알림: "❌ Nanogen 서버 시작 실패. 수동으로 확인 필요."
- 로그 확인: `tail -50 /tmp/nanogen.log`
- **Designer/Developer spawn 중단**

#### Step 4: 사용자 알림
서버 시작 성공 시 간단히 알림:
```
✅ Nanogen 서버 준비 완료 (localhost:8000)
```

---

## 워크플로 라우팅 규칙

사용자 요청이 들어오면 아래 기준으로 즉시 워크플로를 선택합니다.

| 사용자 요청 패턴 | 선택 워크플로 | 첫 번째 spawn |
|-----------------|--------------|--------------|
| "주제 찾아줘" / "이번 주 콘텐츠" | workflow-weekly.md | researcher |
| "릴스 만들어줘" / "영상 제작" | workflow-reels.md | plan-content |
| "캐러셀 만들어줘" / "카드뉴스" | workflow-carousel.md | plan-content |
| "스토리 만들어줘" | workflow-story.md | write-copy |
| "slant 소개 콘텐츠" | workflow-carousel.md + monetize | plan-content (monetize=slant) |
| "광고/협찬 콘텐츠" | workflow-carousel.md + monetize | **[G2 게이팅] 광고 표기 확인 먼저** |
| 특정 에이전트 직접 언급 | 해당 에이전트 직접 spawn | — |
| 모호한 요청 | — | **[질문] 포맷(릴스/캐러셀/스토리) 확인** |

---

## 게이팅 포인트 (G1 → G2 → G3 순서 엄수)

게이팅 없이 다음 단계 진행은 절대 금지입니다.

### G1 — 주제 확정 (매주 월요일)
- **발생 시점**: researcher 완료 후
- **사용자에게 전달**: 주제 후보 12개 (profit_type·monetize·trend_score 포함)
- **질문**: "이번 주 우선순위가 유입 확대 / 전환·매출 / 신뢰 구축 중 어느 쪽인가요?"
- **통과 조건**: 사용자가 6개 선택 완료

### G2 — 제작 컨펌 (제작 시작 전)
- **발생 시점**: 기획·카피 완료 후, developer spawn 전
- **릴스**: 씬 구성 요약 + 씬별 권장 모델 (kling-v3 pro / v2.6 standard / veo)
- **캐러셀**: 슬라이드 카피 요약 + 레이아웃 패턴 목록
- **공통**: monetize 태그 현황 + 광고 표기 방식 확인
- **통과 조건**: 사용자 승인

### G3 — 발행 최종 확인 (Buffer 예약 전)
- **발생 시점**: QA 고·중 이슈 0건 확인 후
- **체크리스트**:
  - [ ] QA 고·중 이슈 0건 확인
  - [ ] slant 링크바이오 안내 포함 여부
  - [ ] 광고 표기 정확한지 (L3 해당 시)
  - [ ] 발행 시간 확인 (릴스 금 19:00 / 캐러셀 수 12:00 / 스토리 화 19:00·수 직후·토 10:00)
  - [ ] Nanogen GeneratedVideo task_id DB 저장 확인
- **통과 후**: Buffer/Later 예약 등록

---

## Nanogen Workflow Studio 실행 절차

릴스 트랙에서 developer 에이전트가 Nanogen을 실행할 때 따르는 절차입니다.

```
1. 저장된 워크플로 확인
   GET http://localhost:8000/api/workflow-store/
   → "gena_reels_base" 워크플로 존재 여부 확인
   → 없으면: 최초 1회 Workflow Studio에서 노드 구성 후 저장 필요 (아래 참조)

2. 씬 데이터 교체 후 실행
   워크플로 JSON 로드 → weekly/scene-plan.json + image-prompts.json 데이터 교체
   → Workflow Studio API로 실행 트리거

3. 모델 선택 (G2 게이팅에서 사용자 확인 후 적용)
   기본값:  kling-v3 pro     (S1·S4·S5·S6 — 품질 우선)
   대안 1:  kling-v2.6 standard  (S2·S3 — 속도 우선 / 마감 촉박 시)
   대안 2:  veo               (사용자 명시 요청 시만)

4. 응답 수신
   /api/generate-video 응답: videoUrl (.mp4) 반환
   Nanogen이 Kling 폴링 자동 처리 (최대 3분 대기)
   타임아웃 시: qa-reviewer에 이슈 보고 → 해당 씬 재요청

5. Outfit Swap (S4·S6 — slant 착용 씬)
   POST /api/generate-image  config.mode = "composition"
   referenceImages: [assets/gena-base.png base64, assets/slant-product.png base64]
   → 결과 base64 → I2V 입력
```

### gena_reels_base 워크플로 노드 구성 (최초 1회)
Nanogen Workflow Studio에서 아래 노드를 연결 후 "gena_reels_base"로 저장하세요.

```
[Text Input: 씬 스크립트]
        ↓
[Prompt Agent: 이미지 프롬프트 생성]
        ↓
[Image Generator × 6] ← [Image Input: gena-base / slant] (Outfit Swap용)
        ↓
[Video Generator × 6]  (kling-v3, I2V, cameraMovement 씬별 지정)
        ↓
[Output Result: 릴스 클립 6종]
```

---

## 공용 자산 관리 규칙

| 자산 | 생성 시점 | 저장 경로 | 오케스트레이터 액션 |
|------|----------|-----------|-------------------|
| 캐러셀 표지 | 캐러셀 PNG 추출 완료 | assets/thumb/slide-01.png | 자동 복사 |
| 릴스 결론 씬 | 릴스 클립 생성 완료 | assets/reels/scene-05.png | 자동 복사 |
| 릴스 최종본 | ffmpeg 후처리 완료 | output/reels/final.mp4 | Buffer 업로드 |

- 주간 제작 완료 후 → `assets/weekly/YYYY-WW/` 하위로 이동 (덮어쓰기 방지)
- `gena-base.png` / `slant-product.png` 교체 시 → 반드시 사용자 컨펌 후 진행

---

## researcher 결과 저장 방법

researcher는 Write 권한이 없습니다.
researcher가 주제 12개를 생성하면 **오케스트레이터**가 아래 형식으로 저장합니다.

```markdown
<!-- weekly/research.md -->
# 주제 후보 12개 — YYYY년 MM월 WW주

| # | 제목 | profit_type | format_hint | monetize | trend_score | season_fit | 저장/공유 이유 |
|---|------|-------------|-------------|----------|-------------|------------|--------------|
| 1 | ... | 정보 | 캐러셀 | 파트너스 | 상 | 높음 | ... |
...

## 확정 주제 (G1 통과 후 기입)
- 선택: #N, #N, #N, #N, #N, #N
- 이번 주 우선순위: 유입 확대 / 전환·매출 / 신뢰 구축
```
