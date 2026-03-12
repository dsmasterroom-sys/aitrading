#!/usr/bin/env python3
"""Napoleon Jacket carousel image generation pipeline."""

import base64
import json
import os
import sys
import time
import requests

BASE_DIR = "/Users/master/.openclaw/workspace/projects/gena_feed"
SERIES_DIR = os.path.join(BASE_DIR, "series/napoleon-jacket")
GEN_DIR = os.path.join(SERIES_DIR, "generated")
API_URL = "http://localhost:8000/api/generate"

NEGATIVE = "oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout"

DEFAULT_CONFIG = {
    "aspectRatio": "3:4",
    "guidanceScale": 3.5,
    "numInferenceSteps": 28
}

PHASE2_PROMPT = "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."


def file_to_data_uri(filepath):
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = filepath.rsplit(".", 1)[-1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


def generate(prompt, config, ref_images=None, negative=None, save_path=None, label=""):
    payload = {"prompt": prompt, "config": config}
    if ref_images:
        payload["referenceImages"] = ref_images
    if negative:
        payload["negativePrompt"] = negative

    print(f"\n{'='*60}")
    print(f"[GENERATING] {label}")
    print(f"  refs: {len(ref_images) if ref_images else 0}")
    print(f"  save: {save_path}")
    print(f"{'='*60}")

    for attempt in range(2):
        try:
            resp = requests.post(API_URL, json=payload, timeout=300)
            result = resp.json()

            if "url" in result:
                url = result["url"]
                if url.startswith("data:"):
                    header, b64data = url.split(",", 1)
                    img_bytes = base64.b64decode(b64data)
                else:
                    img_resp = requests.get(url, timeout=60)
                    img_bytes = img_resp.content

                if save_path:
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, "wb") as f:
                        f.write(img_bytes)
                    size_kb = len(img_bytes) / 1024
                    print(f"  [OK] Saved: {save_path} ({size_kb:.0f} KB)")
                return save_path or url
            else:
                print(f"  [ERROR] attempt {attempt+1}: {result}")
                if attempt == 0:
                    print("  Retrying in 5s...")
                    time.sleep(5)
        except Exception as e:
            print(f"  [EXCEPTION] attempt {attempt+1}: {e}")
            if attempt == 0:
                print("  Retrying in 5s...")
                time.sleep(5)

    print(f"  [FAILED] {label}")
    return None


def persona(name):
    return os.path.join(BASE_DIR, f"shared/persona/{name}")


def product(name):
    return os.path.join(BASE_DIR, f"shared/products/genarchive_crossbag/{name}")


