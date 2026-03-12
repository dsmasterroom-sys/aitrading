# GENA_FEED QA 자동화 시스템 설계

**작성일:** 2026-03-02  
**목적:** @gena_feed 인스타그램 콘텐츠 품질 검증 자동화

---

## 📋 1. QA 체크 항목 전체 목록

| 카테고리 | 체크 항목 | 기준 | 자동화 여부 | 우선순위 |
|---------|----------|------|------------|---------|
| **이미지 품질** | 해상도 - 캐러셀 | 1080x1080px | ✅ 자동 | P0 |
| | 해상도 - 스토리/릴스 | 1080x1920px | ✅ 자동 | P0 |
| | 파일 크기 | 1-10MB | ✅ 자동 | P0 |
| | 색상 프로필 | sRGB | ✅ 자동 | P1 |
| | 이미지 파일 형식 | JPG/PNG | ✅ 자동 | P1 |
| | 비트 깊이 | 8-bit | ✅ 자동 | P2 |
| **브랜드 일관성** | 브랜드 컬러 사용 | #1A1A2E, #D4AF37, #FAFAFA | 🔶 반자동 | P1 |
| | 폰트 사용 | Pretendard 또는 Inter | ⚠️ 수동 | P2 |
| | 로고 배치 | 일관된 위치/크기 | ⚠️ 수동 | P2 |
| **텍스트 가독성** | 최소 폰트 크기 | 28px 이상 | 🔶 반자동 | P1 |
| | 명암 대비 | 4.5:1 이상 (WCAG AA) | 🔶 반자동 | P1 |
| | 텍스트 가독성 | 읽기 쉬운 배경 대비 | ⚠️ 수동 | P2 |
| **제품 정확성** | 소재 설명 | 나일론 (NOT leather) | ⚠️ 수동 | P0 |
| | 스트랩 위치 | 사이드 (NOT top) | ⚠️ 수동 | P0 |
| | 제품 컨텍스트 | 캐주얼/스트릿 스타일 | ⚠️ 수동 | P1 |
| | 제품 이미지 품질 | 흐림/왜곡 없음 | 🔶 반자동 | P1 |
| **발행 전 체크** | 캡션 길이 | 2200자 이내 | ✅ 자동 | P0 |
| | 해시태그 개수 | 30개 이내 | ✅ 자동 | P0 |
| | 링크바이오 안내 | 포함 여부 | ✅ 자동 | P0 |
| | 멘션 형식 | @username 올바른 형식 | ✅ 자동 | P1 |
| | 이모지 사용 | 적절한 배치 | ⚠️ 수동 | P2 |
| **메타데이터** | 파일명 규칙 | YYYYMMDD_type_seq.ext | ✅ 자동 | P1 |
| | EXIF 데이터 | GPS/개인정보 제거 | ✅ 자동 | P1 |
| | Alt 텍스트 준비 | 접근성 설명 준비 | ⚠️ 수동 | P2 |

**범례:**
- ✅ 자동: 완전 자동화 가능
- 🔶 반자동: 자동 분석 + 수동 검토 필요
- ⚠️ 수동: 수동 검토만 가능
- P0: 필수 (블로킹), P1: 중요, P2: 선택

---

## 🤖 2. 자동화 가능 vs 수동 검토 분류

### ✅ **완전 자동화 가능 (8개 항목)**
1. **이미지 해상도 검증** - Pillow로 픽셀 크기 확인
2. **파일 크기 검증** - os.path.getsize()
3. **색상 프로필 검증** - Pillow ImageCms 모듈
4. **이미지 형식 검증** - 파일 확장자 및 MIME 타입
5. **캡션 길이 검증** - len() 함수
6. **해시태그 개수** - 정규표현식 카운트
7. **링크바이오 키워드** - 텍스트 검색
8. **파일명 규칙** - 정규표현식 패턴 매칭
9. **EXIF 제거** - piexif 라이브러리

### 🔶 **반자동화 가능 (4개 항목)**
1. **브랜드 컬러 추출** - 주요 색상 추출 후 유사도 계산 (수동 최종 판단)
2. **텍스트 크기 추정** - OCR + 픽셀 크기 추정 (정확도 제한)
3. **명암 대비 분석** - 텍스트 영역 색상 분석 (OCR 기반)
4. **이미지 선명도** - 라플라시안 분산 (blur detection)

