# slide-07 — Look 3: Minimal Casual (Half Body)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a complete outfit: deep olive medium-gauge crewneck knit sweater, light gray wide slacks, white canvas sneakers, a gray light cardigan (folded/draped to suggest "over shoulders"), and a matte black nylon crossbody bag in shoulder-carry configuration.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Calm, minimal styling on a warm off-white linen surface. Earthy neutral palette.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus across all items.
[LIGHTING] Golden hour, 3500-4500K color temperature. Soft warm directional light from upper-right. Gentle shadows beneath each garment. Golden warmth on the olive knit and gray fabrics.
[KEY TECHNICAL CHARACTERISTICS] Visible medium-gauge knit texture on the olive sweater. Soft drape of the gray cardigan. Light gray fabric of the wide slacks. Clean white canvas texture on sneakers. Natural, calming color palette: deep olive, light gray, white, black accent.
[SCENE & ACTION] An overhead flat-lay on a warm off-white linen surface. The deep olive crewneck knit sits at center-top, its medium-gauge knit texture visible. The gray light cardigan is loosely folded at upper-right, suggesting it would be draped over shoulders. Light gray wide slacks extend below. White canvas sneakers placed at bottom-left, clean and minimal. The matte black nylon crossbag at right, strap extended in shoulder-carry configuration. A small white ceramic coffee cup as styling prop at the corner. Warm, inviting, weekend-morning energy.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look
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
[INDICATIONS] @model wearing @outfit — deep olive medium-gauge crewneck knit sweater, light gray wide slacks, white canvas sneakers. A gray light cardigan draped casually over shoulders. @object (gen archive matte black nylon slant crossbag, 196g) worn as shoulder bag. Hair: basic straight. Half-body shot, seated at cafe terrace, holding coffee.
[STYLE] UGC candid Korean fashion influencer photography. Kodak Portra 400 film emulation. Warm, approachable, weekend-cafe aesthetic. Natural and unposed. Soft Korean lifestyle mood.
[CAMERA SETTINGS] Kodak Portra 400, 50mm lens, f/1.8, half-body framing from across the cafe table. Focus on model's face and torso, background cafe elements in soft bokeh.
[LIGHTING] Golden hour, 3500-4500K color temperature. Warm natural light streaming from camera-left (cafe window or open terrace). Golden reflections in the coffee cup surface. Soft golden highlights on hair and knitwear. Gentle warm fill creating a cozy, inviting atmosphere.
[KEY TECHNICAL CHARACTERISTICS] Visible knit texture on the deep olive sweater catching warm light. Gray cardigan draped casually creating relaxed silhouette. Film grain. Muted earthy palette: olive, gray, white, black bag accent, warm gold highlights. Natural skin, relaxed expression. Coffee cup with golden light reflection as secondary focal point.
[SCENE & ACTION] @model sits at a cafe terrace table in Seoul, half-body visible. She holds a ceramic coffee cup with both hands at chest level, steam barely visible. She looks slightly off-camera to the left with a soft, contented half-smile. Her basic straight hair falls naturally. The deep olive knit sweater is the color anchor, the gray cardigan draped over her shoulders adds a layering detail. The gen archive crossbag hangs on her left shoulder, strap visible across the sweater. Behind her, the cafe terrace opens to a street with cherry blossom trees in soft pink bokeh. A few petals have landed on the table. The warm golden light wraps everything in a weekend-afternoon glow.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result, shared/products/genarchive_crossbag/genarchive_crossbag_fit.png, shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png]
