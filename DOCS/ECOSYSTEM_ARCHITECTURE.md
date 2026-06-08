# SuperInstance Ecosystem Architecture

> **Version:** 2.0.0  
> **Last Updated:** 2026-06-07  
> **Status:** Living Document  
> **Authors:** SuperInstance Core Team

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Layers](#2-architecture-layers)
3. [Data Flow](#3-data-flow)
4. [Supabase Schema](#4-supabase-schema)
5. [Deployment Topology](#5-deployment-topology)
6. [Testing Strategy](#6-testing-strategy)
7. [Conservation Law Deep Dive](#7-conservation-law-deep-dive)
8. [BATON.md Handoff Protocol](#8-batonmd-handoff-protocol)
9. [Appendices](#9-appendices)

---

# 1. Overview

## 1.1 What Is SuperInstance?

SuperInstance is a **constraint-aware AI agent ecosystem** — a distributed collection of repositories, runtime libraries, mathematical foundations, and fleet infrastructure that together form a self-regulating, conservation-law-governed platform for building and orchestrating AI agents at scale.

Unlike traditional agent frameworks that treat resource management as an afterthought, SuperInstance places a **conservation law** at its core. Every agent, every computation, and every communication act is governed by an invariant borrowed from physics:

```
γ + η = total_budget
```

Where:
- **γ (gamma)** — compute energy budget (CPU, memory, inference tokens)
- **η (eta)** — communication information budget (messages, bandwidth, sync overhead)
- **total_budget** — the total capacity allocated to an agent or fleet

This single equation flows through every layer of the system, from the lowest Rust crate to the highest-level dashboard visualization. It is the invariant that makes the ecosystem **homeostatic** — capable of self-regulation without external intervention.

## 1.2 Scale and Scope

The SuperInstance ecosystem encompasses:

| Metric | Value |
|--------|-------|
| Total repositories | 3,608 |
| Runtime languages | 7 (C, Rust, TypeScript, Python, Go, Zig, WASM) |
| Published crates (crates.io) | 24+ |
| Published packages (PyPI) | 4+ |
| Total tests | ~4,761 |
| Core math libraries | 14 |
| Fleet infrastructure repos | 5 |
| Application repos | 8+ |
| Mothership files | 1,505 |
| Mothership tests | 2,065+ |

## 1.3 Core Principle: Conservation Law

The conservation law is not merely a metaphor. It is a **formally enforced invariant** with roots in Lagrangian mechanics, category theory, and optimal transport theory. The system ensures that at any point in time, for any agent or fleet:

```
∑γ_i + ∑η_i ≤ TotalFleetBudget
```

This constraint is:
- **Checked at compile time** (Rust type system)
- **Enforced at runtime** (budget allocators in every language runtime)
- **Monitored continuously** (fleet-warden health checks)
- **Visualized in real time** (ecosystem-dashboard)

When the invariant is violated, the system triggers corrective action through PID controllers (agent-homeostasis) or fleet-wide rebalancing (fleet-warden).

## 1.4 Design Philosophy

### 1.4.1 Physics-Informed Architecture

Every component in SuperInstance draws from a mathematical or physical formalism:

- **Lagrangian mechanics** → constraint-dynamics
- **Category theory** → categorical-agents
- **Optimal transport** → wasserstein-agents
- **Sheaf theory** → persistent-sheaf, sheaf-coherence
- **Geometric algebra** → ga-core
- **Hodge decomposition** → hodge-consensus
- **Spectral graph theory** → spectral-fleet
- **Renormalization group** → renormalization-group
- **Tropical geometry** → tropical-geometry
- **Symplectic optimization** → symplectic-opt
- **Lotka-Volterra dynamics** → dial-theory

This is not decoration — each formalism solves a real engineering problem (ranking, composition, health, consensus, scaling).

### 1.4.2 Polyglot by Design

The ecosystem supports 7 runtime languages not out of indecision, but out of conviction that different tools serve different purposes:

- **C** — foundational ABI, FFI boundary
- **Rust** — systems programming, safety-critical paths
- **TypeScript** — web, dashboard, API layer
- **Python** — ML/AI integration, research
- **Go** — concurrency-heavy fleet services
- **Zig** — performance-critical, embedded scenarios
- **WASM** — portable, sandboxed execution

All languages implement the **same API surface** through si-core-c as the ABI foundation.

### 1.4.3 Fleet-First Thinking

Every agent is designed to operate within a fleet — a collection of agents sharing a common budget. Individual agents can be added, removed, or migrated without breaking the conservation invariant. The fleet is the unit of deployment, the unit of budgeting, and the unit of observation.

### 1.4.4 Open by Default

All repositories are public. All APIs are documented. All schemas are versioned. The ecosystem is designed to be forkable, auditable, and extensible by anyone.

## 1.5 Repository Organization

```
SuperInstance/
├── conservation-law-rs/       # Layer 1: Core invariant
├── si-core-c/                 # Layer 2: C ABI foundation
├── si-runtime-rs/             # Layer 2: Rust runtime
├── si-runtime-js/             # Layer 2: TypeScript runtime
├── si-runtime-python/         # Layer 2: Python runtime
├── si-runtime-go/             # Layer 2: Go runtime
├── si-runtime-zig/            # Layer 2: Zig runtime
├── si-runtime-wasm/           # Layer 2: WASM runtime
├── si-cli/                    # Layer 3: Unified CLI
├── si-fleet-api/              # Layer 3: REST API
├── si-registry-rs/            # Layer 3: Local registry
├── ecosystem-dashboard/       # Layer 3: Visualization
├── spectral-fleet/            # Layer 4: Spectral ranking
├── fleet-warden/              # Layer 4: Health checking
├── agent-homeostasis/         # Layer 4: PID control
├── constraint-dynamics/       # Layer 4: Lagrangian mechanics
├── categorical-agents/        # Layer 4: Category theory
├── wasserstein-agents/        # Layer 4: Optimal transport
├── persistent-sheaf/          # Layer 4: Topological analysis
├── ga-core/                   # Layer 4: Geometric algebra
├── hodge-consensus/           # Layer 4: Hodge decomposition
├── dial-theory/               # Layer 4: Cultural dynamics
├── tropical-geometry/         # Layer 4: Tropical math
├── symplectic-opt/            # Layer 4: Symplectic optimization
├── renormalization-group/     # Layer 4: RG scaling
├── sheaf-coherence/           # Layer 4: Sheaf coherence
├── sunset-ecosystem/          # Layer 5: Mothership
├── cocapn/                    # Layer 5: Explainability
├── plato-construct/           # Layer 5: Education
├── open-terminal/             # Layer 5: Open apps
├── open-iterator/             # Layer 5: Open apps
├── open-application/          # Layer 5: Open apps
├── open-vectors/              # Layer 5: Open apps
├── open-parallel/             # Layer 5: Open apps
└── agent-operations/          # Meta: Operations & docs
```

---

# 2. Architecture Layers

## 2.0 Layer Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Layer 5: Applications                 │
│  sunset-ecosystem · cocapn · plato-construct · open-*   │
├─────────────────────────────────────────────────────────┤
│                Layer 4: Math Foundation                  │
│  spectral · warden · homeostasis · constraint ·          │
│  categorical · wasserstein · sheaf · ga · hodge ·        │
│  dial · tropical · symplectic · renorm · sheaf-coh       │
├─────────────────────────────────────────────────────────┤
│               Layer 3: Fleet Infrastructure              │
│  si-cli · si-fleet-api · si-registry · dashboard ·       │
│  Supabase                                                │
├─────────────────────────────────────────────────────────┤
│              Layer 2: Runtime Libraries (×7)             │
│  C · Rust · TypeScript · Python · Go · Zig · WASM       │
├─────────────────────────────────────────────────────────┤
│              Layer 1: Conservation Law Core              │
│                   conservation-law-rs                    │
└─────────────────────────────────────────────────────────┘
```

Each layer depends only on the layers below it. There are no circular dependencies. The conservation law in Layer 1 is the single source of truth for all budget computation.

---

## 2.1 Layer 1: Conservation Law (conservation-law-rs)

### 2.1.1 Purpose

`conservation-law-rs` is the **invariant core** of the entire ecosystem. It defines the data types, budget allocators, and enforcement mechanisms that every other component depends on. It is written in Rust for memory safety and performance, and compiled to a C ABI for consumption by all other runtimes.

### 2.1.2 Core Types

```rust
/// A budget allocation for a single agent or fleet
pub struct Budget {
    /// Compute energy budget (γ)
    pub gamma: f64,
    /// Communication information budget (η)
    pub eta: f64,
    /// Total capacity (immutable once allocated)
    pub total: f64,
}

/// Budget error types
pub enum BudgetError {
    /// γ + η would exceed total
    OverAllocation { requested: f64, available: f64 },
    /// Budget has been exhausted
    Exhausted { component: BudgetComponent },
    /// Invalid budget (negative values, NaN, etc.)
    Invalid { reason: String },
}

/// Which component of the budget
pub enum BudgetComponent {
    Gamma, // compute
    Eta,   // communication
}
```

### 2.1.3 The Conservation Invariant

The fundamental invariant is enforced by the `Budget::allocate` method:

```rust
impl Budget {
    /// Allocate from the budget, enforcing γ + η ≤ total
    pub fn allocate(&mut self, gamma: f64, eta: f64) -> Result<(), BudgetError> {
        if gamma < 0.0 || eta < 0.0 {
            return Err(BudgetError::Invalid {
                reason: "Budget components must be non-negative".into(),
            });
        }
        if gamma + eta > self.total {
            return Err(BudgetError::OverAllocation {
                requested: gamma + eta,
                available: self.total,
            });
        }
        self.gamma = gamma;
        self.eta = eta;
        Ok(())
    }

    /// Check if the invariant γ + η ≤ total holds
    pub fn is_conserved(&self) -> bool {
        (self.gamma + self.eta - self.total).abs() < f64::EPSILON
            || self.gamma + self.eta < self.total
    }

    /// Remaining budget capacity
    pub fn remaining(&self) -> f64 {
        (self.total - self.gamma - self.eta).max(0.0)
    }
}
```

### 2.1.4 Crate Structure

```
conservation-law-rs/
├── src/
│   ├── lib.rs              # Public API
│   ├── budget.rs           # Budget types and allocation
│   ├── invariant.rs        # Invariant checking and assertion
│   ├── allocator.rs        # Fleet-wide budget allocator
│   ├── conservation.rs     # Conservation law enforcement
│   └── cbindgen.rs         # C ABI exports
├── tests/
│   ├── budget_tests.rs
│   ├── invariant_tests.rs
│   └── allocator_tests.rs
├── Cargo.toml
└── build.rs                # cbindgen for C header generation
```

### 2.1.5 Fleet-Wide Allocation

The allocator distributes a total fleet budget across N agents while maintaining the global invariant:

```rust
pub struct FleetAllocator {
    total_budget: f64,
    allocations: HashMap<AgentId, Budget>,
}

impl FleetAllocator {
    /// Distribute budget proportionally across agents
    pub fn distribute(&mut self, weights: &[(AgentId, f64)]) -> Result<(), BudgetError> {
        let total_weight: f64 = weights.iter().map(|(_, w)| w).sum();
        for (id, weight) in weights {
            let share = (weight / total_weight) * self.total_budget;
            let gamma = share * 0.6; // 60% compute default
            let eta = share * 0.4;   // 40% communication default
            self.allocations.insert(*id, Budget::new(gamma, eta, share)?);
        }
        // Verify global invariant
        let total_allocated: f64 = self.allocations.values()
            .map(|b| b.gamma + b.eta).sum();
        assert!(total_allocated <= self.total_budget + f64::EPSILON);
        Ok(())
    }
}
```

### 2.1.6 How Every Crate Enforces Conservation

Every crate in the ecosystem imports `conservation-law-rs` and:

1. **Never constructs a `Budget` directly** — always through `Budget::new()` or `FleetAllocator::distribute()`
2. **Checks the invariant after every mutation** — `budget.is_conserved()` is called after allocations, transfers, and rebalancing
3. **Propagates errors, never panics** — `BudgetError` is returned and handled at every call site
4. **Logs violations** — any near-violation (within tolerance) is logged for fleet-warden to observe

This means that the conservation law is not a convention — it is a **compile-time guarantee** backed by runtime enforcement.

---

## 2.2 Layer 2: Runtime Libraries (7 Languages)

### 2.2.1 The Polyglot Contract

All 7 runtime libraries implement the **exact same API surface**. This is guaranteed by:

1. A shared test suite (`si-runtime-tests/`) that runs against every runtime
2. A C ABI boundary (`si-core-c`) that all runtimes either call directly or emulate
3. A compatibility matrix in CI that fails if any runtime diverges

The unified API surface:

```
// Every runtime must implement:
budget_create(total: f64) -> Budget
budget_allocate(b: Budget, gamma: f64, eta: f64) -> Result<Budget, Error>
budget_remaining(b: Budget) -> f64
budget_is_conserved(b: Budget) -> bool
budget_transfer(from: Budget, to: Budget, amount: f64) -> Result<(Budget, Budget), Error>

agent_register(id: AgentId, capabilities: Capabilities) -> Result<(), Error>
agent_execute(id: AgentId, task: Task, budget: Budget) -> Result<Output, Error>
agent_deregister(id: AgentId) -> Result<(), Error>

fleet_status() -> FleetStatus
fleet_health() -> HealthReport
```

### 2.2.2 si-core-c — C ABI Foundation

`si-core-c` is the lingua franca of the ecosystem. It exposes the conservation-law-rs functionality as a C ABI, enabling any language with FFI support to consume it directly.

**Key characteristics:**
- Zero-allocation hot paths
- Thread-safe reference counting for `Budget` objects
- Error codes (not exceptions) for cross-language compatibility
- Header generation via `cbindgen` in conservation-law-rs build

**API surface (C):**
```c
typedef struct SiBudget SiBudget;
typedef struct SiAgent SiAgent;

SiBudget* si_budget_create(double total);
int si_budget_allocate(SiBudget* b, double gamma, double eta);
double si_budget_remaining(const SiBudget* b);
int si_budget_is_conserved(const SiBudget* b);
void si_budget_free(SiBudget* b);

int si_agent_register(const char* id, const char* capabilities_json);
int si_agent_execute(const char* id, const char* task_json, SiBudget* budget);
int si_agent_deregister(const char* id);
```

### 2.2.3 si-runtime-rs — Rust Native

The Rust runtime is the most feature-complete implementation. It uses conservation-law-rs directly (same language, no FFI overhead) and adds:

- **Async runtime integration** (tokio)
- **Serde serialization** for budget types
- **Tracing instrumentation** for observability
- **Property-based testing** via proptest

```rust
use si_runtime_rs::{Budget, Agent, Fleet};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut fleet = Fleet::new(1000.0); // 1000 total budget units
    
    let agent = Agent::register("agent-1", Default::default()).await?;
    let budget = fleet.allocate("agent-1", 100.0)?;
    
    let output = agent.execute(task, budget).await?;
    println!("Result: {:?}", output);
    
    Ok(())
}
```

### 2.2.4 si-runtime-js — TypeScript/Node

The TypeScript runtime wraps si-core-c via `node-ffi-rs` or uses a pure TypeScript fallback for environments without native module support.

**Key features:**
- Full TypeScript type definitions
- Node.js EventEmitter for budget events
- Integration with Express.js (used by si-fleet-api)
- Deno compatibility

```typescript
import { Budget, Agent, Fleet } from 'si-runtime-js';

const fleet = new Fleet(1000.0);
const agent = await Agent.register('agent-1', {});
const budget = fleet.allocate('agent-1', 100.0);

const output = await agent.execute(task, budget);
console.log('Result:', output);
```

### 2.2.5 si-runtime-python — Python (PyO3)

The Python runtime uses PyO3 to wrap conservation-law-rs directly, providing native Python objects with Rust performance.

**Key features:**
- PyO3 bindings with zero-copy where possible
- Integration with NumPy for vectorized budget operations
- Async support via `asyncio`
- PyPI package: `si-runtime`

```python
from si_runtime import Budget, Agent, Fleet

fleet = Fleet(1000.0)
agent = Agent.register("agent-1", capabilities={})
budget = fleet.allocate("agent-1", 100.0)

output = agent.execute(task, budget)
print(f"Result: {output}")
```

### 2.2.6 si-runtime-go — Go

The Go runtime uses `cgo` to call si-core-c, providing idiomatic Go APIs.

**Key features:**
- Goroutine-safe budget operations
- Context-aware execution with cancellation
- Integration with Go's testing framework
- Channel-based budget event streaming

```go
import siruntime "si-runtime-go"

fleet := siruntime.NewFleet(1000.0)
agent, _ := siruntime.RegisterAgent("agent-1", nil)
budget, _ := fleet.Allocate("agent-1", 100.0)

output, _ := agent.Execute(task, budget)
fmt.Printf("Result: %v\n", output)
```

### 2.2.7 si-runtime-zig — Zig

The Zig runtime provides compile-time safety and zero-cost abstractions over si-core-c.

**Key features:**
- Comptime budget validation
- No hidden allocations
- Direct C interop without wrapper overhead
- Cross-compilation for embedded targets

```zig
const si = @import("si-runtime-zig");

var fleet = si.Fleet.init(1000.0);
var agent = try si.Agent.register("agent-1", .{});
var budget = try fleet.allocate("agent-1", 100.0);

var output = try agent.execute(task, budget);
std.debug.print("Result: {}\n", .{output});
```

### 2.2.8 si-runtime-wasm — WASM

The WASM runtime compiles conservation-law-rs to WebAssembly, enabling browser and edge deployment.

**Key features:**
- WASM target compilation (wasm32-unknown-unknown)
- JavaScript bindings via wasm-bindgen
- Browser-compatible budget management
- Edge runtime support (Cloudflare Workers, Deno Deploy)

```javascript
import { Budget, Fleet } from 'si-runtime-wasm';

const fleet = new Fleet(1000.0);
const budget = fleet.allocate('agent-1', 100.0);
// Works in browser, Node, Deno, edge runtimes
```

### 2.2.9 Runtime Compatibility Matrix

| Feature | C | Rust | TS | Python | Go | Zig | WASM |
|---------|---|------|----|--------|----|-----|------|
| Budget create | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Budget allocate | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Budget transfer | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Agent register | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Agent execute | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Fleet status | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Async execution | — | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Serde/JSON | — | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Property tests | — | ✅ | — | — | — | ✅ | — |

---

## 2.3 Layer 3: Fleet Infrastructure

### 2.3.1 Overview

Layer 3 provides the operational backbone: CLI tools, REST APIs, registries, and dashboards that make the ecosystem usable by developers and operators.

### 2.3.2 si-cli — Unified CLI

The `si-cli` is the primary interface for developers interacting with the ecosystem. It provides 8 core commands and has 23 tests.

**Commands:**

| Command | Description |
|---------|-------------|
| `si init` | Initialize a new agent project |
| `si scan` | Scan repository for CAPABILITY.toml |
| `si register` | Register agent with fleet |
| `si budget` | View/manage budget allocations |
| `si fleet` | Fleet status and health |
| `si run` | Execute an agent task |
| `si test` | Run agent test suite |
| `si publish` | Publish to registry |

**Architecture:**
- Written in Rust using `clap` for argument parsing
- Calls si-fleet-api for fleet operations
- Local operations use si-runtime-rs directly
- Supports `--format json` for scripting

**Usage example:**
```bash
# Initialize a new agent
si init my-agent --runtime rust

# Scan for capabilities
si scan

# Register with fleet
si register --fleet https://fleet.superinstance.dev

# Check budget
si budget --agent my-agent

# Run a task
si run --task task.json --budget 100.0

# Check fleet health
si fleet health
```

### 2.3.3 si-fleet-api — REST API

The fleet API is an Express.js application backed by Supabase, providing 11 REST routes for fleet management.

**Tech stack:**
- **Runtime:** Node.js with Express
- **Database:** Supabase (PostgreSQL)
- **Auth:** Supabase Row Level Security (RLS)
- **Validation:** Joi/Zod schemas

**Routes:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/repos` | List all registered repos |
| GET | `/api/repos/:id` | Get repo details |
| POST | `/api/repos` | Register a new repo |
| GET | `/api/capabilities` | List all capabilities |
| GET | `/api/capabilities/:repo` | Get capabilities for repo |
| GET | `/api/fleet/budgets` | Fleet-wide budget overview |
| GET | `/api/fleet/budgets/:agent` | Agent budget details |
| POST | `/api/fleet/budgets/:agent/allocate` | Allocate budget to agent |
| GET | `/api/fleet/health` | Fleet health report |
| GET | `/api/fleet/events` | Recent fleet events |
| POST | `/api/fleet/events` | Emit a fleet event |

**Budget enforcement in the API:**
Every allocation request goes through conservation-law validation:

```typescript
// POST /api/fleet/budgets/:agent/allocate
async function allocateBudget(req, res) {
    const { agentId } = req.params;
    const { gamma, eta } = req.body;
    
    // Fetch current fleet state
    const fleetBudget = await getFleetBudget(supabase);
    
    // Enforce conservation: γ + η ≤ remaining
    const requested = gamma + eta;
    const remaining = fleetBudget.total - fleetBudget.allocated;
    
    if (requested > remaining) {
        return res.status(409).json({
            error: 'BudgetOverAllocation',
            requested,
            remaining,
            message: `Cannot allocate ${requested}: only ${remaining} remaining`
        });
    }
    
    // Allocate
    await createAllocation(supabase, agentId, gamma, eta);
    res.json({ agentId, gamma, eta, allocated: requested });
}
```

### 2.3.4 si-registry-rs — Local Registry Client

The registry client provides offline-capable, local-first access to the fleet registry.

**Key features:**
- Local SQLite cache of registry data
- Background sync with Supabase
- Conflict resolution via last-write-wins with conservation-law tiebreaker
- Rust-native implementation using si-runtime-rs

**Why local registry?**
- Developers can work offline
- CI pipelines don't need API access for reads
- Reduces load on Supabase
- Enables air-gapped deployments

### 2.3.5 ecosystem-dashboard — Live Visualization

The dashboard provides real-time visualization of the fleet across 10 panels.

**Tech stack:**
- React + TypeScript
- D3.js for visualizations
- Supabase Realtime for live updates
- Deployed to GitHub Pages

**Panels:**

| Panel | Description |
|-------|-------------|
| Fleet Overview | Total agents, active/idle, geographic distribution |
| Budget Gauge | γ/η breakdown, remaining capacity |
| Agent Map | Network graph of agent relationships |
| Conservation Monitor | Real-time invariant checking |
| Health Dashboard | Fleet-warden health report |
| Event Stream | Live fleet events |
| Spectral Ranking | PageRank/eigenvector ranking |
| Capability Matrix | Which agents have which capabilities |
| Topology View | Sheaf-coherence topological map |
| Audit Log | Budget allocation history |

### 2.3.6 Supabase — Cloud Backbone

Supabase serves as the persistent cloud backbone for the fleet, providing:

- **PostgreSQL database** — repos, capabilities, budgets, events tables
- **Row Level Security** — public read, authenticated write
- **Realtime subscriptions** — live dashboard updates
- **Edge Functions** — serverless budget enforcement hooks
- **Storage** — agent artifacts and logs

**Project details:**
- Region: us-west-2
- Project ID: igogykhksgkaxcwzudwi
- Public URL: `https://igogykhksgkaxcwzudwi.supabase.co`

---

## 2.4 Layer 4: Math Foundation

### 2.4.1 Overview

Layer 4 is the mathematical engine room of the ecosystem. Each library addresses a specific computational need, grounded in a rigorous mathematical formalism. Together, they provide ranking, health monitoring, self-regulation, constraint solving, composition, transport, topology, geometry, consensus, cultural dynamics, and scaling.

### 2.4.2 spectral-fleet — Ranking and Centrality

**Formalism:** Spectral graph theory  
**Purpose:** Rank agents and capabilities by importance using graph-theoretic measures

Implements:
- **PageRank** — importance ranking based on capability links
- **Eigenvector centrality** — influence measurement in the agent graph
- **Laplacian eigenvalues** — connectivity analysis
- **Spectral clustering** — automatic fleet partitioning

**Use case:** When a fleet needs to identify the most critical agents (for budget priority, health check frequency, or failover ordering), spectral-fleet provides mathematically grounded rankings.

```rust
use spectral_fleet::{AgentGraph, PageRank};

let graph = AgentGraph::from_fleet(&fleet);
let rankings = PageRank::compute(&graph, 0.85, 100);
// rankings[0] = most central agent
```

### 2.4.3 fleet-warden — Health Checking and Conservation Enforcement

**Formalism:** Control theory  
**Purpose:** Continuous health monitoring with conservation law enforcement

Implements:
- **Heartbeat monitoring** — periodic agent health checks
- **Budget conservation verification** — fleet-wide invariant checking
- **Anomaly detection** — statistical deviation from expected budget patterns
- **Auto-remediation** — budget rebalancing when violations detected

**Health check cycle:**
```
Every 30 seconds:
  1. Poll all registered agents
  2. Collect budget states (γ, η, total)
  3. Verify ∑(γ + η) ≤ FleetTotal
  4. Flag agents with budget > 2σ from mean
  5. Trigger remediation if invariant violated
  6. Emit fleet_events to Supabase
```

### 2.4.4 agent-homeostasis — PID Control and Self-Regulation

**Formalism:** Classical control theory (PID controllers)  
**Purpose:** Self-regulation of agent resource consumption

Implements:
- **PID controller** — proportional-integral-derivative control for budget usage
- **Setpoint tracking** — target budget utilization (e.g., 80% of allocation)
- **Oscillation damping** — prevent budget usage spikes
- **Multi-variable control** — simultaneous γ and η regulation

**PID parameters:**
```rust
pub struct PidConfig {
    /// Proportional gain: how aggressively to respond to error
    pub kp: f64,  // default: 1.0
    /// Integral gain: accumulation of past error
    pub ki: f64,  // default: 0.1
    /// Derivative gain: prediction of future error
    pub kd: f64,  // default: 0.05
    /// Target utilization fraction
    pub setpoint: f64, // default: 0.8
}
```

The homeostasis controller ensures agents don't oscillate between budget exhaustion and idle states, maintaining steady resource consumption within conservation constraints.

### 2.4.5 constraint-dynamics — CSP and Lagrangian Mechanics

**Formalism:** Lagrangian mechanics, constraint satisfaction problems (CSP)  
**Purpose:** Solve constraint optimization problems for fleet configuration

Implements:
- **Lagrangian formulation** — express fleet constraints as Lagrangian mechanics
- **Constraint satisfaction** — solve CSP instances for fleet configuration
- **Hamiltonian** — energy function for fleet state
- **Euler-Lagrange equations** — derive optimal budget trajectories

The Lagrangian for fleet state:
```
L(γ, η, γ̇, η̇) = T(γ̇, η̇) - V(γ, η)
```
Where T is the "kinetic energy" (rate of budget change) and V is the "potential energy" (budget utilization pressure).

### 2.4.6 categorical-agents — Category Theory for Agent Composition

**Formalism:** Category theory  
**Purpose:** Compose agents using mathematically sound composition laws

Implements:
- **Morphisms** — agent transformations as category theory morphisms
- **Functors** — structure-preserving mappings between agent categories
- **Natural transformations** — mappings between functors
- **Limits and colimits** — universal constructions for agent assembly
- **Monoidal categories** — sequential and parallel agent composition

**Use case:** When building a pipeline of agents, categorical-agents ensures the composition is well-typed (output types match input types) and respects the conservation law (budgets compose correctly).

### 2.4.7 wasserstein-agents — Optimal Transport

**Formalism:** Optimal transport theory (Wasserstein distances)  
**Purpose:** Compute the "cost" of moving agent distributions from one state to another

Implements:
- **Wasserstein-1 distance** — earth mover's distance between budget distributions
- **Wasserstein-2 distance** — quadratic cost transport
- **Sinkhorn algorithm** — regularized optimal transport
- **Transport plans** — optimal reallocation of budgets across agents

**Use case:** When rebalancing a fleet (e.g., after an agent failure), wasserstein-agents computes the minimum-cost reallocation that satisfies the conservation invariant.

### 2.4.8 persistent-sheaf — Topological Data Analysis

**Formalism:** Sheaf theory, persistent homology  
**Purpose:** Analyze the topological structure of agent networks

Implements:
- **Persistent homology** — detect holes, voids, and connected components in fleet topology
- **Sheaf cohomology** — measure consistency of local-to-global data
- **Betti numbers** — quantify topological features
- **Persistence diagrams** — visualize topological evolution over time

**Use case:** Detect when a fleet has "structural gaps" — agents that are isolated or clusters that are disconnected — before they cause operational problems.

### 2.4.9 ga-core — Geometric Algebra Cl(3,1)

**Formalism:** Geometric algebra (Clifford algebra)  
**Purpose:** Provide a unified mathematical framework for spatial reasoning

Implements:
- **Cl(3,1) algebra** — spacetime algebra for agent state representation
- **Multivector operations** — geometric product, outer product, inner product
- **Rotors** — rotation operators for state transformations
- **Geometric calculus** — differentiation and integration on multivectors

**Use case:** Represent agent state as multivectors for compact, rotation-invariant state comparison and transformation.

### 2.4.10 hodge-consensus — Hodge Decomposition for Consensus

**Formalism:** Hodge decomposition (Helmholtz decomposition on graphs)  
**Purpose:** Decompose agent opinions/preferences into consensus, gradient, and harmonic components

Implements:
- **Hodge decomposition** — split agent preferences into:
  - **Consensus component** — globally agreed ranking
  - **Gradient component** — cyclically consistent preferences
  - **Harmonic component** — irreducible cycles
- **HodgeRank** — consensus ranking from pairwise comparisons
- **Cycle detection** — identify circular preference inconsistencies

**Use case:** When agents have conflicting preferences (e.g., for task assignment), hodge-consensus extracts the consensus and quantifies disagreement.

### 2.4.11 dial-theory — Cultural Dynamics

**Formalism:** Lotka-Volterra equations, cultural evolution  
**Purpose:** Model cultural and behavioral dynamics in agent populations

Implements:
- **Lotka-Volterra dynamics** — predator-prey model for agent interaction patterns
- **Cultural dialectic** — thesis-antithesis-synthesis for agent behavior evolution
- **Dial parameters** — configurable cultural interaction coefficients
- **Population dynamics** — track agent type distributions over time

**Use case:** In heterogeneous fleets where different agent types compete for resources, dial-theory predicts and manages the population dynamics.

### 2.4.12 tropical-geometry

**Formalism:** Tropical geometry (min-plus algebra)  
**Purpose:** Solve optimization problems in tropical semirings

Implements:
- **Tropical semiring** — (ℝ ∪ {∞}, min, +) algebra
- **Tropical polynomials** — piecewise-linear optimization
- **Tropical curves** — visualize tropical solution spaces
- **Shortest path computation** — tropical matrix operations

### 2.4.13 symplectic-opt

**Formalism:** Symplectic geometry  
**Purpose:** Structure-preserving optimization for agent state evolution

Implements:
- **Symplectic integrators** — energy-preserving numerical integration
- **Hamiltonian systems** — optimize without violating conservation constraints
- **Symplectic gradient** — constrained optimization respecting symplectic structure

### 2.4.14 renormalization-group

**Formalism:** Renormalization group (physics)  
**Purpose:** Multi-scale analysis of fleet behavior

Implements:
- **Coarse-graining** — simplify fleet description at larger scales
- **Flow equations** — track how parameters change under renormalization
- **Fixed points** — identify stable fleet configurations
- **Critical exponents** — characterize phase transitions in fleet behavior

### 2.4.15 sheaf-coherence

**Formalism:** Sheaf theory  
**Purpose:** Measure and maintain coherence across distributed agent data

Implements:
- **Sheaf assignments** — local data consistent with global constraints
- **Cohomological coherence** — measure consistency via sheaf cohomology
- **Coherence repair** — fix inconsistent local data assignments
- **Consistency verification** — validate sheaf conditions across agent boundaries

---

## 2.5 Layer 5: Applications

### 2.5.1 sunset-ecosystem — The Mothership

**The crown jewel of the ecosystem.** With 1,505 files and 2,065+ tests, sunset-ecosystem is the primary application platform, implementing a **Trinity Architecture** for multi-agent orchestration.

**Trinity Architecture:**
The system is organized into three interdependent pillars:

1. **The Creator** — Agent creation, configuration, and capability definition
2. **The Executor** — Task execution with conservation-law enforcement
3. **The Arbiter** — Conflict resolution, budget arbitration, and fleet governance

**VCG Auction Mechanism:**
sunset-ecosystem uses a Vickrey-Clarke-Groves (VCG) auction for budget allocation among competing agents:

```
1. Each agent submits a bid (how much budget it wants)
2. The Arbiter computes the socially optimal allocation
3. Each agent pays the externality it imposes on others
4. The conservation invariant is maintained throughout
```

This ensures truthful bidding (agents have no incentive to misrepresent their needs) and efficient allocation (budget goes to agents that create the most value).

**Scale:**
- 1,505 source files
- 2,065+ tests
- Trinity: Creator + Executor + Arbiter
- VCG auction for budget allocation
- Full conservation-law integration

### 2.5.2 cocapn — Explainability

**Purpose:** Provide human-readable explanations of agent decisions and budget allocations.

Implements:
- **Decision trees** — trace why an agent chose a particular action
- **Budget explanations** — "Agent X received 100γ because its bid was highest in the VCG auction"
- **Conservation explanations** — "The fleet has 50 units remaining after this allocation"
- **Counterfactual analysis** — "What would happen if Agent Y had requested more budget?"

### 2.5.3 plato-construct — Education Platform

**Purpose:** Educational platform for learning the SuperInstance ecosystem and its mathematical foundations.

Implements:
- **Interactive tutorials** — step-by-step guides for each math library
- **Visualization tools** — see spectral-fleet, sheaf-coherence in action
- **Budget simulators** — experiment with conservation law without real agents
- **Curriculum paths** — from beginner (what is a budget?) to advanced (Lagrangian mechanics)

### 2.5.4 Open Applications

A suite of open-source applications built on the ecosystem:

| Repository | Purpose |
|------------|---------|
| open-terminal | Terminal/CLI interface for fleet interaction |
| open-iterator | Iterator pattern library for agent pipelines |
| open-application | Application scaffolding and templates |
| open-vectors | Vector operations for agent state management |
| open-parallel | Parallel execution framework for multi-agent tasks |

---

# 3. Data Flow

## 3.1 Overview

Data flows through the ecosystem in a well-defined hierarchy, with the conservation law enforced at every transition point.

```
┌──────────┐     ┌──────────────┐     ┌──────────┐     ┌───────────┐
│ Supabase │ ──→ │ si-fleet-api │ ──→ │  si-cli  │ ──→ │ Developer │
│ (Source) │     │  (Gateway)   │     │  (CLI)   │     │  (User)   │
└──────────┘     └──────────────┘     └──────────┘     └───────────┘
      ↑                  ↑                   ↑
      │                  │                   │
      │    ┌─────────────┴───────────────────┘
      │    │ Conservation law enforcement
      │    │ at every layer transition
      │    │
      ├─── fleet-warden (periodic health checks)
      │
      └─── ecosystem-dashboard (real-time subscriptions)
```

## 3.2 Registration Flow

When a new repository is added to the ecosystem:

```
1. Developer creates CAPABILITY.toml in repo root
   ┌─────────────────────────────────────┐
   │ [agent]                             │
   │ name = "my-agent"                   │
   │ runtime = "rust"                    │
   │ version = "0.1.0"                   │
   │                                     │
   │ [capabilities]                      │
   │ compute = true                      │
   │ communication = true                │
   │ budget_requirement = 100.0          │
   │                                     │
   │ [dependencies]                      │
   │ spectral-fleet = ">=0.2.0"          │
   └─────────────────────────────────────┘

2. si scan reads CAPABILITY.toml
   → Validates schema
   → Extracts capabilities and budget requirements
   → Checks conservation feasibility

3. si register posts to si-fleet-api
   → API validates against fleet budget
   → Creates entry in Supabase repos table
   → Creates entries in capabilities table
   → Emits fleet_event

4. fleet-warden picks up new registration
   → Initial health check
   → Adds to monitoring rotation
   → Updates spectral-fleet graph

5. ecosystem-dashboard shows new agent
   → Real-time subscription from Supabase
   → Agent appears in Fleet Overview panel
   → Budget gauge updates
```

## 3.3 Budget Allocation Flow

```
Developer                     si-cli              si-fleet-api           Supabase
    │                           │                      │                    │
    │  si budget allocate       │                      │                    │
    │  --agent my-agent         │                      │                    │
    │  --gamma 60 --eta 40      │                      │                    │
    │──────────────────────────→│                      │                    │
    │                           │  POST /api/fleet/    │                    │
    │                           │  budgets/my-agent/   │                    │
    │                           │  allocate            │                    │
    │                           │─────────────────────→│                    │
    │                           │                      │  SELECT remaining  │
    │                           │                      │───────────────────→│
    │                           │                      │  remaining=150.0   │
    │                           │                      │←───────────────────│
    │                           │                      │                    │
    │                           │                      │  100 ≤ 150? YES   │
    │                           │                      │  [conservation OK] │
    │                           │                      │                    │
    │                           │                      │  INSERT allocation │
    │                           │                      │───────────────────→│
    │                           │                      │  OK                │
    │                           │                      │←───────────────────│
    │                           │  200 OK              │                    │
    │                           │←─────────────────────│                    │
    │  Budget allocated         │                      │                    │
    │←──────────────────────────│                      │                    │
    │                           │                      │                    │
    │                           │                      │  [fleet-warden     │
    │                           │                      │   verifies invariant│
    │                           │                      │   on next cycle]   │
```

## 3.4 Conservation Law Enforcement at Every Layer

| Layer | Enforcement Mechanism | Frequency |
|-------|----------------------|-----------|
| Layer 1 | Compile-time type guarantees | Every build |
| Layer 2 | Runtime `is_conserved()` checks | Every allocation |
| Layer 3 | API validation + Supabase constraints | Every API call |
| Layer 4 | Mathematical invariant verification | Every computation |
| Layer 5 | Application-level budget guards | Every task execution |

## 3.5 CAPABILITY.toml → si scan → Fleet Registry

The `CAPABILITY.toml` file is the declarative entry point for any repository into the fleet ecosystem. It follows a strict schema:

```toml
# CAPABILITY.toml — Agent capability declaration

[agent]
name = "agent-name"          # Required: unique identifier
runtime = "rust"              # Required: one of c|rust|ts|python|go|zig|wasm
version = "0.1.0"            # Required: semver
description = "What this agent does"

[capabilities]
compute = true                # Can perform computation
communication = true          # Can send/receive messages
storage = false               # Needs persistent storage
network = false               # Needs network access

[budget]
gamma_requirement = 60.0     # Compute budget needed
eta_requirement = 40.0       # Communication budget needed
priority = "normal"          # normal|high|critical

[dependencies]
spectral-fleet = ">=0.2.0"
fleet-warden = ">=0.1.0"

[integration]
# Optional: links to INTEGRATION.md for cross-repo wiring
upstream = ["agent-producer"]
downstream = ["agent-consumer"]
```

**si scan process:**
1. Walk directory tree looking for `CAPABILITY.toml`
2. Parse and validate against JSON Schema
3. Check that declared runtime has corresponding si-runtime-* package
4. Verify budget requirements are physically meaningful (positive, finite)
5. Output structured report (JSON or table)
6. Optionally register with fleet (if `--register` flag)

## 3.6 INTEGRATION.md → Cross-Repo Wiring

`INTEGRATION.md` files describe how repositories connect to each other:

```markdown
# INTEGRATION.md

## Upstream Dependencies
- `spectral-fleet` — Provides ranking data for agent prioritization
- `conservation-law-rs` — Core budget types

## Downstream Consumers
- `si-fleet-api` — Consumes our health check data
- `ecosystem-dashboard` — Displays our metrics

## Data Contracts
- Health check response: `{ status: "healthy"|"degraded"|"down", budget: Budget }`
- Event emission: `{ type: string, agent: string, timestamp: ISO8601 }`

## Conservation Impact
- This repo consumes 5% of fleet γ budget for health checks
- Emits 2% η budget in event notifications
```

---

# 4. Supabase Schema

## 4.1 Overview

The Supabase PostgreSQL database serves as the persistent state store for the fleet. It uses Row Level Security (RLS) to provide public anonymous read access while requiring authentication for writes.

## 4.2 Tables

### repos

```sql
CREATE TABLE repos (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL UNIQUE,
    full_name   TEXT NOT NULL,          -- e.g., "SuperInstance/si-cli"
    description TEXT,
    language    TEXT,                    -- primary language
    runtime     TEXT,                    -- c|rust|ts|python|go|zig|wasm
    url         TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now(),
    metadata    JSONB DEFAULT '{}'::jsonb
);

-- RLS: Public read
ALTER TABLE repos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON repos FOR SELECT USING (true);
CREATE POLICY "Authenticated write" ON repos FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "Authenticated update" ON repos FOR UPDATE USING (auth.role() = 'authenticated');
```

### capabilities

```sql
CREATE TABLE capabilities (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id     UUID NOT NULL REFERENCES repos(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,           -- e.g., "compute", "communication"
    value       JSONB NOT NULL,          -- capability configuration
    created_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE(repo_id, name)
);

ALTER TABLE capabilities ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON capabilities FOR SELECT USING (true);
CREATE POLICY "Authenticated write" ON capabilities FOR INSERT WITH CHECK (auth.role() = 'authenticated');
```

### fleet_budgets

```sql
CREATE TABLE fleet_budgets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id        TEXT NOT NULL UNIQUE,
    gamma           DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    eta             DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    total           DOUBLE PRECISION NOT NULL,
    fleet_total     DOUBLE PRECISION NOT NULL,  -- snapshot of fleet total at allocation time
    allocated_at    TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now(),
    
    -- Conservation constraint: γ + η ≤ total
    CONSTRAINT conservation_invariant CHECK (gamma + eta <= total + 0.0001),
    CONSTRAINT positive_budgets CHECK (gamma >= 0 AND eta >= 0 AND total > 0)
);

ALTER TABLE fleet_budgets ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON fleet_budgets FOR SELECT USING (true);
CREATE POLICY "Authenticated write" ON fleet_budgets FOR ALL 
    USING (auth.role() = 'authenticated');
```

### fleet_events

```sql
CREATE TABLE fleet_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type  TEXT NOT NULL,           -- "allocation", "health_check", "violation", "registration"
    agent_id    TEXT,
    payload     JSONB DEFAULT '{}'::jsonb,
    severity    TEXT DEFAULT 'info',     -- info|warning|error|critical
    created_at  TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE fleet_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON fleet_events FOR SELECT USING (true);
CREATE POLICY "Authenticated write" ON fleet_events FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Index for recent events queries
CREATE INDEX idx_fleet_events_type_time ON fleet_events (event_type, created_at DESC);
CREATE INDEX idx_fleet_events_agent ON fleet_events (agent_id, created_at DESC);
```

## 4.3 Database-Level Conservation Enforcement

The `fleet_budgets` table has a CHECK constraint that enforces the conservation invariant at the database level:

```sql
CONSTRAINT conservation_invariant CHECK (gamma + eta <= total + 0.0001)
```

The small epsilon (0.0001) accounts for floating-point rounding. This means even if a bug in the API layer allows an invalid allocation through, the database will reject it.

## 4.4 Realtime Subscriptions

The dashboard subscribes to realtime updates:

```typescript
const subscription = supabase
    .channel('fleet-updates')
    .on('postgres_changes', 
        { event: '*', schema: 'public', table: 'fleet_budgets' },
        (payload) => updateDashboard(payload))
    .on('postgres_changes',
        { event: '*', schema: 'public', table: 'fleet_events' },
        (payload) => updateEventStream(payload))
    .subscribe();
```

---

# 5. Deployment Topology

## 5.1 Component Map

```
┌─────────────────────────────────────────────────────────────────┐
│                        Internet                                  │
│                                                                  │
│  ┌──────────────────┐         ┌───────────────────────────┐     │
│  │  GitHub Pages     │         │  Supabase (us-west-2)     │     │
│  │  ecosystem-       │ ←─────→ │  Project: igogykhksgkax-  │     │
│  │  dashboard        │  API    │  cwzudwi                  │     │
│  │                   │         │                           │     │
│  │  Static SPA       │         │  • PostgreSQL             │     │
│  │  React + D3       │         │  • Realtime WS            │     │
│  │  CDN-backed       │         │  • RLS policies           │     │
│  └──────────────────┘         └───────────────────────────┘     │
│                                                                  │
│  ┌──────────────────┐         ┌───────────────────────────┐     │
│  │  crates.io        │         │  PyPI                     │     │
│  │  24+ published    │         │  4+ published             │     │
│  │  crates           │         │  packages                 │     │
│  └──────────────────┘         └───────────────────────────┘     │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitHub (SuperInstance org)                               │   │
│  │  3,608 repositories                                       │   │
│  │  CI: GitHub Actions (multi-language matrix)               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 5.2 Distribution Channels

### crates.io (Rust)
24+ published crates including:
- `conservation-law` — core invariant library
- `si-runtime` — Rust runtime
- `spectral-fleet` — spectral ranking
- `fleet-warden` — health checking
- `agent-homeostasis` — PID control
- `ga-core` — geometric algebra
- `hodge-consensus` — Hodge decomposition
- `categorical-agents` — category theory
- `wasserstein-agents` — optimal transport
- And 15+ more

### PyPI (Python)
4+ published packages:
- `si-runtime` — Python runtime (PyO3)
- `conservation-law` — Python bindings
- Additional math library bindings

### npm (TypeScript/JavaScript)
- `si-runtime-wasm` — WASM runtime
- `si-runtime-js` — Node.js runtime
- Dashboard dependencies

### GitHub Container Registry
- Docker images for si-fleet-api
- CI/CD base images

## 5.3 CI/CD Pipeline

```
GitHub Push → GitHub Actions → Multi-language Matrix
                                 ├── Rust (stable, nightly, MSRV)
                                 ├── TypeScript (node 18, 20, 22)
                                 ├── Python (3.10, 3.11, 3.12)
                                 ├── Go (1.21, 1.22)
                                 ├── Zig (0.12, 0.13)
                                 └── WASM (wasm-pack test)
                                 │
                                 ├── Test → Lint → Build
                                 ├── Conservation invariant test
                                 ├── Cross-runtime compatibility
                                 └── Publish (on tag)
```

## 5.4 Environments

| Environment | Purpose | URL/Location |
|-------------|---------|-------------|
| Production Dashboard | Live fleet visualization | GitHub Pages |
| Production API | Fleet management | si-fleet-api (deployed) |
| Production DB | Persistent state | Supabase us-west-2 |
| crates.io | Rust package distribution | crates.io |
| PyPI | Python package distribution | pypi.org |
| npm | JS/WASM package distribution | npmjs.com |
| CI | Automated testing | GitHub Actions |

---

# 6. Testing Strategy

## 6.1 Test Scale

The ecosystem maintains approximately **4,761 total tests** across all repositories.

### Per-Component Breakdown

| Component | Tests | Language | Type |
|-----------|-------|----------|------|
| sunset-ecosystem | 2,065+ | Multiple | Unit + Integration + E2E |
| conservation-law-rs | ~150 | Rust | Unit + Property |
| si-runtime-rs | ~200 | Rust | Unit + Property |
| si-runtime-js | ~100 | TypeScript | Unit + Integration |
| si-runtime-python | ~80 | Python | Unit |
| si-runtime-go | ~70 | Go | Unit |
| si-runtime-zig | ~60 | Zig | Unit |
| si-runtime-wasm | ~50 | WASM | Unit |
| si-cli | 23 | Rust | Integration |
| si-fleet-api | ~40 | TypeScript | Integration + E2E |
| spectral-fleet | ~120 | Rust | Unit + Property |
| fleet-warden | ~100 | Rust | Unit + Integration |
| agent-homeostasis | ~90 | Rust | Unit + Property |
| constraint-dynamics | ~110 | Rust | Unit + Property |
| categorical-agents | ~80 | Rust | Unit |
| wasserstein-agents | ~70 | Rust | Unit + Property |
| persistent-sheaf | ~60 | Rust | Unit |
| ga-core | ~90 | Rust | Unit + Property |
| hodge-consensus | ~70 | Rust | Unit |
| dial-theory | ~50 | Rust | Unit |
| tropical-geometry | ~40 | Rust | Unit |
| symplectic-opt | ~40 | Rust | Unit |
| renormalization-group | ~35 | Rust | Unit |
| sheaf-coherence | ~40 | Rust | Unit |
| Other repos | ~1,000+ | Mixed | Various |

## 6.2 Testing Types

### 6.2.1 Unit Tests
Every function in every runtime has at least one unit test. Conservation-law functions have comprehensive coverage including edge cases (zero budget, max budget, floating-point edge cases).

### 6.2.2 Property-Based Testing
Math-heavy libraries use `proptest` (Rust) to generate thousands of random inputs and verify invariants hold:

```rust
proptest! {
    #[test]
    fn conservation_invariant_holds(
        gamma in 0.0f64..1000.0,
        eta in 0.0f64..1000.0,
        total in 0.0f64..1000.0,
    ) {
        // Skip if gamma + eta > total (allocation should fail)
        if gamma + eta <= total {
            let budget = Budget::new(gamma, eta, total).unwrap();
            prop_assert!(budget.is_conserved());
            prop_assert!((budget.gamma + budget.eta - total).abs() < 1e-10
                || budget.gamma + budget.eta < total);
        }
    }
}
```

### 6.2.3 Integration Tests
Cross-component interactions are tested:
- si-cli ↔ si-fleet-api communication
- Runtime ↔ conservation-law-rs FFI
- API ↔ Supabase database operations

### 6.2.4 Cross-Runtime Compatibility Tests
A shared test suite validates that all 7 runtimes produce identical results for the same inputs:

```yaml
# .github/workflows/cross-runtime.yml
strategy:
  matrix:
    runtime: [rust, ts, python, go, zig, wasm, c]
steps:
  - name: Run shared test suite
    run: |
      ./scripts/run-shared-tests.sh ${{ matrix.runtime }}
```

### 6.2.5 Conservation Invariant Tests
Every CI run includes a dedicated conservation invariant test:

```bash
# Runs in every CI pipeline
cargo test --package conservation-law --test invariant_tests
```

This test suite verifies:
- Budget allocation never exceeds total
- Fleet allocation sums never exceed fleet total
- Transfer operations maintain bilateral conservation
- PID controller outputs respect budget bounds

## 6.3 CI Matrix

```yaml
# Simplified CI matrix
strategy:
  matrix:
    include:
      - language: rust
        versions: [stable, nightly, 1.75.0]  # MSRV
        os: [ubuntu-latest, macos-latest]
      - language: typescript
        versions: [18, 20, 22]
      - language: python
        versions: ["3.10", "3.11", "3.12"]
      - language: go
        versions: ["1.21", "1.22"]
      - language: zig
        versions: ["0.12.0", "0.13.0"]
      - language: wasm
        targets: [wasm32-unknown-unknown]
```

---

# 7. Conservation Law Deep Dive

## 7.1 Mathematical Formulation

### 7.1.1 The Fundamental Invariant

The conservation law is expressed as:

```
γ(t) + η(t) ≤ B    ∀t
```

Where:
- **γ(t)** — total compute energy in use at time t
- **η(t)** — total communication information in use at time t
- **B** — total budget capacity (constant for a given fleet)

This is analogous to the first law of thermodynamics: energy cannot be created or destroyed, only transformed. In the SuperInstance context, the "energy" of the system (compute + communication) is conserved — it can be allocated and transferred but never exceeds the total capacity.

### 7.1.2 Lagrangian Formulation

The constraint can be embedded in a Lagrangian:

```
L = T(γ̇, η̇) - V(γ, η) - λ(γ + η - B)
```

Where:
- **T(γ̇, η̇)** — "kinetic energy" (rate of budget change)
- **V(γ, η)** — "potential energy" (budget utilization pressure)
- **λ** — Lagrange multiplier enforcing the constraint
- **γ̇, η̇** — time derivatives of budget components

The Euler-Lagrange equations yield optimal budget trajectories:

```
d/dt(∂L/∂γ̇) - ∂L/∂γ = 0
d/dt(∂L/∂η̇) - ∂L/∂η = 0
```

### 7.1.3 Hamiltonian Formulation

The Hamiltonian (total energy) is:

```
H = p_γ · γ̇ + p_η · η̇ - L
```

Where p_γ and p_η are conjugate momenta. This formulation is used by `symplectic-opt` for structure-preserving optimization.

### 7.1.4 Fleet-Level Conservation

For a fleet of N agents, the conservation law becomes:

```
Σᵢ (γᵢ + ηᵢ) ≤ B_fleet    ∀t
```

This global invariant is maintained by:
1. **Centralized checking** — fleet-warden verifies every 30 seconds
2. **Decentralized enforcement** — each agent checks before allocation
3. **Database constraint** — CHECK constraint in Supabase
4. **Mathematical proof** — categorical-agents proves composition correctness

## 7.2 Enforcement in Each Runtime

### 7.2.1 Rust (conservation-law-rs)

```rust
// Compile-time: type system prevents constructing invalid budgets
let budget = Budget::new(60.0, 40.0, 100.0)?; // OK: 60+40=100

// Runtime: allocation checks invariant
budget.allocate(70.0, 40.0)?; // Error: 70+40=110 > 100

// Transfer: bilateral conservation
let (a, b) = Budget::transfer(&mut a, &mut b, 10.0)?;
// a.total decreases by 10, b.total increases by 10
// Both individual and global invariants preserved
```

### 7.2.2 TypeScript (si-runtime-js)

```typescript
const budget = Budget.create(100.0); // total = 100
budget.allocate(60.0, 40.0);        // OK: 60+40=100
budget.allocate(70.0, 40.0);        // throws BudgetError: OverAllocation

// Event-driven enforcement
budget.on('near-violation', (usage) => {
    console.warn(`Budget at ${(usage * 100).toFixed(1)}% capacity`);
});
```

### 7.2.3 Python (si-runtime-python)

```python
budget = Budget(100.0)
budget.allocate(60.0, 40.0)  # OK

try:
    budget.allocate(70.0, 40.0)  # raises BudgetError
except BudgetError as e:\n    print(f"Conservation violated: {e}")

# NumPy vectorized conservation check
import numpy as np
budgets = np.array([[60, 40], [30, 20], [10, 5]])
totals = np.array([100, 50, 20])
conserved = np.sum(budgets, axis=1) <= totals  # [True, True, True]
```

### 7.2.4 Go (si-runtime-go)

```go
budget, _ := siruntime.NewBudget(100.0)
err := budget.Allocate(60.0, 40.0)  // nil = OK
err = budget.Allocate(70.0, 40.0)   // BudgetError

// Goroutine-safe conservation check
go func() {
    for range time.Tick(30 * time.Second) {
        if !budget.IsConserved() {
            log.Error("Conservation invariant violated!")
        }
    }
}()
```

### 7.2.5 Zig (si-runtime-zig)

```zig
var budget = try si.Budget.init(100.0);
try budget.allocate(60.0, 40.0);  // OK

// Comptime validation
const StaticBudget = si.Budget.Comptime(60, 40, 100); // compiles
// const BadBudget = si.Budget.Comptime(70, 40, 100);  // compile error!
```

### 7.2.6 WASM (si-runtime-wasm)

```javascript
const budget = new Budget(100.0);
budget.allocate(60.0, 40.0);  // OK
budget.allocate(70.0, 40.0);  // throws WebAssembly.RuntimeError

// Browser-compatible conservation monitoring
setInterval(() => {
    if (!budget.isConserved()) {
        console.error('Conservation violation detected!');
    }
}, 30000);
```

## 7.3 Fleet-Wide Invariant Checking

### 7.3.1 fleet-warden Monitoring Cycle

```
Every 30 seconds:
  ┌────────────────────────────────────────────────┐
  │ 1. SELECT all rows from fleet_budgets           │
  │ 2. Compute sum(gamma + eta) across all agents   │
  │ 3. If sum > fleet_total:                        │
  │    a. Log CRITICAL violation                    │
  │    b. Identify offending agents                 │
  │    c. Trigger remediation (reduce allocations)  │
  │    d. Emit fleet_event with type "violation"    │
  │ 4. If sum > 0.9 * fleet_total:                 │
  │    a. Log WARNING (near capacity)               │
  │    b. Emit fleet_event with type "near-limit"   │
  │ 5. If all OK:                                   │
  │    a. Emit fleet_event with type "health_ok"    │
  │    b. Update dashboard                          │
  └────────────────────────────────────────────────┘
```

### 7.3.2 Remediation Strategy

When a conservation violation is detected:

1. **Identify** — Which agents are over-budget?
2. **Rank** — Use spectral-fleet to rank by criticality
3. **Reduce** — Scale down least-critical agents first
4. **Verify** — Re-check global invariant
5. **Report** — Emit fleet_event with details

The remediation uses the PID controller from agent-homeostasis to smoothly reduce allocations rather than abruptly cutting them:

```rust
// PID-controlled budget reduction
fn remediate(overage: f64, agents: &mut [(AgentId, Budget)]) {
    let pid = PidController::new(1.0, 0.1, 0.05);
    let reduction = pid.compute(overage, 0.0); // drive overage to zero
    
    // Distribute reduction proportionally
    let total_budget: f64 = agents.iter().map(|(_, b)| b.total).sum();
    for (_, budget) in agents {
        let fraction = budget.total / total_budget;
        budget.reduce(reduction * fraction);
    }
}
```

### 7.3.3 Continuous Invariant Proof

For fleets using categorical-agents, the composition of budget operations is formally verified:

```
If agent A has conservation invariant: γA + ηA ≤ BA
And agent B has conservation invariant: γB + ηB ≤ BB
Then composition A⊗B has: (γA+γB) + (ηA+ηB) ≤ BA + BB
```

This means fleets can prove conservation holds for any composition of individually-conserving agents — no runtime check needed for composed operations.

## 7.4 VCG Auction in sunset-ecosystem

### 7.4.1 Overview

sunset-ecosystem uses a Vickrey-Clarke-Groves (VCG) auction for budget allocation. This mechanism is **strategy-proof** — agents have no incentive to misreport their budget needs.

### 7.4.2 Mechanism

```
Given:
  - N agents, each with valuation vi(budget)
  - Total fleet budget B
  
Step 1: Collect bids
  Each agent i submits bid bi = vi(budget)
  
Step 2: Find optimal allocation
  Solve: max Σi vi(budgeti) subject to Σi budgeti ≤ B
  
Step 3: Compute payments (VCG prices)
  Paymenti = Σj≠i vj(allocation_without_i) - Σj≠i vj(allocation_with_i)
  (Agent i pays its "externality" — the harm it causes others by existing)
  
Step 4: Enforce conservation
  Verify Σi budgeti ≤ B
  If violated, scale all allocations proportionally
```

### 7.4.3 Conservation Guarantee

The VCG auction naturally enforces conservation because:
1. The optimization constraint is Σ budgeti ≤ B
2. Over-allocation is infeasible in the optimization
3. Payment computation preserves the allocation
4. Any rounding errors are caught by the database CHECK constraint

### 7.4.4 Example

```
Fleet budget: B = 100
Agents: A, B, C with valuations:
  vA(b) = 2√b   (A has diminishing returns)
  vB(b) = 1.5b  (B has linear returns)
  vC(b) = 3ln(b+1) (C has logarithmic returns)

Optimal allocation (Lagrangian):
  ∂vA/∂bA = ∂vB/∂bB = ∂vC/∂bC = λ
  
  1/√bA = 1.5 = 3/(bC+1) = λ
  
  bA = (1/1.5)² ≈ 0.44
  bB = ... (solved numerically)
  bC = 3/1.5 - 1 = 1.0
  
  Total ≈ 100 (scaled to budget)
```

---

# 8. BATON.md Handoff Protocol

## 8.1 Overview

The BATON.md protocol defines how agents pass work between each other within the ecosystem. It ensures continuity, accountability, and conservation-law compliance across handoffs.

## 8.2 Protocol Steps

```
┌──────────────────────────────────────────────────┐
│                 BATON HANDOFF                     │
│                                                  │
│  1. CLAIM                                        │
│     Agent A claims the baton for task T          │
│     BATON.md: { holder: A, task: T, status:      │
│                  "claimed" }                     │
│                                                  │
│  2. EXECUTE                                      │
│     Agent A performs work, producing output O     │
│     BATON.md: { holder: A, task: T, status:      │
│                  "executing", output: O }        │
│                                                  │
│  3. OUTPUT + NEXT                                │
│     Agent A writes output and names next agent    │
│     BATON.md: { holder: A, task: T, status:      │
│                  "complete", output: O,           │
│                  next: B }                       │
│                                                  │
│  4. VERIFY                                       │
│     Agent B verifies A's output before accepting  │
│     - Conservation invariant check               │
│     - Output schema validation                   │
│     - Integration test pass                      │
│     BATON.md: { holder: B, task: T, status:      │
│                  "verifying" }                   │
│                                                  │
│  5. ACCEPT OR REJECT                             │
│     If valid: B accepts, becomes new holder      │
│     If invalid: B rejects, baton returns to A    │
│                                                  │
│  6. ARCHIVE                                      │
│     Completed batons are archived for audit       │
│     BATON.md: { status: "archived",              │
│                  result: "success|failure" }     │
└──────────────────────────────────────────────────┘
```

## 8.3 BATON.md Format

```markdown
# BATON.md

## Current State
- **Holder:** agent-name
- **Task:** task-description
- **Status:** claimed | executing | complete | verifying | archived
- **Claimed At:** 2026-06-07T19:00:00Z

## Output
[Description of work completed]

## Next
- **Agent:** next-agent-name
- **Instructions:** What the next agent should do

## Budget Impact
- **γ consumed:** 50.0
- **η consumed:** 30.0
- **Conservation:** ✅ verified

## History
| Step | Agent | Status | Timestamp |
|------|-------|--------|-----------|
| 1 | agent-a | claimed | 2026-06-07T19:00:00Z |
| 2 | agent-a | complete | 2026-06-07T19:05:00Z |
| 3 | agent-b | verifying | 2026-06-07T19:06:00Z |
```

## 8.4 Conservation Compliance

Every baton handoff includes a budget impact statement. The receiving agent verifies:
1. The claimed budget consumption is consistent with the output
2. The total γ + η consumed does not exceed the allocated budget
3. The fleet-wide conservation invariant still holds after the handoff

If any check fails, the receiving agent rejects the baton and escalates to fleet-warden.

---

# 9. Appendices

## Appendix A: Repository Quick Reference

| Repository | Layer | Language | Description |
|------------|-------|----------|-------------|
| conservation-law-rs | 1 | Rust | Core invariant library |
| si-core-c | 2 | C | C ABI foundation |
| si-runtime-rs | 2 | Rust | Rust runtime |
| si-runtime-js | 2 | TypeScript | TypeScript/Node runtime |
| si-runtime-python | 2 | Python | Python runtime (PyO3) |
| si-runtime-go | 2 | Go | Go runtime |
| si-runtime-zig | 2 | Zig | Zig runtime |
| si-runtime-wasm | 2 | WASM | WASM runtime |
| si-cli | 3 | Rust | Unified CLI |
| si-fleet-api | 3 | TypeScript | REST API |
| si-registry-rs | 3 | Rust | Local registry |
| ecosystem-dashboard | 3 | TypeScript | Live visualization |
| spectral-fleet | 4 | Rust | Spectral ranking |
| fleet-warden | 4 | Rust | Health checking |
| agent-homeostasis | 4 | Rust | PID control |
| constraint-dynamics | 4 | Rust | Lagrangian mechanics |
| categorical-agents | 4 | Rust | Category theory |
| wasserstein-agents | 4 | Rust | Optimal transport |
| persistent-sheaf | 4 | Rust | Topological analysis |
| ga-core | 4 | Rust | Geometric algebra |
| hodge-consensus | 4 | Rust | Hodge decomposition |
| dial-theory | 4 | Rust | Cultural dynamics |
| tropical-geometry | 4 | Rust | Tropical geometry |
| symplectic-opt | 4 | Rust | Symplectic optimization |
| renormalization-group | 4 | Rust | RG scaling |
| sheaf-coherence | 4 | Rust | Sheaf coherence |
| sunset-ecosystem | 5 | Multiple | Mothership |
| cocapn | 5 | Multiple | Explainability |
| plato-construct | 5 | Multiple | Education |
| open-terminal | 5 | Multiple | Open app |
| open-iterator | 5 | Multiple | Open app |
| open-application | 5 | Multiple | Open app |
| open-vectors | 5 | Multiple | Open app |
| open-parallel | 5 | Multiple | Open app |

## Appendix B: Key Metrics

| Metric | Value |
|--------|-------|
| Total repositories | 3,608 |
| Ecosystem-wide tests | ~4,761 |
| Published Rust crates | 24+ |
| Published Python packages | 4+ |
| Runtime languages | 7 |
| Math libraries | 14 |
| Dashboard panels | 10 |
| CLI commands | 8 |
| API routes | 11 |
| Mothership files | 1,505 |
| Mothership tests | 2,065+ |

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| **γ (gamma)** | Compute energy budget — CPU, memory, inference tokens |
| **η (eta)** | Communication information budget — messages, bandwidth |
| **Conservation invariant** | γ + η ≤ total_budget |
| **Fleet** | A collection of agents sharing a common budget |
| **Agent** | A computational entity with allocated budget |
| **Budget** | A triple (γ, η, total) satisfying the conservation invariant |
| **Homeostasis** | Self-regulation via PID control |
| **Trinity** | Creator + Executor + Arbiter in sunset-ecosystem |
| **VCG Auction** | Strategy-proof budget allocation mechanism |
| **Sheaf** | Mathematical structure for local-to-global consistency |
| **Wasserstein** | Optimal transport distance between distributions |
| **Spectral** | Graph-theoretic ranking via eigenvalues |
| **Hodge** | Decomposition into consensus + gradient + harmonic |
| **BATON** | Agent handoff protocol for work continuity |
| **CAPABILITY.toml** | Declarative agent capability manifest |
| **INTEGRATION.md** | Cross-repository wiring document |

---

*This document is maintained by the SuperInstance core team. For questions or contributions, open an issue in [agent-operations](https://github.com/SuperInstance/agent-operations).*

*Last updated: 2026-06-07*
