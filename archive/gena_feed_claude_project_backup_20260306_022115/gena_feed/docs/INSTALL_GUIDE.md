# @gena_feed Claude Code 설치 & 실행 가이드

---

## 준비물 체크리스트

- [ ] Claude Code 설치 완료
- [ ] Nanogen 로컬 서버 실행 가능 (localhost:8000)
- [ ] Node.js 18 이상 (Puppeteer PNG 추출용)
- [ ] Python 3.9 이상 (Pillow 스토리 합성용)
- [ ] ffmpeg 설치 (릴스 클립 합성용)

---

## STEP 1. Claude Code 설치

터미널을 열고 아래 명령어를 실행합니다.

```bash
npm install -g @anthropic-ai/claude-code
```

설치 확인:
```bash
claude --version
```

---

## STEP 2. 프로젝트 폴더 준비

압축 파일을 원하는 위치에 풀어주세요.

```bash
unzip gena_feed_claude_project.zip
cd gena_feed
```

폴더 구조 확인:
```
gena_feed/
├── CLAUDE.md         ✅ 공통 지시서
├── AGENT.md          ✅ 오케스트레이터 지시서
├── .env.example      ✅ 환경변수 템플릿
├── .gitignore        ✅
├── skills/           ✅ 스킬 파일 8개
├── workflows/        ✅ 워크플로 4개
├── assets/           ⚠️ 이미지 직접 추가 필요
└── shared/           ✅ design-tokens.css
```

---

## STEP 3. 환경변수 설정

`.env.example`을 복사해서 `.env`를 만듭니다.

```bash
cp .env.example .env
```

`.env` 파일을 열어 값을 입력합니다:
```
NANOGEN_BASE_URL=http://localhost:8000
BUFFER_API_KEY=실제_버퍼_API_키
```

---

## STEP 4. Nanogen 서버 실행 확인

Claude Code를 시작하기 전에 **Nanogen이 먼저 실행 중**이어야 합니다.

```bash
# Nanogen 프로젝트 폴더에서
cd 나노젠_프로젝트_폴더
python manage.py runserver
```

확인:
```bash
curl http://localhost:8000/
# 응답이 오면 정상
```

---

## STEP 5. Python 의존성 설치

스토리 PNG 합성에 Pillow가 필요합니다.

```bash
pip install Pillow
```

---

## STEP 6. 초기 자산 등록 (최초 1회)

`assets/` 폴더에 아래 파일을 직접 추가하세요.

| 파일명 | 내용 | 권장 크기 |
|--------|------|----------|
| `assets/gena-base.png` | gena 페르소나 전신 이미지 | 1080×1920px |
| `assets/slant-product.png` | slant 슬링백 제품 단독 이미지 | 흰 배경 |
| `assets/bgm.mp3` | 릴스 배경음악 (저작권 무료) | — |
| `assets/Pretendard-Bold.ttf` | 폰트 파일 | [Pretendard 다운로드](https://github.com/orioncactus/pretendard) |

> `gena-base.png`와 `slant-product.png`가 없으면 릴스 Outfit Swap 씬이 작동하지 않습니다.

---

## STEP 7. Nanogen Workflow Studio 워크플로 저장 (최초 1회)

릴스 제작 전에 Nanogen Workflow Studio에서 기본 워크플로를 저장해야 합니다.

1. 브라우저에서 `http://localhost:8000` 접속
2. Workflow Studio 메뉴 진입
3. 아래 노드 순서로 연결:

```
[Text Input: 씬 스크립트]
        ↓
[Prompt Agent: 이미지 프롬프트 생성]
        ↓
[Image Generator × 6]  ← [Image Input: gena-base / slant]
        ↓
[Video Generator × 6]  (kling-v3, I2V 설정)
        ↓
[Output Result]
```

4. 저장 이름: **`gena_reels_base`**

> 이 워크플로가 없으면 릴스 제작 시 Claude Code가 안내 메시지를 보냅니다.

---

## STEP 8. Claude Code 실행

모든 준비가 완료됐으면 프로젝트 폴더에서 Claude Code를 시작합니다.

```bash
cd gena_feed
claude
```

Claude Code가 자동으로 `CLAUDE.md`와 `AGENT.md`를 읽고 프로젝트 컨텍스트를 파악합니다.

---

## 첫 번째 실행 — 주제 발굴

```
사용자: 이번 주 콘텐츠 주제 찾아줘
```

Claude Code가 자동으로:
1. researcher 에이전트 spawn → 트렌드 조사
2. 주제 12개 생성 후 사용자에게 전달
3. 6개 선택 컨펌 (G1 게이팅)
4. 선택된 주제로 캐러셀·릴스·스토리 트랙 연결

---

## 포맷별 실행 명령어

```bash
# 주간 주제 발굴
"이번 주 콘텐츠 주제 찾아줘"

# 캐러셀 제작
"캐러셀 만들어줘"
"slant 소개 캐러셀 만들어줘"

# 릴스 제작
"릴스 만들어줘"
"이번 주 릴스 제작 시작해"

# 스토리 제작
"스토리 만들어줘"
# (캐러셀 완료 후 자동 연계도 가능)

# 전체 주간 프로세스
"이번 주 전체 콘텐츠 만들어줘"
```

---

## 문제 해결

### Nanogen 서버 연결 실패
```
Error: ECONNREFUSED localhost:8000
```
→ Nanogen 서버가 실행 중인지 확인 후 `python manage.py runserver` 재실행

### Outfit Swap 실패
```
assets/gena-base.png 없음
```
→ `assets/` 폴더에 파일 추가 후 재시도

### Puppeteer PNG 추출 실패
```
Error: Cannot find module 'puppeteer'
```
```bash
npm install puppeteer
```

### Pillow 스토리 합성 실패
```
ModuleNotFoundError: No module named 'PIL'
```
```bash
pip install Pillow
```

### Pretendard 폰트 없음
→ https://github.com/orioncactus/pretendard 에서 다운로드
→ `assets/Pretendard-Bold.ttf` 위치에 저장

---

## 주간 루틴 요약

| 요일 | 할 일 |
|------|-------|
| 월 | `"이번 주 주제 찾아줘"` → G1 게이팅 (6개 선택) |
| 화 | 기획·카피 자동 생성 → G2 게이팅 (모델 선택·승인) → 스토리 D-1 발행 |
| 수 | 디자인·제작 자동 실행 → 캐러셀 발행 + 스토리 D+0 발행 |
| 목 | QA 자동 실행 → 이슈 수정 |
| 금 | G3 게이팅 (최종 확인) → 릴스 발행 |
| 토 | 스토리 D+3 발행 (slant CTA) |
