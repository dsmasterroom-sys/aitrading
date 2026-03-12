# 제품 파트너스 자동화 프로세스

**목표**: 인스타그램 콘텐츠에 제품 파트너스 링크를 자동으로 연결하여 수익화

---

## 전체 플로우

```
토픽 확정 (G1)
    ↓
Planner: 제품 카테고리 지정
    ↓
Researcher: 제품 검색/선정 + DB 업데이트
    ↓
Writer: 제품 자연스럽게 카피에 녹이기
    ↓
Designer: 제품 이미지 생성 (필요 시)
    ↓
QA: 제품 링크 유효성 + 재고 체크
    ↓
게시 + 링크 삽입
```

---

## 제품 DB 구조 (Google Sheets)

### Sheet 이름: `gena_feed_products`

#### 컬럼 구조
| 컬럼 | 설명 | 예시 |
|------|------|------|
| product_id | 제품 고유 ID | `PROD-001` |
| category | 제품 카테고리 | `denim`, `shirt`, `skincare`, `accessory` |
| name | 제품명 | `여성 와이드 데님 팬츠` |
| brand | 브랜드 | `Uniqlo`, `Olive Young` |
| price | 가격 | `39000` |
| affiliate_link | 파트너스 링크 | `https://coupa.ng/...` |
| platform | 플랫폼 | `coupang`, `naver`, `musinsa` |
| season | 시즌 적합성 | `spring`, `summer`, `all` |
| trend_score | 트렌드 점수 (0-10) | `8` |
| stock_status | 재고 상태 | `available`, `low`, `out` |
| image_url | 제품 이미지 URL | `https://...` |
| last_checked | 마지막 확인 날짜 | `2026-03-02` |
| notes | 메모 | `봄 시즌 추천` |

### Google Sheets API 연동
```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open("gena_feed_products").sheet1
```

---

## Agent별 역할

### 1. Planner: 제품 카테고리 지정

**입력**: `weekly/research.md` (확정된 토픽 6개)

**작업**:
- 각 토픽별 적합한 제품 카테고리 지정
- monetize 태그 확인 (`파트너스` / `slant` / `-`)

**출력**: `weekly/content-plan.md`에 제품 카테고리 추가

```markdown
## W10-02: 제니가 매번 같은 셔츠 입는 이유 (릴스)
- 포맷: 릴스
- monetize: 파트너스
- **제품 카테고리**: `shirt` (화이트 셔츠)
- 제품 요구사항: 깔끔한 핏, 중가 브랜드, 봄 시즌
```

### 2. Researcher: 제품 검색/선정

**스킬**: `skills/product-search.md` (새로 생성 필요)

**입력**: `weekly/content-plan.md` (제품 카테고리)

**작업**:
1. Google Sheets DB에서 해당 카테고리 제품 검색
   ```python
   products = sheet.get_all_records()
   filtered = [p for p in products if p['category'] == 'shirt' 
               and p['season'] in ['spring', 'all']
               and p['stock_status'] == 'available']
   sorted_products = sorted(filtered, key=lambda x: x['trend_score'], reverse=True)
   ```

2. 상위 3-5개 후보 선정
3. 링크 유효성 간단 체크 (404 아닌지)
4. 신규 제품 필요 시 웹 검색 (쿠팡/네이버 API)

**출력**: `weekly/research.md`에 제품 추천 추가

```markdown
## 제품 추천 (W10-02)
1. **유니클로 슈퍼논아이론 셔츠** (₩29,900)
   - 링크: https://coupa.ng/...
   - 트렌드 점수: 9/10
   - 재고: 충분

2. **스파오 베이직 화이트 셔츠** (₩19,900)
   - 링크: https://coupa.ng/...
   - 트렌드 점수: 7/10
```

### 3. Writer: 제품 자연스럽게 카피에 삽입

**입력**: `weekly/research.md` (제품 추천) + Planner 기획

**작업**:
- 제품을 카피에 자연스럽게 녹이기
- 링크는 캡션 끝 또는 댓글에 배치
- 광고 표기 준수 (필요 시)

**출력**: `weekly/copy.md`

