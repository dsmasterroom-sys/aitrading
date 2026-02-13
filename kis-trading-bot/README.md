# 주식 자동매매 시스템

**개발자**: 자비스 (마보스님의 AI 비서)  
**버전**: 1.0  
**작성일**: 2026-02-13  
**환경**: Python 3.9+, macOS/Linux

---

## 🎯 시스템 개요

한국투자증권 API를 활용한 **완전 자동화 주식 매매 시스템**입니다.

### 주요 기능

✅ **실시간 모니터링** (30초 간격)
- 보유 종목 가격 추적
- 매수/매도 조건 자동 감지
- 손절가 실시간 모니터링

✅ **자동 매매**
- 전략 파일 기반 자동 실행
- 지정가/시장가 주문 지원
- 일일 거래 한도 관리

✅ **안전장치**
- 손절가 자동 정리
- 일일 최대 거래 금액 제한
- 비정상 가격 감지 및 알림

✅ **자동 리포팅**
- 08:30 사전 점검 (계좌 현황 + 오늘의 전략)
- 15:30 일일 리포트 (거래 내역 + 수익률)
- 텔레그램 실시간 알림

---

## 📁 파일 구조

```
kis-trading-bot/
├── README.md                    # 이 파일
├── SETUP.md                     # 설치 가이드
├── OPERATION.md                 # 운영 매뉴얼
├── kis_api.py                   # API 클라이언트
├── strategy_parser.py           # 전략 파서
├── trading_engine.py            # 자동매매 엔진
├── morning_check.py             # 사전 점검 스크립트
├── kis-demo-config.json         # API 설정 (모의투자)
├── strategy-2026-02-13.md       # 매매 전략 (매일 작성)
├── report-2026-02-13.json       # 일일 리포트 (자동 생성)
├── morning-report.txt           # 사전 점검 결과 (자동 생성)
└── trading.log                  # 매매 로그 (자동 생성)
```

---

## 🚀 빠른 시작

### 1. 설치

**자세한 가이드**: `SETUP.md`

```bash
# 파일 압축 해제
tar -xzf kis-trading-bot-package.tar.gz
cd kis-trading-bot-package

# OpenClaw workspace로 복사
cp -r kis-trading-bot ~/.openclaw/workspace/

# Python 패키지 설치
pip3 install requests

# API 연결 테스트
cd ~/.openclaw/workspace/kis-trading-bot
python3 -c "from kis_api import KISAPIClient; KISAPIClient()"
```

### 2. 크론잡 등록

OpenClaw 텔레그램에서:
- 08:30 사전 점검
- 09:00 자동매매 시작
- 15:30 일일 리포트

**자세한 방법**: `SETUP.md` 참고

### 3. 첫 실행

```bash
# 시뮬레이션 모드 (실제 주문 없음)
python3 trading_engine.py

# 실전 모드 (수동 확인)
python3 trading_engine.py real

# 실전 모드 (자동 실행, 크론잡용)
python3 trading_engine.py real --auto-confirm
```

---

## 📋 일일 운영

**자세한 가이드**: `OPERATION.md`

### 아침 (08:30)
- ✅ 텔레그램으로 사전 점검 리포트 도착
- ✅ 계좌 현황, 오늘의 전략 확인

### 장 시작 (09:00)
- ✅ 자동매매 시스템 자동 시작
- ✅ 실시간 모니터링 시작 (30초마다)

### 장 마감 (15:30)
- ✅ 일일 리포트 자동 생성
- ✅ 거래 내역, 수익률 확인

---

## 📝 매매 전략 작성

### 전략 파일 예시

**파일명**: `strategy-2026-02-14.md`

```markdown
# 2026-02-14 매매 전략

## 📊 시장 전망
- KOSPI: 5,521.3pt(+3.1%)
- 전략: 눌림 국면에서 포지션 재정비

## 📉 매도 전략

### 1. 두산로보틱스 (7주 보유)
- 현재가: 약 101,800원
- 매도 조건: 100,000~120,000원 구간에서 3-4주 매도
- 손절 기준: 90,000원

## 📈 매수 전략

### 1. 삼성전자 (36주 → 40주 목표)
- 현재가: 약 174,300원
- 매수 조건: 170,000~172,000원 눌림 시 4주 추가
- 손절: 165,000원
```

