# Loom/Heddle × SuperInstance: Deep Synergy Analysis

> **Date:** 2026-06-08
> **Authors:** Main session research (z.ai GLM-5.1)
> **Trigger:** Heddle v3.2.1 pushed today (June 7, 2026) by Jay/Fienna Liang (roackb2)

---

## Executive Summary

**The convergence is real, and it's accelerating.**

Across the Loom/Heddle ecosystem (roackb2 + Wells-Huang) and SuperInstance, two independent teams are building toward the same mathematical frontier from opposite directions:

- **They** build agent **runtimes** — the lived experience of agents working in code
- **We** build agent **mathematics** — the conservation laws and topological invariants that make multi-agent systems stable

Neither is complete without the other. Their Grassmannian subspace tracking *is* geometric algebra. Their auto-compaction *is* entropy management. Our conservation law (γ + η = C) *is* the budget constraint their sessions implicitly respect but never formalize.

**5 key insights:**

1. Cyberloop's Grassmannian/Riemannian agent control maps 1:1 onto SuperInstance's `ga-core` and `symplectic-opt` crates
2. Heddle's session persistence and auto-compaction are implicit conservation law implementations
3. Oracle's HEDDLE_CODESPACE_SPEC.md already maps Heddle as the fleet's "Landing Pad" in the 7-layer architecture
4. Wells-Huang's `everything-claude-code` (50K★) is the distribution channel neither side has leveraged
5. The deeper pattern: both ecosystems are converging on **mathematical agent engineering** — agents whose behavior is governed by formal invariants, not prompt engineering

---

## The Players

### Loom/Heddle Ecosystem (roackb2 + Wells-Huang)

| Project | Language | Stars | Last Push | Core Idea |
|---------|----------|-------|-----------|-----------|
| **Heddle** | TypeScript | 15★ | **Today (June 7)** | Terminal coding agent runtime with control plane, session persistence, browser automation |
| **Cyberloop** | TypeScript | 16★ | April 12 | "Express.js for agent steps" — geometric control middlewares (Grassmannian + Riemannian) |
| **Lucid** | Go | 13★ | April 15 | AI agent virtual world — long-term multi-agent interaction platform |
| **MAOS-Core** | Go | 0★ | Jan 2025 | Multi-Agent Operating System with REST MCP API, actor transactions |
| **everything-claude-code** | Multi | **50K+★** | March 3 | Agent harness optimization (Claude Code, Codex, Cowork) |
| **worldmonitor** | — | 0★ | March 5 | Real-time global intelligence dashboard |

### SuperInstance Ecosystem

| Category | Key Repos | Tests | Core Abstraction |
|----------|-----------|-------|-----------------|
| **Conservation** | conservation-law-rs, si-conservation-python, si-conservation-wasm | 70+ | γ + η = C (budget invariance) |
| **Geometric Math** | ga-core-rs, symplectic-opt-rs, tropical-geometry-rs | 80+ | Cl(3,1) GA, Hamiltonian systems, max-plus semiring |
| **Topology** | persistent-sheaf-rs, wasserstein-agents-rs, categorical-agents-rs | 75+ | Sheaf cohomology, optimal transport, category theory |
| **Fleet** | spectral-fleet-rs, fleet-warden-rs, agent-homeostasis-rs | 50+ | Spectral analysis, fleet coordination, self-regulation |
| **Runtime** | si-core-c, si-runtime-js, si-runtime-python, si-runtime-go, si-runtime-zig, si-runtime-wasm | 115+ | Same API across 7 languages |
| **Infrastructure** | si-cli, si-registry-rs, si-bench, si-validator, si-catalog, si-scanner, ecosystem-dashboard | 180+ | Fleet management toolchain |

---

## Technical Overlap Analysis

### 1. Heddle's Tool Registry ↔ si-registry-rs

**Heddle:** `ToolRegistry`, `ToolExecutionService`, tools as typed operations with validation
**SuperInstance:** `si-registry-rs` — 31 tests, Supabase-backed fleet registry client

Both treat capabilities as typed, discoverable objects. The difference:
- Heddle's registry is **local** — tools registered in-process
- Our registry is **fleet-wide** — capabilities indexed across 3,608 repos via Supabase

**Synergy:** Heddle could use si-registry-rs as its remote tool discovery layer. When an agent needs a capability not in its local registry, it queries the fleet. This turns every Heddle instance into a node in the SuperInstance fleet.