### ⚠️ **수동 검토 필요 (8개 항목)**
1. **폰트 사용** - 시각적 판단 필요
2. **로고 배치** - 디자인 일관성 판단
3. **제품 소재 설명** - 텍스트/컨텍스트 이해 필요
4. **스트랩 위치** - 제품 사진 세밀 검토
5. **제품 스타일링** - 전반적인 분위기 판단
6. **텍스트 가독성** - 주관적 판단
7. **이모지 적절성** - 감성적 판단
8. **Alt 텍스트 품질** - 접근성 전문성

---

## 🏗️ 3. scripts/qa_checker.py 설계

### 3.1 아키텍처 개요

```
qa_checker.py
├── QAChecker (메인 클래스)
│   ├── ImageQualityChecker
│   ├── BrandConsistencyChecker
│   ├── TextReadabilityChecker
│   └── ContentChecker
├── QAReport (결과 리포트)
└── QAConfig (설정 관리)
```

### 3.2 클래스 구조

```python
# qa_checker.py

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional
from PIL import Image, ImageCms
import piexif
import re
import numpy as np
import cv2

# ==================== 설정 ====================

@dataclass
class QAConfig:
    """QA 체크 기준 설정"""
    
    # 이미지 해상도
    CAROUSEL_SIZE = (1080, 1080)
    STORY_REEL_SIZE = (1080, 1920)
    SIZE_TOLERANCE = 0  # 픽셀 허용 오차
    
    # 파일 크기
    MIN_FILE_SIZE_MB = 1.0
    MAX_FILE_SIZE_MB = 10.0
    
    # 색상 프로필
    COLOR_PROFILE = 'sRGB'
    
    # 브랜드 컬러 (RGB)
    BRAND_COLORS = {
        'deep_navy': (26, 26, 46),      # #1A1A2E
        'gold': (212, 175, 55),         # #D4AF37
        'off_white': (250, 250, 250)    # #FAFAFA
    }
    COLOR_SIMILARITY_THRESHOLD = 30  # RGB 거리 기준
    
    # 텍스트
    MIN_FONT_SIZE_PX = 28
    MIN_CONTRAST_RATIO = 4.5  # WCAG AA
    
    # 콘텐츠
    MAX_CAPTION_LENGTH = 2200
    MAX_HASHTAGS = 30
    REQUIRED_KEYWORDS = ['링크바이오', 'link in bio', '프로필']  # 하나라도 포함
    
    # 파일명 패턴
    FILENAME_PATTERN = r'^\d{8}_[a-z]+_\d+\.(jpg|png)$'


class CheckStatus(Enum):
    """체크 결과 상태"""
    PASS = "✅ PASS"
    WARN = "⚠️ WARNING"
    FAIL = "❌ FAIL"
    SKIP = "⏭️ SKIP"
    MANUAL = "👁️ MANUAL_REVIEW"


@dataclass
class CheckResult:
    """개별 체크 결과"""
    category: str
    item: str
    status: CheckStatus
    message: str
    details: Optional[Dict] = None
    priority: str = "P1"


# ==================== 이미지 품질 체커 ====================

class ImageQualityChecker:
    """이미지 품질 자동 검증"""
    
    def __init__(self, config: QAConfig):
        self.config = config
    
    def check_resolution(self, image_path: Path, content_type: str) -> CheckResult:
        """해상도 검증"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                if content_type in ['story', 'reel']:
                    expected = self.config.STORY_REEL_SIZE
                else:  # carousel, feed
                    expected = self.config.CAROUSEL_SIZE
                
                if (width, height) == expected:
                    return CheckResult(
                        category="이미지 품질",
                        item="해상도",
                        status=CheckStatus.PASS,
                        message=f"해상도 정확: {width}x{height}px",
                        details={'width': width, 'height': height},
                        priority="P0"
                    )
                else:
                    return CheckResult(
                        category="이미지 품질",
                        item="해상도",
                        status=CheckStatus.FAIL,
                        message=f"해상도 불일치: {width}x{height}px (기대: {expected[0]}x{expected[1]}px)",
                        details={'width': width, 'height': height, 'expected': expected},
                        priority="P0"
                    )
        except Exception as e:
            return CheckResult(
                category="이미지 품질",
                item="해상도",
                status=CheckStatus.FAIL,
                message=f"이미지 읽기 실패: {str(e)}",
                priority="P0"
            )
    
    def check_file_size(self, image_path: Path) -> CheckResult:
        """파일 크기 검증"""
        size_mb = image_path.stat().st_size / (1024 * 1024)
        
        if self.config.MIN_FILE_SIZE_MB <= size_mb <= self.config.MAX_FILE_SIZE_MB:
            return CheckResult(
                category="이미지 품질",
                item="파일 크기",
                status=CheckStatus.PASS,
                message=f"파일 크기 적정: {size_mb:.2f}MB",
                details={'size_mb': size_mb},
                priority="P0"
            )
        else:
            status = CheckStatus.WARN if size_mb < 1 else CheckStatus.FAIL
            return CheckResult(
                category="이미지 품질",
                item="파일 크기",
                status=status,
                message=f"파일 크기 범위 벗어남: {size_mb:.2f}MB (기준: {self.config.MIN_FILE_SIZE_MB}-{self.config.MAX_FILE_SIZE_MB}MB)",
                details={'size_mb': size_mb},
                priority="P0"
            )
    
    def check_color_profile(self, image_path: Path) -> CheckResult:
        """색상 프로필 검증"""
        try:
            with Image.open(image_path) as img:
                if 'icc_profile' in img.info:
                    # ICC 프로필이 있으면 sRGB인지 확인
                    profile = ImageCms.ImageCmsProfile(io.BytesIO(img.info['icc_profile']))
                    profile_desc = ImageCms.getProfileDescription(profile).strip()
                    
                    if 'sRGB' in profile_desc:
                        return CheckResult(
                            category="이미지 품질",
                            item="색상 프로필",
                            status=CheckStatus.PASS,
                            message=f"색상 프로필: {profile_desc}",
                            details={'profile': profile_desc},
                            priority="P1"
                        )
                    else:
                        return CheckResult(
                            category="이미지 품질",
                            item="색상 프로필",
                            status=CheckStatus.WARN,
                            message=f"비표준 프로필: {profile_desc} (권장: sRGB)",
                            details={'profile': profile_desc},
                            priority="P1"
                        )
                else:
                    # ICC 프로필 없음 (대부분 sRGB 가정)
                    return CheckResult(
                        category="이미지 품질",
                        item="색상 프로필",
                        status=CheckStatus.PASS,
                        message="ICC 프로필 없음 (기본 sRGB 가정)",
                        priority="P1"
                    )
        except Exception as e:
            return CheckResult(
                category="이미지 품질",
                item="색상 프로필",
                status=CheckStatus.WARN,
                message=f"프로필 확인 실패: {str(e)}",
                priority="P1"
            )
    
    def check_sharpness(self, image_path: Path) -> CheckResult:
        """이미지 선명도 검증 (라플라시안 분산)"""
        try:
            img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
            
            # 경험적 임계값: 100 이상이면 선명
            if laplacian_var >= 100:
                return CheckResult(
                    category="이미지 품질",
                    item="선명도",
                    status=CheckStatus.PASS,
                    message=f"선명도 양호: {laplacian_var:.2f}",
                    details={'laplacian_variance': laplacian_var},
                    priority="P1"
                )
            else:
                return CheckResult(
                    category="이미지 품질",
                    item="선명도",
                    status=CheckStatus.WARN,
                    message=f"흐림 감지: {laplacian_var:.2f} (권장: 100+). 수동 확인 필요.",
                    details={'laplacian_variance': laplacian_var},
                    priority="P1"
                )
        except Exception as e:
            return CheckResult(
                category="이미지 품질",
                item="선명도",
                status=CheckStatus.SKIP,
                message=f"선명도 분석 실패: {str(e)}",
                priority="P1"
            )


# ==================== 브랜드 일관성 체커 ====================

class BrandConsistencyChecker:
    """브랜드 일관성 반자동 검증"""
    
    def __init__(self, config: QAConfig):
        self.config = config
    
    def check_brand_colors(self, image_path: Path) -> CheckResult:
        """브랜드 컬러 사용 확인 (주요 색상 추출)"""
        try:
            with Image.open(image_path) as img:
                # 이미지 리사이즈로 성능 향상
                img_small = img.resize((150, 150))
                pixels = np.array(img_small).reshape(-1, 3)
                
                # K-means로 주요 색상 5개 추출
                from sklearn.cluster import KMeans
                kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
                kmeans.fit(pixels)
                dominant_colors = kmeans.cluster_centers_.astype(int)
                
                # 브랜드 컬러와 유사도 체크
                found_colors = []
                for color_name, brand_rgb in self.config.BRAND_COLORS.items():
                    for dom_color in dominant_colors:
                        distance = np.linalg.norm(np.array(brand_rgb) - dom_color)
                        if distance < self.config.COLOR_SIMILARITY_THRESHOLD:
                            found_colors.append(color_name)
                            break
                
                if found_colors:
                    return CheckResult(
                        category="브랜드 일관성",
                        item="브랜드 컬러",
                        status=CheckStatus.PASS,
                        message=f"브랜드 컬러 사용 확인: {', '.join(found_colors)}",
                        details={'found_colors': found_colors, 'dominant_colors': dominant_colors.tolist()},
                        priority="P1"
                    )
                else:
                    return CheckResult(
                        category="브랜드 일관성",
                        item="브랜드 컬러",
                        status=CheckStatus.MANUAL,
                        message="브랜드 컬러 자동 감지 실패. 수동 확인 필요.",
                        details={'dominant_colors': dominant_colors.tolist()},
                        priority="P1"
                    )
        except ImportError:
            return CheckResult(
                category="브랜드 일관성",
                item="브랜드 컬러",
                status=CheckStatus.SKIP,
                message="sklearn 미설치. 수동 확인 필요.",
                priority="P1"
            )
        except Exception as e:
            return CheckResult(
                category="브랜드 일관성",
                item="브랜드 컬러",
                status=CheckStatus.SKIP,
                message=f"색상 분석 실패: {str(e)}",
                priority="P1"
            )


# ==================== 텍스트 가독성 체커 ====================

class TextReadabilityChecker:
    """텍스트 가독성 반자동 검증 (OCR 기반)"""
    
    def __init__(self, config: QAConfig):
        self.config = config
    
    def check_text_presence(self, image_path: Path) -> CheckResult:
        """텍스트 존재 여부 확인 (Tesseract OCR)"""
        try:
            import pytesseract
            with Image.open(image_path) as img:
                text = pytesseract.image_to_string(img, lang='kor+eng')
                
                if text.strip():
                    return CheckResult(
                        category="텍스트 가독성",
                        item="텍스트 감지",
                        status=CheckStatus.MANUAL,
                        message=f"텍스트 감지됨 ({len(text)} 글자). 폰트 크기/대비는 수동 확인 필요.",
                        details={'text_length': len(text), 'preview': text[:100]},
                        priority="P1"
                    )
                else:
                    return CheckResult(
                        category="텍스트 가독성",
                        item="텍스트 감지",
                        status=CheckStatus.PASS,
                        message="텍스트 없음 (이미지만)",
                        priority="P1"
                    )
        except ImportError:
            return CheckResult(
                category="텍스트 가독성",
                item="텍스트 감지",
                status=CheckStatus.SKIP,
                message="pytesseract 미설치. 수동 확인 필요.",
                priority="P1"
            )
        except Exception as e:
            return CheckResult(
                category="텍스트 가독성",
                item="텍스트 감지",
                status=CheckStatus.SKIP,
                message=f"OCR 실패: {str(e)}",
                priority="P1"
            )


# ==================== 콘텐츠 체커 ====================

class ContentChecker:
    """캡션/해시태그 등 콘텐츠 검증"""
    
    def __init__(self, config: QAConfig):
        self.config = config
    
    def check_caption_length(self, caption: str) -> CheckResult:
        """캡션 길이 검증"""
        length = len(caption)
        
        if length <= self.config.MAX_CAPTION_LENGTH:
            return CheckResult(
                category="발행 전 체크",
                item="캡션 길이",
                status=CheckStatus.PASS,
                message=f"캡션 길이: {length}/{self.config.MAX_CAPTION_LENGTH}자",
                details={'length': length},
                priority="P0"
            )
        else:
            return CheckResult(
                category="발행 전 체크",
                item="캡션 길이",
                status=CheckStatus.FAIL,
                message=f"캡션 초과: {length}/{self.config.MAX_CAPTION_LENGTH}자 (초과: {length - self.config.MAX_CAPTION_LENGTH}자)",
                details={'length': length, 'excess': length - self.config.MAX_CAPTION_LENGTH},
                priority="P0"
            )
    
    def check_hashtags(self, caption: str) -> CheckResult:
        """해시태그 개수 검증"""
        hashtags = re.findall(r'#\w+', caption)
        count = len(hashtags)
        
        if count <= self.config.MAX_HASHTAGS:
            return CheckResult(
                category="발행 전 체크",
                item="해시태그 개수",
                status=CheckStatus.PASS,
                message=f"해시태그: {count}/{self.config.MAX_HASHTAGS}개",
                details={'count': count, 'hashtags': hashtags},
                priority="P0"
            )
        else:
            return CheckResult(
                category="발행 전 체크",
                item="해시태그 개수",
                status=CheckStatus.FAIL,
                message=f"해시태그 초과: {count}/{self.config.MAX_HASHTAGS}개 (초과: {count - self.config.MAX_HASHTAGS}개)",
                details={'count': count, 'excess': count - self.config.MAX_HASHTAGS, 'hashtags': hashtags},
                priority="P0"
            )
    
    def check_link_in_bio(self, caption: str) -> CheckResult:
        """링크바이오 안내 포함 여부"""
        caption_lower = caption.lower()
        found_keywords = [kw for kw in self.config.REQUIRED_KEYWORDS if kw in caption_lower]
        
        if found_keywords:
            return CheckResult(
                category="발행 전 체크",
                item="링크바이오 안내",
                status=CheckStatus.PASS,
                message=f"링크바이오 안내 포함: '{found_keywords[0]}'",
                details={'found_keywords': found_keywords},
                priority="P0"
            )
        else:
            return CheckResult(
                category="발행 전 체크",
                item="링크바이오 안내",
                status=CheckStatus.WARN,
                message="링크바이오 안내 미포함. 필요 시 추가 권장.",
                details={'required_keywords': self.config.REQUIRED_KEYWORDS},
                priority="P0"
            )
    
    def check_filename_format(self, filename: str) -> CheckResult:
        """파일명 규칙 검증"""
        if re.match(self.config.FILENAME_PATTERN, filename):
            return CheckResult(
                category="메타데이터",
                item="파일명 규칙",
                status=CheckStatus.PASS,
                message=f"파일명 규칙 준수: {filename}",
                details={'filename': filename},
                priority="P1"
            )
        else:
            return CheckResult(
                category="메타데이터",
                item="파일명 규칙",
                status=CheckStatus.WARN,
                message=f"파일명 비표준: {filename} (권장: YYYYMMDD_type_seq.jpg)",
                details={'filename': filename, 'pattern': self.config.FILENAME_PATTERN},
                priority="P1"
            )
    
    def check_exif_data(self, image_path: Path) -> CheckResult:
        """EXIF 데이터 제거 확인"""
        try:
            exif_dict = piexif.load(str(image_path))
            gps_data = exif_dict.get('GPS', {})
            
            if gps_data:
                return CheckResult(
                    category="메타데이터",
                    item="EXIF 데이터",
                    status=CheckStatus.FAIL,
                    message="GPS 정보 포함됨. 제거 필요!",
                    details={'gps_keys': list(gps_data.keys())},
                    priority="P1"
                )
            else:
                return CheckResult(
                    category="메타데이터",
                    item="EXIF 데이터",
                    status=CheckStatus.PASS,
                    message="GPS 정보 없음 (안전)",
                    priority="P1"
                )
        except Exception:
            return CheckResult(
                category="메타데이터",
                item="EXIF 데이터",
                status=CheckStatus.PASS,
                message="EXIF 데이터 없음",
                priority="P1"
            )


# ==================== 메인 QA 체커 ====================

class QAChecker:
    """메인 QA 체커 클래스"""
    
    def __init__(self, config: Optional[QAConfig] = None):
        self.config = config or QAConfig()
        self.image_checker = ImageQualityChecker(self.config)
        self.brand_checker = BrandConsistencyChecker(self.config)
        self.text_checker = TextReadabilityChecker(self.config)
        self.content_checker = ContentChecker(self.config)
    
    def check_image(self, image_path: Path, content_type: str = 'carousel') -> List[CheckResult]:
        """이미지 파일 전체 검증"""
        results = []
        
        # 이미지 품질
        results.append(self.image_checker.check_resolution(image_path, content_type))
        results.append(self.image_checker.check_file_size(image_path))
        results.append(self.image_checker.check_color_profile(image_path))
        results.append(self.image_checker.check_sharpness(image_path))
        
        # 브랜드 일관성
        results.append(self.brand_checker.check_brand_colors(image_path))
        
        # 텍스트 가독성
        results.append(self.text_checker.check_text_presence(image_path))
        
        # 메타데이터
        results.append(self.content_checker.check_filename_format(image_path.name))
        results.append(self.content_checker.check_exif_data(image_path))
        
        return results
    
    def check_caption(self, caption: str) -> List[CheckResult]:
        """캡션 검증"""
        results = []
        
        results.append(self.content_checker.check_caption_length(caption))
        results.append(self.content_checker.check_hashtags(caption))
        results.append(self.content_checker.check_link_in_bio(caption))
        
        return results
    
    def check_post(self, image_path: Path, caption: str, content_type: str = 'carousel') -> 'QAReport':
        """전체 게시물 검증"""
        results = []
        
        # 이미지 체크
        results.extend(self.check_image(image_path, content_type))
        
        # 캡션 체크
        results.extend(self.check_caption(caption))
        
        return QAReport(results)


# ==================== QA 리포트 ====================

class QAReport:
    """QA 체크 결과 리포트"""
    
    def __init__(self, results: List[CheckResult]):
        self.results = results
        self.timestamp = datetime.now()
    
    def get_summary(self) -> Dict[str, int]:
        """결과 요약"""
        summary = {
            'total': len(self.results),
            'pass': sum(1 for r in self.results if r.status == CheckStatus.PASS),
            'warn': sum(1 for r in self.results if r.status == CheckStatus.WARN),
            'fail': sum(1 for r in self.results if r.status == CheckStatus.FAIL),
            'manual': sum(1 for r in self.results if r.status == CheckStatus.MANUAL),
            'skip': sum(1 for r in self.results if r.status == CheckStatus.SKIP),
        }
        return summary
    
    def is_blocking(self) -> bool:
        """P0 FAIL 있는지 확인 (발행 블로킹)"""
        return any(r.status == CheckStatus.FAIL and r.priority == "P0" for r in self.results)
    
    def print_report(self):
        """콘솔에 리포트 출력"""
        print("\n" + "="*70)
        print(f"📊 QA 체크 리포트 - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # 요약
        summary = self.get_summary()
        print(f"\n📈 요약: {summary['pass']}개 통과 | {summary['warn']}개 경고 | {summary['fail']}개 실패 | {summary['manual']}개 수동 필요")
        
        if self.is_blocking():
            print("\n🚨 **발행 블로킹**: P0 필수 항목 실패!")
        else:
            print("\n✅ 발행 가능 (P0 필수 항목 모두 통과)")
        
        # 카테고리별 결과
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
        
        for category, items in categories.items():
            print(f"\n📁 {category}")
            print("-" * 70)
            for item in items:
                priority_badge = f"[{item.priority}]" if item.priority in ["P0", "P1"] else ""
                print(f"  {item.status.value} {item.item} {priority_badge}")
                print(f"      → {item.message}")
    
    def to_dict(self) -> Dict:
        """딕셔너리로 변환 (JSON 저장용)"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'summary': self.get_summary(),
            'is_blocking': self.is_blocking(),
            'results': [
                {
                    'category': r.category,
                    'item': r.item,
                    'status': r.status.value,
                    'message': r.message,
                    'details': r.details,
                    'priority': r.priority
                }
                for r in self.results
            ]
        }


# ==================== CLI 인터페이스 ====================

def main():
    """CLI 메인 함수"""
    import argparse
    import json
    from datetime import datetime
    import io
    
    parser = argparse.ArgumentParser(description='GENA_FEED QA 자동화 도구')
    parser.add_argument('image', type=Path, help='이미지 파일 경로')
    parser.add_argument('--caption', type=str, help='캡션 텍스트 또는 파일 경로')
    parser.add_argument('--type', choices=['carousel', 'story', 'reel'], default='carousel', help='콘텐츠 타입')
    parser.add_argument('--output', type=Path, help='결과 JSON 저장 경로')
    
    args = parser.parse_args()
    
    # 캡션 로드
    caption = ""
    if args.caption:
        if Path(args.caption).exists():
            caption = Path(args.caption).read_text(encoding='utf-8')
        else:
            caption = args.caption
    
    # QA 체크 실행
    checker = QAChecker()
    report = checker.check_post(args.image, caption, args.type)
    
    # 결과 출력
    report.print_report()
    
    # JSON 저장
    if args.output:
        args.output.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n💾 결과 저장: {args.output}")
    
    # 종료 코드 (블로킹 시 1 반환)
    return 1 if report.is_blocking() else 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
```

