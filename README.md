# agent-operations

**Strategic operations center for the SuperInstance ecosystem.** Agent reliability analysis, task prompt patterns, the A2A handoff protocol, the BATON structured handoff format, capability specifications, and the 5-layer mathematical stack — everything you need to run 300+ repos as one system.

---

## What This Repository Is

`agent-operations` is NOT a software crate. It is the documentation hub, playbook collection, and protocol specification that connects the entire SuperInstance ecosystem. If the 300+ repos are the engine, this is the driver's manual.

---

## Quick Start

```bash
git clone https://github.com/SuperInstance/agent-operations.git
cd agent-operations

# Start with agent reliability (5 min read)
cat docs/agent-reliability.md

# Then task prompt patterns (5 min read)
cat patterns/task-prompts.md

# Then the full vision (45 min read)
cat UNIFIED_VISION.md
```

### Scan Your Repos

```bash
# Discover integration opportunities across repos
python3 tools/discover_integrations.py ~/repos/superinstance

# Output: markdown report with dependency graph and suggestions
```

---

## Key Documents

| Document | Size | What It Is |
|----------|------|------------|
| [`README.md`](README.md) | This file | Operations hub overview |
| [`UNIFIED_VISION.md`](UNIFIED_VISION.md) | 45 min read | Full system architecture — application-first loop, decomposition pipeline, agent protocol, PLATO education system |
| [`AGI_CONVERGENCE_ROADMAP.md`](AGI_CONVERGENCE_ROADMAP.md) | 30 min read | The 5-layer stack in detail. Why 300+ repos are one system. Self-improvement engine. Priority crate matrix |
| [`POST_CODE_AGENT_VISION.md`](POST_CODE_AGENT_VISION.md) | 20 min read | Agents produce structured output that IS the application. No compilation. Ten killer apps |
| [`PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md`](PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md) | 25 min read | How `.prs` files become agent deployment manifests. PromptScript → WASM → structured output pipeline |
| [`SPEC_CAPABILITY_TOML.md`](SPEC_CAPABILITY_TOML.md) | 10 min read | Specification for `CAPABILITY.toml` — self-describing repos |
| [`INTEGRATION.md`](INTEGRATION.md) | 10 min read | How every crate connects to every other crate. Integration map |
| [`docs/agent-reliability.md`](docs/agent-reliability.md) | 5 min read | Hard-won data: 42% silent failure rate, 5-repo limit, procedural > descriptive |

---

## Agent Reliability Analysis

Source: [`docs/agent-reliability.md`](docs/agent-reliability.md)

### Failure Modes

| Mode | Rate | Symptoms | Root Cause |
|------|------|----------|------------|
| Silent Failure | ~42% | 0 tokens used, "completed successfully" status | Model hits reasoning limit during planning, returns without output |
| Timeout | ~8% | Uses tokens but doesn't finish | Task too large or model loops |
| Partial Completion | ~15% | Completes some items, not all | Context exhaustion, loses track |

### What Works

1. **Numbered procedural steps** — "For each repo: 1. clone, 2. read, 3. write, 4. push"
2. **Repetitive identical tasks** — Same treatment for every repo
3. **Concrete examples** — Show a sample output
4. **Single responsibility** — One agent does READMEs, another does CI

### What Doesn't Work

1. **Meta-instructions about quality/style** — Model reasons about style instead of working
2. **Template requirements** — "Must have sections 1-10" adds tracking overhead
3. **Conditional logic** — "If X do Y, else Z" increases cognitive load
4. **More than 7 items** — Success rate drops sharply

### The Task Prompt Formula

```
[ONE SENTENCE: What the agent does]

## Repos (N repos, max 5-7)

### 1. org/repo-name
"GitHub description"
[1-2 sentences about what to do]

## For each repo
1. gh repo clone org/REPO /tmp/REPO -- --depth=1
2. Read source files
3. Write README.md
4. git add README.md && git commit -m "docs: README" && git push
```

---

## Task Prompt Patterns

Source: [`patterns/task-prompts.md`](patterns/task-prompts.md)

### Pattern: Repo Sweep (README Upgrade)

**Success rate:** ~80% with 5-7 repos, ~50% with 8+

**Good prompt:**

```
Write README.md files for these repos. Clone each, study source, write, push.

## Repos

### 1. org/repo-a
"Single-header C engine — 250M checks/sec"
Study the C source. Document the API with code examples.

### 2. org/repo-b
"Rust constraint solver with 83 tests"
Study src/lib.rs. Document public API with Rust examples.

### 3. org/repo-c
"Python analysis toolkit"
Study the package. Document installation and usage.

## For each repo
1. gh repo clone org/REPO /tmp/REPO -- --depth=1
2. Read source files
3. Write README.md
4. git add README.md && git commit -m "docs: README" && git push
```

