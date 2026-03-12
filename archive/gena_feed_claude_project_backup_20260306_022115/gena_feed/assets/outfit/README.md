# Outfit Grid Reference Images

이 폴더에 outfit grid 이미지를 추가하면 자동으로 이미지 생성 시 reference로 첨부됩니다.

## 📂 파일 명명 규칙

```
YYYYMMDD_description.png
```

**예시:**
- `20260301_casual_spring.png`
- `20260302_street_layered.png`
- `20260305_minimal_chic.png`

## 🎯 용도

- **착장 일관성**: 동일한 outfit으로 여러 슬라이드 촬영
- **브랜드 톤 유지**: GenArchive 스타일 가이드 반영
- **직접 컨트롤**: 마보스님이 직접 outfit 큐레이션

## 🔄 자동 로드 규칙

### 기본 동작
- **최신 3개** outfit grid 자동 첨부 (날짜순 역순)
- 파일명 날짜 기준 정렬

### 사용자 지정 (image-prompts.json)

```json
{
  "outfit_reference": {
    "enabled": true,
    "mode": "latest",  // "latest", "date_range", "specific"
    "count": 3,        // mode: latest일 때 개수
    "date_from": "20260301",  // mode: date_range일 때
    "date_to": "20260307",
    "specific_files": []  // mode: specific일 때 파일명 리스트
  }
}
```

## 📝 Outfit Grid 제작 가이드

### 권장 포맷
- **레이아웃**: 3x3 또는 2x2 그리드
- **항목**: 상의, 하의, 신발, 악세서리, 아우터 등
- **배경**: 깔끔한 흰색 또는 회색
- **해상도**: 최소 1200x1200px

### 스타일 방향
- Casual street fashion
- Comfortable everyday wear
- Minimal clean aesthetic
- GenArchive brand tone

## 🚫 주의사항

- 파일명에 날짜(YYYYMMDD) 필수
- 이미지 포맷: PNG, JPG 권장
- 용량: 10MB 이하 권장 (API 전송 고려)