---

## 📅 4. 구현 우선순위 로드맵

### Phase 0: 필수 기능 (1주차)
**목표:** P0 블로킹 항목 자동화로 발행 사고 방지

- ✅ **이미지 해상도 검증** - 잘못된 크기 업로드 차단
- ✅ **파일 크기 검증** - 인스타그램 제한 준수
- ✅ **캡션 길이 검증** - 2200자 초과 방지
- ✅ **해시태그 개수 검증** - 30개 제한
- ✅ **링크바이오 키워드** - 필수 CTA 누락 방지
- ✅ **기본 CLI 구조** - 단일 파일 체크 가능

**예상 공수:** 3-4일  
**산출물:** `qa_checker.py` v1.0 (기본 체커만)

---

### Phase 1: 브랜드 품질 강화 (2주차)
**목표:** 브랜드 일관성 자동 모니터링

- 🔶 **색상 프로필 검증** - sRGB 확인
- 🔶 **브랜드 컬러 분석** - 주요 색상 추출 (sklearn)
- 🔶 **이미지 선명도** - blur detection
- ✅ **EXIF 제거 확인** - 개인정보 보호
- ✅ **파일명 규칙** - 네이밍 컨벤션 자동 체크

**예상 공수:** 3-4일  
**의존성:** `opencv-python`, `scikit-learn`, `piexif`

