#!/usr/bin/env python3
"""cherry-blossom-v2 Nanogen Image Generation Pipeline
Reads prompts from nanogen-prompts/image_slide_XX.md files."""

import base64, json, os, re, sys, time, requests

API = "http://localhost:8000/api/generate"
BASE = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(os.path.dirname(os.path.dirname(BASE)), "shared")
GEN = os.path.join(BASE, "generated")
PROMPTS_DIR = os.path.join(BASE, "nanogen-prompts")
os.makedirs(os.path.join(GEN, "outfits"), exist_ok=True)
os.makedirs(os.path.join(GEN, "compositions"), exist_ok=True)

DEFAULT_NEG = ("oversaturated, western aesthetic, heavy filter, text overlay, "
               "cluttered background, artificial glamour, unnatural skin, plastic look, "
               "stiff pose, mannequin-like, stock photo feel, generic smile, "
               "bad anatomy, extra fingers, deformed hands, blurry face, "
               "watermark, signature, logo, frame border, collage layout, "
               "AI-generated artifact, synthetic appearance, disproportionate body")

CONFIG = {"aspectRatio": "4:5", "resolution": "1080x1350"}

# ── Slide metadata: persona + look mapping ──
SLIDES = {
    "01": {"persona": "gena_ref_06_long_wave.png",       "look": "A", "phases": [1,2,3]},
    "02": {"persona": "gena_ref_03_basic_straight.png",   "look": "B", "phases": [1,2,3]},
    "03": {"persona": None,                               "look": None, "phases": [3]},
    "04": {"persona": "gena_ref_02_medium_straight.png",  "look": "C", "phases": [1,2,3]},
    "05": {"persona": "gena_ref_05_updo.png",             "look": "D", "phases": [1,2,3]},
    "06": {"persona": "gena_ref_01_long_twinhalfup_wave.png", "look": "D", "phases": [2,3]},
    "07": {"persona": None,                               "look": None, "phases": [3]},
    "08": {"persona": "gena_ref_09_long_hippie.png",      "look": "D", "phases": [2,3], "product_refs": True},
    "09": {"persona": "gena_ref_07_long_halfupdown_wave.png", "look": "A", "phases": [2,3]},
    "10": {"persona": "gena_ref_04_high_braid_ponytail.png", "look": None, "phases": [3]},
}

# Flat-lay prompt definitions per look (only A-D need flat-lays)
LOOK_SLIDES = {"A": "01", "B": "02", "C": "04", "D": "05"}

COMP_PROMPT = ("Change only the main clothing garments to strictly match the design, "
               "texture, and details of the provided clothing reference image. "
               "Replicate the attached outfit exactly. Crucially, preserve all "
               "original accessories intact. Keep the original model's face, pose, "
               "hair, background, and lighting exactly the same. "
               "Seamless integration, photorealistic, 8k resolution.")


def to_data_uri(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = path.lower().split(".")[-1]
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


def save_result(resp_json, out_path):
    url = resp_json.get("url", "")
    if "," in url:
        data = base64.b64decode(url.split(",", 1)[1])
    else:
        data = base64.b64decode(url)
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"  -> Saved: {os.path.basename(out_path)} ({len(data)//1024}KB)")


def generate(prompt, neg=None, refs=None, out_path=None):
    body = {"prompt": prompt, "negativePrompt": neg or DEFAULT_NEG,
            "config": CONFIG, "referenceImages": refs or []}
    print(f"  API call... ({len(refs or [])} refs)")
    try:
        r = requests.post(API, json=body, timeout=600)
        r.raise_for_status()
        d = r.json()
        if out_path:
            save_result(d, out_path)
        return d
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def parse_prompt_md(slide_num):
    """Parse a nanogen-prompts/image_slide_XX.md file.
    Returns dict with keys: phase1_prompt, phase2_prompt, phase3_prompt,
    phase1_neg, phase3_neg (extracted from **Negative prompt:** lines)"""
    path = os.path.join(PROMPTS_DIR, f"image_slide_{slide_num}.md")
    with open(path, "r") as f:
        content = f.read()

    result = {}
    # Extract Phase 3 prompt (always present)
    phase3_match = re.search(
        r"## Phase 3.*?\n\n\*\*Prompt:\*\*\n(.*?)(?=\n\*\*Negative prompt:\*\*)",
        content, re.DOTALL
    )
    if not phase3_match:
        # Try "Phase 3 only" variant
        phase3_match = re.search(
            r"## Phase 3.*?\n\n\*\*Prompt:\*\*\n(.*?)(?=\n\*\*Negative prompt:\*\*)",
            content, re.DOTALL
        )
    if phase3_match:
        result["phase3_prompt"] = phase3_match.group(1).strip()

    # Extract Phase 1 prompt (if present)
    phase1_match = re.search(
        r"## Phase 1.*?\n\n\*\*Prompt:\*\*\n(.*?)(?=\n\*\*Negative prompt:\*\*)",
        content, re.DOTALL
    )
    if phase1_match:
        result["phase1_prompt"] = phase1_match.group(1).strip()

    # Extract negative prompts
    neg_matches = re.findall(r"\*\*Negative prompt:\*\*\s*(.*?)(?:\n)", content)
    if neg_matches:
        result["neg"] = neg_matches[-1].strip()  # Use the last (Phase 3) neg

    return result


