from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass
class FallbackResult:
    ok: bool
    return_code: int
    command: list[str]
    message: str
    stdout: str = ""
    stderr: str = ""


class FallbackHandler:
    """Fallback handler that runs legacy HTML-based carousel generation."""

    def __init__(
        self,
        *,
        use_html_fallback: bool | None = None,
        compose_script: str | None = None,
    ) -> None:
        env_default = _to_bool(os.getenv("USE_HTML_FALLBACK"), default=False)
        self.use_html_fallback = env_default if use_html_fallback is None else use_html_fallback
        self.compose_script = Path(compose_script or "scripts/compose_carousel.py")

    def run_html_fallback(self) -> FallbackResult:
        if not self.use_html_fallback:
            return FallbackResult(
                ok=False,
                return_code=1,
                command=[],
                message="Fallback disabled by configuration",
            )

        if not self.compose_script.exists():
            return FallbackResult(
                ok=False,
                return_code=1,
                command=[],
                message=f"Fallback script not found: {self.compose_script}",
            )

        command = [sys.executable, str(self.compose_script)]
        proc = subprocess.run(command, capture_output=True, text=True)
        return FallbackResult(
            ok=(proc.returncode == 0),
            return_code=proc.returncode,
            command=command,
            message="HTML fallback completed" if proc.returncode == 0 else "HTML fallback failed",
            stdout=proc.stdout,
            stderr=proc.stderr,
        )
