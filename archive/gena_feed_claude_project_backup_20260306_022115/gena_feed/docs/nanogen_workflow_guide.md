# Nanogen Workflow Processing Guide

## Workflow: concept_sunnyday

### Overview
- **Purpose**: Generate 9 carousel slide images for @gena_feed Instagram
- **Method**: Sequential processing (one slide at a time)
- **Estimated Time**: 6-10 minutes total

## Workflow Structure

```
┌─────────────┐
│ Text Input  │  Creative Vision + Slide Prompt
│   (Node 7)  │
└──────┬──────┘
       │
       ├───────┐
       │       ├─────────────┐
       │       │  4× Image   │  References:
       │       │   Inputs    │  - Model (gena_hair)
       │       │  (Nodes    │  - Outfit grid
       │       │   3-6)      │  - Bag images
       │       └──────┬──────┘
       │              │
       ▼              ▼
┌────────────────────────┐
│   Prompt Agent         │  Enhances prompt using
│     (Node 1)           │  creative vision + refs
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Image Generator       │  Gemini 3 Pro Image
│     (Node 9)           │  Output: 16:9, 1K
└────────────────────────┘
```

## Processing Strategy: SEQUENTIAL

### Why Sequential?
✅ **Resource Management**: Local GPU focused on one generation
✅ **Quality Control**: Review each output before proceeding
✅ **Error Handling**: Retry individual slides without re-running all
✅ **Stability**: No memory overflow from parallel processing

❌ **Why NOT Batch?**
- Local resources may be limited
- Each slide needs unique inputs
- Harder to debug if batch fails
- No time savings (GPU processes one at a time anyway)

## Step-by-Step Execution

### Preparation
1. Open Nanogen: `http://localhost:8000`
2. Load workflow: "concept_sunnyday"
3. Have reference images ready in `/assets/`
4. Have `weekly/image-prompts.json` open

### For Each Slide (1-9)

#### Slide Processing Template:

**Slide ID**: `slide01-bg`
**Prompt**: From `image-prompts.json` → `slides[0].prompt`
**References**: `slides[0].referenceImages`

**Steps**:
1. **Update Node 7 (Text Input)**:
   ```
   Creative Vision: [Your base creative direction]
   
   Slide: slide01-bg
   Role: 훅 배경 — 슬링백 실루엣
   
   Prompt: [Paste from JSON]
   ```

2. **Update Image Inputs (Nodes 3-6)**:
   - Attach images listed in `referenceImages` field
   - For slide01: `slant_product` images

3. **Run Workflow**:
   - Click ▶️ "Run Workflow" (or run button on final generator node)
   - Monitor progress in Image Generator node

4. **Save Output**:
   - Right-click generated image → Save As
   - Name: `output/nanogen_images/slide01-bg.png`

5. **Verify**:
   - Check image quality
   - Confirm it matches the brief
   - Retry if needed

6. **Proceed to Next Slide**

### Slide-by-Slide Checklist

| Slide | ID | Reference Images | Status |
|-------|----|--------------------|--------|
| 1 | slide01-bg | slant_product | ⬜ |
| 2 | slide02-bg | gena_identity, slant_product | ⬜ |
| 3a | slide03-wrong | gena_identity, slant_product | ⬜ |
| 3b | slide03-right | gena_identity, slant_product | ⬜ |
| 4 | slide04-straplength | gena_identity, slant_product | ⬜ |
| 6 | slide06-styleshot | gena_identity, slant_product | ⬜ |
| 7 | slide07-outfitswap | (Outfit Swap - special) | ⬜ |

*Slides 5, 8, 9 don't need AI generation (text-only or CSS-based)*

## Optimization Tips

### 1. **Batch Similar Inputs**
- Group slides with same reference images
- Switch references only when needed

### 2. **Prompt Reuse**
- If a slide generates well, note the enhanced prompt
- Reuse similar structures for related slides

### 3. **Parallel Prep**
- While one slide generates, prepare the next slide's inputs

### 4. **Save Intermediate Results**
- Save all prompts (both input and Prompt Agent output)
- Helps with retries and future batches

## Troubleshooting

### Generation Takes Too Long
- Expected: 30-60 seconds per image
- If >2 minutes: Check Nanogen logs
- Consider reducing resolution or count

### Poor Image Quality
- Check reference image quality
- Verify prompt clarity
- Try regenerating with adjusted prompt

### Out of Memory
- Restart Nanogen
- Reduce image count to 1
- Lower resolution to 1K

## Post-Processing

After all slides generated:

1. **Organize Outputs**:
   ```bash
   /output/nanogen_images/
   ├── slide01-bg.png
   ├── slide02-bg.png
   ├── slide03-wrong.png
   ├── slide03-right.png
   └── ...
   ```

2. **Run Carousel Composer**:
   ```bash
   python scripts/compose_carousel.py
   ```

3. **Review Final Slides**:
   - Check all 9 PNG files in `output/slides/`
   - Verify text overlays are readable
   - Confirm brand consistency

## Estimated Timeline

| Phase | Time | Notes |
|-------|------|-------|
| Setup | 2 min | Open workflow, load refs |
| Slide 1 | 1 min | Input + 45s generation |
| Slide 2 | 1 min | |
| Slide 3a | 1 min | |
| Slide 3b | 1 min | |
| Slide 4 | 1 min | |
| Slide 6 | 1 min | |
| Slide 7 | 2 min | Outfit Swap (special) |
| Review | 1 min | Quick QC |
| **Total** | **10-12 min** | End-to-end |

## Next Steps

1. ✅ Workflow is ready at `http://localhost:8000`
2. ✅ Reference images are in `/assets/`
3. ✅ Prompts are in `weekly/image-prompts.json`
4. ▶️ **Start with Slide 1** → Test the full flow
5. 🔄 Refine and repeat for all 9 slides

---

**Questions or issues?** Check Nanogen logs or ask for help!
