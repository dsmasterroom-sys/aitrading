# schedule-post.SKILL.md

**용도**: Instagram 발행 예약 및 성과 수집  
**사용 에이전트**: scheduler  
**버전**: 1.0

---

## 📥 입력

- QA 통과 콘텐츠 (slides/ or reels/)
- copy.md (캡션용)
- research.md (해시태그)

---

## 📤 출력

- schedule.json (발행 예약 정보)
- performance_log.json (성과 데이터)

---

## 🔧 Meta Business API 발행

### 캐러셀 발행
```python
import requests

# 1. 미디어 컨테이너 생성 (슬라이드별)
containers = []
for slide_png in slides:
    response = requests.post(
        f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
        data={
            "image_url": upload_to_temp_host(slide_png),
            "is_carousel_item": True,
            "access_token": ACCESS_TOKEN
        }
    )
    containers.append(response.json()["id"])

# 2. 캐러셀 컨테이너 생성
carousel_response = requests.post(
    f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
    data={
        "media_type": "CAROUSEL",
        "children": ",".join(containers),
        "caption": caption + "\n\n" + hashtags,
        "access_token": ACCESS_TOKEN
    }
)

# 3. 발행
publish_response = requests.post(
    f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish",
    data={
        "creation_id": carousel_response.json()["id"],
        "access_token": ACCESS_TOKEN
    }
)
```

### 릴스 발행
```python
response = requests.post(
    f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
    data={
        "media_type": "REELS",
        "video_url": upload_to_temp_host(reel_mp4),
        "caption": caption + "\n\n" + hashtags,
        "share_to_feed": True,
        "access_token": ACCESS_TOKEN
    }
)
```

---

## 📅 최적 시간 계산

### 초기 고정 시간
**릴스**: 평일 오전 7:30 / 저녁 8:00  
**캐러셀**: 토요일 오전 9:00  
**스토리**: 릴스 발행 10분 후 자동

### Insights 기반 동적 최적화 (팔로워 500+)
```python
# 팔로워 활성 시간 조회
response = requests.get(
    f"https://graph.facebook.com/v18.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/insights",
    params={
        "metric": "follower_demographics",
        "period": "lifetime",
        "access_token": ACCESS_TOKEN
    }
)

# 상위 활성 시간대 추출
active_hours = analyze_peak_hours(response.json())
optimal_time = active_hours[0]  # 최상위 시간
```

---

## 📊 성과 수집 (24시간 후)

### 수집 지표
```python
response = requests.get(
    f"https://graph.facebook.com/v18.0/{MEDIA_ID}/insights",
    params={
        "metric": "impressions,reach,saves,engagement",
        "access_token": ACCESS_TOKEN
    }
)

performance = {
    "media_id": MEDIA_ID,
    "published_at": timestamp,
    "impressions": response.json()["impressions"],
    "reach": response.json()["reach"],
    "saves": response.json()["saves"],
    "engagement": response.json()["engagement"],
    "save_rate": saves / reach * 100
}
```

### performance_log.json 누적
```json
{
  "20260306_carousel_01": {
    "impressions": 1250,
    "reach": 980,
    "saves": 87,
    "save_rate": 8.9
  }
}
```

---

## 🔄 피드백 루프 (주 1회)

### 상위 20% 콘텐츠 패턴 분석
```python
# save_rate 기준 상위 20% 추출
sorted_logs = sorted(performance_log, key=lambda x: x["save_rate"], reverse=True)
top_20_percent = sorted_logs[:len(sorted_logs)//5]

# 패턴 추출
patterns = {
    "topics": extract_topics(top_20_percent),
    "hashtags": extract_hashtags(top_20_percent),
    "posting_times": extract_times(top_20_percent)
}
```

### research.md 업데이트
- 성공 토픽 → 다음 주 우선 순위
- 실패 토픽 → 제외 또는 변형

---

## ✅ 검증

### [ ] Meta API 토큰 유효
### [ ] 미디어 URL HTTPS
### [ ] 캡션 2200자 이내
### [ ] 해시태그 30개 이내

---

**최종 업데이트**: 2026-03-06 04:03
