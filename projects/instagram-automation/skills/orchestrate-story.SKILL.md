# Orchestrate Story SKILL

**용도**: 스토리 자동 생성 전체 파이프라인 오케스트레이션  
**담당**: 자비스 (메인 세션)  
**트리거**: "스토리 만들어줘", "오늘의 스토리 생성"

---

## 🎯 목표

사용자가 주제를 요청하면, 자동으로:
1. 프롬프트 생성
2. 이미지 생성 (1장)
3. 캡션 작성
4. QA 검수 (간소화)
5. 발행

**특징**: 캐러셀/릴스보다 훨씬 간단. 약 30분 완성.

---

## 📋 실행 흐름

### Step 1: 작업 폴더 생성

```python
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
work_dir = f"content/{timestamp}_story"

# 폴더 생성
exec(f"mkdir -p {work_dir}/stories")
```

### Step 2: 주제 확인

**사용자 입력**:
- "오늘의 봄 재킷"
- "재고 아이템 XYZ"

**자동 모드** (cron):
```python
# researcher 스폰 (옵션)
researcher_session = sessions_spawn(
    agentId="researcher",
    task="오늘의 스토리 주제 추천 (간단한 일상/트렌드 1개)",
    model="claude-sonnet-4-6",
    runTimeoutSeconds=300
)

# 결과 저장
topic = read(f"{work_dir}/story_topic.txt")
```

**수동 모드**:
```python
# 사용자 입력 그대로 사용
topic = "봄 재킷"
write(f"{work_dir}/story_topic.txt", topic)
```

### Step 3: 아이템 선정 (옵션)

**자동 모드**:
```python
item_researcher_session = sessions_spawn(
    agentId="item-researcher",
    task=f"'{topic}' 관련 아이템 1개 추천 (재고 우선)",
    model="claude-sonnet-4-6",
    runTimeoutSeconds=300
)

# 결과 저장: work_dir/story_item.json
```

**수동 모드**:
```python
# 재고 아이템 직접 지정
item = {
    "id": "jacket_001",
    "name": "스프링 데님 재킷",
    "ref_image_url": "https://...",
    "price": 89000
}
write(f"{work_dir}/story_item.json", json.dumps(item))
```

### Step 4: 프롬프트 생성

```python
prompt_engineer_session = sessions_spawn(
    agentId="prompt-engineer",
    task=f"스토리 이미지 프롬프트 1개 생성.\n"
         f"주제: {topic}\n"
         f"아이템: {work_dir}/story_item.json (있으면)\n"
         f"Gena Master Prompt: shared/gena-master-prompt.md\n"
         f"출력: {work_dir}/story_prompt.json",
    model="claude-opus-4-6",
    runTimeoutSeconds=300
)
```

**출력**:
```json
{
  "image_prompt": "A young Korean woman wearing spring denim jacket...",
  "reference_images": ["gena_ref_02.png", "jacket_001"]
}
```

### Step 5: 이미지 생성

```python
designer_session = sessions_spawn(
    agentId="designer",
    task=f"스토리 이미지 1장 생성 (Nanogen Outfit Swap).\n"
         f"입력: {work_dir}/story_prompt.json\n"
         f"Gena 참조: shared/gena-references/\n"
         f"출력: {work_dir}/stories/story_01.png (1080×1920px, 9:16)\n"
         f"Gena 캐릭터 일관성 최우선.",
    model="openai/gpt-5-mini",
    runTimeoutSeconds=1200  # 20분
)
```

**내부 실행** (designer 에이전트):
```bash
python scripts/nanogen_image.py \
    --content-path {work_dir} \
    --slide-id story_01 \
    --aspect-ratio 9:16 \
    --resolution 2K
```

### Step 6: 캡션 작성

```python
marketer_session = sessions_spawn(
    agentId="contents-marketer",
    task=f"스토리 캡션 작성 (짧고 감성적, 1~2줄).\n"
         f"주제: {topic}\n"
         f"아이템: {work_dir}/story_item.json (있으면)\n"
         f"출력: {work_dir}/story_caption.txt",
    model="openai/gpt-5.2",
    runTimeoutSeconds=300
)
```

**출력 예시**:
```
봄이 오는 소리 🌸
#봄재킷 #데일리룩
```

### Step 7: 간소화 QA