---

### Phase 2: 텍스트 가독성 (3주차)
**목표:** 텍스트 포함 이미지 품질 향상

- 🔶 **OCR 텍스트 감지** - pytesseract 연동
- 🔶 **폰트 크기 추정** - 픽셀 기반 대략 계산
- 🔶 **명암 대비 분석** - 텍스트 영역 색상 분석
- ⚠️ **수동 체크리스트** - 폰트/로고/스타일 가이드 문서화

**예상 공수:** 4-5일  
**의존성:** `pytesseract`, Tesseract OCR 설치  
**참고:** 정확도 제한 있음. 최종 판단은 수동

---

### Phase 3: 제품 정확성 (4주차)
**목표:** slant 백 제품 설명 오류 방지

- ⚠️ **제품 체크리스트 템플릿** - 수동 검토용 폼
- 🔶 **캡션 키워드 분석** - "나일론", "사이드 스트랩" 키워드 검증
- ⚠️ **이미지 태깅 시스템** - 제품 속성 메타데이터 관리
- 📋 **발행 전 매뉴얼 체크시트** - Notion/Airtable 연동

**예상 공수:** 3-4일  
**참고:** 완전 자동화 불가. 보조 도구 + 프로세스 개선

---

### Phase 4: 통합 & 대시보드 (5주차)
**목표:** 팀 전체 사용 가능한 시스템 완성

