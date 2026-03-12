#!/usr/bin/env python3
"""
validate_slide.py - 슬라이드 자동 QA 스크립트

검증 항목:
1. Canvas 크기 (1080×1440px)
2. Overflow 체크
3. 폰트 크기 (28px 이상)
4. Design Tokens 사용 여부

사용법:
    python validate_slide.py path/to/slide.html
"""

import sys
import re
from pathlib import Path


def validate_canvas_size(html_content):
    """Canvas 크기 검증"""
    issues = []
    
    # CSS 변수에서 width/height 추출
    canvas_width_match = re.search(r'--canvas-width:\s*(\d+)px', html_content)
    canvas_height_match = re.search(r'--canvas-height:\s*(\d+)px', html_content)
    
    if canvas_width_match:
        width = int(canvas_width_match.group(1))
        if width != 1080:
            issues.append(f"❌ Canvas width: {width}px (expected 1080px)")
    else:
        issues.append("❌ Canvas width variable (--canvas-width) not found")
    
    if canvas_height_match:
        height = int(canvas_height_match.group(1))
        if height != 1440:
            issues.append(f"❌ Canvas height: {height}px (expected 1440px)")
    else:
        issues.append("❌ Canvas height variable (--canvas-height) not found")
    
    # body width/height도 체크
    body_width_match = re.search(r'body\s*{[^}]*width:\s*var\(--canvas-width\)', html_content, re.DOTALL)
    body_height_match = re.search(r'body\s*{[^}]*height:\s*var\(--canvas-height\)', html_content, re.DOTALL)
    
    if not body_width_match:
        issues.append("⚠️  body width should use var(--canvas-width)")
    
    if not body_height_match:
        issues.append("⚠️  body height should use var(--canvas-height)")
    
    return issues


def validate_overflow(html_content):
    """Overflow 검증"""
    issues = []
    
    # overflow: hidden 체크
    if 'overflow: hidden' not in html_content and 'overflow:hidden' not in html_content:
        issues.append("⚠️  Overflow 속성 누락 (권장: overflow: hidden)")
    
    return issues


def validate_font_size(html_content):
    """폰트 크기 검증 (28px 이상)"""
    issues = []
    
    # font-size 값 추출
    font_sizes = re.findall(r'font-size:\s*(\d+)px', html_content)
    
    for size in font_sizes:
        if int(size) < 28:
            issues.append(f"❌ Font size: {size}px (minimum 28px required)")
    
    return issues


def validate_design_tokens(html_content):
    """Design Tokens 사용 여부 검증"""
    issues = []
    
    # var(--color-...) 또는 var(--font-...) 패턴 체크
    has_color_tokens = re.search(r'var\(--color-', html_content)
    has_font_tokens = re.search(r'var\(--font-', html_content)
    
    if not has_color_tokens:
        issues.append("⚠️  Design token 미사용 (색상): var(--color-...) 권장")
    
    if not has_font_tokens:
        issues.append("⚠️  Design token 미사용 (폰트): var(--font-...) 권장")
    
    return issues


def validate_external_resources(html_content):
    """외부 리소스 참조 체크"""
    issues = []
    
    # CDN/외부 URL 체크
    if re.search(r'https?://(?!localhost)', html_content):
        # data: URL은 허용
        if 'data:image' not in html_content:
            issues.append("❌ 외부 URL 참조 발견 (스탠드얼론 HTML 위반)")
    
    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_slide.py <slide.html>")
        sys.exit(1)
    
    html_file = Path(sys.argv[1])
    
    if not html_file.exists():
        print(f"❌ File not found: {html_file}")
        sys.exit(1)
    
    html_content = html_file.read_text()
    
    print("=" * 70)
    print(f"🔍 Validating: {html_file.name}")
    print("=" * 70)
    print()
    
    all_issues = []
    
    # 1. Canvas 크기
    canvas_issues = validate_canvas_size(html_content)
    all_issues.extend(canvas_issues)
    
    # 2. Overflow
    overflow_issues = validate_overflow(html_content)
    all_issues.extend(overflow_issues)
    
    # 3. 폰트 크기
    font_issues = validate_font_size(html_content)
    all_issues.extend(font_issues)
    
    # 4. Design Tokens
    token_issues = validate_design_tokens(html_content)
    all_issues.extend(token_issues)
    
    # 5. 외부 리소스
    external_issues = validate_external_resources(html_content)
    all_issues.extend(external_issues)
    
    # 결과 출력
    if not all_issues:
        print("✅ All checks passed!")
        print()
        sys.exit(0)
    else:
        print("Issues found:")
        print()
        
        critical = [i for i in all_issues if i.startswith("❌")]
        warnings = [i for i in all_issues if i.startswith("⚠️")]
        
        if critical:
            print("🚨 Critical (고 심각도):")
            for issue in critical:
                print(f"  {issue}")
            print()
        
        if warnings:
            print("⚠️  Warnings (중 심각도):")
            for issue in warnings:
                print(f"  {issue}")
            print()
        
        print(f"Total issues: {len(all_issues)} ({len(critical)} critical, {len(warnings)} warnings)")
        print()
        
        # Critical 이슈가 있으면 exit code 1
        sys.exit(1 if critical else 0)


if __name__ == "__main__":
    main()