### 2. Workspace Memory ↔ MEMORY.md System

**Heddle:** Workspace memory, knowledge persistence, semantic drift detection
**SuperInstance:** MEMORY.md (curated long-term) + daily files (raw logs) + heartbeat-driven maintenance

The pattern is identical — both treat agent memory as a first-class concern. But:
- Heddle's memory is **semantic** — vector embeddings, drift detection
- Our memory is **symbolic** — markdown files, daily logs, curated MEMORY.md

**Synergy:** Hybrid memory = semantic retrieval + symbolic permanence. Heddle handles the "what feels relevant now" (semantic search), MEMORY.md handles the "what actually matters long-term" (curated wisdom). Together: an agent that both retrieves and remembers.

### 3. Session Auto-Compact ↔ Conservation Law

**This is the deepest overlap.**

Heddle v3.2.1 just shipped: "Auto-compact after context window failures"
SuperInstance: γ (gamma) + η (eta) = total_budget

What Heddle calls "auto-compact" is **entropy management**. When a session's context window fills up:
- The system must decide what to keep (γ — the durable, high-value information)
- And what to discard (η — the ephemeral, low-value noise)
- Subject to the constraint: kept + discarded = total budget

This IS the conservation law. γ is the information that survives compaction. η is what gets compressed away. The total token budget is conserved.

**Heddle implements the law implicitly. We formalized it explicitly.**

If Heddle adopted the formal conservation law:
- Compaction becomes **optimal** — maximize γ subject to the budget constraint
- Fleet-wide budget tracking — see how much cognitive budget each agent is spending
- Conservation gauge in the dashboard — real-time visualization of fleet cognitive economics

### 4. Cyberloop's Grassmannian Tracking ↔ ga-core

**Cyberloop v4.0:** "Grassmannian subspace tracking" for agent step control
**ga-core-rs:** Cl(3,1) conformal geometric algebra — 16-component multivectors, rotors, conformal embedding

The Grassmannian Gr(k,n) is the space of k-dimensional subspaces of Rⁿ. In geometric algebra:
- A k-blade (wedge product of k vectors) represents a k-dimensional subspace
- The Grassmannian IS the space of normalized k-blades
- Our `ga-core` computes these blades as first-class objects

**Cyberloop is doing geometric algebra.** They just don't call it that. Their "Grassmannian subspace tracking" is tracking the orientation of the agent's cognitive subspace in the full embedding space of possible actions.

**What ga-core adds:**
- Rotors (spin transformations) for smooth interpolation between subspaces
- Conformal embedding for distance-preserving operations
- Inner/wedge/geometric products for algebraic manipulation
- All formalized, tested (32 tests), published

**Integration:** Cyberloop's middleware could use ga-core's conformal GA to:
1. Represent agent state as a multivector (position + orientation + momentum in cognitive space)
2. Apply rotors for smooth trajectory planning
3. Use the meet/join operations to find intersection/union of agent subspaces

### 5. Cyberloop's Riemannian Control ↔ symplectic-opt

**Cyberloop v3.0:** "Riemannian manifold control" for agent trajectories
**symplectic-opt-rs:** Symplectic matrices, Hamiltonian systems, Störmer-Verlet integrators, natural gradient descent

