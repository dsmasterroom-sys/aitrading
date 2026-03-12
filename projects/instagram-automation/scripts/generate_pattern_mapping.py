#!/usr/bin/env python3
"""
패턴 매핑 자동 생성기

prompts.json을 분석하여 각 슬라이드에 적합한 design-system 패턴을 자동 매핑

Usage:
    python scripts/generate_pattern_mapping.py content/20260306_spring_crossbag/prompts.json
"""

import sys
import json
from pathlib import Path
from typing import Dict, List


def auto_detect_pattern(slide: Dict) -> str:
    """
    슬라이드 정보를 분석하여 적합한 패턴 선택
    
    Args:
        slide: prompts.json의 슬라이드 딕셔너리
    
    Returns:
        패턴 파일명 (예: "01-hero.html")
    """
    slide_num = slide.get("slide", 0)
    copy_guide = slide.get("copy_guide", "").lower()
    image_prompt = slide.get("image_prompt", "").lower()
    
    # 키워드 기반 매칭
    keywords = {
        "01-hero.html": ["훅", "오프닝", "시작", "hero", "hook"],
        "11-overlay.html": ["문제", "고민", "페인포인트", "problem", "pain"],
        "02-split.html": ["솔루션", "해결", "전환", "solution", "before", "after"],
        "03-product.html": ["제품", "아이템", "브랜드", "가격", "product", "item"],
        "05-grid-4.html": ["라인업", "전체", "옵션", "컬러", "lineup", "grid"],
        "06-cta.html": ["cta", "저장", "클릭", "구매", "팔로우", "shop", "save"],
        "04-quote.html": ["인용", "후기", "리뷰", "quote", "review"],
        "07-fullscreen.html": ["풀스크린", "전체화면", "fullscreen"],
        "08-text-heavy.html": ["설명", "가이드", "팁", "guide", "tip"],
        "09-minimal.html": ["미니멀", "심플", "minimal", "simple"],
        "10-bold-typo.html": ["강조", "타이포", "bold", "emphasis"],
        "12-comparison.html": ["비교", "대비", "vs", "comparison"]
    }
    
    # 키워드 매칭
    text = f"{copy_guide} {image_prompt}"
    for pattern, kws in keywords.items():
        if any(kw in text for kw in kws):
            return pattern
    
    # 위치 기반 기본값
    if slide_num == 1:
        return "01-hero.html"
    elif slide_num == 2:
        return "11-overlay.html"
    elif slide_num == 3:
        return "02-split.html"
    elif slide_num >= 10:
        return "06-cta.html"
    else:
        return "03-product.html"


def generate_pattern_mapping(prompts_file: Path) -> Dict[int, str]:
    """
    prompts.json 파일을 읽어서 패턴 매핑 생성
    
    Args:
        prompts_file: prompts.json 파일 경로
    
    Returns:
        {슬라이드 번호: 패턴 파일명} 딕셔너리
    """
    with open(prompts_file) as f:
        prompts = json.load(f)
    
    mapping = {}
    
    for prompt in prompts:
        slide_num = prompt.get("slide")
        if slide_num:
            pattern = auto_detect_pattern(prompt)
            mapping[slide_num] = pattern
    
    return mapping


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_pattern_mapping.py <prompts.json>")
        sys.exit(1)
    
    prompts_file = Path(sys.argv[1])
    
    if not prompts_file.exists():
        print(f"❌ 파일 없음: {prompts_file}")
        sys.exit(1)
    
    print("=" * 70)
    print("🎨 패턴 매핑 자동 생성")
    print("=" * 70)
    print(f"입력: {prompts_file}")
    print()
    
    # 패턴 매핑 생성
    mapping = generate_pattern_mapping(prompts_file)
    
    # 결과 출력
    print("📋 생성된 패턴 매핑:")
    print()
    print(json.dumps(mapping, indent=2, ensure_ascii=False))
    print()
    
    # 통계
    pattern_counts = {}
    for pattern in mapping.values():
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    print("📊 패턴별 사용 개수:")
    for pattern, count in sorted(pattern_counts.items()):
        print(f"  {pattern}: {count}개")
    
    print()
    print("=" * 70)
    print("✅ 완료")
    print("=" * 70)
    
    # JSON 파일로 저장 (선택사항)
    output_file = prompts_file.parent / "pattern_mapping.json"
    with open(output_file, 'w') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"💾 저장: {output_file}")
    
    return mapping


if __name__ == "__main__":
    main()