def main():
    # ─── SLIDE 05: Detail macro (Phase 1 only) ───
    print("\n" + "█"*60)
    print("█  SLIDE 05 — Detail Macro (Phase 1 only)")
    print("█"*60)

    slide05 = generate(
        prompt='[INDICATIONS] Extreme close-up detail shot of a dark navy Napoleon jacket focusing on gold double-breasted buttons arranged in two parallel rows, ornate military-style button engravings, stand collar with structured boning, and decorative braiding along the front placket. [STYLE] Product hero macro photography, Kodak Portra 400 film emulation, muted cool tones, desaturated -15%, editorial product still life. [CAMERA SETTINGS] 100mm macro lens, f/2.8, extremely shallow depth of field with front button row in tack-sharp focus and rear row falling into soft blur, slightly angled top-down perspective at 30 degrees. [LIGHTING] Overcast soft diffused light 5500-6500K, low contrast, no harsh shadows, subtle directional light from upper left to reveal button engravings and fabric texture weave. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, visible thread stitching, gold button surface reflections, fabric weave texture at macro level, structured collar boning visible through fabric, military braiding detail crisp and clear. [SCENE & ACTION] The jacket resting on a matte light grey surface, camera pulled in extremely tight on the chest area where gold buttons, stand collar, and braiding converge, creating an intimate study of the three defining Napoleon jacket details — double-breasted button arrangement, stand collar architecture, and decorative military trim.',
        config=DEFAULT_CONFIG,
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "slide_05.png"),
        label="slide-05 detail macro"
    )
    if not slide05:
        print("FATAL: slide-05 failed")
        sys.exit(1)

    # ─── SLIDE 01: Cover (3-phase) ───
    print("\n" + "█"*60)
    print("█  SLIDE 01 — Cover (3-phase pipeline)")
    print("█"*60)

    s01_p1 = generate(
        prompt='[INDICATIONS] A dark charcoal-black Napoleon jacket with prominent gold double-breasted buttons, two-row button arrangement, stand collar, military-inspired structured shoulders, paired with black slim-fit trousers and black leather ankle boots, neatly arranged on a light beige linen surface. [STYLE] Editorial flat-lay, clean minimalist arrangement, Kodak Portra 400 film emulation, muted warm tones, desaturated -10%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across entire frame. [LIGHTING] Soft diffused natural window light from upper left, 5500K neutral daylight, minimal shadows, even illumination. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic fabric textures, visible gold button engravings, structured jacket silhouette preserved in lay-flat position. [SCENE & ACTION] Garments laid flat on a natural linen backdrop, each piece spaced with intentional breathing room, gold buttons catching subtle light reflection, military details clearly visible.',
        config=DEFAULT_CONFIG,
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "outfits/look_cover.png"),
        label="slide-01 Phase 1 flat-lay"
    )
    if not s01_p1:
        print("FATAL: slide-01 Phase 1 failed"); sys.exit(1)

    s01_p2 = generate(
        prompt=PHASE2_PROMPT,
        config=DEFAULT_CONFIG,
        ref_images=[
            file_to_data_uri(persona("gena_ref_02_medium_straight.png")),
            file_to_data_uri(s01_p1)
        ],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "compositions/comp_cover.png"),
        label="slide-01 Phase 2 composition"
    )
    if not s01_p2:
        print("FATAL: slide-01 Phase 2 failed"); sys.exit(1)

    s01_p3 = generate(
        prompt='[INDICATIONS] A Korean fashion model influencer wearing a dark charcoal-black Napoleon jacket with gold double-breasted buttons, black slim trousers, and black ankle boots, captured in a confident side profile walking pose. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft highlight rolloff, subtle film grain at ISO 400, clean urban atmosphere. [CAMERA SETTINGS] 85mm f/1.8, shallow depth of field, side profile framing, model occupying left 40% of frame, background softly blurred, shot at slight low angle. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, no harsh shadows, cool neutral tones, even illumination wrapping the figure, subtle directional light from camera-right revealing gold button details and jacket structure. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic skin texture, visible gold button reflections catching soft diffused light, structured jacket shoulder line sharp against blurred background, natural hair movement from gentle breeze, cool-toned urban greys and soft blues in environment. [SCENE & ACTION] Walking along a quiet Seoul side street (Seongsu-dong aesthetic — exposed brick, minimal signage), mid-stride with one foot forward, chin slightly lifted, gaze directed ahead past camera, overcast sky creating even cool light across the jacket\'s military details, the street stretching into soft bokeh behind her.',
        config=DEFAULT_CONFIG,
        ref_images=[file_to_data_uri(s01_p2)],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "slide_01.png"),
        label="slide-01 Phase 3 final"
    )
    if not s01_p3:
        print("FATAL: slide-01 Phase 3 failed"); sys.exit(1)

    # ─── SLIDE 07: Office look (3-phase) ───
    print("\n" + "█"*60)
    print("█  SLIDE 07 — Office Look (3-phase pipeline)")
    print("█"*60)

    s07_p1 = generate(
        prompt='[INDICATIONS] A charcoal Napoleon jacket with gold double-breasted buttons and structured shoulders, paired with charcoal-grey wide-leg trousers, black leather penny loafers, and a Burnished Lilac (smoky lavender) silk scarf loosely draped, all arranged on a cream linen surface. [STYLE] Editorial flat-lay, clean minimalist arrangement, Kodak Portra 400 film emulation, muted neutral tones, cool undertone, desaturated -10%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across entire frame. [LIGHTING] Soft diffused natural window light from upper left, 5500K neutral daylight, minimal shadows, even illumination. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic fabric textures, visible weave on trousers, silk scarf translucency, gold button detail, lavender scarf as the single color accent against monochrome palette. [SCENE & ACTION] Office-ready outfit laid flat with intentional spacing, the lilac scarf casually draped across the jacket collar area suggesting how it would be worn, loafers placed at bottom with toes pointing outward, creating a complete outfit story from top to bottom.',
        config=DEFAULT_CONFIG,
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "outfits/look1_office.png"),
        label="slide-07 Phase 1 flat-lay"
    )
    if not s07_p1:
        print("FATAL: slide-07 Phase 1 failed"); sys.exit(1)

    s07_p2 = generate(
        prompt=PHASE2_PROMPT,
        config=DEFAULT_CONFIG,
        ref_images=[
            file_to_data_uri(persona("gena_ref_03_basic_straight.png")),
            file_to_data_uri(s07_p1)
        ],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "compositions/comp_look1_office.png"),
        label="slide-07 Phase 2 composition"
    )
    if not s07_p2:
        print("FATAL: slide-07 Phase 2 failed"); sys.exit(1)

    s07_p3 = generate(
        prompt='[INDICATIONS] A Korean fashion model influencer wearing a charcoal Napoleon jacket with gold buttons, charcoal wide-leg trousers, black penny loafers, and a Burnished Lilac silk scarf loosely tied at the neck, walking confidently through a modern office building lobby. [STYLE] Street documentary meets editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, natural unposed energy, slight motion captured. [CAMERA SETTINGS] 35mm f/2.0, low angle shot from near ground level looking up, full body in frame, converging vertical lines of the building adding dynamism, 1/250s shutter freezing mid-stride. [LIGHTING] Overcast daylight filtering through large glass lobby windows, 5500-6500K cool neutral, low contrast, soft even illumination with no harsh shadows, slight cool reflection from marble or concrete flooring. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, visible gold button details on jacket, lilac scarf color accurate as the single warm accent, shoe-level perspective creating empowering upward gaze, natural straight hair with subtle movement. [SCENE & ACTION] Descending the last two steps of a modern minimalist office building staircase (polished concrete, glass railings, clean lines), mid-stride with purpose, one hand adjusting the lilac scarf at her neck, the other arm swinging naturally, looking slightly downward at her path with a focused expression, the geometric architecture framing her figure from this low vantage point.',
        config=DEFAULT_CONFIG,
        ref_images=[file_to_data_uri(s07_p2)],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "slide_07.png"),
        label="slide-07 Phase 3 final"
    )
    if not s07_p3:
        print("FATAL: slide-07 Phase 3 failed"); sys.exit(1)

    # ─── SLIDE 08: Weekend look (3-phase) ───
    print("\n" + "█"*60)
    print("█  SLIDE 08 — Weekend Look (3-phase pipeline)")
    print("█"*60)

    s08_p1 = generate(
        prompt='[INDICATIONS] A black Napoleon jacket with silver-toned military buttons and structured shoulders, paired with light blue wide-leg raw-hem denim jeans, white leather low-top sneakers, and a Muskmelon (soft warm orange) canvas tote bag, all arranged on a light grey concrete surface. [STYLE] UGC-inspired flat-lay, slightly imperfect casual arrangement, Kodak Portra 400 film emulation, muted tones with the orange tote as sole color pop, desaturated -10%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across frame. [LIGHTING] Overcast diffused daylight, 6000K cool neutral, low contrast, even soft illumination. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic denim texture, visible raw hem fraying, sneaker sole texture, tote bag canvas weave, military button detail on black jacket. [SCENE & ACTION] Weekend outfit casually arranged — jacket slightly angled as if just tossed down, jeans folded once at the waist, sneakers placed at a playful angle, the muskmelon tote bag partially overlapping the jeans suggesting effortless pairing.',
        config=DEFAULT_CONFIG,
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "outfits/look2_weekend.png"),
        label="slide-08 Phase 1 flat-lay"
    )
    if not s08_p1:
        print("FATAL: slide-08 Phase 1 failed"); sys.exit(1)

    s08_p2 = generate(
        prompt=PHASE2_PROMPT,
        config=DEFAULT_CONFIG,
        ref_images=[
            file_to_data_uri(persona("gena_ref_08_double_down_braid.png")),
            file_to_data_uri(s08_p1)
        ],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "compositions/comp_look2_weekend.png"),
        label="slide-08 Phase 2 composition"
    )
    if not s08_p2:
        print("FATAL: slide-08 Phase 2 failed"); sys.exit(1)

    s08_p3 = generate(
        prompt='[INDICATIONS] A Korean fashion model influencer wearing a black Napoleon jacket with military buttons, light blue wide-leg denim jeans, white sneakers, carrying a Muskmelon (warm soft orange) tote bag on one shoulder, captured in a POV selfie angle on a Seoul street. [STYLE] UGC candid selfie aesthetic, shot on iPhone 16 Pro, computational photography look, natural HDR, slight lens flare, soft highlight rolloff, Portrait mode bokeh, true-to-life color science, subtle noise grain at ISO 800, Kodak Portra 400 color palette overlay, muted cool tones. [CAMERA SETTINGS] 24mm wide-angle front camera, f/1.9, above eye-level selfie angle, upper body and face in frame, one arm extended holding phone (implied), background falling into natural Portrait mode bokeh. [LIGHTING] Overcast cloudy day diffused light, 6000-6500K cool neutral, low contrast, flat even illumination, no harsh shadows on face, soft catchlight in eyes. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, natural skin texture with minimal retouching look, double down braid hairstyle clearly visible, muskmelon tote bag color accurate as warm accent against cool-toned outfit, denim texture visible at waist area. [SCENE & ACTION] Standing in a Seongsu-dong alley with indie cafe storefronts softly blurred behind her, one hand holding phone up for selfie (POV — we see from phone\'s perspective), the other hand casually holding the tote bag strap on her shoulder, slight head tilt with a relaxed closed-lip half-smile, natural candid energy as if snapping a quick outfit check before meeting friends.',
        config=DEFAULT_CONFIG,
        ref_images=[file_to_data_uri(s08_p2)],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "slide_08.png"),
        label="slide-08 Phase 3 final"
    )
    if not s08_p3:
        print("FATAL: slide-08 Phase 3 failed"); sys.exit(1)

    # ─── SLIDE 09: Date look + sponsored bag (3-phase) ───
    print("\n" + "█"*60)
    print("█  SLIDE 09 — Date Look + Crossbag (3-phase pipeline)")
    print("█"*60)

    s09_p1 = generate(
        prompt='[INDICATIONS] A light grey Napoleon jacket with gold double-breasted buttons and structured military shoulders, paired with an ivory champagne satin midi skirt with subtle sheen, nude leather strappy heeled sandals, and a baby pink silk camisole as the inner layer, all arranged on a warm beige linen surface. [STYLE] Editorial feminine flat-lay, elegant arrangement, Kodak Portra 400 film emulation, warm muted tones, soft pink and champagne palette, desaturated -5%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across entire frame. [LIGHTING] Warm diffused light from upper right, 4500K slightly warm, minimal shadows, satin skirt catching soft highlights. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic satin sheen on skirt, silk camisole delicate texture, gold button detail on grey jacket, nude heel strap detail, overall feminine-military contrast visible in the arrangement. [SCENE & ACTION] Date night outfit elegantly arranged — the grey jacket placed open to reveal the baby pink camisole layered beneath, satin skirt fanned slightly to show its drape and sheen, heels placed at the bottom with straps artfully visible, creating a romantic yet structured outfit narrative.',
        config=DEFAULT_CONFIG,
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "outfits/look3_date.png"),
        label="slide-09 Phase 1 flat-lay"
    )
    if not s09_p1:
        print("FATAL: slide-09 Phase 1 failed"); sys.exit(1)

    s09_p2 = generate(
        prompt=PHASE2_PROMPT,
        config=DEFAULT_CONFIG,
        ref_images=[
            file_to_data_uri(persona("gena_ref_07_long_halfupdown_wave.png")),
            file_to_data_uri(s09_p1)
        ],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "compositions/comp_look3_date.png"),
        label="slide-09 Phase 2 composition"
    )
    if not s09_p2:
        print("FATAL: slide-09 Phase 2 failed"); sys.exit(1)

    s09_p3 = generate(
        prompt='[INDICATIONS] A Korean fashion model influencer wearing a light grey Napoleon jacket with gold double-breasted buttons over a baby pink silk camisole, an ivory champagne satin midi skirt, nude strappy heels, and a matte black minimalist crossbody bag worn cross-body, captured from a rear three-quarter angle walking away. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft diffused atmosphere, subtle film grain at ISO 400, clean elegant mood. [CAMERA SETTINGS] 50mm f/1.4, rear three-quarter view from behind-right, full body in frame, shallow depth of field with background restaurant facades falling into creamy bokeh, shot at eye level. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, cool neutral tones, no harsh shadows, even illumination with subtle directional light from camera-left, satin skirt catching soft diffused highlights, gentle cool reflection from surrounding surfaces. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, long half-up-down wavy hair with natural movement, crossbody bag strap visible across her back with bag resting at hip level — bag details clearly visible (matte black nylon, minimal hardware), gold jacket buttons catching soft diffused light, satin skirt movement captured mid-stride, baby pink camisole peeking at neckline, cool urban greys and muted tones in environment. [SCENE & ACTION] Walking along a quiet Hannam-dong street on an overcast day, passing a restaurant entrance with soft interior glow visible through windows, mid-stride with satin skirt swaying, one hand lightly touching the crossbody bag strap, head turned slightly to the right giving a three-quarter profile glimpse, the cool diffused light creating an elegant cinematic atmosphere, the military-structured jacket contrasting beautifully with the flowing feminine skirt.',
        config=DEFAULT_CONFIG,
        ref_images=[
            file_to_data_uri(s09_p2),
            file_to_data_uri(product("genarchive_crossbag_fit.png")),
            file_to_data_uri(product("genarchive_crossbag_4-view.png"))
        ],
        negative=NEGATIVE,
        save_path=os.path.join(GEN_DIR, "slide_09.png"),
        label="slide-09 Phase 3 final"
    )
    if not s09_p3:
        print("FATAL: slide-09 Phase 3 failed"); sys.exit(1)

    # ─── Summary ───
    print("\n" + "="*60)
    print("ALL DONE! Generated files:")
    print("="*60)
    for root, dirs, files in os.walk(GEN_DIR):
        for f in sorted(files):
            fp = os.path.join(root, f)
            size = os.path.getsize(fp) / 1024
            print(f"  {fp} ({size:.0f} KB)")


if __name__ == "__main__":
    main()
