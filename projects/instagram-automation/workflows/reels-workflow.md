# Reels Workflow

**용도**: 릴스 콘텐츠 제작 전체 흐름  
**목표**: 트렌드 주제 → 5초 릴스 완성 → QA → 발행  
**자동화율**: 85%+

---

## 📊 전체 프로세스

```
1. 트렌드 리서치 (researcher)
   ↓
2. 아이템 리서치 (item-researcher) [병렬]
   ↓
[게이트 G1: 토픽 확정]
   ↓
3. 씬 기획 (contents-marketer)
   ↓
4. 프롬프트 생성 (prompt-engineer) [이미지 + 비디오]
   ↓
[게이트 G2: 프롬프트 검증]
   ↓
5. 키 프레임 생성 (designer) [병렬]
6. 비디오 씬 생성 (video-agent) [병렬]
   ↓
7. 자막 오버레이 (developer)
   ↓
8. QA 검수 (qa-reviewer)
   ↓
[게이트 G3: QA 통과]
   ↓
9. 스케줄링 (scheduler)
   ↓
[게이트 G4: 발행 승인]
   ↓
10. 발행 (Meta API)
```

---

## 🚀 Phase별 상세 실행

### Phase 1: 트렌드 리서치 (30분)

**담당**: researcher (sonnet-4-6)  
**스킬**: research-trend.SKILL.md

**입력**:
- 사용자 요청 (예: "봄 패션 릴스 트렌드")

**실행**:
```python
sessions_spawn(
    agentId="researcher",
    task="봄 패션 릴스 트렌드 조사 (인스타그램 Reels 중심)",
    model="claude-sonnet-4-6"
)
```

**출력**:
- `research.md` (6개 추천 토픽, 릴스 포맷 특화)

**게이트 G1: 토픽 확정**
- Orchestrator → 마보스님께 6개 토픽 제시
- 선택된 토픽으로 다음 단계 진행

---

### Phase 2: 아이템 리서치 (30분)

**담당**: item-researcher (sonnet-4-6)  
**스킬**: item-research.SKILL.md

**입력**:
- 선택된 토픽 (예: "봄 트렌치코트 착장")

**실행**:
```python
sessions_spawn(
    agentId="item-researcher",
    task="트렌치코트 착장 아이템 3개 수집 (릴스용)",
    model="claude-sonnet-4-6"
)
```

**출력**:
- `items.json` (3~5개 아이템, 릴스는 캐러셀보다 적음)

---

### Phase 3: 씬 기획 (30분)

**담당**: contents-marketer (gpt-5.2)  
**스킬**: plan-content.SKILL.md

**입력**:
- `research.md`
- `items.json`

**실행**:
```python
sessions_spawn(
    agentId="contents-marketer",
    task="릴스 씬 기획 (3~5씬, 각 씬당 1초)",
    model="openai/gpt-5.2"
)
```

**출력**:
- `plan.md` (씬별 구성, 전환 효과, BGM 제안)
- `scenes.json` (씬별 정보)

**씬 구조 예시**:
```json
{
  "scene_01": {
    "duration": 1,
    "description": "정면에서 걸어오는 Gena (트렌치코트)",
    "camera_movement": "pan_right",
    "item_ids": ["outer_001"]
  },
  "scene_02": {
    "duration": 1,
    "description": "측면 각도에서 회전 (트렌치코트 디테일)",
    "camera_movement": "rotate_left",
    "item_ids": ["outer_001"]
  },
  "scene_03": {
    "duration": 1,
    "description": "전신샷 (니트 + 트렌치코트)",
    "camera_movement": "zoom_in",
    "item_ids": ["outer_001", "top_001"]
  }
}
```

---

### Phase 4: 프롬프트 생성 (30분)

**담당**: prompt-engineer (opus-4-6)  
**스킬**: prompt-image.SKILL.md, prompt-video.SKILL.md

**입력**:
- `scenes.json`
- `items.json`
- `shared/gena-master-prompt.md`

**실행**:
```python
sessions_spawn(
    agentId="prompt-engineer",
    task="릴스 키 프레임 + 비디오 프롬프트 생성",
    model="claude-opus-4-6"
)
```