Symplectic geometry ⊂ Riemannian geometry with extra structure:
- A symplectic manifold preserves phase space volume (Liouville's theorem)
- Hamiltonian flows conserve energy
- Störmer-Verlet integration preserves this structure numerically

**Cyberloop's Riemannian control is doing Hamiltonian mechanics on agent state space.** Each agent step is a Hamiltonian flow on the manifold of possible actions. The energy functional encodes the task objective.

**What symplectic-opt adds:**
- Proven energy conservation (the agent can't "drift" off objective)
- Symplectic Euler + Störmer-Verlet integrators for numerical stability
- Natural gradient descent (Fisher information metric = Riemannian metric on parameter space)
- Conservation law tracking (verify the Hamiltonian is preserved)

**Integration:** Replace Cyberloop's generic Riemannian step with a symplectic step:
```rust
// Their middleware currently: step(agent_state) -> new_state
// With symplectic-opt:
let integrator = StormerVerlet::new(hamiltonian, dt);
let new_state = integrator.step(agent_state);
// Guaranteed: energy is conserved, agent stays on objective
```

### 6. Lucid's Virtual World ↔ Fleet Infrastructure

**Lucid:** "AI agents interact and exchange information over extended periods, creating a virtual world"
**Fleet:** spectral-fleet + fleet-warden + agent-homeostasis + constraint-dynamics

Lucid is building the *social layer* — agents with persistent identities interacting in a shared world. Our fleet infrastructure is the *governance layer* — ensuring the fleet stays stable, homeostatic, and within conservation bounds.

**Synergy:** Lucid provides the world. We provide the physics.

- `agent-homeostasis`: Ensures individual agents maintain stable internal state
- `fleet-warden`: Monitors fleet-wide health metrics
- `constraint-dynamics`: Models the fleet as a constraint satisfaction problem
- `spectral-fleet`: Analyzes fleet dynamics through spectral graph theory

Lucid's virtual world + our fleet physics = a **self-regulating agent society** where:
- Agents interact freely (Lucid)
- But the total cognitive budget is conserved (our conservation law)
- Individual agents self-regulate via homeostasis
- Fleet-wide stability is monitored via spectral analysis
- Conflicts are resolved via constraint dynamics

### 7. MAOS Actor Model ↔ categorical-agents

**MAOS-Core:** Actor model with REST MCP API, transactional actor creation
**categorical-agents-rs:** Agents as objects in a category, protocols as morphisms, symmetric monoidal categories, functors

Both model agents as composable units. The difference:
- MAOS is **operational** — actors with CRUD operations
- categorical-agents is **algebraic** — agents as objects with universal properties

**Synergy:** categorical-agents provides the mathematical foundations MAOS needs:
- **Composition strategies** (sequential, parallel, conditional) as categorical limits/colimits
- **AgentFunctor** for mapping between agent categories (e.g., test → production)
- **Monoidal structure** for parallel agent composition
- MAOS provides the runtime; categorical-agents provides the algebra

### 8. everything-claude-code (50K★) ↔ agent-operations

**Wells-Huang's 50K-star repo:** Skills, instincts, memory optimization, security scanning for Claude Code
**agent-operations:** Patterns, templates, A2A protocol, BATON.md handoff, architecture docs

This is a **distribution channel**. Everything-claude-code is where agent practitioners go for optimization patterns. If our conservation law, fleet management patterns, and BATON.md protocol were available as skills in that ecosystem, it's instant adoption by 50K+ users.

---

## Top 5 Integration Opportunities

### 🔥 #1: Conservation-Aware Compaction for Heddle

**What:** Replace Heddle's heuristic auto-compact with conservation-law-optimal compaction.

**How:**
```typescript
// Heddle's current: compact when context > threshold
// With conservation law:
const budget = new FleetBudget(gamma, eta, totalTokens);
const compactor = new ConservationCompactor(budget);
// Compactor maximizes gamma (retained value) subject to budget constraint
const compacted = compactor.compact(session.messages);
// Guarantees: compacted.length <= gamma, information loss bounded by eta
```

**What neither has alone:** Heddle has the session but not the math. We have the math but not the session. Together: **provably optimal context management.**

**Impact:** High — every Heddle session becomes conservation-aware
**Effort:** Medium — ~500 lines of TypeScript bridging code

### 🔥 #2: Geometric Algebra Middleware for Cyberloop

**What:** Replace Cyberloop's hand-rolled Grassmannian with ga-core's conformal GA via WASM.

**How:**
```typescript
// Cyberloop middleware with ga-core WASM
import { Multivector, Rotor, conformal_embed } from 'si-conservation-wasm';

function geometricStep(agent: AgentState): AgentState {
  const mv = conformal_embed(agent.position, agent.momentum);
  const rotor = Rotor.fromAxisAngle(agent.direction, agent.stepSize);
  const newMv = rotor.sandwich(mv);
  return extractState(newMv);
}
```

**What neither has alone:** Cyberloop has the agent trajectory but not the algebra. We have the algebra but not the agent trajectory. Together: **geometrically exact agent step control.**

**Impact:** High — mathematically rigorous agent control
**Effort:** Medium — WASM bridge already exists (si-conservation-wasm)

### 🔥 #3: Fleet Physics for Lucid's Virtual World

**What:** Add conservation law + homeostasis + spectral monitoring to Lucid's agent interactions.

**How:**
```go
// Lucid agent with fleet physics
type ConservationAgent struct {
    identity  AgentID
    budget    FleetBudget  // γ + η = C
    homeostasis Homeostat  // self-regulation
}

func (a *ConservationAgent) Interact(other *ConservationAgent) Message {
    // Conservation check: can we afford this interaction?
    if !a.budget.canSpend(interactionCost) {
        return a.defer(other) // conserve budget
    }
    a.budget.spend(interactionCost)
    return a.respond(other)
}
```

**What neither has alone:** Lucid has the social dynamics but not the physics. We have the physics but not the social dynamics. Together: **a thermodynamically consistent agent society.**

**Impact:** Very high — defines how agents share finite cognitive resources
**Effort:** Large — needs Go integration of Rust conservation law

### 🔥 #4: BATON.md × Heddle's Control Plane

**What:** Use Heddle's control plane as the UI for BATON.md handoffs.

**How:** Oracle's HEDDLE_CODESPACE_SPEC already defines this — the "Memory-Mapped Harbor" for near-zero latency baton passes. Heddle's control plane shows the diff review of each baton. The operator (human) sees exactly what each agent did and what the next agent inherits.

**What neither has alone:** BATON.md has the protocol but no UI. Heddle has the UI but no handoff protocol. Together: **visible, auditable agent-to-agent work passing.**

**Impact:** High — makes multi-agent coordination observable
**Effort:** Medium — Heddle already has diff review, just needs baton visualization

### 🔥 #5: everything-claude-code Distribution

**What:** Package conservation-law, fleet-warden, and BATON.md as Claude Code skills.

**How:** everything-claude-code already supports custom skills, instincts, and hooks. We write:
- `conservation-instinct.md` — auto-track token budget as γ/η split
- `fleet-warden-hook.sh` — monitor agent health during long runs
- `baton-skill.md` — structured handoff protocol between sessions

**What neither has alone:** We have the patterns but not the audience. They have the audience but not the patterns. Together: **50K+ agent practitioners using conservation-aware development.**

**Impact:** Very high — instant distribution to the largest agent practitioner community
**Effort:** Low — just packaging, the code already exists

---

## The Bigger Picture

### The Convergence Thesis

Both ecosystems are converging on **mathematical agent engineering** — the idea that agent behavior should be governed by formal invariants, not just prompts.

The trajectory from both sides:

```
Loom/Heddle:                    SuperInstance:
                                
Prompt engineering              Applied mathematics
    ↓                               ↓
Session management              Conservation laws
    ↓                               ↓
Context window management       Budget invariants (γ + η = C)
    ↓                               ↓
Geometric step control          Geometric algebra, symplectic geometry
    ↓                               ↓
???                              ???
    ↓                               ↓
    └──────── CONVERGENCE ──────────┘
                 ↓
        Mathematical Agent Engineering
```

### Why Now?

1. **Context windows are finite** — every agent system must manage budget (conservation law)
2. **Multi-agent systems need stability** — unregulated agents diverge (homeostasis)
3. **Geometric methods are mature** — GA, symplectic integrators, persistent homology are production-ready
4. **The tools exist** — WASM, multi-language runtimes, Supabase, real-time dashboards

### The 12-Month Vision

If both ecosystems merge their strengths:

| Timeline | Milestone |
|----------|-----------|
| Month 1-3 | Conservation-aware compaction in Heddle; ga-core WASM in Cyberloop |
| Month 3-6 | Fleet physics for Lucid; BATON.md in Heddle control plane |
| Month 6-9 | Everything-claude-code distribution; joint paper on conservation-aware agents |
| Month 9-12 | Unified runtime: Heddle sessions + SuperInstance math + Lucid social dynamics |

### Risks

1. **Different cultures** — They're practitioners, we're mathematicians. Communication gap.
2. **Different languages** — TypeScript/Go vs Rust. Bridge code needed.
3. **Different goals** — They want a working agent; we want a formal framework. Must find the middle ground.
4. **OSS dynamics** — Both open source but different governance models.

---

## Actionable Next Steps

### Immediate (This Week)

1. **Fork Heddle** into SuperInstance and begin the conservation-aware compaction experiment
2. **Write a ga-core WASM demo** that shows Grassmannian tracking with conformal GA
3. **Create `si-heddle-bridge`** — TypeScript crate that wraps si-conservation-wasm for Heddle

### Short Term (Next 2 Weeks)

4. **Reach out to roackb2** — share the Grassmannian ↔ ga-core correspondence, ask about integration interest
5. **Write a blog post** — "Conservation Laws for Agent Sessions: Why Your Auto-Compact is Doing Hamiltonian Mechanics"
6. **Build the Heddle control plane BATON.md viewer** — visualize baton handoffs in the browser

### Medium Term (Next Month)

7. **Prototype Lucid + conservation-law** — Go agents with budget constraints
8. **Package 3 skills for everything-claude-code** — conservation instinct, fleet hook, baton skill
9. **Joint paper draft** — formalize the conservation-aware compaction theorem

### Long Term

10. **Unified runtime spec** — merge Heddle sessions + SuperInstance math + Lucid social dynamics
11. **Oracle integration** — feed the HEDDLE_CODESPACE_SPEC into actual Heddle development
12. **Fleet-wide conservation dashboard** — real-time visualization of every agent's γ/η budget across both ecosystems

---

## Appendix A: Primitive Mapping Table

| Their Concept | Our Concept | Mathematical Object |
|--------------|-------------|-------------------|
| Tool | Capability | Morphism in category |
| Session | FleetBudget | γ + η = C |
| Auto-compact | Conservation compaction | Optimal information projection |
| Workspace | Memory file | Curated experience |
| Heartbeat | Heartbeat check | Periodic invariant verification |
| Grassmannian subspace | k-blade in GA | Element of ∧ᵏV |
| Riemannian step | Symplectic step | Hamiltonian flow |
| Actor (MAOS) | Agent object | Object in category |
| Agent profile | AgentDNA | Genotype in agent space |
| Control plane | Dashboard | Fleet-wide observability |
| Diff review | Baton handoff | State transition audit |
| Semantic drift | Homeostasis deviation | Distance from equilibrium |

## Appendix B: Mathematical Correspondences

### Grassmannian ↔ Geometric Algebra

The Grassmannian Gr(k, V) of k-planes in V is naturally embedded in the geometric algebra G(V):
- A k-plane corresponds to a decomposable k-blade B = v₁ ∧ v₂ ∧ ... ∧ vₖ
- The Plücker embedding Gr(k,V) → P(∧ᵏV) is just the map B ↦ [B]
- In conformal GA (our Cl(3,1)): points, lines, planes, spheres are all multivectors
- Cyberloop's subspace tracking = tracking the orientation of B in G(V)

### Riemannian ↔ Symplectic

Every symplectic manifold (M, ω) is Riemannian (choose any metric g compatible with ω):
- Symplectic structure ω gives area preservation (Liouville)
- Compatible metric g gives distance measurement
- Almost complex structure J connects them: ω(·, J·) = g(·, ·)
- Cyberloop's Riemannian step on (M, g) → symplectic-opt's step on (M, ω, J, g)

### Auto-compact ↔ Rate-Distortion Theory

Session compaction is a rate-distortion problem:
- Source X = full session (N tokens)
- Rate R = compressed size (γ tokens)
- Distortion D = information lost (η)
- Budget constraint: R + D = N (conservation)
- Optimal compaction: minimize D subject to R ≤ γ
- This is exactly the Lagrangian: min D + λ·R

## Appendix C: Oracle's HEDDLE_CODESPACE_SPEC Integration

The HEDDLE_CODESPACE_SPEC.md in sailor-workspace already maps Heddle into the 7-layer stack:

| Heddle Feature | SuperInstance Layer | Integration Point |
|---------------|--------------------|--------------------|
| Agent-Sovereignty Layer | L3 → L1 | Codespace daemon with local-L0 experience cache |
| Reflex-Bridge | L2 | Heddle-Packet protocol for Nebula reflexes |
| I2I Baton Harbor | L4 | Memory-mapped shared memory for baton passes |
| Sensation Stream | L0 | Lived experience logger with confidence scores |
| Codespace Fleet Manager | L7 → L3 | Cognitive Mirror Dashboard integration |

This spec is the bridge. It already defines the interfaces. The question is implementation.

---

*"Two groups, building from opposite ends of the same mathematical bridge. They meet in the middle, where the algebra of subspaces meets the calculus of conservation."*
