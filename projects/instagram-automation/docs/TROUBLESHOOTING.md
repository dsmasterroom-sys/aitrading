# 트러블슈팅 가이드

**인스타 자동화 시스템 문제 해결**

---

## 📋 목차

1. [Meta API 관련](#1-meta-api-관련)
2. [이미지 생성 (Nanogen)](#2-이미지-생성-nanogen)
3. [비디오 생성 (Nanogen Video)](#3-비디오-생성-nanogen-video)
4. [FFmpeg 관련](#4-ffmpeg-관련)
5. [OpenClaw 에이전트](#5-openclaw-에이전트)
6. [Cron 자동화](#6-cron-자동화)

---

## 1. Meta API 관련

### 🔴 401 Unauthorized

**증상**:
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
```

**원인**:
- Access Token 만료 (60일)
- 권한 부족
- Facebook Page 연결 해제

**해결**:
```bash
# 1. 토큰 유효성 확인
curl "https://graph.facebook.com/v21.0/me?access_token=YOUR_TOKEN"

# 2. 새 토큰 발급
# Meta Graph API Explorer → Generate Access Token
# 권한: instagram_basic, instagram_content_publish

# 3. Long-Lived Token으로 변환
curl -X GET "https://graph.facebook.com/v21.0/oauth/access_token" \
  -d "grant_type=fb_exchange_token" \
  -d "client_id=APP_ID" \
  -d "client_secret=APP_SECRET" \
  -d "fb_exchange_token=SHORT_LIVED_TOKEN"

# 4. .env 업데이트
nano .env
# INSTAGRAM_ACCESS_TOKEN=NEW_TOKEN

# 5. 테스트
python scripts/instagram_api.py recent
```

---

### 🔴 429 Too Many Requests (Rate Limit)

**증상**:
```
requests.exceptions.HTTPError: 429 Client Error: Too Many Requests
```

**원인**:
- Instagram Graph API Rate Limit 초과 (시간당 200 calls)

**해결**:
```python
# 즉시: 1시간 대기
time.sleep(3600)

# 장기: 요청 간격 증가
# instagram_api.py에서 time.sleep(0.5) → time.sleep(2)

# Cron: 빈도 감소
# 주 5회 → 주 3회
```

**예방**:
- 캐러셀당 약 12 calls 소요
- 시간당 최대 16개 캐러셀 발행 가능
- 여유롭게 시간당 10개 이하로 제한

---

### 🔴 이미지 URL 접근 불가

**증상**:
```
{"error": {"message": "Image URL is not accessible"}}
```

**원인**:
- 공개 URL이 아님 (localhost, 로컬 파일)
- URL 만료 (Imgur 등)

**해결**:
```bash
# 1. Imgur에 재업로드
python scripts/imgur_uploader.py \
  slides/slide_01.png \
  --output url.txt

# 2. URL 공개 접근 확인
curl -I "$(cat url.txt)"
# HTTP/1.1 200 OK 확인

# 3. 재발행
python scripts/instagram_api.py publish-carousel \
  --images "$(cat url.txt)" \
  --caption "..."
```

**대안**:
- S3, Cloudflare R2 등 영구 스토리지 사용
- ngrok으로 로컬 서버 임시 공개

---

## 2. 이미지 생성 (Nanogen)

### 🔴 캐릭터 불일치

**증상**:
- Gena 얼굴이 다르게 생성됨
- 헤어스타일 불일치

**원인**:
- 참조 이미지 누락
- 프롬프트 불충분

**해결**:
```bash
# 1. Gena 참조 이미지 확인
ls -la shared/gena-references/
# gena_ref_01.png ~ gena_ref_08.png (8장)

# 2. gena-master-prompt.md 확인
cat shared/gena-master-prompt.md

# 3. 프롬프트 재생성
# prompt-engineer 에이전트 재실행
# 10개 체크리스트 통과 확인

# 4. Outfit Swap 2단계 사용
python scripts/nanogen_outfit_swap.py \
  --gena-ref shared/gena-references/gena_ref_01.png \
  --item-image items/outer_001.jpg \
  --output assets/result.png
```

---

### 🔴 Nanogen API 타임아웃

**증상**:
```
TimeoutError: Container ready timeout
```

**원인**:
- Nanogen 서버 과부하
- 네트워크 지연

**해결**:
```bash
# 1. 타임아웃 증가
python scripts/nanogen_image.py \
  --poll-timeout 600  # 10분

# 2. Nanogen 서버 상태 확인
curl http://localhost:8000/health

# 3. 재시도 (최대 2회)
# 자동으로 재시도됨

# 4. 다른 모델로 대체
# 나노바나나2 → 나노바나나Pro
```

---

## 3. 비디오 생성 (Nanogen Video)

### 🔴 비디오 생성 실패

**증상**:
```
{"status": "failed", "error": "Generation failed"}
```

**원인**:
- 프롬프트 문제
- 참조 프레임 품질
- Kling/Veo 서버 오류

**해결**:
```bash
# 1. 프롬프트 확인
cat content/20260306_spring_reels/prompts.json

# 2. 참조 프레임 확인
ls -la content/20260306_spring_reels/assets/

# 3. 모델 변경
# Kling Pro → Standard
python scripts/nanogen_video.py \
  --model-id kling-v3 \
  --kling-mode standard

# 4. 다른 모델 시도
# Kling → Veo
python scripts/nanogen_video.py \
  --model-id veo
```

---

### 🔴 비디오 처리 시간 너무 길음

**증상**:
- 1씬 생성에 30분 이상 소요

**원인**:
- Kling Pro 사용
- 서버 혼잡

**해결**:
```bash
# 1. Standard 모드 사용
--kling-mode standard

# 2. 영상 길이 단축
--duration 1  # 1초 (기본 5초)

# 3. 병렬 생성 (조심)
# 여러 씬을 동시에 생성 (Rate Limit 주의)

# 4. 나중에 재시도
# 서버 혼잡 시간대 피하기
```

---

## 4. FFmpeg 관련

### 🔴 자막 한글 깨짐

**증상**:
```
자막이 □□□□로 표시됨
```

**원인**:
- 폰트 파일 없음
- 인코딩 문제

**해결**:
```bash
# 1. 시스템 폰트 확인
fc-list :lang=ko

# 2. 한글 폰트 지정
python scripts/ffmpeg_assemble_reels.py \
  --font-file "/System/Library/Fonts/AppleSDGothicNeo.ttc"

# 3. 또는 폰트 설치
brew install fontconfig
fc-cache -fv

# 4. UTF-8 인코딩 확인
cat copy.md | file -
# UTF-8 Unicode text
```

---

### 🔴 비디오 결합 실패

**증상**:
```
[concat @ ...] Impossible to open 'file:...'
```

**원인**:
- 파일 경로 문제
- 씬 비디오 누락

**해결**:
```bash
# 1. 씬 비디오 확인
ls -la reels/scenes/
# scene_01.mp4, scene_02.mp4, ...

# 2. filelist.txt 확인
cat reels/filelist.txt

# 3. 절대 경로 사용
# ffmpeg_assemble_reels.py에서 resolve() 사용

# 4. 수동 결합
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

---

## 5. OpenClaw 에이전트

### 🔴 에이전트 응답 없음

**증상**:
- sessions_spawn 후 무응답
- 세션이 멈춤

**원인**:
- 타임아웃 초과
- 에이전트 에러

**해결**:
```python
# 1. 세션 상태 확인
sessions_list(limit=10)

# 2. 세션 로그 확인
sessions_history(sessionKey="SESSION_KEY_HERE", limit=50)

# 3. 세션 종료 후 재시도
# 세션 목록에서 멈춘 세션 확인 후 새로 시작

# 4. 타임아웃 증가
sessions_spawn(
    agentId="designer",
    task="...",
    runTimeoutSeconds=3600  # 1시간
)
```

---

### 🔴 에이전트 파일 저장 실패

**증상**:
- Write 권한 없음
- 파일 경로 오류

**원인**:
- 에이전트 설정 오류
- 경로 문제

**해결**:
```bash
# 1. 작업 폴더 확인
ls -la content/20260306_spring_outfits/

# 2. 권한 확인
chmod -R 755 content/

# 3. 에이전트 설정 확인
cat agents/designer.md
# Write 권한 확인

# 4. 오케스트레이터가 대신 저장
# researcher, item-researcher는 Read만
# 오케스트레이터가 파일 저장
```

---

## 6. Cron 자동화

### 🔴 Cron Job 실행 안 됨

**증상**:
- 예정 시간에 실행 안 됨
- 로그 없음

**원인**:
- Job disabled
- 스케줄 설정 오류
- 타임존 불일치

**해결**:
```python
# 1. Cron Job 목록 확인
cron(action='list', includeDisabled=True)

# 2. Job 상태 확인
# enabled: true 확인

# 3. Job 수동 실행
cron(action='run', jobId='JOB_ID', runMode='force')

# 4. 타임존 확인
# Asia/Seoul 확인

# 5. 스케줄 재확인
# Cron 표현식 검증
# 0 10 * * MON → 매주 월요일 10:00
```

---

### 🔴 Cron Job 무한 실패

**증상**:
- 매번 실패
- 에러 메시지 반복

**원인**:
- Task 문제
- 모델 오류

**해결**:
```python
# 1. Job 비활성화
cron(action='update', jobId='JOB_ID', patch={'enabled': False})

# 2. 수동 실행 테스트
# 동일한 task를 메인 세션에서 실행

# 3. Task 수정
cron(action='update', jobId='JOB_ID', patch={
    'payload': {
        'kind': 'agentTurn',
        'message': '수정된 task',
        'timeoutSeconds': 7200
    }
})

# 4. 재활성화
cron(action='update', jobId='JOB_ID', patch={'enabled': True})
```

---

## 🆘 긴급 상황 대처

### 발행 직전 오류

1. **로컬 저장 확인**
   ```bash
   ls -la content/LATEST_FOLDER/slides/
   # 최종 슬라이드 10장 확인
   ```

2. **수동 발행**
   ```bash
   # Imgur 업로드
   python scripts/imgur_uploader.py slides/*.png -o urls.txt
   
   # Instagram 발행
   python scripts/instagram_api.py publish-carousel \
     --images $(cat urls.txt | tr '\n' ' ') \
     --caption "..."
   ```

3. **나중에 발행**
   - 슬라이드는 로컬에 저장됨
   - 언제든 재발행 가능

---

### 전체 시스템 재시작

```bash
# 1. OpenClaw Gateway 재시작
openclaw gateway restart

# 2. 환경 변수 재로드
source .env

# 3. Cron Jobs 재확인
# OpenClaw 세션에서
cron(action='list')

# 4. 테스트 실행
python scripts/instagram_api.py recent
```

---

## 📞 지원

**문제 해결 안 되면**:
1. `memory/YYYY-MM-DD.md`에 이슈 기록
2. 자비스에게 보고: "자비스, 인스타 오류 확인해줘"
3. 로그 첨부: 에러 메시지, 스크린샷

**유용한 로그 위치**:
- OpenClaw: `~/.openclaw/logs/`
- Python 스크립트: stdout/stderr
- FFmpeg: `ffmpeg.log` (생성 시)

---

**최종 업데이트**: 2026-03-06  
**작성**: 자비스
