# 주식 자동매매 시스템 설치 가이드

**대상 환경**: MacBook Pro 2015 (macOS)
**작성일**: 2026-02-13
**작성자**: 자비스

---

## 📋 사전 요구사항

### 1. 시스템 환경
- **OS**: macOS (MacBook Pro 2015)
- **OpenClaw**: 설치 완료 ✅
- **Python**: 3.9 이상 (확인: `python3 --version`)
- **인터넷**: 한국투자증권 API 접속 필요

### 2. 계정 정보
- 한국투자증권 모의투자 계좌
- API 키 (APP_KEY, APP_SECRET)
- 텔레그램 봇 (알림용, 선택사항)

---

## 🚀 설치 순서

### Step 1: 파일 압축 해제

```bash
# 다운로드한 압축 파일 위치로 이동
cd ~/Downloads

# 압축 해제
tar -xzf kis-trading-bot-package.tar.gz

# 작업 디렉토리로 이동
cd kis-trading-bot-package

# OpenClaw workspace로 복사
cp -r kis-trading-bot ~/.openclaw/workspace/
```

---

### Step 2: Python 패키지 설치

```bash
# 필수 패키지 설치
pip3 install requests

# 설치 확인
pip3 list | grep requests
```

**예상 출력**:
```
requests    2.31.0
```

---

### Step 3: API 설정 파일 구성

#### 방법 A: 구글 시트 사용 (권장)

**구글 시트 URL**:
https://docs.google.com/spreadsheets/d/1NEgJIigfVQuuS4Ox9uldLGCrgVmZ79ro64FkQYTsli0

1. 구글 시트 접속
2. `KIS_API` 시트에서 API 키 확인
3. 자동으로 로드됨 (코드에 이미 구현됨)

#### 방법 B: 로컬 설정 파일 사용

`kis-demo-config.json` 파일 수정:

```json
{
  "account_number": "50158566",
  "account_product_code": "01",
  "app_key": "YOUR_APP_KEY",
  "app_secret": "YOUR_APP_SECRET",
  "base_url": "https://openapivts.koreainvestment.com:29443"
}
```

**⚠️ 주의**: 실전 계좌 사용 시 `base_url` 변경 필요
- 모의투자: `https://openapivts.koreainvestment.com:29443`
- 실전투자: `https://openapi.koreainvestment.com:9443`

---

### Step 4: API 연결 테스트

```bash
cd ~/.openclaw/workspace/kis-trading-bot

# 토큰 발급 테스트
python3 -c "
from kis_api import KISAPIClient
client = KISAPIClient()
print('✅ API 연결 성공!')
"
```

**예상 출력**:
```
INFO:kis_api:✅ 설정 로드 완료
INFO:kis_api:   계좌: 50158566-01
INFO:kis_api:✅ 토큰 발급 성공
✅ API 연결 성공!
```

**오류 발생 시**:
- `app_key`, `app_secret` 확인
- 인터넷 연결 확인
- 한투 API 서버 상태 확인

---

### Step 5: 시뮬레이션 모드 테스트

```bash
# 시뮬레이션 모드 실행 (실제 주문 없음)
python3 trading_engine.py

# 출력 확인
# "🧪 시뮬레이션 모드로 시작" 메시지가 나와야 함
```

**Ctrl+C**로 중지하고 다음 단계로 진행

---

### Step 6: OpenClaw 크론잡 등록

#### 6-1. OpenClaw 텔레그램 연동 확인

OpenClaw가 텔레그램과 연동되어 있는지 확인:
```bash
openclaw status
```

#### 6-2. 크론잡 등록

`cron-jobs.json` 파일을 사용해서 3개의 크론잡 등록:

**방법 1: 수동 등록 (추천)**

OpenClaw 텔레그램 대화창에서:

```
/cron add
```

그 다음 아래 JSON을 각각 입력:

**① 08:30 사전 점검**
```json
{
  "name": "주식 자동매매 - 사전점검 (08:30)",
  "schedule": {
    "kind": "cron",
    "expr": "30 8 * * 1-5",
    "tz": "Asia/Seoul"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "오늘 주식 자동매매 사전 점검을 실행하고 결과를 텔레그램으로 보내줘.\n\n실행 명령어: python3 ~/.openclaw/workspace/kis-trading-bot/morning_check.py\n\n그리고 morning-report.txt 파일 내용을 읽어서 텔레그램으로 전송해줘. 09:00에 자동으로 매매 시스템이 시작된다는 것도 알려주고, 문제가 있으면 09:00 전에 말씀해달라고 안내해줘.",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram"
  }
}
```

