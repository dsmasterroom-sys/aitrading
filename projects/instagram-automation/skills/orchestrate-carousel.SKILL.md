# Orchestrate Carousel SKILL

**용도**: 캐러셀 자동 생성 전체 파이프라인 오케스트레이션  
**담당**: 자비스 (메인 세션)  
**트리거**: "캐러셀 만들어줘", "인스타 캐러셀 생성"

---

## 🎯 목표

사용자가 토픽을 요청하면, 자동으로:
1. 리서치 (병렬)
2. 프롬프트 생성
3. 콘텐츠 기획 + 이미지 생성 (병렬)
4. HTML 슬라이드
5. QA 검수
6. 스케줄링

각 단계 완료 시 자동 저장.

---

## 📋 실행 흐름

### Step 1: 작업 폴더 생성

```python
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
topic_slug = topic.lower().replace(" ", "_")[:50]
work_dir = f"content/{timestamp}_{topic_slug}"

# 폴더 생성
exec(f"mkdir -p {work_dir}/{{assets,slides,reels}}")
```

### Step 2: 병렬 리서치

```python
# researcher 스폰
researcher_session = sessions_spawn(
    agentId="researcher",
    task=f"{topic} 관련 인스타그램 트렌드 조사.\n"
         f"추천 토픽 6개 제시.\n"
         f"출력: {work_dir}/research.md",
    model="claude-sonnet-4-6",
    label=f"{timestamp}_researcher",
    runTimeoutSeconds=600
)

# item-researcher 스폰 (병렬)
item_researcher_session = sessions_spawn(
    agentId="item-researcher",
    task=f"{topic} 관련 패션 아이템 10개 수집 (무신사/지그재그).\n"
         f"각 아이템: ref_image_url, brand, price, visual_desc.\n"
         f"출력: {work_dir}/items.json",
    model="claude-sonnet-4-6",
    label=f"{timestamp}_item_researcher",
    runTimeoutSeconds=600
)
```

**대기 전략**:
- 두 세션 모두 완료될 때까지 대기
- `sessions_history`로 폴링
- 완료 시 다음 단계 진행

### Step 3: Gate G1 - 토픽 확정

```python
# research.md 읽기
research = read(f"{work_dir}/research.md")

# 사용자에게 토픽 선택 요청
message = f"""
📊 트렌드 리서치 완료!

{research}

어떤 토픽으로 진행할까요? (1-6 번호 또는 직접 입력)
"""

# 사용자 응답 대기
# selected_topic = ... (사용자 입력)
```

**자동화 옵션**:
- 사용자 확인 생략 시 첫 번째 토픽 자동 선택

### Step 4: 프롬프트 생성

```python
prompt_engineer_session = sessions_spawn(
    agentId="prompt-engineer",
    task=f"토픽: {selected_topic}\n"
         f"아이템: {work_dir}/items.json\n"
         f"Gena Master Prompt: shared/gena-master-prompt.md\n"
         f"캐러셀 10슬라이드 프롬프트 생성.\n"
         f"출력: {work_dir}/prompts.json",
    model="claude-opus-4-6",
    label=f"{timestamp}_prompt_engineer",
    runTimeoutSeconds=900
)
```

**자기 검증**:
- prompt-engineer가 내부적으로 10개 체크리스트 실행
- 실패 시 자동 재생성 (최대 2회)

### Step 5: 콘텐츠 기획 + 이미지 생성 (병렬)

```python
# contents-marketer 스폰
marketer_session = sessions_spawn(
    agentId="contents-marketer",
    task=f"캐러셀 기획 및 카피 작성.\n"
         f"입력: {work_dir}/prompts.json, {work_dir}/items.json\n"
         f"출력: {work_dir}/plan.md, {work_dir}/copy.md",
    model="openai/gpt-5.2",
    label=f"{timestamp}_marketer",
    runTimeoutSeconds=600
)

# designer 스폰 (병렬)
designer_session = sessions_spawn(
    agentId="designer",
    task=f"캐러셀 10슬라이드 이미지 생성 (Nanogen Outfit Swap).\n"
         f"입력: {work_dir}/prompts.json, shared/gena-references/*.png\n"
         f"출력: {work_dir}/assets/carousel_slide_01.png ~ 10.png\n"
         f"Gena 캐릭터 일관성 최우선.",
    model="openai/gpt-5-mini",
    label=f"{timestamp}_designer",
    runTimeoutSeconds=1800  # 30분
)
```

