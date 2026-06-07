# CAPABILITY.toml Specification

> **Version:** 1.0.0
> **Status:** Active
> **Purpose:** Make every SuperInstance repo self-describing — any human or agent can discover what a crate provides, what it needs, and how to integrate it.

---

## 1. Overview

Every repository in the SuperInstance organization contains a `CAPABILITY.toml` file in its root directory. This file is a machine-readable contract that describes:

- **What the crate provides** (types, functions, traits)
- **What it requires** from other crates
- **How it integrates** with specific crates
- **Onboarding procedures** for humans and agents

This enables:
- **Agents** to autonomously discover integration points and write glue code
- **Humans** to quickly understand a crate's role in the ecosystem
- **Tooling** to build dependency graphs and detect integration opportunities

---

## 2. File Location

```
<repo-root>/
├── CAPABILITY.toml    ← This file
├── Cargo.toml
├── src/
└── ...
```

The file MUST be named exactly `CAPABILITY.toml` and placed in the repository root.

---

## 3. TOML Structure

### 3.1 Top-Level Sections

```toml
[crate]           # Required — identity and classification
[provides]        # Required — what this crate exports
[requires]        # Optional — what this crate needs from others
[integrates.X]    # Optional — named integration with crate X
[onboarding.human] # Optional — human quick-start
[onboarding.agent] # Optional — agent integration guide
```

---

### 3.2 `[crate]` — Identity

Required. Identifies the crate.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Crate name (matches `Cargo.toml`) |
| `version` | string | ✅ | Current version |
| `layer` | string | ✅ | Architectural layer (see §4) |
| `description` | string | ✅ | One-line summary |

```toml
[crate]
name = "conservation-law-rs"
version = "0.1.0"
layer = "conservation"
description = "Conservation laws for agent energy budgets"
```

---

### 3.3 `[provides]` — Exported Capabilities

Required. Declares what this crate offers to consumers.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `capabilities` | array of tables | ✅ | Named capabilities with types |
| `exports` | array of strings | ✅ | Public type/trait/function names |

Each capability entry:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Capability identifier |
| `type` | string | ✅ | One of: `struct`, `trait`, `fn`, `module`, `enum` |
| `description` | string | ✅ | What this capability does |

```toml
[provides]
capabilities = [
  { name = "conservation_law", type = "struct", description = "Validates γ+H=C for any agent" },
  { name = "energy_budget", type = "struct", description = "Allocates energy across agents" },
]
exports = [
  "ConservationLaw", "AgentEnergy", "EnergyBudget", "ViolationReport"
]
```

---

### 3.4 `[requires]` — Dependencies

