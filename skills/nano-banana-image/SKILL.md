# Google Gemini Flash Image Generation Skill

Google의 Gemini 3.1 Flash Image Preview API (새 google-genai SDK)를 사용하여 이미지를 생성하는 스킬입니다.

## 📋 기능

- 텍스트 프롬프트로 이미지 생성
- 다양한 가로세로 비율 지원 (1:1, 16:9, 4:3 등)
- Negative prompt 지원 (원하지 않는 요소 제외)
- 배치 생성 (여러 이미지 한 번에 생성)
- 캐릭터 일관성 유지 (seed 활용)
- PNG 형식 직접 저장

## 🔧 사전 준비

1. **API 키 발급**
   - 방법 1: [Google AI Studio](https://aistudio.google.com/) (개발용, 빠름)
   - 방법 2: [Google Cloud Console](https://console.cloud.google.com/) (프로덕션용, 권장)

2. **API 키 등록**
   - OpenClaw config에 API 키 추가:
     ```bash
     openclaw config edit
     ```
   - 또는 환경 변수로 설정:
     ```bash
     export GEMINI_API_KEY="your-api-key-here"
     ```

## 📖 사용법

### 기본 이미지 생성

```python
python generate_image.py "A cute banana character wearing sunglasses, fun cartoon style"
```

### 고급 옵션 사용

```python
python generate_image.py \
  --prompt "A futuristic cityscape at night with neon lights" \
  --aspect-ratio "16:9" \
  --negative-prompt "blurry, low quality, distorted" \
  --number 2 \
  --output-dir "./generated_images"
```

### 배치 생성

```python
python batch_generate.py prompts.txt
```

## 🎨 프롬프트 작성 팁

- **구체적으로 작성**: "A cat" → "A fluffy orange cat sitting on a windowsill, soft natural lighting"
- **스타일 명시**: "cartoon style", "photorealistic", "oil painting", "minimalist"
- **조명/분위기 지정**: "golden hour", "studio lighting", "cinematic"
- **품질 키워드**: "4k", "high quality", "detailed", "professional"

## ⚙️ 매개변수

| 매개변수 | 타입 | 설명 | 기본값 |
|---------|------|------|--------|
| prompt | string | 이미지 설명 (필수) | - |
| number_of_images | int | 생성 이미지 수 (1-4) | 1 |
| aspect_ratio | string | 가로세로 비율 | "1:1" |
| negative_prompt | string | 제외할 요소 | "" |
| seed | int | 재현성을 위한 시드 | random |

## 🔗 API 엔드포인트

```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:predict?key=YOUR_API_KEY
```

## 📂 출력 형식

- PNG 형식
- Base64 인코딩
- 메타데이터 포함 (seed, finish_reason 등)

## 🚨 주의사항

- API 키는 절대 코드에 하드코딩하지 말 것
- 안전 필터가 적용되므로 부적절한 콘텐츠는 생성 거부됨
- Rate limit 확인 (무료 계정은 제한 있음)
- 프로덕션 환경에서는 에러 핸들링 필수

## 📚 참고 자료

- [공식 문서](https://ai.google.dev/gemini-api/docs)
- [API 가이드](https://apidog.com/kr/blog/nano-banana-2-api-kr/)
