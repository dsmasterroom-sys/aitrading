# @gena_feed 프로젝트 현재 상태 (2026-03-01 20:46)

## 🎯 진행 방향 결정: 혼합 접근 - 단계별 점진적 완성

### Phase 현황
- ✅ **Phase 0**: 이미지 생성 고도화 완료 (제품 분석, Outfit Grid Reference)
- 🔄 **Phase 1 진행 중**: 전략 수립 → 핵심 자동화 → 테스트

---

## 📋 다음 작업 순서 (우선순위)

### Step 1: 전략 문서 작성 (2-3시간)
**파일:** `gena_feed/strategy/growth-strategy.md`
**담당:** Researcher 에이전트 spawn
**내용:**
- 인기 계정 벤치마크 (패션/AI 콘텐츠)
- 성장 전략 핵심 4요소
  1. 콘텐츠 트리거 (Hook 최적화)
  2. 인게이지먼트 유도 (저장/댓글/공유)
  3. 알고리즘 최적화 (발행시간/해시태그/포맷비율)
  4. 수익화 동선 (링크바이오 전환율)
- 6개월 로드맵

### Step 2: 발행 자동화 (4-5시간)
**파일:** `gena_feed/scripts/publish_to_buffer.py`
**담당:** Developer 에이전트 spawn
**기능:**
- Buffer/Later API 연동
- G3 게이팅 통과 후 자동 예약
- 발행 시간: 릴스(금 19:00), 캐러셀(수 12:00), 스토리(화/수/토)
- 환경변수: `BUFFER_API_KEY` (`.env`)

### Step 3: 스케줄러 설정 (2-3시간)
**파일:** OpenClaw cron job
**담당:** 자비스 (오케스트레이터)
**스케줄:**
- 매주 월요일 09:00 → Researcher 에이전트 자동 spawn
- 수요일 11:30 → 캐러셀 발행 전 최종 확인
- 금요일 18:30 → 릴스 발행 전 최종 확인

### Step 4: 1주 테스트 운영 (7일)
- 2026년 W10 (3/3~3/9) 실전 테스트
- 이슈 트래킹 & 개선
- 필요시 나머지 개선 (릴스 편집, QA 자동화, Figma)

---

## 🔧 Phase 0: 이미지 생성 고도화 (완료)

### 완성된 기능
1. **제품 분석 시스템**
   - `scripts/analyze_product.py` - Gemini Vision API로 제품 스펙 자동 추출
   - `assets/output/product_analysis.json` - slant 제품 상세 스펙 저장

2. **Outfit Grid Reference 시스템**
   - `assets/outfit/` - 사용자 큐레이션 outfit 이미지 폴더
   - 날짜순 자동 로드 (최신 3개 기본)
   - 착장 일관성 & 브랜드 톤 유지

3. **개선된 프롬프트**
   - `weekly/image-prompts.json` - Reference Object Strict Preservation 방식
   - 제품 디테일 강제 복제 (나일론 재질, 사이드 스트랩, 매트 블랙)

4. **이미지 생성 워크플로우**
   ```
   STEP 1: Product Analysis (자동)
   STEP 1.5: Outfit References (자동)
   STEP 2: Image Generation
   ```

### 핵심 파일
- `scripts/generate_images_nanogen.py` - 이미지 생성 실행
- `assets/output/product_analysis.json` - 제품 스펙
- `weekly/image-prompts.json` - 프롬프트 설정
- `assets/outfit/` - outfit 참조 이미지

---

## 🎨 Phase 2: Figma 템플릿 시스템 (2026-03-03 완료)

### 구현된 모듈
1. **핵심 라이브러리** (`gena_feed/`)
   - `figma_client.py` - Figma REST API 클라이언트
   - `figma_updater.py` - 템플릿 업데이트 페이로드 생성 + Plugin bridge
   - `figma_exporter.py` - PNG Export/다운로드/최적화
   - `models.py` - 데이터 모델 (SlideData, NodeMapping, TemplatePattern)
   - `fallback_handler.py` - Figma 실패 시 HTML fallback 실행
   - `content_parser.py` - 콘텐츠 파싱 유틸리티
   - `__init__.py` - 패키지 초기화