Optional. Declares what this crate needs from others. Split into:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `required` | array of tables | ❌ | Hard dependencies (crate won't compile without) |
| `optional` | array of tables | ❌ | Soft dependencies (feature-gated or enhancement) |

Each dependency entry:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `crate` | string | ✅ | Target crate name |
| `reason` | string | ✅ | Why this dependency exists |
| `import` | string | ❌ | The specific import path |
| `feature` | string | ❌ | Cargo feature that enables this |

```toml
[requires]
optional = [
  { crate = "fleet-warden-rs", reason = "Anomaly detection triggers conservation audits", import = "fleet_integration::FleetConservation" },
]
```

---

### 3.5 `[integrates.X]` — Named Integrations

Optional. One section per integration partner. `X` is a short identifier for the integration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `crate` | string | ✅ | Target crate name |
| `module` | string | ✅ | Module within this crate that implements the integration |
| `description` | string | ✅ | What this integration achieves |
| `human_steps` | array of strings | ❌ | Step-by-step instructions for humans |
| `agent_steps` | array of strings | ❌ | Step-by-step instructions for agents |

```toml
[integrates.fleet_warden]
crate = "fleet-warden-rs"
module = "fleet_integration"
description = "Fleet conservation: track energy budget across agents"
human_steps = [
  "1. cargo add fleet-warden",
  "2. use conservation_law::fleet_integration::FleetConservation",
]
agent_steps = [
  "Import fleet_integration module from conservation-law-rs",
  "Initialize FleetConservation with agent count and total budget",
]
```

---

### 3.6 `[onboarding.human]` — Human Quick Start

Optional. Helps humans get started quickly.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `quick_start` | string | ✅ | One-line install command |
| `example` | string | ✅ | Runnable example code |

---

### 3.7 `[onboarding.agent]` — Agent Integration Guide

Optional. Structured information for AI agents.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `context_needed` | array of strings | ✅ | What context the agent must gather |
| `api_surface` | array of strings | ✅ | Key API calls to know |
| `integration_pattern` | string | ✅ | High-level pattern description |

---

## 4. Layer Taxonomy

The `layer` field classifies the crate's role in the architecture:

| Layer | Description | Examples |
|-------|-------------|---------|
| `conservation` | Energy/momentum conservation laws | conservation-law-rs |
| `spectral` | Eigenvalue methods, spectral analysis | spectral-fleet-rs |
| `temporal` | Scheduling, deadlines, time management | t-minus-rs |
| `monitoring` | System monitoring, anomaly detection | fleet-warden-rs |
| `composition` | Category-theoretic agent composition | categorical-agents-rs |
| `distribution` | Optimal transport, distribution coordination | wasserstein-agents-rs |
| `security` | Cryptographic primitives | lattice-crypto-rs |
| `topology` | Topological data analysis | persistent-sheaf-rs |
| `music` | Music generation and arrangement | self-improving-band |
| `meta` | Documentation, tooling, operations | agent-operations |
| `transport` | Optimal transport algorithms | optimal-transport-rs |
| `identity` | Agent identity and authentication | agent-identity-rs |
| `handshake` | Secure agent handshake protocols | agent-handshake-rs |

---

## 5. Conventions

### 5.1 Naming

- Integration section names (`[integrates.X]`): use `snake_case` identifiers
- Capability names: use `snake_case`
- Export names: match the actual Rust public name (usually `CamelCase`)

### 5.2 Steps

- `human_steps`: Numbered list with code inline
- `agent_steps`: Imperative sentences describing the logical operation

### 5.3 Accuracy

- `exports` MUST match actual `pub` items in `src/lib.rs`
- `capabilities` type field MUST match the Rust construct (`struct`, `trait`, `fn`, `enum`, `module`)
- `integrates.X.module` MUST be an actual module in the crate

### 5.4 Versioning

When updating `CAPABILITY.toml`:
- Update the `version` field to match `Cargo.toml`
- Add new capabilities when new public items are added
- Mark removed items — do not silently delete them

---

## 6. Discovery Tool

The `tools/discover_integrations.py` script in `agent-operations` scans directories for `CAPABILITY.toml` files, builds a dependency graph, and identifies integration opportunities.

Usage:
```bash
python3 tools/discover_integrations.py /path/to/repos
```

---

## 7. Example: Full CAPABILITY.toml

```toml
[crate]
name = "conservation-law-rs"
version = "0.1.0"
layer = "conservation"
description = "Conservation laws (γ+H=C) for agent energy budgets"

[provides]
capabilities = [
  { name = "conservation_law", type = "struct", description = "Validates γ+H=C for any agent" },
  { name = "energy_budget", type = "struct", description = "Allocates energy across agents" },
  { name = "violation_detection", type = "fn", description = "Detects when conservation is violated" }
]
exports = [
  "ConservationLaw", "AgentEnergy", "EnergyBudget", "ViolationReport"
]

[requires]
optional = [
  { crate = "fleet-warden-rs", reason = "Anomaly detection triggers conservation audits", import = "fleet_integration::FleetConservation" },
  { crate = "t-minus-rs", reason = "Deadline-aware energy transfers", import = "deadline::DeadlinePropagation" }
]

[integrates.fleet_warden]
crate = "fleet-warden-rs"
module = "fleet_integration"
description = "Fleet conservation: track energy budget across agents with anomaly-triggered audits"
human_steps = [
  "1. cargo add fleet-warden",
  "2. use conservation_law::fleet_integration::FleetConservation",
  "3. Create FleetConservation::new(agent_count, total_budget)",
  "4. Call .audit_fleet(metrics) to check conservation",
  "5. Call .transfer_with_guard(from, to, amount) for safe transfers"
]
agent_steps = [
  "Import fleet_integration module from conservation-law-rs",
  "Initialize FleetConservation with agent count and total energy budget",
  "Wire anomaly detector output into audit_fleet() input",
  "Use transfer_with_guard() instead of direct energy transfers",
  "Monitor ConservationReport.violations for corrective action"
]

[onboarding.human]
quick_start = "cargo add conservation-law"
example = """
use conservation_law::ConservationLaw;
let law = ConservationLaw::new(100.0);
let agent = AgentEnergy::new(50.0, 10.0);
assert!(law.validate(&agent));
"""

[onboarding.agent]
context_needed = ["agent_count", "total_energy_budget"]
api_surface = ["ConservationLaw::new(total_budget)", "AgentEnergy::new(gamma, eta)", "validate(agent) -> bool"]
integration_pattern = "Initialize with total budget, create agents with energy allocations, validate before every state transition"
```

---

## 8. Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-06-07 | Initial specification |
