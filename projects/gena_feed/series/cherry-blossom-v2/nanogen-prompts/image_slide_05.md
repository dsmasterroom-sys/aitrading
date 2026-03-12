# slide-05 — 3단 레이어링: 카페 테라스 (Look D)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a layered outfit: mustard/camel oversized trench coat, ivory cable-knit turtleneck sweater, charcoal wide-leg pants, black ankle boots. Arranged to show the layering concept clearly.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Warm styling on natural linen surface. The arrangement emphasizes the layering depth.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus.
[LIGHTING] Soft warm directional light from upper-left. Gentle shadows. Golden warmth on the mustard trench fabric.
[KEY TECHNICAL CHARACTERISTICS] Layering concept visible — turtleneck partially tucked under trench to show how they combine. Cable-knit texture on turtleneck visible. Rich mustard/camel trench cotton. Charcoal twill weave on pants. Color palette: mustard, ivory, charcoal, black.
[SCENE & ACTION] An overhead flat-lay on warm natural linen. The mustard/camel oversized trench coat spread as the base, slightly angled. The ivory cable-knit turtleneck placed overlapping the trench neckline — showing the layering relationship. Charcoal wide-leg pants folded to the side with one leg extended. Black ankle boots at bottom corner. A takeaway coffee cup and a small cherry blossom branch as styling props. Warm, intentional, layered-look editorial energy.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered, artificial glamour
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** []

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_05_updo.png, Phase 1 flat-lay result]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — mustard/camel oversized trench coat (open, showing layers), ivory cable-knit turtleneck, charcoal wide-leg pants, black ankle boots. Hair: elegant updo revealing neckline. Half-body shot, seated at outdoor cafe terrace, holding coffee with both hands.
[STYLE] UGC candid Korean fashion influencer photography. Kodak Portra 400 film emulation. Warm, approachable, afternoon-cafe aesthetic. Natural and unposed. Weekend lifestyle mood.
[CAMERA SETTINGS] Kodak Portra 400, 50mm lens, f/1.8, half-body framing from across the cafe table. Focus on model's face and torso, background cafe elements in soft bokeh.
[LIGHTING] Warm afternoon natural light, 4000-4500K. Sunlight streaming from camera-left through the cafe terrace opening. Golden reflections in the coffee cup. Soft golden highlights on her updo hair and the ivory turtleneck collar. Gentle warm fill creating a cozy, inviting atmosphere. No harsh shadows.
[KEY TECHNICAL CHARACTERISTICS] Layering clearly visible — trench coat open wide, ivory turtleneck high collar prominent, sleeves of turtleneck visible under trench cuffs. Cable-knit texture catching warm light. Coffee cup steam barely visible. Film grain moderate. Palette: mustard, ivory, charcoal, warm gold highlights, pink cherry blossom bokeh. Natural skin texture, relaxed expression.
[SCENE & ACTION] @model sits at a wooden cafe terrace table in a Seoul cherry blossom neighborhood. Half-body visible from the waist up. She holds a ceramic coffee cup with both hands at chest level, fingers wrapped around it for warmth. Her mustard trench coat is open wide, revealing the ivory cable-knit turtleneck underneath — the layering is the visual story. Her elegant updo exposes the high turtleneck collar, showing the outfit's intentional design. She looks slightly off-camera to the left with a knowing half-smile — the expression of someone who dressed right and is comfortable while others around her shiver. Behind her, the cafe terrace opens to a street where cherry blossom trees paint soft pink bokeh. A few fallen petals sit on the wooden table near her cup. The warm light wraps everything in a weekend-afternoon glow.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, AI-generated artifact, synthetic appearance
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result]
