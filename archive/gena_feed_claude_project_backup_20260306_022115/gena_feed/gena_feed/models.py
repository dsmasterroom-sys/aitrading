from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TemplatePattern(str, Enum):
    """Supported slide template patterns."""

    H1 = "H-1"
    H2 = "H-2"
    H3 = "H-3"
    I1 = "I-1"
    I2 = "I-2"
    I3 = "I-3"
    I4 = "I-4"
    I5 = "I-5"
    P1 = "P-1"
    P2 = "P-2"
    P3 = "P-3"
    C1 = "C-1"
    C2 = "C-2"
    M1 = "M-1"
    M2 = "M-2"
    CTA1 = "CTA-1"
    CTA2 = "CTA-2"

    @classmethod
    def parse(cls, value: str) -> "TemplatePattern":
        normalized = value.strip().upper().replace("_", "-")
        if normalized == "CTA1":
            normalized = "CTA-1"
        if normalized == "CTA2":
            normalized = "CTA-2"
        return cls(normalized)


@dataclass
class SlideData:
    """Input content data per slide."""

    slide_number: int
    template: TemplatePattern
    variables: dict[str, Any]
    title: str | None = None
    description: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SlideData":
        slide_number = int(data["slide_number"])
        template_raw = data["template"]
        template = template_raw if isinstance(template_raw, TemplatePattern) else TemplatePattern.parse(str(template_raw))
        return cls(
            slide_number=slide_number,
            template=template,
            variables=dict(data.get("variables", {})),
            title=data.get("title"),
            description=data.get("description"),
        )


@dataclass
class NodeMapping:
    """Figma node mapping data for one slide/frame."""

    frame_id: str
    template: TemplatePattern | None
    text_nodes: dict[str, str] = field(default_factory=dict)
    image_nodes: dict[str, str] = field(default_factory=dict)
    color_nodes: dict[str, str] = field(default_factory=dict)
    frame_name: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NodeMapping":
        template_value = data.get("template")
        template = None
        if template_value:
            template = template_value if isinstance(template_value, TemplatePattern) else TemplatePattern.parse(str(template_value))
        return cls(
            frame_id=str(data["frame_id"]),
            template=template,
            text_nodes={str(k): str(v) for k, v in dict(data.get("text_nodes", {})).items()},
            image_nodes={str(k): str(v) for k, v in dict(data.get("image_nodes", {})).items()},
            color_nodes={str(k): str(v) for k, v in dict(data.get("color_nodes", {})).items()},
            frame_name=data.get("frame_name"),
        )


@dataclass
class PreparedSlideUpdate:
    """Prepared payload for Figma plugin updates."""

    frame_id: str
    template: str
    updates: dict[str, dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "frameId": self.frame_id,
            "template": self.template,
            "updates": self.updates,
        }
