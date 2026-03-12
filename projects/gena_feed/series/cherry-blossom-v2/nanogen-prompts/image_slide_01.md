# slide-01 — 훅: 벚꽃 터널 뒷모습 (Look A)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a complete outfit: oversized beige/camel trench coat, cream cable-knit turtleneck sweater, beige wide-leg pants, black leather loafers. Neatly arranged with natural folds on warm cream linen.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Minimal styling. Warm, inviting palette.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus across all items.
[LIGHTING] Soft diffused top light. Even warm illumination. Gentle shadows beneath each garment.
[KEY TECHNICAL CHARACTERISTICS] Sharp detail on cable-knit texture of turtleneck. Trench coat cotton twill weave visible. Wide-leg pants drape apparent. Color palette: camel, cream, beige, black accent.
[SCENE & ACTION] A carefully styled overhead flat-lay on warm cream linen. The oversized beige trench coat spread wide as the base layer, belt untied and draped to the side. Cream cable-knit turtleneck folded neatly on top of the trench, showing the ribbed collar. Beige wide-leg pants to the right, one leg slightly folded. Black leather loafers at bottom corner, polished. A single cherry blossom sprig as styling prop at upper-right corner.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, AI-generated artifact, synthetic appearance
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** []

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_06_long_wave.png, Phase 1 flat-lay result]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — oversized beige/camel trench coat, cream cable-knit turtleneck, beige wide-leg pants, black loafers. Hair: long wavy, wind-blown. Rear three-quarter view, walking away, one hand reaching up to hold hair against wind.
[STYLE] Cinematic editorial Korean fashion photography. Kodak Portra 400 film emulation. Warm sepia golden wash. Heavy film grain. Magazine cover energy.
[CAMERA SETTINGS] Kodak Portra 400, 35mm lens, f/2.0, 1/125s. Medium shot from behind, slight low angle. Shallow DOF blurring cherry blossom canopy.
[LIGHTING] Golden hour, 3500-4500K. Strong backlight streaming through cherry blossom tunnel overhead. Golden rim light outlining trench coat edges and wind-blown hair. Long warm shadows stretching forward on the path. Cool shadows in the tree-lined corridor.
[KEY TECHNICAL CHARACTERISTICS] Trench coat fabric caught mid-flutter in wind — belt and hem swinging. Film grain heavy. Warm amber-gold tint. Soft pink bokeh from cherry blossom canopy. Hair strands catching golden backlight individually. Natural motion blur on coat hem.
[SCENE & ACTION] @model walks through a cherry blossom tunnel in Seoul's Yeouido. She is captured mid-stride from behind in three-quarter view, her right hand reaching up to hold her wind-blown long wavy hair. The wind catches her oversized trench coat dramatically — the belt swings free, the hem flutters wide revealing the cream turtleneck underneath. Cherry blossom petals swirl around her ankles. She glances slightly over her right shoulder, just enough to catch a sliver of her profile. The golden hour sun at the tunnel's end backlights everything, turning the floating petals into glowing confetti. The path ahead stretches invitingly into warm golden haze.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, AI-generated artifact, synthetic appearance, generic smile
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result]