- 📊 **배치 체크 모드** - 여러 파일 한 번에 검증
- 📈 **HTML 리포트 생성** - 시각적 대시보드
- 🔗 **Slack/Discord 알림** - QA 실패 시 자동 알림
- 📁 **폴더 감시 모드** - 특정 폴더 자동 모니터링
- 🎨 **GUI 래퍼** (선택) - 비개발자 친화적 인터페이스

**예상 공수:** 5-7일  
**의존성:** `jinja2`, `watchdog`, Slack/Discord webhook

---

## 🛠️ 5. 설치 & 사용법

### 5.1 필수 의존성 설치

```bash
# Phase 0 필수
pip install Pillow piexif

# Phase 1 추가
pip install opencv-python scikit-learn numpy

# Phase 2 추가 (선택)
pip install pytesseract
brew install tesseract tesseract-lang  # macOS
# apt install tesseract-ocr tesseract-ocr-kor  # Ubuntu

# Phase 4 추가 (선택)
pip install jinja2 watchdog
```

### 5.2 기본 사용법

```bash
# 단일 이미지 + 캡션 체크
python scripts/qa_checker.py images/20260302_carousel_01.jpg \
  --caption "지나백 slant 신상 출시! 나일론 소재로 가볍고 튼튼해요 💪 #지나백 #슬랜트백 링크바이오" \
  --type carousel

# 결과 JSON 저장
python scripts/qa_checker.py images/20260302_story_01.jpg \
  --caption caption.txt \
  --type story \
  --output qa_report.json
```

