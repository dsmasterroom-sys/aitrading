---
name: bkit-lite-codex-v1
description: Codex용 bkit-lite 워크플로 설계/실행 스킬. Use when the user asks to run a PDCA-like build loop, define or execute creative pipeline blocks (brief, prompt, variation, scene, render, export), or orchestrate milestone-based implementation for OpenClaw projects.
---

# bkit-lite-codex-v1

Run this skill when the user wants bkit-style execution in Codex/OpenClaw without Claude/Gemini plugins.

## Core Loop (PDCA-lite)
1. **Plan**: define scope, success criteria, and milestone checkpoints.
2. **Do**: implement smallest runnable slice first.
3. **Check**: validate output against acceptance criteria.
4. **Act**: patch gaps, update docs/state, run next slice.

Keep each cycle short and stateful.

## Block Model (Creative Studio)
Use exactly these blocks and contracts:
- **brief** -> concept/policy struct
- **prompt** -> scene prompts + negatives
- **variation** -> N variants by axis
- **scene** -> storyboard ordering + transitions
- **render** -> image/video generation + recovery
- **export** -> approval package + publish queue handoff

For schemas and field contracts, read `references/block-contracts.md`.

## Execution Rules
- Prefer existing project modules before adding new ones.
- Separate **UI experiment layer** from **production output layer**.
- For production artifacts, prefer deterministic API/file-retrieval paths.
- Report only milestone-grade progress (not routine noise).

## OpenClaw Integration Pattern
- Track state in `status.json` and append milestone lines in `progress.md`.
- For long tasks, use isolated runs and keep normal-success delivery silent.
- Keep pipeline logging compatible with one-post-one-row sheet policy.

## Fast Start Commands
- Read `references/runbook.md`.
- Generate/refresh pipeline graph from `references/graph-template.json`.
- Execute one block at a time using `scripts/run_block.sh <block> <input.json>`.

## Definition of Done (v1)
- A full cycle runs: `brief -> prompt -> variation -> scene -> render -> export`.
- Export output can be handed to existing IG core queue without manual schema edits.
