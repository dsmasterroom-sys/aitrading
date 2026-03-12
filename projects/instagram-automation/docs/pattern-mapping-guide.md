# 패턴 매핑 가이드

**목적**: developer 에이전트가 매번 새로운 CSS를 작성하지 않고, 기존 패턴을 재사용하도록 강제

---

## 🎯 기본 원칙

1. **모든 슬라이드는 반드시 patterns/*.html 기반**
2. **새로운 CSS 작성 절대 금지**
3. **CSS 변수만 참조**
4. **{{PLACEHOLDER}} 부분만 교체**

---

## 📐 슬라이드 타입별 패턴 매핑

### 캐러셀 10슬라이드 표준 구조

```
Slide 1: 훅 → 01-hero.html
Slide 2: 문제 → 11-overlay.html
Slide 3: 솔루션 → 02-split.html
Slide 4-8: 제품 → 03-product.html (5개)
Slide 9: 라인업 → 05-grid-4.html
Slide 10: CTA → 06-cta.html
```

### 패턴별 사용 시나리오

#### 01-hero.html
- **용도**: 훅, 히어로, 오프닝
- **구조**: 상단 65% 이미지, 하단 35% 텍스트
- **강조**: 네온 컬러 박스
- **예시**: "봄 가방 고민 끝 🌸"

#### 02-split.html
- **용도**: 솔루션 제시, Before/After
- **구조**: 좌우 50/50 분할
- **강조**: 화살표 또는 대비
- **예시**: "토트백 → 크로스백 전환"

#### 03-product.html
- **용도**: 제품 소개, 아이템 디테일
- **구조**: 중앙 이미지 + 좌하단 정보 박스
- **정보**: 브랜드, 가격, 특징
- **예시**: "라벤더 나일론 39,000원"

#### 04-quote.html
- **용도**: 인용, 강조 문구
- **구조**: 큰 따옴표 + 중앙 텍스트
- **강조**: 볼드 타이포
- **예시**: "200g도 안 돼서 깜짝 놀랐어요"

#### 05-grid-4.html
- **용도**: 라인업, 옵션 쇼케이스
- **구조**: 2×2 그리드
- **정보**: 4개 아이템 동시 표시
- **예시**: "봄 컬러 총집합"

#### 06-cta.html
- **용도**: 행동 유도, 마무리
- **구조**: 큰 버튼 + 유도 문구
- **강조**: 네온 컬러 버튼
- **예시**: "SHOP NOW" + "저장 📌"

#### 07-fullscreen.html
- **용도**: 임팩트, 브랜드 이미지
- **구조**: 전체 화면 이미지
- **텍스트**: 최소 (로고나 짧은 문구만)

#### 08-text-heavy.html
- **용도**: 설명, 가이드, 팁
- **구조**: 긴 텍스트 + 작은 이미지
- **가독성**: 충분한 여백, 큰 폰트

#### 09-minimal.html
- **용도**: 미니멀 브랜딩
- **구조**: 최소 요소, 여백 많음
- **강조**: 심플함, 세련됨

#### 10-bold-typo.html
- **용도**: 한 단어 강조
- **구조**: 초대형 타이포그래피
- **예시**: "NEW", "SALE", "LIMITED"

#### 11-overlay.html
- **용도**: 문제 제기, 공감
- **구조**: 전체 이미지 + 그라데이션 오버레이 + 하단 텍스트
- **분위기**: 어두운 배경, 공감 유도
- **예시**: "출근길 어깨 괴롭히는 토트백 🥲"

#### 12-comparison.html
- **용도**: 비교, 장단점
- **구조**: 좌우 비교 (VS)
- **정보**: 각 옵션의 특징

---

## 🔧 Orchestrator 실행 예시

### Phase 4: Developer 스폰 시

```python
# 1. prompts.json 읽기
with open(f"{work_dir}/prompts.json") as f:
    prompts = json.load(f)

# 2. 슬라이드 타입 분석 (자동 또는 수동)
pattern_mapping = auto_detect_patterns(prompts)
# 또는
pattern_mapping = {
    1: "01-hero.html",
    2: "11-overlay.html",
    3: "02-split.html",
    4: "03-product.html",
    5: "03-product.html",
    6: "03-product.html",
    7: "03-product.html",
    8: "03-product.html",
    9: "05-grid-4.html",
    10: "06-cta.html"
}

# 3. developer에게 패턴 매핑 전달
sessions_spawn({
    agentId: "developer",
    task: f"""
캐러셀 HTML 슬라이드 생성 및 PNG 렌더링

⚠️ 필수: 아래 패턴 매핑 엄수 (새로운 CSS 작성 금지)

패턴 매핑:
{json.dumps(pattern_mapping, indent=2, ensure_ascii=False)}

입력 파일:
- {work_dir}/assets/*.png (이미지)
- {work_dir}/copy.md (카피)
- shared/design-system/design-tokens.css (변수)
- shared/design-system/patterns/*.html (패턴)

작업 단계:
1. 각 슬라이드 번호 → 지정된 패턴 파일 읽기
2. {{{{PLACEHOLDER}}}} 부분만 copy.md 내용으로 교체
3. {{{{IMAGE_URL}}}} 부분을 assets 이미지로 교체 (base64 인라인)
4. CSS 변수 그대로 유지 (하드코딩 금지)
5. slides/ 폴더에 HTML 저장
6. Puppeteer로 PNG 렌더링 (2160×2880px)

금지 사항:
- 새로운 <style> 블록 추가 ❌
- 인라인 스타일 하드코딩 ❌ (font-size: 48px 같은 것)
- 레이아웃 구조 변경 ❌
- 패턴 외 HTML 템플릿 생성 ❌

허용 사항:
- CSS 변수 사용 ✅ (var(--font-size-h1))
- {{{{PLACEHOLDER}}}} 내용 교체 ✅
- 이미지 src 교체 ✅
- 텍스트 내용 교체 ✅
"""
})
```

---

## 🧪 자동 패턴 감지 로직 (선택사항)

```python
def auto_detect_patterns(prompts: List[Dict]) -> Dict[int, str]:
    """
    prompts.json의 copy_guide를 분석하여 자동으로 패턴 선택
    
    키워드 기반 매칭:
    - "훅", "오프닝", "시작" → 01-hero.html
    - "문제", "고민", "페인포인트" → 11-overlay.html
    - "솔루션", "해결", "전환" → 02-split.html
    - "제품", "아이템", "브랜드" → 03-product.html
    - "라인업", "전체", "옵션" → 05-grid-4.html
    - "CTA", "저장", "클릭", "구매" → 06-cta.html
    """
    mapping = {}
    
    for prompt in prompts:
        slide_num = prompt["slide"]
        guide = prompt.get("copy_guide", "").lower()
        
        if any(kw in guide for kw in ["훅", "오프닝", "시작"]):
            mapping[slide_num] = "01-hero.html"
        elif any(kw in guide for kw in ["문제", "고민", "페인포인트"]):
            mapping[slide_num] = "11-overlay.html"
        elif any(kw in guide for kw in ["솔루션", "해결", "전환"]):
            mapping[slide_num] = "02-split.html"
        elif any(kw in guide for kw in ["제품", "아이템", "브랜드", "가격"]):
            mapping[slide_num] = "03-product.html"
        elif any(kw in guide for kw in ["라인업", "전체", "옵션", "컬러"]):
            mapping[slide_num] = "05-grid-4.html"
        elif any(kw in guide for kw in ["cta", "저장", "클릭", "구매", "팔로우"]):
            mapping[slide_num] = "06-cta.html"
        else:
            # 기본값: 슬라이드 위치 기반
            if slide_num == 1:
                mapping[slide_num] = "01-hero.html"
            elif slide_num <= 3:
                mapping[slide_num] = "11-overlay.html"
            elif slide_num >= len(prompts):
                mapping[slide_num] = "06-cta.html"
            else:
                mapping[slide_num] = "03-product.html"
    
    return mapping
```

---

## ✅ 검증 체크리스트

**Phase 4 실행 전** (Orchestrator):
- [ ] 패턴 매핑 딕셔너리 생성
- [ ] 모든 슬라이드에 패턴 지정
- [ ] developer task에 매핑 포함

**Phase 4 실행 중** (Developer):
- [ ] 지정된 패턴 파일 읽기 확인
- [ ] 새로운 CSS 작성하지 않음
- [ ] CSS 변수만 사용

**Phase 5 검수 시** (QA Reviewer):
- [ ] HTML에 패턴 기반 구조 확인
- [ ] 하드코딩된 스타일 없음
- [ ] design-tokens.css 변수 사용 확인

---

**작성일**: 2026-03-06  
**작성자**: 자비스 (Orchestrator)  
**버전**: 1.0
