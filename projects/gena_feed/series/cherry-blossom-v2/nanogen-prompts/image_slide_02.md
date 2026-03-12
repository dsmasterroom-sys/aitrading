# slide-02 — 문제 제기: 수변 난간에 기대서 (Look B - 실패 코디)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a minimal outfit: thin cream knit sweater, light beige thin cardigan. Intentionally sparse — only two lightweight items on surface. No heavy outerwear.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Minimal. The sparseness tells the story — this is not enough clothing.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus.
[LIGHTING] Soft diffused top light. Cool-shifted white balance. Slightly clinical feel.
[KEY TECHNICAL CHARACTERISTICS] Thin, lightweight fabric textures emphasized. The knit sweater looks insufficient. Cool cream tones. Intentional visual emptiness communicating "not enough layers."
[SCENE & ACTION] A simple flat-lay on cool grey linen. The thin cream knit sweater at center, looking wispy and delicate. The light beige cardigan beside it, thin and unstructured. The arrangement is deliberately sparse — large negative space around the two items emphasizes how little protection they offer. No accessories, no heavy items. A single fallen cherry blossom petal at the corner, almost mocking.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** []

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_03_basic_straight.png, Phase 1 flat-lay result]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — thin cream knit sweater, light beige thin cardigan only. Clearly underdressed for cold wind. Hair: basic straight. Side profile, leaning against riverside metal railing, arms crossed tightly, shoulders hunched up near ears.
[STYLE] Cinematic cool-toned documentary photography. Fuji Pro 400H film emulation. Blue-green color shift. Melancholic, slightly desaturated. Street documentary feel, not fashion.
[CAMERA SETTINGS] Fuji Pro 400H, 50mm lens, f/2.8, 1/100s. Side profile medium shot. Cool white balance shifted 1000K cooler than neutral.
[LIGHTING] Late afternoon fading light with cool shift. Bluish ambient fill dominating. Side light from camera-right illuminating her profile. Cool shadows on the far side. Minimal warm tones — the golden hour is gone.
[KEY TECHNICAL CHARACTERISTICS] Cool blue-green color grading. Desaturated. Film grain visible. Goosebumps implied on bare forearms below thin cardigan sleeves. Wind lifting hair slightly. Dominant tones: blue-grey, cold green, muted pink from distant blossoms across the river. Metal railing texture adding cold industrial feel.
[SCENE & ACTION] @model leans against a metal railing along the Han River cherry blossom walkway. She's shot in side profile from camera-left. Her arms are crossed tightly over her thin cream knit sweater, elbows tucked in, shoulders hunched up near her ears — unmistakably cold. The thin beige cardigan flutters uselessly in the river breeze. Her basic straight hair blows across her face. She stares out over the grey water with an expression of mild regret. Behind her, cherry blossom trees line the walkway in soft pink, but the cool blue-green grading makes even the blossoms look chilly. A few other walkers in the far background are bundled in proper coats. She is the only one underdressed.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, generic smile, AI-generated artifact
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result]