**② 09:00 자동매매 시작**
```json
{
  "name": "주식 자동매매 시작 (09:00)",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1-5",
    "tz": "Asia/Seoul"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "주식 자동매매 시스템을 시작해줘.\n\n명령어:\ncd ~/.openclaw/workspace/kis-trading-bot && nohup python3 trading_engine.py real --auto-confirm > /tmp/trading.log 2>&1 &\n\n그리고 텔레그램으로 알려줘:\n- 자동매매 시스템 가동 시작\n- 09:30부터 실시간 모니터링 시작\n- 거래 발생 시 즉시 알림\n- 중지하려면 /stop 입력",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram"
  }
}
```

**③ 15:30 일일 리포트**
```json
{
  "name": "주식 매매 일일 리포트 (15:30)",
  "schedule": {
    "kind": "cron",
    "expr": "30 15 * * 1-5",
    "tz": "Asia/Seoul"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "오늘 주식 매매 일일 리포트를 생성해서 텔레그램으로 보내줘.\n\n1. 계좌 잔고 조회 (kis_api.py 사용)\n2. 오늘의 매매 내역 읽기 (report-YYYY-MM-DD.json)\n3. 수익률 계산\n4. 텔레그램으로 전송\n\n포함 내용:\n- 총 거래 건수\n- 매수/매도 내역\n- 계좌 현황\n- 오늘의 수익/손실",
    "timeoutSeconds": 300
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram"
  }
}
```

**방법 2: 파일로 일괄 등록**

```bash
# cron-jobs.json 파일이 있는 경우
# (현재는 수동 등록만 지원됨)
```

---

### Step 7: 크론잡 등록 확인

```bash
# OpenClaw 텔레그램 대화창에서
/cron list
```

3개의 크론잡이 보여야 함:
- 주식 자동매매 - 사전점검 (08:30)
- 주식 자동매매 시작 (09:00)
- 주식 매매 일일 리포트 (15:30)

---

### Step 8: 첫 실행 테스트

#### 수동 실행 테스트

```bash
cd ~/.openclaw/workspace/kis-trading-bot

# 사전 점검 스크립트 실행
python3 morning_check.py

# 출력 확인
cat morning-report.txt
```

**예상 출력**:
```
✅ **사전 점검 완료!**

🌅 **장 시작 전 체크** (2026-02-14)

━━━━━━━━━━━━━━━━━━

💼 **계좌 현황**
• 예수금: XXXXX원
• 총평가: XXXXX원
...
```

---

## ✅ 설치 완료 체크리스트

- [ ] Python 3.9+ 설치 확인
- [ ] `requests` 패키지 설치
- [ ] 파일 압축 해제 및 복사
- [ ] API 설정 파일 구성 (`kis-demo-config.json` 또는 구글 시트)
- [ ] API 연결 테스트 성공
- [ ] 시뮬레이션 모드 테스트 성공
- [ ] OpenClaw 크론잡 3개 등록
- [ ] 크론잡 등록 확인
- [ ] 사전 점검 스크립트 테스트 성공

---

## 🎯 첫 운영 시작

**내일 (다음 거래일) 아침**:
- 08:30 - 자동으로 사전 점검 알림 도착
- 09:00 - 자동으로 매매 시스템 시작
- 15:30 - 자동으로 일일 리포트 도착

**수동 실행이 필요한 경우**:
```bash
# 실전 모드 수동 시작
cd ~/.openclaw/workspace/kis-trading-bot
nohup python3 trading_engine.py real --auto-confirm > /tmp/trading.log 2>&1 &

# 프로세스 확인
ps aux | grep trading_engine

# 로그 확인
tail -f /tmp/trading.log
```

---

## 🆘 문제 해결

### API 연결 실패
```
ERROR:kis_api:❌ HTTP 오류: 401
```
→ `app_key`, `app_secret` 확인

### 크론잡 실행 안 됨
→ OpenClaw 게이트웨이 재시작
```bash
openclaw gateway restart
```

### 프로세스가 멈춤
→ 수동으로 중지 후 재시작
```bash
# 프로세스 찾기
ps aux | grep trading_engine

# 중지
kill -9 [PID]

# 재시작
cd ~/.openclaw/workspace/kis-trading-bot
nohup python3 trading_engine.py real --auto-confirm > /tmp/trading.log 2>&1 &
```

---

## 📞 지원

- **개발자**: 자비스 (마보스님의 AI 비서)
- **문서**: `OPERATION.md` (운영 매뉴얼)
- **로그 위치**: 
  - 매매 로그: `/tmp/trading.log`
  - 사전 점검: `~/.openclaw/workspace/kis-trading-bot/morning-report.txt`
  - 일일 리포트: `~/.openclaw/workspace/kis-trading-bot/report-YYYY-MM-DD.json`

---

**설치 완료를 축하합니다!** 🎉

다음 문서: `OPERATION.md` (일일 운영 매뉴얼)
