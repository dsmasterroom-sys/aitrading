# @gena_feed 에이전트 정의

---

## researcher
description: 트렌드 리서치와 팩트 수집 전담 + 벤치마크 계정 분석
model: claude-opus-4-5
tools: WebSearch, Read
disallowedTools: Write, Edit
skillFile: skills/research.md
contextFiles:
  - shared/brand-identity.md
  - workflows/benchmark-analysis.md
  - docs/benchmarks/insights-summary.md

---

## contents-marketer
description: 콘텐츠 기획 및 카피라이팅 전담 + 벤치마크 인사이트 적용
model: claude-opus-4-5
tools: Read, Write
disallowedTools: Bash
skillFile:
  - skills/plan-content.md
  - skills/write-copy.md
contextFiles:
  - shared/brand-identity.md
  - docs/benchmarks/insights-summary.md

---

## designer
description: 비주얼 기획 및 나노젠 프롬프트 생성 전담 + 벤치마크 비주얼 트렌드 반영
model: claude-opus-4-5
tools: Read, Write
disallowedTools: Bash
skillFile:
  - skills/design-brief.md
  - skills/nanogen-image.md
  - skills/nanogen-video.md
contextFiles:
  - shared/brand-identity.md
  - shared/design-tokens.css
  - shared/persona/
  - shared/products/
  - docs/benchmarks/insights-summary.md

---

## developer
description: 나노젠 API 호출·HTML 구현·PNG/MP4 추출 전담
model: claude-opus-4-5
tools: Read, Write, Bash
disallowedTools: 없음
skillFile:
  - skills/build-html.md
  - skills/nanogen-workflow.md
contextFiles:
  - shared/design-tokens.css

---

## qa-reviewer
description: 완성물 검수 전담 — 발견만 하고 수정 안 함
model: claude-opus-4-5
tools: Read
disallowedTools: Write, Edit, Bash
skillFile: skills/qa-check.md
contextFiles:
  - shared/brand-identity.md
