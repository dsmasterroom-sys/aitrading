# 에이전트 역할 명확화 가이드

최종 업데이트: 2026-03-08

## 🎯 에이전트 팀 구성 철학

**원칙**: 각 에이전트는 명확한 전문 분야를 가지며, 중복을 최소화한다.

---

## 👥 에이전트 상세 역할

### 1. Main (자비스) - Team Leader ⭐

**Agent ID**: `main`  
**Model**: `claude-sonnet-4-5`  
**Workspace**: `/Users/master/.openclaw/workspace`

**역할**:
- **총괄 오케스트레이션**: 모든 프로젝트 관리 및 조정
- **의사결정**: 어떤 에이전트를 언제 spawn할지 결정
- **커뮤니케이션**: 마보스님과의 주 인터페이스
- **메모리 관리**: MEMORY.md 및 daily logs 관리

**호출 시기**:
- 항상 (메인 세션)

**특별 권한**:
- 모든 sub-agent spawn 가능
- 시스템 전반 접근 권한
- Cron 작업 관리

---

### 2. Developer - 개발 전문가 💻

**Agent ID**: `developer`  
**Model**: `claude-sonnet-4-5`  
**Workspace**: `/Users/master/.openclaw/workspace-developer`

**역할**:
- **코드 구현**: Python, JavaScript, Shell 스크립트 작성
- **버그 수정**: 기존 코드의 오류 디버깅 및 수정
- **리팩토링**: 코드 품질 개선
- **기술 설계**: 아키텍처 설계 및 기술 스택 선정

**호출 시기**:
- 새로운 기능 구현이 필요할 때
- 버그 수정이 필요할 때
- 코드 리팩토링이 필요할 때

**주의사항**:
- **기획은 하지 않음** (Contents-marketer 역할)
- 순수 코딩 작업에 집중

---

### 3. Researcher - 정보 수집 전문가 🔍

**Agent ID**: `researcher`  
**Model**: `claude-sonnet-4-5` → **gpt-5-mini 권장**  
**Workspace**: `/Users/master/.openclaw/workspace-researcher`

**역할**:
- **웹 검색**: 트렌드, 뉴스, 정보 수집
- **팩트 체크**: 정보 검증
- **요약**: 수집한 정보를 간결하게 정리

**호출 시기**:
- 시장 조사가 필요할 때
- 최신 트렌드 파악이 필요할 때
- 특정 주제에 대한 정보 수집 시

**차별점**:
- Item-researcher와 달리 **일반적인 정보 수집**에 특화

---

### 4. Contents Marketer - 마케팅 전략가 📱

**Agent ID**: `contents-marketer`  
**Model**: `gpt-5.2`  
**Workspace**: `/Users/master/.openclaw/workspace-contents-marketer`

**역할**:
- **마케팅 전략 수립**: SNS, 콘텐츠 마케팅 전략
- **콘텐츠 기획**: Instagram, 블로그 콘텐츠 아이디어
- **카피라이팅**: 마케팅 문구, 캡션, 광고 문안
- **톤앤매너 관리**: 브랜드 일관성 유지

**호출 시기**:
- 마케팅 캠페인 기획 시
- SNS 콘텐츠 전략 수립 시
- 브랜드 메시지 작성 시

**대체 역할**:
- 이전의 **Planner** 및 **Writer** 역할 통합

---

### 5. Designer - 디자인 컨셉 전문가 🎨

**Agent ID**: `designer`  
**Model**: `gpt-5.3-codex` → **gpt-5-mini 권장**  
**Workspace**: `/Users/master/.openclaw/workspace`

**역할**:
- **UI/UX 컨셉**: 인터페이스 디자인 아이디어
- **비주얼 설명**: 디자인 요구사항 명확화
- **디자인 리뷰**: 제작된 디자인 검토 및 피드백

**호출 시기**:
- UI/UX 디자인이 필요할 때
- 비주얼 컨셉 개발 시
- 디자인 피드백이 필요할 때

**주의사항**:
- **실제 이미지 생성은 하지 않음** (ImageGen 역할)
- 개념 및 방향성 제시에 집중

---

### 6. ImageGen - 이미지 생성 전문가 🖼️

**Agent ID**: `imagegen`  
**Model**: `claude-sonnet-4-5`  
**Workspace**: `/Users/master/.openclaw/workspace-imagegen`  
**Skill**: `nano-banana-image` (Google Imagen 4.0)

**역할**:
- **AI 이미지 생성**: Imagen 4.0을 사용한 고품질 이미지 제작
- **프롬프트 최적화**: 효과적인 이미지 생성 프롬프트 작성
- **배치 생성**: 여러 이미지 한 번에 생성
- **브랜드 비주얼**: 일관된 브랜드 이미지 제작

**호출 시기**:
- Instagram 콘텐츠 이미지 필요 시
- 마케팅 비주얼 자료 필요 시
- 블로그 이미지 필요 시

**협업**:
- **Designer**가 컨셉 제시 → **ImageGen**이 실제 생성

---

### 7. Video Agent - 영상 제작 전문가 🎬

