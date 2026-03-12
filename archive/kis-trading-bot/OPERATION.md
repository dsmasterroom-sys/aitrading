# 주식 자동매매 시스템 운영 매뉴얼

**작성일**: 2026-02-13
**작성자**: 자비스

---

## 📅 일일 운영 루틴

### 🌅 아침 (08:30)

**자동 실행**: 사전 점검 크론잡

**확인 사항**:
- [ ] 텔레그램으로 사전 점검 리포트 도착
- [ ] 계좌 현황 확인 (예수금, 총평가, 보유종목)
- [ ] 오늘의 매매 전략 확인
- [ ] 이상 없으면 대기

**문제 발생 시**:
- API 오류 → `SETUP.md` 문제 해결 참고
- 계좌 정보 이상 → 한투 앱에서 직접 확인
- 전략 파일 없음 → `strategy-YYYY-MM-DD.md` 작성 필요

---

### 🚀 장 시작 (09:00)

**자동 실행**: 자동매매 시스템 시작

**확인 사항**:
- [ ] 텔레그램으로 "자동매매 시스템 가동 시작" 메시지 도착
- [ ] 09:30부터 실시간 모니터링 시작됨

**수동 시작 필요 시**:
```bash
cd ~/.openclaw/workspace/kis-trading-bot
nohup python3 trading_engine.py real --auto-confirm > /tmp/trading.log 2>&1 &
echo "✅ 자동매매 시스템 시작됨 (PID: $(pgrep -f trading_engine))"
```

**실시간 로그 모니터링**:
```bash
tail -f /tmp/trading.log
```

---

### 📊 장 마감 (15:30)

**자동 실행**: 일일 리포트 생성

**확인 사항**:
- [ ] 텔레그램으로 일일 리포트 도착
- [ ] 오늘 거래 내역 확인
- [ ] 수익/손실 확인
- [ ] 내일 전략 준비

**리포트 파일 위치**:
```bash
~/.openclaw/workspace/kis-trading-bot/report-2026-02-13.json
```

---

## 📝 매매 전략 업데이트

### 전략 파일 구조

**파일명**: `strategy-YYYY-MM-DD.md`

**예시**: `strategy-2026-02-14.md`

### 전략 작성 방법

1. **이전 전략 파일 복사**
```bash
cd ~/.openclaw/workspace/kis-trading-bot
cp strategy-2026-02-13.md strategy-2026-02-14.md
```

2. **전략 파일 수정**
```bash
open strategy-2026-02-14.md
```

3. **필수 포함 내용**:
   - 시장 전망
   - 매도 전략 (종목, 목표가, 손절가)
   - 매수 전략 (종목, 목표가, 손절가)
   - 보유 유지 종목

4. **전략 파일 형식**:
```markdown
# 2026-02-14 매매 전략

## 📊 시장 전망
- KOSPI: [전망]
- 전략: [전략]

## 📉 매도 전략

### 1. [종목명] ([보유수량]주 보유)
- 현재가: 약 [가격]원
- 매도 조건: [가격] 구간에서 [수량]주 매도
- 손절 기준: [가격]원

## 📈 매수 전략

### 1. [종목명] ([보유수량]주 → [목표수량]주)
- 현재가: 약 [가격]원
- 매수 조건: [가격] 구간에서 [수량]주 매수
- 손절: [가격]원
```

### 전략 파일 적용

**자동 적용**: 시스템이 매일 아침 최신 전략 파일을 자동으로 읽음

**수동 확인**:
```bash
cd ~/.openclaw/workspace/kis-trading-bot
python3 -c "
from strategy_parser import get_current_strategy
strategy = get_current_strategy()
print(f'적용된 전략: {strategy}')
"
```

---

## 🔍 모니터링

### 실시간 로그 확인

**터미널에서**:
```bash
tail -f /tmp/trading.log
```

**주요 로그 메시지**:
- `📈 매수 조건 충족` - 매수 대상 감지
- `✅ 매수 완료` - 매수 주문 완료
- `📉 매도 조건 충족` - 매도 대상 감지
- `✅ 매도 완료` - 매도 주문 완료
- `🚨 손절가 도달` - 손절 알림
- `⚠️ 일일 거래 한도 초과` - 거래 제한

### 프로세스 상태 확인

**실행 중인지 확인**:
```bash
ps aux | grep trading_engine
```

**출력 예시**:
```
master    10207  0.0  0.5  python3 trading_engine.py real --auto-confirm
```

**실행 중이면** PID가 표시됨

**실행 중이 아니면** 아무것도 표시 안 됨 → 재시작 필요

### 계좌 현황 수동 확인

```bash
cd ~/.openclaw/workspace/kis-trading-bot
python3 -c "
from kis_api import KISAPIClient
client = KISAPIClient()
balance = client.get_balance()
print(balance)
"
```

---

## 🛑 긴급 중지

### 자동매매 시스템 중지

**방법 1: 프로세스 종료**
```bash
# PID 확인
ps aux | grep trading_engine

# 프로세스 종료
kill -9 [PID]

# 확인
ps aux | grep trading_engine  # 아무것도 안 나와야 함
```

