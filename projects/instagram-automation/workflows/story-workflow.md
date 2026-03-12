# Story Workflow

**용도**: 스토리 콘텐츠 제작 전체 흐름  
**목표**: 트렌드/일상 주제 → 1장 스토리 완성 → 발행 (QA 간소화)  
**자동화율**: 95%+

---

## 📊 전체 프로세스

```
1. 주제 선정 (researcher 또는 수동)
   ↓
2. 아이템 선정 (1개, item-researcher 또는 수동)
   ↓
3. 프롬프트 생성 (prompt-engineer)
   ↓
4. 이미지 생성 (designer)
   ↓
5. 캡션 작성 (contents-marketer)
   ↓
6. 간소화 QA (qa-reviewer, 자동)
   ↓
7. 발행 (scheduler, 자동)
```

---

## 🚀 Phase별 상세 실행

### Phase 1: 주제 선정 (5분)

**담당**: researcher (선택) 또는 수동 입력

**자동 모드**:
```python
# 매일 오전 9시 자동 실행 (cron)
sessions_spawn(
    agentId="researcher",
    task="오늘의 스토리 주제 추천 (간단한 일상/트렌드 1개)",
    model="claude-sonnet-4-6"
)
```

**수동 모드**:
- 마보스님 직접 입력 (예: "오늘의 봄 재킷")

**출력**:
- `story_topic.txt` (주제 1줄)

---

### Phase 2: 아이템 선정 (5분)

**담당**: item-researcher (선택) 또는 수동

**자동 모드**:
```python
sessions_spawn(
    agentId="item-researcher",
    task="'{주제}' 관련 아이템 1개 추천",
    model="claude-sonnet-4-6"
)
```

**수동 모드**:
- 재고 아이템 직접 선택

**출력**:
- `story_item.json` (아이템 1개)

---

### Phase 3: 프롬프트 생성 (5분)

**담당**: prompt-engineer (opus-4-6)  
**스킬**: prompt-image.SKILL.md

**입력**:
- `story_topic.txt`
- `story_item.json`
- `shared/gena-master-prompt.md`

**실행**:
```python
sessions_spawn(
    agentId="prompt-engineer",
    task="스토리 이미지 프롬프트 1개 생성",
    model="claude-opus-4-6"
)
```

**출력**:
- `story_prompt.json`:
  ```json
  {
    "image_prompt": "A young Korean woman...",
    "reference_images": ["gena_ref_02.png", "jacket_001"]
  }
  ```

---

### Phase 4: 이미지 생성 (15분)

**담당**: designer (gpt-5-mini)  
**스킬**: design-visual.SKILL.md

**입력**:
- `story_prompt.json`
- `story_item.json`

**실행**:
```python
sessions_spawn(
    agentId="designer",
    task="스토리 이미지 1장 생성 (Nanogen Outfit Swap)",
    model="openai/gpt-5-mini"
)
```

**내부 실행**:
```bash
python scripts/nanogen_image.py \
    --content-path content/20260306_story \
    --slide-id story_01 \
    --aspect-ratio 9:16 \
    --resolution 2K
```

**출력**:
- `stories/story_01.png` (1080×1920px, 9:16)

---

### Phase 5: 캡션 작성 (5분)

**담당**: contents-marketer (gpt-5.2)  
**스킬**: write-copy.SKILL.md

**입력**:
- `story_topic.txt`
- `story_item.json`
- `stories/story_01.png`

**실행**:
```python
sessions_spawn(
    agentId="contents-marketer",
    task="스토리 캡션 작성 (짧고 감성적, 1~2줄)",
    model="openai/gpt-5.2"
)
```

**출력**:
- `story_caption.txt`:
  ```
  봄이 오는 소리 🌸
  #봄재킷 #데일리룩
  ```

---

### Phase 6: 간소화 QA (자동, 3분)

**담당**: qa-reviewer (gpt-5-mini)  
**스킬**: qa-visual.SKILL.md (간소화 버전)

**입력**:
- `stories/story_01.png`
- `story_item.json`

**검수 항목** (스토리용 간소화):
- [ ] 캐릭터 일관성 (Gena 맞음)
- [ ] 아이템 시각 정확성 (색상/스타일 일치)
- [ ] 해상도 1080×1920px
- [ ] 비율 9:16

**출력**:
- `qa-report.md` (간단한 통과/실패)

