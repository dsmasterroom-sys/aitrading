"""Core modules for Figma-based carousel export."""

from .figma_client import FigmaClient, FigmaApiError
from .figma_exporter import FigmaExporter
from .figma_updater import FigmaPluginBridge, FigmaTemplateUpdater
from .models import NodeMapping, SlideData, TemplatePattern

__all__ = [
    "FigmaApiError",
    "FigmaClient",
    "FigmaExporter",
    "FigmaPluginBridge",
    "FigmaTemplateUpdater",
    "NodeMapping",
    "SlideData",
    "TemplatePattern",
]
