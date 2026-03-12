# slide-04 — 실패 공식: 벚꽃 골목 역광 실루엣 (Look C - 실패 코디)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a delicate outfit: white sheer blouse, beige pleated midi skirt. Feminine, pretty, but clearly inadequate for cold weather.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Delicate, airy styling on warm cream linen.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus.
[LIGHTING] Soft diffused top light. Warm neutral. Light passing through sheer blouse fabric.
[KEY TECHNICAL CHARACTERISTICS] Sheer fabric texture of blouse clearly visible — you can see the linen surface through it. Pleated skirt folds crisp and regular. Both items look thin, lightweight, decorative rather than protective.
[SCENE & ACTION] A flat-lay on warm cream linen. The white sheer blouse draped naturally at center, its transparency clearly visible against the surface. The beige pleated midi skirt fanned out below, each pleat sharp and defined. Beautiful arrangement — like a magazine styling. But visually communicating fragility. No outerwear, no layers. A few scattered cherry blossom petals as props.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered, artificial glamour
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** []

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_02_medium_straight.png, Phase 1 flat-lay result]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — thin white sheer blouse, beige pleated midi skirt. Beautiful but inadequate clothing. Hair: medium straight. Full body silhouette, walking away through a narrow cherry blossom alley, extreme backlight creating dramatic silhouette.
[STYLE] Cinematic silhouette photography. Golden hour dramatic. Kodak Portra 400. High-contrast backlit editorial. The beauty of the image contrasts with the foolishness of the outfit choice.
[CAMERA SETTINGS] Kodak Portra 400, 85mm lens, f/2.0, 1/200s. Full body from behind. Extreme backlight creating near-silhouette. Compressed perspective from telephoto.
[LIGHTING] Golden hour, 3500K extreme. Sun directly at end of narrow alley, creating god rays between buildings. Strong golden rim light outlining the model's silhouette and making the sheer blouse fabric glow translucent. Long dramatic shadows stretching toward camera on the alley floor.
[KEY TECHNICAL CHARACTERISTICS] Near-silhouette exposure — model is dark shape with glowing golden edges. Sheer blouse fabric glowing translucent where backlight passes through, revealing her silhouette. Pleated skirt catching wind at the hem. Heavy film grain. Golden lens flare. Dominant tones: deep gold, amber, dark silhouette, warm shadows. Beautiful but visually communicating vulnerability.
[SCENE & ACTION] @model walks away from camera through a narrow residential alley in Seoul. Cherry blossom branches hang over the alley walls on both sides, creating a natural ceiling. The setting sun at the alley's end turns everything to gold. Her thin white sheer blouse glows translucent in the extreme backlight — beautiful but you can see she has nothing underneath for warmth. Her pleated skirt catches a breeze, hem lifting slightly. Her medium straight hair sways with each step. Long dramatic shadows stretch toward the camera. She looks gorgeous — and completely unprepared for the temperature drop that's coming in 30 minutes when the sun disappears. The image is intentionally beautiful to make the point: pretty outfit ≠ smart outfit.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered, artificial glamour, stiff pose, AI-generated artifact, synthetic appearance
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result]