2. **CLI 도구** (`scripts/`)
   - `figma_export.py` - 통합 CLI (개선됨)
     - `--all` / `--slide N,N,N` - 슬라이드 선택
     - `--update --data <file>` - 템플릿 업데이트 (Figma Plugin 연동)
     - `--optimize` - PNG 최적화 (Pillow)
     - `--fallback` - Figma 실패 시 HTML 방식 자동 전환
     - `--dry-run` - 검증 모드
     - `--test` - API 연결 테스트
   - `figma_node_mapper.py` - 노드 매핑 JSON 생성

3. **문서 및 설정**
   - `.env.example` - 환경변수 템플릿
   - `README.md` - 사용법 가이드
   - `docs/figma-template-guide.md` - 템플릿 설계 문서
   - `docs/figma-api-design.md` - API 연동 설계
   - `docs/figma-workflow.md` - 워크플로우 통합 방안
   - `scripts/backup/` - 기존 스크립트 백업

### 사용법
```bash
# API 연결 테스트
python scripts/figma_export.py --test

# 전체 슬라이드 Export
python scripts/figma_export.py --all

# 특정 슬라이드만 Export
python scripts/figma_export.py --slide 1,3,7

# 템플릿 업데이트 + Export
python scripts/figma_export.py --all --update --data weekly/copy.md

# 최적화 + Fallback
python scripts/figma_export.py --all --optimize --fallback
```

### 다음 작업
- [ ] Figma 파일 생성 및 템플릿 17개 디자인
- [ ] Figma API 키 발급 및 `.env` 설정
- [ ] Node mapping JSON 생성 (`figma_node_mapper.py`)
- [ ] 실전 테스트 및 검증

---

## 📂 프로젝트 핵심 구조

```
gena_feed/
├── STATUS.md              ← 이 파일 (현재 상태)
├── CLAUDE.md              ← 공통 참조 (에이전트 규칙)
├── AGENT.md               ← 오케스트레이터 지시서
├── README.md              ← 프로젝트 개요 & 사용법
├── .env                   ← 환경변수
├── .env.example           ← 환경변수 템플릿
│
├── gena_feed/             ← Python 패키지
│   ├── __init__.py
│   ├── figma_client.py    ← Figma API 클라이언트
│   ├── figma_updater.py   ← 템플릿 업데이트
│   ├── figma_exporter.py  ← PNG Export
│   ├── models.py          ← 데이터 모델
│   ├── fallback_handler.py ← HTML Fallback
│   └── content_parser.py  ← 콘텐츠 파싱
│
├── docs/                  ← 설계 문서
│   ├── figma-template-guide.md
│   ├── figma-api-design.md
│   ├── figma-workflow.md
│   └── ...
│
├── strategy/
│   └── growth-strategy.md
│
├── skills/                ← 에이전트별 스킬
├── workflows/             ← 워크플로우 명세
├── scripts/               ← 실행 스크립트
│   ├── figma_export.py    ← Figma Export CLI (개선됨)
│   ├── figma_node_mapper.py ← 노드 매핑 생성
│   ├── generate_images_nanogen.py
│   ├── publish_to_buffer.py
│   ├── analyze_product.py
│   └── backup/            ← 백업
├── assets/                ← 공용 자산
├── weekly/                ← 주간 작업 파일
└── output/                ← 산출물
    └── figma-samples/     ← Figma Export 결과
```

---

## ⚠️ 알려진 이슈

### 해결됨
- ✅ 제품 디테일 오류 (재질, 스트랩 위치) → Product Analysis 추가
- ✅ 착장 컨트롤 부족 → Outfit Grid Reference 시스템

