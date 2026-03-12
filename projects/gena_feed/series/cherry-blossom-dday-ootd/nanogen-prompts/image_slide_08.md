# slide-08 — Look 4: Street Casual (Full Body)

## Phase 1 (flat-lay)

**Prompt:**
[INDICATIONS] Flat-lay arrangement of a complete outfit: deep forest green crop hoodie with visible drawstring, khaki wide cargo pants with multiple pockets, black chunky sneakers, a matte black nylon crossbody bag in cross-body configuration, and a small silver ring as accessory.
[STYLE] Clean editorial flat-lay photography. Overhead bird's-eye view. Casual street-style energy on a neutral concrete-grey surface. Urban, youthful.
[CAMERA SETTINGS] Kodak Ektar 100, 50mm lens, f/5.6, even focus across all items.
[LIGHTING] Golden hour, 3500-4500K color temperature. Warm directional light from upper-left. Golden highlights on the hoodie drawstring hardware and silver ring. Gentle shadows beneath garments.
[KEY TECHNICAL CHARACTERISTICS] Hoodie drawstring detail visible. Cargo pants multi-pocket construction clear — flap pockets, side pockets. Chunky sneaker sole profile visible. Crop length of hoodie apparent from arrangement. Color palette: deep forest green, khaki, black, silver accent.
[SCENE & ACTION] An overhead flat-lay on a cool concrete-grey surface. The deep forest green crop hoodie at center-top, drawstrings pulled out to show detail, cropped length evident. Khaki wide cargo pants below, one leg slightly folded to show a side cargo pocket with flap. Black chunky sneakers at bottom, showing their thick sole profile. The matte black nylon crossbag positioned at right, strap extended in cross-body configuration. A single silver ring placed near the hoodie cuff. A small green leaf as styling prop. Youthful, streetwear energy.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** []

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_08_double_down_braid.png, Phase 1 flat-lay result]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — deep forest green crop hoodie with drawstring, khaki wide cargo pants with multiple pockets, black chunky sneakers. Silver ring on finger. @object (gen archive matte black nylon slant crossbag, 196g) worn cross-body, bag sitting at right hip. Hair: double down braids. Full body shot, seated on park bench, relaxed pose.
[STYLE] UGC candid Korean fashion influencer photography. Kodak Portra 400 film emulation. Relaxed, youthful street-casual energy. Candid park setting, not posed. Soft natural tones.
[CAMERA SETTINGS] Kodak Portra 400, 35mm lens, f/2.0, full body framing. Slightly low angle, shooting from path level toward the bench. Focus on model, park background in gentle bokeh.
[LIGHTING] Golden hour, 3500-4500K color temperature. Low-angle side light filtering through park trees, creating dappled golden beams across the scene. Warm golden patches on the hoodie and cargo pants. Rim light on the double braids. Soft green-gold tones from light through leaves.
[KEY TECHNICAL CHARACTERISTICS] Crop hoodie showing a sliver of midriff. Cargo pocket flaps visible on the wide khaki pants. Chunky sneaker soles prominent from the seated angle. Cross-body bag strap visible diagonally across torso, bag at hip. Double down braids catching golden rim light. Silver ring glinting. Film grain. Palette: forest green, khaki, black, gold highlights.
[SCENE & ACTION] @model sits on a wooden park bench in a Seoul park, legs extended and crossed casually at the ankles. She leans back slightly, one arm resting on the bench back, the other resting on her thigh near a cargo pocket. She looks off to the right with a relaxed, easy smile. Her double down braids fall over each shoulder. The deep forest green crop hoodie shows a small sliver of waist above the khaki cargo pants. The gen archive crossbag crosses her torso diagonally, the compact bag body at her right hip. Behind her, park trees filter golden light into warm beams and dappled shadows. A few cherry blossom petals dot the ground near her chunky black sneakers. The mood is unhurried, confident, Sunday-afternoon cool.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result, shared/products/genarchive_crossbag/genarchive_crossbag_fit.png, shared/products/genarchive_crossbag/genarchive_crossbag_4-view.png]
