# Gena 캐릭터 일관성 테스트 가이드

**목표**: 8개 참조 이미지로 캐릭터 일관성 검증

---

## 1. Nanogen 서버 접속

- URL: http://localhost:8001
- 상태: ✅ 실행 중 (포트 8001)
- 서버 종료 시: `cd /Users/master/.openclaw/workspace/nanogen && source venv/bin/activate && python manage.py runserver 8001`

---

## 2. 참조 이미지 위치

```
/Users/master/.openclaw/workspace/projects/instagram-automation/shared/gena-references/
├── gena_ref_01.png  (5.4MB)
├── gena_ref_02.png  (5.1MB)
├── gena_ref_03.png  (5.9MB)
├── gena_ref_04.png  (5.2MB)
├── gena_ref_05.png  (5.1MB)
├── gena_ref_06.png  (5.5MB)
├── gena_ref_07.png  (5.6MB)
└── gena_ref_08.png  (5.5MB)
```

---

## 3. 테스트 프롬프트 (복사용)

### 기본 테스트 (참조 이미지 일관성 검증)

```
gena, 20s korean woman, wearing casual white t-shirt and blue jeans, 
standing on urban street in Seoul, afternoon golden hour, 
editorial fashion photography, full body shot, soft lighting
```

### 헤어스타일별 테스트

**참조 이미지 01번 사용 시**:
```
gena, 20s korean woman, wearing elegant black dress, 
standing in modern cafe interior, soft window light, 
portrait photography, half body shot
```

**참조 이미지 03번 사용 시**:
```
gena, 20s korean woman, wearing oversized shirt and wide-leg pants, 
walking on Seongsu-dong street, afternoon, 
street fashion photography, full body shot
```

---

## 4. Nanogen 설정값

### Image Generator 노드 설정
- **Model**: Gemini 3.1 Flash Image (gemini-3.1-flash-image-preview)
- **Aspect Ratio**: 3:4 (Instagram 최적)
- **Resolution**: 2K
- **Number of Images**: 1
- **Reference Images**: 참조 이미지 1장 업로드

---

## 5. 캐릭터 일관성 검증 체크리스트

생성된 이미지와 참조 이미지를 비교하여 확인:

### 필수 검증 항목 (고)
- [ ] **얼굴 동일인 여부**: 눈, 코, 입 윤곽이 같은 사람인가?
- [ ] **피부톤 일치**: 색온도가 유사한가?
- [ ] **전체적인 인물 느낌**: 같은 사람으로 인식되는가?

### 권장 검증 항목 (중)
- [ ] **얼굴 각도/표정 변화**: 다른 포즈에서도 일관성 유지?
- [ ] **조명 환경 변화**: 다른 조명에서도 동일인 유지?
- [ ] **의상 변화**: 옷이 바뀌어도 얼굴/체형 일관성 유지?

---

## 6. 테스트 결과 기록

### 참조 이미지별 결과

| 참조 이미지 | 생성 성공 | 일관성 평가 | 비고 |
|---|---|---|---|
| gena_ref_01.png | ⬜ | ⬜ |  |
| gena_ref_02.png | ⬜ | ⬜ |  |
| gena_ref_03.png | ⬜ | ⬜ |  |
| gena_ref_04.png | ⬜ | ⬜ |  |
| gena_ref_05.png | ⬜ | ⬜ |  |
| gena_ref_06.png | ⬜ | ⬜ |  |
| gena_ref_07.png | ⬜ | ⬜ |  |
| gena_ref_08.png | ⬜ | ⬜ |  |

### 일관성 평가 기준
- **✅ 우수**: 확실히 같은 사람, 브랜드 사용 가능
- **⚠️ 보통**: 비슷하지만 미세한 차이, 추가 테스트 필요
- **❌ 불량**: 다른 사람처럼 보임, 참조 방식 재검토 필요

---

## 7. 다음 단계 (테스트 통과 시)

### Phase 1 완료 조건
- 8개 참조 이미지 중 **최소 6개 이상** "우수" 평가
- 나머지도 최소 "보통" 이상

### Phase 2: Outfit Swap 테스트
1. 무신사에서 실제 제품 이미지 1개 다운로드
2. Nanogen Composition 모드로 Outfit Swap 시도
3. Gena + 실제 제품 착용 이미지 생성 검증

---

## 8. 트러블슈팅

### Gemini API 응답 없음
- **원인**: 미국 데이타임 트래픽 폭주
- **해결**: 한국 시간 오전 (미국 밤) 재시도 또는 Kling AI 대안 사용

### 이미지 생성 실패
- **원인**: API 할당량 초과 또는 프롬프트 문제
- **해결**: API 키 확인, 프롬프트 단순화

### 캐릭터 일관성 낮음
- **원인**: 참조 이미지 품질 또는 모델 한계
- **해결**: 
  1. 더 선명한 참조 이미지 사용
  2. LoRA 학습 고려 (별도 작업)
  3. Midjourney --cref 대안 검토

---

**작성일**: 2026-03-06  
**작성자**: 자비스  
**테스트 담당**: 마보스님
