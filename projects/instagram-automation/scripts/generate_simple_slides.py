#!/usr/bin/env python3
"""
간단한 텍스트 이미지 슬라이드 생성 (Pillow)
HTML/Puppeteer 없이 빠르게 테스트용 이미지 생성
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_slide_1(output_path, width=1080, height=1440):
    """Slide 1: 훅 - 문제 제기"""
    
    img = Image.new('RGB', (width, height), color='#FF2D78')  # 핑크
    draw = ImageDraw.Draw(img)
    
    # 폰트 (한글 지원)
    try:
        # macOS 시스템 한글 폰트
        font_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 80)
        font_body = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 40)
        font_small = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 24)
    except:
        # 대체 폰트
        try:
            font_title = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 80)
            font_body = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 40)
            font_small = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 24)
        except:
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 텍스트
    title = "출근할 때\n가방 무거워서\n어깨 아프신가요?"
    subtitle = "초경량 196g 솔루션"
    watermark = "@genarchive.kr"
    
    # 제목 (중앙)
    bbox = draw.textbbox((0, 0), title, font=font_title, align='center')
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 100
    
    # 검은 배경 박스
    padding = 30
    draw.rectangle([x - padding, y - padding, x + text_width + padding, y + text_height + padding], 
                   fill='#00FF41', outline='#000000', width=4)
    
    draw.text((x, y), title, fill='#000000', font=font_title, align='center')
    
    # 부제
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_body)
    text_width2 = bbox2[2] - bbox2[0]
    x2 = (width - text_width2) // 2
    y2 = y + text_height + 100
    draw.text((x2, y2), subtitle, fill='#FFFFFF', font=font_body)
    
    # 워터마크
    draw.text((width - 250, height - 50), watermark, fill='#FFFFFF', font=font_small)
    
    img.save(output_path)
    print(f"✅ Slide 1 생성: {output_path}")


def create_slide_2(output_path, width=1080, height=1440):
    """Slide 2: 솔루션 - 제품 소개"""
    
    img = Image.new('RGB', (width, height), color='#FFE600')  # 옐로우
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 70)
        font_body = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 36)
        font_badge = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 32)
    except:
        try:
            font_title = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 70)
            font_body = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 36)
            font_badge = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 32)
        except:
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_badge = ImageFont.load_default()
    
    # 텍스트
    title = "초경량 196g\n미니 크로스백"
    features = [
        "✓ 깃털처럼 가벼운 196g",
        "✓ 슬림한 디자인",
        "✓ 출근/데이트 올라운더",
        "✓ 가성비 끝판왕"
    ]
    badge = "한정 특가"
    
    # 제목
    bbox = draw.textbbox((0, 0), title, font=font_title, align='center')
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = 200
    draw.text((x, y), title, fill='#000000', font=font_title, align='center')
    
    # 특징
    y_feature = y + text_height + 80
    for feature in features:
        bbox_f = draw.textbbox((0, 0), feature, font=font_body)
        text_width_f = bbox_f[2] - bbox_f[0]
        x_f = (width - text_width_f) // 2
        draw.text((x_f, y_feature), feature, fill='#1A1A1A', font=font_body)
        y_feature += 70
    
    # 뱃지
    badge_y = height - 250
    bbox_badge = draw.textbbox((0, 0), badge, font=font_badge)
    badge_width = bbox_badge[2] - bbox_badge[0]
    badge_x = (width - badge_width) // 2
    
    draw.rectangle([badge_x - 40, badge_y - 20, badge_x + badge_width + 40, badge_y + 50],
                   fill='#FF1A1A', outline='#000000', width=4)
    draw.text((badge_x, badge_y), badge, fill='#FFFFFF', font=font_badge)
    
    img.save(output_path)
    print(f"✅ Slide 2 생성: {output_path}")


def create_slide_3(output_path, width=1080, height=1440):
    """Slide 3: CTA"""
    
    img = Image.new('RGB', (width, height), color='#000000')  # 블랙
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 90)
        font_cta = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 50)
        font_small = ImageFont.truetype('/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc', 30)
    except:
        try:
            font_title = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 90)
            font_cta = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 50)
            font_small = ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', 30)
        except:
            font_title = ImageFont.load_default()
            font_cta = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 텍스트
    title = "지금 바로\n확인하세요!"
    cta = "SHOP NOW"
    subtitle = "프로필 링크 👆"
    
    # 제목
    bbox = draw.textbbox((0, 0), title, font=font_title, align='center')
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = 350
    draw.text((x, y), title, fill='#FFFFFF', font=font_title, align='center')
    
    # CTA 버튼
    cta_y = y + text_height + 120
    bbox_cta = draw.textbbox((0, 0), cta, font=font_cta)
    cta_width = bbox_cta[2] - bbox_cta[0]
    cta_x = (width - cta_width) // 2
    
    draw.rectangle([cta_x - 60, cta_y - 30, cta_x + cta_width + 60, cta_y + 80],
                   fill='#00FF41', outline='#FFFFFF', width=4)
    draw.text((cta_x, cta_y), cta, fill='#000000', font=font_cta)
    
    # 부제
    subtitle_y = cta_y + 150
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_small)
    sub_width = bbox_sub[2] - bbox_sub[0]
    sub_x = (width - sub_width) // 2
    draw.text((sub_x, subtitle_y), subtitle, fill='#FFFFFF', font=font_small)
    
    img.save(output_path)
    print(f"✅ Slide 3 생성: {output_path}")


def main():
    output_dir = Path("/Users/master/.openclaw/workspace/projects/instagram-automation/content/20260306_spring_bag/slides")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("🎨 슬라이드 이미지 생성 중...")
    print("=" * 70)
    print()
    
    create_slide_1(output_dir / "slide_01.png")
    create_slide_2(output_dir / "slide_02.png")
    create_slide_3(output_dir / "slide_03.png")
    
    print()
    print("=" * 70)
    print("✅ 완료! 3개 슬라이드 생성")
    print("=" * 70)


if __name__ == "__main__":
    main()
