# GitHub 배포/이전 가이드 (다른 PC 실행용)

## 목표
- 코드는 GitHub로 관리
- 민감정보(API 키/토큰/계좌)는 GitHub에 올리지 않음
- 실행 시 Google Sheet에서 로컬 설정 파일을 동기화

---

## 1) 로컬 정리
이 프로젝트는 이미 `.gitignore`가 설정되어 있어 아래 파일들은 커밋에서 제외됩니다.
- `kis-demo-config.json`
- `client_secret.json`, `token.json`
- `runtime-state.json`, `report-*.json`, `*.log`
- `.env*`

---

## 2) GitHub 초기 업로드
```bash
cd ~/.openclaw/workspace

git add .gitignore kis-trading-bot/
git commit -m "feat: restore trading bot with safety improvements and github-ready layout"

# 새 원격 저장소 생성 후
# git remote add origin <YOUR_GITHUB_REPO_URL>
# git branch -M main
# git push -u origin main
```

---

## 3) 다른 PC에서 실행
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <repo>/kis-trading-bot
python3 -m pip install -r requirements.txt
```

### 3-1) Google OAuth 파일 준비
다른 PC 로컬(절대 커밋 금지)에 다음 파일 배치:
- `<repo>/client_secret.json`
- `<repo>/token.json` (없으면 최초 1회 인증 필요)

### 3-2) 시트에서 설정 동기화
```bash
cd <repo>/kis-trading-bot
./sync_config_from_sheet.py
```
생성 결과:
- `<repo>/kis-demo-config.json`

### 3-3) 사전 점검
```bash
python3 morning_check.py
```

### 3-4) 자동매매 실행
```bash
# 드라이런
python3 trading_engine.py

# 실모드(모의투자 실주문)
python3 trading_engine.py real --auto-confirm
```

---

## 4) 운영 권장
- `market-holidays.json`에 휴장일 갱신
- 실행은 tmux/launchd/systemd 중 하나로 서비스화
- 로그는 `/tmp/trading.log` + 프로젝트 `trading.log` 함께 모니터링

---

## 5) 보안 체크리스트
- [ ] API 키/토큰 커밋 금지
- [ ] GitHub에 비밀 스캔(Secret scanning) 활성화
- [ ] 키 주기적 로테이션
- [ ] Google Sheet 공유권한 최소화(읽기 전용)
