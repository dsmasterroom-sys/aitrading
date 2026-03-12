#!/usr/bin/env python3
"""
OpenClaw Cron 자동화 설정

목표:
- 주간 콘텐츠 자동 생성 일정 등록
- 성과 추적 자동화
- 토큰 자동 갱신

사용법:
    python scripts/setup_cron_jobs.py --schedule-type weekly
    python scripts/setup_cron_jobs.py --schedule-type daily-test
"""

import argparse
import json
import sys
from datetime import datetime, timedelta


def create_carousel_job(day_of_week, hour, minute, timezone="Asia/Seoul"):
    """
    캐러셀 자동 생성 Cron Job
    
    Args:
        day_of_week: 요일 (MON, TUE, WED, THU, FRI, SAT, SUN)
        hour: 시 (0-23)
        minute: 분 (0-59)
        timezone: 타임존
    
    Returns:
        dict: Cron job 설정
    """
    
    # Cron 표현식: 분 시 일 월 요일
    # 매주 특정 요일 특정 시간
    cron_expr = f"{minute} {hour} * * {day_of_week}"
    
    return {
        "name": f"Carousel Auto-Gen ({day_of_week} {hour:02d}:{minute:02d})",
        "schedule": {
            "kind": "cron",
            "expr": cron_expr,
            "tz": timezone
        },
        "payload": {
            "kind": "agentTurn",
            "message": "인스타 캐러셀 자동 생성 실행. 트렌드 조사 후 아이템 매칭하고 10슬라이드 생성.",
            "model": "claude-sonnet-4-6",
            "timeoutSeconds": 7200  # 2시간
        },
        "delivery": {
            "mode": "announce",
            "channel": "webchat",  # 또는 telegram, discord 등
            "bestEffort": True
        },
        "sessionTarget": "isolated",
        "enabled": True
    }


def create_reels_job(day_of_week, hour, minute, timezone="Asia/Seoul"):
    """
    릴스 자동 생성 Cron Job
    
    Args:
        day_of_week: 요일
        hour: 시
        minute: 분
        timezone: 타임존
    
    Returns:
        dict: Cron job 설정
    """
    
    cron_expr = f"{minute} {hour} * * {day_of_week}"
    
    return {
        "name": f"Reels Auto-Gen ({day_of_week} {hour:02d}:{minute:02d})",
        "schedule": {
            "kind": "cron",
            "expr": cron_expr,
            "tz": timezone
        },
        "payload": {
            "kind": "agentTurn",
            "message": "인스타 릴스 자동 생성 실행. 트렌드 조사 후 5초 릴스 생성.",
            "model": "claude-sonnet-4-6",
            "timeoutSeconds": 10800  # 3시간
        },
        "delivery": {
            "mode": "announce",
            "channel": "webchat",
            "bestEffort": True
        },
        "sessionTarget": "isolated",
        "enabled": True
    }


def create_insights_tracking_job(media_id, publish_time, tracking_hours=24):
    """
    성과 추적 Cron Job
    
    Args:
        media_id: Instagram 미디어 ID
        publish_time: 발행 시간 (ISO 8601)
        tracking_hours: 추적 시간 (24, 168 등)
    
    Returns:
        dict: Cron job 설정
    """
    
    publish_dt = datetime.fromisoformat(publish_time)
    tracking_dt = publish_dt + timedelta(hours=tracking_hours)
    
    return {
        "name": f"Insights {media_id} ({tracking_hours}h)",
        "schedule": {
            "kind": "at",
            "at": tracking_dt.isoformat()
        },
        "payload": {
            "kind": "systemEvent",
            "text": f"Instagram 성과 조회 실행: {media_id} ({tracking_hours}시간 경과)"
        },
        "sessionTarget": "main",
        "enabled": True
    }


def create_token_refresh_job(interval_days=50, timezone="Asia/Seoul"):
    """
    Access Token 자동 갱신 Cron Job
    
    Args:
        interval_days: 갱신 주기 (기본 50일, 60일 만료 전)
        timezone: 타임존
    
    Returns:
        dict: Cron job 설정
    """
    
    interval_ms = interval_days * 24 * 60 * 60 * 1000
    
    return {
        "name": "Instagram Token Refresh",
        "schedule": {
            "kind": "every",
            "everyMs": interval_ms,
            "anchorMs": int(datetime.now().timestamp() * 1000)
        },
        "payload": {
            "kind": "systemEvent",
            "text": "⚠️ Instagram Access Token 갱신 필요! 50일 경과."
        },
        "sessionTarget": "main",
        "enabled": True
    }


