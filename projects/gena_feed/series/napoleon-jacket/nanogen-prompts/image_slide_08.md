# slide-08 — 룩2 주말 (POV 셀피)

## Phase 1: Flat-lay
**Prompt:**
`[INDICATIONS] A black Napoleon jacket with silver-toned military buttons and structured shoulders, paired with light blue wide-leg raw-hem denim jeans, white leather low-top sneakers, and a Muskmelon (soft warm orange) canvas tote bag, all arranged on a light grey concrete surface. [STYLE] UGC-inspired flat-lay, slightly imperfect casual arrangement, Kodak Portra 400 film emulation, muted tones with the orange tote as sole color pop, desaturated -10%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across frame. [LIGHTING] Overcast diffused daylight, 6000K cool neutral, low contrast, even soft illumination. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic denim texture, visible raw hem fraying, sneaker sole texture, tote bag canvas weave, military button detail on black jacket. [SCENE & ACTION] Weekend outfit casually arranged — jacket slightly angled as if just tossed down, jeans folded once at the waist, sneakers placed at a playful angle, the muskmelon tote bag partially overlapping the jeans suggesting effortless pairing.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** 없음

## Phase 2: Composition
**Prompt:**
`Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [shared/persona/gena_ref_08_double_down_braid.png, Phase 1 결과]

## Phase 3: Final
**Prompt:**
`[INDICATIONS] A Korean fashion model influencer wearing a black Napoleon jacket with military buttons, light blue wide-leg denim jeans, white sneakers, carrying a Muskmelon (warm soft orange) tote bag on one shoulder, captured in a POV selfie angle on a Seoul street. [STYLE] UGC candid selfie aesthetic, shot on iPhone 16 Pro, computational photography look, natural HDR, slight lens flare, soft highlight rolloff, Portrait mode bokeh, true-to-life color science, subtle noise grain at ISO 800, Kodak Portra 400 color palette overlay, muted cool tones. [CAMERA SETTINGS] 24mm wide-angle front camera, f/1.9, above eye-level selfie angle, upper body and face in frame, one arm extended holding phone (implied), background falling into natural Portrait mode bokeh. [LIGHTING] Overcast cloudy day diffused light, 6000-6500K cool neutral, low contrast, flat even illumination, no harsh shadows on face, soft catchlight in eyes. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic, natural skin texture with minimal retouching look, double down braid hairstyle clearly visible, muskmelon tote bag color accurate as warm accent against cool-toned outfit, denim texture visible at waist area. [SCENE & ACTION] Standing in a Seongsu-dong alley with indie cafe storefronts softly blurred behind her, one hand holding phone up for selfie (POV — we see from phone's perspective), the other hand casually holding the tote bag strap on her shoulder, slight head tilt with a relaxed closed-lip half-smile, natural candid energy as if snapping a quick outfit check before meeting friends.`

**Negative:** `oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout`
**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [Phase 2 결과]
