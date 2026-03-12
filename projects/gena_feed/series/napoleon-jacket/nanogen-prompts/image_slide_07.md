# slide-07 — 룩1 출근 (로우앵글 워킹)

## Phase 1: Flat-lay
**Prompt:**
`[INDICATIONS] A charcoal Napoleon jacket with gold double-breasted buttons and structured shoulders, paired with charcoal-grey wide-leg trousers, black leather penny loafers, and a Burnished Lilac (smoky lavender) silk scarf loosely draped, all arranged on a cream linen surface. [STYLE] Editorial flat-lay, clean minimalist arrangement, Kodak Portra 400 film emulation, muted neutral tones, cool undertone, desaturated -10%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across entire frame. [LIGHTING] Soft diffused natural window light from upper left, 5500K neutral daylight, minimal shadows, even illumination. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic fabric textures, visible weave on trousers, silk scarf translucency, gold button detail, lavender scarf as the single color accent against monochrome palette. [SCENE & ACTION] Office-ready outfit laid flat with intentional spacing, the lilac scarf casually draped across the jacket collar area suggesting how it would be worn, loafers placed at bottom with toes pointing outward, creating a complete outfit story from top to bottom.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** 없음

## Phase 2: Composition
**Prompt:**
`Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [shared/persona/gena_ref_03_basic_straight.png, Phase 1 결과]

## Phase 3: Final
**Prompt:**
`[INDICATIONS] A Korean fashion model influencer wearing a charcoal Napoleon jacket with gold buttons, charcoal wide-leg trousers, black penny loafers, and a Burnished Lilac silk scarf loosely tied at the neck, walking confidently through a modern office building lobby. [STYLE] Street documentary meets editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, natural unposed energy, slight motion captured. [CAMERA SETTINGS] 35mm f/2.0, low angle shot from near ground level looking up, full body in frame, converging vertical lines of the building adding dynamism, 1/250s shutter freezing mid-stride. [LIGHTING] Overcast daylight filtering through large glass lobby windows, 5500-6500K cool neutral, low contrast, soft even illumination with no harsh shadows, slight cool reflection from marble or concrete flooring. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, visible gold button details on jacket, lilac scarf color accurate as the single warm accent, shoe-level perspective creating empowering upward gaze, natural straight hair with subtle movement. [SCENE & ACTION] Descending the last two steps of a modern minimalist office building staircase (polished concrete, glass railings, clean lines), mid-stride with purpose, one hand adjusting the lilac scarf at her neck, the other arm swinging naturally, looking slightly downward at her path with a focused expression, the geometric architecture framing her figure from this low vantage point.`

**Negative:** `oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout`
**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [Phase 2 결과]
