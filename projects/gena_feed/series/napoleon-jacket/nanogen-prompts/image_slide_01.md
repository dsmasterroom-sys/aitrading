# slide-01 — 표지 (사이드 프로필, 골든아워)

## Phase 1: Flat-lay
**Prompt:**
`[INDICATIONS] A dark charcoal-black Napoleon jacket with prominent gold double-breasted buttons, two-row button arrangement, stand collar, military-inspired structured shoulders, paired with black slim-fit trousers and black leather ankle boots, neatly arranged on a light beige linen surface. [STYLE] Editorial flat-lay, clean minimalist arrangement, Kodak Portra 400 film emulation, muted warm tones, desaturated -10%. [CAMERA SETTINGS] Top-down aerial view, 35mm equivalent, f/8.0, sharp focus across entire frame. [LIGHTING] Soft diffused natural window light from upper left, 5500K neutral daylight, minimal shadows, even illumination. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic fabric textures, visible gold button engravings, structured jacket silhouette preserved in lay-flat position. [SCENE & ACTION] Garments laid flat on a natural linen backdrop, each piece spaced with intentional breathing room, gold buttons catching subtle light reflection, military details clearly visible.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** 없음

## Phase 2: Composition
**Prompt:**
`Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution.`

**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [shared/persona/gena_ref_02_medium_straight.png, Phase 1 결과]

## Phase 3: Final
**Prompt:**
`[INDICATIONS] A Korean fashion model influencer wearing a dark charcoal-black Napoleon jacket with gold double-breasted buttons, black slim trousers, and black ankle boots, captured in a confident side profile walking pose. [STYLE] Cinematic editorial, Kodak Portra 400 film emulation, cool muted tones, desaturated -15%, soft highlight rolloff, subtle film grain at ISO 400, clean urban atmosphere. [CAMERA SETTINGS] 85mm f/1.8, shallow depth of field, side profile framing, model occupying left 40% of frame, background softly blurred, shot at slight low angle. [LIGHTING] Overcast soft diffused daylight 5500-6500K, low contrast, no harsh shadows, cool neutral tones, even illumination wrapping the figure, subtle directional light from camera-right revealing gold button details and jacket structure. [KEY TECHNICAL CHARACTERISTICS] 8k resolution, photorealistic skin texture, visible gold button reflections catching soft diffused light, structured jacket shoulder line sharp against blurred background, natural hair movement from gentle breeze, cool-toned urban greys and soft blues in environment. [SCENE & ACTION] Walking along a quiet Seoul side street (Seongsu-dong aesthetic — exposed brick, minimal signage), mid-stride with one foot forward, chin slightly lifted, gaze directed ahead past camera, overcast sky creating even cool light across the jacket's military details, the street stretching into soft bokeh behind her.`

**Negative:** `oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, stock photo feel, generic smile, bad anatomy, extra fingers, deformed hands, blurry face, watermark, signature, logo, frame border, collage layout`
**Config:** aspectRatio: "3:4", guidanceScale: 3.5, numInferenceSteps: 28
**referenceImages:** [Phase 2 결과]
