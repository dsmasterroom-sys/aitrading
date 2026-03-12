import base64, json, requests, os, time

BASE = "/Users/master/.openclaw/workspace/projects/gena_feed"
SERIES = f"{BASE}/series/napoleon-jacket"
PERSONA = f"{BASE}/shared/persona"
PRODUCTS = f"{BASE}/shared/products/genarchive_crossbag"

def file_to_data_uri(filepath):
    ext = filepath.lower().split('.')[-1]
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"

COMP_PROMPT = "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."

NEGATIVE = "oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout, readable text, signage, store names, Korean text, Japanese text, Chinese characters, kanji"

CONFIG = {"aspectRatio": "3:4", "guidanceScale": 3.5, "numInferenceSteps": 28}

def generate(prompt, refs_paths, save_path, negative=None):
    refs = [file_to_data_uri(p) for p in refs_paths]
    payload = {
        "prompt": prompt,
        "config": CONFIG,
        "referenceImages": refs
    }
    if negative:
        payload["negativePrompt"] = negative

    print(f"\n{'='*60}")
    print(f"[GENERATING] {save_path.split('/')[-1]}")
    print(f"  refs: {len(refs)}")
    print(f"{'='*60}")

    for attempt in range(2):
        try:
            resp = requests.post("http://localhost:8000/api/generate", json=payload, timeout=600)
            result = resp.json()
            if "url" in result:
                url = result["url"]
                if url.startswith("data:"):
                    header, b64data = url.split(",", 1)
                    img_bytes = base64.b64decode(b64data)
                else:
                    img_bytes = requests.get(url).content
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  [OK] Saved: {save_path} ({len(img_bytes)//1024} KB)")
                return save_path
            else:
                print(f"  [ERROR] {result}")
        except Exception as e:
            print(f"  [EXCEPTION] attempt {attempt+1}: {e}")
            if attempt == 0:
                time.sleep(5)
    return None

slides = [
    {
        "name": "slide-01",
        "persona": f"{PERSONA}/gena_ref_02_medium_straight.png",
        "outfit": f"{SERIES}/generated/outfits/look_cover.jpeg",
        "comp_save": f"{SERIES}/generated/compositions/comp_cover.png",
        "final_save": f"{SERIES}/generated/slide_01.png",
        "final_prompt": '[INDICATIONS] A Korean fashion model influencer wearing a black cropped Napoleon military jacket with elaborate braiding trim (passementerie loops) across the chest, antique silver buttons, structured stand collar, paired with a white ruffled blouse underneath peeking at cuffs and hem, black wide-leg trousers with a decorative chain belt, and black pointed-toe ankle boots. No bag, no backpack. No overlay, no text, no logo, no signage. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft highlight rolloff, subtle film grain at ISO 400, clean urban atmosphere. [CAMERA SETTINGS] 85mm f/1.8, shallow depth of field, side profile framing, model occupying left 40% of frame, background softly blurred, shot at slight low angle. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, no harsh shadows, cool neutral tones, even illumination wrapping the figure. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic skin texture, braiding trim loops clearly visible on jacket chest, antique buttons catching soft light, ruffled blouse detail at wrists, chain belt glinting subtly, cool-toned urban greys and soft blues. [SCENE & ACTION] Walking along a quiet Seoul side street with weathered brick walls and minimal architectural details — no readable signs or text visible. Mid-stride with one foot forward, chin slightly lifted, gaze directed ahead past camera, one hand casually at side, the overcast sky creating even cool light across the jacket\'s military braiding details.',
        "extra_refs": []
    },
    {
        "name": "slide-07",
        "persona": f"{PERSONA}/gena_ref_03_basic_straight.png",
        "outfit": f"{SERIES}/generated/outfits/look1_office.jpg",
        "comp_save": f"{SERIES}/generated/compositions/comp_look1_office.png",
        "final_save": f"{SERIES}/generated/slide_07.png",
        "final_prompt": '[INDICATIONS] A Korean fashion model influencer wearing a navy-black cropped Napoleon jacket with gold buttons and front flap pockets, a crisp white dress shirt underneath with cuffs showing, charcoal wide-leg trousers, and dark leather loafers. Clean office-ready styling. No overlay, no text, no logo, no signage. [STYLE] Street documentary meets editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, natural unposed energy, slight motion captured. [CAMERA SETTINGS] 35mm f/2.0, low angle shot from near ground level looking up, full body in frame, converging vertical lines adding dynamism, 1/250s shutter freezing mid-stride. [LIGHTING] Overcast daylight filtering through large glass windows, 5500-6500K cool neutral, low contrast, soft even illumination, slight cool reflection from polished concrete flooring. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, gold buttons on jacket clearly visible, white shirt cuffs extending below jacket sleeves, shoe-level perspective creating empowering upward gaze, natural straight hair with subtle movement. [SCENE & ACTION] Descending the last two steps of a modern minimalist building staircase — polished concrete, glass and steel railings, clean geometric lines, NO text or signage visible. Mid-stride with purpose, one hand holding a suede tote bag, looking slightly downward with a focused expression, geometric architecture framing her figure.',
        "extra_refs": []
    },
    {
        "name": "slide-08",
        "persona": f"{PERSONA}/gena_ref_08_double_down_braid.png",
        "outfit": f"{SERIES}/generated/outfits/look2_weekend.jpeg",
        "comp_save": f"{SERIES}/generated/compositions/comp_look2_weekend.png",
        "final_save": f"{SERIES}/generated/slide_08.png",
        "final_prompt": '[INDICATIONS] A Korean fashion model influencer wearing a black cropped Napoleon military jacket with elaborate braiding trim (passementerie loops) across the chest, open and unbuttoned showing a hint of midriff, antique silver buttons, paired with low-rise light blue wide-leg denim jeans, hands casually at sides or one in pocket. No overlay, no text, no logo, no signage. [STYLE] UGC candid selfie aesthetic, shot on iPhone 16 Pro, computational photography look, natural HDR, slight lens flare, soft highlight rolloff, Portrait mode bokeh, true-to-life color science, subtle noise grain at ISO 800, Kodak Portra 400 color palette, muted cool tones. [CAMERA SETTINGS] 24mm wide-angle front camera, f/1.9, above eye-level selfie angle, upper body and face in frame, background falling into natural Portrait mode bokeh. [LIGHTING] Overcast cloudy day diffused light, 6000-6500K cool neutral, low contrast, flat even illumination, no harsh shadows, soft catchlight in eyes. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, natural skin texture, double down braid hairstyle clearly visible, Napoleon jacket braiding trim loops visible on chest, open jacket showing casual confidence, low-rise denim waistband detail. [SCENE & ACTION] Standing in a quiet alley with brick walls and potted plants softly blurred behind — NO readable text or store signs. POV selfie angle, one hand extended holding phone, slight head tilt with relaxed closed-lip half-smile, natural candid energy, bold casual styling with open jacket.',
        "extra_refs": []
    },
    {
        "name": "slide-09",
        "persona": f"{PERSONA}/gena_ref_07_long_halfupdown_wave.png",
        "outfit": f"{SERIES}/generated/outfits/look3_date.jpeg",
        "comp_save": f"{SERIES}/generated/compositions/comp_look3_date.png",
        "final_save": f"{SERIES}/generated/slide_09.png",
        "final_prompt": '[INDICATIONS] A Korean fashion model influencer wearing an ivory/cream-colored Napoleon military jacket with fabric-covered buttons in a single row, structured stand collar, fitted waist-hugging silhouette, paired with a black flowing maxi skirt and black pointed-toe flats. She wears a compact matte black nylon mini crossbody sling bag DIAGONALLY ACROSS HER TORSO — strap from left shoulder to right hip, small rectangular bag at right hip. No overlay, no text, no logo, no signage. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft diffused atmosphere, subtle film grain at ISO 400, clean elegant mood. [CAMERA SETTINGS] 50mm f/1.4, rear three-quarter view from behind-right, full body in frame, shallow depth of field with background facades in creamy bokeh, shot at eye level. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, cool neutral tones, no harsh shadows, even illumination, skirt catching soft diffused highlights. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, long half-up-down wavy hair with natural movement, crossbody sling bag strap DIAGONALLY visible from left shoulder across back to right hip, bag is small compact rectangle at hip, ivory jacket stand collar visible from rear, black maxi skirt flowing mid-stride. [SCENE & ACTION] Walking along a quiet upscale Seoul street on an overcast day — clean modern building facades with warm interior lights through large glass windows, NO readable text or signs. Mid-stride with skirt flowing, right hand touching crossbody bag at hip, head turned slightly right for three-quarter profile, the light-colored military jacket creating striking contrast with the black skirt.',
        "extra_refs": [
            f"{PRODUCTS}/genarchive_crossbag_fit.png",
            f"{PRODUCTS}/genarchive_crossbag_4-view.png"
        ]
    }
]

print("=" * 60)
print("PHASE 2 + PHASE 3 PIPELINE — USER REFERENCE OUTFITS")
print("=" * 60)

for s in slides:
    # Phase 2: Composition
    print(f"\n{'█' * 60}")
    print(f"█  {s['name'].upper()} — Phase 2 + Phase 3")
    print(f"{'█' * 60}")

    comp_result = generate(
        prompt=COMP_PROMPT,
        refs_paths=[s["persona"], s["outfit"]],
        save_path=s["comp_save"]
    )

    if not comp_result:
        print(f"  [FAILED] {s['name']} Phase 2 — skipping Phase 3")
        continue

    # Phase 3: Final
    final_refs = [comp_result] + s["extra_refs"]
    generate(
        prompt=s["final_prompt"],
        refs_paths=final_refs,
        save_path=s["final_save"],
        negative=NEGATIVE
    )

print("\n\n" + "=" * 60)
print("ALL DONE!")
print("=" * 60)