### 미해결 (Phase 2 진행 중)
- ⏸️ 릴스 편집 자동화 (`scripts/compose_reels.py` 없음)
- ⏸️ QA 자동 검증 (`scripts/run_qa.py` 없음)
- ⏸️ Figma 템플릿 실전 테스트 (API 키 설정 필요)
- ⏸️ Nanogen Workflow 실전 검증

### 최근 완료 (2026-03-03)
- ✅ Figma 템플릿 시스템 구현 (Codex)
  - API 클라이언트, 업데이터, exporter 모듈
  - Fallback 메커니즘 (Figma 실패 시 HTML 방식)
  - CLI 개선 및 문서화

---

## 🔄 세션 재시작 시 체크리스트

1. 이 파일(`STATUS.md`) 먼저 읽기
2. `CLAUDE.md` + `AGENT.md` 참조
3. 현재 Step 확인 후 이어서 진행
4. 완료 시 이 파일 업데이트

---

**마지막 업데이트:** 2026-03-03 05:31 (자비스)
**현재 진행:** Phase 2 - 콘텐츠 품질 고도화
**세션:** main

**Phase 1 완료 (반자동화 시스템):**
- ✅ Step 1: 전략 문서 작성 (`strategy/growth-strategy.md`)
- ✅ Step 2: Buffer 발행 자동화 (`scripts/publish_to_buffer.py`)
- ✅ Step 3: OpenClaw cron 스케줄러 (월/수/금 자동 실행)
- ✅ API 키 설정 완료

**Phase 2 진행 중 (콘텐츠 품질 개선):**
- ✅ 1. Figma 템플릿 시스템 구현 완료 (2026-03-03, Codex)
  - 핵심 모듈 7개 구현 (`figma_client`, `figma_updater`, `figma_exporter`, `models`, `fallback_handler`, `content_parser`, `__init__`)
  - CLI 개선 (`scripts/figma_export.py` - update/optimize/fallback 옵션 추가)
  - 문서화 완료 (`.env.example`, `README.md`)
  - 기존 스크립트 백업 (`scripts/backup/`)
- ✅ 2. Figma 템플릿 시스템 검증 완료 (2026-03-03 02:33)
  - API 연결 성공
  - 노드 매핑 생성 (`figma-node-mapping.json`)
  - PNG Export 성공 (2160x3840, @2x scale)
  - 최적화 작동 확인 (PIL, 5% 압축)
  - Dry-run 모드 검증
  - Fallback 메커니즘 완벽 작동 (Figma 실패 시 자동 HTML 전환)
- ✅ 3. Figma 디자인 스펙 문서 작성 완료 (`docs/figma-design-spec-실전.md`, 16KB)
  - HTML 샘플 9장 분석 기반
  - Design System (Color/Typography/Spacing/Effects)
  - 4개 템플릿 상세 스펙 (H-1, H-2, I-2, CTA-1)
  - Figma 제작 실전 가이드
- 📋 4. Figma 자동화 제약 확인 완료 (2026-03-03 05:00)
  - **결론:** REST API는 읽기 전용, 자동 생성 불가
  - **대안:** HTML 방식 유지 (권장) 또는 수동 작업 (2-3시간)
  - **Plugin 개발:** 자동화하려면 JavaScript/TypeScript 개발 필요 (1-2일)
- ✅ 5. HTML 템플릿 디자인 수정 가이드 제공 (2026-03-03 05:20)
  - 색상/폰트/레이아웃 수정 방법 설명
  - `shared/design-tokens.css` 활용
  - 미리보기: `python scripts/compose_carousel.py`
- 🔄 6. Nanogen Workflow 검증 진행 중 (2026-03-03 05:31)
  - Nanogen 서버 확인 (localhost:8000, Django)
  - API 엔드포인트 파악 (/api/generate, /api/workflow/store, /api/images)
  - 문서 읽기 완료 (nanogen_workflow_guide.md, image-prompts.json)
  - **다음:** API 테스트 및 워크플로우 실행
- ⏸️ 7. QA 자동화 시스템

**결정 필요:**
- Figma vs HTML 선택 (HTML 방식 권장 - 완전 자동화, 즉시 사용 가능)
