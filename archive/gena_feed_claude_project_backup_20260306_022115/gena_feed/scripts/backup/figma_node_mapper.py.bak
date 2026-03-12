#!/usr/bin/env python3
"""
Figma 파일의 프레임/변수 노드 매핑 생성 스크립트.

기능:
1) Figma API로 파일 구조 조회
2) 모든 프레임(Frame) Node ID 추출
3) 변수명 패턴 인식: Text/{var}, Image/{var}
4) 결과를 figma-node-mapping.json으로 저장

사용법:
    python scripts/figma_node_mapper.py

필수 환경변수(.env):
    FIGMA_ACCESS_TOKEN=...
    FIGMA_FILE_KEY=...

출력:
    figma-node-mapping.json
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv

FIGMA_API_BASE = "https://api.figma.com/v1"
TEXT_PATTERN = re.compile(r"^Text/(.+)$")
IMAGE_PATTERN = re.compile(r"^Image/(.+)$")


def _load_env() -> Tuple[str, str]:
    load_dotenv()
    token = os.getenv("FIGMA_ACCESS_TOKEN", "").strip()
    file_key = os.getenv("FIGMA_FILE_KEY", "").strip()

    if not token or not file_key:
        raise ValueError(
            "필수 환경변수 누락: FIGMA_ACCESS_TOKEN, FIGMA_FILE_KEY (.env 확인 필요)"
        )
    return token, file_key


def _figma_get(endpoint: str, token: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    url = f"{FIGMA_API_BASE}{endpoint}"
    headers = {"X-Figma-Token": token}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
    except requests.RequestException as exc:
        raise RuntimeError(f"Figma API 요청 실패: {url} ({exc})") from exc

    if resp.status_code != 200:
        msg = ""
        try:
            msg = resp.json().get("err", "")
        except Exception:
            msg = resp.text[:200]
        raise RuntimeError(f"Figma API 오류 {resp.status_code}: {msg}")

    try:
        return resp.json()
    except ValueError as exc:
        raise RuntimeError("Figma API 응답 JSON 파싱 실패") from exc


def _walk_frames_and_vars(node: Dict[str, Any], frames: List[Dict[str, str]], var_hits: Dict[str, Dict[str, List[Dict[str, str]]]]) -> None:
    node_type = node.get("type")
    node_id = node.get("id")
    node_name = node.get("name", "")

    if node_type == "FRAME" and node_id:
        frames.append({"id": node_id, "name": node_name})

    if node_name and node_id:
        text_match = TEXT_PATTERN.match(node_name)
        image_match = IMAGE_PATTERN.match(node_name)

        if text_match:
            key = text_match.group(1).strip()
            if key:
                var_hits.setdefault("text", {}).setdefault(key, []).append({"id": node_id, "name": node_name})

        if image_match:
            key = image_match.group(1).strip()
            if key:
                var_hits.setdefault("image", {}).setdefault(key, []).append({"id": node_id, "name": node_name})

    for child in node.get("children", []) or []:
        _walk_frames_and_vars(child, frames, var_hits)


def build_mapping(token: str, file_key: str) -> Dict[str, Any]:
    print("[1/3] Figma 파일 구조 조회 중...")
    data = _figma_get(f"/files/{file_key}", token)

    document = data.get("document")
    if not document:
        raise RuntimeError("파일 구조(document)를 찾을 수 없습니다.")

    frames: List[Dict[str, str]] = []
    var_hits: Dict[str, Dict[str, List[Dict[str, str]]]] = {"text": {}, "image": {}}

    print("[2/3] 프레임/변수 노드 스캔 중...")
    _walk_frames_and_vars(document, frames, var_hits)

    mapping = {
        "fileKey": file_key,
        "fileName": data.get("name", ""),
        "lastModified": data.get("lastModified", ""),
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "frameCount": len(frames),
        "frames": [
            {
                "index": i + 1,
                "id": f["id"],
                "name": f["name"],
                "suggestedFileName": f"slide-{i + 1:02d}.png",
            }
            for i, f in enumerate(frames)
        ],
        "variables": {
            "text": [
                {"name": name, "nodes": nodes}
                for name, nodes in sorted(var_hits.get("text", {}).items(), key=lambda x: x[0].lower())
            ],
            "image": [
                {"name": name, "nodes": nodes}
                for name, nodes in sorted(var_hits.get("image", {}).items(), key=lambda x: x[0].lower())
            ],
        },
    }

    return mapping


def main() -> int:
    try:
        token, file_key = _load_env()
        mapping = build_mapping(token, file_key)

        out_path = Path("figma-node-mapping.json")
        print("[3/3] 매핑 파일 저장 중...")
        out_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")

        print(
            f"완료: {out_path} (frames={mapping['frameCount']}, "
            f"text_vars={len(mapping['variables']['text'])}, "
            f"image_vars={len(mapping['variables']['image'])})"
        )
        return 0
    except Exception as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