### 5.3 출력 예시

```
======================================================================
📊 QA 체크 리포트 - 2026-03-02 14:30:15
======================================================================

📈 요약: 8개 통과 | 2개 경고 | 1개 실패 | 2개 수동 필요

🚨 **발행 블로킹**: P0 필수 항목 실패!

📁 이미지 품질
----------------------------------------------------------------------
  ✅ PASS 해상도 [P0]
      → 해상도 정확: 1080x1080px
  ❌ FAIL 파일 크기 [P0]
      → 파일 크기 범위 벗어남: 12.34MB (기준: 1-10MB)
  ✅ PASS 색상 프로필 [P1]
      → ICC 프로필 없음 (기본 sRGB 가정)
  ✅ PASS 선명도 [P1]
      → 선명도 양호: 256.78

📁 발행 전 체크
----------------------------------------------------------------------
  ✅ PASS 캡션 길이 [P0]
      → 캡션 길이: 156/2200자
  ✅ PASS 해시태그 개수 [P0]
      → 해시태그: 2/30개
  ✅ PASS 링크바이오 안내 [P0]
      → 링크바이오 안내 포함: '링크바이오'
```

---

## 🧪 6. 테스트 전략

### 6.1 단위 테스트

```bash
# tests/test_qa_checker.py
pytest tests/ -v
```

