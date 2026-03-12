# 벤치마킹 자동화 워크플로

**목적:** 레퍼런스 계정 분석 → 인사이트 추출 → 다음 콘텐츠 기획 자동 반영

---

## 🎯 워크플로 개요

```
[주간 트리거] 
    ↓
Step 1: Researcher - 벤치마크 계정 분석 (5개)
    ↓
Step 2: Contents-Marketer - 인사이트 추출 & 패턴 분석
    ↓
Step 3: 자동 저장 (docs/benchmarks/)
    ↓
Step 4: 다음 시리즈 기획 시 자동 참조
    ↓
[Gate 1 통과 전 필수 체크]
```

---

## 📅 실행 주기

### 정기 실행 (Cron)
- **주간 분석:** 매주 월요일 09:00 (최신 트렌드 파악)
- **월간 딥다이브:** 매월 첫째 주 목요일 (장기 전략 수립)

### 수동 트리거
- 마보스님 요청 시
- 신규 시리즈 기획 전
- 성과 부진 시 (저장률 < 1.5%)

---

## 🔍 Step 1: Researcher - 벤치마크 계정 분석

### Input
- **분석 대상 계정 5개:**
  1. @1ldk_shop
  2. @oncuration
  3. @eun_noo
  4. @theopen_product
  5. @nobordersshop

- **분석 기간:** 최근 7일 (주간) / 30일 (월간)

### Process

#### 1.1 데이터 수집 (WebSearch + 브라우저)
```markdown
각 계정당:
- 최신 게시물 5개 수집
- 슬라이드 구조 분석 (캐러셀 10장 기준)
- 훅·본문·CTA 카피 추출
- 비주얼 스타일 관찰 (앵글, 색온도, 레이아웃)
- 인게이지먼트 데이터 수집 (좋아요, 댓글, 저장 추정)
```

#### 1.2 분석 항목 (6가지)

**A. 슬라이드 구조 패턴**
```
예:
@1ldk_shop 최신 5개 게시물 공통 패턴:
- 슬라이드 1: 전신 룩 (훅)
- 슬라이드 2-3: 디테일 클로즈업
- 슬라이드 4-7: 아이템별 정보 (브랜드·가격)
- 슬라이드 8-9: 스타일링 팁
- 슬라이드 10: CTA + 구매 링크

→ 정보 밀도 HIGH 슬라이드 비율: 60% (4-7번)
```

**B. 훅 카피 공식**
```
@oncuration 훅 패턴:
- 숫자 + 반전: "2025 S/S 트렌드 10가지, 7번은 의외"
- 질문형 공감: "이 컬러 조합, 올해 핵심인 이유는?"
- 충격적 사실: "작년 베스트셀러 가방, 올해는 NG"

→ 공통점: 구체적 숫자 + 호기심 유발
```

**C. 정보 가치 레벨**
```
@nobordersshop 정보 깊이:
- Level 1 (기본 정보): 20%
- Level 2 (해석 정보): 30%
- Level 3 (독점/통찰): 50%

→ 차별화 전략: 브랜드 스토리 + 지속가능성 맥락
```

**D. 비주얼 훅 유형**
```
@theopen_product 슬라이드 01 패턴:
- 70% 풀블리드 (제품 중심)
- 20% 타이포 중심
- 10% 플랫레이

→ 색온도: 80% Golden Hour, 20% Overcast
```

**E. 호기심 루프 전략**
```
@eun_noo 슬라이드 간 연결:
- 질문 남기기: 60%
- 반전 예고: 30%
- 숫자 떡밥: 10%

→ 다음 슬라이드 스와이프 유도 강함
```

**F. 인게이지먼트 전략**
```
@eun_noo 댓글 유도:
- CTA에서 질문 던지기: 80%
- 스토리 연계 언급: 60%
- 투표·퀴즈 스티커 활용: 40%

→ 댓글 평균: 50+ / 게시물
```

#### 1.3 Output 포맷

**파일명:** `docs/benchmarks/weekly-YYYY-MM-DD.md`

