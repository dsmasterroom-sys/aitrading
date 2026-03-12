# Runbook (bkit-lite-codex-v1)

## Goal
Ship a working v1 pipeline with minimum risk and quick iteration.

## Sequence
1. Build `brief.json`
2. Generate `prompts.json`
3. Generate `variations.json`
4. Build `scene_graph.json`
5. Render media
6. Export approval + queue handoff

## Milestone Reporting Rule
Report only when one of these happens:
- first runnable slice works
- schema/contract finalized
- full chain completes end-to-end
- blocker discovered with concrete next action

## Fail-safe
- On render retrieval failure: store operation IDs and run recovery worker.
- On schema mismatch: patch adapter, do not mutate core producer schema.

## Recommended Folder Layout
```text
studio/
  inputs/
  jobs/
  artifacts/
  exports/
  logs/
```
