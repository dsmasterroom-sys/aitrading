from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import SlideData

_SLIDE_HEADER_RE = re.compile(r"^##\s*Slide\s*(\d+).*?\(([^)]+)\)\s*$", re.IGNORECASE | re.MULTILINE)
_FENCED_BLOCK_RE = re.compile(r"```(?:yaml|yml)\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def parse_content_file(path: str) -> list[SlideData]:
    file_path = Path(path)
    ext = file_path.suffix.lower()
    text = file_path.read_text(encoding="utf-8")

    if ext == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("slides", [])
        if not isinstance(data, list):
            raise ValueError("JSON content file must be a list or {'slides': [...]}")
        return [SlideData.from_dict(item) for item in data]

    if ext in {".yaml", ".yml"}:
        data = _parse_yaml(text)
        if isinstance(data, dict):
            data = data.get("slides", [])
        if not isinstance(data, list):
            raise ValueError("YAML content file must be a list or {'slides': [...]}")
        return [SlideData.from_dict(item) for item in data]

    if ext == ".md":
        return _parse_markdown_slides(text)

    raise ValueError(f"Unsupported content file type: {ext}")


def _parse_markdown_slides(text: str) -> list[SlideData]:
    headers = list(_SLIDE_HEADER_RE.finditer(text))
    if not headers:
        return []

    slides: list[SlideData] = []
    for idx, match in enumerate(headers):
        start = match.end()
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(text)
        section = text[start:end]
        block_match = _FENCED_BLOCK_RE.search(section)
        if not block_match:
            continue
        variables = _parse_yaml(block_match.group(1))
        if not isinstance(variables, dict):
            continue
        slides.append(
            SlideData.from_dict(
                {
                    "slide_number": int(match.group(1)),
                    "template": match.group(2),
                    "variables": variables,
                }
            )
        )
    return slides


def _parse_yaml(text: str) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError:
        return _naive_yaml_dict(text)
    return yaml.safe_load(text)


def _naive_yaml_dict(text: str) -> dict[str, Any]:
    """Minimal parser for flat key:value YAML blocks."""
    output: dict[str, Any] = {}
    for line in text.splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        output[key.strip()] = _coerce_scalar(value.strip())
    return output


def _coerce_scalar(value: str) -> Any:
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    low = value.lower()
    if low in {"true", "false"}:
        return low == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