```markdown
# 벤치마크 분석 리포트

**기간:** 2026-03-10 ~ 2026-03-16  
**분석 대상:** 5개 계정, 총 25개 게시물

---

## 📊 종합 인사이트

### 1. 슬라이드 구조 트렌드
- **정보 밀도 HIGH 비율:** 평균 55% (슬라이드 4-7번 집중)
- **훅 → 정보 → CTA 3단 구조:** 80% 계정 채택

### 2. 훅 카피 베스트 프랙티스
| 유형 | 비율 | 예시 |
|------|------|------|
| 숫자 + 반전 | 50% | "2025 S/S 트렌드 10가지, 7번은 의외" |
| 질문형 공감 | 30% | "이 컬러 조합, 올해 핵심인 이유는?" |
| 충격적 사실 | 20% | "작년 베스트셀러 가방, 올해는 NG" |

### 3. 차별화 정보 전략
- **@oncuration:** 트렌드 리포트 교차 분석 (Level 3 정보 60%)
- **@nobordersshop:** 브랜드 스토리 + 지속가능성 맥락

### 4. 비주얼 트렌드
- **슬라이드 01 훅 유형:** 풀블리드 60%, 타이포 중심 25%, 분할 15%
- **색온도:** Golden Hour 우세 (65%)

### 5. 호기심 루프 패턴
- **질문 남기기 (60%)** > 반전 예고 (25%) > 숫자 떡밥 (15%)

### 6. 인게이지먼트 전략
- **댓글 유도 CTA:** 질문형 80%
- **스토리 연계:** 60% 계정 활용
- **평균 댓글 수:** 35+ / 게시물

---

## 🎯 @gena_feed 적용 액션

### 즉시 적용 (다음 시리즈)
1. ✅ **슬라이드 4-7번 정보 밀도 강화** (현재 40% → 목표 55%)
2. ✅ **훅 카피 공식 변경:** "숫자 + 반전" 우선 적용
3. ✅ **슬라이드 01 비주얼 훅:** 풀블리드 → 감정 표정 클로즈업 테스트

### 실험 (A/B 테스트)
1. 🧪 **호기심 루프 강화:** 질문 남기기 4개 이상 삽입
2. 🧪 **댓글 유도 CTA:** "댓글로 공유해주세요" 추가

### 장기 전략
1. 📅 **차별화 앵글 개발:** 제철코어 맥락 강화 (Level 3 정보 비율 40% → 60%)
2. 📅 **스토리 연계:** 캐러셀 발행 후 2시간 내 스토리 퀴즈 게시

---

## 📌 계정별 상세 분석

### @1ldk_shop (5개 게시물 분석)
...
(각 계정별 세부 분석 데이터)

---

**다음 분석 예정일:** 2026-03-17
```

---

## 🔄 Step 2: Contents-Marketer - 인사이트 추출

### Input
- `docs/benchmarks/weekly-YYYY-MM-DD.md`

### Process
1. **패턴 추출:** 5개 계정 공통 패턴 식별
2. **차별화 포인트:** @gena_feed만의 독특한 앵글 유지
3. **적용 우선순위:** HIGH (즉시) / MID (실험) / LOW (장기)

### Output
- 위 리포트의 "🎯 @gena_feed 적용 액션" 섹션 자동 생성

---

## 💾 Step 3: 자동 저장

### 저장 위치
```
docs/benchmarks/
├── weekly-2026-03-10.md
├── weekly-2026-03-17.md
├── monthly-2026-03.md
└── insights-summary.md  # 누적 인사이트 (자동 업데이트)
```

### insights-summary.md 구조
```markdown
# 벤치마킹 누적 인사이트

**최종 업데이트:** 2026-03-10

## 검증된 베스트 프랙티스 (적용 완료)
- ✅ 숫자 + 반전 훅 (저장률 +35% 향상)
- ✅ 정보 밀도 55% 유지 (스와이프 완료율 +20%)

## 실험 중
- 🧪 감정 표정 클로즈업 훅 (A/B 테스트 진행 중)
- 🧪 댓글 유도 CTA (첫 주 댓글 수 +15%)

## 보류 (효과 미미)
- ❌ 플랫레이 슬라이드 01 (훅 강도 약함)
- ❌ 타임라인형 스토리 (MZ 공감 낮음)
```

---

## 🎯 Step 4: 다음 시리즈 기획 시 자동 참조

### Gate 1 전 체크리스트 (Jarvis 자동 검증)

**Researcher가 research.md 제출 시:**

```python
def validate_research_with_benchmark(research_md):
    """
    research.md가 최신 벤치마크 인사이트를 반영했는지 검증
    """
    latest_benchmark = load_latest("docs/benchmarks/weekly-*.md")
    insights = latest_benchmark["적용 액션"]["즉시 적용"]
    
    checks = {
        '차별화 정보 Level 3': check_level3_info(research_md),
        '트렌드 교차 분석': check_cross_reference(research_md),
        '베스트 프랙티스 반영': check_best_practices(research_md, insights),
    }
    
    missing = [k for k, v in checks.items() if not v]
    
    if missing:
        return f"⚠️ 벤치마크 인사이트 미반영: {', '.join(missing)}"
    
    return "✅ 벤치마크 인사이트 반영 완료"
```

**Contents-Marketer가 plan.md 제출 시:**

```python
def validate_plan_with_benchmark(plan_md):
    """
    plan.md가 최신 벤치마크 슬라이드 구조를 반영했는지 검증
    """
    latest_benchmark = load_latest("docs/benchmarks/weekly-*.md")
    structure = latest_benchmark["슬라이드 구조 트렌드"]
    
    checks = {
        '정보 밀도 HIGH 비율': check_info_density(plan_md) >= structure["정보 밀도 평균"],
        '훅 카피 공식': check_hook_formula(plan_md, structure["훅 패턴"]),
        '호기심 루프': count_curiosity_hooks(plan_md) >= 4,
    }
    
    missing = [k for k, v in checks.items() if not v]
    
    if missing:
        return f"⚠️ 벤치마크 베스트 프랙티스 미적용: {', '.join(missing)}"
    
    return "✅ 벤치마크 베스트 프랙티스 적용 완료"
```

