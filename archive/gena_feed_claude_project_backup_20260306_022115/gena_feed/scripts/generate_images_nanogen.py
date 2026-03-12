#!/usr/bin/env python3
"""Generate weekly images from Nanogen API using contents[] + slides[] structure.

Expected prompt JSON shape:
{
  "contents": [
    {
      "content_id": "W10-01-reels",
      "slides": [
        {"slide_id": "S1", "prompt": "..."}
      ]
    }
  ]
}
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
PROMPTS_PATH = ROOT / "weekly" / "image-prompts.json"
ASSETS_DIR = ROOT / "assets"
OUTPUT_DIR = ASSETS_DIR / "output"
OUTFIT_DIR = ASSETS_DIR / "outfit"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"
ANALYSIS_PATH = OUTPUT_DIR / "product_analysis.json"
ANALYZE_SCRIPT = Path(__file__).parent / "analyze_product.py"

API_ENDPOINT = "/api/generate"
API_TIMEOUT_SECONDS = 180
MAX_RETRIES = 2


class GenerationError(RuntimeError):
    pass


def log(msg: str) -> None:
    print(f"[generate_images_nanogen] {msg}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images using Nanogen")
    parser.add_argument(
        "--skip-existing",
        dest="skip_existing",
        action="store_true",
        default=True,
        help="Skip generating images that already exist (default: on)",
    )
    parser.add_argument(
        "--no-skip-existing",
        dest="skip_existing",
        action="store_false",
        help="Regenerate images even if output file already exists",
    )
    return parser.parse_args()


def load_env(path: Path) -> Dict[str, str]:
    env: Dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def ensure_product_analysis(ref_catalog: Dict[str, List[str]], force: bool = False) -> Dict[str, Any]:
    if ANALYSIS_PATH.exists() and not force:
        log(f"✓ Product analysis found: {ANALYSIS_PATH.relative_to(ROOT)}")
        return json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))

    log("⚠️  Product analysis not found. Running analyzer...")

    product_refs = []
    for key, paths in ref_catalog.items():
        if "product" in key.lower():
            product_refs.extend(paths)

    if not product_refs:
        log("Warning: No product reference images found in catalog. Skipping analysis.")
        return {}

    try:
        cmd = [sys.executable, str(ANALYZE_SCRIPT), "--references"] + product_refs
        subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True)
        log("✓ Product analysis complete")

        if ANALYSIS_PATH.exists():
            return json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))
        log("Warning: Analysis script ran but output file not created")
        return {}
    except subprocess.CalledProcessError as e:
        log(f"Warning: Product analysis failed: {e}")
        log(f"stderr: {e.stderr}")
        return {}


def load_outfit_references(config: Dict[str, Any]) -> List[str]:
    if not OUTFIT_DIR.exists():
        OUTFIT_DIR.mkdir(parents=True, exist_ok=True)
        log(f"Created outfit directory: {OUTFIT_DIR.relative_to(ROOT)}")
        return []

    outfit_config = config.get("outfit_reference", {})
    enabled = outfit_config.get("enabled", True)
    if not enabled:
        log("Outfit references disabled in config")
        return []

    mode = outfit_config.get("mode", "latest")
    count = outfit_config.get("count", 3)
    date_from = outfit_config.get("date_from", "")
    date_to = outfit_config.get("date_to", "")
    specific_files = outfit_config.get("specific_files", [])

    image_exts = {".png", ".jpg", ".jpeg", ".webp"}
    all_outfits = [
        f for f in OUTFIT_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in image_exts and not f.name.startswith(".")
    ]

    if not all_outfits:
        log(f"No outfit grid images found in {OUTFIT_DIR.relative_to(ROOT)}")
        return []

    selected: List[Path] = []
    if mode == "specific":
        for fname in specific_files:
            fpath = OUTFIT_DIR / fname
            if fpath.exists():
                selected.append(fpath)
            else:
                log(f"Warning: Specific outfit file not found: {fname}")
    elif mode == "date_range":
        for f in all_outfits:
            file_date = f.name.split("_")[0]
            if len(file_date) == 8 and file_date.isdigit():
                if (not date_from or file_date >= date_from) and (not date_to or file_date <= date_to):
                    selected.append(f)
        selected.sort(key=lambda x: x.name.split("_")[0], reverse=True)
    else:
        dated_outfits: List[Tuple[str, Path]] = []
        for f in all_outfits:
            file_date = f.name.split("_")[0]
            if len(file_date) == 8 and file_date.isdigit():
                dated_outfits.append((file_date, f))
        dated_outfits.sort(key=lambda x: x[0], reverse=True)
        selected = [f for _, f in dated_outfits[:count]]

    relative_paths = [str(f.relative_to(ROOT)) for f in selected]
    if relative_paths:
        log(f"Loaded {len(relative_paths)} outfit reference(s) (mode: {mode})")
    return relative_paths


def ensure_nanogen_reachable(base_url: str) -> None:
    try:
        requests.get(base_url, timeout=3)
    except requests.RequestException as e:
        raise GenerationError(
            "Nanogen 서버에 연결할 수 없습니다. Nanogen이 실행 중인지 확인하세요.\n"
            f"- BASE_URL: {base_url}\n"
            "- 예시: cd /Users/master/.openclaw/workspace/nanogen && python manage.py runserver\n"
            f"- 원인: {e}"
        )


def to_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def decode_response_image(data: Dict[str, Any]) -> bytes:
    url = data.get("url")
    if not url:
        raise GenerationError(f"API 응답에 url이 없습니다: {data}")

    if isinstance(url, str) and url.startswith("data:"):
        _, b64part = url.split("base64,", 1)
        return base64.b64decode(b64part)

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content


def post_generate(base_url: str, payload: Dict[str, Any]) -> requests.Response:
    return requests.post(
        f"{base_url.rstrip('/')}{API_ENDPOINT}",
        json=payload,
        timeout=API_TIMEOUT_SECONDS,
    )


def collect_jobs(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Preferred schema: contents[]
    # Backward compatibility: some files may still place content blocks under top-level slides[]
    contents = config.get("contents") or config.get("slides") or []
    if not contents:
        raise GenerationError("image-prompts.json의 contents/slides가 비어 있습니다")

    jobs: List[Dict[str, Any]] = []
    for content in contents:
        content_id = str(content.get("content_id", "")).strip()
        if not content_id:
            log("경고: content_id가 없는 항목을 건너뜁니다")
            continue

        slides = content.get("slides", []) or []
        for idx, slide in enumerate(slides, start=1):
            slide_id = slide.get("slide_id") or f"S{idx}"
            prompt = str(slide.get("prompt", "")).strip()
            if not prompt:
                log(f"경고: {content_id}/{slide_id} prompt가 비어 있어 건너뜁니다")
                continue
            jobs.append(
                {
                    "content_id": content_id,
                    "slide_id": str(slide_id),
                    "prompt": prompt,
                    "referenceImages": slide.get("referenceImages", []),
                }
            )

    if not jobs:
        raise GenerationError("생성할 유효한 슬라이드가 없습니다")
    return jobs


def generate_one(
    base_url: str,
    job: Dict[str, Any],
    ref_catalog: Dict[str, List[str]],
    outfit_refs: List[str],
    skip_existing: bool,
) -> Dict[str, Any]:
    content_id = job["content_id"]
    slide_id = job["slide_id"]
    prompt = job["prompt"]

    content_output_dir = OUTPUT_DIR / content_id
    content_output_dir.mkdir(parents=True, exist_ok=True)
    out_path = content_output_dir / f"slide-{slide_id}.png"

    if skip_existing and out_path.exists():
        log(f"스킵(기존 파일): {out_path.relative_to(ROOT)}")
        return {
            "content_id": content_id,
            "slide_id": slide_id,
            "output": str(out_path.relative_to(ROOT)),
            "status": "skipped",
        }

    payload: Dict[str, Any] = {
        "prompt": prompt,
        "config": {"aspectRatio": "3:4", "size": "1080x1440"},
        "referenceImages": [],
    }

    ref_uris: List[str] = []
    for outfit_path in outfit_refs:
        abs_path = ROOT / outfit_path
        if abs_path.exists():
            ref_uris.append(to_data_uri(abs_path))

    for key in job.get("referenceImages", []):
        for rel_path in ref_catalog.get(key, []):
            abs_path = ROOT / rel_path
            if abs_path.exists():
                ref_uris.append(to_data_uri(abs_path))

    if ref_uris:
        payload["referenceImages"] = ref_uris

    last_error = None
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            r = post_generate(base_url, payload)
            if r.status_code >= 400:
                raise GenerationError(f"API 오류 {r.status_code} - {r.text[:500]}")
            data = r.json()
            image_bytes = decode_response_image(data)
            out_path.write_bytes(image_bytes)
            log(f"저장 완료: {out_path.relative_to(ROOT)}")
            return {
                "content_id": content_id,
                "slide_id": slide_id,
                "output": str(out_path.relative_to(ROOT)),
                "status": "generated",
                "saved_image": data.get("saved_image"),
            }
        except Exception as e:  # noqa: BLE001
            last_error = e
            if attempt <= MAX_RETRIES:
                log(f"재시도 {attempt}/{MAX_RETRIES}: {content_id}/{slide_id} - {e}")
                time.sleep(1.5)
            else:
                break

    raise GenerationError(f"{content_id}/{slide_id} 생성 실패: {last_error}")


def main() -> int:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    required_assets = [ASSETS_DIR / "gena-base.png", ASSETS_DIR / "slant-product.png"]
    missing = [str(p.relative_to(ROOT)) for p in required_assets if not p.exists()]
    if missing:
        raise GenerationError("필수 에셋이 누락되었습니다: " + ", ".join(missing))

    env = load_env(ENV_PATH)
    base_url = env.get("NANOGEN_BASE_URL") or os.getenv("NANOGEN_BASE_URL") or "http://localhost:8000"

    ensure_nanogen_reachable(base_url)

    config = json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))
    ref_catalog: Dict[str, List[str]] = config.get("reference_images", {})

    log("=" * 60)
    log("STEP 1: Product Analysis")
    log("=" * 60)
    _ = ensure_product_analysis(ref_catalog, force=False)

    log("=" * 60)
    log("STEP 1.5: Outfit References")
    log("=" * 60)
    outfit_refs = load_outfit_references(config)

    jobs = collect_jobs(config)

    log("=" * 60)
    log("STEP 2: Image Generation")
    log("=" * 60)
    manifest: List[Dict[str, Any]] = []

    total = len(jobs)
    for i, job in enumerate(jobs, start=1):
        log(f"진행률: {i}/{total} | {job['content_id']}/{job['slide_id']}")
        manifest.append(
            generate_one(
                base_url=base_url,
                job=job,
                ref_catalog=ref_catalog,
                outfit_refs=outfit_refs,
                skip_existing=args.skip_existing,
            )
        )

    MANIFEST_PATH.write_text(
        json.dumps({"generated": manifest}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log(f"매니페스트 저장: {MANIFEST_PATH.relative_to(ROOT)}")
    log(f"총 {len(manifest)}개 작업 완료")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GenerationError as e:
        log(f"오류: {e}")
        raise SystemExit(1)
