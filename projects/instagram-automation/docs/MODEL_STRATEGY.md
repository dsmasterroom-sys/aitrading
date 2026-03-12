# 모델 사용 전략 - @gena_feed 인스타그램 자동화

## 핵심 원칙

**비용 vs 품질 최적화**: Opus는 핵심 의사결정에만, 나머지는 경량 모델로 효율화

---

## 모델 할당표

### 🔴 Tier 1: Opus (claude-opus-4-6) - 핵심 브레인

| 에이전트 | 모델 | 이유 |
|---|---|---|
| **CLAUDE.md (orchestrator)** | `claude-opus-4-6` | 전체 라우팅, 게이팅, 에이전트 스폰 결정 |
| **prompt-engineer** | `claude-opus-4-6` | **가장 중요** - 프롬프트 품질이 이미지/영상 결과 직접 좌우 |

**사용 빈도**: 콘텐츠 1개당 2~3회 호출
**월 예상 호출**: 약 50~70회 (주간 콘텐츠 5개 × 4주)

---

### 🟡 Tier 2: Sonnet (claude-sonnet-4-6) - 메인 워커

| 에이전트 | 모델 | 이유 |
|---|---|---|
| **researcher** | `claude-sonnet-4-6` | 트렌드 리서치, WebSearch 결과 정리 |
| **item-researcher** | `claude-sonnet-4-6` | 아이템 크롤링, items.json 구조화 |
| **video-agent** | `claude-sonnet-4-6` | ffmpeg 스크립트 정확성, 영상 파이프라인 |
| **developer** | `claude-sonnet-4-6` | HTML/CSS 구현, PNG 추출 정확성 |

**사용 빈도**: 콘텐츠 1개당 8~12회 호출
**월 예상 호출**: 약 200~300회

---

### 🟢 Tier 3: GPT-5.2 - 전문 작업

| 에이전트 | 모델 | 이유 |
|---|---|---|
| **contents-marketer** | `openai/gpt-5.2` | 카피라이팅 고품질 (USER.md의 Writer와 동일 전략) |

**사용 빈도**: 콘텐츠 1개당 2~3회 호출
**월 예상 호출**: 약 50회

---

### 🔵 Tier 4: GPT-5-mini - 경량 실행

| 에이전트 | 모델 | 이유 |
|---|---|---|
| **designer** | `openai/gpt-5-mini` | Nanogen API 호출 위주, 복잡한 추론 불필요 |
| **qa-reviewer** | `openai/gpt-5-mini` | 체크리스트 검증, validate_slide.py 실행 |
| **scheduler** | `openai/gpt-5-mini` | Meta API 호출, 스케줄링 로직 |

**사용 빈도**: 콘텐츠 1개당 5~8회 호출
**월 예상 호출**: 약 150~200회

---

## 에이전트 파일 상단 명시 형식

각 에이전트 파일(.md) 상단에 다음 형식으로 모델을 명시:

```markdown
# [에이전트명]

**Model**: claude-opus-4-6
**Role**: [역할 설명]
**Allowed Tools**: [허용 도구]
**Forbidden**: [금지 도구]

---

[에이전트 지시사항]
```

---

## 비용 예측 (월간)

| 모델 | 예상 호출 | 추정 비용 |
|---|---|---|
| claude-opus-4-6 | 120회 | 중간 |
| claude-sonnet-4-6 | 500회 | 높음 |
| openai/gpt-5.2 | 50회 | 낮음 |
| openai/gpt-5-mini | 350회 | 매우 낮음 |

**총 예상**: 월 1,000~1,200회 API 호출 (주간 콘텐츠 5개 기준)

---

## 모델 변경 기준

### Opus → Sonnet 다운그레이드 가능 조건:
- 에이전트가 3회 이상 안정적으로 작동
- 산출물 품질이 일정 수준 이상 유지
- QA 통과율 95% 이상

### Sonnet/GPT → Opus 업그레이드 필요 조건:
- QA 통과율 70% 미만
- 재작업이 2회 이상 반복
- 핵심 품질(캐릭터 일관성, 아이템 매칭) 문제 발생

---

## 특별 규칙

1. **prompt-engineer는 절대 다운그레이드 금지**
   - 프롬프트 품질 = 전체 시스템 품질
   - 비용 절감 대상에서 제외

2. **QA 루프 시 모델 유지**
   - 재작업 요청 시 원래 에이전트와 동일 모델 사용
   - 모델 혼용 시 컨텍스트 오염 가능

3. **성과 피드백 루프 후 재평가**
   - 월 1회 모델 할당 재검토
   - 비용/품질 밸런스 최적화

---

**작성일**: 2026-03-06  
**작성자**: 자비스 (OpenClaw orchestrator)