**Designer가 design-brief.md 제출 시:**

```python
def validate_design_with_benchmark(design_brief_md):
    """
    design-brief.md가 최신 벤치마크 비주얼 트렌드를 반영했는지 검증
    """
    latest_benchmark = load_latest("docs/benchmarks/weekly-*.md")
    visual = latest_benchmark["비주얼 트렌드"]
    
    checks = {
        '슬라이드 01 비주얼 훅': check_visual_hook_type(design_brief_md, visual["슬라이드 01 훅 유형"]),
        '색온도 리듬': check_color_temp_rhythm(design_brief_md),
        '앵글 변화': check_angle_variety(design_brief_md),
    }
    
    missing = [k for k, v in checks.items() if not v]
    
    if missing:
        return f"⚠️ 벤치마크 비주얼 트렌드 미반영: {', '.join(missing)}"
    
    return "✅ 벤치마크 비주얼 트렌드 반영 완료"
```

---

## 🔧 자동화 구현 방법

### Option A: Cron Job (추천)

**설정:**
```bash
# 매주 월요일 09:00 벤치마크 분석 실행
0 9 * * 1 cd /path/to/gena_feed && openclaw run benchmark-weekly

# 매월 첫째 주 목요일 딥다이브
0 9 1-7 * 4 cd /path/to/gena_feed && openclaw run benchmark-monthly
```

**스크립트:** `scripts/benchmark-weekly.sh`
```bash
#!/bin/bash
# 벤치마크 주간 분석 자동 실행

echo "🔍 벤치마크 분석 시작 (주간)"

# Researcher 에이전트 실행
claude --agent researcher \
  --task "벤치마크 계정 5개 분석: @1ldk_shop, @oncuration, @eun_noo, @theopen_product, @nobordersshop (최근 7일)" \
  --context workflows/benchmark-analysis.md \
  --output docs/benchmarks/weekly-$(date +%Y-%m-%d).md

# Contents-Marketer 에이전트 실행 (인사이트 추출)
claude --agent contents-marketer \
  --task "벤치마크 리포트에서 인사이트 추출 및 적용 액션 생성" \
  --context docs/benchmarks/weekly-$(date +%Y-%m-%d).md \
  --append-to docs/benchmarks/weekly-$(date +%Y-%m-%d).md

# 누적 인사이트 업데이트
python scripts/update_insights_summary.py

echo "✅ 벤치마크 분석 완료"
echo "📄 리포트: docs/benchmarks/weekly-$(date +%Y-%m-%d).md"
```

### Option B: 수동 트리거 (Claude Code)

**마보스님 명령 시:**
```
"벤치마크 분석 실행해줘"
```

**Jarvis 실행:**
1. `workflows/benchmark-analysis.md` 읽기
2. Researcher 에이전트 spawn
3. 분석 완료 후 Contents-Marketer 에이전트 spawn
4. 리포트 저장 및 알림

---

## 📈 성과 측정 (벤치마킹 효과 검증)

### 추적 지표

**매주 측정:**
```markdown
## 벤치마크 적용 전후 비교

| 지표 | 적용 전 (평균) | 적용 후 (이번 주) | 변화율 |
|------|---------------|------------------|--------|
| 저장률 | 1.2% | 1.8% | +50% |
| 스와이프 완료율 | 55% | 68% | +24% |
| 댓글 수 | 3 | 7 | +133% |
| 팔로워 증가 | +20 | +35 | +75% |

**적용 인사이트:**
- ✅ 숫자 + 반전 훅 (저장률 +0.6%p 기여)
- ✅ 정보 밀도 55% (스와이프 완료율 +13%p)
```

**분기별 리뷰:**
- 가장 효과적인 벤치마크 인사이트 TOP 3
- 효과 미미한 실험 종료
- 새로운 가설 수립

---

## ✅ 체크리스트 (매주 확인)

**벤치마크 분석 실행 전:**
- [ ] 분석 대상 계정 5개 접근 가능 (Instagram 로그인)
- [ ] 최신 게시물 5개 수집 가능 (API 또는 브라우저)
- [ ] 이전 주 리포트 백업 완료

**벤치마크 리포트 완료 후:**
- [ ] 적용 액션 3가지 이상 도출
- [ ] HIGH 우선순위 항목 1개 이상
- [ ] insights-summary.md 업데이트 완료

**다음 시리즈 기획 시작 전:**
- [ ] 최신 벤치마크 리포트 읽기 (Researcher)
- [ ] 적용 액션 체크리스트 확인 (Contents-Marketer, Designer)
- [ ] Gate 검증 통과 (Jarvis)

---

**언제 사용:**
- 주간: 매주 월요일 자동 실행 (Cron)
- 수동: 신규 시리즈 기획 전 또는 성과 부진 시
- 검증: Gate 1-3 통과 전 Jarvis 자동 체크