**Bad prompt** (will likely fail):

```
CRITICAL STYLE GUIDE — READ THIS FIRST:
- DO NOT use marketing language
- NO "blazing fast" NO "enterprise-ready"
- Engineers should have "ah-ha" moments

Write README.md files for these 8 repos. Each must have:
1. Name + badges
2. What it does
3. Key features
...
10. License
```

**Why it fails:** Style guide consumes reasoning tokens. 10-section template adds output planning overhead. 8 repos exceeds the working limit.

### Pattern: Single Deep Task

**Success rate:** ~85%

```
Study the EDDI codebase at /tmp/EDDI and write an adaptation plan.

## Key files
- src/main/java/.../llm/ — LLM provider abstraction
- src/main/java/.../a2a/ — Agent-to-agent protocol

## Output
Write /tmp/EDDI-ADAPTATION.md with:
1. Architecture analysis
2. Integration plan
3. Concrete steps
4. Example configs
```

---

## A2A Protocol (Agent-to-Agent Handoff)

Source: [`a2a-protocol/README.md`](a2a-protocol/README.md)

When one agent completes work and another needs to continue, they communicate via a standard handoff format.

### Handoff File Format

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

### Agent Handshake Protocol

**Parent → Subagent:**

1. Task description (procedural, not descriptive)
2. File paths to input (already cloned)
3. Expected output location
4. Max 5 work items
5. No style guides in task prompt

**Subagent → Parent:**

1. Summary of what was done (per-item)
2. What was pushed (repo + commit)
3. What failed and why
4. Recommendations for follow-up

### Failure Cascading

When a subagent fails:

1. **Check token count** — 0 tokens = silent failure
2. **Check what was pushed** — partial work is valuable
3. **Create a NEW task** for remaining items:
   - Fewer items (3 instead of 5)
   - Simpler instructions
   - No retry of the same prompt
4. **If second attempt also fails** — parent does the work directly

### Multi-Model Coordination

| Model | Best For | Max Concurrent | Avg Success |
|-------|----------|----------------|-------------|
| GLM-5.1 | Bulk code, repetitive tasks | 5 | 50-80% |
| Claude Code | Rigorous math, complex code | 1 | 90%+ |
| Kimi | Creative writing, synthesis | 1 | 70%+ |
| Direct work | Single tasks, verification | 1 | 95%+ |

**Assignment strategy:**

```
For each task:
  if task.type == "bulk_repetitive":   → GLM-5.1 (5 repos max)
  elif task.type == "deep_analysis":   → Claude Code (single task)
  elif task.type == "creative":        → Kimi (single task)
  elif task.type == "verification":    → do it yourself
  elif task.type == "single_repo":     → do it yourself
```

---

## The 5-Layer Mathematical Stack

The ecosystem is built on five layers, each providing guarantees that the layer above depends on:

```
Layer 5: Verification  ← Musical math, live formal proofs
Layer 4: Timing        ← Temporal logic, coordination constraints
Layer 3: Composition   ← Category theory, correct-by-construction pipelines
Layer 2: Coordination  ← Spectral methods, eigenvalue-based ranking
Layer 1: Physics       ← Conservation laws, γ + H = C
```

| Layer | Domain | Key Crates | Guarantee |
|-------|--------|------------|-----------|
| **1: Physics** | Conservation laws (γ + H = C) | `conservation-law`, `entropy-conservation` | Budget never created or destroyed |
| **2: Coordination** | Spectral methods | `spectral-fleet` | Fleet convergence bounded by spectral gap |
| **3: Composition** | Category theory | `categorical-agents` | Compositions correct by construction |
| **4: Timing** | Temporal logic | `t-minus` | Temporal constraints satisfied |
| **5: Proof** | Musical math | `self-improving-band` | Live formal verification |

### The Self-Improvement Loop

```
SIA watches fleet (spectral eigenvalues)
  → identifies weakest eigenmode
  → generates improvements (categorical composition)
  → validates against conservation laws (γ + H = C)
  → deploys gradually (t-minus coordination)
  → measures improvement (Wasserstein distance)
  → the improvement process improves itself
```

---

## The Conservation Law

The foundational invariant:

```
γ + H = C

γ (gamma) = productive energy — tokens spent on useful output
H (eta)   = entropy — tokens burned on errors, retries, hallucinations
C         = total budget — GPU hours, token allocation, compute ceiling
```

- You can't create energy. You can't destroy it.
- Every agent action converts γ to H (useful → waste) or doesn't happen.
- Agents that waste budget run out. Agents that are productive keep theirs.
- Natural selection for compute.

