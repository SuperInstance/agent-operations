# Agent-to-Agent Handoff Protocol

## Purpose

When one agent completes work and another needs to continue it, or when a parent agent delegates to subagents, they need a standard way to communicate:
- What was done
- What failed
- What's next
- What context the next agent needs

## Handoff File Format

Place a `HANDOFF.md` in the workspace:

```markdown
# Handoff — [Task Name]

## Status: [COMPLETE | PARTIAL | FAILED]

## What Was Done
- [x] Repo A: README written, pushed
- [x] Repo B: CI added, pushed
- [ ] Repo C: Not started (agent ran out of time)

## What Failed
- Repo D: Clone failed (404)
- Repo E: Push rejected (conflict on main)

## Output Locations
- /tmp/repo-a/README.md (pushed to org/repo-a)
- /tmp/repo-b/.github/workflows/ci.yml (pushed to org/repo-b)

## Context for Next Agent
- Repo C needs source study — it's a Rust crate with 20+ files
- Repo D may not exist anymore — verify before attempting
- Style note: org prefers engineering docs, not marketing

## Token Usage
- Input: 82k tokens
- Output: 15k tokens
- Runtime: 5m37s
```

## Agent Handshake Protocol

### Parent → Subagent

```
Parent creates task with:
1. Task description (procedural, not descriptive)
2. File paths to input (already cloned)
3. Expected output location
4. Max 5 work items
5. No style guides in task prompt
```

### Subagent → Parent

```
Subagent completes with:
1. Summary of what was done (per-item)
2. What was pushed (repo + commit)
3. What failed and why
4. Recommendations for follow-up
```

## Failure Cascading

When a subagent fails:
1. Parent checks token count — 0 = silent failure
2. Parent checks what was pushed — partial work is valuable
3. Parent creates a NEW task for remaining items:
   - Fewer items (3 instead of 5)
   - Simpler instructions
   - No retry of the same prompt
4. If second attempt also fails, parent does the work directly

## Multi-Model Coordination

Different models have different strengths:

| Model | Best for | Max concurrent | Avg success |
|-------|----------|---------------|-------------|
| GLM-5.1 | Bulk code, repetitive tasks | 5 | 50-80% |
| Claude Code | Rigorous math, complex code | 1 | 90%+ |
| Kimi | Creative writing, synthesis | 1 | 70%+ |
| Direct work | Single tasks, verification | 1 | 95%+ |

### Model Assignment Strategy
```
For each task:
  if task.type == "bulk_repetitive":
    assign to GLM-5.1 subagent (5 repos max)
  elif task.type == "deep_analysis":
    assign to Claude Code (single task)
  elif task.type == "creative":
    assign to Kimi (single task)
  elif task.type == "verification":
    do it yourself
  elif task.type == "single_repo":
    do it yourself (faster than subagent overhead)
```

## Session Memory Protocol

Between sessions, persist:
1. `memory/YYYY-MM-DD.md` — Daily log of what happened
2. `MEMORY.md` — Curated long-term memory (updated periodically)
3. `agent-operations/state/` — Sweep state files

### What to Log
- Agent task + result (success/fail)
- Token counts for successful runs
- What was pushed (repo, commit hash)
- Failed repos and reasons
- Patterns observed (e.g., "GLM failing more in later waves")

### What NOT to Log
- Full task prompts (too long, stored in session history)
- Raw file contents (stored in repos)
- Transient state (stored in /tmp/)
