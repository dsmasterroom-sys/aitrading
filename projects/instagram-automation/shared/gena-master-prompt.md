# Gena Master Prompt - 캐릭터 절대 기준

**버전**: 1.0  
**최종 업데이트**: 2026-03-06  
**용도**: Nanogen 이미지 생성 시 Gena 캐릭터 일관성 유지

---

## ⚠️ 최우선 원칙

**Gena 캐릭터 일관성 = 프로젝트 성공의 전제 조건**

- 모든 이미지 생성 시 **반드시 참조 이미지 사용**
- 참조 이미지 없이 텍스트 프롬프트만으로 생성 **절대 금지**
- 생성 결과가 참조 이미지와 다른 사람처럼 보이면 **즉시 재생성**

---

## 👤 Gena 캐릭터 정의

### 기본 정보
- **이름**: Gena (제나)
- **나이**: 20대 중반 (24-26세)
- **국적**: 한국
- **직업 설정**: 패션 인플루언서 / 라이프스타일 크리에이터
- **브랜드 톤**: 세련되고 친근한, 트렌디하면서도 편안한

### 외모 특징 (절대 기준)

#### 얼굴
- **얼굴형**: 타원형 (Oval), 약간 긴 비율
- **피부톤**: 밝은 웜톤 (Warm Fair), 건강한 광채
- **눈**: 
  - 크고 또렷한 쌍꺼풀
  - 눈동자 색: 다크 브라운
  - 눈매: 부드러운 느낌, 약간 처진 듯한 고양이상
- **코**: 
  - 오뚝한 콧대
  - 작고 둥근 코끝
- **입**: 
  - 풍만한 입술 (중간 두께)
  - 자연스러운 핑크 컬러
- **턱선**: 부드럽고 매끄러운 V라인