**출력**:
- `prompts.json`:
  ```json
  {
    "keyframes": {
      "frame_01": {
        "image_prompt": "...",
        "reference_images": ["gena_ref_01.png", "outer_001"]
      }
    },
    "video_prompts": {
      "scene_01": {
        "video_prompt": "A young Korean woman walks toward camera...",
        "reference_frame": "assets/reel_frame_01.png",
        "duration": 1,
        "camera_movement": "pan_right"
      }
    }
  }
  ```

**게이트 G2: 프롬프트 검증**
- 자동 검증: prompt-quality-check.SKILL.md
- 통과 → 다음 단계
- 실패 → 재생성

---

### Phase 5: 키 프레임 생성 (40분)

**담당**: designer (gpt-5-mini)  
**스킬**: design-visual.SKILL.md

**입력**:
- `prompts.json` (keyframes)
- `items.json`

**실행**:
```python
sessions_spawn(
    agentId="designer",
    task="릴스 키 프레임 생성 (Nanogen Outfit Swap)",
    model="openai/gpt-5-mini"
)
```

**내부 실행**:
```bash
python scripts/nanogen_image.py \
    --content-path content/20260306_spring_reels \
    --slide-id frame_01 \
    --aspect-ratio 9:16 \
    --resolution 2K
```

**출력**:
- `assets/reel_frame_01.png` ~ `reel_frame_05.png` (1080×1920px, 9:16)

---

### Phase 6: 비디오 씬 생성 (90분)

**담당**: video-agent (sonnet-4-6)  
**스킬**: video-nanogen-call.SKILL.md, video-ffmpeg-assemble.SKILL.md

**입력**:
- `prompts.json` (video_prompts)
- `assets/reel_frame_*.png` (키 프레임)

**실행**:
```python
sessions_spawn(
    agentId="video-agent",
    task="릴스 비디오 씬 생성 (Kling v3.0)",
    model="claude-sonnet-4-6"
)
```

**내부 실행**:
```bash
# 씬별 비디오 생성
python scripts/nanogen_video.py \
    --content-path content/20260306_spring_reels \
    --all \
    --model-id kling-v3 \
    --kling-mode standard \
    --duration 5
```

**출력**:
- `reels/scenes/scene_01.mp4` ~ `scene_05.mp4`

**모델 선택 전략**:
- **Kling v3.0 Standard**: 대부분의 씬 (빠르고 저렴)
- **Kling v3.0 Pro**: 훅 씬만 (첫 1초, 고품질)
- **Veo**: 감성 씬 (슬로우모션, 예술적 효과)

---

### Phase 7: 자막 오버레이 (30분)

**담당**: developer (sonnet-4-6)  
**스킬**: video-ffmpeg-assemble.SKILL.md

**입력**:
- `reels/scenes/*.mp4` (씬 비디오)
- `copy.md` (자막 텍스트)

**실행**:
```python
sessions_spawn(
    agentId="developer",
    task="릴스 자막 오버레이 + 씬 결합 (ffmpeg)",
    model="claude-sonnet-4-6"
)
```

**내부 실행**:
```bash
# ffmpeg로 자막 추가 + 씬 결합
ffmpeg -i scene_01.mp4 \
       -vf "drawtext=text='봄 트렌치코트':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h-100" \
       -c:v libx264 -preset fast \
       scene_01_subtitle.mp4

# 씬 결합
ffmpeg -f concat -i filelist.txt -c copy final_reel.mp4
```

**출력**:
- `reels/final_reel.mp4` (5초, 1080×1920px, 9:16)

---

### Phase 8: QA 검수 (15분)

**담당**: qa-reviewer (gpt-5-mini)  
**스킬**: qa-visual.SKILL.md

**입력**:
- `reels/final_reel.mp4`

**실행**:
```python
sessions_spawn(
    agentId="qa-reviewer",
    task="릴스 QA 검수 (비디오 품질, 자막, 타이밍)",
    model="openai/gpt-5-mini"
)
```

**검수 항목**:
- [ ] 캐릭터 일관성 (전 씬)
- [ ] 아이템 시각 정확성
- [ ] 자막 가독성
- [ ] 씬 전환 자연스러움
- [ ] 총 길이 5초 이내
- [ ] 해상도 1080×1920px
- [ ] 비율 9:16

**출력**:
- `qa-report.md`

**게이트 G3: QA 통과**
- 고/중 이슈 0건 → 통과
- 이슈 발견 → developer 수정 루프 (최대 3회)

