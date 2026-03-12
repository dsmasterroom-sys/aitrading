#!/usr/bin/env python3
"""
Instagram Graph API 연동 스크립트

기능:
- 캐러셀 발행
- 릴스 발행
- 스토리 발행
- 미디어 업로드
- 성과 조회

Requirements:
- Instagram Business Account
- Facebook Page 연결
- Access Token (User Token → Page Token)

Setup:
1. Meta for Developers에서 App 생성
2. Instagram Graph API 권한 설정
3. Access Token 발급
4. .env에 저장
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# .env 로드
load_dotenv()

# API 설정
GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# 환경 변수
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")


class InstagramAPI:
    """Instagram Graph API 래퍼"""
    
    def __init__(self, access_token: Optional[str] = None, account_id: Optional[str] = None):
        self.access_token = access_token or ACCESS_TOKEN
        self.account_id = account_id or INSTAGRAM_ACCOUNT_ID
        
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN이 설정되지 않았습니다. .env 파일을 확인하세요.")
        if not self.account_id:
            raise ValueError("INSTAGRAM_ACCOUNT_ID가 설정되지 않았습니다.")
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """API 요청 헬퍼"""
        url = f"{GRAPH_API_BASE}/{endpoint}"
        kwargs.setdefault("params", {})["access_token"] = self.access_token
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    # ========== 미디어 컨테이너 생성 ==========
    
    def create_image_container(
        self,
        image_url: str,
        caption: Optional[str] = None,
        is_carousel_item: bool = False
    ) -> str:
        """
        이미지 컨테이너 생성
        
        Args:
            image_url: 이미지 URL (공개 접근 가능)
            caption: 캡션 (캐러셀 아이템은 불가)
            is_carousel_item: 캐러셀 아이템 여부
        
        Returns:
            container_id
        """
        endpoint = f"{self.account_id}/media"
        data = {
            "image_url": image_url,
            "is_carousel_item": is_carousel_item
        }
        
        if caption and not is_carousel_item:
            data["caption"] = caption
        
        result = self._request("POST", endpoint, data=data)
        return result["id"]
    
    def create_carousel_container(
        self,
        children: List[str],
        caption: str
    ) -> str:
        """
        캐러셀 컨테이너 생성
        
        Args:
            children: 자식 컨테이너 ID 리스트 (최대 10개)
            caption: 캡션
        
        Returns:
            container_id
        """
        if len(children) > 10:
            raise ValueError("캐러셀은 최대 10개 슬라이드만 가능합니다.")
        
        endpoint = f"{self.account_id}/media"
        data = {
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "caption": caption
        }
        
        result = self._request("POST", endpoint, data=data)
        return result["id"]
    
    def create_video_container(
        self,
        video_url: str,
        caption: Optional[str] = None,
        media_type: str = "REELS"
    ) -> str:
        """
        비디오 컨테이너 생성
        
        Args:
            video_url: 비디오 URL (공개 접근 가능)
            caption: 캡션
            media_type: REELS 또는 VIDEO
        
        Returns:
            container_id
        """
        endpoint = f"{self.account_id}/media"
        data = {
            "media_type": media_type,
            "video_url": video_url
        }
        
        if caption:
            data["caption"] = caption
        
        result = self._request("POST", endpoint, data=data)
        return result["id"]
    
    # ========== 발행 ==========
    
    def publish_media(self, container_id: str) -> str:
        """
        미디어 발행
        
        Args:
            container_id: 컨테이너 ID
        
        Returns:
            media_id
        """
        endpoint = f"{self.account_id}/media_publish"
        data = {"creation_id": container_id}
        
        result = self._request("POST", endpoint, data=data)
        return result["id"]
    
    def check_container_status(self, container_id: str) -> Dict:
        """
        컨테이너 상태 확인
        
        Args:
            container_id: 컨테이너 ID
        
        Returns:
            {"status_code": "FINISHED|IN_PROGRESS|ERROR"}
        """
        endpoint = f"{container_id}"
        params = {"fields": "status_code"}
        
        return self._request("GET", endpoint, params=params)
    
    # ========== 통합 헬퍼 ==========
    
    def publish_carousel(
        self,
        image_urls: List[str],
        caption: str,
        wait_for_ready: bool = True
    ) -> str:
        """
        캐러셀 발행 (원스톱)
        
        Args:
            image_urls: 이미지 URL 리스트 (최대 10개)
            caption: 캡션
            wait_for_ready: 컨테이너 준비 대기 여부
        
        Returns:
            media_id
        """
        print(f"📸 캐러셀 발행 시작 ({len(image_urls)}장)")
        
        # 1. 각 이미지의 컨테이너 생성
        children = []
        for i, image_url in enumerate(image_urls, 1):
            print(f"  [{i}/{len(image_urls)}] 컨테이너 생성 중...")
            child_id = self.create_image_container(image_url, is_carousel_item=True)
            children.append(child_id)
            time.sleep(0.5)  # Rate limit 방지
        
        # 2. 캐러셀 컨테이너 생성
        print(f"  캐러셀 컨테이너 생성 중...")
        carousel_id = self.create_carousel_container(children, caption)
        
        # 3. 컨테이너 준비 대기
        if wait_for_ready:
            print(f"  컨테이너 준비 대기 중...")
            self._wait_until_ready(carousel_id, timeout=300)
        
        # 4. 발행
        print(f"  발행 중...")
        media_id = self.publish_media(carousel_id)
        
        print(f"✅ 캐러셀 발행 완료: {media_id}")
        return media_id
    
    def publish_reels(
        self,
        video_url: str,
        caption: str,
        wait_for_ready: bool = True
    ) -> str:
        """
        릴스 발행 (원스톱)
        
        Args:
            video_url: 비디오 URL
            caption: 캡션
            wait_for_ready: 컨테이너 준비 대기 여부
        
        Returns:
            media_id
        """
        print(f"🎬 릴스 발행 시작")
        
        # 1. 비디오 컨테이너 생성
        print(f"  컨테이너 생성 중...")
        container_id = self.create_video_container(video_url, caption, media_type="REELS")
        
        # 2. 컨테이너 준비 대기 (비디오는 시간이 오래 걸림)
        if wait_for_ready:
            print(f"  컨테이너 준비 대기 중 (최대 10분)...")
            self._wait_until_ready(container_id, timeout=600)
        
        # 3. 발행
        print(f"  발행 중...")
        media_id = self.publish_media(container_id)
        
        print(f"✅ 릴스 발행 완료: {media_id}")
        return media_id
    
    def _wait_until_ready(self, container_id: str, timeout: int = 300) -> None:
        """컨테이너가 준비될 때까지 대기"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.check_container_status(container_id)
            status_code = status.get("status_code")
            
            if status_code == "FINISHED":
                return
            elif status_code == "ERROR":
                raise RuntimeError(f"컨테이너 생성 실패: {container_id}")
            
            time.sleep(5)  # 5초마다 체크
        
        raise TimeoutError(f"컨테이너 준비 타임아웃: {container_id}")
    
    # ========== 성과 조회 ==========
    
    def get_media_insights(
        self,
        media_id: str,
        metrics: Optional[List[str]] = None
    ) -> Dict:
        """
        미디어 성과 조회
        
        Args:
            media_id: 미디어 ID
            metrics: 조회할 메트릭 리스트
                     (impressions, reach, likes, comments, saves, shares)
        
        Returns:
            {"data": [{"name": "impressions", "values": [...]}]}
        """
        if metrics is None:
            metrics = ["impressions", "reach", "likes", "comments", "saves"]
        
        endpoint = f"{media_id}/insights"
        params = {"metric": ",".join(metrics)}
        
        return self._request("GET", endpoint, params=params)
    
    def get_account_insights(
        self,
        metrics: Optional[List[str]] = None,
        period: str = "day"
    ) -> Dict:
        """
        계정 성과 조회
        
        Args:
            metrics: 조회할 메트릭 리스트
                     (impressions, reach, profile_views, follower_count)
            period: day, week, days_28
        
        Returns:
            {"data": [{"name": "impressions", "period": "day", "values": [...]}]}
        """
        if metrics is None:
            metrics = ["impressions", "reach", "profile_views"]
        
        endpoint = f"{self.account_id}/insights"
        params = {
            "metric": ",".join(metrics),
            "period": period
        }
        
        return self._request("GET", endpoint, params=params)
    
    # ========== 미디어 조회 ==========
    
    def get_recent_media(self, limit: int = 10) -> List[Dict]:
        """
        최근 미디어 조회
        
        Args:
            limit: 조회할 개수
        
        Returns:
            [{"id": "...", "media_type": "...", "caption": "..."}]
        """
        endpoint = f"{self.account_id}/media"
        params = {
            "fields": "id,media_type,media_url,caption,timestamp,permalink",
            "limit": limit
        }
        
        result = self._request("GET", endpoint, params=params)
        return result.get("data", [])


