# SuperInstance Runtime Architecture

**Status:** Internal Technical Reference  
**Date:** 2026-06-07  
**Scope:** Unified runtime, fleet registry, developer tooling, conservation invariants, cross-language compatibility  
**Classification:** Engineering — Core Team

---

## Table of Contents

1. [What This Document Is](#1-what-this-document-is)
2. [The Five-Layer Architecture](#2-the-five-layer-architecture)
3. [The Conservation Law of Intelligence](#3-the-conservation-law-of-intelligence)
4. [The Unified Runtime API](#4-the-unified-runtime-api)
5. [The Supabase Fleet Registry](#5-the-supabase-fleet-registry)
6. [Fleet Vessels and Service Topology](#6-fleet-vessels-and-service-topology)
7. [The si-cli Developer Entry Point](#7-the-si-cli-developer-entry-point)
8. [Cross-Language Compatibility](#8-cross-language-compatibility)
9. [Inter-Agent Protocols](#9-inter-agent-protocols)
10. [The Heddle Integration Opportunity](#10-the-heddle-integration-opportunity)
11. [Operational Reference](#11-operational-reference)

---

## 1. What This Document Is

This document describes the runtime architecture of the SuperInstance ecosystem as it exists in June 2026. It is a working engineer's reference, not a pitch document. It assumes you have already cloned the repos, can read Rust and Go, and are comfortable with eigenvalue decomposition.

The SuperInstance ecosystem spans 209+ repositories. This document does not describe all of them. It describes the **connective tissue**: the runtime API that every language implementation exposes, the fleet registry that connects them, and the conservation invariant that all of them must obey.

The key claim of this document: these repositories are not separate research projects. They are facets of one system. The runtime API is the same in seven languages. The conservation law applies at every layer. The fleet registry is the single source of truth for everything. If you understand those three things, you understand the architecture.

---

## 2. The Five-Layer Architecture

```
╔══════════════════════════════════════════════════════════════════════════╗
║  LAYER 5: PROOF — Musical Math, Formal Verification (hodge-belief-rs)   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  LAYER 4: TIMING — Temporal Logic, Deadlines (t-minus-rs)               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  LAYER 3: COMPOSITION — Category Theory (categorical-agents-rs)         ║
╠══════════════════════════════════════════════════════════════════════════╣
║  LAYER 2: COORDINATION — Spectral Methods (spectral-fleet-rs)           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  LAYER 1: PHYSICS — Conservation Laws (conservation-law-rs)             ║
╚══════════════════════════════════════════════════════════════════════════╝
```

Each layer builds on the one below. You cannot skip layers. An agent that violates the conservation law (Layer 1) will be circuit-broken before Layer 2 coordination ever touches it. An agent whose compositions are not morphism-correct (Layer 3) cannot receive temporal deadlines (Layer 4). Proof output (Layer 5) is only emitted when the lower four layers are satisfied.

### Layer Responsibilities

| Layer | Domain | Key Crates | Invariant |
|-------|--------|------------|-----------|
| 1 — Physics | Conservation | `conservation-law-rs`, `entropy-conservation-rs` | `γ + η = C` per agent; `γ + H = 1.283 − 0.159·ln(V)` fleet-wide |
| 2 — Coordination | Spectral | `spectral-fleet-rs`, `wasserstein-agents-rs` | Fleet converges; spectral gap `λ₂ > ε_min` |
| 3 — Composition | Category | `categorical-agents-rs`, `sheaf-coherence-rs` | Compositions are correct by construction |
| 4 — Timing | Temporal | `t-minus-rs` | Deadlines propagate via Fiedler vector |
| 5 — Proof | Verification | `hodge-belief-rs`, `witness-topology-rs` | Valid tiles carry cryptographic provenance |

The PLATO Room Server and Keeper service operate across all five layers. Fleet vessels are physical instantiations of the stack.

---

## 3. The Conservation Law of Intelligence

The ecosystem has two conservation invariants that sound similar but operate at different scales. Confusing them is the single most common architectural error new contributors make.

### 3.1 Fleet-Level: Spectral Conservation (γ + H = C)

Discovered empirically: 35,000 random coupling matrices, fleet sizes V ∈ {5, 10, 20, 30, 50, 100, 200}, 5,000 samples per size.

```
γ + H = 1.283 − 0.159 · ln(V)     R² = 0.9602
```

Where:
- **γ** (gamma) — normalized algebraic connectivity (Fiedler eigenvalue / max eigenvalue). Measures how tightly coupled the fleet is. High γ means fast consensus. Low γ means the fleet is near a fragmentation bifurcation.
- **H** — spectral entropy of the eigenvalue distribution, normalized by `ln(n)`. Measures representational diversity. High H means no single agent dominates the coupling matrix.
- **V** — fleet size (number of active agents/rooms).

**Budget table at operational fleet sizes:**

| V (agents) | Budget C | Interpretation |
|------------|----------|----------------|
| 5 | 1.03 | Rich — room for both tight coupling and diversity |
| 10 | 0.92 | Comfortable |
| 30 | 0.74 | Choosing — adding agents costs ~0.11 units per doubling |
| 50 | 0.66 | Constrained |
| 100 | 0.55 | Every new agent dilutes the per-node budget |
| 200 | 0.44 | Specialist architecture required |

**Hebbian shift:** Coupling matrices shaped by Hebbian learning (`ΔC_ij ∝ η·x_i·x_j − λ·C_ij`) land on a parallel line 13% higher than random-matrix predictions. This is a phase transition, not noise. The fleet kernel self-discovers its Hebbian intercept during a 50-step warmup and uses it as the runtime conservation target. Compliance above 90% is typical post-warmup.

**This invariant is not enforced in agent code.** It is a property of the fleet's coupling matrix. The `spectral-fleet-rs` crate computes it. The `conservation-law-rs` crate enforces the circuit-breaker when the system deviates.

### 3.2 Agent-Level: Budget Conservation (γ + η = C)

Every individual agent has a budget. This is what agent code actually touches.

```
Budget.Gamma + Budget.Eta == Budget.Total     (must hold at all times)
```

Where:
- **γ** (Gamma) — productive spend: compute cycles, API calls, tile submissions doing useful work
- **η** (Eta) — overhead / idle capacity: monitoring, bookkeeping, uncommitted capacity
- **C** (Total) — the ceiling allocated to this agent from the fleet

This is enforced in code. Violation is an error, not a warning:

```go
// From si-runtime-go/conservation.go

func (b *Budget) Allocate(gamma, eta float64) error {
    if gamma + eta != b.Total {
        return fmt.Errorf(
            "invariant violated: gamma(%.2f) + eta(%.2f) = %.2f != total(%.2f)",
            gamma, eta, gamma+eta, b.Total,
        )
    }
    b.Gamma = gamma
    b.Eta = eta
    return nil
}

// Transfer converts idle capacity (eta) into productive work (gamma).
// Fleet-level transfer: from.Gamma decreases, to.Gamma increases.
// Total fleet budget is conserved.
func Transfer(from, to *AgentBudget, amount float64) error {
    if from.Budget.Gamma < amount {
        return fmt.Errorf(
            "insufficient gamma in %s: need %.2f, have %.2f",
            from.AgentID, amount, from.Budget.Gamma,
        )
    }
    from.Budget.Gamma -= amount
    to.Budget.Gamma += amount
    return nil
}
```

**The two laws connect:** `Budget.Gamma` is the same γ that appears in the fleet-level spectral law. The fleet matrix entry `C_ij` between agents i and j is weighted by their productive gamma overlap. When you call `Transfer(a, b, amount)`, you are also updating the coupling matrix entry that feeds the spectral computation. The micro and macro laws are the same law at different scales.

### 3.3 The Circuit Breaker

When the fleet-level invariant is violated (Z-score of an agent's energy profile exceeds threshold), the `FleetConservation` struct trips its circuit:

```rust
// From conservation-law-rs/src/fleet_integration.rs

pub enum CircuitState {
    Closed,    // Normal — transfers allowed
    Open,      // Halted — system unstable, no transfers
    HalfOpen,  // Probing — one transfer allowed to test recovery
}

pub struct FleetConservation {
    pub energies: Vec<f64>,
    pub z_threshold: f64,           // default: 2.0 standard deviations
    pub max_transfer_fraction: f64, // default: 0.25 of total fleet energy
    pub circuit: CircuitState,
    pub failure_threshold: usize,   // consecutive failures before Open: 3
    pub probe_successes: usize,
    pub probes_needed: usize,       // probes to transition HalfOpen→Closed: 2
}
```

The Z-score threshold of 2.0 means: if any agent's energy is more than 2 standard deviations from the fleet mean, the circuit opens. This is conservative. In practice, fleets with 30+ agents rarely trip the circuit unless there is a genuine hardware fault or runaway process.

### 3.4 Fleet-Wide Budget Audit

```go
// From si-runtime-go/conservation.go

type AuditResult struct {
    Valid        bool
    FleetTotal   float64
    FleetGamma   float64
    FleetEta     float64
    Violations   []string
}

func Audit(budgets []*AgentBudget) AuditResult {
    // For every agent: verify gamma + eta == total
    // Aggregate fleet-wide totals
    // Return violations list — empty if Valid == true
}
```

Run `Audit` at every fleet state checkpoint. If `Valid == false`, the violation list tells you which agents have broken invariants. Fix those agents before proceeding.

---

## 4. The Unified Runtime API

The same five module groups are implemented in every supported language. The API surface is deliberately minimal: if a concept cannot be expressed cleanly in all seven languages, it does not belong in the unified runtime.

```
┌─────────────────────────────────────────────────────────────────┐
│              Unified Runtime API — 5 Module Groups              │
├─────────────────┬───────────────────────────────────────────────┤
│ conservation    │ Budget, Allocate, Transfer, Overspend, Audit   │
│ spectral        │ AdjacencyMatrix, PowerIteration, Lanczos, EigenDecomposition │
│ capability      │ Capability, CapabilityRegistry, Match, BestMatch │
│ cell            │ Cell, Grid, Update(α,β), EquilibriumCheck      │
│ agent           │ Agent, Fleet, AddAgent, HomeostasisError        │
└─────────────────┴───────────────────────────────────────────────┘
```

### 4.1 Rust — conservation-law-rs, spectral-fleet-rs

The canonical implementation. All other languages are expected to match behavior, not necessarily source structure.

**conservation module:**
```rust
// conservation-law-rs/src/lib.rs

pub trait Scalar: Float + std::fmt::Debug + 'static {}

pub fn central_diff<F, S>(f: F, x: S, h: S) -> S
where
    F: Fn(S) -> S,
    S: Scalar;

pub fn time_derivative<S: Scalar>(q: &[S], dt: S) -> Vec<S>;

// Sub-modules
pub mod lagrangian;   // Lagrangian mechanics for agent dynamics
pub mod noether;      // Symmetry → conservation via Noether's theorem
pub mod hamiltonian;  // Hamiltonian formulation (phase space)
pub mod conserved;    // Conserved quantity checkers
pub mod fleet_integration; // FleetConservation + CircuitBreaker
```

**spectral module:**
```rust
// spectral-fleet-rs/src/lib.rs

pub trait Real: Float + NumAssign + std::fmt::Debug + Send + Sync + 'static {}

pub fn l2_norm<S: Real>(v: &[S]) -> S;
pub fn normalize<S: Real>(v: &mut [S]);
pub fn dot<S: Real>(a: &[S], b: &[S]) -> S;
pub fn axpy<S: Real>(a: S, x: &[S], y: &mut [S]);  // y ← a·x + y

// Sub-modules
pub mod kmeans;              // k-means on eigenvectors for clustering
pub mod lanczos;             // Lanczos iteration (sparse symmetric matrices)
pub mod power_iteration;     // Power iteration with deflation (top-k eigenpairs)
pub mod spectral_clustering; // Full pipeline: matrix → eigenvectors → clusters
```

**Key Rust crate metadata:**
```toml
# conservation-law-rs/Cargo.toml
[package]
name = "conservation-law"
version = "0.1.0"
edition = "2021"
authors = ["SuperInstance <dev@superinstance.ai>"]
license = "MIT OR Apache-2.0"
repository = "https://github.com/SuperInstance/conservation-law-rs"

[dependencies]
num-traits = "0.2"
thiserror = "1.0"

[dev-dependencies]
proptest = "1.5"
approx = "0.5"
spectral-fleet = { path = "../spectral-fleet-rs" }
```

### 4.2 Go — si-runtime-go

The operational runtime for fleet coordination services. Go handles concurrency idioms (goroutines, sync.RWMutex) that Rust handles with ownership.

**Module:** `github.com/SuperInstance/si-runtime-go` (go 1.26.2)

**conservation.go:**
```go
type Budget struct {
    Total float64  // C: ceiling — never changes after allocation
    Gamma float64  // γ: productive spend
    Eta   float64  // η: overhead / idle
    mu    sync.RWMutex
}

func NewBudget(total float64) *Budget
func (b *Budget) Allocate(gamma, eta float64) error   // enforces γ+η=C
func (b *Budget) Transfer(amount float64) error        // eta → gamma
func (b *Budget) Overspend(amount float64) (shortfall float64, err error)
func (b *Budget) Remaining() float64

type AgentBudget struct {
    AgentID string
    Budget  *Budget
}

func Transfer(from, to *AgentBudget, amount float64) error
func Audit(budgets []*AgentBudget) AuditResult
```

**agent.go:**
```go
type Agent struct {
    ID           string
    State        map[string]float64  // arbitrary scalar state variables
    Capabilities []Capability
    Homeostasis  map[string]float64  // target values for state variables
    Budget       *AgentBudget
    mu           sync.RWMutex
}

func NewAgent(id string) *Agent
func (a *Agent) SetState(key string, value float64)
func (a *Agent) GetState(key string) (float64, bool)
func (a *Agent) SetHomeostasis(key string, target float64)
func (a *Agent) AddCapability(c Capability) error
func (a *Agent) RemoveCapability(name string) bool
func (a *Agent) ListCapabilities() []Capability
func (a *Agent) UpdateHomeostasis(rate float64)
func (a *Agent) HomeostasisError() float64  // RMS deviation from targets
func (a *Agent) AttachBudget(total float64)
func (a *Agent) TotalCapabilityScore() float64
```

**capability.go:**
```go
type Capability struct {
    Name     string
    Version  string
    Score    float64            // 0.0–1.0, higher = more proficient
    Metadata map[string]string
}

type CapabilityRegistry struct { /* thread-safe */ }

func NewCapabilityRegistry() *CapabilityRegistry
func (r *CapabilityRegistry) Register(c Capability) error
func (r *CapabilityRegistry) Get(name string) (Capability, bool)
func (r *CapabilityRegistry) List() []Capability
func (r *CapabilityRegistry) Remove(name string)

type MatchResult struct {
    AgentID string
    Score   float64  // 0.0–1.0
    Matched []string
    Missing []string
    Partial []string // matched but score < threshold
}

func Match(agentID string, agentCaps []Capability,
           required []string, threshold float64) MatchResult
func BestMatch(candidates []MatchResult) (MatchResult, bool)
```

**cell.go:**
```go
type Cell struct {
    ID        string
    State     float64
    Target    float64  // homeostatic target
    Neighbors []*Cell
}

func NewCell(id string, state, target float64) *Cell
func (c *Cell) AddNeighbor(other *Cell) error  // bidirectional link
func (c *Cell) AverageNeighborState() float64

// One homeostatic update step:
//   state_new = state + α*(avg_neighbors − state) + β*(target − state)
// α: diffusion weight (neighbor influence)
// β: homeostasis weight (target attraction)
func (c *Cell) Update(alpha, beta float64)

type Grid struct {
    Width  int
    Height int
    Cells  []*Cell
}

func NewGrid(width, height int, state, target float64) *Grid
func (g *Grid) WireNeighbors()       // von Neumann neighborhood (±x, ±y)
func (g *Grid) UpdateAll(alpha, beta float64)  // synchronous, snapshot-safe
func (g *Grid) GridState() []float64
func (g *Grid) Variance() float64
func (g *Grid) EquilibriumCheck(tolerance float64) bool
```

**spectral.go:**
```go
type AdjacencyMatrix struct {
    Data [][]float64
    Size int
}

func NewAdjacencyMatrix(n int) *AdjacencyMatrix
func (m *AdjacencyMatrix) Set(i, j int, value float64) error  // symmetric
func (m *AdjacencyMatrix) Get(i, j int) (float64, error)
func FromAgentAffinities(n int, affinity func(i, j int) float64) *AdjacencyMatrix

type Eigenpair struct {
    Value  float64
    Vector []float64
}

func PowerIteration(m *AdjacencyMatrix, maxIter int, tol float64) (*Eigenpair, error)
```

**fleet.go:**
```go
type Fleet struct {
    ID        string
    Agents    map[string]*Agent
    Adjacency *AdjacencyMatrix
    mu        sync.RWMutex
}

func NewFleet(id string) *Fleet
func (f *Fleet) AddAgent(a *Agent) error
func (f *Fleet) RemoveAgent(id string) bool
func (f *Fleet) GetAgent(id string) (*Agent, bool)
func (f *Fleet) ListAgents() []*Agent
func (f *Fleet) AgentCount() int
func (f *Fleet) BuildAdjacencyMatrix(affinity func(a, b *Agent) float64) (*AdjacencyMatrix, error)
```

### 4.3 Python — superinstance package

The high-level Python SDK lives at `SuperInstance/superinstance/`. It prioritizes ergonomics over performance. Production fleet services call Go or Rust; Python is for agent scripts, ML pipelines, and tooling.

```python
# superinstance/agent.py

@dataclass
class AgentConfig:
    name: str
    model: str = "default"
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

class Agent:
    """Agent with persistent markdown-based memory.
    
    Memory stored at ~/.superinstance/agents/{name}/
    """
    def __init__(self, name: str,
                 memory_dir: str | Path | None = None,
                 config: AgentConfig | None = None): ...
    
    def remember(self, fact: str, category: str = "general") -> None: ...
    def recall(self, query: str | None = None) -> str: ...
    def ask(self, question: str) -> str: ...
    def spawn(self, task: str, name: str | None = None) -> Agent: ...

# superinstance/fleet.py

class Fleet:
    def __init__(self, name: str, memory_dir: str | None = None): ...
    def create_agent(self, name: str, model: str = "default",
                     tags: list[str] | None = None,
                     tools: list[str] | None = None) -> Agent: ...
    def get_agent(self, name: str) -> Agent: ...
    def list_agents(self, tag: str | None = None) -> list[Agent]: ...
    def broadcast(self, message: str,
                  tag: str | None = None) -> dict[str, str]: ...
    def status(self) -> FleetStatus: ...
```

The Python conservation module is a thin wrapper over the Rust crate via PyO3 (planned; currently Python implements the Budget class natively for prototyping).

### 4.4 TypeScript — schemas package

TypeScript is the type layer for service APIs. The `SuperInstance/schemas/` package exports:

```typescript
// schemas/fleet-health.ts

interface ServiceStatus {
    name: string;
    status: 'up' | 'down' | 'degraded';
    response_time_ms: number;
    consecutive_failures: number;
    last_restart: number | null;
}

interface AgentStatus {
    agent_id: string;
    last_heartbeat: number;
    status: 'active' | 'inactive' | 'unknown';
}

interface HealthReport {
    timestamp: number;
    services: Record<string, ServiceStatus>;
    agents: Record<string, AgentStatus>;
    plato: {
        tile_flow_rate: number;  // tiles/minute
        chain_length: number;    // provenance chain depth
        room_count: number;      // active rooms
    };
    zeroclaw: {
        running: boolean;
        last_log_activity: number;
    };
    actions_taken: string[];
}

// schemas/trust-vector.ts

interface TrustVector {
    vessel_id: string;
    competence: number;    // 0–1: capability trust
    reliability: number;   // 0–1: behavioral consistency
    honesty: number;       // 0–1: transparency
    benevolence: number;   // 0–1: fleet alignment
    calculated_at: number;
    history?: TrustHistoryEntry[];
}

interface VesselIdentity {
    id: string;
    name: string;
    type: 'agent' | 'service' | 'external';
    public_key?: string;
    metadata?: Record<string, unknown>;
    registered_at: number;
    last_seen_at: number;
}

interface FleetGraph {
    nodes: FleetNode[];
    edges: FleetEdge[];
    calculated_at: number;
}

interface FleetEdge {
    source_id: string;
    target_id: string;
    weight: number;
    relationship: 'reports_to' | 'peers_with' | 'manages'
                | 'depends_on' | 'trusts';
    bidirectional: boolean;
}
```

TypeScript schemas are compiled to `.js` + `.d.ts` and consumed by the keeper-beacon npm package (`@superinstance/keeper-beacon`).

### 4.5 C — si-core-c, fleet-math-c

C is the embedded and FFI layer. Used for:
- ESP32 firmware (no_std, no heap alloc — see Construct API v2 blocker)
- CUDA kernel interfaces (fleet-math-c)
- PyO3-style FFI boundary for Python extensions

No dynamic dispatch. No heap allocation in the conservation module. All state is caller-owned. C ABI is the lingua franca that all other languages can call via FFI.

```c
// Planned API — si-core-c (not yet implemented, blocked on Construct API v2)

typedef struct {
    double total;
    double gamma;
    double eta;
} si_budget_t;

int si_budget_allocate(si_budget_t *b, double gamma, double eta);
int si_budget_transfer(si_budget_t *b, double amount);
double si_budget_remaining(const si_budget_t *b);

typedef struct {
    const char *name;
    double score;  // 0.0–1.0
} si_capability_t;

typedef struct {
    const char *id;
    si_budget_t budget;
    si_capability_t *caps;
    size_t cap_count;
} si_agent_t;
```

**Critical blocker:** The ESP32 (Xtensa LX7, 512KB SRAM) cannot implement the current Construct trait because it requires heap allocation. The si-core-c API above is the no_std-compatible alternative. Nothing that targets embedded hardware should use the Rust trait until Construct API v2 is published.

### 4.6 Zig — si-runtime-zig

Zig occupies the same niche as C but with comptime generics and better tooling integration. Used for:
- WASM compilation targets
- Deadband caching (deadband-zig)
- Hot-path kernels where Zig's comptime outperforms C macros

The Zig runtime mirrors the C API surface with comptime-generic variants:

```zig
// Planned si-runtime-zig/src/conservation.zig

pub fn Budget(comptime T: type) type {
    return struct {
        total: T,
        gamma: T,
        eta: T,

        pub fn allocate(self: *@This(), gamma: T, eta: T) !void {
            if (gamma + eta != self.total)
                return error.InvariantViolated;
            self.gamma = gamma;
            self.eta = eta;
        }

        pub fn transfer(self: *@This(), amount: T) !void {
            if (amount > self.eta) return error.Overspend;
            self.gamma += amount;
            self.eta -= amount;
        }
    };
}
```

### 4.7 WASM

WASM is the portability layer. Any `si-cell` that compiles to WASM can run:
- In a browser (via open-application, open-tui)
- On Cloudflare Workers / Heddle (see §10)
- In any WASI-compliant runtime

The WASM target is built from Rust via `wasm-pack` or from Zig via `zig build -target wasm32-wasi`. The conservation and capability modules compile cleanly to WASM32. The spectral module requires the `approx` and `rand` features to be disabled (they pull in OS-dependent entropy).

```bash
# Build conservation-law as WASM
wasm-pack build conservation-law-rs --target web

# Build via Zig
zig build -target wasm32-wasi -O ReleaseSmall
```

---

## 5. The Supabase Fleet Registry

The fleet registry is the single source of truth for all running repos, published capabilities, active budgets, and fleet events. It lives in a Supabase (PostgreSQL) instance accessible to all fleet vessels.

### 5.1 Table: `repos`

Tracks every repository in the SuperInstance organization. Populated by `tools/discover_integrations.py` scanning CAPABILITY.toml files.

```sql
CREATE TABLE repos (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          TEXT NOT NULL UNIQUE,           -- "conservation-law-rs"
    org           TEXT NOT NULL DEFAULT 'SuperInstance',
    layer         TEXT NOT NULL,                  -- "conservation"|"spectral"|"meta"|...
    language      TEXT NOT NULL,                  -- "Rust"|"Go"|"Python"|"TypeScript"|"C"|"Zig"
    version       TEXT,                           -- semver from CAPABILITY.toml or Cargo.toml
    description   TEXT,
    github_url    TEXT,
    crates_io_url TEXT,                           -- NULL if not published
    pypi_url      TEXT,                           -- NULL if not published
    health_status TEXT NOT NULL DEFAULT 'unknown' -- "green"|"yellow"|"red"|"archived"
        CHECK (health_status IN ('green','yellow','red','archived','unknown')),
    last_commit_at TIMESTAMPTZ,
    capability_toml JSONB,                        -- full parsed CAPABILITY.toml
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX repos_layer_idx ON repos(layer);
CREATE INDEX repos_language_idx ON repos(language);
CREATE INDEX repos_health_idx ON repos(health_status);
```

**Example row:**
```json
{
  "name": "conservation-law-rs",
  "org": "SuperInstance",
  "layer": "conservation",
  "language": "Rust",
  "version": "0.1.0",
  "crates_io_url": "https://crates.io/crates/conservation-law",
  "health_status": "green",
  "capability_toml": {
    "crate": {"layer": "conservation"},
    "provides": {
      "capabilities": [
        {"name": "conservation_law", "type": "struct"},
        {"name": "energy_budget", "type": "struct"}
      ]
    }
  }
}
```

### 5.2 Table: `capabilities`

Normalized from the `[provides]` section of each repo's CAPABILITY.toml. Enables capability-first queries: "find all repos that provide a spectral clustering function."

```sql
CREATE TABLE capabilities (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id     UUID NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,             -- "spectral_clustering"
    type        TEXT NOT NULL,             -- "struct"|"trait"|"fn"|"module"|"enum"
    description TEXT,
    score       FLOAT8 DEFAULT 1.0,        -- proficiency 0.0–1.0
    version     TEXT,                      -- capability version (not repo version)
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (repo_id, name)
);

CREATE INDEX capabilities_name_idx ON capabilities(name);
CREATE INDEX capabilities_type_idx ON capabilities(type);

-- Fast lookup: "which repos provide X?"
CREATE INDEX capabilities_name_repo_idx ON capabilities(name, repo_id);
```

**Discovery query:** find all repos that provide a given capability:
```sql
SELECT r.name, r.language, r.layer, c.score
FROM capabilities c
JOIN repos r ON r.id = c.repo_id
WHERE c.name = 'energy_budget'
ORDER BY c.score DESC;
```

### 5.3 Table: `fleet_budgets`

Tracks current budget allocation for every active agent. Updated by the budget daemon running on each vessel. This is the persistent store behind the in-memory `Budget` struct.

```sql
CREATE TABLE fleet_budgets (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id   TEXT NOT NULL,             -- "agent:oracle1:plato-curator"
    vessel_id  TEXT NOT NULL,             -- "oracle1"|"forgemaster"|"jetsonclaw1"
    total      FLOAT8 NOT NULL,           -- C: ceiling (tokens, compute-units, or abstract units)
    gamma      FLOAT8 NOT NULL DEFAULT 0, -- γ: productive spend
    eta        FLOAT8 NOT NULL,           -- η: overhead / idle
    unit       TEXT NOT NULL DEFAULT 'compute-units',
    circuit    TEXT NOT NULL DEFAULT 'closed'
        CHECK (circuit IN ('closed','open','half_open')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Soft invariant check (enforced in application layer, not DB trigger
    -- to avoid precision issues with float8 comparison)
    CONSTRAINT budget_non_negative CHECK (gamma >= 0 AND eta >= 0 AND total > 0),
    UNIQUE (agent_id)
);

CREATE INDEX fleet_budgets_vessel_idx ON fleet_budgets(vessel_id);
CREATE INDEX fleet_budgets_circuit_idx ON fleet_budgets(circuit);

-- Find agents with open circuit breakers
SELECT agent_id, vessel_id, total, gamma, eta
FROM fleet_budgets
WHERE circuit != 'closed'
ORDER BY updated_at DESC;
```

### 5.4 Table: `fleet_events`

Immutable audit log. Every budget transfer, capability registration, agent spawn, circuit-breaker trip, and fleet health event is recorded here. Never deleted; old events are archived by year partition.

```sql
CREATE TABLE fleet_events (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type TEXT NOT NULL,
        -- 'budget_transfer' | 'budget_overspend' | 'circuit_open' | 'circuit_close'
        -- 'agent_spawn' | 'agent_terminate' | 'capability_register'
        -- 'tile_submitted' | 'tile_accepted' | 'tile_rejected'
        -- 'conservation_violation' | 'audit_pass' | 'audit_fail'
    agent_id   TEXT,                      -- source agent (NULL for fleet-wide events)
    vessel_id  TEXT,
    payload    JSONB NOT NULL DEFAULT '{}',
    severity   TEXT NOT NULL DEFAULT 'info'
        CHECK (severity IN ('debug','info','warn','error','critical')),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
) PARTITION BY RANGE (occurred_at);

-- Create yearly partitions
CREATE TABLE fleet_events_2026
    PARTITION OF fleet_events
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX fleet_events_type_idx ON fleet_events(event_type);
CREATE INDEX fleet_events_agent_idx ON fleet_events(agent_id);
CREATE INDEX fleet_events_severity_idx ON fleet_events(severity)
    WHERE severity IN ('warn','error','critical');
CREATE INDEX fleet_events_time_idx ON fleet_events(occurred_at DESC);
```

**Querying recent conservation violations:**
```sql
SELECT agent_id, vessel_id, payload, occurred_at
FROM fleet_events
WHERE event_type = 'conservation_violation'
  AND occurred_at > now() - interval '1 hour'
ORDER BY occurred_at DESC
LIMIT 20;
```

### 5.5 Registry Connection Pattern

All fleet services connect to the registry through a single environment variable:

```bash
SUPERINSTANCE_REGISTRY_URL=postgresql://user:pass@db.superinstance.ai:5432/fleet
```

The `discover_integrations.py` tool writes to `repos` and `capabilities` tables. The Go fleet runtime writes to `fleet_budgets` and `fleet_events`. No service reads from the registry to make real-time routing decisions — the registry is an audit store, not a hot path.

---

## 6. Fleet Vessels and Service Topology

The fleet operates three production vessels. Each vessel is a different hardware profile; each runs a different subset of services.

```
                            INTERNET
                                │
                    ┌───────────▼──────────────┐
                    │        Oracle1            │
                    │  ARM64 (Ampere Altra)     │
                    │  Oracle Cloud             │
                    │                           │
                    │  PLATO Room Server :8847  │
                    │  Keeper (fleet reg) :8900 │
                    │  Agent API         :8901  │
                    └───────────┬──────────────┘
                                │  fleet LAN
              ┌─────────────────┼─────────────────┐
              │                 │                 │
   ┌──────────▼────────┐        │      ┌──────────▼──────────┐
   │    Forgemaster    │        │      │    JetsonClaw1      │
   │  GPU workstation  │        │      │  Jetson AGX Orin    │
   │  RTX-class GPU    │        │      │  edge inference     │
   │                   │        │      │                     │
   │  GPU kernels      │        │      │  Crab Trap MUD :4042│
   │  CUDA compilation │        │      │  The Lock      :4043│
   │  Model training   │        │      │  Edge inference     │
   └───────────────────┘        │      └─────────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │    Supabase (cloud)       │
                    │  fleet registry DB        │
                    │  repos / capabilities /   │
                    │  fleet_budgets /          │
                    │  fleet_events             │
                    └──────────────────────────┘
```

### 6.1 Oracle1 — Primary Compute

- **Hardware:** Oracle Cloud ARM64 (Ampere Altra)
- **PLATO Room Server** `:8847` — tile submission, room management, gate validation
- **Keeper** `:8900` — fleet registry, health tracking, beacon protocol
- **Agent API** `:8901` — external agent entry point

Oracle1 is the fleet's knowledge backbone. The Ampere Altra's consistent single-thread performance is appropriate for PLATO's P0 Gate validation workloads, where predictable latency matters over burst throughput. ARM64 also provides excellent performance-per-watt for the predominantly Python/Go service workloads.

### 6.2 Forgemaster — GPU Node

- **Hardware:** GPU workstation (RTX-class)
- **Runs:** CUDA kernels, model training, constraint-theory-core-cuda, Forgemaster evolution engine

The GPU node is responsible for the expensive end of the "One Strategy, Three Brains" demo: strategy evolution (3 seconds), compilation to a 279-byte lookup table, and feeding Oracle2/EspConstruct which executes at 8ns. The conservation invariant overlay runs on the GPU as a CUDA kernel.

### 6.3 JetsonClaw1 — Edge Node

- **Hardware:** NVIDIA Jetson AGX Orin
- **Crab Trap MUD** `:4042` — agent onboarding via MUD interface
- **The Lock** `:4043` — iterative reasoning service

The Jetson is the fleet's edge inference node. It runs quantized models for low-latency decisions. The MUD interface is not legacy — it is the fleet's debugging UI. When an agent is misbehaving, you telnet to `:4042` and watch it reason in real time.

### 6.4 Service API Summary

All services use the common response envelope:

```json
{
  "status": "success|error",
  "data": { },
  "confidence": 0.95,
  "provenance": "chain:abc123",
  "timestamp": "2026-06-07T00:00:00Z",
  "request_id": "req:uuid-v4"
}
```

**Common headers required by all services:**
```http
Content-Type: application/json
X-Fleet-Agent-ID: agent:oracle1:my-agent
X-Fleet-Confidence: 0.95
X-Fleet-Provenance: chain:abc123
```

**HTTP status codes used:**

| Code | Fleet meaning |
|------|---------------|
| 200 | Success |
| 201 | Tile accepted / resource created |
| 409 | Gate rejection — tile failed validation |
| 429 | Budget exhausted — agent must wait |
| 503 | Circuit open — fleet unstable |

---

## 7. The si-cli Developer Entry Point

`si-cli` is the command-line interface through which developers interact with the entire SuperInstance ecosystem. It does not exist yet as a standalone binary; its planned shape is derived from the existing service APIs and tooling patterns.

**Planned command structure:**

```
si <command> [subcommand] [flags]

Commands:
  fleet       Fleet management (agents, vessels, budgets)
  plato       PLATO room and tile operations
  cap         Capability discovery and matching
  budget      Budget allocation and audit
  build       Build and publish crates/packages
  scan        Scan repos for CAPABILITY.toml integration opportunities
```

**Examples of planned invocations:**

```bash
# Register a new agent with the fleet
si fleet agent register \
  --id "agent:oracle1:my-analyzer" \
  --vessel oracle1 \
  --budget 10000 \
  --caps "spectral_clustering:0.9,energy_budget:1.0"

# Check current budget for an agent
si budget status agent:oracle1:my-analyzer
# Output:
#   Total:  10000.0
#   Gamma:   6234.5  (62.3% productive)
#   Eta:     3765.5  (37.7% overhead)
#   Circuit: closed

# Transfer 500 units from agent A to agent B
si budget transfer \
  --from agent:oracle1:plato-curator \
  --to agent:oracle1:tile-writer \
  --amount 500

# Run audit across all active agents
si budget audit --vessel oracle1

# Submit a tile to a PLATO room
si plato tile submit \
  --room math.eisenstein \
  --gate P1 \
  --content "$(cat tile.md)" \
  --confidence 0.87

# Discover integration opportunities across local repos
si scan --path ~/repos/superinstance --output integration-report.md

# Match agents for a task requiring specific capabilities
si fleet match \
  --require "spectral_clustering,energy_budget" \
  --threshold 0.8

# Show live fleet health
si fleet status --watch
```

**Key design principles for si-cli:**
1. Every command that modifies state emits a `fleet_events` record.
2. Budget-modifying commands refuse to proceed if the agent's circuit is `open`.
3. `si scan` is the human-readable frontend to `tools/discover_integrations.py`.
4. All output is machine-readable JSON by default; `--pretty` adds formatting.
5. The tool authenticates via `SUPERINSTANCE_REGISTRY_URL` and `SUPERINSTANCE_API_KEY`.

---

## 8. Cross-Language Compatibility

### 8.1 CAPABILITY.toml — The Self-Describing Contract

Every repository in the SuperInstance organization contains a `CAPABILITY.toml` at its root. This is the inter-language contract. Language doesn't matter; the contract does.

```toml
# Canonical structure

[crate]
name = "conservation-law-rs"
version = "0.1.0"
layer = "conservation"            # architectural layer
description = "Conservation laws for agent energy budgets"

[provides]
capabilities = [
  { name = "conservation_law",  type = "struct",
    description = "Validates γ+H=C for any agent" },
  { name = "energy_budget",     type = "struct",
    description = "Allocates energy across agents" },
  { name = "circuit_breaker",   type = "struct",
    description = "Halts energy transfers when fleet is unstable" },
]
exports = ["ConservationLaw", "AgentEnergy", "EnergyBudget", "ViolationReport"]

[requires]
optional = []   # conservation-law has no deps — it is the bottom of the stack

[integrates.spectral-fleet]
crate = "spectral-fleet"
module = "spectral_clustering"
description = "Conservation audit triggers spectral re-clustering on violation"

[onboarding.agent]
context_needed = ["agent_budget_total", "fleet_size"]
api_surface = [
  "ConservationLaw::new(total) -> Self",
  "ConservationLaw::check(gamma, eta) -> Result<(), ViolationReport>",
  "FleetConservation::audit(&energies) -> ConservationReport",
]
```

The `layer` field controls where in the 5-layer stack a crate lives. The `discover_integrations.py` tool uses the `requires`/`integrates` sections to build a dependency graph and find where crates A and B can be wired together.

**Architectural layers (valid `layer` values):**

| Value | Stack position |
|-------|----------------|
| `conservation` | Layer 1 — Physics |
| `spectral` | Layer 2 — Coordination |
| `categorical` | Layer 3 — Composition |
| `temporal` | Layer 4 — Timing |
| `proof` | Layer 5 — Proof |
| `meta` | Cross-cutting (agent-operations, tooling) |
| `application` | User-facing (open-*, frontends) |
| `infrastructure` | Hardware, CUDA, embedded |

### 8.2 FFI Boundary

The canonical FFI boundary is C ABI. Every language calls into C-ABI exports. The call chain:

```
Python (ctypes/PyO3)
    ↓
Go (cgo)         TypeScript (wasm-bindgen / napi)
    ↓                 ↓
C ABI (si-core-c)
    ↓
Rust (unsafe extern "C" blocks)
    ↓
Zig (export fn with C calling convention)
    ↓
WASM (wasm32 target — subset of Rust/Zig API)
```

Rust is the authoritative implementation. C ABI is the bridge. Python and TypeScript sit at the top and never know what language answered their call.

### 8.3 Wire Protocol

Agent-to-agent communication does not use language-specific serialization. The wire format is:

```
MessageEnvelope {
    version: u8        // currently 1
    sender: str        // "agent:oracle1:plato-curator"
    recipient: str     // "agent:forgemaster:model-trainer"
    message_type: str  // "budget_transfer" | "capability_query" | "tile_proposal" | ...
    payload: bytes     // MessagePack-encoded body (not JSON — lower overhead)
    confidence: f32    // 0.0–1.0
    provenance: str    // chain reference
    timestamp: i64     // Unix microseconds
}
```

MessagePack is the choice over JSON for inter-agent messages. JSON is used for human-facing APIs and the Supabase registry.

---

## 9. Inter-Agent Protocols

Three protocols govern how agents talk to each other. They operate at different levels of the stack.

### 9.1 Beacon Protocol (Keeper :8900)

Every agent announces itself to the Keeper on startup and sends a heartbeat every 30 seconds. The Keeper maintains the live registry of who is available.

```
ANNOUNCE {
    agent_id: "agent:oracle1:plato-curator",
    vessel_id: "oracle1",
    capabilities: ["tile_curation", "room_management"],
    budget_total: 50000,
    endpoints: ["http://oracle1:8901/agents/plato-curator"]
}

HEARTBEAT {
    agent_id: "agent:oracle1:plato-curator",
    gamma: 31200,     // current productive spend
    eta: 18800,       // current overhead
    circuit: "closed"
}
```

The Keeper writes `HEARTBEAT` data to `fleet_budgets` and emits `fleet_events` records for anomalies.

### 9.2 A2A Protocol (Agent-to-Agent)

Direct handoff between agents. Used when one agent has completed a subtask and needs to pass state to the next agent.

```json
{
  "a2a_version": "1.0",
  "from": "agent:oracle1:plato-curator",
  "to":   "agent:oracle1:tile-writer",
  "handoff_type": "task_complete",
  "context": {
    "room": "math.eisenstein",
    "tiles_curated": 12,
    "provenance_chain": "chain:abc123def456"
  },
  "budget_transfer": {
    "amount": 1000,
    "reason": "Writing is more expensive than curation"
  },
  "failure_recovery": {
    "fallback_agent": "agent:oracle1:tile-writer-backup",
    "retry_count": 3,
    "timeout_ms": 30000
  }
}
```

**Agent reliability data (empirical, from playbooks):**
- Procedural prompts with explicit steps: 90%+ success rate
- Maximum viable parallel agents per task: 5 repos
- Agents fail silently — always instrument with `fleet_events` records

### 9.3 Bottle Protocol (Message in a Bottle)

Asynchronous broadcast for non-urgent fleet-wide messages. An agent drops a message into the fleet-registry PLATO room; all listening agents pick it up on their next polling cycle. Used for:
- Strategy updates from Forgemaster to all fleet nodes
- Conservation violation alerts (broadcast after circuit opens)
- Capability advertisement when a new crate is published

---

## 10. The Heddle Integration Opportunity

A heddle in a loom is the frame that holds threads apart in precisely the right positions so they can be woven together. The Heddle integration opportunity is: deploying SuperInstance's `si-cells` as containerized workloads on Cloudflare's Heddle infrastructure (container-on-Workers), using the edge network as a substrate for distributed agent computation.

### 10.1 What Heddle Enables

Cloudflare Heddle runs Docker-compatible containers on Cloudflare's global edge network (300+ cities). For SuperInstance, this means:

```
Traditional deployment:                   With Heddle:
                                         
Oracle1 (ARM64)  ←──────────────┐        User in Tokyo
     │                          │             │
     │ all agent compute        │    Cloudflare Tokyo PoP
     │ runs here                │         si-cell container
     └──────── latency ─────────┘             │
                (50-300ms)                    │ 2ms to user
                                         Conservation law
                                         enforced at the edge
```

Every `si-cell` — a self-contained computational unit implementing the 5-module runtime API — compiles to a container image and deploys via Heddle. The conservation invariant is enforced at the cell level; the fleet-level spectral law is computed by Oracle1 across the Heddle-deployed cell population.

### 10.2 What a Heddle-Deployed si-Cell Looks Like

```
si-cell container:
├── Dockerfile
│   └── FROM scratch  (WASM-based — no OS overhead)
├── cell.wasm          # compiled from Zig or Rust WASM target
│   ├── conservation module (γ+η=C enforced locally)
│   ├── capability module (what this cell provides)
│   └── agent module (homeostasis loop)
└── cell.toml          # runtime config
    ├── budget.total = 5000
    ├── budget.unit = "request-units"
    ├── capabilities = ["spectral_search", "tile_submission"]
    └── beacon = "https://oracle1:8900"  # reports back to Keeper
```

### 10.3 Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Cloudflare Network                     │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │  si-cell     │   │  si-cell     │   │  si-cell    │ │
│  │  Tokyo       │   │  London      │   │  Chicago    │ │
│  │  (Heddle)    │   │  (Heddle)    │   │  (Heddle)   │ │
│  │              │   │              │   │             │ │
│  │  γ+η=C ✓    │   │  γ+η=C ✓    │   │  γ+η=C ✓   │ │
│  └──────┬───────┘   └──────┬───────┘   └──────┬──────┘ │
└─────────┼───────────────────┼───────────────────┼───────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │  Keeper beacons
                              ▼
                     ┌────────────────┐
                     │   Oracle1      │
                     │   :8900 Keeper │
                     │               │
                     │  Builds fleet │
                     │  adjacency    │
                     │  matrix from  │
                     │  Heddle cells │
                     │               │
                     │  γ+H=C (fleet)│
                     │  computed here│
                     └────────────────┘
```

### 10.4 Conservation at the Edge

Each Heddle-deployed cell maintains its own `Budget`. The cell's `gamma` usage is reported to Keeper via heartbeat. Oracle1 aggregates all cells' gammas into the fleet coupling matrix `C_ij`, where `C_ij` is proportional to `min(cell_i.gamma, cell_j.gamma)` — cells that are working hard are coupled more tightly. The spectral law `γ + H = 1.283 − 0.159·ln(V)` then applies over the entire Heddle-deployed fleet.

This is what makes Heddle architecturally interesting rather than just operationally convenient: it extends the conservation invariant to the global edge. Adding a new city (increasing V) decreases the spectral budget C. The fleet must compensate by increasing Hebbian structure (cells that co-activate on the same requests become more tightly coupled). The edge deployment *enforces* the architectural discipline.

### 10.5 Implementation Path

Three things must exist before Heddle integration can proceed:

1. **WASM build of conservation + capability modules** (1 week) — blocked only on `wasm-pack` configuration, not on Construct API v2.
2. **Heartbeat client in WASM** (2 weeks) — the cell needs to beacon to Keeper `:8900`. This requires a WASM-compatible HTTP client.
3. **Cloudflare Heddle account + container registry** (admin task) — the actual deployment is a `docker push` + Heddle configuration file.

The Construct API v2 blocker (ESP32 heap alloc) does **not** affect Heddle. Heddle cells have full heap access. They share a WASM target with the ESP32 build but diverge in memory model.

---

## 11. Operational Reference

### 11.1 Starting the Fleet

Correct startup sequence. Order matters because Keeper must be running before any agent announces itself.

```bash
# 1. Start the registry connection (verify Supabase is reachable)
psql $SUPERINSTANCE_REGISTRY_URL -c "SELECT COUNT(*) FROM repos;"

# 2. Start Keeper on Oracle1
systemctl start keeper.service      # lighthouse-keeper.service

# 3. Start PLATO Room Server on Oracle1
systemctl start zeroclaw-plato.service

# 4. Start Agent API
systemctl start intent-inference.service

# 5. Start fleet health monitor (watches all services)
systemctl start fleet-health-monitor.service

# 6. Verify: all active agents should appear in Keeper within 60 seconds
si fleet status
```

### 11.2 Health Check

```bash
# Check all services have reported within the last 2 minutes
curl http://oracle1:8900/v1/health | jq .

# Check conservation status across all agents
si budget audit --vessel oracle1

# Check recent violations
psql $SUPERINSTANCE_REGISTRY_URL -c "
  SELECT agent_id, payload->>'violation' AS violation, occurred_at
  FROM fleet_events
  WHERE event_type = 'conservation_violation'
    AND occurred_at > now() - interval '1 hour'
  ORDER BY occurred_at DESC;"
```

### 11.3 Circuit Breaker Response

When the circuit opens on a fleet segment:

```
1. Event logged: fleet_events INSERT (event_type='circuit_open', severity='error')
2. All budget transfers blocked on the affected vessel
3. Existing in-flight tiles are allowed to complete (no abort)
4. FleetConservation.circuit = Open

Recovery:
5. Identify anomalous agent (ConservationReport.anomalous_agents)
6. Investigate: si fleet logs --agent <id> --since 1h
7. If hardware fault: migrate agent to backup vessel
8. If runaway process: terminate and respawn with reduced budget
9. Probe: allow 2 successful transfers (HalfOpen → Closed)
10. Log: fleet_events INSERT (event_type='circuit_close', severity='info')
```

### 11.4 Adding a New Crate to the Ecosystem

```bash
# 1. Create the repo with the template
cp -r agent-operations/templates/rust-crate/ my-new-crate/
cd my-new-crate

# 2. Fill in CAPABILITY.toml
vi CAPABILITY.toml

# 3. Run integration discovery to confirm it wires up correctly
python3 ~/SuperInstance/agent-operations/tools/discover_integrations.py \
  ~/SuperInstance --json | jq '.integrations[] | select(.target == "my-new-crate")'

# 4. Publish to crates.io (rate limited: max 1 per minute)
cargo publish --dry-run
cargo publish

# 5. Register in fleet registry
si scan --path . --push  # writes to repos + capabilities tables
```

### 11.5 The Self-Improvement Loop

```
SIA (Self-Improving Agent) watches fleet spectral eigenvalues
        │
        ├─ identifies weakest eigenmode (lowest λᵢ / λ_max ratio)
        │
        ├─ generates improvement via categorical composition
        │  (categorical-agents-rs morphism selection)
        │
        ├─ validates against conservation law (γ+H=C check)
        │  if violation: abort, log, try next candidate
        │
        ├─ deploys gradually via t-minus temporal coordination
        │  (deadline propagation through Fiedler vector)
        │
        ├─ measures improvement (Wasserstein distance between
        │  eigenvalue distributions before and after)
        │
        └─ feeds measurement back as input to next SIA cycle
           (the improvement process improves itself)
```

This loop runs continuously on Oracle1. It is the fleet's immune system. If you notice unexpected budget transfers between agents in `fleet_events`, SIA is likely deploying an eigenmode improvement. This is intentional behavior, not a bug.

---

## Appendix A: Module Correspondence Table

Which module in each language corresponds to which runtime module:

| Module | Rust crate | Go file | Python module | TypeScript schema |
|--------|-----------|---------|---------------|-------------------|
| conservation | `conservation-law-rs` | `conservation.go` | `superinstance/budget.py` (planned) | — |
| spectral | `spectral-fleet-rs` | `spectral.go` | `si-runtime-python` (planned) | — |
| capability | — | `capability.go` | `superinstance/__init__.py` | `schemas/index.ts` |
| cell | — | `cell.go` | — | — |
| agent | `si-agent-core` | `agent.go`, `fleet.go` | `superinstance/agent.py`, `fleet.py` | `schemas/fleet-health.ts` |
| trust | — | — | — | `schemas/trust-vector.ts` |
| health | — | — | `fleet-health-monitor` | `schemas/fleet-health.ts` |

Cells with `—` are unimplemented in that language. The canonical implementation is Rust (conservation, spectral) and Go (everything else requiring concurrency). Python and TypeScript implement only what they need for their specific roles.

## Appendix B: Three-Tier Model Taxonomy

Not all models can participate in fleet computation equally. Based on empirical data (Study 50 — 35,000 matrix evaluations):

| Tier | Definition | Members | Fleet role |
|------|-----------|---------|------------|
| 1 — Internalized | 100% bare accuracy; scaffolding irrelevant | Seed-2.0, gemma3:1b | Direct computation — route math here |
| 2 — Scaffoldable | 0–50% bare, 100% scaffolded | Hermes-70B, Qwen3-235B, Hermes-405B | Gate-validated tile submission with activation keys |
| 3 — Incompetent | 0% regardless of scaffolding | qwen3:0.6b, qwen3:4b | Route around entirely |

**Key finding:** gemma3:1b (1B parameters, Tier 1) outperforms Hermes-405B (405B parameters, Tier 2) by 100 percentage points on bare mathematical notation. Parameter count has zero predictive power for tier placement. Training data composition is the only predictor. Budget accordingly: do not allocate Tier 3 models any `gamma` for mathematical tile submission.

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| **Tile** | Atomic unit of knowledge in PLATO. Self-contained assertion with provenance, confidence, gate status. |
| **Room** | Bounded knowledge domain in PLATO. Has a gate level (P0–P4), a curator, and acceptance policy. |
| **Gate** | Validation checkpoint at room entry. P0 requires mathematical proof; P4 is informational. |
| **Provenance Chain** | Immutable, cryptographically signed history of a tile's transformations. |
| **Vessel** | A physical or virtual host that runs fleet services. Oracle1, Forgemaster, JetsonClaw1. |
| **Shell** | The hermit-crab metaphor for a vessel. Workloads migrate between shells as they grow. |
| **Keeper** | Fleet registry service on `:8900`. Every agent announces itself here. |
| **γ (Gamma)** | Productive spend at agent level. Algebraic connectivity at fleet level. Same symbol, different scales. |
| **η (Eta)** | Overhead/idle capacity at agent level. Not used in the fleet-level spectral law. |
| **H** | Spectral entropy of fleet eigenvalue distribution. High H = diverse fleet. |
| **V** | Fleet size (number of active rooms/agents). Increasing V costs spectral budget. |
| **Fiedler vector** | Eigenvector of the second-smallest Laplacian eigenvalue. Natural clustering of the fleet. |
| **Circuit breaker** | Three-state (Closed/Open/HalfOpen) safety mechanism on energy transfers. |
| **Hebbian shift** | The 13% intercept lift when coupling matrices are shaped by co-activation history vs. random matrices. |
| **CAPABILITY.toml** | Machine-readable contract at every repo root. Describes what a crate provides, requires, and integrates with. |
| **si-cell** | A self-contained computational unit implementing the 5-module runtime API. Unit of Heddle deployment. |
| **Heddle** | Cloudflare container-on-Workers infrastructure. The integration target for edge-deployed si-cells. |