---

### Phase 9: 스케줄링 (10분)

**담당**: scheduler (gpt-5-mini)  
**스킬**: schedule-post.SKILL.md

**입력**:
- `reels/final_reel.mp4`
- `copy.md` (캡션)
- `research.md` (해시태그)

**실행**:
```python
sessions_spawn(
    agentId="scheduler",
    task="릴스 발행 준비 (Meta API 업로드)",
    model="openai/gpt-5-mini"
)
```

**출력**:
- `schedule.json`

**게이트 G4: 발행 승인**
- Orchestrator → 마보스님께 최종 릴스 제시
- 승인 → 발행 실행

---

### Phase 10: 발행 (5분)

**담당**: scheduler (자동)

**실행**:
```python
# Meta Graph API 호출
POST /me/media
{
    "media_type": "REELS",
    "video_url": "...",
    "caption": "...",
    "share_to_feed": true
}
```

**출력**:
- Instagram Reels 발행 완료
- `performance_log.json` 업데이트

---

## ⏱️ 전체 소요 시간

| Phase | 소요 시간 |
|---|---|
| 트렌드 리서치 | 30분 |
| 아이템 리서치 | 30분 |
| 씬 기획 | 30분 |
| 프롬프트 생성 | 30분 |
| 키 프레임 생성 | 40분 |
| 비디오 씬 생성 | 90분 |
| 자막 오버레이 | 30분 |
| QA 검수 | 15분 |
| 스케줄링 | 10분 |
| 발행 | 5분 |
| **총 소요 시간** | **약 5시간** |

*(병렬 실행으로 약 3.5시간으로 단축 가능)*

---

## 🔧 병렬 실행 최적화

### 1차 병렬 (Phase 1-2)
```python
researcher_session = sessions_spawn(agentId="researcher", ...)
item_researcher_session = sessions_spawn(agentId="item-researcher", ...)
wait_for_completion([researcher_session, item_researcher_session])
```

### 2차 병렬 (Phase 5-6)
```python
# 키 프레임 생성 후 바로 비디오 생성 시작
# (키 프레임이 완료되는 대로 순차 비디오 생성)
designer_session = sessions_spawn(agentId="designer", ...)
video_agent_session = sessions_spawn(agentId="video-agent", ...)
```

---

## 📂 최종 산출물 구조

```
content/20260306_spring_reels/
├── research.md
├── items.json
├── scenes.json               # contents-marketer 씬 기획
├── prompts.json              # keyframes + video_prompts
├── plan.md
├── copy.md
├── assets/
│   ├── reel_frame_01.png
│   └── ... (5개)
├── reels/
│   ├── scenes/
│   │   ├── scene_01.mp4
│   │   └── ... (5개)
│   └── final_reel.mp4        # 최종 결과물
├── qa-report.md
├── schedule.json
└── performance_log.json
```

---

## 🎥 Nanogen 모델 선택 가이드

### Kling v3.0 Standard
- **용도**: 일반 씬 (걷기, 회전, 포즈)
- **비용**: ~$0.3/씬
- **속도**: 약 15분/씬
- **품질**: 균형

### Kling v3.0 Pro
- **용도**: 훅 씬 (첫 1초, 임팩트 필요)
- **비용**: ~$1.5/씬
- **속도**: 약 30분/씬
- **품질**: 최고

### Veo
- **용도**: 감성 씬 (슬로우모션, 예술적)
- **비용**: 측정 필요
- **속도**: 약 20분/씬
- **품질**: 슬로우모션 강점

---

## 🚨 릴스 특화 주의사항

### 1. 캐릭터 일관성 (최우선)
- 전 씬에서 동일 Gena 참조 이미지 사용
- 씬별 프롬프트에 동일한 캐릭터 디스크립션 포함

### 2. 타이밍
- 총 길이 5초 엄수
- 씬당 1~2초 (너무 짧으면 어지러움)

### 3. 자막
- 1줄 최대 20자
- 화면 하단 1/5 영역
- 고대비 (흰색 텍스트 + 검은색 아웃라인)

### 4. 해상도
- 반드시 9:16 (1080×1920px)
- Instagram Reels 최적화

---

**최종 업데이트**: 2026-03-06 04:17  
**프로젝트**: @gena_feed Instagram 자동화  
**담당**: 자비스 (OpenClaw orchestrator)
