#!/usr/bin/env python3
"""Analyze product reference images using vision model.

Extracts detailed product specifications to ensure accurate AI generation:
- Material type and texture
- Structure and shape
- Hardware details
- Color and finish
- Wearing style and positioning
- Target context and vibe

Usage:
    python analyze_product.py --references assets/slant_4-view.png assets/slant-produact.png
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
OUTPUT_DIR = ROOT / "assets" / "output"
ANALYSIS_PATH = OUTPUT_DIR / "product_analysis.json"


class AnalysisError(RuntimeError):
    pass


def log(msg: str) -> None:
    print(f"[analyze_product] {msg}", flush=True)


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


def image_to_base64(path: Path) -> str:
    """Convert image to base64 data URI."""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    # Detect mime type
    ext = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


def analyze_with_gemini(api_key: str, image_paths: List[Path]) -> Dict[str, Any]:
    """Analyze product images using Gemini Vision API."""
    
    analysis_prompt = """Analyze these product images in extreme detail. This is a product for AI image generation reference - accuracy is CRITICAL.

Extract and describe:

1. MATERIAL & TEXTURE:
   - Exact fabric/material type (e.g., nylon, leather, canvas, polyester)
   - Surface texture (smooth, textured, ribbed, etc.)
   - Finish (matte, glossy, satin, etc.)
   - Any visible patterns or weaves

2. STRUCTURE & SHAPE:
   - Overall shape and silhouette
   - Dimensions and proportions
   - Structural elements (panels, seams, padding)
   - How parts are assembled

3. STRAPS & ATTACHMENT:
   - Strap type and material
   - WHERE straps attach to the bag body (top edge? side panels? bottom?)
   - Strap width and adjustability
   - Buckle/fastener types

4. HARDWARE & DETAILS:
   - Zipper type, color, placement
   - Buckles and fasteners (material, color)
   - Logo/branding visibility
   - Pockets and compartments
   - Any decorative elements

5. COLOR & FINISH:
   - Exact color(s)
   - Color of hardware vs main body
   - Any color variations or accents

6. WEARING STYLE:
   - How is this product meant to be worn/carried?
   - Body positioning when worn correctly
   - Angle or orientation when in use

7. CONTEXT & VIBE:
   - What lifestyle/activity is this designed for?
   - Target user demographic
   - Formal vs casual context
   - Keywords that capture the product vibe

Format your response as a structured JSON object with these exact keys:
{
  "material": { "type": "...", "texture": "...", "finish": "..." },
  "structure": { "shape": "...", "proportions": "...", "construction": "..." },
  "straps": { "type": "...", "attachment_point": "...", "width": "...", "hardware": "..." },
  "hardware": { "zippers": "...", "buckles": "...", "color": "..." },
  "color": { "primary": "...", "hardware_color": "...", "finish": "..." },
  "wearing_style": { "method": "...", "position": "...", "angle": "..." },
  "context": { "lifestyle": "...", "target_user": "...", "formality": "...", "vibe_keywords": [] }
}

BE EXTREMELY SPECIFIC. Avoid vague terms like "stylish" or "modern". Focus on physical, observable facts."""

    # Prepare image parts for Gemini API
    image_parts = []
    for img_path in image_paths:
        b64_data = image_to_base64(img_path)
        # Remove data URI prefix for Gemini API
        if b64_data.startswith("data:"):
            mime, b64_only = b64_data.split(",", 1)
            mime_type = mime.split(":")[1].split(";")[0]
        else:
            b64_only = b64_data
            mime_type = "image/png"
        
        image_parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": b64_only
            }
        })

    # Build request payload
    payload = {
        "contents": [{
            "parts": [
                {"text": analysis_prompt},
                *image_parts
            ]
        }],
        "generationConfig": {
            "temperature": 0.2,  # Low temperature for factual analysis
            "maxOutputTokens": 2048
        }
    }

    # Call Gemini API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        # Extract text from response
        if "candidates" not in data or len(data["candidates"]) == 0:
            raise AnalysisError("No candidates in Gemini response")
        
        candidate = data["candidates"][0]
        if "content" not in candidate or "parts" not in candidate["content"]:
            raise AnalysisError("Invalid response structure from Gemini")
        
        text_response = candidate["content"]["parts"][0].get("text", "")
        
        # Try to parse as JSON
        # Remove markdown code blocks if present
        text_response = text_response.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
        text_response = text_response.strip()
        
        try:
            analysis_result = json.loads(text_response)
        except json.JSONDecodeError:
            # If JSON parsing fails, save raw text for manual review
            log("Warning: Could not parse response as JSON. Saving raw text.")
            analysis_result = {"raw_analysis": text_response}
        
        return analysis_result
        
    except requests.RequestException as e:
        raise AnalysisError(f"Gemini API request failed: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze product reference images")
    parser.add_argument(
        "--references",
        nargs="+",
        help="Paths to product reference images (relative to project root)"
    )
    parser.add_argument(
        "--output",
        default=str(ANALYSIS_PATH),
        help="Output JSON path for analysis results"
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load API key
    env = load_env(ENV_PATH)
    api_key = env.get("GOOGLE_API_KEY") or env.get("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise AnalysisError(
            "GOOGLE_API_KEY or GEMINI_API_KEY not found in .env or environment.\n"
            "Set one of these to use Gemini Vision for product analysis."
        )

    # Resolve reference image paths
    if not args.references:
        # Default: use slant product images
        ref_paths = [
            ROOT / "assets" / "slant_4-view.png",
            ROOT / "assets" / "slant-produact.png"
        ]
    else:
        ref_paths = [ROOT / ref for ref in args.references]

    # Validate paths
    missing = [str(p.relative_to(ROOT)) for p in ref_paths if not p.exists()]
    if missing:
        raise AnalysisError(f"Reference images not found: {', '.join(missing)}")

    log(f"Analyzing {len(ref_paths)} reference image(s)...")
    for p in ref_paths:
        log(f"  - {p.relative_to(ROOT)}")

    # Analyze with Gemini
    analysis = analyze_with_gemini(api_key, ref_paths)

    # Save result
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    log(f"Analysis saved to: {output_path.relative_to(ROOT)}")
    log("✅ Product analysis complete!")
    
    # Print summary
    print("\n" + "="*60)
    print("PRODUCT ANALYSIS SUMMARY")
    print("="*60)
    if "raw_analysis" in analysis:
        print(analysis["raw_analysis"])
    else:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    print("="*60 + "\n")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AnalysisError as e:
        log(f"오류: {e}")
        raise SystemExit(1)