### 전략 적용

**자동 적용**: 시스템이 매일 아침 최신 전략 파일(`strategy-YYYY-MM-DD.md`)을 자동으로 읽음

---

## 🔍 모니터링

### 실시간 로그

```bash
tail -f /tmp/trading.log
```

### 프로세스 확인

```bash
ps aux | grep trading_engine
```

### 계좌 현황

```bash
python3 -c "from kis_api import KISAPIClient; print(KISAPIClient().get_balance())"
```

---

## 🛑 긴급 중지

```bash
# PID 확인
ps aux | grep trading_engine

# 프로세스 종료
kill -9 [PID]
```

또는 OpenClaw 텔레그램에서:
```
/stop
```

---

## 📊 성과 분석

### 일일 리포트

```bash
cat ~/.openclaw/workspace/kis-trading-bot/report-2026-02-13.json
```

### 주간 분석

```bash
ls -l ~/.openclaw/workspace/kis-trading-bot/report-2026-02-*.json
```

---

## 🔧 문제 해결

### API 오류
```
ERROR:kis_api:❌ HTTP 오류: 500
```
→ 한투 API 서버 일시적 문제, 대부분 자동 재시도됨

### 자동매매 미실행
→ 크론잡 확인: `/cron list` (텔레그램)  
→ 게이트웨이 재시작: `openclaw gateway restart`

### 거래 미체결
→ 한투 앱에서 미체결 주문 확인  
→ 필요시 수동 체결

**자세한 문제 해결**: `OPERATION.md` 참고

---

## 📞 지원

### 문서
- **설치**: `SETUP.md`
- **운영**: `OPERATION.md`

### 로그 위치
- 실시간 매매: `/tmp/trading.log`
- 사전 점검: `~/.openclaw/workspace/kis-trading-bot/morning-report.txt`
- 일일 리포트: `~/.openclaw/workspace/kis-trading-bot/report-YYYY-MM-DD.json`

### 개발자
- **자비스** (마보스님의 AI 비서)
- 문의: OpenClaw 텔레그램

---

## 🎓 시스템 아키텍처

### 1. kis_api.py
- 한국투자증권 API 클라이언트
- 토큰 발급, 시세 조회, 주문, 잔고 조회

### 2. strategy_parser.py
- 매매 전략 파일(`strategy-YYYY-MM-DD.md`) 파싱
- 매수/매도 조건 추출

### 3. trading_engine.py
- 실시간 모니터링 루프 (30초 간격)
- 가격 조건 체크 및 자동 주문
- 손절가 자동 감지 및 처리

### 4. morning_check.py
- 장 시작 전 사전 점검
- 계좌 현황 + 오늘의 전략 리포트 생성

### 5. OpenClaw 크론잡
- 08:30 사전 점검
- 09:00 자동매매 시작
- 15:30 일일 리포트

---

## ⚠️ 주의사항

### 1. 모의투자 vs 실전투자

**현재 설정**: 모의투자 (기본)

**실전투자로 변경 시**:
`kis-demo-config.json`의 `base_url` 변경:
```json
{
  "base_url": "https://openapi.koreainvestment.com:9443"
}
```

### 2. API 보안

- `kis-demo-config.json` 파일 보안 유지
- API 키 노출 금지
- 백업 시 암호화 권장

### 3. 거래 한도

- 일일 최대 거래 금액: **500만원** (기본)
- 변경 필요 시 `trading_engine.py` 수정

### 4. 손절가

- 전략 파일에 손절가 필수 명시
- 손절가 도달 시 자동 전량 매도
- 시장가로 즉시 체결

---

## 📜 라이선스

이 시스템은 마보스님을 위해 자비스가 개발한 개인 프로젝트입니다.

**개발 기간**: 2026-02-12 ~ 2026-02-13  
**개발자**: 자비스 🤖

---

## 🎉 시작하기

**다음 단계**:
1. `SETUP.md` - 설치 가이드
2. `OPERATION.md` - 운영 매뉴얼
3. 첫 전략 파일 작성
4. 시뮬레이션 모드 테스트
5. 크론잡 등록
6. 실전 운영 시작!

**행운을 빕니다!** 📈🚀
