# slide-05 — Look 1: Sheer Layering (Full Body)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a complete outfit: charcoal ribbed sleeveless tank top as inner layer, deep green sheer mesh long-sleeve top as outer layer (placed overlapping the tank), charcoal high-waist wide slacks, black minimal loafers, and a matte black nylon crossbody bag in shoulder-carry configuration.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Minimalist styling on a neutral warm-grey fabric surface. Items neatly arranged with intentional spacing.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus across all items.
[LIGHTING] Golden hour, 3500-4500K color temperature. Soft warm directional light from upper-left creating gentle shadows beneath each garment. Long subtle shadows. Golden tones on fabric surfaces.
[KEY TECHNICAL CHARACTERISTICS] Sharp detail on rib-knit texture of tank top. Sheer mesh weave visible on the green top layer. Wide slacks fabric drape visible. Clean edges, no wrinkles. Muted color palette: charcoal, deep green, black.
[SCENE & ACTION] A carefully styled overhead flat-lay on a warm linen surface. The charcoal ribbed tank top sits at center-top, the deep green sheer mesh long-sleeve draped partially over it to show the layering concept. The charcoal wide slacks are folded neatly below. Black loafers placed at bottom-right. The matte black nylon crossbody bag positioned at top-right. Small sprig of cherry blossom as styling prop at corner.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** []

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_07_long_halfupdown_wave.png, Phase 1 flat-lay result]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — charcoal ribbed sleeveless tank layered under a deep green sheer mesh long-sleeve top (loose fit), charcoal high-waist wide slacks, black loafers. @object (gen archive matte black nylon slant crossbag, 196g) worn as shoulder bag. Hair: long half-up-down wavy. Full body shot, walking pose.
[STYLE] UGC candid Korean fashion influencer photography. Kodak Portra 400 film emulation. Muted warm tones, natural and unposed feel. Not over-polished editorial — spontaneous energy. Handheld camera feel.
[CAMERA SETTINGS] Kodak Portra 400, 35mm lens, f/2.0, full body framing with slight low angle. Focus on model, background softly out of focus.
[LIGHTING] Golden hour, 3500-4500K color temperature. Strong backlight creating golden rim light around model's silhouette and hair. Warm light passing through the sheer mesh top, revealing the layering underneath. Long shadow cast forward. Cool fill in shadow areas.
[KEY TECHNICAL CHARACTERISTICS] Backlit sheer mesh fabric glowing with transmitted golden light — key visual hook. Film grain texture. Muted palette: charcoal, deep green, black, warm gold highlights. Natural skin texture. Crossbag strap and bag body clearly visible on shoulder. Hair catching golden rim light.
[SCENE & ACTION] @model walks casually under a cherry blossom tree-lined street in Seoul. Mid-stride, one foot slightly ahead, arms relaxed at sides. She looks slightly off-camera with a soft, natural expression. The golden hour sun behind her creates a luminous rim around her silhouette. The sheer green mesh top catches the backlight beautifully, the charcoal tank visible underneath. The gen archive crossbag sits naturally on her left shoulder, strap crossing her torso. Cherry blossom petals drift in the warm air around her. The street stretches behind her, soft pink bokeh from distant cherry trees.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result, shared/products/genarchive_crossbag/genarchive_crossbag_fit.png, shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png]