**방법 2: OpenClaw 텔레그램**
```
/stop
```

### 크론잡 일시 중지

**방법 1: 크론잡 비활성화**
```bash
# OpenClaw 텔레그램에서
/cron list

# 각 크론잡 ID 확인 후
/cron disable [JOB_ID]
```

**방법 2: 크론잡 삭제** (주의!)
```bash
/cron remove [JOB_ID]
```

---

## 📈 성과 분석

### 일일 리포트 보기

**파일 위치**:
```bash
~/.openclaw/workspace/kis-trading-bot/report-2026-02-13.json
```

**내용 확인**:
```bash
cat ~/.openclaw/workspace/kis-trading-bot/report-2026-02-13.json | python3 -m json.tool
```

**출력 예시**:
```json
{
  "date": "2026-02-13",
  "total_trades": 1,
  "total_amount": 403200,
  "orders": [
    {
      "time": "2026-02-13T13:10:00",
      "action": "매도",
      "stock_name": "두산로보틱스",
      "stock_code": "454910",
      "price": 100800,
      "quantity": 4,
      "amount": 403200
    }
  ]
}
```

### 주간/월간 분석

**주간 리포트 생성**:
```bash
cd ~/.openclaw/workspace/kis-trading-bot
ls -l report-2026-02-*.json
```

**월간 수익률 계산**:
```bash
# OpenClaw 텔레그램에서
"이번 달 주식 거래 수익률을 계산해줘. report-2026-02-*.json 파일들을 읽어서 분석해줘."
```

---

## 🔧 문제 해결

### 1. 자동매매가 실행되지 않음

**증상**: 09:00에 시스템 시작 메시지가 안 옴

**원인**:
- 크론잡 비활성화
- OpenClaw 게이트웨이 중지

**해결**:
```bash
# 크론잡 확인
/cron list  # (텔레그램)

# 게이트웨이 재시작
openclaw gateway restart

# 수동 시작
cd ~/.openclaw/workspace/kis-trading-bot
nohup python3 trading_engine.py real --auto-confirm > /tmp/trading.log 2>&1 &
```

---

### 2. API 오류 (HTTP 500)

**증상**: 로그에 `ERROR:kis_api:❌ HTTP 오류: 500`

**원인**: 한투 API 서버 일시적 문제

**해결**:
- 대부분 자동으로 재시도됨
- 지속되면 한투 API 서버 상태 확인
- 필요시 시스템 재시작

---

### 3. 거래가 체결되지 않음

**증상**: "매수/매도 조건 충족" 로그는 있는데 "완료" 메시지 없음

**원인**:
- 가격 변동으로 지정가 미체결
- 계좌 잔고 부족
- API 오류

**해결**:
1. 한투 앱에서 미체결 주문 확인
2. 필요시 수동으로 체결
3. 시스템 로그 확인: `tail -50 /tmp/trading.log`

---

### 4. 손절가 도달 시

**증상**: `🚨 손절가 도달` 로그

**원인**: 주가가 손절가 이하로 하락

**자동 처리**:
- 시스템이 자동으로 전량 손절 매도
- 시장가로 즉시 체결

**확인**:
1. 텔레그램 알림 확인
2. 한투 앱에서 체결 확인
3. 필요시 전략 수정

---

### 5. 일일 한도 초과

**증상**: `⚠️ 일일 거래 한도 초과` 로그

**원인**: 하루 거래 금액이 500만원 초과

**해결**:
- 자동으로 추가 거래 중지됨
- 한도 변경 필요 시 `trading_engine.py` 수정:
```python
self.max_daily_amount = 10000000  # 1000만원으로 변경
```

---

## 📞 지원 및 문의

### 로그 위치

**주요 로그 파일**:
- 실시간 매매: `/tmp/trading.log`
- 사전 점검: `~/.openclaw/workspace/kis-trading-bot/morning-report.txt`
- 일일 리포트: `~/.openclaw/workspace/kis-trading-bot/report-YYYY-MM-DD.json`
- 전략 파일: `~/.openclaw/workspace/kis-trading-bot/strategy-YYYY-MM-DD.md`

### 백업

**정기 백업 권장**:
```bash
# 전체 폴더 백업
tar -czf kis-trading-bot-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/kis-trading-bot/

# 구글 드라이브 업로드 (선택)
```

---

## 🎯 운영 팁

### 1. 매일 아침 체크리스트
- [ ] 08:30 사전 점검 리포트 확인
- [ ] 오늘의 전략 검토
- [ ] 09:00 자동매매 시작 확인
- [ ] 장 중 알림 모니터링

### 2. 매일 저녁 체크리스트
- [ ] 15:30 일일 리포트 확인
- [ ] 오늘 거래 내역 검토
- [ ] 내일 전략 준비 (필요시)
- [ ] 시스템 상태 확인

### 3. 주말 체크리스트
- [ ] 주간 성과 분석
- [ ] 전략 회고
- [ ] 다음 주 전략 준비
- [ ] 시스템 백업

---

**운영을 시작하신 것을 축하합니다!** 🎉

이전 문서: `SETUP.md` (설치 가이드)
참고 문서: `README.md` (시스템 개요)
