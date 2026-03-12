#!/usr/bin/env python3
"""
Imgur 이미지 업로더

Instagram Graph API는 공개 URL만 허용하므로,
로컬 이미지를 Imgur에 업로드하여 공개 URL을 생성합니다.

Setup:
1. https://api.imgur.com/oauth2/addclient 에서 Client ID 발급
2. .env에 IMGUR_CLIENT_ID 추가

Usage:
    python imgur_uploader.py image.png
    python imgur_uploader.py slides/*.png --output urls.txt
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
IMGUR_API_URL = "https://api.imgur.com/3/image"


def upload_image(image_path: str, client_id: str = None) -> Dict:
    """
    Imgur에 이미지 업로드
    
    Args:
        image_path: 이미지 파일 경로
        client_id: Imgur Client ID (생략 시 환경 변수 사용)
    
    Returns:
        {
            "link": "https://i.imgur.com/abc123.png",
            "deletehash": "...",
            "id": "abc123"
        }
    """
    client_id = client_id or IMGUR_CLIENT_ID
    
    if not client_id:
        raise ValueError("IMGUR_CLIENT_ID가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    headers = {"Authorization": f"Client-ID {client_id}"}
    
    with open(image_path, "rb") as f:
        response = requests.post(
            IMGUR_API_URL,
            headers=headers,
            files={"image": f}
        )
    
    response.raise_for_status()
    data = response.json()
    
    if not data["success"]:
        raise RuntimeError(f"Imgur 업로드 실패: {data}")
    
    return data["data"]


def upload_multiple(image_paths: List[str], client_id: str = None) -> List[Dict]:
    """
    여러 이미지를 Imgur에 업로드
    
    Args:
        image_paths: 이미지 파일 경로 리스트
        client_id: Imgur Client ID
    
    Returns:
        [{"path": "...", "link": "...", "id": "..."}, ...]
    """
    results = []
    
    for i, image_path in enumerate(image_paths, 1):
        print(f"[{i}/{len(image_paths)}] {image_path} 업로드 중...")
        
        try:
            data = upload_image(image_path, client_id)
            results.append({
                "path": image_path,
                "link": data["link"],
                "id": data["id"],
                "deletehash": data["deletehash"]
            })
            print(f"  ✅ {data['link']}")
        except Exception as e:
            print(f"  ❌ 실패: {e}")
            results.append({
                "path": image_path,
                "error": str(e)
            })
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Imgur 이미지 업로더")
    parser.add_argument("images", nargs="+", help="이미지 파일 경로")
    parser.add_argument("--output", "-o", help="결과를 저장할 파일 (JSON 또는 TXT)")
    parser.add_argument("--client-id", help="Imgur Client ID (생략 시 환경 변수 사용)")
    
    args = parser.parse_args()
    
    # 이미지 경로 확장 (glob 지원)
    image_paths = []
    for pattern in args.images:
        paths = list(Path().glob(pattern))
        if paths:
            image_paths.extend([str(p) for p in paths])
        else:
            image_paths.append(pattern)
    
    # 중복 제거 및 정렬
    image_paths = sorted(set(image_paths))
    
    if not image_paths:
        print("❌ 업로드할 이미지가 없습니다.")
        sys.exit(1)
    
    print(f"🚀 {len(image_paths)}개 이미지 업로드 시작\n")
    
    # 업로드
    results = upload_multiple(image_paths, args.client_id)
    
    # 결과 저장
    if args.output:
        output_path = Path(args.output)
        
        if output_path.suffix == ".json":
            # JSON 형식
            output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
            print(f"\n💾 결과 저장: {output_path}")
        
        else:
            # TXT 형식 (URL만)
            urls = [r["link"] for r in results if "link" in r]
            output_path.write_text("\n".join(urls))
            print(f"\n💾 URL 저장: {output_path}")
    
    # 요약
    success_count = sum(1 for r in results if "link" in r)
    fail_count = len(results) - success_count
    
    print(f"\n✅ 성공: {success_count}개")
    if fail_count > 0:
        print(f"❌ 실패: {fail_count}개")
    
    # 실패한 파일 목록
    if fail_count > 0:
        print("\n실패한 파일:")
        for r in results:
            if "error" in r:
                print(f"  - {r['path']}: {r['error']}")
    
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
