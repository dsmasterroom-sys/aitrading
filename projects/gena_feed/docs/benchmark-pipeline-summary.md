# 벤치마킹 자동화 파이프라인 요약

**작성일:** 2026-03-11  
**목적:** 레퍼런스 계정 분석 → 인사이트 추출 → 다음 콘텐츠 자동 반영

---

## 🎯 파이프라인 개요

```
[주간 트리거 (Cron)] 
    ↓
① Researcher: 벤치마크 계정 5개 분석
    ↓
② Contents-Marketer: 인사이트 추출 & 패턴 분석
    ↓
③ 자동 저장 (docs/benchmarks/)
    ↓
④ 다음 시리즈 기획 시 자동 참조
    ↓
[Gate 1-3 통과 전 Jarvis 자동 검증]
```

---

## 📂 생성된 파일 목록

### 1. 워크플로 정의
- **`workflows/benchmark-analysis.md`** (8KB)
  - 벤치마킹 자동화 전체 워크플로
  - 6가지 분석 항목 상세 가이드
  - 출력 포맷 정의

### 2. 스킬 업데이트
- **`skills/research.md`** (업데이트)
  - Step 4 추가: 벤치마크 계정 분석
  - 자동 검증 규칙 포함

### 3. 에이전트 설정 업데이트
- **`AGENT.md`** (업데이트)
  - researcher: contextFiles에 `benchmark-analysis.md`, `insights-summary.md` 추가
  - contents-marketer: 신규 스킬 3개 + `insights-summary.md` 추가
  - designer: `visual-hook-strategy.md` + `insights-summary.md` 추가

### 4. 누적 인사이트 저장소
- **`docs/benchmarks/insights-summary.md`** (신규)
  - 검증된 베스트 프랙티스
  - 실험 중 항목
  - 보류 (효과 미미) 항목
  - 계정별 핵심 인사이트

### 5. 자동화 스크립트
- **`scripts/benchmark-weekly.sh`** (신규)
  - 주간 벤치마크 분석 실행
  - 3단계 자동화 (Researcher → Contents-Marketer → 인사이트 업데이트)

---

## 📅 실행 주기

### 정기 실행 (Cron 설정 권장)

```bash
# 매주 월요일 09:00
0 9 * * 1 cd /path/to/gena_feed && bash scripts/benchmark-weekly.sh

# 매월 첫째 주 목요일 09:00 (딥다이브)
0 9 1-7 * 4 cd /path/to/gena_feed && bash scripts/benchmark-monthly.sh
```

### 수동 트리거
- 마보스님 요청 시: "벤치마크 분석 실행해줘"
- 신규 시리즈 기획 전
- 성과 부진 시 (저장률 < 1.5%)

---

## 🔍 분석 대상 계정 5개

| 계정 | 카테고리 | 벤치마킹 포인트 |
|------|---------|----------------|
| **@1ldk_shop** | 편집샵 | 제품 정보 상세성, 레이아웃 |
| **@oncuration** | 트렌드 큐레이션 | 정보 구조, 데이터 시각화 |
| **@eun_noo** | 패션 인플루언서 | 릴스 전환, 소통 전략 |
| **@theopen_product** | 패션 브랜드 | 스토리텔링, 시즌 콘셉트 |
| **@nobordersshop** | 지속가능 패션 | 차별화 가치, 정보 깊이 |

---

## 📊 분석 항목 6가지

1. **슬라이드 구조 패턴**
   - 훅 → 정보 → CTA 배분 비율
   - 정보 밀도 HIGH 슬라이드 위치

2. **훅 카피 공식**
   - 숫자 + 반전 / 질문형 / 충격 비율
   - 구체적 예시 추출

3. **정보 가치 레벨 분석**
   - Level 1/2/3 비율
   - 차별화 전략 패턴

4. **비주얼 훅 유형**
   - 슬라이드 01 주요 유형
   - 색온도 분포

5. **호기심 루프 패턴**
   - 슬라이드 간 연결 전략

6. **인게이지먼트 전략**
   - 댓글 유도 CTA 패턴
   - 평균 댓글/저장 추정

---

## 🔄 자동 반영 프로세스

### Gate 1: Researcher 제출 시
```python
# Jarvis 자동 검증
def validate_research_with_benchmark(research_md):
    latest_benchmark = load_latest("docs/benchmarks/weekly-*.md")
    
    checks = {
        '차별화 정보 Level 3': check_level3_info(research_md),
        '트렌드 교차 분석': check_cross_reference(research_md),
        '베스트 프랙티스 반영': check_best_practices(research_md),
    }
    
    if missing:
        return "⚠️ 벤치마크 인사이트 미반영: ..."
    return "✅ 반영 완료"
```

