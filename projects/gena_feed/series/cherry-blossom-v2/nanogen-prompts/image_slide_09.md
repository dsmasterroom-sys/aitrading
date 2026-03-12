# slide-09 — 요약: 야간 벚꽃길 롱샷 (Look A)

## Phase 1 (flat-lay)

(Look A 재사용 — slide-01에서 생성된 flat-lay)

**referenceImages:** [series/cherry-blossom-v2/generated/outfits/look_A.png]

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_07_long_halfupdown_wave.png, Phase 1 flat-lay result (look_A)]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — beige oversized trench coat with collar turned up, cream turtleneck visible at neck, wide-leg pants. Hair: long half-up-down wavy. Long shot, small figure in night cherry blossom scene, walking alone through pools of streetlamp light. Hands in trench pockets.
[STYLE] Cinematic night photography. Kodak Portra 800 pushed. Cool-warm mixed tones. Moody, atmospheric, contemplative. Wong Kar-wai-inspired urban night mood.
[CAMERA SETTINGS] Kodak Portra 800, 35mm lens, f/1.8, 1/60s. Long shot — figure occupies bottom third of frame. Night exposure with warm streetlamp pools against cool ambient sky. Slight motion blur acceptable for cinematic feel.
[LIGHTING] Night scene — warm tungsten streetlamp pools (3000K amber) against cool ambient night sky (7000K+ deep blue). Mixed warm-cool creating color contrast. Cherry blossom branches lit from below by streetlamps, glowing ethereal pink against the navy sky. Streetlamp creating a warm spotlight pool on the path where the model walks.
[KEY TECHNICAL CHARACTERISTICS] Night grain (ISO 800 pushed). Warm-cool contrast between amber streetlamp pools and deep blue night sky. Cherry blossoms glowing supernatural pink under artificial light — almost ghostly. Bokeh circles from distant lamps along the street. Trench coat collar silhouette distinctive. Dominant tones: deep navy sky, warm amber lamp pools, ghostly pink blossoms, cool grey path.
[SCENE & ACTION] A cherry blossom-lined residential street in Seoul at night. Long shot — @model is a relatively small figure walking alone through a pool of warm streetlamp light at the center of the frame. She wears her beige trench coat with the collar turned up, hands tucked in the pockets, walking with quiet purpose. Her half-up-down wavy hair catches the amber light. The cherry blossom trees on both sides of the street are lit from below by the streetlamps, their pink flowers glowing ethereal and almost supernatural against the deep navy night sky. The street stretches ahead and behind her, marked by a progression of warm lamp pools fading into darkness. She's the only person on the street. The mood is contemplative, cinematic — she dressed for the cold this time, and she's enjoying the night blossoms alone. Prepared, confident, self-sufficient.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, stiff pose, AI-generated artifact, synthetic appearance, daytime, sunny
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result]