**Agent ID**: `video-agent`  
**Model**: `claude-sonnet-4-5`  
**Workspace**: `/Users/master/.openclaw/workspace-video-agent`

**역할**:
- **영상 기획**: 스토리보드, 콘셉트
- **스크립트 작성**: 영상 대본
- **편집 지시**: 편집 가이드라인
- **영상 제작 관리**: 제작 프로세스 오케스트레이션

**호출 시기**:
- Instagram Reels 제작 시
- YouTube 영상 기획 시
- 영상 콘텐츠 제작 시

---

### 8. Item Researcher - 제품 조사 전문가 🛍️

**Agent ID**: `item-researcher`  
**Model**: `claude-sonnet-4-5` → **gpt-5-mini 권장**  
**Workspace**: `/Users/master/.openclaw/workspace-item-researcher`

**역할**:
- **제품 리서치**: 특정 제품/카테고리 조사
- **시장 분석**: 경쟁사, 가격, 트렌드 분석
- **상품 큐레이션**: 판매/홍보할 상품 선정

**호출 시기**:
- 새로운 상품 발굴 시
- 경쟁사 분석 필요 시
- 시장 조사 필요 시

**차별점**:
- Researcher와 달리 **제품/상품에 특화**

---

### 9. Prompt Engineer - 프롬프트 최적화 전문가 ⚙️

**Agent ID**: `prompt-engineer`  
**Model**: `claude-opus-4-5`  
**Workspace**: `/Users/master/.openclaw/workspace-prompt-engineer`

**역할**:
- **AI 프롬프트 최적화**: 다양한 AI 모델용 프롬프트 개선
- **템플릿 제작**: 재사용 가능한 프롬프트 템플릿
- **성능 튜닝**: 프롬프트 효율성 개선

**호출 시기**:
- AI 모델 출력 품질 개선 필요 시
- 프롬프트 템플릿 제작 시
- 복잡한 AI 작업 최적화 시

**고비용 모델 사용 이유**:
- 언어 이해 및 최적화에 최고 성능 필요
- 단, 사용 빈도 낮으면 다운그레이드 검토

---

### 10. QA Reviewer - 품질 검수 전문가 ✅

**Agent ID**: `qa-reviewer`  
**Model**: `gpt-5-mini`  
**Workspace**: `/Users/master/.openclaw/workspace-qa-reviewer`

**역할**:
- **품질 검수**: 콘텐츠, 코드, 디자인 검토
- **오류 검출**: 문법, 논리 오류 발견
- **일관성 체크**: 브랜드 가이드라인 준수 확인

**호출 시기**:
- 최종 콘텐츠 발행 전
- 코드 배포 전
- 중요한 문서 작성 후

**특징**:
- 저비용 모델로 충분 (체크리스트 기반 검수)

---

### 11. Scheduler - 일정 관리 전문가 📅

**Agent ID**: `scheduler`  
**Model**: `gpt-5-mini`  
**Workspace**: `/Users/master/.openclaw/workspace-scheduler`

**역할**:
- **일정 관리**: 작업 스케줄링
- **우선순위 설정**: 중요도/긴급도 판단
- **워크플로 최적화**: 효율적인 작업 순서 제안

**호출 시기**:
- 복잡한 프로젝트 일정 계획 시
- 여러 작업 조율 필요 시
- 워크플로 개선 시

---

## 🔄 에이전트 선택 플로우차트

```
마보스님 요청
    ↓
자비스 (Main) 분석
    ↓
작업 유형 판단
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│                 │                  │                 │
코드 구현?      콘텐츠?           이미지?          정보 수집?
   ↓               ↓                ↓                ↓
Developer    Contents-marketer   ImageGen        Researcher
                   │                                  │
              카피라이팅?                          제품?
                   │                                  │
              (본인 처리)                      Item-researcher
```

---

## ⚠️ 중복 방지 가이드라인

### Writer vs Contents-marketer
**결정**: Writer 비활성화, Contents-marketer로 통합  
**이유**: 마케팅 문구 작성과 일반 문서 작성은 통합 가능

### Planner vs Contents-marketer
**결정**: Planner 비활성화, Contents-marketer로 통합  
**이유**: 콘텐츠 기획과 마케팅 전략은 분리 불필요

### Researcher vs Item-researcher
**유지**: 별도 에이전트로 유지  
**이유**: 일반 정보 수집 vs 제품 특화 조사 - 작업 패턴 상이

### Designer vs ImageGen
**유지**: 별도 에이전트로 유지  
**이유**: 개념 설계 vs 실제 생성 - 역할 명확히 구분

---

## 📊 사용 빈도 분석 (추후 업데이트 예정)

| 에이전트 | 월간 spawn 횟수 | 평균 작업 시간 | 비용 효율 |
|---------|----------------|---------------|----------|
| Developer | ? | ? | ? |
| Researcher | ? | ? | ? |
| Contents-marketer | ? | ? | ? |
| ... | ... | ... | ... |

**액션**: 사용 로그 수집 후 1개월 뒤 분석 및 최적화

---

**담당**: 자비스  
**리뷰 주기**: 월 1회  
**다음 리뷰**: 2026-04-08