#### 헤어
- **기본 컬러**: 다크 브라운 (#3D2817)
- **질감**: 부드럽고 윤기 있는
- **스타일 바리에이션**: 8가지 참조 이미지 (상황에 맞게 선택)

#### 체형
- **키**: 165-168cm (추정)
- **체형**: 슬림하면서도 건강한 (S라인)
- **어깨**: 적당히 넓은 편, 여성스러운 라인
- **허리-힙 비율**: 명확한 S라인

---

## 📸 참조 이미지 가이드 (8종)

**위치**: `shared/gena-references/`

| ID | 파일명 | 헤어스타일 | 용도 | 우선순위 |
|---|---|---|---|---|
| 01 | `gena_ref_01.png` | 숏/미디엄 스트레이트 | 캐주얼 룩, 데일리웨어 | ⭐⭐⭐ |
| 02 | `gena_ref_02.png` | 미디엄 웨이브 | 로맨틱 룩, 데이트룩 | ⭐⭐⭐ |
| 03 | `gena_ref_03.png` | 롱 스트레이트 | 세련된 룩, 오피스룩 | ⭐⭐⭐⭐ |
| 04 | `gena_ref_04.png` | 롱 웨이브 | 화보 스타일, 드레시 룩 | ⭐⭐⭐⭐⭐ |
| 05 | `gena_ref_05.png` | 업스타일 (업두) | 파티룩, 포멀 이벤트 | ⭐⭐⭐ |
| 06 | `gena_ref_06.png` | 기본 베이직 | 다용도 기본 참조 | ⭐⭐⭐⭐ |
| 07 | `gena_ref_07.png` | 캐주얼 스타일 | 스트릿 패션 | ⭐⭐⭐ |
| 08 | `gena_ref_08.png` | (추가 바리에이션) | 예비 참조 | ⭐⭐ |

### 참조 이미지 선택 기준

**콘텐츠 유형별 추천**:

1. **데일리 캐주얼**: `gena_ref_01.png` (숏 스트레이트)
2. **로맨틱 / 데이트**: `gena_ref_02.png` (미디엄 웨이브)
3. **오피스 / 세련**: `gena_ref_03.png` (롱 스트레이트)
4. **화보 / 고급**: `gena_ref_04.png` (롱 웨이브) ⭐ **최우선 추천**
5. **파티 / 이벤트**: `gena_ref_05.png` (업두)
6. **범용 / 기본**: `gena_ref_06.png` (베이직)
7. **스트릿 / 액티브**: `gena_ref_07.png` (캐주얼)

**기본 원칙**: 
- 의상 스타일이 명확하지 않으면 → `gena_ref_04.png` (롱 웨이브) 사용
- 여러 개 테스트할 시간이 있으면 → 2-3개 참조 이미지로 여러 버전 생성 후 선택

---

## 🎨 Nanogen 생성 가이드

### Outfit Swap 2단계 파이프라인

#### 1단계: 기본 포즈 생성 (선택 사항)
**목적**: Gena가 특정 포즈를 취한 기본 이미지 생성

```python
# 참조 이미지: gena_ref_04.png
# 프롬프트 예시
prompt = """
gena, 20s korean woman,
wearing white t-shirt and blue jeans,
standing on urban street in Seoul,
afternoon golden hour,
editorial fashion photography,
full body shot,
soft lighting,
high quality, professional photography
"""
```

#### 2단계: Outfit Swap (필수)
**목적**: 실제 제품 이미지를 Gena에게 착용

```python
# API: POST http://localhost:8000/api/generate
# referenceImages:
#   [0] = gena_ref_04.png (인물 참조)
#   [1] = product_image.jpg (의상 이미지)

request_data = {
    "prompt": "의상교체",
    "config": {
        "modelId": "gemini-3.1-flash-image-preview",
        "aspectRatio": "1:1",  # 또는 "3:4" (Instagram)
        "resolution": "1K"     # 또는 "2K" (고화질)
    },
    "referenceImages": [
        gena_ref_b64,    # Gena 참조 이미지
        garment_b64      # 의상 이미지
    ]
}
```

### 프롬프트 작성 원칙

#### ✅ 반드시 포함
- `gena` (캐릭터 이름)
- `20s korean woman` (나이/국적)
- `high quality, professional photography` (품질 보장)

#### ⚠️ 주의사항
- **얼굴 묘사 금지**: 참조 이미지가 얼굴을 정의함
- **과도한 디테일 금지**: 참조 이미지와 충돌 가능
- **복잡한 포즈 요청 주의**: Outfit Swap 실패 가능성 증가

#### 추천 프롬프트 템플릿

**기본 템플릿**:
```
gena, 20s korean woman,
wearing {outfit_description},
{location_description},
{lighting_condition},
editorial fashion photography,
{shot_type},
soft lighting,
high quality, professional photography
```

**예시**:
```
gena, 20s korean woman,
wearing casual white t-shirt and black leather jacket,
urban street in Seoul with modern buildings,
afternoon golden hour,
editorial fashion photography,
full body shot,
soft lighting,
high quality, professional photography
```

---

## 🔍 QA 체크리스트

생성된 이미지가 다음 기준을 모두 충족해야 **합격**:

### 필수 체크 항목

- [ ] **동일인 여부**: 참조 이미지와 명확히 같은 사람으로 인식
- [ ] **피부톤 일치**: 밝은 웜톤 유지
- [ ] **얼굴 비율**: 타원형 얼굴형 유지
- [ ] **눈 형태**: 크고 또렷한 쌍꺼풀, 부드러운 눈매
- [ ] **코 형태**: 오뚝한 콧대, 작고 둥근 코끝
- [ ] **입술**: 풍만한 입술, 자연스러운 컬러
- [ ] **헤어 컬러**: 다크 브라운 유지
- [ ] **전체 분위기**: 세련되고 친근한 느낌

### 불합격 사례

❌ **즉시 재생성이 필요한 경우**:
- 다른 사람처럼 보임 (동일인 인식 불가)
- 피부톤이 너무 차갑거나 어두움
- 얼굴형이 둥글거나 각진 형태로 변형
- 눈이 작아지거나 단꺼풀로 변형
- 인종이 달라 보임 (비아시안)
- 나이가 달라 보임 (10대 또는 30대 이상)

---

## 📊 성능 지표

### 목표 KPI

| 지표 | 목표 | 측정 방법 |
|---|---|---|
| **캐릭터 일관성** | 95% 이상 | 육안 검증 합격률 |
| **1회 생성 성공률** | 80% 이상 | 재생성 없이 합격 |
| **평균 재생성 횟수** | 1.2회 이하 | 1개당 평균 시도 횟수 |
| **QA 통과율** | 90% 이상 | 최종 게시물 채택률 |

### 실제 성과 (Phase 1 검증)

- **캐릭터 일관성**: ⭐⭐⭐⭐⭐ (5/5)
- **1회 생성 성공률**: 100% (1/1)
- **재생성 횟수**: 0회
- **품질 평가**: 패션 화보급

---

## 🔄 버전 관리

### v1.0 (2026-03-06)
- 초기 버전 작성
- 8개 참조 이미지 정의
- Outfit Swap 2단계 파이프라인 확립
- Phase 1 검증 결과 반영

### 업데이트 예정
- [ ] 참조 이미지 추가 (계절별/스타일별)
- [ ] 프롬프트 템플릿 확장 (상황별 20종)
- [ ] QA 자동화 스크립트 연동
- [ ] 실패 케이스 데이터베이스 구축

---

## 📞 문의 및 피드백

**담당**: 자비스 (OpenClaw orchestrator)  
**프로젝트**: @gena_feed 인스타그램 콘텐츠 자동화  
**업데이트**: 매주 검토, 필요 시 즉시 수정

---

**마지막 업데이트**: 2026-03-06 02:29  
**다음 리뷰**: 2026-03-13 (Week 1 종료 시)
