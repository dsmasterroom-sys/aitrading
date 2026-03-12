# Meta (Instagram) Graph API 설정 가이드

**목표**: Instagram Business 계정에서 캐러셀/릴스 자동 발행

---

## 📋 사전 요구사항

1. **Instagram Business 계정** (또는 Creator 계정)
2. **Facebook Page** (Instagram과 연결)
3. **Meta for Developers 계정**

---

## 🚀 설정 단계

### Step 1: Meta for Developers App 생성

1. https://developers.facebook.com/ 접속
2. 우측 상단 "My Apps" → "Create App" 클릭
3. **Use case**: "Other" 선택 → "Next"
4. **App type**: "Business" 선택 → "Next"
5. **App details**:
   - App name: `Gena Feed Automation`
   - App contact email: (본인 이메일)
   - "Create app" 클릭

### Step 2: Instagram Graph API 추가

1. App Dashboard → "Add products" 섹션
2. **Instagram Graph API** 찾아서 "Set up" 클릭
3. Basic Settings에서 App ID, App Secret 확인 (나중에 사용)

### Step 3: Facebook Page 연결

1. App Dashboard 좌측 메뉴 → "Settings" → "Basic"
2. **App Domains**에 도메인 추가 (예: `localhost`, `yourdomain.com`)
3. "Save Changes"

### Step 4: Access Token 발급

#### 방법 A: Graph API Explorer (빠른 테스트)

1. https://developers.facebook.com/tools/explorer/ 접속
2. 상단 드롭다운에서 본인 App 선택
3. **User or Page** → "Get User Access Token" 클릭
4. 권한 선택:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
   - `pages_show_list`
5. "Generate Access Token" 클릭 → 로그인 및 권한 승인
6. 생성된 토큰 복사 (임시 토큰, 1-2시간 유효)

#### 방법 B: Long-Lived Token (권장)

임시 토큰을 장기 토큰으로 변환:

```bash
curl -X GET "https://graph.facebook.com/v21.0/oauth/access_token" \
  -d "grant_type=fb_exchange_token" \
  -d "client_id=YOUR_APP_ID" \
  -d "client_secret=YOUR_APP_SECRET" \
  -d "fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
```

응답:
```json
{
  "access_token": "LONG_LIVED_TOKEN",
  "token_type": "bearer",
  "expires_in": 5183944  // 약 60일
}
```

### Step 5: Instagram Account ID 확인

```bash
curl -X GET "https://graph.facebook.com/v21.0/me/accounts" \
  -d "access_token=YOUR_ACCESS_TOKEN"
```

응답에서 `id` (Facebook Page ID) 확인.

그 다음 Instagram Business Account ID 확인:

```bash
curl -X GET "https://graph.facebook.com/v21.0/PAGE_ID" \
  -d "fields=instagram_business_account" \
  -d "access_token=YOUR_ACCESS_TOKEN"
```

응답:
```json
{
  "instagram_business_account": {
    "id": "17841XXXXXXXXX"  // 이게 Instagram Account ID
  },
  "id": "PAGE_ID"
}
```

### Step 6: .env 파일 설정

프로젝트 루트에 `.env` 파일 생성:

```env
# Instagram Graph API
INSTAGRAM_ACCESS_TOKEN=YOUR_LONG_LIVED_ACCESS_TOKEN
INSTAGRAM_ACCOUNT_ID=17841XXXXXXXXX

# Meta App (선택)
META_APP_ID=YOUR_APP_ID
META_APP_SECRET=YOUR_APP_SECRET
```

---

## 🧪 테스트

### 1. API 연결 테스트

```bash
cd /Users/master/.openclaw/workspace/projects/instagram-automation

python scripts/instagram_api.py recent
```

출력 예시:
```json
[
  {
    "id": "17891...",
    "media_type": "CAROUSEL_ALBUM",
    "caption": "봄 패션 트렌드 🌸",
    "timestamp": "2026-03-06T05:00:00+0000"
  }
]
```

### 2. 캐러셀 발행 테스트

**주의**: 이미지 URL은 **공개 접근 가능**해야 합니다!

