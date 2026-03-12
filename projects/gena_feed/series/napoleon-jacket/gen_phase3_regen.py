import base64, json, requests, os, time

BASE = "/Users/master/.openclaw/workspace/projects/gena_feed/series/napoleon-jacket"
PRODUCTS = "/Users/master/.openclaw/workspace/projects/gena_feed/shared/products/genarchive_crossbag"

def file_to_data_uri(filepath):
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"

NEGATIVE = "oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout, readable text, signage, store names, Korean text, Japanese text, Chinese characters, kanji, backpack, clutch, extra accessories not described in prompt"

CONFIG = {"aspectRatio": "3:4", "guidanceScale": 3.5, "numInferenceSteps": 28}

def generate(prompt, refs_paths, save_path):
    refs = [file_to_data_uri(p) for p in refs_paths]
    payload = {
        "prompt": prompt,
        "negativePrompt": NEGATIVE,
        "config": CONFIG,
        "referenceImages": refs
    }
    print(f"\n{'='*60}")
    print(f"[GENERATING] {os.path.basename(save_path)}")
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
                return True
            else:
                print(f"  [ERROR] {result}")
        except Exception as e:
            print(f"  [EXCEPTION] attempt {attempt+1}: {e}")
            if attempt == 0:
                time.sleep(5)
    return False

# SLIDE 01 — Cover, side profile
generate(
    prompt="[INDICATIONS] A Korean fashion model influencer wearing a dark charcoal-black NAPOLEON MILITARY JACKET with prominent gold double-breasted buttons arranged in two parallel rows, high structured stand collar, military epaulettes on shoulders, and decorative braiding along the front placket. Paired with black slim-fit trousers and black leather ankle boots. No other accessories — no bag, no backpack, no clutch, no scarf. Hands free or one hand in pocket. No overlay, no text, no logo, no signage. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft highlight rolloff, subtle film grain at ISO 400, clean urban atmosphere. [CAMERA SETTINGS] 85mm f/1.8, shallow depth of field, side profile framing, model occupying left 40% of frame, background softly blurred, shot at slight low angle. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, no harsh shadows, cool neutral tones, even illumination wrapping the figure, subtle directional light from camera-right revealing gold button details and structured stand collar. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic skin texture, visible gold double-breasted button rows catching soft diffused light, structured military shoulder line with epaulettes sharp against blurred background, stand collar rising to jawline clearly visible in profile, natural medium straight hair with subtle movement, cool-toned urban greys and soft blues. [SCENE & ACTION] Walking along a quiet Seoul side street with weathered brick walls and minimal architectural details — no readable signs or text visible anywhere in frame. Mid-stride with one foot forward, chin slightly lifted, gaze directed ahead past camera, hands free at sides, the overcast sky creating even cool light across the Napoleon jacket's military details, the street stretching into soft bokeh behind her.",
    refs_paths=[f"{BASE}/generated/compositions/comp_cover.png"],
    save_path=f"{BASE}/generated/slide_01.png"
)

# SLIDE 07 — Office, low angle walking
generate(
    prompt="[INDICATIONS] A Korean fashion model influencer wearing a charcoal NAPOLEON MILITARY JACKET with gold double-breasted buttons in two rows, structured stand collar, military epaulettes, paired with charcoal-grey wide-leg trousers, black leather penny loafers, and a Burnished Lilac (smoky lavender) silk scarf loosely tied at the neck. No other accessories. No overlay, no text, no logo, no signage. [STYLE] Street documentary meets editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, natural unposed energy, slight motion captured. [CAMERA SETTINGS] 35mm f/2.0, low angle shot from near ground level looking up, full body in frame, converging vertical lines of the building adding dynamism, 1/250s shutter freezing mid-stride. [LIGHTING] Overcast daylight filtering through large glass windows, 5500-6500K cool neutral, low contrast, soft even illumination with no harsh shadows, slight cool reflection from polished concrete flooring. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, visible gold double-breasted button rows on jacket, stand collar rising to jawline, military epaulettes on shoulders, lilac scarf color accurate as the single warm accent against monochrome outfit, shoe-level perspective creating empowering upward gaze, natural straight hair with subtle movement. [SCENE & ACTION] Descending the last two steps of a modern minimalist building staircase — polished concrete steps, glass and steel railings, clean geometric lines, NO text or signage visible. Mid-stride with purpose, one hand adjusting the lilac scarf at her neck, looking slightly downward with a focused expression, the geometric architecture framing her figure from this low vantage point.",
    refs_paths=[f"{BASE}/generated/compositions/comp_look1_office.png"],
    save_path=f"{BASE}/generated/slide_07.png"
)