```python
qa_reviewer_session = sessions_spawn(
    agentId="qa-reviewer",
    task=f"스토리 QA 검수 (간소화).\n"
         f"입력: {work_dir}/stories/story_01.png, {work_dir}/story_item.json\n"
         f"검수 항목 4개만:\n"
         f"1. Gena 캐릭터 일관성\n"
         f"2. 아이템 시각 정확성\n"
         f"3. 해상도 1080×1920px\n"
         f"4. 비율 9:16\n"
         f"출력: {work_dir}/qa-report.md",
    model="openai/gpt-5-mini",
    runTimeoutSeconds=300
)
```

**자동 통과 조건**:
- 4개 모두 통과 → 즉시 발행
- 1개라도 실패 → 사용자 확인 요청

### Step 8: 발행 (자동)

```python
# QA 통과 확인
qa_report = read(f"{work_dir}/qa-report.md")

if "전체 통과" in qa_report or "PASS" in qa_report:
    # 자동 발행
    scheduler_session = sessions_spawn(
        agentId="scheduler",
        task=f"스토리 발행 (Meta API 업로드).\n"
             f"입력: {work_dir}/stories/story_01.png, {work_dir}/story_caption.txt\n"
             f"출력: {work_dir}/schedule.json",
        model="openai/gpt-5-mini",
        runTimeoutSeconds=300
    )
else:
    # 사용자 확인 요청
    message = f"""
    ⚠️ 스토리 QA 이슈 발견
    
    {qa_report}
    
    그래도 발행할까요?
    """
```

---

## 📝 자동 저장 규칙

각 단계 완료 시:
1. 해당 세션의 출력 파일 확인
2. `memory/YYYY-MM-DD.md`에 진행 상황 기록
3. 사용자에게 간단히 알림

**저장 형식**:
```markdown
## 스토리 자동 생성 ({timestamp})

- 주제: {topic}
- 작업 폴더: {work_dir}
- 진행 상황:
  - [x] 프롬프트 (완료)
  - [x] 이미지 (완료)
  - [x] 캡션 (완료)
  - [x] QA (통과)
  - [x] 발행 (완료)
```

---

## ⏱️ 예상 소요 시간

| Phase | 소요 시간 |
|---|---|
| 주제 선정 | 1분 (수동) / 5분 (자동) |
| 아이템 선정 | 1분 (수동) / 5분 (자동) |
| 프롬프트 | 5분 |
| 이미지 생성 | 15분 |
| 캡션 작성 | 5분 |
| QA 검수 | 3분 |
| 발행 | 2분 |
| **총** | **약 30분** |

---

## 🔧 Cron 자동화 (매일 오전 9시)

```python
# OpenClaw cron 설정
cron(
    action="add",
    job={
        "name": "Daily Story Auto-Gen",
        "schedule": {
            "kind": "cron",
            "expr": "0 9 * * 1-5",  # 월~금 9:00
            "tz": "Asia/Seoul"
        },
        "payload": {
            "kind": "agentTurn",
            "message": "오늘의 스토리 자동 생성 (주제는 researcher가 추천)",
            "model": "claude-sonnet-4-6",
            "timeoutSeconds": 2400  # 40분
        },
        "delivery": {
            "mode": "announce",
            "channel": "telegram",
            "bestEffort": True
        },
        "sessionTarget": "isolated",
        "enabled": True
    }
)
```

---

## 🚨 에러 핸들링

### 이미지 생성 실패
- 재시도 (최대 2회)
- 다른 Gena 참조 이미지 시도
- 실패 시 → 사용자 알림

### QA 실패
- 자동 발행 중단
- 사용자 확인 요청
- 수동 승인 후 발행

### 발행 실패
- 재시도 (최대 2회)
- 로컬 저장 유지
- 나중에 재발행 가능

---

## ✅ 성공 조건

1. 이미지 1장 생성
2. QA 통과 (4개 항목)
3. Instagram Stories 발행 완료

**최종 알림**:
```
🎉 오늘의 스토리 발행 완료!

주제: {topic}
이미지: {work_dir}/stories/story_01.png

24시간 후 자동 삭제됩니다.
```

---

## 🔄 재고 연계 시나리오

### GenArchive 재고 우선

```python
# item-researcher에게 재고 우선 지시
task = """
GenArchive 재고 아이템 중에서 1개 추천.
재고 목록: [재고 파일 경로 또는 API]
조건:
- 시즌 적합성 (봄/여름/가을/겨울)
- 판매 우선순위 (세일 아이템 우선)
- Gena에게 어울림
"""
```

### 세일즈 파트너스 링크

```python
# 캡션에 링크 자동 삽입
caption = f"""
{기본_캡션}

🛒 구매하기: {sales_partners_link}
"""
```

---

**최종 업데이트**: 2026-03-06  
**담당**: 자비스 (Orchestrator)