**자동 통과 조건**:
- 4개 항목 모두 통과 → 즉시 발행
- 1개라도 실패 → Orchestrator 알림 (수동 확인)

---

### Phase 7: 발행 (자동, 2분)

**담당**: scheduler (gpt-5-mini)  
**스킬**: schedule-post.SKILL.md

**입력**:
- `stories/story_01.png`
- `story_caption.txt`

**실행**:
```python
# 자동 발행 (QA 통과 시)
POST /me/media
{
    "media_type": "STORIES",
    "image_url": "...",
    "caption": "..."
}
```

**출력**:
- Instagram Stories 발행 완료
- `performance_log.json` 업데이트

---

## ⏱️ 전체 소요 시간

| Phase | 소요 시간 |
|---|---|
| 주제 선정 | 5분 (자동) / 1분 (수동) |
| 아이템 선정 | 5분 (자동) / 1분 (수동) |
| 프롬프트 생성 | 5분 |
| 이미지 생성 | 15분 |
| 캡션 작성 | 5분 |
| 간소화 QA | 3분 (자동) |
| 발행 | 2분 (자동) |
| **총 소요 시간** | **약 35분 (자동) / 30분 (수동)** |

---

## 🔧 Cron 자동화 (주 5회)

### 매일 오전 9시 자동 실행

```yaml
# OpenClaw cron 설정
schedule:
  kind: cron
  expr: "0 9 * * 1-5"  # 월~금 오전 9시
  tz: "Asia/Seoul"

payload:
  kind: agentTurn
  message: "오늘의 스토리 생성 (story-workflow)"

sessionTarget: isolated
delivery:
  mode: announce  # 완료 후 마보스님께 알림
```

---

## 📂 최종 산출물 구조

```
content/20260306_story/
├── story_topic.txt           # 주제
├── story_item.json           # 아이템 1개
├── story_prompt.json         # 프롬프트
├── story_caption.txt         # 캡션
├── stories/
│   └── story_01.png          # 최종 이미지
├── qa-report.md              # 간소화 QA
└── performance_log.json
```

---

## 🎯 스토리 특화 전략

### 1. 간소화된 프로세스
- 캐러셀/릴스보다 훨씬 단순
- QA 간소화 (4개 항목만)
- 수동 개입 최소화

### 2. 빠른 제작
- 총 30분 이내
- 매일 오전 9시 자동 실행 가능

### 3. 재고 연계
- GenArchive 재고 아이템 우선 노출
- 세일즈 파트너스 링크 삽입

### 4. 일관된 톤앤매너
- Gena 캐릭터 일관성 유지
- 감성적이고 간결한 캡션

---

## 🚨 스토리 특화 주의사항

### 1. 해상도
- 반드시 9:16 (1080×1920px)
- Instagram Stories 최적화

### 2. 24시간 제한
- 스토리는 24시간 후 자동 삭제
- 중요 콘텐츠는 하이라이트 저장

### 3. 링크 활용
- 세일즈 파트너스 링크 삽입 (스와이프 업)
- 재고 제품 페이지 연결

### 4. 일일 1회 원칙
- 너무 많으면 팔로워 피로도 증가
- 주 5회 (월~금) 권장

---

## 📊 성과 측정

### 주간 리포트 (매주 월요일)
```python
# scheduler가 자동 생성
weekly_stories_report = {
    "week": "2026-03-03 ~ 2026-03-09",
    "total_stories": 5,
    "avg_views": 850,
    "avg_reach": 720,
    "link_clicks": 42,
    "top_performing": "story_20260306"
}
```

---

## 🔄 자동화 시나리오

### 완전 자동 모드
```
[Cron 9:00 AM] → researcher → item-researcher → prompt-engineer 
→ designer → contents-marketer → qa-reviewer → scheduler → 발행 완료
→ [Telegram 알림] "오늘의 스토리 발행 완료! 👗"
```

### 반자동 모드 (마보스님 선택)
```
[마보스님] "재고 아이템 XYZ로 스토리 만들어줘"
→ prompt-engineer → designer → contents-marketer → qa-reviewer → scheduler
→ [Telegram 알림] "스토리 준비 완료! 발행할까요?"
→ [마보스님] "발행"
→ 발행 완료
```

---

**최종 업데이트**: 2026-03-06 04:18  
**프로젝트**: @gena_feed Instagram 자동화  
**담당**: 자비스 (OpenClaw orchestrator)