```markdown
### 캡션
요즘 제니 공항 패션 보면
매번 똑같은 화이트 셔츠 입고 나오던데 🤔

그 이유 알고 나면 너도 똑같이 할걸?

핏 하나만 완벽하면
셔츠 하나로 10가지 룩 완성 👕✨

📌 제품 정보는 프로필 링크 확인!
(또는 댓글에 링크)

### 댓글 (자동 게시)
🔗 유니클로 슈퍼논아이론 셔츠
https://coupa.ng/...

🔗 스파오 베이직 화이트 셔츠  
https://coupa.ng/...
```

### 4. Designer: 제품 이미지 참조 (선택)

**조건**: 제품을 이미지에 직접 노출해야 하는 경우

**작업**:
- 제품 이미지 URL을 reference로 추가
- 또는 제품 설명 프롬프트에 포함

```json
{
  "prompt": "Korean woman wearing crisp white shirt, clean minimal style, shirt details visible (collar, buttons, tailored fit), ...",
  "referenceImages": [
    "gena_hair base64...",
    "product_image base64..." 
  ]
}
```

### 5. QA: 제품 링크 유효성 체크

**입력**: 완성된 콘텐츠

**체크 항목**:
- [ ] 제품 링크 404 아닌지
- [ ] 재고 상태 확인 (품절 아닌지)
- [ ] 가격 변동 확인 (너무 올랐는지)
- [ ] 광고 표기 올바른지 (법적 요구사항)
- [ ] 링크 단축 URL 작동 확인

**출력**: `weekly/qa-report.md`

```markdown
## 제품 링크 검증 (W10-02)

### 🟢 통과
- 유니클로 셔츠: 링크 OK, 재고 충분, 가격 변동 없음

### 🟡 주의
- 스파오 셔츠: 재고 "낮음" 상태, 조기 품절 가능

### 🔴 실패
- (없음)
```

---

## 자동화 스크립트 (예시)

### 제품 검색 스크립트
```python
# scripts/search_products.py
import gspread
import requests

def search_products(category, season="all", min_score=7):
    """Google Sheets에서 제품 검색"""
    sheet = get_sheet("gena_feed_products")
    products = sheet.get_all_records()
    
    filtered = [
        p for p in products
        if p['category'] == category
        and p['season'] in [season, 'all']
        and p['trend_score'] >= min_score
        and p['stock_status'] == 'available'
    ]
    
    return sorted(filtered, key=lambda x: x['trend_score'], reverse=True)[:5]

def check_link_validity(url):
    """링크 유효성 체크"""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False
```

### 제품 DB 업데이트
```python
# scripts/update_product_db.py
def add_product(product_data):
    """새 제품 추가"""
    sheet = get_sheet("gena_feed_products")
    sheet.append_row([
        product_data['product_id'],
        product_data['category'],
        product_data['name'],
        # ... 나머지 컬럼
    ])

def update_stock_status():
    """재고 상태 자동 업데이트 (크롤링 또는 API)"""
    # 구현 예정
    pass
```

---

## 파트너스 플랫폼별 설정

### 쿠팡 파트너스
- **API**: 쿠팡 파트너스 API
- **링크 형식**: `https://coupa.ng/...`
- **수수료**: 상품별 상이 (보통 1-5%)

### 네이버 쇼핑
- **API**: 네이버 쇼핑 API
- **링크 형식**: `https://search.shopping.naver.com/...`
- **수수료**: CPA 기반

### 무신사 파트너스
- **링크 형식**: `https://www.musinsa.com/...?ref=...`
- **수수료**: 3-5%

---

## 게이팅 포인트 통합

### G1 게이팅: 제품 카테고리 확정
- 토픽 선택 시 제품 카테고리도 함께 확정
- Planner가 제품 요구사항 명시

### G2 게이팅: 제품 선정 승인
- Researcher가 추천한 제품 중 최종 선택
- 마보스님이 제품 확정 (가격/브랜드 적합성)

### G3 게이팅: 링크 최종 확인
- QA 통과 후 링크 한 번 더 수동 확인
- 게시 직전 재고 상태 재확인

---

## 초기 세팅 TODO

- [ ] Google Sheets `gena_feed_products` 생성
- [ ] 카테고리별 기본 제품 10-20개 입력
- [ ] 쿠팡/네이버 파트너스 계정 연동
- [ ] `skills/product-search.md` 스킬 생성
- [ ] `scripts/search_products.py` 작성
- [ ] QA 체크리스트에 제품 검증 추가

---

**핵심**: 제품 파트너스도 Agent 기반 자동화 플로우의 일부로 통합
