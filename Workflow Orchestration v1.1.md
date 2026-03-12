## Workflow Orchestration v1.1

### Purpose
This document defines the default execution standard for all projects.
Goal: maximize speed **without** sacrificing quality, safety, or maintainability.

---

## 1) Plan Mode (Default for Non-trivial Work)

### Enter Plan Mode when ANY of the following is true:
- Task has **3+ meaningful steps**
- Architecture/design decisions are required
- External integrations are involved (API, DB, auth, third-party services)
- Deployment/runtime config changes are involved
- Permission/security-sensitive actions are involved
- Data-loss risk exists (delete/migration/overwrite)

### Plan Mode Rules
- Write a concrete plan before implementation
- If execution deviates or fails, **stop and re-plan**
- Use plan mode for verification strategy, not just build steps
- Reduce ambiguity upfront (inputs, outputs, constraints, acceptance criteria)

---

## 2) Subagent Strategy

- Use subagents liberally to keep main context clean
- Offload research, exploration, and parallel analyses
- One objective per subagent for focus and traceability
- For complex tasks, parallelize where safe
- Main agent owns orchestration, integration, and final quality gate

---

## 3) Task Management Protocol

1. **Plan First**: Write checkable plan in `tasks/todo.md`
2. **Verify Plan**: Confirm scope/assumptions before implementation
3. **Track Progress**: Mark items done as work completes
4. **Explain Changes**: Provide high-level intent at each major step
5. **Document Results**: Add review section in `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

---

## 4) Definition of Done (DoD) — Mandatory

Never mark a task complete unless all are satisfied:
- [ ] Functional validation passed (test/manual proof)
- [ ] Relevant logs/results captured as evidence
- [ ] Regression risk checked (impacted paths reviewed)
- [ ] Rollback path identified (when change is non-trivial)
- [ ] Documentation/memory updated (`todo`, `lessons`, relevant docs)

---

## 5) Verification Before “Done”

- Prove behavior, don’t assume it
- Compare before/after behavior where applicable
- Ask: **“Would a staff engineer approve this?”**
- Run tests/checks proportional to risk

---

## 6) Elegance Gate (Balanced)

For non-trivial changes:
- Pause and ask: “Is there a simpler, more elegant solution?”
- If fix feels hacky, redesign with current understanding
- Avoid over-engineering for simple tasks

Principle: **Simple, correct, maintainable** beats clever complexity.

---

## 7) Autonomous Bug Fixing

When given a bug report:
- Reproduce/locate via logs, errors, and failing tests
- Identify root cause (not symptom patching)
- Implement fix with minimal, targeted impact
- Validate with proof (tests/logs/manual check)
- No unnecessary context-switch requests to the user

---

## 8) Self-Improvement Loop

After any user correction:
- Record pattern in `tasks/lessons.md`
- Convert into a preventive rule/checklist
- Apply rule on subsequent similar tasks
- Periodically review lessons to reduce repeat errors

---

## 9) Core Principles

- **Simplicity First**: keep changes as small and clear as possible
- **Root Cause over Quick Patch**: no temporary bandaids unless explicitly requested
- **Minimal Impact**: touch only necessary code/scope
- **Quality with Speed**: fast execution with disciplined verification
- **Security & Safety**: avoid risky/destructive actions without explicit confirmation

---

## 10) Quick Execution Template

```markdown
### Plan
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

### Verification
- [ ] Test/check A
- [ ] Test/check B

### Review (Result)
- What changed:
- Evidence:
- Risks/rollback:
- Follow-ups:

### Lessons (if corrected)
- Pattern:
- New rule:
```

---

## Operating Note
This standard is the default baseline across projects.
Project-specific constraints may add stricter rules, but should not weaken this baseline.
