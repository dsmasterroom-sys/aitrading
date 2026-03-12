from __future__ import annotations

from pathlib import Path
from typing import Iterable

import requests

from .figma_client import FigmaClient
from .models import NodeMapping


class FigmaExporter:
    """Export Figma frames to image files."""

    def __init__(self, client: FigmaClient, output_dir: str = "./output", *, request_timeout: int = 120) -> None:
        self.client = client
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.request_timeout = request_timeout

    def export_slide(
        self,
        node_id: str,
        output_filename: str,
        *,
        scale: float = 2.0,
        format: str = "png",
        file_id: str | None = None,
    ) -> Path:
        response = self.client.get_images([node_id], scale=scale, format=format, file_id=file_id)
        if response.get("err"):
            raise RuntimeError(f"Figma image API error: {response['err']}")

        image_url = (response.get("images") or {}).get(node_id)
        if not image_url:
            raise RuntimeError(f"No image URL returned for node {node_id}")

        output_path = self.output_dir / output_filename
        self._download_image(image_url, output_path)
        return output_path

    def export_all_slides(self, node_mappings: dict[str, NodeMapping], *, scale: float = 2.0, format: str = "png") -> list[Path]:
        node_ids = [m.frame_id for m in node_mappings.values()]
        output_paths: list[Path] = []

        image_urls: dict[str, str] = {}
        for group in _chunked(node_ids, 50):
            response = self.client.get_images(group, scale=scale, format=format)
            if response.get("err"):
                raise RuntimeError(f"Figma image API error: {response['err']}")
            image_urls.update(response.get("images", {}))

        for slide_key, mapping in node_mappings.items():
            image_url = image_urls.get(mapping.frame_id)
            if not image_url:
                continue
            output_path = self.output_dir / f"{slide_key}.{format}"
            self._download_image(image_url, output_path)
            output_paths.append(output_path)

        return output_paths

    def export_with_optimization(
        self,
        node_id: str,
        output_filename: str,
        *,
        optimize: bool = True,
        scale: float = 2.0,
    ) -> Path:
        output_path = self.export_slide(node_id, output_filename, scale=scale, format="png")
        if not optimize:
            return output_path
        self._optimize_png(output_path)
        return output_path

    def _download_image(self, url: str, output_path: Path) -> None:
        try:
            response = requests.get(url, timeout=self.request_timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to download image: {url} ({exc})") from exc
        output_path.write_bytes(response.content)

    def _optimize_png(self, output_path: Path) -> None:
        try:
            from PIL import Image
            from PIL import PngImagePlugin
        except ImportError:
            return

        image = Image.open(output_path)
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Author", "GenArchive Carousel Generator")
        metadata.add_text("Software", "Figma API + Python")
        image.save(output_path, "PNG", optimize=True, pnginfo=metadata)


def _chunked(seq: Iterable[str], size: int) -> list[list[str]]:
    items = list(seq)
    return [items[i : i + size] for i in range(0, len(items), size)]
