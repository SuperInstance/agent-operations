# AGI Convergence Roadmap

> "The system was never separate. We just hadn't found the connective tissue yet."

**Status:** Draft v0.1 — Internal Strategic Document  
**Date:** 2026-06-07  
**Author:** SuperInstance Strategic Ideation  
**Classification:** Internal — Core Team

---

## Table of Contents

1. [The Convergence Argument](#1-the-convergence-argument)
2. [Phase 4 — Production Hardening](#2-phase-4--production-hardening)
3. [Phase 5 — Integration & Platform](#3-phase-5--integration--platform)
4. [Phase 6 — The Self-Improvement Engine](#4-phase-6--the-self-improvement-engine)
5. [Competitive Landscape](#5-competitive-landscape)
6. [Appendix: Priority Crate Matrix](#appendix-priority-crate-matrix)

---

## 1. The Convergence Argument

### 1.1 The Illusion of Separation

At time of writing, the SuperInstance ecosystem spans 300+ repositories. To an outside observer — and, frankly, to many inside the project — these appear to be distinct research efforts. Tropical geometry over here, lattice cryptography over there, a musical math engine somewhere else, and an agent identity protocol that looks like yet another PKI system. The fork integrations (baml, aider, dify, BMAD) look like tactical tooling choices, not architectural decisions.

This perception is wrong. These are not separate projects. They are facets of one system, and the reason they appear separate is that we have been building the components before articulating the architecture they implicitly compose. This section makes that architecture explicit.

### 1.2 The Five Layers

The SuperInstance ecosystem decomposes into five computational layers, each building on the one below:

#### Layer 1: Physics — Conservation Laws (γ + H = C)

The conservation law `γ + H = C` (where γ is the spectral gap, H is the entropy production rate, and C is the system capacity constant) is not a metaphor. It is the invariant that governs every agent in the fleet. It plays the role that energy conservation plays in classical mechanics: a hard constraint that all dynamics must respect.

The entropy-conservation crate enforces this. Every agent action that increases entropy H must be compensated by a decrease in spectral gap γ (the "tightness" of coordination), and the total must remain within C. This is not a soft heuristic — it is a hard budget enforced at the runtime level. Agents that violate it are, by definition, malfunctioning.

This layer is the *physics* of the system. Just as you cannot engineer a bridge without respecting the conservation of energy, you cannot build reliable agent coordination without respecting γ + H = C. Everything else builds on top of this invariant.

**Key crates:** `entropy-conservation`, `spectral-gap`, `capacity-budget`

#### Layer 2: Coordination — Spectral Methods

If conservation laws are the physics, spectral methods are the coordination mechanism. The `spectral-fleet` crate represents the fleet as a graph where edge weights encode inter-agent trust, communication latency, and task affinity. The eigenvalues of this graph's Laplacian tell us:

- **The spectral gap** (smallest non-zero eigenvalue): How quickly the fleet converges to consensus. A large gap means fast coordination. A small gap means the fleet is near a bifurcation point — it's about to fragment.
- **The Fiedler vector** (eigenvector of the smallest non-zero eigenvalue): The natural clustering of agents. This is how the fleet self-organizes into sub-teams without central direction.
- **Higher eigenvalues**: The multi-scale structure of coordination — which groups of groups can operate semi-independently.

The spectral-fleet crate doesn't just compute these — it computes them *incrementally*, updating the decomposition as agents join, leave, and reconfigure. This is what makes real-time fleet coordination possible: the eigenstructure is the fleet's living representation of its own state.

The connection to Layer 1 is direct: the spectral gap γ *is* the first term in the conservation law. The coordination layer is literally reading out the physics variable.

**Key crates:** `spectral-fleet`, `laplacian-update`, `fiedler-cluster`, `eigenstream`

#### Layer 3: Composition — Category Theory

Category theory is the composition layer. Individual agents are objects in a category. Agent transformations (learning, adaptation, communication) are morphisms. The composition of morphisms gives us guaranteed properties: if agent A → B is correct and B → C is correct, then A → C is correct, without needing to verify the composite directly.

The `categorical-agents` crate implements this. But it goes deeper than type-safe composition. It implements:

- **Functorial mappings** between agent categories: An agent in the "exploration" category can be mapped to an agent in the "exploitation" category via a functor that preserves the compositional structure. This is how we get principled exploration-exploitation tradeoffs.
- **Natural transformations** between coordination strategies: When the fleet switches from one coordination protocol to another (e.g., from hierarchical to mesh), a natural transformation guarantees that the switch preserves all in-flight computations.
- **Adjunctions** between specification and implementation: There's a free functor from specifications (what you want) to implementations (what you get), and a forgetful functor back. The adjunction says that the "best" implementation is the one that adds the least unnecessary structure.

This is where the `constraint-dsl` fits: it's the internal language of the category. When you write constraints in the DSL, you're writing in the internal language of a monoidal category, and the type system ensures your constraints are compositional.

**Key crates:** `categorical-agents`, `constraint-dsl`, `functor-compose`, `nat-transform`

#### Layer 4: Timing — Temporal Coordination (t-minus)

Temporal coordination — the `t-minus` system — is the timing layer. It's not a scheduler. It's a temporal logic engine that enforces:

- **Temporal invariants:** "Agent A must complete task X before agent B starts task Y" is a temporal logic constraint, enforced at the protocol level.
- **Clock synchronization:** Agents operate on a logical clock (Lamport-style, but augmented with spectral timestamps that encode fleet state). This means temporal ordering is consistent even across network partitions.
- **Deadline propagation:** When a deadline changes, it propagates through the fleet via the spectral graph (Layer 2), using the Fiedler vector to prioritize which agents need the update first.

The connection to the lower layers is precise: temporal constraints are constraints in the DSL (Layer 3), which compose categorically, and their enforcement respects the conservation budget (Layer 1). When the fleet is running hot (high H, low γ), the temporal layer knows to relax soft deadlines rather than risk a conservation violation.

**Key crates:** `t-minus`, `temporal-logic`, `spectral-clock`, `deadline-prop`

#### Layer 5: Proof-of-Concept — Musical Math

Musical math is the proof-of-concept layer, and it is the most strategically important layer for demonstration purposes. Here's why:

Music is the *simplest non-trivial testbed* for the entire stack. A piece of music has:
- Conservation: The total energy of a performance is bounded (you can't play louder than the instrument allows).
- Spectral structure: Harmonic analysis is literally spectral analysis. The eigenvalues of a musical system are its resonant frequencies.
- Categorical composition: Musical phrases compose associatively. A → B → C is well-defined.
- Temporal coordination: Musical time is precise, structured, and hierarchical (beat → measure → phrase → section → movement).
- Self-improvement: A musician practices, gets feedback, and improves. The Self-Improving Band (SIA²) is a musician that practices mathematically.

When the Self-Improving Band performs, it is not just making music. It is demonstrating that:
1. The conservation laws hold under adversarial conditions (improvisation pushes against the budget).
2. The spectral coordination works in real-time (ensemble synchronization).
3. The categorical composition produces correct outputs under time pressure.
4. The temporal logic handles syncopation, rubato, and tempo changes without violating invariants.
5. The self-improvement loop closes: the band gets better at playing, which means the underlying engine got better at coordinating.

A successful live performance by the Self-Improving Band is proof that the entire stack works. It is not a toy demo — it is a formal verification with aesthetic output.

**Key crates:** `musical-math`, `sia-band`, `harmonic-conservation`, `rhythm-logic`

### 1.3 The Self-Improvement Loop Closes the System

The SIA (Self-Improving Agent) is not a separate component bolted on top. It is the recursive closure of the system:

```
SIA watches fleet performance (via spectral-fleet eigenvalues)
  → identifies weakest eigenmode (spectral gap analysis)
  → generates improvement candidates (via categorical-agents composition)
  → validates against conservation laws (γ + H = C budget check)
  → schedules deployment (via t-minus temporal coordination)
  → measures improvement (via wasserstein-agents: Wasserstein distance between before/after distributions)
  → the measured improvement feeds back into the watch phase
```

This loop is not metaphorical. Each arrow is a crate call. Each step produces a verifiable artifact. The loop terminates only when the Wasserstein distance between consecutive iterations falls below a threshold — which, by the conservation law, it must, because entropy production cannot be negative.

The system is *self-improving by construction*. It's not that we hope it improves. It's that the mathematical structure guarantees improvement until the system reaches a fixed point, and the conservation laws guarantee that fixed point exists.

### 1.4 The Fork Integrations Are Not Tactical — They're Architectural

The integrations with external tools (baml, aider, dify, BMAD) serve a specific purpose: they are the *surface area* where the mathematical stack meets the software engineering world.

- **baml:** The boundary between natural language specifications and formal constraints. BAML provides the LLM-side parsing; constraint-dsl provides the formal semantics.
- **aider:** The interface where AI-assisted code generation meets categorical composition. Aider generates code; categorical-agents verifies that the generated code composes correctly.
- **dify:** The workflow orchestration layer where non-mathematical users interact with the system. Dify workflows are compiled down to categorical compositions internally.
- **BMAD:** The multi-agent decision framework. BMAD's decision trees are enriched with spectral-fleet information so that decisions are made with full fleet awareness.

These are not "we use these tools." These are "these tools are the API surface of our mathematical stack."

### 1.5 The Remaining Pieces

The components not yet mentioned fill specific architectural roles:

- **Tropical geometry:** Provides the semi-ring structure for combining constraints. Tropical addition (min/max) and tropical multiplication (addition) give a natural algebra for optimization over the constraint DSL.
- **Geometric algebra (Clifford algebra):** The language for representing rotations, reflections, and multi-dimensional quantities in agent state space. Essential for robotics-adjacent applications where agents manipulate spatial quantities.
- **Persistent homology:** The topological analysis of fleet state. When the fleet's state space has "holes" (regions of configuration space that no agent occupies), persistent homology detects them and quantifies their significance. This is the fleet's self-diagnostic: "we have a coverage gap in this region."
- **Optimal transport (Wasserstein distances):** The metric for measuring how far the fleet is from its target configuration. Unlike Euclidean distance, Wasserstein distance respects the geometry of the distribution — it measures the "cost" of transporting the fleet from where it is to where it wants to be.
- **Lattice cryptography:** The trust and identity layer. Agent identity certificates are lattice-based (resistant to quantum attack), and the trust graph is a lattice in the algebraic sense, enabling efficient trust propagation.
- **Symplectic optimization:** Optimization that preserves the symplectic structure of Hamiltonian dynamics. This is how we optimize agent trajectories through state space without violating the conservation laws (which are, structurally, a Hamiltonian constraint).
- **Agent identity/trust/handshake:** The security layer, built on lattice cryptography. Agents prove identity, establish trust, and negotiate capabilities via a handshake protocol that is itself a categorical construction (a pullback in the category of trust graphs).
- **Fleet management:** The operational layer. Fleet-warden manages agent lifecycles, using spectral-fleet for coordination, t-minus for scheduling, and entropy-conservation for resource budgets.

### 1.6 Summary of the Convergence

The 300+ repos are not a bag of independent projects. They are:

| Layer | Function | Mathematical Foundation |
|-------|----------|------------------------|
| Physics | Conservation invariant | γ + H = C |
| Coordination | Real-time fleet state | Spectral graph theory |
| Composition | Guaranteed correctness | Category theory |
| Timing | Temporal logic enforcement | Linear temporal logic |
| Proof | Music as formal verification | Harmonic analysis + all above |
| Security | Identity and trust | Lattice cryptography + categorical pullbacks |
| Optimization | Trajectory planning | Symplectic geometry + optimal transport |
| Self-improvement | Recursive system closure | SIA² loop with Wasserstein convergence |

One system. One mathematical stack. One architectural vision.

---

## 2. Phase 4 — Production Hardening

### 2.1 The Gap Between Research and Production

The current state of the ecosystem is research-grade. The math is sound, the implementations are correct (by construction, in many cases), and the tests pass. But "research-grade" and "production-grade" are different regimes. Production means:

- **API stability:** External consumers depend on your interfaces not breaking.
- **Performance guarantees:** Not "it works" but "it works in ≤2ms at P99."
- **Observability:** When something goes wrong at 3 AM, you need to know what and why without reading source code.
- **Cross-platform:** Not just Linux x86_64 but macOS ARM, Windows, WASM, and potentially embedded targets.
- **Documentation:** Not README.md files with "TODO: document this" but actual API docs with examples.

Phase 4 is the transition from "mathematically correct" to "industrially reliable." This is unglamorous, essential work.

### 2.2 API Stability

**Semver enforcement:** Every crate must have an explicit versioning policy. For crates below v1.0, the policy must state which changes are breaking and provide migration notes. For crates at v1.0+, semver is enforced mechanically: breaking API changes require a major version bump.

**Deprecation policy:** Deprecated APIs must be annotated with `#[deprecated(since = "x.y.z", note = "...")]` and must remain functional for at least one major version cycle. The deprecation note must link to the replacement API and a migration guide.

**Feature flags:** Every crate must use feature flags to separate:
- `std` vs `no_std` (for embedded targets)
- `full` vs `minimal` (for dependency-constrained environments)
- `experimental` (for APIs that are published but not yet stable)

**Minimum Supported Rust Version (MSRV):** Each crate must declare its MSRV and test against it in CI. Changes that bump the MSRV are semver-minor at minimum.

### 2.3 FFI Bindings

The mathematical stack is implemented in Rust for correctness and performance. But the users of this stack will not all be Rust developers. FFI bindings are the bridge.

**Python via PyO3:** Priority #1. The ML/data science community lives in Python. Every crate in the priority list (Section 2.7) must have PyO3 bindings with:
- Type stubs for IDE autocomplete
- NumPy integration for array-heavy crates (spectral-fleet, wasserstein-agents, harmonic-conservation)
- Async support via PyO3's async features for crates with async APIs (t-minus, fleet-warden)
- Comprehensive docstrings (not just `/// See Rust docs`)

**JavaScript/WASM:** Priority #2. The web dashboard (Phase 5) needs client-side computation. Key crates compile to WASM:
- `spectral-fleet` (for real-time fleet visualization)
- `constraint-dsl` (for in-browser constraint editing)
- `musical-math` (for the Self-Improving Band web demo)
- `entropy-conservation` (for budget visualization)

**C FFI:** Priority #3. For integration with legacy systems, embedded targets, and language runtimes that speak C. The C FFI layer should be auto-generated via `cbindgen` with hand-written header documentation.

### 2.4 Observability

**Metrics (via `metrics` crate facade):** Every crate must emit:
- Operation counters (how many times each public API is called)
- Latency histograms (time for key operations)
- Gauge metrics (current fleet size, current spectral gap, current entropy budget)

**Tracing (via `tracing` crate):** Every crate must instrument:
- Entry/exit from public API functions (at DEBUG level)
- Conservation law checks (at TRACE level for success, WARN for near-violation, ERROR for violation)
- Spectral decomposition steps (at TRACE level)
- Categorical composition chains (at DEBUG level)

**Structured logging:** All log output must be structured (JSON) in production mode, human-readable in development mode. The `tracing-subscriber` configuration must support both via feature flags.

**Conservation audit log:** A dedicated append-only log that records every conservation law check, its result, and the agent state at the time. This is the system's flight data recorder — when something goes wrong, this log is the primary diagnostic tool.

### 2.5 Benchmarking

**criterion.rs for every crate:** Performance is a correctness property in real-time systems. Every crate must have criterion benchmarks for:
- Public API hot paths
- Incremental update operations (spectral decomposition, constraint satisfaction)
- Memory allocation patterns (no unexpected allocations in hot paths)

**Benchmark CI:** Benchmarks run on every PR. A regression beyond 10% on any benchmark blocks merge. The threshold is configurable per benchmark (some operations are expected to vary more than others).

**Benchmark publishing:** Benchmark results are published to a dashboard (Phase 5) so that performance trends are visible over time. This is how we catch slow drift — the kind where each PR is within threshold but the cumulative effect over 100 PRs is catastrophic.

### 2.6 CI/CD Hardening

**Cross-platform testing:** Every merge must pass on:
- Linux x86_64 (Ubuntu 22.04, Ubuntu 24.04)
- macOS ARM (Apple Silicon)
- macOS x86_64 (Intel Macs)
- Windows x86_64 (MSVC toolchain)

**Cross-architecture:** For crates targeting embedded:
- ARMv7 (Cortex-M4, common in IoT)
- RISC-V ( emerging embedded target)
- WASM (via wasm-pack test)

**Fuzz testing:** Key crates (entropy-conservation, spectral-fleet, categorical-agents) must have fuzz targets. The conservation law crate especially — it is the invariant enforcement point, and fuzzing it is how we find edge cases in invariant checking.

**Property-based testing (via `proptest`):** Every crate must have property tests that verify:
- Conservation laws hold under random inputs
- Categorical composition is associative
- Spectral decompositions satisfy expected properties (eigenvalues are non-negative for positive semi-definite matrices, Fiedler vector is orthogonal to the all-ones vector)

**Release automation:** Tagged releases trigger automated:
- Crate publication to crates.io
- Docker image builds for the unified runtime (Phase 5)
- NPM package publication for WASM bindings
- PyPI package publication for Python bindings

### 2.7 Priority Crate Matrix — The Top 20

Not all crates are equal. The following 20 crates are highest priority for production hardening, ranked by their position in the dependency stack and their external impact:

| # | Crate | Priority Rationale |
|---|-------|--------------------|
| 1 | `entropy-conservation` | The invariant. Everything depends on this being bulletproof. A bug here is a system-wide correctness failure. |
| 2 | `spectral-fleet` | The coordination engine. Every fleet operation flows through this. Performance is critical — eigenvalue decomposition must be fast. |
| 3 | `t-minus` | The temporal engine. Every coordinated action depends on correct temporal logic. Edge cases in temporal logic are famously subtle. |
| 4 | `categorical-agents` | The composition engine. If composition is wrong, nothing built on top can be trusted. Associativity and identity laws must be mechanically verified. |
| 5 | `constraint-dsl` | The user-facing language. API stability is paramount — user-written constraints must not break across versions. |
| 6 | `fleet-warden` | The operational runtime. This is what ops teams interact with. It must be reliable, observable, and debuggable. |
| 7 | `wasserstein-agents` | The improvement metric. Self-improvement depends on accurate distance measurement. Numerical stability is the key concern. |
| 8 | `musical-math` | The demo/showcase. Must be rock-solid for live performances. Has unique real-time constraints (audio buffer deadlines are hard real-time). |
| 9 | `sia-band` | The Self-Improving Band. Combines musical-math with the self-improvement loop. Must demonstrate the loop closing convincingly. |
| 10 | `laplacian-update` | Incremental Laplacian decomposition. Performance-critical inner loop of spectral-fleet. Must be benchmarked to microsecond precision. |
| 11 | `fiedler-cluster` | Fleet clustering. Used by fleet-warden for sub-team formation. Correctness of clustering affects all downstream coordination. |
| 12 | `temporal-logic` | The LTL engine under t-minus. Must handle all standard LTL operators correctly. Property testing is essential. |
| 13 | `lattice-identity` | Agent identity and authentication. Security-critical. Must be audited, fuzzed, and tested against known attack vectors. |
| 14 | `trust-handshake` | The trust establishment protocol. Network-level security. Must be tested under adversarial network conditions. |
| 15 | `tropical-constraints` | Tropical algebra for constraint optimization. Numerical edge cases in tropical arithmetic (addition-as-min creates non-smooth landscapes). |
| 16 | `geometric-algebra` | Multi-dimensional state representation. Used by spatial applications. Numerical precision in high-dimensional rotors is the concern. |
| 17 | `persistent-homology` | Topological fleet diagnostics. Computational cost is the concern — persistent homology on large point clouds is expensive. |
| 18 | `symplectic-opt` | Symplectic optimization. Must preserve symplectic structure to machine precision. Symplectic integrators have known failure modes. |
| 19 | `spectral-clock` | Logical clock with spectral timestamps. Must maintain consistency under network partitions (akin to CRDT consistency proofs). |
| 20 | `harmonic-conservation` | Conservation law for harmonic systems. Bridges musical-math and entropy-conservation. Must demonstrate that musical constraints are a strict specialization of the general conservation law. |

### 2.8 Phase 4 Timeline Estimate

Production hardening of these 20 crates is estimated at:

- **Months 1-3:** Crate 1-5 (foundation layer). API audits, test coverage, benchmark establishment.
- **Months 3-5:** Crate 6-9 (operational layer). Fleet-warden hardening, musical-math real-time guarantees.
- **Months 5-7:** Crate 10-14 (inner loop + security). Performance optimization, security audit.
- **Months 7-9:** Crate 15-20 (specialized layer). Numerical precision, computational cost optimization.

Running in parallel: FFI bindings (starting month 2), CI/CD hardening (starting month 1), documentation (continuous).

---

## 3. Phase 5 — Integration & Platform

### 3.1 The Unified Agent Runtime

The current state is one-binary-per-crate. This is fine for development and testing, but production deployments need a single unified binary that combines:

- `fleet-warden` (agent lifecycle management)
- `t-minus` (temporal coordination)
- `spectral-fleet` (coordination state)
- `entropy-conservation` (budget enforcement)

into one process with one configuration file, one observability stack, and one deployment artifact.

**Architecture:** The unified runtime is a tokio-based async binary with a plugin system. Core services (conservation enforcement, spectral decomposition, temporal logic) run as tokio tasks communicating via channels. Plugins register capabilities (e.g., "I can process musical constraints" or "I can perform lattice-based authentication").

**Configuration:** A single TOML/YAML file:
```toml
[runtime]
conservation_budget = 1000.0
spectral_update_interval_ms = 100
temporal_logic_strictness = "strict"  # strict | relaxed | permissive

[fleet]
max_agents = 10000
cluster_algorithm = "fiedler"
trust_model = "lattice-pki"

[plugins]
enabled = ["musical-math", "wasserstein-agents", "persistent-homology"]
```

**Hot reload:** Configuration changes are applied without restart where possible (e.g., adding a plugin, adjusting conservation budget). Changes that require restart (e.g., changing the trust model) are flagged and deferred to a t-minus coordinated restart window.

### 3.2 Plugin System

**Plugin interface:** A plugin is a Rust dynamic library (`.so`/`.dylib`/`.dll`) that implements the `SuperInstancePlugin` trait:

```rust
pub trait SuperInstancePlugin: Send + Sync {
    fn name(&self) -> &str;
    fn version(&self) -> &str;
    fn initialize(&mut self, ctx: &PluginContext) -> Result<(), PluginError>;
    fn capabilities(&self) -> Vec<Capability>;
    fn handle_event(&mut self, event: &FleetEvent) -> Result<Vec<Action>, PluginError>;
    fn shutdown(&mut self) -> Result<(), PluginError>;
}
```

**PluginContext** provides access to:
- The spectral-fleet state (read-only snapshot)
- The conservation budget (read-only, with request mechanism for budget changes)
- The temporal scheduler (for scheduling plugin-initiated actions)
- The categorical composition engine (for composing plugin actions with fleet actions)

**Capability negotiation:** Plugins declare capabilities. The runtime matches capabilities to fleet needs. If a fleet task requires musical constraint processing and no plugin provides it, the task is rejected with a clear error message.

**Plugin isolation:** Plugins run in their own tokio task with a budget of CPU time and memory. A misbehaving plugin cannot starve the core runtime. If a plugin exceeds its budget, it's throttled; if it violates conservation laws through its actions, those actions are rejected.

**WASM plugins:** For sandboxed execution (e.g., user-submitted plugins), the runtime also supports WASM-based plugins via wasmtime. These have stricter resource limits but provide strong isolation guarantees.

### 3.3 Web Dashboard

**Tech stack:** React frontend + our WASM crates for client-side computation. The dashboard is not just a viewer — it's an interactive control surface.

**Key views:**

1. **Fleet topology:** Real-time visualization of the agent graph, colored by spectral cluster. Edge thickness shows trust strength. Nodes pulse with their current entropy production rate. The Fiedler vector is visualized as a color gradient.

2. **Conservation budget:** A live gauge showing γ, H, and C. History graph of conservation law checks. Alert when the system is approaching budget limits.

3. **Temporal timeline:** A Gantt-chart view of temporal constraints. Shows which agents are active, which are waiting, and which are approaching deadlines. The t-minus schedule is interactive — operators can drag deadlines and see the cascading effects.

4. **Self-improvement monitor:** Shows the Wasserstein distance between fleet states over time. When the SIA loop is running, this view shows the loop closing in real-time — each iteration bringing the fleet closer to the target state.

5. **Musical performance:** When the Self-Improving Band is active, a dedicated view shows the musical performance with overlaid conservation law checks and spectral decomposition state. This is the demo view — the one you show to investors, customers, and conference audiences.

**Real-time transport:** The dashboard communicates with the runtime via WebSocket. State updates are pushed, not polled. The WASM crates handle client-side computation (spectral decomposition visualization, constraint validation) so the server isn't a bottleneck.

### 3.4 CLI Tool

**Name:** `si` (SuperInstance). Built with `clap`, wrapping all operations.

```bash
# Fleet management
si fleet status                    # Show fleet state, spectral gap, conservation budget
si fleet scale --agents 100        # Scale fleet to 100 agents
si fleet deploy --config prod.toml # Deploy with configuration

# Temporal coordination
si schedule list                   # List all scheduled tasks
si schedule cancel <task-id>       # Cancel a task
si schedule inspect <task-id>      # Show temporal constraints for a task

# Conservation
si budget status                   # Show current γ, H, C
si budget history --last 1h        # Show conservation history
si budget audit <agent-id>         # Show conservation audit log for agent

# Spectral
si spectral clusters               # Show current Fiedler clusters
si spectral gap                    # Show current spectral gap
si spectral inspect --eigenvalues  # Show full eigenvalue spectrum

# Self-improvement
si sia status                      # Show SIA loop state
si sia run --iterations 10         # Run 10 SIA iterations
si sia report                      # Generate improvement report

# Musical
si band perform --duration 5m      # 5-minute performance
si band practice --focus harmony   # Focus practice on harmonic constraints
si band status                     # Show band improvement history
```

The CLI is the power-user interface. The dashboard is the visual interface. Both talk to the same API gateway.

### 3.5 API Gateway

**Protocols:**

- **REST:** Standard CRUD operations, health checks, configuration management. OpenAPI spec auto-generated.
- **gRPC:** High-performance fleet operations. Protobuf definitions for all fleet messages. Used for inter-service communication and performance-sensitive clients.
- **WebSocket:** Real-time state streaming. Used by the web dashboard and any client that needs live fleet state.

**Authentication:** Lattice-based agent identity (from `lattice-identity`). Each API client presents a lattice certificate. The gateway verifies the certificate, establishes a trust level, and enforces capability-based access control.

**Rate limiting:** Conservation-aware. API calls that increase entropy production are rate-limited based on the current conservation budget. When the system is running cool (low H), rate limits are relaxed. When running hot, rate limits tighten automatically. This is not a configuration parameter — it's a mathematical consequence of the conservation law.

### 3.6 The Self-Improving Band as the Demo

The Self-Improving Band is the centerpiece demo because it is simultaneously:
- A musical performance (aesthetically compelling)
- A formal verification (mathematically rigorous)
- A live demonstration of self-improvement (the band improves during the performance)
- A stress test of the entire stack (real-time constraints, conservation enforcement, spectral coordination)

**Demo flow:**
1. Start with a naive musical agent (random notes within key).
2. The SIA loop runs, identifying harmonic weaknesses via spectral gap analysis.
3. Improvement candidates are generated (better chord voicings, smoother voice leading).
4. Each improvement is validated against the conservation budget (you can't add infinite complexity).
5. Valid improvements are deployed mid-performance.
6. The audience hears the performance improve in real-time.
7. The dashboard shows the mathematical machinery operating behind the scenes.

This is the demo that no competitor can replicate, because no competitor has the mathematical stack that makes it possible.

---

## 4. Phase 6 — The Self-Improvement Engine

### 4.1 The Loop In Detail

Phase 6 is the system's ultimate state: a self-improving agent fleet where the improvement process is itself governed by the mathematical stack. The SIA² (Self-Improving Agent, squared — the agent improves itself improving itself) loop operates as follows:

#### Step 1: Watch — SIA Observes Its Own Performance

The SIA monitors the fleet via `spectral-fleet`. Specifically, it tracks:
- The eigenvalue spectrum of the fleet Laplacian over time
- The rate of change of each eigenvalue (eigenvalue velocity)
- The conservation budget utilization (γ and H over time)
- The Wasserstein distance between the current fleet state and the target state

This is not passive observation. The SIA maintains a *spectral state model* — a prediction of what the eigenvalue spectrum should look like under normal operation. Deviations from this model are anomalies that trigger investigation.

The spectral state model is itself a categorical construction: it's a functor from the category of fleet states to the category of spectral models. Natural transformations between models represent regime changes (e.g., the fleet transitioning from "exploration mode" to "exploitation mode").

#### Step 2: Identify — Spectral Gap Analysis

The SIA identifies the *weakest eigenmode* — the eigenmode whose eigenvalue has the highest velocity in the wrong direction (increasing entropy, decreasing coordination). This eigenmode is the fleet's weakest link.

Why eigenmode-level rather than agent-level? Because:
- An agent appearing weak might be the victim of poor coordination with its neighbors, not a problem with the agent itself.
- The eigenmode captures the multi-agent interaction that is the actual source of the problem.
- Fixing an eigenmode fixes all agents in that mode simultaneously.

The spectral gap analysis uses `persistent-homology` to identify *persistent* weaknesses (ones that survive across time) versus *transient* weaknesses (ones that appear and disappear). Only persistent weaknesses are candidates for systemic improvement.

#### Step 3: Generate — Categorical Composition of Improvements

The SIA generates improvement candidates using `categorical-agents`. Each candidate is a morphism from the current fleet state to a proposed improved state. The generation process:

1. **Decompose the problem:** The weak eigenmode is decomposed into its constituent agent interactions (via the eigenvector).
2. **Search the morphism space:** For each problematic interaction, search for morphisms (in the categorical sense) that improve it. The search space is the cospan completion of the category of agent transformations.
3. **Compose candidates:** Individual morphisms are composed (via categorical composition) into fleet-wide improvement candidates. Associativity of composition guarantees that the order of composition doesn't matter — all orders produce the same candidate.
4. **Rank candidates:** Candidates are ranked by expected improvement (measured in projected Wasserstein distance reduction) and conservation cost (how much budget the improvement consumes).

#### Step 4: Validate — Conservation Law Check

Each candidate is validated against the conservation law γ + H = C. Specifically:
- Does the proposed improvement increase entropy H? If so, is there sufficient spectral gap γ to compensate?
- Does the proposed improvement decrease the spectral gap? If so, is the fleet still above the critical threshold for stable coordination?
- Is the total conservation budget respected after the improvement?

Candidates that violate the conservation law are rejected. This is not a soft preference — it's a hard constraint. The conservation law is the system's physical law, and violating it would be as nonsensical as a perpetual motion machine.

The validation also checks *second-order effects*: does the improvement, by changing the fleet's state, cause any other conservation check to fail? This is done by running the proposed improvement through the `constraint-dsl` and checking all constraints simultaneously.

#### Step 5: Deploy — t-minus Scheduled Rollout

Validated improvements are deployed via `t-minus`. The rollout is:
- **Gradual:** The improvement is applied to a small subset of agents first (a Fiedler cluster), then expanded.
- **Monitored:** The conservation budget and spectral gap are monitored continuously during rollout.
- **Reversible:** If any conservation violation is detected during rollout, the improvement is automatically rolled back via a t-minus compensating action.
- **Coordinated:** The rollout schedule is computed by t-minus to minimize disruption to ongoing fleet operations.

#### Step 6: Measure — Wasserstein Distance

After deployment, the SIA measures the improvement using `wasserstein-agents`. The Wasserstein distance between the pre-improvement fleet state distribution and the post-improvement fleet state distribution quantifies the improvement.

Wasserstein distance is used rather than simpler metrics (e.g., Euclidean distance, KL divergence) because:
- It respects the geometry of the fleet state space (agents that are "close" in capability space should have low transport cost).
- It handles distributions with different support (the post-improvement fleet might have different agents than the pre-improvement fleet).
- It has a natural interpretation: it's the "cost" of transforming the old fleet into the new fleet.

If the measured improvement matches the predicted improvement (within tolerance), the SIA's spectral state model is reinforced. If it doesn't match, the model is updated — and this update is itself a learning signal.

#### Step 7: Close the Loop

The measured improvement feeds back into Step 1. The SIA now watches the improved fleet, looking for the next weakest eigenmode. But the SIA itself has also been updated — its spectral state model is more accurate, its morphism search is more targeted, and its conservation predictions are more precise.

This is the "squared" in SIA²: the agent improves the fleet, and the improvement process improves the agent. The loop is:

```
Watch → Identify → Generate → Validate → Deploy → Measure → Watch
  ↑                                                        |
  └──────────── Improvement of the improvement ────────────┘
```

### 4.2 Convergence Guarantees

The conservation law guarantees that this loop converges. Here's the argument:

1. Each iteration of the SIA loop either improves the fleet (decreases Wasserstein distance to target) or does nothing (if no valid improvement candidate exists).
2. The Wasserstein distance is bounded below by 0 (it's a metric).
3. Therefore, the sequence of Wasserstein distances is a monotonically decreasing sequence bounded below, hence convergent.

The fixed point of convergence is the fleet state where no valid improvement candidate exists — meaning every eigenmode is as strong as it can be given the conservation budget. This is the fleet's *Pareto optimal* state: you can't improve any eigenmode without worsening another.

### 4.3 Safety Guarantees

The conservation law doesn't just guarantee convergence — it guarantees safety:

- **No runaway improvement:** The conservation budget caps the total amount of change per iteration. The fleet can't improve so fast that it becomes unstable.
- **No degradation masquerading as improvement:** If an "improvement" actually worsens the fleet (e.g., by creating a conservation violation), it's caught in Step 4 and never deployed.
- **Graceful degradation under resource pressure:** If the conservation budget is tight (high entropy, low spectral gap), the SIA automatically becomes more conservative — proposing smaller, safer improvements. Under extreme pressure, it proposes no improvements at all, which is correct behavior.

### 4.4 The Self-Improvement Engine as a Product

The self-improvement engine is not just a research result — it's a product. Customers don't buy "category theory" or "spectral graph theory." They buy a system that *automatically improves itself* with *mathematical guarantees* on the improvement.

The pitch: "Your agent fleet gets better over time. Not through manual tuning. Not through heuristic parameter sweeps. Through mathematically guaranteed optimization that respects hard constraints. We can prove it works, and we can prove it's safe."

No competitor can currently make this claim. Not because they lack the engineering talent, but because they lack the mathematical foundations.

---

## 5. Competitive Landscape

### 5.1 Hugging Face

**What they have:** The dominant model hub. Transformers, diffusers, datasets. An enormous community. Hub-and-spoke model distribution with versioning and reproducibility. The `transformers` library is the de facto standard for ML model inference.

**What they lack:** Any notion of multi-agent coordination, mathematical guarantees on agent behavior, or formal verification. Their `transformers.agents` module is a thin wrapper around single-model tool use. There is no fleet concept, no conservation law, no spectral coordination.

**Where we differentiate:** Hugging Face provides the models. We provide the *orchestration layer* with mathematical guarantees. A Hugging Face model is an agent in our fleet. We can use their models as components while providing the coordination, safety, and self-improvement that their platform doesn't.

**Strategic position:** Complementary, not competitive. We should target integration with Hugging Face models as first-class agent capabilities in our runtime.

### 5.2 LangChain / LangGraph

**What they have:** The most widely adopted agent framework. LangGraph provides graph-based agent workflows with persistence, human-in-the-loop, and streaming. Massive developer adoption. Good documentation. Simple mental model (graph = workflow).

**What they lack:** Mathematical rigor. LangGraph's "graph" is an informal notion — a directed graph with conditional edges, not a mathematically structured object. There are no spectral properties, no conservation laws, no categorical composition guarantees. The system is built on engineering heuristics, not mathematical foundations.

The critical limitation: **LangGraph cannot provide guarantees on agent behavior.** If an agent loop diverges, the best they can do is set a maximum iteration count. If agents conflict, the best they can do is sequential execution with retry. These are engineering patches, not solutions.

**Where we differentiate:** We provide what LangChain can't: mathematical guarantees. Our agents don't diverge (conservation law). Our agents don't conflict (categorical composition). Our agents don't deadlock (temporal logic verification). These aren't features — they're properties of the mathematical structure.

**Strategic risk:** LangChain's developer experience is excellent. Our mathematical rigor comes at the cost of conceptual complexity. We must invest heavily in making the complexity invisible to developers who just want "agents that work."

### 5.3 Anthropic

**What they have:** State-of-the-art models (Claude series). Constitutional AI as a safety framework. Tool use, multi-turn reasoning, strong alignment research. The Model Context Protocol (MCP) for agent-tool integration.

**What they lack:** Multi-agent fleet coordination. Constitutional AI is a single-agent alignment technique — it constrains what one model does, not what a fleet of models does collectively. MCP connects agents to tools, but doesn't coordinate fleets.

Anthropic's approach to safety is fundamentally different from ours: they train models to be safe (behavioral safety), while we build mathematical structures that guarantee safety (structural safety). These are complementary approaches, but structural safety has a critical advantage: it's verifiable. You can formally verify that γ + H = C holds. You cannot formally verify that a model won't produce harmful output — you can only test it empirically.

**Where we differentiate:** Multi-agent safety with mathematical guarantees. Anthropic ensures one agent is safe. We ensure a fleet of agents is safe *collectively* — that their interactions don't produce emergent unsafe behavior.

**Strategic position:** Anthropic is a potential model provider (Claude as an agent in our fleet) and a potential research partner (combining behavioral and structural safety).

### 5.4 OpenAI

**What they have:** The dominant model provider. GPT series, DALL-E, Whisper. The Assistants API for persistent agents. The Realtime API for voice. The Agents SDK. Massive distribution and brand recognition.

**What they lack:** Mathematical foundations for agent coordination. The Assistants API is a single-agent abstraction — each assistant operates independently. The Agents SDK adds multi-agent orchestration but via Python-level control flow, not mathematical structure. There are no guarantees on multi-agent behavior.

OpenAI's scaling philosophy ("just make the model bigger") is fundamentally at odds with our approach. We believe that intelligence emerges from the *structure of coordination*, not the size of the model. A fleet of small, well-coordinated agents will outperform a single large model on complex tasks, because the fleet can decompose the task, specialize, and compose results — which is exactly what our mathematical stack enables.

**Where we differentiate:** Scale through coordination, not through model size. We make 10 small agents do the work of 1 giant model, with mathematical guarantees on correctness and efficiency.

**Strategic risk:** OpenAI has the distribution. If they decide to add mathematical coordination to their Agents SDK (which is architecturally possible), they have the developer mindshare to dominate. Our window is the time before they realize they need math.

### 5.5 Google DeepMind

**What they have:** The deepest research bench. Gemini models. AlphaFold, AlphaGo, AlphaGeometry — they've demonstrated that mathematical reasoning is achievable. Gemini's multi-modal capabilities are state-of-the-art. They have experience with large-scale agent systems (AlphaStar, Game-playing agents).

**What they lack:** The specific combination of mathematical structures we've assembled. DeepMind has produced brilliant work in individual areas (category theory for program synthesis, spectral methods for graph learning, etc.), but they haven't *composed* these into a unified agent framework. Their research is deep but siloed.

**Where we differentiate:** We have the unified stack. DeepMind has individual components that are, in isolation, more mature than ours. But they don't have the composition — they don't have conservation laws feeding into spectral methods feeding into category theory feeding into temporal logic feeding into self-improvement. We do.

**Strategic position:** DeepMind is the most credible threat, because they have the talent and the research depth to build something similar. Our advantage is focus: we are building this specific system, while DeepMind is exploring many directions. The question is whether we can reach production before DeepMind decides this is a priority.

### 5.6 The Differentiation Thesis

Our differentiation is not "better engineering" or "more features." It is a *qualitative* difference: **we provide mathematical guarantees on agent behavior.** No amount of engineering can substitute for this. You cannot test your way to a guarantee. You cannot scale your way to a guarantee. You need the math.

The guarantees we provide:
1. **Conservation guarantee:** Agent actions respect the entropy budget. Always.
2. **Coordination guarantee:** Fleet convergence is bounded by the spectral gap. Always.
3. **Composition guarantee:** Agent compositions are correct. Always. (By categorical construction.)
4. **Temporal guarantee:** Temporal constraints are satisfied. Always. (By LTL verification.)
5. **Improvement guarantee:** The self-improvement loop converges. Always. (By monotone convergence.)
6. **Safety guarantee:** Improvements cannot degrade the fleet. Always. (By conservation law validation.)

These guarantees compose. The conservation guarantee + the coordination guarantee = guaranteed coordination within the entropy budget. The composition guarantee + the temporal guarantee = guaranteed correct temporal behavior. The improvement guarantee + the safety guarantee = guaranteed safe self-improvement.

This composability of guarantees is itself a consequence of the categorical structure: guarantees are morphisms, and categorical composition preserves them.

**No competitor has this.** Not today. The race is to production before someone else figures out that math is the moat.

---

## Appendix: Priority Crate Matrix

### Dependency Graph (Simplified)

```
entropy-conservation ──┐
                       ├── spectral-fleet ──┐
spectral-gap ──────────┘                    ├── fleet-warden
                       ├── t-minus ─────────┤
temporal-logic ────────┘                    ├── categorical-agents ── constraint-dsl
                                            │
                       ├── wasserstein-agents│
optimal-transport ─────┘                    │
                                            ├── sia-band ── musical-math
lattice-identity ──────┐                    │
                       ├── trust-handshake ─┤
tropical-constraints ──┘                    │
                                            │
geometric-algebra ─────┐                    │
                       ├── symplectic-opt ──┤
persistent-homology ───┘                    │
                                            │
                                   spectral-clock ── deadline-prop
                                   laplacian-update ── fiedler-cluster
                                   harmonic-conservation
```

### Production Hardening Checklist Template

For each priority crate:

- [ ] API audit: All public items documented, no unnamed parameters
- [ ] Semver policy: Declared in Cargo.toml `[package]` section
- [ ] MSRV: Declared and CI-tested
- [ ] Feature flags: `std`, `full`, `experimental` at minimum
- [ ] Deprecation annotations: All deprecated items annotated with migration notes
- [ ] Test coverage: ≥90% line coverage for public API
- [ ] Property tests: Conservation/categorical/temporal properties verified
- [ ] Fuzz targets: For security-critical and invariant-enforcing crates
- [ ] Benchmarks: criterion.rs for all public API hot paths
- [ ] Python bindings: PyO3 with type stubs and docstrings
- [ ] WASM bindings: For visualization and client-side crates
- [ ] Observability: Metrics, tracing, and structured logging integrated
- [ ] CI: Cross-platform (Linux, macOS, Windows) + cross-arch where applicable
- [ ] Examples: At least 3 usage examples per crate
- [ ] Migration guide: For any API changes from current state

---

*This document is a living artifact. As the system evolves through Phases 4-6, this roadmap should be updated to reflect learnings, pivots, and discoveries. The convergence argument, however, is structural — it will not change. The math is the math.*

---

**End of AGI Convergence Roadmap v0.1**
