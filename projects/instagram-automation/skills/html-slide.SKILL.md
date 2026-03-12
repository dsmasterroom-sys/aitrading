# html-slide.SKILL.md

**용도**: HTML/CSS 슬라이드 구현 규칙  
**사용 에이전트**: developer  
**버전**: 1.0

---

## 📥 입력

- copy.md
- assets/ 이미지
- design-tokens.css

---

## 📤 출력

slides/{slide_id}.html:
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    :root { @import '../shared/design-system/design-tokens.css'; }
    .slide {
      width: 1080px;
      height: 1440px;
      background: var(--color-white);
    }
  </style>
</head>
<body>
  <div class="slide">
    <img src="data:image/png;base64,..." />
    <h1>카피 텍스트</h1>
  </div>
</body>
</html>
```

---

## 🔧 구현 규칙

### 스탠드얼론 HTML
- ❌ 외부 URL, CDN 참조 금지
- ✅ 이미지 base64 인라인 삽입
- ✅ CSS 인라인 또는 `<style>` 태그

### Canvas 고정
```css
.slide {
  width: 1080px;
  height: 1440px;
  position: relative;
  overflow: hidden; /* 필수 */
}
```

### Design Tokens 사용
```css
background: var(--color-primary-neon);
font-family: var(--font-primary);
font-size: var(--font-size-h1);
```

---

## 🎨 네오브루탈리즘 스타일

### 필수 요소
- **두꺼운 보더**: 4px solid black
- **강렬한 색상**: neon, red, pink, yellow
- **그림자**: `box-shadow: 8px 8px 0 black`
- **0 border-radius**: 직각

### 예시
```css
.card {
  border: 4px solid var(--color-black);
  box-shadow: var(--shadow-brutal);
  background: var(--color-primary-neon);
  padding: var(--space-md);
}
```

---

## 🖼️ 이미지 처리

### Base64 변환
```python
import base64
with open('image.png', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
    img_tag = f'<img src="data:image/png;base64,{b64}" />'
```

### 배치
- Object-fit: cover (비율 유지)
- Position: absolute (자유 배치)

---

## ✅ 검증

### [ ] Canvas 1080×1440
### [ ] Overflow 없음
### [ ] 폰트 28px 이상
### [ ] Design tokens 사용
### [ ] Base64 이미지

---

**최종 업데이트**: 2026-03-06 04:00