# ========== CLI ==========

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Instagram Graph API CLI")
    subparsers = parser.add_subparsers(dest="command", help="명령어")
    
    # publish carousel
    carousel_parser = subparsers.add_parser("publish-carousel", help="캐러셀 발행")
    carousel_parser.add_argument("--images", nargs="+", required=True, help="이미지 URL 리스트")
    carousel_parser.add_argument("--caption", required=True, help="캡션")
    
    # publish reels
    reels_parser = subparsers.add_parser("publish-reels", help="릴스 발행")
    reels_parser.add_argument("--video", required=True, help="비디오 URL")
    reels_parser.add_argument("--caption", required=True, help="캡션")
    
    # insights
    insights_parser = subparsers.add_parser("insights", help="성과 조회")
    insights_parser.add_argument("--media-id", help="미디어 ID (생략 시 계정 전체)")
    
    # recent media
    subparsers.add_parser("recent", help="최근 미디어 조회")
    
    args = parser.parse_args()
    
    api = InstagramAPI()
    
    if args.command == "publish-carousel":
        media_id = api.publish_carousel(args.images, args.caption)
        print(f"Media ID: {media_id}")
    
    elif args.command == "publish-reels":
        media_id = api.publish_reels(args.video, args.caption)
        print(f"Media ID: {media_id}")
    
    elif args.command == "insights":
        if args.media_id:
            insights = api.get_media_insights(args.media_id)
        else:
            insights = api.get_account_insights()
        print(json.dumps(insights, indent=2, ensure_ascii=False))
    
    elif args.command == "recent":
        media_list = api.get_recent_media()
        print(json.dumps(media_list, indent=2, ensure_ascii=False))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