### Gate 2: Contents-Marketer 제출 시
```python
def validate_plan_with_benchmark(plan_md):
    checks = {
        '정보 밀도 HIGH 비율': check_info_density(plan_md) >= 55%,
        '훅 카피 공식': check_hook_formula(plan_md),
        '호기심 루프': count_curiosity_hooks(plan_md) >= 4,
    }
```

### Gate 3: Designer 제출 시
```python
def validate_design_with_benchmark(design_brief_md):
    checks = {
        '슬라이드 01 비주얼 훅': check_visual_hook_type(...),
        '색온도 리듬': check_color_temp_rhythm(...),
        '앵글 변화': check_angle_variety(...),
    }
```

---

## 📈 성과 측정 (벤치마킹 효과 검증)

### 주간 측정 지표

| 지표 | 적용 전 (평균) | 적용 후 (목표) | 실제 결과 |
|------|---------------|---------------|----------|
| 저장률 | 1.2% | 2.5%+ | ? |
| 스와이프 완료율 | 55% | 70%+ | ? |
| 댓글 수 | 3 | 5+ | ? |
| 팔로워 증가 | +20 | +50+ | ? |

### 분기별 리뷰
- 가장 효과적인 벤치마크 인사이트 TOP 3
- 효과 미미한 실험 종료
- 새로운 가설 수립

---

## ✅ 즉시 실행 체크리스트

### Phase 1: 초기 설정 (완료)
- ✅ `workflows/benchmark-analysis.md` 생성
- ✅ `skills/research.md` 업데이트
- ✅ `AGENT.md` contextFiles 추가
- ✅ `docs/benchmarks/insights-summary.md` 초기화
- ✅ `scripts/benchmark-weekly.sh` 생성

### Phase 2: 첫 실행 (다음 단계)
- [ ] 수동으로 첫 벤치마크 분석 실행
  - Jarvis에게 요청: "벤치마크 주간 분석 실행해줘"
- [ ] `docs/benchmarks/weekly-2026-03-17.md` 생성 확인
- [ ] `insights-summary.md` 업데이트 확인

### Phase 3: 자동화 (선택)
- [ ] Cron 설정 (매주 월요일 09:00)
- [ ] `update_insights_summary.py` 스크립트 개발 (자동 업데이트)
- [ ] Slack/Telegram 알림 연동 (분석 완료 시)

### Phase 4: 첫 적용 (검증)
- [ ] 신규 시리즈 기획 시 벤치마크 인사이트 자동 참조 확인
- [ ] Gate 1-3 검증 통과 여부 확인
- [ ] A/B 테스트 (벤치마크 적용 전 vs 후)

---

## 🎯 기대 효과

### 단기 (1-2개월)
- ✅ 최신 트렌드 자동 반영 (수동 리서치 시간 50% 절감)
- ✅ 베스트 프랙티스 자동 적용 (품질 일관성 향상)
- ✅ 실험 데이터 누적 (실패 사례 반복 방지)

### 중장기 (3-6개월)
- 🎯 저장률 1.2% → 2.5%+ (벤치마크 인사이트 적용)
- 🎯 스와이프 완료율 55% → 70%+ (호기심 루프 강화)
- 🎯 성과 예측 정확도 향상 (과거 데이터 기반)

---

## 💡 추가 개선 아이디어 (향후)

1. **AI 자동 분석**
   - GPT Vision으로 계정 스크린샷 자동 분석
   - 슬라이드 구조·색온도·레이아웃 자동 추출

2. **실시간 트렌드 알림**
   - 벤치마크 계정 신규 게시물 자동 감지
   - 바이럴 게시물 (저장 1000+ 달성 시) 즉시 알림

3. **경쟁사 확대**
   - 벤치마크 계정 5개 → 10개로 확대
   - 카테고리별 분류 (편집샵 / 인플루언서 / 브랜드)

4. **성과 자동 연결**
   - Instagram Insights API 연동
   - 벤치마크 인사이트별 성과 기여도 자동 계산

---

## 📞 문의 및 피드백

**실행 중 문제 발생 시:**
- Jarvis에게 문의: "벤치마크 파이프라인 상태 확인해줘"
- 수동 실행: `bash scripts/benchmark-weekly.sh`

**개선 제안:**
- 마보스님 요청 시 즉시 반영
- 분기별 파이프라인 리뷰 및 최적화

---

**작성 완료: 2026-03-11**  
**다음 액션:** 첫 벤치마크 분석 실행 (수동 트리거)
