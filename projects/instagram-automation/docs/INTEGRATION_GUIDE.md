# 통합 가이드 - 인스타 자동화 시스템

**전체 시스템을 처음부터 설정하고 실행하는 완전 가이드**

---

## 📋 목차

1. [사전 준비](#1-사전-준비)
2. [환경 설정](#2-환경-설정)
3. [Meta API 설정](#3-meta-api-설정)
4. [첫 캐러셀 생성 테스트](#4-첫-캐러셀-생성-테스트)
5. [자동 스케줄링 설정](#5-자동-스케줄링-설정)
6. [모니터링 및 유지보수](#6-모니터링-및-유지보수)

---

## 1. 사전 준비

### 필수 계정
- ✅ Instagram Business 계정 (@gena_feed)
- ✅ Facebook Page (Instagram 연결)
- ✅ Meta for Developers 계정
- ✅ Imgur 계정 (이미지 호스팅)
- ✅ OpenClaw 설치 및 실행 중

### 필수 소프트웨어
- Python 3.9+
- FFmpeg (`brew install ffmpeg`)
- Node.js 18+ (OpenClaw 실행용)
- Git

### 프로젝트 폴더 확인
```bash
cd /Users/master/.openclaw/workspace/projects/instagram-automation
ls -la

# 필수 폴더/파일:
# - agents/          (9개 에이전트)
# - skills/          (15개 스킬)
# - scripts/         (API, Nanogen, FFmpeg 스크립트)
# - shared/          (Gena 참조 이미지, 디자인 시스템)
# - workflows/       (캐러셀, 릴스, 스토리)
# - .env.example     (환경 변수 템플릿)
```

---

## 2. 환경 설정

### Step 1: Python 패키지 설치

```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
python-dotenv
requests
pillow
```

### Step 2: .env 파일 생성

```bash
cp .env.example .env
nano .env
```

**.env 내용**:
```env
# Instagram Graph API
INSTAGRAM_ACCESS_TOKEN=YOUR_LONG_LIVED_TOKEN
INSTAGRAM_ACCOUNT_ID=17841XXXXXXXXX

# Meta App
META_APP_ID=YOUR_APP_ID
META_APP_SECRET=YOUR_APP_SECRET

# Imgur (이미지 호스팅)
IMGUR_CLIENT_ID=YOUR_IMGUR_CLIENT_ID

# Nanogen (비디오/이미지 생성)
NANOGEN_API_URL=http://localhost:8000
NANOGEN_API_KEY=YOUR_NANOGEN_KEY
```

### Step 3: 권한 확인

```bash
# 스크립트 실행 권한
chmod +x scripts/*.py

# FFmpeg 설치 확인
ffmpeg -version

# Python 환경 확인
python --version
```

---

## 3. Meta API 설정

**상세 가이드**: `docs/meta-api-setup.md` 참조

### 빠른 설정

1. **Meta for Developers App 생성**
   - https://developers.facebook.com/
   - "Create App" → "Business" → "Instagram Graph API" 추가

2. **Access Token 발급**
   ```bash
   # Graph API Explorer에서 User Access Token 발급
   # 권한: instagram_basic, instagram_content_publish, pages_read_engagement
   
   # Long-Lived Token으로 변환
   curl -X GET "https://graph.facebook.com/v21.0/oauth/access_token" \
     -d "grant_type=fb_exchange_token" \
     -d "client_id=YOUR_APP_ID" \
     -d "client_secret=YOUR_APP_SECRET" \
     -d "fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
   ```

3. **Instagram Account ID 확인**
   ```bash
   # Page ID 조회
   curl -X GET "https://graph.facebook.com/v21.0/me/accounts" \
     -d "access_token=YOUR_ACCESS_TOKEN"
   
   # Instagram Business Account ID 조회
   curl -X GET "https://graph.facebook.com/v21.0/PAGE_ID" \
     -d "fields=instagram_business_account" \
     -d "access_token=YOUR_ACCESS_TOKEN"
   ```

4. **.env 업데이트**
   - `INSTAGRAM_ACCESS_TOKEN` 추가
   - `INSTAGRAM_ACCOUNT_ID` 추가

5. **연결 테스트**
   ```bash
   python scripts/instagram_api.py recent
   
   # 출력 예시:
   # [
   #   {
   #     "id": "17891...",
   #     "media_type": "CAROUSEL_ALBUM",
   #     "caption": "...",
   #     "timestamp": "..."
   #   }
   # ]
   ```

---

## 4. 첫 캐러셀 생성 테스트

### Step 1: Gena 참조 이미지 확인

```bash
ls -la shared/gena-references/

# 8개 헤어스타일 참조 이미지 확인
# gena_ref_01.png ~ gena_ref_08.png
```

### Step 2: 수동 캐러셀 생성 (E2E 테스트)

**OpenClaw 메인 세션에서 실행**:

```
자비스, 인스타 캐러셀 만들어줘. 주제: "봄 트렌치코트 코디"
```

**자비스 자동 실행 흐름**:
1. orchestrate-carousel.SKILL.md 읽기
2. researcher + item-researcher 병렬 실행
3. 토픽 확정 (마보스님 선택)
4. prompt-engineer 실행
5. contents-marketer + designer 병렬 실행
6. developer (HTML 슬라이드)
7. qa-reviewer (자동 검수)
8. scheduler (Imgur 업로드 + Instagram 발행)

**예상 소요 시간**: 약 2.5시간

### Step 3: 수동 발행 테스트 (API만)

이미지가 준비되어 있다면:

```bash
# 1. 이미지를 Imgur에 업로드
python scripts/imgur_uploader.py \
  content/20260306_spring_outfits/slides/slide_*.png \
  --output urls.txt

# 2. Instagram에 발행
python scripts/instagram_api.py publish-carousel \
  --images $(cat urls.txt) \
  --caption "봄 트렌치코트 코디 🌸 #봄패션 #트렌치코트 #데일리룩"
```

---

## 5. 자동 스케줄링 설정

### Step 1: Cron Jobs 생성

```bash
python scripts/setup_cron_jobs.py --schedule-type weekly --output cron_jobs.json
```

**생성된 스케줄**:
- 월요일 10:00 - 캐러셀
- 화요일 15:00 - 릴스
- 수요일 10:00 - 캐러셀
- 목요일 15:00 - 릴스
- 금요일 10:00 - 캐러셀

### Step 2: OpenClaw에 등록

**OpenClaw 메인 세션에서**:

```python
# cron_jobs.json 읽기
import json
with open('cron_jobs.json') as f:
    jobs = json.load(f)

# 각 job 등록
for job in jobs:
    cron(action='add', job=job)

# 등록 확인
cron(action='list')
```

### Step 3: 자동 실행 확인

첫 실행까지 기다리거나, 수동 트리거:

```python
# 특정 job 즉시 실행 (테스트용)
cron(action='run', jobId='JOB_ID_HERE', runMode='force')
```

---

## 6. 모니터링 및 유지보수

### 일일 점검

**OpenClaw 세션에서**:
```
자비스, 인스타 성과 확인해줘
```

**또는 직접**:
```bash
python scripts/instagram_api.py insights
```

### 주간 점검

1. **성과 분석**
   - Engagement Rate 확인
   - 상위 20% 콘텐츠 패턴 분석

2. **토큰 유효성**
   ```bash
   python scripts/instagram_api.py recent
   
   # HTTP 401 발생 시 → 토큰 갱신 필요
   ```

3. **Cron Jobs 상태**
   ```python
   cron(action='list', includeDisabled=True)
   ```

### 월간 점검

1. **Access Token 갱신** (50일마다)
   - Meta Graph API Explorer에서 재발급
   - .env 업데이트
   - OpenClaw 재시작

2. **성과 리포트**
   - 월간 Impressions, Reach, Engagement 집계
   - 개선점 도출

3. **Gena 참조 이미지 업데이트** (필요 시)
   - 새 헤어스타일, 시즌 업데이트

---

## 🚨 트러블슈팅

### 문제 1: Instagram API 401 Unauthorized

**원인**: Access Token 만료

**해결**:
```bash
# 1. 새 토큰 발급 (meta-api-setup.md 참조)
# 2. .env 업데이트
# 3. 테스트
python scripts/instagram_api.py recent
```

### 문제 2: 이미지 업로드 실패 (Imgur 403)

**원인**: Imgur Client ID 문제

**해결**:
1. https://api.imgur.com/oauth2/addclient 재확인
2. .env에 `IMGUR_CLIENT_ID` 업데이트
3. 재시도

### 문제 3: Nanogen 비디오 생성 타임아웃

**원인**: 비디오 생성 시간 초과 (>5분)

**해결**:
```bash
# 폴링 타임아웃 증가
python scripts/nanogen_video.py \
  --content-path ... \
  --poll-timeout 600  # 10분
```

### 문제 4: FFmpeg 자막 깨짐

**원인**: 폰트 파일 문제

**해결**:
```bash
# 시스템 폰트 확인
fc-list | grep -i arial

# 폰트 파일 지정
python scripts/ffmpeg_assemble_reels.py \
  --content-path ... \
  --font-file /System/Library/Fonts/Supplemental/Arial.ttf
```

---

## ✅ 체크리스트

### 초기 설정
- [ ] Python 패키지 설치
- [ ] .env 파일 설정
- [ ] Meta API Access Token 발급
- [ ] Instagram Account ID 확인
- [ ] Imgur Client ID 발급
- [ ] API 연결 테스트 성공

### 첫 실행
- [ ] Gena 참조 이미지 확인
- [ ] 첫 캐러셀 수동 생성 성공
- [ ] Instagram 발행 성공
- [ ] 성과 조회 성공

### 자동화
- [ ] Cron Jobs 등록
- [ ] 자동 생성 테스트 (1주)
- [ ] 성과 모니터링 설정
- [ ] 토큰 갱신 알림 설정

---

## 📚 참고 문서

- **Meta API 설정**: `docs/meta-api-setup.md`
- **워크플로우**: `workflows/*.md`
- **에이전트 설명**: `agents/*.md`
- **스킬 상세**: `skills/*.SKILL.md`

---

**최종 업데이트**: 2026-03-06  
**작성**: 자비스  
**프로젝트**: @gena_feed Instagram 자동화