def create_weekly_schedule():
    """
    주간 스케줄 생성 (캐러셀 3회, 릴스 2회)
    
    Returns:
        list: Cron jobs 리스트
    """
    
    jobs = []
    
    # 캐러셀: 월/수/금 10:00
    jobs.append(create_carousel_job("MON", 10, 0))
    jobs.append(create_carousel_job("WED", 10, 0))
    jobs.append(create_carousel_job("FRI", 10, 0))
    
    # 릴스: 화/목 15:00
    jobs.append(create_reels_job("TUE", 15, 0))
    jobs.append(create_reels_job("THU", 15, 0))
    
    return jobs


def create_daily_test_schedule():
    """
    일일 테스트 스케줄 (매일 1회)
    
    Returns:
        list: Cron jobs 리스트
    """
    
    jobs = []
    
    # 캐러셀: 매일 09:00
    jobs.append(create_carousel_job("*", 9, 0))
    
    return jobs


def print_cron_setup_guide(jobs):
    """
    OpenClaw Cron 설정 가이드 출력
    
    Args:
        jobs: Cron jobs 리스트
    """
    
    print("\n" + "=" * 70)
    print("📅 OpenClaw Cron Jobs 설정")
    print("=" * 70)
    print()
    print(f"총 {len(jobs)}개 Job 생성됨:")
    print()
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['name']}")
        schedule = job['schedule']
        if schedule['kind'] == 'cron':
            print(f"   일정: {schedule['expr']} ({schedule['tz']})")
        elif schedule['kind'] == 'every':
            days = schedule['everyMs'] / (24 * 60 * 60 * 1000)
            print(f"   일정: 매 {days:.0f}일")
        elif schedule['kind'] == 'at':
            print(f"   일정: {schedule['at']}")
        print()
    
    print("=" * 70)
    print("📋 OpenClaw에 등록하는 방법:")
    print("=" * 70)
    print()
    print("방법 1: Python (권장)")
    print("-" * 70)
    print("```python")
    print("# OpenClaw 세션에서 실행")
    print("jobs = [")
    for job in jobs:
        print(f"    {json.dumps(job, ensure_ascii=False, indent=4)},")
    print("]")
    print()
    print("for job in jobs:")
    print("    cron(action='add', job=job)")
    print("```")
    print()
    
    print("방법 2: JSON 파일로 저장 후 수동 등록")
    print("-" * 70)
    print("1. 아래 JSON을 cron_jobs.json에 저장")
    print("2. OpenClaw UI 또는 API로 등록")
    print()
    print(json.dumps(jobs, ensure_ascii=False, indent=2))
    print()


def main():
    parser = argparse.ArgumentParser(description='OpenClaw Cron 자동화 설정')
    parser.add_argument(
        '--schedule-type',
        choices=['weekly', 'daily-test', 'token-refresh'],
        default='weekly',
        help='스케줄 타입'
    )
    parser.add_argument('--output', help='JSON 파일로 저장 (옵션)')
    
    args = parser.parse_args()
    
    print()
    print("=" * 70)
    print("🤖 Instagram 자동화 Cron Jobs 생성")
    print("=" * 70)
    print()
    
    # 스케줄 타입별 생성
    if args.schedule_type == 'weekly':
        jobs = create_weekly_schedule()
        print("📅 주간 스케줄 (캐러셀 3회, 릴스 2회)")
    
    elif args.schedule_type == 'daily-test':
        jobs = create_daily_test_schedule()
        print("🧪 일일 테스트 스케줄 (캐러셀 1회)")
    
    elif args.schedule_type == 'token-refresh':
        jobs = [create_token_refresh_job()]
        print("🔑 Token 갱신 스케줄 (50일마다)")
    
    # JSON 파일로 저장 (옵션)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"\n💾 저장 완료: {args.output}")
    
    # 설정 가이드 출력
    print_cron_setup_guide(jobs)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
