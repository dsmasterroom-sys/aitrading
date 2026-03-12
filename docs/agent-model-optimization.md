# 에이전트 모델 할당 최적화 가이드

최종 업데이트: 2026-03-08

## 📊 현재 모델 할당 현황

| 에이전트 | 현재 모델 | 비용 | 성능 | 최적화 상태 |
|---------|----------|------|------|-----------|
| **main (자비스)** | claude-sonnet-4-5 | $$$ | ⭐⭐⭐⭐⭐ | ✅ 최적 |
| **developer** | claude-sonnet-4-5 | $$$ | ⭐⭐⭐⭐⭐ | ⚠️ 검토 필요 |
| **researcher** | claude-sonnet-4-5 | $$$ | ⭐⭐⭐⭐ | ⚠️ 오버스펙 |
| **contents-marketer** | gpt-5.2 | $$ | ⭐⭐⭐⭐ | ✅ 최적 |
| **designer** | gpt-5.3-codex | $$ | ⭐⭐⭐ | ⚠️ 모델 불일치 |
| **item-researcher** | claude-sonnet-4-5 | $$$ | ⭐⭐⭐⭐ | ⚠️ 오버스펙 |
| **prompt-engineer** | claude-opus-4-5 | $$$$ | ⭐⭐⭐⭐⭐ | ⚠️ 고비용 |
| **video-agent** | claude-sonnet-4-5 | $$$ | ⭐⭐⭐⭐ | ✅ 적정 |
| **qa-reviewer** | gpt-5-mini | $ | ⭐⭐⭐ | ✅ 최적 |
| **scheduler** | gpt-5-mini | $ | ⭐⭐⭐ | ✅ 최적 |
| **imagegen** | claude-sonnet-4-5 | $$$ | ⭐⭐⭐⭐ | ✅ 적정 |

---

## 🎯 최적화 제안

### 우선순위 높음 (즉시 적용 권장)

#### 1. **Researcher → gpt-5-mini**
**현재**: claude-sonnet-4-5 ($$$)  
**제안**: gpt-5-mini ($)  
**이유**:
- 웹 검색 및 정보 수집은 고성능 모델 불필요
- 비용 절감: 약 70% ↓
- 성능: 웹 검색 결과 요약에는 충분

**리스크**: 복잡한 분석 능력 저하 (단, 대부분 작업은 단순 검색/요약)

#### 2. **Item-Researcher → gpt-5-mini**
**현재**: claude-sonnet-4-5 ($$$)  
**제안**: gpt-5-mini ($)  
**이유**:
- 제품 정보 수집 및 정리 작업
- Researcher와 유사한 작업 패턴
- 비용 절감: 약 70% ↓

**리스크**: 낮음 (단순 정보 수집 작업)

#### 3. **Designer → claude-sonnet-4-5 또는 gpt-5-mini**
**현재**: gpt-5.3-codex ($$)  
**문제**: Codex는 코딩 모델, 디자인 개념화에는 부적합  
**제안**:
- **Option A**: claude-sonnet-4-5 (고품질 디자인 설명 필요 시)
- **Option B**: gpt-5-mini (비용 우선 시)

**권장**: Option B (gpt-5-mini)

### 우선순위 중간 (선택적 적용)

#### 4. **Prompt-Engineer 모델 검토**
**현재**: claude-opus-4-5 ($$$$)  
**이유**: 가장 비싼 모델 사용 중  
**옵션**:
- **유지**: 프롬프트 엔지니어링은 고도의 언어 이해 필요
- **다운그레이드**: claude-sonnet-4-5로 변경 (30% 비용 절감)

**권장**: 사용 빈도 확인 후 결정 (빈도 낮으면 유지, 높으면 다운그레이드)

#### 5. **Developer 역할 재검토**
**현재**: claude-sonnet-4-5 ($$$)  
**질문**: 실제로 복잡한 코딩 작업을 하는가?  
**옵션**:
- **유지**: 고급 리팩토링/아키텍처 설계 시
- **다운그레이드**: gpt-5.3-codex (코딩 특화, 비용 ↓)

**권장**: 사용 패턴 분석 필요

---

## 💰 예상 비용 절감

### 현재 구성 (월간 추정)
- Main: 고정 (필수)
- Developer: $150
- Researcher: $100 → **$30 (gpt-5-mini)**
- Contents-marketer: $80 (유지)
- Designer: $60 → **$30 (gpt-5-mini)**
- Item-researcher: $80 → **$25 (gpt-5-mini)**
- Prompt-engineer: $200 (검토)
- Video-agent: $120 (유지)
- QA-reviewer: $20 (유지)
- Scheduler: $15 (유지)
- ImageGen: $50 (유지)

**절감 잠재력**: 약 $215/월 (약 30% 절감)

---

## 🔄 적용 방법

### 1단계: 즉시 적용 (리스크 낮음)
```bash
openclaw config edit
```

```json
{
  "agents": {
    "list": [
      {
        "id": "researcher",
        "model": "openai/gpt-5-mini"
      },
      {
        "id": "item-researcher",
        "model": "openai/gpt-5-mini"
      },
      {
        "id": "designer",
        "model": "openai/gpt-5-mini"
      }
    ]
  }
}
```

### 2단계: 모니터링 (1주일)
- 각 에이전트의 출력 품질 확인
- 작업 실패율 모니터링
- 마보스님 피드백 수집

### 3단계: 추가 최적화 (필요 시)
- Prompt-engineer 다운그레이드
- Developer 모델 변경

---

## 📈 성공 지표

- ✅ 비용 30% 이상 절감
- ✅ 작업 품질 유지 (90% 이상)
- ✅ 작업 실패율 5% 이하
- ✅ 마보스님 만족도 유지

---

## ⚠️ 주의사항

1. **Main (자비스)는 절대 다운그레이드 금지**
   - 전체 오케스트레이션 담당
   - 최고 성능 필수

2. **Contents-marketer 유지**
   - 브랜드 톤 유지 중요
   - 고품질 마케팅 문구 필요

3. **점진적 적용**
   - 한 번에 모든 에이전트 변경 금지
   - 단계별 테스트 및 검증

---

**다음 리뷰 예정**: 2026-03-15 (1주일 후)
