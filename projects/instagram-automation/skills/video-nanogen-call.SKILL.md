# video-nanogen-call.SKILL.md

**용도**: Nanogen Video API 호출 규칙  
**사용 에이전트**: video-agent  
**버전**: 1.0

---

## 📥 입력

- prompts.json (video_prompts)
- assets/reel_frames/ (키 프레임 이미지)

---

## 📤 출력

- reels/scenes/{scene_id}.mp4

---

## 🔧 API 호출

### Kling v3.0 (메인)
```python
import requests

response = requests.post(
    "http://localhost:8000/api/generate-video",
    json={
        "prompt": prompts["scene_01"]["video_prompt"],
        "config": {
            "modelId": "kling-v3",
            "klingMode": "standard",  # or "pro"
            "durationSeconds": 5,
            "cameraMovement": "pan_right"
        },
        "referenceImages": [gena_frame_base64]
    }
)
```

### 모델 선택

**Kling v3.0 Standard** (기본):
- 비용: ~$0.3/씬
- 품질: 균형
- 속도: 중간

**Kling v3.0 Pro** (훅 씬만):
- 비용: ~$1.5/씬
- 품질: 최고
- 속도: 느림

**Veo** (감성 씬):
- 비용: 측정 필요
- 품질: 슬로우모션 강점
- 속도: 느림

---

## ⏱️ 폴링 처리

생성 완료 대기:
```python
import time

job_id = response.json()["jobId"]
max_wait = 300  # 5분

for i in range(max_wait // 5):
    status_response = requests.get(
        f"http://localhost:8000/api/video-status/{job_id}"
    )
    
    if status_response.json()["status"] == "completed":
        video_url = status_response.json()["url"]
        break
    
    time.sleep(5)
```

---

## ✅ 검증

### [ ] durationSeconds: 5초
### [ ] 카메라 무브먼트 유효
### [ ] 폴링 타임아웃 설정
### [ ] 에러 핸들링

---

**최종 업데이트**: 2026-03-06 04:00
