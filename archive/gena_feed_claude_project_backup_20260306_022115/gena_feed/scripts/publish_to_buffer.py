#!/usr/bin/env python3
"""
Buffer 예약 발행 자동화 스크립트 (@gena_feed)

기능
- Buffer API v1 연동
- 인스타그램 프로필 ID 자동 탐색
- 발행 타입: carousel / reels / story / auto-schedule
- 예약 목록 확인(--list), 예약 취소(--cancel)
- G3 게이팅 자동 검증
- dry-run 지원

사용 예시
  python scripts/publish_to_buffer.py --type carousel --date "2026-03-05 12:00"
  python scripts/publish_to_buffer.py --type reels --date "2026-03-07 19:00"
  python scripts/publish_to_buffer.py --type story --date "2026-03-04 19:00"
  python scripts/publish_to_buffer.py --auto-schedule
  python scripts/publish_to_buffer.py --list
  python scripts/publish_to_buffer.py --cancel <update_id>
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import requests
except Exception as e:  # pragma: no cover
    print("[오류] requests 패키지가 필요합니다. 예: pip install requests", file=sys.stderr)
    raise

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

try:
    import pytz

    KST = pytz.timezone("Asia/Seoul")

    def ensure_kst(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return KST.localize(dt)
        return dt.astimezone(KST)

except Exception:
    from zoneinfo import ZoneInfo

    KST = ZoneInfo("Asia/Seoul")

    def ensure_kst(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=KST)
        return dt.astimezone(KST)


BASE_DIR = Path(__file__).resolve().parents[1]  # gena_feed/
API_BASE = "https://api.bufferapp.com/1"

REELS_HASHTAGS = [
    "#릴스",
    "#reels",
    "#인스타릴스",
    "#gena_feed",
]


class AppError(Exception):
    pass


@dataclass
class SchedulePayload:
    post_type: str
    scheduled_at: datetime
    text: str
    media_files: List[Path]


class BufferClient:
    def __init__(self, token: str, dry_run: bool = False) -> None:
        self.token = token
        self.dry_run = dry_run

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        params = dict(params or {})
        params["access_token"] = self.token
        url = f"{API_BASE}{endpoint}"
        resp = requests.get(url, params=params, timeout=30)
        self._raise_if_error(resp)
        return resp.json()

    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        data = dict(data or {})
        data["access_token"] = self.token
        url = f"{API_BASE}{endpoint}"
        resp = requests.post(url, data=data, timeout=60)
        self._raise_if_error(resp)
        return resp.json()

    @staticmethod
    def _raise_if_error(resp: requests.Response) -> None:
        if resp.status_code >= 400:
            msg = resp.text
            try:
                j = resp.json()
                msg = j.get("message") or j.get("error") or msg
            except Exception:
                pass
            raise AppError(f"Buffer API 오류({resp.status_code}): {msg}")

    def get_instagram_profile_id(self) -> str:
        profiles = self._get("/profiles.json")
        if not isinstance(profiles, list):
            raise AppError("Buffer 프로필 목록 형식이 올바르지 않습니다.")

        # 우선순위: instagram_business -> instagram
        for wanted in ("instagram_business", "instagram"):
            for p in profiles:
                if str(p.get("service", "")).lower() == wanted:
                    return p.get("id")

        # fallback: service명이 instagram 포함
        for p in profiles:
            if "instagram" in str(p.get("service", "")).lower():
                return p.get("id")

        raise AppError("인스타그램 프로필을 찾지 못했습니다. Buffer에서 인스타그램 계정을 먼저 연결하세요.")

    def create_update(self, profile_id: str, text: str, media_file: Path, scheduled_at: datetime) -> Any:
        b64 = file_to_data_url(media_file)
        data: Dict[str, Any] = {
            "profile_ids[]": profile_id,
            "text": text,
            "scheduled_at": scheduled_at.isoformat(),
            "media[photo]": b64,
        }

        if self.dry_run:
            return {
                "dry_run": True,
                "endpoint": "/updates/create.json",
                "payload_preview": {
                    "profile_ids[]": profile_id,
                    "text": text[:200] + ("..." if len(text) > 200 else ""),
                    "scheduled_at": scheduled_at.isoformat(),
                    "media_file": str(media_file),
                    "media_data_url_prefix": b64[:40] + "...",
                },
            }

        return self._post("/updates/create.json", data=data)

    def list_pending(self, profile_id: str) -> Any:
        return self._get(f"/profiles/{profile_id}/updates/pending.json")

    def cancel_update(self, update_id: str) -> Any:
        if self.dry_run:
            return {"dry_run": True, "endpoint": f"/updates/{update_id}/destroy.json", "update_id": update_id}
        return self._post(f"/updates/{update_id}/destroy.json")


def load_env() -> str:
    env_path = BASE_DIR / ".env"
    if load_dotenv:
        load_dotenv(env_path)
    token = os.getenv("BUFFER_API_KEY")
    if not token:
        raise AppError(".env에 BUFFER_API_KEY를 설정하세요")
    return token


def parse_datetime_kst(date_str: str) -> datetime:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return ensure_kst(dt)
    except ValueError:
        raise AppError("날짜 형식이 올바르지 않습니다. 예: '2026-03-05 12:00'")


def next_weekday_at(base_dt: datetime, weekday: int, hour: int, minute: int) -> datetime:
    # Monday=0 ... Sunday=6
    base_dt = ensure_kst(base_dt)
    days_ahead = (weekday - base_dt.weekday()) % 7
    candidate = (base_dt + timedelta(days=days_ahead)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= base_dt:
        candidate += timedelta(days=7)
    return candidate


def file_to_data_url(path: Path) -> str:
    if not path.exists():
        raise AppError(f"파일이 없습니다: {path}")
    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
    }.get(suffix, "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def read_text(path: Path) -> str:
    if not path.exists():
        raise AppError(f"파일이 없습니다: {path}")
    return path.read_text(encoding="utf-8")


def parse_copy_md(copy_md_path: Path) -> Tuple[str, str]:
    """weekly/copy.md에서 본문/해시태그를 느슨하게 파싱"""
    text = read_text(copy_md_path)

    # 1) '해시태그' 섹션이 있으면 분리
    m = re.search(r"(?is)(.*?)(?:^|\n)\s*#+\s*해시태그\s*\n(.*)$", text)
    if m:
        body = m.group(1).strip()
        tags = m.group(2).strip()
        return body, normalize_hashtags(tags)

    # 2) 줄 기준 #시작 토큰 모아 해시태그로 간주
    lines = [ln.rstrip() for ln in text.splitlines()]
    tag_lines = [ln for ln in lines if re.search(r"(^|\s)#\w+", ln)]
    if tag_lines:
        tags = normalize_hashtags("\n".join(tag_lines))
        body_lines = [ln for ln in lines if ln not in tag_lines]
        return "\n".join(body_lines).strip(), tags

    return text.strip(), ""


def normalize_hashtags(text: str) -> str:
    tags = re.findall(r"#\S+", text)
    if not tags:
        return text.strip()
    uniq = []
    seen = set()
    for t in tags:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return " ".join(uniq)


def parse_scene_plan_caption(scene_plan_path: Path) -> str:
    raw = read_text(scene_plan_path)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise AppError(f"JSON 파싱 실패: {scene_plan_path}")

    for key in ("caption", "post_caption", "instagram_caption", "ig_caption"):
        v = data.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()

    # nested fallback
    post = data.get("post") if isinstance(data, dict) else None
    if isinstance(post, dict):
        v = post.get("caption")
        if isinstance(v, str) and v.strip():
            return v.strip()

    raise AppError("weekly/scene-plan.json에서 릴스 캡션 필드를 찾지 못했습니다. (caption/post_caption 등)")


def validate_g3_gate(post_type: Optional[str], root: Path) -> None:
    errors: List[str] = []

    qa = root / "weekly" / "qa-report.md"
    if not qa.exists():
        errors.append("weekly/qa-report.md 파일이 없습니다.")
    else:
        qa_text = qa.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"고\s*이슈\s*[:：]?\s*[1-9]", qa_text) or re.search(r"High\s*[:：]?\s*[1-9]", qa_text, re.I):
            errors.append("qa-report.md에 고(High) 이슈가 1건 이상 있습니다.")
        if re.search(r"중\s*이슈\s*[:：]?\s*[1-9]", qa_text) or re.search(r"Medium\s*[:：]?\s*[1-9]", qa_text, re.I):
            errors.append("qa-report.md에 중(Medium) 이슈가 1건 이상 있습니다.")

    copy_md = root / "weekly" / "copy.md"
    scene_json = root / "weekly" / "scene-plan.json"

    def check_slant_and_ad_disclosure(content: str, source: str) -> None:
        lowered = content.lower()
        if "slant" in lowered:
            if not ("링크바이오" in content or "link in bio" in lowered or "bio 링크" in content):
                errors.append(f"{source}: slant 언급은 있으나 링크바이오 안내가 없습니다.")
        # L3일 때 광고표기 필요(휴리스틱): 문서 내 L3/광고 문맥이 있으면 '#광고' 또는 '#ad' 확인
        if re.search(r"\bL3\b", content, re.I) or "광고" in content:
            if not (re.search(r"#광고\b", content) or re.search(r"#ad\b", lowered) or "유료광고" in content):
                errors.append(f"{source}: L3/광고 문맥이 있으나 광고 표기가 없습니다. (#광고/#ad/유료광고)")

    if copy_md.exists():
        check_slant_and_ad_disclosure(copy_md.read_text(encoding="utf-8", errors="ignore"), "weekly/copy.md")
    if scene_json.exists():
        check_slant_and_ad_disclosure(scene_json.read_text(encoding="utf-8", errors="ignore"), "weekly/scene-plan.json")

    # 산출물 파일 체크
    output = root / "output"
    if post_type in ("carousel", "auto", None):
        slides = sorted((output / "slides").glob("*.png"))
        if len(slides) < 1:
            errors.append("캐러셀 산출물 없음: output/slides/*.png")
        elif len(slides) != 9:
            errors.append(f"캐러셀 이미지는 9장을 권장합니다. 현재 {len(slides)}장")
    if post_type in ("reels", "auto", None):
        reel = output / "reels" / "final.mp4"
        if not reel.exists():
            errors.append("릴스 산출물 없음: output/reels/final.mp4")
    if post_type in ("story", "auto", None):
        for name in ("story-d1.png", "story-d0.png", "story-d3.png"):
            p = output / "story" / name
            if not p.exists():
                errors.append(f"스토리 산출물 없음: output/story/{name}")

    if errors:
        raise AppError("G3 게이팅 실패:\n- " + "\n- ".join(errors))


def compose_text(caption: str, hashtags: str) -> str:
    caption = (caption or "").strip()
    hashtags = (hashtags or "").strip()
    if caption and hashtags:
        return f"{caption}\n\n{hashtags}".strip()
    return caption or hashtags


def build_carousel_payload(scheduled_at: datetime, root: Path) -> SchedulePayload:
    slides = sorted((root / "output" / "slides").glob("*.png"))
    if not slides:
        raise AppError("캐러셀 파일이 없습니다: output/slides/*.png")
    body, hashtags = parse_copy_md(root / "weekly" / "copy.md")
    text = compose_text(body, hashtags)
    return SchedulePayload("carousel", scheduled_at, text, slides)


def build_reels_payload(scheduled_at: datetime, root: Path) -> SchedulePayload:
    reel = root / "output" / "reels" / "final.mp4"
    if not reel.exists():
        raise AppError("릴스 파일이 없습니다: output/reels/final.mp4")
    caption = parse_scene_plan_caption(root / "weekly" / "scene-plan.json")
    text = compose_text(caption, " ".join(REELS_HASHTAGS))
    return SchedulePayload("reels", scheduled_at, text, [reel])


def build_story_payloads(base_date: datetime, root: Path) -> List[SchedulePayload]:
    # 입력된 base_date를 D-1 화 19:00으로 간주
    d1 = ensure_kst(base_date)
    d0 = d1 + timedelta(days=1)
    d3 = d1 + timedelta(days=4)

    story_dir = root / "output" / "story"
    files = {
        "d1": story_dir / "story-d1.png",
        "d0": story_dir / "story-d0.png",
        "d3": story_dir / "story-d3.png",
    }
    for k, p in files.items():
        if not p.exists():
            raise AppError(f"스토리 파일이 없습니다({k}): {p}")

    return [
        SchedulePayload("story", d1.replace(hour=19, minute=0, second=0, microsecond=0), "", [files["d1"]]),
        SchedulePayload("story", d0.replace(hour=12, minute=5, second=0, microsecond=0), "", [files["d0"]]),
        SchedulePayload("story", d3.replace(hour=10, minute=0, second=0, microsecond=0), "", [files["d3"]]),
    ]


def perform_schedule(client: BufferClient, profile_id: str, payloads: Sequence[SchedulePayload]) -> None:
    for p in payloads:
        for idx, media in enumerate(p.media_files, start=1):
            # Buffer 단건 업데이트 API 기반으로 파일별 예약 생성
            text = p.text if idx == 1 else ""
            result = client.create_update(profile_id, text, media, p.scheduled_at)
            print(json.dumps({
                "post_type": p.post_type,
                "scheduled_at": p.scheduled_at.isoformat(),
                "media": str(media),
                "result": result,
            }, ensure_ascii=False, indent=2))


def auto_schedule_payloads(now_kst: datetime, root: Path) -> List[SchedulePayload]:
    carousel_dt = next_weekday_at(now_kst, weekday=2, hour=12, minute=0)  # 수
    reels_dt = next_weekday_at(now_kst, weekday=4, hour=19, minute=0)     # 금
    story_d1_dt = next_weekday_at(now_kst, weekday=1, hour=19, minute=0)  # 화 19:00

    payloads = [
        build_carousel_payload(carousel_dt, root),
        build_reels_payload(reels_dt, root),
    ]
    payloads.extend(build_story_payloads(story_d1_dt, root))
    return payloads


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="G3 게이팅 통과 후 Buffer API로 인스타그램 예약 발행",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--type", choices=["carousel", "reels", "story"], help="발행 타입")
    parser.add_argument("--date", help="예약 시각 (KST) 예: '2026-03-05 12:00'")
    parser.add_argument("--auto-schedule", action="store_true", help="이번 주 수/금/토 자동 예약")
    parser.add_argument("--list", action="store_true", help="예약 목록 확인")
    parser.add_argument("--cancel", metavar="UPDATE_ID", help="예약 취소")
    parser.add_argument("--dry-run", action="store_true", help="실제 API 호출 없이 내용만 출력")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    mode_flags = [bool(args.auto_schedule), bool(args.list), bool(args.cancel), bool(args.type)]
    if sum(mode_flags) == 0:
        print("실행 모드를 지정하세요. --help 참고", file=sys.stderr)
        return 2

    root = BASE_DIR

    try:
        token = load_env()
        client = BufferClient(token=token, dry_run=args.dry_run)
        profile_id = client.get_instagram_profile_id()

        if args.list:
            pending = client.list_pending(profile_id)
            print(json.dumps(pending, ensure_ascii=False, indent=2))
            return 0

        if args.cancel:
            result = client.cancel_update(args.cancel)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        if args.auto_schedule:
            validate_g3_gate("auto", root)
            now = ensure_kst(datetime.now())
            payloads = auto_schedule_payloads(now, root)
            perform_schedule(client, profile_id, payloads)
            return 0

        # --type 모드
        if not args.type:
            raise AppError("--type 또는 --auto-schedule/--list/--cancel 중 하나가 필요합니다.")
        if not args.date and args.type in ("carousel", "reels", "story"):
            raise AppError("--type 사용 시 --date가 필요합니다. 예: --date '2026-03-05 12:00'")

        validate_g3_gate(args.type, root)
        dt = parse_datetime_kst(args.date)

        if args.type == "carousel":
            payloads = [build_carousel_payload(dt, root)]
        elif args.type == "reels":
            payloads = [build_reels_payload(dt, root)]
        elif args.type == "story":
            payloads = build_story_payloads(dt, root)
        else:
            raise AppError(f"지원하지 않는 타입: {args.type}")

        perform_schedule(client, profile_id, payloads)
        return 0

    except AppError as e:
        print(f"[오류] {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("중단되었습니다.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
