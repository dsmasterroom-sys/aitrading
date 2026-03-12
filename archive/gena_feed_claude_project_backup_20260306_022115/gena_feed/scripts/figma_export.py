#!/usr/bin/env python3
"""GenArchive Carousel - Figma Export Tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="GenArchive Carousel - Figma Export Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/figma_export.py --all\n"
            "  python scripts/figma_export.py --slide 1,3,7\n"
            "  python scripts/figma_export.py --all --update --data weekly/copy.md\n"
            "  python scripts/figma_export.py --all --optimize\n"
            "  python scripts/figma_export.py --all --fallback\n"
            "  python scripts/figma_export.py --test"
        ),
    )

    parser.add_argument("--all", action="store_true", help="Export all slides")
    parser.add_argument("--slide", type=str, help="Export specific slides, e.g. '1,3,7'")
    parser.add_argument("--frames", type=str, help="Legacy alias for --slide")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print plan without exporting")
    parser.add_argument("--update", action="store_true", help="Prepare Figma template update payload before export")
    parser.add_argument("--data", type=str, help="Content data file for --update (md/json/yaml)")
    parser.add_argument("--output", type=str, default="output/figma-samples", help="Output directory")
    parser.add_argument("--scale", type=float, default=2.0, help="Figma export scale (default: 2.0)")
    parser.add_argument("--optimize", action="store_true", help="Optimize PNG after export (requires Pillow)")
    parser.add_argument("--fallback", action="store_true", help="Use HTML fallback when Figma flow fails")
    parser.add_argument("--test", action="store_true", help="Test Figma API connection and exit")
    parser.add_argument("--mapping-file", type=str, default=None, help="Path to mapping JSON")
    parser.add_argument("--bridge-dir", type=str, default="./figma_bridge", help="Plugin bridge directory")
    parser.add_argument("--plugin-timeout", type=int, default=300, help="Plugin completion wait timeout in seconds")
    return parser


def _parse_slide_numbers(raw: str) -> list[int]:
    numbers: set[int] = set()
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        if not token.isdigit():
            raise ValueError(f"Invalid slide number: {token}")
        value = int(token)
        if value < 1:
            raise ValueError(f"Invalid slide number: {token}")
        numbers.add(value)
    if not numbers:
        raise ValueError("No slide number provided")
    return sorted(numbers)


def _resolve_mapping_file(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    candidates = [Path("figma_mappings.json"), Path("figma-node-mapping.json")]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.slide and args.frames:
        parser.error("--slide and --frames cannot be used together")
    if args.all and (args.slide or args.frames):
        parser.error("--all cannot be used with --slide/--frames")
    if not args.test and not args.all and not args.slide and not args.frames:
        parser.error("Must specify one of --all, --slide, --frames (or use --test)")
    if args.update and not args.data:
        parser.error("--update requires --data")
    if args.scale <= 0:
        parser.error("--scale must be > 0")

    try:
        from gena_feed.content_parser import parse_content_file
        from gena_feed.fallback_handler import FallbackHandler
        from gena_feed.figma_client import FigmaApiError, FigmaClient
        from gena_feed.figma_exporter import FigmaExporter
        from gena_feed.figma_updater import FigmaPluginBridge, FigmaTemplateUpdater
    except ModuleNotFoundError as exc:
        print(f"[error] Missing dependency/module: {exc}", file=sys.stderr)
        print("[hint] Install dependencies first: pip install requests python-dotenv", file=sys.stderr)
        return 1

    fallback = FallbackHandler(use_html_fallback=args.fallback)

    try:
        client = FigmaClient()
    except ValueError as exc:
        print(f"[error] Configuration error: {exc}", file=sys.stderr)
        print("[hint] Configure FIGMA_ACCESS_TOKEN and FIGMA_FILE_ID (or FIGMA_FILE_KEY) in .env", file=sys.stderr)
        return 1

    if args.test:
        ok = client.test_connection()
        print("[ok] Figma API connection successful" if ok else "[error] Figma API connection failed")
        return 0 if ok else 1

    updater = FigmaTemplateUpdater(client)
    mapping_file = _resolve_mapping_file(args.mapping_file)

    try:
        updater.load_node_mappings(str(mapping_file))
    except FileNotFoundError:
        print(f"[error] Mapping file not found: {mapping_file}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[error] Failed to load mapping file {mapping_file}: {exc}", file=sys.stderr)
        return 1

    if not updater.node_mappings:
        print("[error] No node mapping entries were loaded", file=sys.stderr)
        return 1

    total_slides = len(updater.node_mappings)
    if args.all:
        selected_numbers = list(range(1, total_slides + 1))
    else:
        raw = args.slide or args.frames
        assert raw is not None
        try:
            selected_numbers = _parse_slide_numbers(raw)
        except ValueError as exc:
            print(f"[error] {exc}", file=sys.stderr)
            return 1

    selected_keys = [f"slide_{n:02d}" for n in selected_numbers]
    missing = [k for k in selected_keys if k not in updater.node_mappings]
    if missing:
        print(f"[error] Missing mapping keys: {', '.join(missing)}", file=sys.stderr)
        return 1

    print(f"[info] Loaded mappings: {total_slides}, selected: {len(selected_keys)}")

    if args.update:
        try:
            slides = parse_content_file(args.data)
        except Exception as exc:
            print(f"[error] Failed to parse content file {args.data}: {exc}", file=sys.stderr)
            return 1

        selected_set = set(selected_numbers)
        prepared_updates = []
        for slide in slides:
            if slide.slide_number not in selected_set:
                continue
            try:
                prepared_updates.append(updater.prepare_slide_data(slide))
            except Exception as exc:
                print(f"[warn] Skipping update for slide_{slide.slide_number:02d}: {exc}", file=sys.stderr)

        if not prepared_updates:
            print("[warn] No plugin update payloads were prepared")
        else:
            bridge = FigmaPluginBridge(bridge_dir=args.bridge_dir)
            request_path = bridge.write_update_request(prepared_updates)
            print(f"[info] Plugin update request written: {request_path}")
            if not args.dry_run:
                print("[action] Run the Figma plugin now, then press Enter to continue export...")
                input()
                ok = bridge.wait_for_completion(request_path, timeout=args.plugin_timeout)
                if not ok:
                    print("[error] Plugin update did not complete successfully", file=sys.stderr)
                    if args.fallback:
                        fb_result = fallback.run_html_fallback()
                        if fb_result.stdout.strip():
                            print(fb_result.stdout.strip())
                        if fb_result.stderr.strip():
                            print(fb_result.stderr.strip(), file=sys.stderr)
                        return 0 if fb_result.ok else 1
                    return 1

    if args.dry_run:
        print("[dry-run] Export plan")
        for key in selected_keys:
            mapping = updater.node_mappings[key]
            print(f"  - {key}: {mapping.frame_id}")
        return 0

    exporter = FigmaExporter(client, output_dir=args.output)
    exported_files: list[Path] = []

    try:
        for key in selected_keys:
            mapping = updater.node_mappings[key]
            filename = f"{key}.png"
            if args.optimize:
                out = exporter.export_with_optimization(mapping.frame_id, filename, optimize=True, scale=args.scale)
            else:
                out = exporter.export_slide(mapping.frame_id, filename, scale=args.scale, format="png")
            exported_files.append(out)
            print(f"[ok] Exported {key} -> {out}")
    except (FigmaApiError, RuntimeError, OSError) as exc:
        print(f"[error] Export failed: {exc}", file=sys.stderr)
        if args.fallback:
            fb_result = fallback.run_html_fallback()
            if fb_result.stdout.strip():
                print(fb_result.stdout.strip())
            if fb_result.stderr.strip():
                print(fb_result.stderr.strip(), file=sys.stderr)
            return 0 if fb_result.ok else 1
        return 1

    print(f"[done] Successfully exported {len(exported_files)} slide(s) to {Path(args.output).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