def persona_uri(name):
    return to_data_uri(os.path.join(SHARED, "persona", name))


def product_ref_uris():
    folder = os.path.join(SHARED, "products", "genarchive_crossbag")
    return [to_data_uri(os.path.join(folder, f))
            for f in sorted(os.listdir(folder)) if f.endswith(".png")]


def run():
    print("=" * 60)
    print("cherry-blossom-v2 Image Generation Pipeline (v2 — .md based)")
    print("=" * 60)

    flatlay_paths = {}
    comp_paths = {}

    # ── PHASE 1: Flat-lays (one per unique look) ──
    print("\n▶ PHASE 1: Generating outfit flat-lays...")
    for look_id, src_slide in LOOK_SLIDES.items():
        out = os.path.join(GEN, "outfits", f"look_{look_id}.png")
        if os.path.exists(out):
            print(f"  Look {look_id}: Already exists, skipping")
            flatlay_paths[look_id] = out
            continue
        prompts = parse_prompt_md(src_slide)
        if "phase1_prompt" not in prompts:
            print(f"  Look {look_id}: No Phase 1 prompt in slide {src_slide}, skipping")
            continue
        print(f"  Look {look_id} (from slide {src_slide}):")
        r = generate(prompts["phase1_prompt"], neg=prompts.get("neg"), refs=[], out_path=out)
        if r:
            flatlay_paths[look_id] = out
        time.sleep(2)

    # ── PHASE 2: Compositions ──
    print("\n▶ PHASE 2: Generating compositions (persona + outfit)...")
    for sid, meta in SLIDES.items():
        if 2 not in meta["phases"]:
            continue
        out = os.path.join(GEN, "compositions", f"comp_slide_{sid}.png")
        if os.path.exists(out):
            print(f"  Slide {sid}: Already exists, skipping")
            comp_paths[sid] = out
            continue
        look_id = meta["look"]
        if look_id not in flatlay_paths:
            print(f"  Slide {sid}: No flatlay for look {look_id}, skipping")
            continue
        print(f"  Slide {sid}: persona={meta['persona']} + look={look_id}")
        refs = [persona_uri(meta["persona"]), to_data_uri(flatlay_paths[look_id])]
        r = generate(COMP_PROMPT, refs=refs, out_path=out)
        if r:
            comp_paths[sid] = out
        time.sleep(2)

    # ── PHASE 3: Final slides ──
    print("\n▶ PHASE 3: Generating final slide images...")
    prod_refs = product_ref_uris()
    for sid, meta in SLIDES.items():
        out = os.path.join(GEN, f"slide_{sid}.png")
        if os.path.exists(out):
            print(f"  Slide {sid}: Already exists, skipping")
            continue
        prompts = parse_prompt_md(sid)
        if "phase3_prompt" not in prompts:
            print(f"  Slide {sid}: No Phase 3 prompt found, skipping")
            continue
        print(f"  Slide {sid}:")
        refs = []
        # Use composition result if available
        if sid in comp_paths:
            refs.append(to_data_uri(comp_paths[sid]))
        # Persona-only for slides without composition but with persona
        elif meta["persona"] and 2 not in meta["phases"]:
            refs.append(persona_uri(meta["persona"]))
        # Product refs if flagged
        if meta.get("product_refs"):
            refs.extend(prod_refs)
        r = generate(prompts["phase3_prompt"], neg=prompts.get("neg"), refs=refs, out_path=out)
        time.sleep(2)

    # ── Summary ──
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    for f in sorted(os.listdir(GEN)):
        if f.endswith(".png"):
            sz = os.path.getsize(os.path.join(GEN, f)) // 1024
            print(f"  {f}: {sz}KB")
    for sub in ["outfits", "compositions"]:
        d = os.path.join(GEN, sub)
        if os.path.exists(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".png"):
                    sz = os.path.getsize(os.path.join(d, f)) // 1024
                    print(f"  {sub}/{f}: {sz}KB")


if __name__ == "__main__":
    run()