# SLIDE 08 — Weekend, POV selfie
generate(
    prompt="[INDICATIONS] A Korean fashion model influencer wearing a black NAPOLEON MILITARY JACKET with silver-toned military buttons in two rows, structured stand collar, military shoulders, paired with light blue wide-leg raw-hem denim jeans, white sneakers, carrying a Muskmelon (warm soft orange) canvas tote bag on one shoulder. No overlay, no text, no logo, no signage. [STYLE] UGC candid selfie aesthetic, shot on iPhone 16 Pro, computational photography look, natural HDR, slight lens flare, soft highlight rolloff, Portrait mode bokeh, true-to-life color science, subtle noise grain at ISO 800, Kodak Portra 400 color palette overlay, muted cool tones. [CAMERA SETTINGS] 24mm wide-angle front camera, f/1.9, above eye-level selfie angle, upper body and face in frame, one arm extended holding phone (implied), background falling into natural Portrait mode bokeh. [LIGHTING] Overcast cloudy day diffused light, 6000-6500K cool neutral, low contrast, flat even illumination, no harsh shadows on face, soft catchlight in eyes. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, natural skin texture, double down braid hairstyle clearly visible, Napoleon jacket military button rows visible on chest, stand collar detail, muskmelon tote bag color accurate as warm accent against cool outfit, denim texture visible. [SCENE & ACTION] Standing in a quiet alley with indie storefronts blurred behind — weathered brick facade, potted plants, glass doors, but absolutely NO readable text or store signs in frame. POV selfie angle, one hand holding phone up, the other casually holding the tote bag strap on her shoulder, slight head tilt with a relaxed closed-lip half-smile, natural candid energy as if snapping a quick outfit check before meeting friends.",
    refs_paths=[f"{BASE}/generated/compositions/comp_look2_weekend.png"],
    save_path=f"{BASE}/generated/slide_08.png"
)

# SLIDE 09 — Date + sponsored crossbag, rear 3/4
generate(
    prompt="[INDICATIONS] A Korean fashion model influencer wearing a light grey NAPOLEON MILITARY JACKET with prominent gold double-breasted buttons in two parallel rows, structured stand collar rising to jawline, military-style epaulettes on shoulders, decorative braiding trim along front placket. Over a baby pink silk camisole, an ivory champagne satin midi skirt, nude strappy heels. She wears a compact matte black nylon mini crossbody sling bag DIAGONALLY ACROSS HER TORSO — the adjustable wide strap cuts from left shoulder across her back to right hip, with the small rectangular bag resting flat against her right hip at waist level. No overlay, no text, no logo, no signage. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft diffused atmosphere, subtle film grain at ISO 400, clean elegant mood. [CAMERA SETTINGS] 50mm f/1.4, rear three-quarter view from behind-right, full body in frame, shallow depth of field with background building facades falling into creamy bokeh, shot at eye level. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, cool neutral tones, no harsh shadows, even illumination with subtle directional light from camera-left, satin skirt catching soft diffused highlights. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, long half-up-down wavy hair with natural movement. Crossbody sling bag strap clearly visible running DIAGONALLY from left shoulder across the back to right hip — the bag is a small compact rectangle with visible front zipper and minimal black hardware. Gold Napoleon jacket buttons visible from rear angle catching ambient light. Satin skirt swaying mid-stride, baby pink camisole at neckline. Cool urban greys. [SCENE & ACTION] Walking along a quiet upscale Seoul street on an overcast day — clean modern building facades with warm interior lights glowing through large glass windows, elegant but NO readable text, NO store signs, NO Korean or Japanese characters visible anywhere. Mid-stride with satin skirt swaying, right hand touching the crossbody bag at her hip, head turned slightly right giving a three-quarter profile, the military Napoleon jacket with gold buttons and stand collar contrasting with the flowing feminine skirt.",
    refs_paths=[
        f"{BASE}/generated/compositions/comp_look3_date.png",
        f"{PRODUCTS}/genarchive_crossbag_fit.png",
        f"{PRODUCTS}/genarchive_crossbag_4-view.png"
    ],
    save_path=f"{BASE}/generated/slide_09.png"
)

print("\n\nALL DONE!")
