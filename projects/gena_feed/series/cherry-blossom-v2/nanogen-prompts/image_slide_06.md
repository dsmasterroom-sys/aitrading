# slide-06 — 아이템 조합: 돌계단에 앉기 (Look D)

## Phase 1 (flat-lay)

(Look D와 동일 — slide-05에서 생성된 flat-lay 재사용)

**referenceImages:** [series/cherry-blossom-v2/generated/outfits/look_D.png]

---

## Phase 2 (composition)

**Prompt:** "Change only the main clothing garments to strictly match the design, texture, and details of the provided clothing reference image. Replicate the attached outfit exactly. Crucially, preserve all original accessories intact. Keep the original model's face, pose, hair, background, and lighting exactly the same. Seamless integration, photorealistic, 8k resolution."
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [shared/persona/gena_ref_01_long_twinhalfup_wave.png, Phase 1 flat-lay result (look_D)]

---

## Phase 3 (final)

**Prompt:**
[INDICATIONS] @model wearing @outfit — mustard/camel oversized trench coat, ivory turtleneck, charcoal wide-leg pants, black ankle boots. Hair: long twin half-up wavy. Full body shot, sitting on old stone steps beside a cherry blossom tree, one knee drawn up, arm resting on knee.
[STYLE] Editorial lookbook photography. Kodak Portra 400 film emulation. Clean, composed framing. Polished but natural. Magazine fashion spread shot on location.
[CAMERA SETTINGS] Kodak Portra 400, 35mm lens, f/2.8, 1/125s. Full body framing, eye-level with seated model. Cherry blossom canopy overhead fills upper frame.
[LIGHTING] Golden hour, 3500-4500K. Side light from camera-right, creating gentle shadows on the left side of face and trench folds. Warm golden patches from light filtering through cherry blossom canopy above. Soft dappled light pattern on the stone steps.
[KEY TECHNICAL CHARACTERISTICS] Full outfit visible — trench structure, turtleneck collar, charcoal pants, ankle boots all identifiable. Stone step texture adds character. Dappled cherry blossom shadows on the steps. Film grain light. Palette: mustard, ivory, charcoal, warm grey stone, soft pink overhead. Natural editorial energy.
[SCENE & ACTION] @model sits on weathered stone steps next to a large cherry blossom tree in a quiet Seoul neighborhood. She has one knee drawn up, her right arm resting casually on it. Her left leg extends down two steps, showing the charcoal wide-leg pants and black ankle boots. The mustard trench coat drapes around her on the steps, the fabric pooling naturally. She looks directly at camera with a subtle, self-assured expression. Her long twin half-up wavy hair falls over both shoulders. Cherry blossom branches from the adjacent tree hang into the upper frame, creating a natural canopy. Petals dot the stone steps around her. Golden side-light from the right creates gentle shadows in the trench coat folds. The mood is editorial but effortless — like a magazine stylist just said "sit there" and she looked perfect.

**Negative prompt:** oversaturated, western aesthetic, heavy filter, text overlay, cluttered background, artificial glamour, unnatural skin, plastic look, stiff pose, mannequin-like, AI-generated artifact, synthetic appearance
**Config:** { "aspectRatio": "4:5", "resolution": "1080x1350" }
**referenceImages:** [Phase 2 composition result]