```bash
python scripts/instagram_api.py publish-carousel \
  --images \
    "https://example.com/slide1.png" \
    "https://example.com/slide2.png" \
    "https://example.com/slide3.png" \
  --caption "테스트 캐러셀 🎨 #테스트 #자동화"
```

---

## 🔐 권한 (Permissions)

필수 권한:
- `instagram_basic`: 기본 계정 정보
- `instagram_content_publish`: 콘텐츠 발행
- `pages_read_engagement`: 성과 조회
- `pages_show_list`: 페이지 목록 조회

추가 권한 (Insights용):
- `instagram_manage_insights`: 상세 성과 조회

---

## 🚨 주의사항

### 1. 이미지 URL 요구사항

Instagram Graph API는 **공개 URL**만 허용합니다:
- ✅ `https://yourdomain.com/images/slide1.png`
- ✅ `https://storage.googleapis.com/...`
- ✅ `https://s3.amazonaws.com/...`
- ❌ `http://localhost/...`
- ❌ 로컬 파일 경로

**해결 방법**:
1. 임시 공개 스토리지 사용 (S3, GCS, Cloudflare R2)
2. 또는 ngrok 등으로 로컬 서버 임시 공개
3. 또는 Imgur API 등 이미지 호스팅 서비스

### 2. Rate Limits

Instagram Graph API는 **시간당 200 calls** 제한이 있습니다.
- 1개 캐러셀 = 약 12 calls (10 images + 1 carousel + 1 publish)
- 시간당 약 16개 캐러셀 발행 가능

### 3. 비디오 처리 시간

릴스(비디오)는 처리 시간이 오래 걸립니다:
- 짧은 영상 (15초): 1-2분
- 긴 영상 (90초): 5-10분

### 4. Token 만료

Long-Lived Token도 60일 후 만료됩니다.
- 자동 갱신 로직 구현 권장
- 또는 매달 수동 재발급

---

## 📊 성과 조회 (Insights)

### 미디어별 성과

```bash
python scripts/instagram_api.py insights --media-id 17891XXXXX
```

출력:
```json
{
  "data": [
    {"name": "impressions", "values": [{"value": 1234}]},
    {"name": "reach", "values": [{"value": 987}]},
    {"name": "likes", "values": [{"value": 45}]},
    {"name": "comments", "values": [{"value": 3}]},
    {"name": "saves", "values": [{"value": 12}]}
  ]
}
```

### 계정 전체 성과

```bash
python scripts/instagram_api.py insights
```

---

## 🔄 자동 갱신 (Token Refresh)

60일마다 토큰을 자동으로 갱신하려면:

```python
import requests

def refresh_access_token(current_token, app_id, app_secret):
    """Access Token 갱신"""
    url = "https://graph.facebook.com/v21.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": current_token
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data["access_token"]
```

**OpenClaw Cron으로 자동 갱신**:

```python
# 50일마다 실행
cron(
    action="add",
    job={
        "name": "Instagram Token Refresh",
        "schedule": {"kind": "every", "everyMs": 50 * 24 * 60 * 60 * 1000},
        "payload": {"kind": "systemEvent", "text": "Instagram Access Token 갱신 필요"},
        "sessionTarget": "main"
    }
)
```

---

## 📚 참고 자료

- [Instagram Graph API 공식 문서](https://developers.facebook.com/docs/instagram-api/)
- [Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [Insights](https://developers.facebook.com/docs/instagram-api/guides/insights)
- [Rate Limits](https://developers.facebook.com/docs/graph-api/overview/rate-limiting/)

---

## ✅ 체크리스트

설정 완료 확인:

- [ ] Meta for Developers App 생성
- [ ] Instagram Graph API 추가
- [ ] Facebook Page 연결
- [ ] Access Token 발급 (Long-Lived)
- [ ] Instagram Account ID 확인
- [ ] .env 파일 설정
- [ ] `python scripts/instagram_api.py recent` 성공
- [ ] 테스트 캐러셀 발행 성공

**모두 완료되면 자동화 시스템 준비 완료!** 🎉

---

**최종 업데이트**: 2026-03-06  
**담당**: 자비스
