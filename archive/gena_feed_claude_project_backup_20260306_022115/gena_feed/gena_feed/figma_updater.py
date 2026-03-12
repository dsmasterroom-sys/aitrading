from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any

from .figma_client import FigmaClient
from .models import NodeMapping, PreparedSlideUpdate, SlideData, TemplatePattern

_TEMPLATE_PATTERN = re.compile(r"(H-[1-3]|I-[1-5]|P-[1-3]|C-[1-2]|M-[1-2]|CTA-[1-2])", re.IGNORECASE)


class FigmaTemplateUpdater:
    """Prepare template update payloads for a Figma plugin."""

    def __init__(self, client: FigmaClient) -> None:
        self.client = client
        self.node_mappings: dict[str, NodeMapping] = {}

    def load_node_mappings(self, mapping_file: str = "figma_mappings.json") -> None:
        path = Path(mapping_file)
        with path.open("r", encoding="utf-8") as fp:
            raw = json.load(fp)

        if "frames" in raw:
            self.node_mappings = self._load_from_frame_index(raw)
            return

        mappings: dict[str, NodeMapping] = {}
        for slide_key, mapping_data in raw.items():
            mapping_dict = dict(mapping_data)
            if "frame_id" not in mapping_dict and "frameId" in mapping_dict:
                mapping_dict["frame_id"] = mapping_dict["frameId"]
            mapping = NodeMapping.from_dict(mapping_dict)
            mappings[slide_key] = mapping
        self.node_mappings = mappings

    def _load_from_frame_index(self, raw: dict[str, Any]) -> dict[str, NodeMapping]:
        mappings: dict[str, NodeMapping] = {}
        frames = list(raw.get("frames", []))
        for i, frame in enumerate(frames, start=1):
            frame_id = str(frame["id"])
            frame_name = str(frame.get("name", ""))
            template_match = _TEMPLATE_PATTERN.search(frame_name)
            template = TemplatePattern.parse(template_match.group(1)) if template_match else None
            mappings[f"slide_{i:02d}"] = NodeMapping(
                frame_id=frame_id,
                template=template,
                text_nodes={},
                image_nodes={},
                color_nodes={},
                frame_name=frame_name,
            )
        return mappings

    def prepare_slide_data(self, slide: SlideData) -> PreparedSlideUpdate:
        slide_key = f"slide_{slide.slide_number:02d}"
        mapping = self.node_mappings.get(slide_key)
        if not mapping:
            raise ValueError(f"No mapping found for {slide_key}")

        if mapping.template and mapping.template != slide.template:
            raise ValueError(
                f"Template mismatch for {slide_key}: mapping={mapping.template.value}, slide={slide.template.value}"
            )

        updates: dict[str, dict[str, str]] = {"text": {}, "images": {}, "colors": {}}
        for var_name, node_id in mapping.text_nodes.items():
            if var_name in slide.variables:
                updates["text"][node_id] = str(slide.variables[var_name])
        for var_name, node_id in mapping.image_nodes.items():
            if var_name in slide.variables:
                updates["images"][node_id] = str(slide.variables[var_name])
        for var_name, node_id in mapping.color_nodes.items():
            if var_name in slide.variables:
                updates["colors"][node_id] = str(slide.variables[var_name])

        template = mapping.template.value if mapping.template else slide.template.value
        return PreparedSlideUpdate(frame_id=mapping.frame_id, template=template, updates=updates)


class FigmaPluginBridge:
    """File-based bridge between Python and a local Figma plugin workflow."""

    def __init__(self, bridge_dir: str = "./figma_bridge") -> None:
        self.bridge_dir = Path(bridge_dir)
        self.bridge_dir.mkdir(parents=True, exist_ok=True)

    def write_update_request(self, slide_updates: list[dict[str, Any] | PreparedSlideUpdate]) -> Path:
        timestamp = int(time.time())
        request_path = self.bridge_dir / f"update_request_{timestamp}.json"
        payload_slides: list[dict[str, Any]] = []

        for slide in slide_updates:
            if isinstance(slide, PreparedSlideUpdate):
                payload_slides.append(slide.to_dict())
            else:
                payload_slides.append(dict(slide))

        payload = {"timestamp": timestamp, "slides": payload_slides}
        request_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return request_path

    def wait_for_completion(self, request_file: str | os.PathLike[str], timeout: int = 300) -> bool:
        request_path = Path(request_file)
        done_file = request_path.with_suffix(request_path.suffix + ".done")
        start = time.time()
        while (time.time() - start) < timeout:
            if done_file.exists():
                try:
                    payload = json.loads(done_file.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    return False
                return payload.get("status") == "success"
            time.sleep(2)
        return False
