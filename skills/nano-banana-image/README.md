# 🎨 Google Gemini Flash Image Generator

Google의 Gemini 3.1 Flash Image Preview API (새 google-genai SDK)를 사용한 AI 이미지 생성 스킬입니다.

## 🚀 빠른 시작

### 1. 라이브러리 설치

```bash
cd skills/nano-banana-image
pip install -r requirements.txt
```

### 2. API 키 발급

**방법 A: Google AI Studio (추천 - 빠르고 간단)**

1. [Google AI Studio](https://aistudio.google.com/) 접속
2. Google 계정으로 로그인
3. "API 키 가져오기" 클릭
4. "API 키 만들기" 클릭
5. 생성된 API 키 복사

**방법 B: Google Cloud Console (프로덕션용)**

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 (예: "nano-banana-image-gen")
3. "API 및 서비스" → "사용자 인증 정보"
4. "사용자 인증 정보 만들기" → "API 키"
5. 생성된 API 키 복사

### 3. API 키 등록

**방법 A: 환경 변수 (권장)**

```bash
# ~/.zshrc 또는 ~/.bashrc에 추가
export GEMINI_API_KEY="your-api-key-here"

# 적용
source ~/.zshrc
```

**방법 B: OpenClaw Config**

```bash
openclaw config edit
```

config에 다음 추가:

```yaml
env:
  GEMINI_API_KEY: "your-api-key-here"
```

### 4. 실행 권한 부여

```bash
chmod +x generate_image.py batch_generate.py
```

## 📖 사용법

### 단일 이미지 생성

```bash
# 기본 (1:1 비율, 1개)
python generate_image.py "A cute cat wearing a hat"

# 가로 이미지 (16:9, 2개)
python generate_image.py "A beautiful sunset" --aspect-ratio 16:9 --number 2

# Negative prompt 사용
python generate_image.py "Portrait photo" --negative-prompt "blurry, ugly, low quality"

# 특정 seed 사용 (재현성)
python generate_image.py "A robot character" --seed 12345

# 출력 위치 지정
python generate_image.py "Modern office" --output-dir ./my_images
```

### 배치 생성

```bash
# TXT 파일로부터
python batch_generate.py examples/prompts.txt

# JSON 파일로부터 (개별 설정 가능)
python batch_generate.py examples/prompts.json

# 출력 위치 지정
python batch_generate.py prompts.txt --output-dir ./instagram_images

# 기본 설정 지정
python batch_generate.py prompts.txt --aspect-ratio 16:9 --negative-prompt "low quality"
```

## 📝 프롬프트 파일 형식

### TXT 형식

```txt
A beautiful sunset over the ocean
A cozy coffee shop interior
A modern minimalist workspace
# 주석도 가능합니다
```

### JSON 형식 (고급)

```json
[
  {
    "prompt": "A cute banana character",
    "aspect_ratio": "1:1",
    "negative_prompt": "scary, dark",
    "seed": 12345
  },
  {
    "prompt": "A modern office",
    "aspect_ratio": "16:9"
  }
]
```

## 🎨 프롬프트 작성 팁

### 구조화된 프롬프트

```
[주제] + [스타일] + [조명/분위기] + [품질 키워드]
```

예시:
```
A cozy coffee shop interior, minimalist style, warm natural lighting, 4k quality
```

### 효과적인 키워드

**스타일:**
- `photorealistic`, `cartoon style`, `oil painting`
- `minimalist`, `cyberpunk`, `retro`

**조명:**
- `natural lighting`, `studio lighting`, `golden hour`
- `dramatic lighting`, `soft light`

**품질:**
- `4k`, `8k`, `high quality`, `detailed`
- `professional`, `cinematic`

**분위기:**
- `cozy`, `dramatic`, `peaceful`, `vibrant`

### Negative Prompt 활용

원하지 않는 요소를 명시적으로 제외:

```
--negative-prompt "blurry, low quality, distorted, ugly, dark"
```

## 📊 출력 구조

```
output/
├── image_20260308_141530_1_seed12345.png
├── image_20260308_141530_2_seed67890.png
└── metadata_20260308_141530.json
```

**metadata.json 예시:**

```json
{
  "prompt": "A cute cat",
  "aspect_ratio": "1:1",
  "number_of_images": 2,
  "timestamp": "20260308_141530",
  "images": [
    {
      "filename": "image_20260308_141530_1_seed12345.png",
      "seed": 12345,
      "finish_reason": "SUCCESS"
    }
  ]
}
```

## 🔧 고급 사용법

### 캐릭터 일관성 유지

같은 캐릭터를 여러 포즈로 생성하려면 seed를 재사용:

```bash
# 첫 이미지 생성 (seed 저장)
python generate_image.py "A robot character, front view" --seed 42

# 같은 seed로 다른 포즈 생성
python generate_image.py "A robot character, waving hand" --seed 42
python generate_image.py "A robot character, sitting pose" --seed 42
```

### Instagram 콘텐츠 워크플로우

1. **아이디어 브레인스토밍**
   ```bash
   # 프롬프트 리스트 작성
   echo "Modern minimalist workspace" >> instagram_prompts.txt
   echo "Cozy reading nook" >> instagram_prompts.txt
   ```

2. **배치 생성**
   ```bash
   python batch_generate.py instagram_prompts.txt \
     --aspect-ratio 1:1 \
     --output-dir ./instagram_content
   ```

3. **결과 검토 및 선택**
   - `batch_summary.json`에서 성공한 이미지 확인
   - 원하는 이미지 선택

## ⚠️ 주의사항

1. **API 키 보안**
   - 절대 코드에 하드코딩하지 말 것
   - Git에 커밋하지 말 것 (`.gitignore` 추가)
   - 환경 변수 사용 권장

2. **Rate Limit**
   - 무료 계정: 제한된 요청 수
   - 과도한 요청 시 일시적 차단 가능
   - 배치 생성 시 간격 조절 필요할 수 있음

3. **안전 필터**
   - 부적절한 콘텐츠는 자동 차단
   - 폭력, 성인 콘텐츠 등 생성 불가

4. **저작권**
   - 생성된 이미지는 상업적 사용 가능
   - Google의 이용 약관 준수 필요

## 🐛 문제 해결

### "GEMINI_API_KEY not found"

```bash
# 환경 변수 확인
echo $GEMINI_API_KEY

# 설정되지 않았다면
export GEMINI_API_KEY="your-key-here"
```

### "google-generativeai not found"

```bash
pip install google-generativeai
```

### 이미지가 생성되지 않음

- 프롬프트가 안전 필터에 걸렸을 가능성
- API 할당량 초과 확인
- 네트워크 연결 확인

## 📚 참고 자료

- [공식 문서](https://ai.google.dev/gemini-api/docs)
- [API 가이드](https://apidog.com/kr/blog/nano-banana-2-api-kr/)
- [Google AI Studio](https://aistudio.google.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

## 🤝 기여

개선 제안이나 버그 리포트는 환영합니다!

## 📄 라이선스

이 스킬은 Google Generative AI API를 사용합니다.
API 사용은 Google의 이용 약관을 따릅니다.
