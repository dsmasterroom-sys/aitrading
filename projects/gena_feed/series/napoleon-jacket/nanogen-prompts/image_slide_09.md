# slide-09 — 룩3 데이트 + 협찬 (뒷모습/3/4 앵글, 골든아워)

## Phase 1: Flat-lay
**Prompt:**
`[INDICATIONS] A light grey Napoleon jacket with gold double-breasted buttons and structured military shoulders, paired with an ivory champagne satin midi skirt with subtle sheen, nude leather strappy heeled sandals, and a baby pink silk camisole as the inner layer, all arranged on a warm beige linen surface. [STYLE] Editorial feminine flat-lay, elegant arrangement, Kodak Portra 400 film emulation, warm muted tones, soft pink and champagne palette, desaturated -5%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across entire frame. [LIGHTING] Warm diffused light from upper right, 4500K slightly warm, minimal shadows, satin skirt catching soft highlights. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic satin sheen on skirt, silk camisole delicate texture, gold button detail on grey jacket, nude heel strap detail, overall feminine-military contrast visible in the arrangement. [SCENE & ACTION] Date night outfit elegantly arranged — the grey jacket placed open to reveal the baby pink camisole layered beneath, satin skirt fanned slightly to show its drape and sheen, heels placed at the bottom with straps artfully visible, creating a romantic yet structured outfit narrative.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** 없음

## Phase 2: Composition
**Prompt:**
`Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [shared/persona/gena_ref_07_long_halfupdown_wave.png, Phase 1 결과]

## Phase 3: Final
**Prompt:**
`[INDICATIONS] A Korean fashion model influencer wearing a light grey Napoleon jacket with gold double-breasted buttons over a baby pink silk camisole, an ivory champagne satin midi skirt, nude strappy heels, and a matte black minimalist crossbody bag worn cross-body, captured from a rear three-quarter angle walking away. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft diffused atmosphere, subtle film grain at ISO 400, clean elegant mood. [CAMERA SETTINGS] 50mm f/1.4, rear three-quarter view from behind-right, full body in frame, shallow depth of field with background restaurant facades falling into creamy bokeh, shot at eye level. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, cool neutral tones, no harsh shadows, even illumination with subtle directional light from camera-left, satin skirt catching soft diffused highlights, gentle cool reflection from surrounding surfaces. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, long half-up-down wavy hair with natural movement, crossbody bag strap visible across her back with bag resting at hip level — bag details clearly visible (matte black nylon, minimal hardware), gold jacket buttons catching soft diffused light, satin skirt movement captured mid-stride, baby pink camisole peeking at neckline, cool urban greys and muted tones in environment. [SCENE & ACTION] Walking along a quiet Hannam-dong street on an overcast day, passing a restaurant entrance with soft interior glow visible through windows, mid-stride with satin skirt swaying, one hand lightly touching the crossbody bag strap, head turned slightly to the right giving a three-quarter profile glimpse, the cool diffused light creating an elegant cinematic atmosphere, the military-structured jacket contrasting beautifully with the flowing feminine skirt.`

**Negative:** `oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout`
**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [Phase 2 결과, shared/products/genarchive_crossbag/genarchive_crossbag_fit.png, shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png]