**커버리지 목표:**
- 이미지 체커: 해상도/크기/프로필 각 edge case
- 콘텐츠 체커: 경계값 (2200자, 30개 등)
- 에러 핸들링: 파일 없음, 손상된 이미지

### 6.2 통합 테스트

**샘플 데이터셋 구성:**
- ✅ 올바른 이미지: `tests/samples/good_carousel.jpg`
- ❌ 잘못된 해상도: `tests/samples/bad_resolution.jpg`
- ❌ 파일 크기 초과: `tests/samples/too_large.jpg`
- ❌ 캡션 초과: `tests/samples/long_caption.txt`

---

## 📚 7. 참고 자료

- **Instagram Guidelines:** https://help.instagram.com/1631821640426723
- **WCAG Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Pillow Documentation:** https://pillow.readthedocs.io/
- **OpenCV Blur Detection:** https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
- **색상 추출 (K-means):** https://scikit-learn.org/stable/modules/clustering.html#k-means

---

## ⚠️ 8. 제약사항 & 알려진 이슈

1. **OCR 정확도:** 한글 폰트 크기 추정 부정확 (수동 검토 필수)
2. **브랜드 컬러:** 조명/필터로 색상 변형 시 false negative
3. **제품 정확성:** 이미지 인식 불가 (Vision AI 미구현)
4. **성능:** 고해상도 이미지(>10MB) 처리 시 10-15초 소요

---

## 🎯 9. 성공 지표

**Phase 0 달성 기준:**
- ✅ P0 블로킹 항목 100% 자동 감지
- ✅ 발행 사고 0건 (잘못된 해상도/캡션 초과)
- ✅ 평균 체크 시간 <5초/이미지

**최종 목표 (Phase 4):**
- ✅ 전체 QA 시간 50% 감소 (20분 → 10분)
- ✅ 수동 검토 항목 문서화로 누락률 90% 감소
- ✅ 팀 전체 도구 사용률 100%

---

**문서 작성:** 2026-03-02  
**다음 리뷰:** Phase 0 완료 후 (1주 후)  
**담당:** AI Agent (Subagent Planner)