**진행 추적**:
- designer는 오래 걸리므로 주기적으로 진행 상황 확인
- 완료 시 "이미지 10장 생성 완료" 알림

### Step 6: HTML 슬라이드 생성

```python
developer_session = sessions_spawn(
    agentId="developer",
    task=f"캐러셀 HTML 슬라이드 생성 (디자인 시스템 기반).\n"
         f"입력: {work_dir}/assets/*.png, {work_dir}/copy.md\n"
         f"디자인 시스템: shared/design-system/\n"
         f"Puppeteer로 PNG 렌더링 (2160×2880px).\n"
         f"출력: {work_dir}/slides/slide_01.html ~ 10.html\n"
         f"출력: {work_dir}/slides/slide_01.png ~ 10.png",
    model="claude-sonnet-4-6",
    label=f"{timestamp}_developer",
    runTimeoutSeconds=900
)
```

### Step 7: QA 검수

```python
qa_reviewer_session = sessions_spawn(
    agentId="qa-reviewer",
    task=f"캐러셀 QA 검수 (시각/팩트/레이아웃).\n"
         f"입력: {work_dir}/slides/*.png, {work_dir}/items.json\n"
         f"validate_slide.py 실행.\n"
         f"출력: {work_dir}/qa-report.md",
    model="openai/gpt-5-mini",
    label=f"{timestamp}_qa_reviewer",
    runTimeoutSeconds=600
)
```

**Gate G3: QA 통과**:
- qa-report.md 읽기
- 고/중 이슈 0건 → 통과
- 고/중 이슈 발견 → developer 수정 루프 (최대 3회)
- 3회 실패 → 사용자 에스컬레이션

### Step 8: 스케줄링

```python
scheduler_session = sessions_spawn(
    agentId="scheduler",
    task=f"캐러셀 발행 준비 (Meta API 업로드).\n"
         f"입력: {work_dir}/slides/*.png, {work_dir}/copy.md, {work_dir}/research.md\n"
         f"출력: {work_dir}/schedule.json",
    model="openai/gpt-5-mini",
    label=f"{timestamp}_scheduler",
    runTimeoutSeconds=300
)
```

**Gate G4: 발행 승인** (선택):
- 사용자 확인 요청: "최종 슬라이드 확인 후 발행하시겠습니까?"
- 승인 → 발행 실행
- 자동 발행 설정 시 즉시 발행

### Step 9: 발행

```python
# scheduler가 자동으로 Meta API 호출
# 또는 수동 발행
```

---

## 📝 자동 저장 규칙

각 단계 완료 시:
1. 해당 세션의 출력 파일 확인
2. `memory/YYYY-MM-DD.md`에 진행 상황 기록
3. 사용자에게 간단히 알림 (예: "✅ Phase 2 완료: 프롬프트 10개 생성")

**저장 형식**:
```markdown
## 캐러셀 자동 생성 ({timestamp})

- 토픽: {topic}
- 작업 폴더: {work_dir}
- 진행 상황:
  - [x] Phase 1: 리서치 (완료)
  - [x] Phase 2: 프롬프트 (완료)
  - [x] Phase 3: 콘텐츠 + 이미지 (완료)
  - [ ] Phase 4: HTML 슬라이드 (진행 중...)
```

---

## ⏱️ 예상 소요 시간

| Phase | 소요 시간 |
|---|---|
| 리서치 (병렬) | 30분 |
| 프롬프트 | 20분 |
| 콘텐츠 + 이미지 (병렬) | 60분 |
| HTML 슬라이드 | 30분 |
| QA 검수 | 15분 |
| 스케줄링 | 10분 |
| **총** | **약 2.5시간** |

---

## 🚨 에러 핸들링

### sessions_spawn 실패
- 재시도 (최대 2회)
- 실패 시 사용자에게 에러 메시지 전달

### QA 루프 무한 방지
- developer 수정 최대 3회
- 3회 실패 → 사용자 수동 확인

### 타임아웃
- 각 세션에 타임아웃 설정
- 초과 시 sessions_send로 "진행 상황 확인" 요청
- 여전히 무응답 시 세션 종료 및 재시도

---

## ✅ 성공 조건

1. 모든 Phase 완료
2. QA 통과
3. 최종 슬라이드 10장 생성
4. schedule.json 작성 완료

**최종 알림**:
```
🎉 캐러셀 자동 생성 완료!

토픽: {topic}
슬라이드: 10장
QA: 통과
작업 폴더: {work_dir}

발행하시겠습니까?
```

---

**최종 업데이트**: 2026-03-06  
**담당**: 자비스 (Orchestrator)