This is enforced at compile time by the `conservation-law` crate.

---

## Tools

### `discover_integrations.py`

Scans a directory for `CAPABILITY.toml` files, builds a dependency graph, and finds integration opportunities.

```bash
python3 tools/discover_integrations.py ~/repos/superinstance

# Output: markdown report with:
# - Discovered capabilities table
# - Dependency graph (provides → requires)
# - Unsatisfied dependencies
# - Integration suggestions
```

**CAPABILITY.toml format:**

```toml
name = "my-repo"
version = "0.1.0"
description = "What this repo does"

provides = ["capability-a", "capability-b"]
requires = ["capability-c"]
```

---

## Patterns & Templates

| Path | What It Provides |
|------|-----------------|
| [`patterns/task-prompts.md`](patterns/task-prompts.md) | How to write agent prompts that work. Procedural > descriptive. |
| [`patterns/repo-sweeps.md`](patterns/repo-sweeps.md) | How to process 300+ repos with parallel agents. Batch of 5, verify output. |
| [`templates/repo-readme-sweep.md`](templates/repo-readme-sweep.md) | Copy-paste template for README sweep tasks |
| [`templates/branch-cleanup.md`](templates/branch-cleanup.md) | Template for branch cleanup sweeps |
| [`templates/ci-addition.md`](templates/ci-addition.md) | Template for CI addition sweeps |
| [`a2a-protocol/README.md`](a2a-protocol/README.md) | Agent-to-agent handoff protocol with failure recovery |

---

## Integration Points

agent-operations integrates with every SuperInstance crate because it defines the architecture that connects them:

```
conservation-law (Layer 1)     → "Energy is conserved"
spectral-fleet (Layer 2)       → "Coordination converges"
categorical-agents (Layer 3)   → "Composition is correct"
t-minus (Layer 4)              → "Timing is satisfied"
```

### Key Integration Chains

- **`si-cli` → `si-fleet-api`** — CLI scans repos, syncs to Supabase, API serves them
- **`conservation-law` → `si-conservation-python`** — Rust core with PyO3 bindings
- **`si-runtime-python` / `si-runtime-go`** — Same API, different languages, same conservation law
- **`ecosystem-dashboard`** — Visualizes data from the Supabase tables that `si-cli` and `si-fleet-api` populate

---

## The Runtime Implementations

Same math at every level. γ + H = C in C, TypeScript, Python, Go, and Rust. Power iteration in every language. The law doesn't change because the language does.

| Runtime | Language | Key Feature |
|---------|----------|-------------|
| [`si-core-c`](https://github.com/SuperInstance/si-core-c) | C | ~15 KB compiled, embedded, WASM |
| [`si-runtime-python`](https://github.com/SuperInstance/si-runtime-python) | Python | Pure Python, zero deps |
| [`si-conservation-python`](https://github.com/SuperInstance/si-conservation-python) | Rust/Python | PyO3 bindings for heavy compute |
| [`si-runtime-go`](https://github.com/SuperInstance/si-runtime-go) | Go | Zero deps, Docker-ready |
| [`si-runtime-js`](https://github.com/SuperInstance/si-runtime-js) | TypeScript | Node.js and browser |
| 300+ Rust crates | Rust | The bedrock |

---

## Where Vectors Become Code

The thesis (from [`POST_CODE_AGENT_VISION.md`](POST_CODE_AGENT_VISION.md)):

- **The vector IS the agent** — An agent's spectral identity is what the agent does
- **The embedding IS the function** — Capability embeddings encode function, not just similarity
- **The distance IS the budget** — Wasserstein distance measures how much γ must be spent to transform fleet state A to B

This is why the ecosystem is one system, not 300 separate repos.

---

## Related Repos

| Repo | Language | Description |
|------|----------|-------------|
| [`conservation-law`](https://github.com/SuperInstance/conservation-law) | Rust | Core conservation law (Layer 1) |
| [`spectral-fleet`](https://github.com/SuperInstance/spectral-fleet) | Rust | Spectral ranking (Layer 2) |
| [`categorical-agents`](https://github.com/SuperInstance/categorical-agents) | Rust | Category theory composition (Layer 3) |
| [`t-minus`](https://github.com/SuperInstance/t-minus) | Rust | Temporal coordination (Layer 4) |
| [`si-cli`](https://github.com/SuperInstance/si-cli) | Rust | CLI for fleet management |
| [`si-fleet-api`](https://github.com/SuperInstance/si-fleet-api) | TypeScript | REST API for fleet budgets |
| [`ecosystem-dashboard`](https://github.com/SuperInstance/ecosystem-dashboard) | HTML/JS | Live ecosystem monitoring |

---

## License

MIT
