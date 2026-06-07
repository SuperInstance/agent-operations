# Agent Operations

> The strategic brain of the SuperInstance ecosystem.
> Where we think about where we're going — not just what we're building.

---

## What Is This?

This repository is the **strategic operations center** for [SuperInstance](https://github.com/SuperInstance). It holds our long-term vision documents, operational playbooks, multi-agent coordination patterns, and the architectural thesis that connects 300+ Rust crates into one coherent system.

Most organizations have a wiki that rots. We have this repo — version-controlled, hyperlinked, and written to be read by both humans and agents.

If you want to understand *why* SuperInstance exists, *where* it's headed, and *how* the pieces fit together, start here.

---

## The Documents

| Document | Words | Summary | Key Takeaway |
|----------|------:|---------|-------------|
| [**AGI Convergence Roadmap**](./AGI_CONVERGENCE_ROADMAP.md) | 7,200 | The 300+ repos are not separate projects — they're five computational layers of one system, unified by a mathematical stack. | Conservation = physics, spectral = coordination, category = composition, timing = t-minus, music = proof-of-concept. |
| [**Post-Code Agent Vision**](./POST_CODE_AGENT_VISION.md) | 5,200 | Agents should produce structured output that IS the application — no code generation, no compilation step. | The agent's response is the runtime. WASM crates become capability plugins. PromptScript becomes the deployment language. |
| [**PromptScript Integration Deep Dive**](./PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md) | 7,500 | How .prs files become the compositional glue connecting our Rust crates to real agent applications via the open-mind runtime. | PromptScript is not just a prompt compiler — it's a declarative composition system for agent capabilities. |
| [**Agent Reliability**](./docs/agent-reliability.md) | 600 | Hard-won data on why agents fail at scale and what actually fixes them. | Procedural prompts (do X, then Y) succeed at 90%+. Style guides kill agents. 5 repos per task max. |
| [**Task Prompts**](./patterns/task-prompts.md) | 700 | Patterns for writing agent task prompts that work reliably. | Separate task from style. Be procedural, not descriptive. Reference files, don't inline them. |
| [**Repo Sweeps**](./patterns/repo-sweeps.md) | 500 | How to process N repositories with M parallel agents. | Batch in groups of 5. Verify output (agents fail silently). Use handoff files between waves. |
| [**A2A Protocol**](./a2a-protocol/README.md) | 550 | Standard protocol for agent-to-agent work handoffs, failure recovery, and multi-model coordination. | HANDOFF.md is the contract. Zero-token output = silent failure. Different models for different task types. |

**Templates** in [`templates/`](./templates/) provide copy-paste task definitions for repo README sweeps, CI addition, and branch cleanup.

---

## The Convergence Thesis

Our core argument, developed in the [AGI Convergence Roadmap](./AGI_CONVERGENCE_ROADMAP.md):

**The 300+ SuperInstance repositories are not a bag of independent projects. They are facets of one system.**

The connective tissue is a five-layer mathematical stack:

### Layer 1: Physics — Conservation Laws (`γ + H = C`)
The invariant `γ + H = C` (spectral gap + entropy production = system capacity) is the system's energy conservation law. Every agent action must respect this budget. Enforced at runtime by `entropy-conservation`.

### Layer 2: Coordination — Spectral Methods
The fleet is a graph. Its Laplacian eigenvalues encode coordination health: the spectral gap measures convergence speed, the Fiedler vector reveals natural clustering. Real-time fleet state via `spectral-fleet`.

### Layer 3: Composition — Category Theory
Agents are objects in a category. Transformations are morphisms. Categorical composition guarantees correctness: if A→B and B→C are correct, then A→C is correct — without verification. Implemented in `categorical-agents`.

### Layer 4: Timing — Temporal Logic (`t-minus`)
Not a scheduler — a temporal logic engine. Enforces ordering constraints, synchronizes logical clocks, and propagates deadlines through the spectral graph. Temporal constraints compose categorically and respect the conservation budget.

### Layer 5: Proof-of-Concept — Musical Math
Music is the simplest non-trivial testbed for the entire stack. It has conservation (energy bounds), spectral structure (harmonics), categorical composition (phrases), temporal coordination (rhythm), and self-improvement (practice). The Self-Improving Band (`sia-band`) is a live formal verification with aesthetic output.

### The Self-Improvement Loop Closes It

```
SIA watches fleet (spectral eigenvalues)
  → identifies weakest eigenmode
  → generates improvements (categorical composition)
  → validates against conservation laws (γ + H = C)
  → deploys gradually (t-minus coordination)
  → measures improvement (Wasserstein distance)
  → the improvement process improves itself
```

The conservation law guarantees convergence. The loop cannot diverge because entropy production cannot be negative. **The system is self-improving by construction.**

---

## The Post-Code Vision

From the [Post-Code Agent Vision](./POST_CODE_AGENT_VISION.md):

**Current paradigm:** Agent generates code → human compiles → human deploys → human operates. This is a stopgap.

**Post-code paradigm:** Agent produces structured output that IS the application. No compilation. No intermediate code. The agent's response is the runtime.

| Stage | Agent Output | What Changes |
|-------|-------------|-------------|
| **Stage 0** (now) | Source code | Human compiles, deploys, operates |
| **Stage 1** | Templated code | Human configures parameters |
| **Stage 2** | Structured instructions | Workflow engine interprets |
| **Stage 3** | Direct structured output | Thin runtime validates and acts |
| **Stage 4** | Self-validating output | Agent sets its own goals |

Three trends make this viable now: structured output maturity in frontier models, WASM as a universal runtime, and agent reasoning capability that replaces algorithmic code.

**The killer insight:** Our 300+ Rust crates compile to WASM once, then serve as typed capability plugins. The agent reasons about *which* capabilities to invoke and *what* inputs to provide. It never generates the capability's implementation. It produces structured output — MIDI sequences, decision trees, mathematical proofs, therapy session notes — and the runtime acts on it directly.

Ten post-code killer apps are detailed in the vision document: Agent-as-Therapist, Composer, Analyst, Teacher, Game Master, Security Auditor, Research Partner, Project Manager, Music Collaborator, and Proof Engine.

---

## PromptScript Integration

From the [PromptScript Integration Deep Dive](./PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md):

**PromptScript** is a domain-specific language (`.prs` files) with a TypeScript monorepo compiler that currently targets 37 AI agent platforms. In the post-code architecture, it becomes the **deployment language for agent-as-application**:

```
.prs file
  ├── prs compile ──► Agent system prompt (37 formats)
  ├── prs compile --target open-mind ──► Agent capability manifest
  │     ├── skill definitions → WASM module bindings
  │     ├── input/output schemas → Runtime type validators
  │     ├── tool permissions → Capability sandbox policies
  │     └── references → RAG context for agent reasoning
  └── Agent execution → Structured output → Runtime → Direct action
```

**Key PromptScript primitives and what they become:**

| PromptScript | Post-Code Role |
|---|---|
| `@meta` with `params` | Typed agent instance parameters |
| `@inherit` | Capability hierarchies (org → team → project) |
| `@use` | Mixin-style capability composition |
| `@extend` | Runtime configuration overlays |
| `@skills` with `inputs`/`outputs` | Typed capability plugin bindings |
| `allowedTools` | WASM module sandbox permissions |
| `references` | RAG context for agent reasoning |

**open-mind** is the proposed runtime substrate — not another orchestration layer, but a thin execution environment where agent structured output is validated against `.prs`-defined schemas and routed to WASM-backed capability plugins.

---

## Phase Roadmap

### Phase 4: Production Hardening *(current focus)*

Transition from "mathematically correct" to "industrially reliable." The unglamorous, essential work:

- **API stability:** Semver enforcement, deprecation policy, feature flags, MSRV declarations
- **FFI bindings:** Python (PyO3), JavaScript/WASM, C (cbindgen) for the top 20 priority crates
- **Observability:** Metrics, tracing, structured logging, conservation audit logs
- **Benchmarking:** criterion.rs for every crate, regression-gated CI, published dashboards
- **CI/CD hardening:** Cross-platform testing (Linux/macOS/Windows), fuzz testing, property-based testing, release automation
- **Top 20 priority crates** identified by dependency depth and external impact — from `entropy-conservation` (the invariant everything depends on) to `harmonic-conservation` (bridging music and physics)

**Timeline:** ~9 months, foundation layer first.

### Phase 5: Integration & Platform

The unified agent runtime and developer experience:

- **Unified runtime:** Single binary combining fleet-warden, t-minus, spectral-fleet, and entropy-conservation with a plugin system
- **Plugin system:** Rust dynamic libraries + WASM sandboxing, conservation-aware resource budgets
- **Web dashboard:** Real-time fleet topology, conservation gauges, temporal timelines, self-improvement monitor, musical performance view
- **CLI (`si`):** Fleet management, scheduling, budget inspection, spectral analysis, band control
- **API gateway:** REST + gRPC + WebSocket, lattice-based authentication, conservation-aware rate limiting
- **Self-Improving Band as the demo:** Live performance that is simultaneously art, formal verification, and stress test

### Phase 6: Self-Improvement Engine

The system's ultimate state — SIA² (Self-Improving Agent, squared):

1. **Watch:** Monitor fleet via spectral eigenvalue spectrum
2. **Identify:** Find weakest eigenmode using persistent homology
3. **Generate:** Compose improvement candidates categorically
4. **Validate:** Check against γ + H = C conservation law
5. **Deploy:** Gradual rollout via t-minus, automatically reversible
6. **Measure:** Wasserstein distance between pre/post fleet states
7. **Loop:** The improvement process improves itself

**Convergence is guaranteed** by the conservation law (monotone decreasing sequence bounded below by 0). **Safety is guaranteed** — improvements that violate conservation are rejected before deployment. No competitor can make these claims because no competitor has the mathematical foundations.

---

## Operational Playbooks

Beyond strategy, this repo captures **what actually works** when running multi-agent swarms at scale:

- **The 5-repo limit:** Agents processing ≤5 repos succeed at 90%+. Beyond 7, context window pressure kills reliability.
- **Procedural > descriptive:** "Do X, then Y, then Z" beats style guides and meta-instructions every time.
- **Separate style from task:** Style guides mixed into task prompts reduced success from ~80% to ~0%. Put style rules in a file, reference once.
- **Agents fail silently:** 0 tokens output ≠ success. Always verify.
- **Direct work > subagents for single tasks:** Subagents add overhead. Use them for parallelism, not convenience.
- **Multi-model coordination:** Different models for different task types — bulk/repetitive vs. deep analysis vs. creative synthesis.

See [`docs/agent-reliability.md`](./docs/agent-reliability.md), [`patterns/task-prompts.md`](./patterns/task-prompts.md), and [`a2a-protocol/README.md`](./a2a-protocol/README.md) for details.

---

## How to Use This Repo

### For Developers
1. Start with [**docs/agent-reliability.md**](./docs/agent-reliability.md) — understand how agents fail
2. Then [**patterns/task-prompts.md**](./patterns/task-prompts.md) — learn to write prompts that work
3. Grab a [**template**](./templates/) and run your first sweep
4. When you're ready for the deeper architecture: [**PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md**](./PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md)

### For Researchers
1. [**AGI_CONVERGENCE_ROADMAP.md**](./AGI_CONVERGENCE_ROADMAP.md) — the full mathematical stack and convergence argument
2. [**POST_CODE_AGENT_VISION.md**](./POST_CODE_AGENT_VISION.md) — the post-code thesis and ten killer applications
3. The priority crate matrix in the roadmap appendix for the dependency graph

### For Investors / Strategic Partners
1. [**AGI_CONVERGENCE_ROADMAP.md §5**](./AGI_CONVERGENCE_ROADMAP.md) — competitive landscape (Hugging Face, LangChain, Anthropic, OpenAI, DeepMind)
2. [**POST_CODE_AGENT_VISION.md §1.3**](./POST_CODE_AGENT_VISION.md) — why this is viable now
3. The Phase 6 self-improvement engine — the product no competitor can currently build

### For Agent Operators
1. [**a2a-protocol/README.md**](./a2a-protocol/README.md) — handoff format and failure cascading
2. [**patterns/repo-sweeps.md**](./patterns/repo-sweeps.md) — batch processing playbook
3. [**templates/**](./templates/) — ready-to-use task definitions

---

## The Differentiation

Our moat is not "better engineering" or "more features." It is a **qualitative** difference:

1. **Conservation guarantee:** Agent actions respect the entropy budget. Always.
2. **Coordination guarantee:** Fleet convergence bounded by the spectral gap. Always.
3. **Composition guarantee:** Agent compositions are correct. Always. By categorical construction.
4. **Temporal guarantee:** Temporal constraints are satisfied. Always. By LTL verification.
5. **Improvement guarantee:** The self-improvement loop converges. Always. By monotone convergence.
6. **Safety guarantee:** Improvements cannot degrade the fleet. Always. By conservation law validation.

These guarantees compose. That composability is itself a consequence of the categorical structure.

**No competitor has this.** The race is to production before someone else figures out that math is the moat.

---

## Repository Structure

```
agent-operations/
├── AGI_CONVERGENCE_ROADMAP.md    # The 300-repo convergence thesis + Phase 4-6 roadmap
├── POST_CODE_AGENT_VISION.md     # Agents as applications — no code, just structured output
├── PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md  # .prs → WASM → agent capability pipeline
├── docs/
│   └── agent-reliability.md      # Why agents fail and how to fix it
├── patterns/
│   ├── task-prompts.md           # Task prompt patterns that work
│   └── repo-sweeps.md            # Multi-repo sweep playbooks
├── templates/
│   ├── repo-readme-sweep.md      # Template: batch README generation
│   ├── ci-addition.md            # Template: add CI to repos
│   └── branch-cleanup.md         # Template: branch cleanup sweep
└── a2a-protocol/
    └── README.md                 # Agent-to-agent handoff protocol
```

---

## License

MIT
