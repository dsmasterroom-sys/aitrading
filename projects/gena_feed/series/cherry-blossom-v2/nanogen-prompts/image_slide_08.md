# slide-08 — 협찬: 벤치에서 크로스백 (Look D + 제품)

## Phase 1 (flat-lay)

(Look D 재사용 — slide-05에서 생성된 flat-lay)

**referenceImages:** [series/cherry-blossom-v2/generated/outfits/look_D.png]

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_09_long_hippie.png, Phase 1 flat-lay result (look_D)]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — mustard/camel oversized trench coat, ivory turtleneck, charcoal wide-leg pants, black ankle boots. @object (gen archive matte black nylon slant crossbag) placed on bench beside her. Hair: long hippie style. Full body shot, sitting on a park bench, legs crossed, leaning back casually.
[STYLE] UGC candid Korean fashion influencer photography. Kodak Portra 400 film emulation. Warm, relaxed, weekend-park aesthetic. Spontaneous and natural. Handheld camera energy. The product appears organically, not staged.
[CAMERA SETTINGS] Kodak Portra 400, 35mm lens, f/2.0, 1/125s. Full body framing, slightly low angle shooting from the path in front of the bench. Focus on model, park background in warm bokeh.
[LIGHTING] Golden hour, 3500-4500K. Low-angle side light filtering through park trees from camera-left. Warm golden patches dappling the bench and model. Rim light on hippie-style hair. Soft green-gold tones from light through spring leaves.
[KEY TECHNICAL CHARACTERISTICS] The matte black nylon crossbag is visible on the bench next to her right hip — its compact form and matte texture contrast with the warm camel trench. Crossbag strap visible, partially draped. Film grain moderate. Palette: mustard trench, ivory turtleneck, charcoal pants, matte black bag, warm gold light, green park. Natural skin, relaxed expression.
[SCENE & ACTION] @model sits on a wooden park bench along a cherry blossom-lined path in Seoul. She leans back comfortably, legs crossed at the ankles, one arm stretched along the bench back. Her other hand rests near the gen archive matte black crossbag that sits on the bench beside her right hip — she just took it off and set it down, the strap still partially draped over the armrest. She looks off to the right with a relaxed, easy smile — mid-laugh, maybe someone walking a dog just made her smile. Her long hippie-style hair falls freely over her shoulders and the bench. The mustard trench coat spreads naturally on the bench around her. Behind her, cherry blossom trees filter golden light into warm beams and dappled shadows on the path. A few petals have landed on the bench slats near the bag. The mood is unhurried, natural, weekend-afternoon — the bag looks like it belongs there, not like it's being advertised.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, AI-generated artifact, synthetic appearance, product placement feel, advertisement
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result, shared/products/genarchive_crossbag/genarchive_crossbag_fit.png, shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png]
