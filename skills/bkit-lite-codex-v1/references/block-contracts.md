# Block Contracts (bkit-lite-codex-v1)

## 1) brief
Input: user concept + product/persona constraints
Output:
```json
{
  "brief_id": "brief_001",
  "concept": "string",
  "persona_goal": "string",
  "hook": "string",
  "must": ["string"],
  "dont": ["string"]
}
```

## 2) prompt
Input: brief
Output:
```json
{
  "brief_id": "brief_001",
  "scene_prompts": [
    {"scene_id":"s1","prompt":"...","negative_prompt":"..."}
  ]
}
```

## 3) variation
Input: scene prompt + refs + variation_policy
Output:
```json
{
  "scene_id":"s1",
  "variants":[{"artifact_id":"img_001","seed":123,"axis":{"angle":"front"}}]
}
```

## 4) scene
Input: variants
Output:
```json
{
  "scenes":[{"id":"s1","images":["img_001","img_002"]}],
  "transitions":[{"from":"s1","to":"s2","type":"match-cut"}]
}
```

## 5) render
Input: scenes + render_profile
Output:
```json
{
  "scene_videos":["vid_s1.mp4"],
  "transition_videos":["tr_s1_s2.mp4"],
  "recoverable_ops":["op_xxx"]
}
```

## 6) export
Input: render outputs + caption metadata
Output:
```json
{
  "approval_package":{"caption":"...","media":["final.mp4"]},
  "publish_queue_entry":{"account":"gena_feed","artifact":"final.mp4"}
}
```
