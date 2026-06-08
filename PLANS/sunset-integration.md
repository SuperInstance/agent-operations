# Sunset Ecosystem Integration Plan

**Repo:** `SuperInstance/sunset-ecosystem`  
**Analyzed:** 2026-06-07  
**File count:** 1,413 (476 test files, 265 fleet/, 118 superinstance-ffi/, 89 swarm/, 41 nerve/, 22 sunset/, 20 logos/)  
**Tests:** 2,215+ (badge); 476 test files  
**Status of existing integration work:** CAPABILITY.toml complete; INTEGRATION.md started; `fleet/conservation_spectral_bridge.py` is the live wire to conservation-law-rs and spectral-fleet-rs  
**Language:** Python primary; Rust C-ABI FFI via `superinstance-ffi/` (Cargo crate); C bloom filter + ring buffer in `nerve/`

---

## Executive Context

sunset-ecosystem is not a satellite. It is the mothership. The 1,413-file repo contains the agent lifecycle (EGG→COMPETE→SURVIVE→BREED→SUNSET→ARCHIVE), the evolutionary breeding engine (PBFT-consensus + MAP-Elites QD), the spectral genome representation, the Hebbian mesh, the thermal device auction, the CRDT vector gossip, the fleet conductor, and the FLAME decision journal. Every other SuperInstance repo either feeds into sunset or is consumed by it.

The good news: the CAPABILITY.toml is already written and comprehensive. The `fleet/conservation_spectral_bridge.py` already bridges to `conservation-law-rs` and `spectral-fleet-rs`. The `FleetBridgeServer` already exposes an HTTP API on `:8850`. The `superinstance-ffi/` Rust crate already exports C-ABI functions that the rest of the runtime needs.

The integration work remaining is: **formalize the wiring** that exists informally, **push sunset into the Supabase fleet registry**, **surface its 29 capability modules to si-cli**, and **extract 9 modules into standalone crates** before sunset grows too large to refactor cleanly.

---

## Table of Contents

1. [Sunset ↔ Runtime Libraries](#1-sunset--runtime-libraries)
2. [Sunset ↔ Supabase Fleet Registry](#2-sunset--supabase-fleet-registry)
3. [Sunset ↔ si-cli](#3-sunset--si-cli)
4. [Sunset ↔ si-fleet-api](#4-sunset--si-fleet-api)
5. [Module Extraction Candidates](#5-module-extraction-candidates)
6. [Cross-Repo INTEGRATION.md Priorities](#6-cross-repo-integrationmd-priorities)
7. [README Rewrite Plan](#7-readme-rewrite-plan)
8. [Implementation Sequence](#8-implementation-sequence)

---

## 1. Sunset ↔ Runtime Libraries

sunset-ecosystem maps to the 7-language runtime across all five architectural layers. The mapping is not 1:1 — some sunset modules span multiple layers, and some runtime modules have no sunset counterpart yet.

### 1.1 Layer Map

```
LAYER 1 — PHYSICS (conservation)
  sunset module       ↔  runtime module
  ─────────────────────────────────────────────────────
  swarm/thermal.py            →  si-runtime-go/conservation.go
    ThermalBudget                   Budget (Total, Gamma, Eta)
    DeviceBudget.max_agents         Budget.Total
    DeviceBudget.current_agents     Budget.Gamma
    (idle slots)                    Budget.Eta
  
  swarm/constraint_bridge.py  →  conservation-law-rs (superinstance-ffi.h)
    ConstraintBridge.snap_vector    constraint_check(value, lower, upper)
    ConstraintBridge.eisenstein_norm  eisenstein_norm(a, b)
    ConstraintBridge.holonomy_check   holonomy_check(states, len, threshold)
  
  fleet/conservation_spectral_bridge.py  ←→  conservation-law-rs + spectral-fleet-rs
    ConservationSpectralEngine      FleetConservation (Rust)
    ConservationRatioMonitor        AuditResult (Go)
    [EXISTING — extend, do not rebuild]

LAYER 2 — COORDINATION (spectral)
  swarm/spectral_breeding.py  →  spectral-fleet-rs
    SpectralGenome.spectrum         power_iteration eigenvectors
    SpectralBreeder.evaluate        l2_norm, dot product ops
    crossover (spectral convolution)  → pointwise mult on eigenvector space

  swarm/hebbian_mesh.py       →  spectral-fleet-rs (Hebbian intercept)
    HebbianAffinity.update()        Hebbian weight update (ΔC_ij ∝ η·x_i·x_j)
    HebbianMeshLayer.chaos_factor   → fleet γ+H Hebbian intercept (+13%)
    DELTA_SUCCESS / DELTA_NOVELTY   feed into C_ij coupling matrix entries

  swarm/fleet_bft_qd.py       →  si-runtime-go/spectral.go
    FleetBFTNetwork.cluster()       spectral_clustering (k-means on eigenvectors)
    QDArchive.get_niche()           Fiedler vector clustering
    BehaviorDescriptor.features     AdjacencyMatrix affinity input

LAYER 3 — COMPOSITION (category)
  swarm/lifecycle_fsm.py      →  categorical-agents-rs (planned)
    AgentLifecycleFSM transitions   morphism composition
    LifecycleState enum             category objects
    TransitionRecord                morphism record

  nexus/fleet_conductor_v2.py →  si-runtime-go/fleet.go
    FleetConductorV2                Fleet struct
    ConductorConfig.enable_*        Fleet.AddAgent with capability set
    SubsystemWrapper                Agent + Budget + Capability

LAYER 4 — TIMING (temporal)
  nerve/metronome.py          →  t-minus-rs (planned)
    LocalMetronome.bpm              t-minus deadline propagation
    MetronomeScheduler              temporal invariant enforcement
    TickAsTask                      task deadline record

  fleet_scheduler_state.json  →  t-minus-rs job registry
    INTERVAL / CRON / ONESHOT jobs  → temporal constraint types

LAYER 5 — PROOF (verification)
  logos/signed_wal.py         →  witness-topology-rs
    WALEntry.signature              cryptographic provenance
    SignedWAL.append()              immutable tile commitment
  
  logos/decision_journal.py   →  PLATO tiles (P2 Gate)
    Decision(why, what, expected, actual)  → tile submission
    FLAME log entries               → provenance chain entries
```

### 1.2 FFI Layer — superinstance-ffi ↔ si-core-c

The `superinstance-ffi/` Rust crate and `si-core-c` should be the same thing. Currently they are parallel implementations of the same C API. The path forward:

```
superinstance-ffi.h (current)   si-core-c/si_agent.h (SUPERINSTANCE_RUNTIME.md §4.5)
────────────────────────────────────────────────────────────────────────────────────
eisenstein_norm(a, b)            si_budget_allocate / constraint_check
laman_check_subset(v, e)         (missing in si-core-c — add)
laman_is_rigid(v, e)             (missing in si-core-c — add)
holonomy_check(states, len, t)   (missing in si-core-c — add)
pythagorean48_encode(n, d)       (missing in si-core-c — add)
constraint_check(v, lo, hi)      (exists in planned si-core-c API)
constraint_violation(v, lo, hi)  (exists in planned si-core-c API)
spline_interpolate(p0,p1,m0,m1,t) (missing — add)
deadband_filter(v, last, db)     (missing — add: matches deadband-zig API)
manhattan_distance(a, b, dim)    (missing — add)
cascade_match(q, c, n, d, t, k)  (missing — add)
```

**Action:** sunset's `superinstance-ffi/` is the authoritative C header. The si-core-c planned API in `SUPERINSTANCE_RUNTIME.md §4.5` should be expanded to include all 12 functions from `superinstance_ffi.h`. Use the sunset Rust crate as the implementation source.

### 1.3 Language-by-Language Integration Status

| Runtime | Status | What Exists | What's Missing |
|---------|--------|-------------|----------------|
| **Rust** | Partial | `superinstance-ffi/` Cargo crate exports 12 C-ABI functions | Publish to crates.io as `superinstance-ffi`; add Cargo feature for `no_std` |
| **Python** | Live | `swarm/constraint_bridge.py` calls FFI; `fleet/conservation_spectral_bridge.py` bridges conservation+spectral | Wire `ThermalBudget` → `fleet_budgets` table; add beacon to Keeper |
| **Go** | Gap | `si-runtime-go/conservation.go` Budget struct exists | No Python↔Go bridge; add heartbeat client that reports ThermalBudget as AgentBudget |
| **TypeScript** | Partial | `schemas/fleet-health.ts` ServiceStatus/AgentStatus | Add SunsetAgentStatus to schemas (trinity_score, lifecycle_state, generation) |
| **C** | Partial | `nerve/bloom_filter.c`, `nerve/ring_buffer.c` (compiled .so) | Expose as si-core-c functions; add to si-core-c header |
| **Zig** | None | — | Add Zig wrapper for `deadband_filter` (matches `deadband-zig` API exactly) |
| **WASM** | None | — | WASM build of trinity_score + constraint_check (pure math, no I/O — builds clean) |

---

## 2. Sunset ↔ Supabase Fleet Registry

### 2.1 Which Sunset Modules Should Register as Capabilities

Every entry in `CAPABILITY.toml [provides]` is a fleet capability. The 29 named capabilities should each get a row in the `capabilities` table.

**Priority registration order** (highest value first):

| Priority | Capability Name | Module | Why First |
|----------|----------------|---------|-----------|
| P0 | `si-fleet-api` | `fleet/fleet_api.py` | REST server — si-cli needs to discover its endpoints |
| P0 | `conservation-spectral-bridge` | `fleet/conservation_spectral_bridge.py` | Live wire to conservation law — already built |
| P0 | `swarm-breeding` | `swarm/breeder_daemon_v2.py` | The core loop — must be visible to fleet routing |
| P1 | `agent-lifecycle` | `swarm/lifecycle_fsm.py` | State machine drives `fleet_events` records |
| P1 | `thermal-auction` | `swarm/thermal_auction.py` | Maps directly to `fleet_budgets.gamma` / device slots |
| P1 | `mesh-gossip` | `swarm/mesh_vector_gossip.py` | Cross-node CRDT sync |
| P2 | `nerve-forward-inference` | `nerve/room_grid.py` | Inference engine — less urgent for registry |
| P2 | `logos-journals` | `logos/decision_journal.py` | Decision audit trail → `fleet_events` |
| P2 | `si-core-c-ffi` | `superinstance-ffi/` | FFI bindings — register once, used everywhere |
| P3 | `tide-pool-viz` | `logos/tide_pool_viz.py` | Visualization — low urgency |

### 2.2 repos Table — Sunset Row

```sql
INSERT INTO repos (name, org, layer, language, version, description,
                   github_url, health_status, capability_toml)
VALUES (
  'sunset-ecosystem',
  'SuperInstance',
  'orchestration',
  'Python',
  '0.1.0',
  'Trinity-architecture agent ecosystem: ethos × pathos × logos.
   Agents breed, compete, and sunset with dignity.',
  'https://github.com/SuperInstance/sunset-ecosystem',
  'green',
  '{ ... parsed CAPABILITY.toml ... }'::jsonb
);
```

### 2.3 fleet_budgets — Mapping ThermalBudget to Budget

The `ThermalBudget` in `swarm/thermal.py` is the same concept as the `Budget` struct in `si-runtime-go/conservation.go`. The mapping:

```python
# sunset-ecosystem: swarm/thermal.py
DEFAULT_BUDGETS = {
    DeviceType.GPU:  9,    # max agents
    DeviceType.CPU:  36,
    DeviceType.IGPU: 14,
    DeviceType.NPU:  6,
}
# ThermalBudget.total = 65 agent-slots
# ThermalBudget.active (occupied slots) = Gamma
# ThermalBudget.idle (free slots) = Eta
```

**fleet_budgets row per vessel per device:**

```sql
-- One row per vessel × device combination
INSERT INTO fleet_budgets (agent_id, vessel_id, total, gamma, eta, unit, circuit)
VALUES
  ('sunset:oracle1:gpu',  'oracle1', 9,  <active_gpu_agents>,  <idle_gpu_slots>,  'agent-slots', 'closed'),
  ('sunset:oracle1:cpu',  'oracle1', 36, <active_cpu_agents>,  <idle_cpu_slots>,  'agent-slots', 'closed'),
  ('sunset:oracle1:igpu', 'oracle1', 14, <active_igpu_agents>, <idle_igpu_slots>, 'agent-slots', 'closed'),
  ('sunset:oracle1:npu',  'oracle1', 6,  <active_npu_agents>,  <idle_npu_slots>,  'agent-slots', 'closed');
```

**Heartbeat pusher (add to `claw_fleet_bridge.py`):**

```python
def _push_budget_heartbeat(thermal: ThermalBudget, vessel_id: str) -> None:
    """Push current thermal state to fleet registry."""
    import psycopg2, os
    dsn = os.environ["SUPERINSTANCE_REGISTRY_URL"]
    for device_type, budget in thermal.budgets.items():
        agent_id = f"sunset:{vessel_id}:{device_type.value}"
        with psycopg2.connect(dsn) as conn:
            conn.execute("""
                INSERT INTO fleet_budgets (agent_id, vessel_id, total, gamma, eta, unit, updated_at)
                VALUES (%s, %s, %s, %s, %s, 'agent-slots', now())
                ON CONFLICT (agent_id)
                DO UPDATE SET gamma=EXCLUDED.gamma, eta=EXCLUDED.eta, updated_at=now()
            """, (agent_id, vessel_id, budget.max_agents,
                  budget.current_agents, budget.max_agents - budget.current_agents))
```

### 2.4 fleet_events — Lifecycle FSM → Audit Log

Every `AgentLifecycleFSM` transition should emit a `fleet_events` record. Add to `swarm/lifecycle_fsm.py`:

```python
# After transition succeeds, in AgentLifecycleFSM.transition():
def _emit_event(self, record: TransitionRecord) -> None:
    """Emit lifecycle transition to fleet_events."""
    payload = {
        "from_state": record.from_state.name,
        "to_state":   record.to_state.name,
        "reason":     record.reason,
        "agent_id":   self.agent_id,
    }
    event_type = {
        (LifecycleState.EGG,     LifecycleState.COMPETE): "agent_spawn",
        (LifecycleState.COMPETE, LifecycleState.SUNSET):  "agent_sunset",
        (LifecycleState.SURVIVE, LifecycleState.BREED):   "agent_breed",
        (LifecycleState.SUNSET,  LifecycleState.ARCHIVE): "agent_archive",
    }.get((record.from_state, record.to_state), "lifecycle_transition")
    _fleet_events_insert(event_type, self.agent_id, payload)
```

### 2.5 capabilities Table — Batch Insert

Run once after registering the repo:

```python
# tools/register_sunset_capabilities.py
import tomllib, psycopg2, os, json

with open("CAPABILITY.toml", "rb") as f:
    cap = tomllib.load(f)

repo_id = "<uuid from repos table>"
dsn = os.environ["SUPERINSTANCE_REGISTRY_URL"]

with psycopg2.connect(dsn) as conn:
    for c in cap["provides"]["capabilities"]:
        conn.execute("""
            INSERT INTO capabilities (repo_id, name, type, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (repo_id, name) DO UPDATE
              SET type=EXCLUDED.type, description=EXCLUDED.description
        """, (repo_id, c["name"], c["type"], c.get("description", "")))
```

---

## 3. Sunset ↔ si-cli

### 3.1 Discovery via FleetBridgeServer

sunset already exposes `FleetBridgeServer` on `:8850`. si-cli should auto-discover this when sunset is a registered fleet member.

```bash
# si-cli commands that work once sunset registers with Keeper:

# List all sunset capabilities
si cap list --repo sunset-ecosystem

# Match a task to the right sunset module
si fleet match --require "swarm-breeding,thermal-auction" --threshold 0.8
# → returns: agent:oracle1:sunset (score 1.0, matched all)

# Check sunset's thermal budget
si budget status "sunset:oracle1:gpu"
# Total:  9.0 agent-slots
# Gamma:  6.0  (66% — 6 agents breeding)
# Eta:    3.0  (33% — 3 GPU slots idle)
# Circuit: closed

# Trigger a breeding round via si-cli
si fleet call sunset-ecosystem breed \
  --payload '{"parent_ids": ["a1b2c3", "d4e5f6"], "mutation_rate": 0.05}'

# Audit sunset's conservation status
si budget audit --repo sunset-ecosystem

# Watch sunset lifecycle events in real time
si fleet events --agent-prefix "sunset:" --follow

# Run sunset drift detection
si fleet call sunset-ecosystem triage/drift --scope all
```

### 3.2 Keeper Announcement

Add a Keeper beacon to `claw_fleet_bridge.py` or the FleetConductorV2 startup:

```python
# Add to FleetBridgeServer.start():
def _announce_to_keeper(self) -> None:
    """Announce sunset-ecosystem to Keeper at :8900."""
    import requests
    keeper_url = os.environ.get("KEEPER_URL", "http://oracle1:8900")
    requests.post(f"{keeper_url}/v1/announce", json={
        "agent_id": f"sunset:{self._vessel_id}:fleet-bridge",
        "vessel_id": self._vessel_id,
        "capabilities": [c["name"] for c in self._capability_toml["provides"]["capabilities"]],
        "budget_total": 65,  # 9+36+14+6 agent-slots
        "endpoints": [f"http://{self.host}:{self.port}"],
        "heartbeat_interval_s": 30,
    })
```

### 3.3 si-cli Audit Command

The `si budget audit` command should also run sunset's built-in drift detection:

```bash
si fleet audit sunset-ecosystem
# → runs: triage.drift_detect.detect_drift()
# → emits DriftReport severity summary
# → pushes findings to fleet_events (event_type='audit_pass' or 'audit_fail')
```

### 3.4 CAPABILITY.toml as CLI Contract

si-cli reads CAPABILITY.toml from the registry (via `capabilities` table) and renders:

```
$ si cap info sunset-ecosystem
sunset-ecosystem (v0.1.0) — orchestration layer
  29 capabilities, 4 modules, 25 functions/protocols

  Layer: orchestration
  Language: Python
  FFI: Rust C-ABI (superinstance-ffi)
  Tests: 2215+ passing

  Capabilities:
    P0 — si-fleet-api         (FastAPI REST server — endpoint discovery)
    P0 — conservation-spectral-bridge  (live wire to conservation-law-rs)
    P0 — swarm-breeding       (PBFT+QD evolutionary loop)
    P1 — agent-lifecycle      (EGG→COMPETE→SURVIVE→BREED→SUNSET→ARCHIVE FSM)
    ...
```

---

## 4. Sunset ↔ si-fleet-api

### 4.1 Existing Endpoints (already in `fleet/fleet_api.py`)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Service liveness |
| GET | `/status` | Fleet snapshot |
| GET | `/agents` | List active agents with trinity scores |
| POST | `/memory/write` | Write vector to mesh |
| POST | `/memory/query` | KNN query against mesh |
| GET | `/swarm/knn` | Agent KNN by vector similarity |
| GET | `/cache/stats` | Cache statistics |

### 4.2 New Endpoints to Add (Priority Order)

**P0 — Breeding and Lifecycle:**

```
POST /swarm/breed
  Body: { parent_ids: [str], mutation_rate: float, strategy: "spectral"|"hebbian"|"qd" }
  Returns: { child_id: str, genome_hash: str, trinity_initial: {e, p, l} }
  Maps to: swarm/breeder_daemon_v2.py BreederDaemonV2.step()

GET /swarm/agents/{agent_id}
  Returns: { id, lifecycle_state, trinity_score, generation, thermal_device, gamma_used }
  Maps to: AgentLifecycleFSM + ThermalBudget

POST /swarm/sunset/{agent_id}
  Body: { reason: str, archive: bool }
  Maps to: AgentLifecycleFSM.transition(SUNSET)
  Side effect: emit fleet_events record

GET /swarm/leaderboard?top=20
  Returns: sorted agents by trinity_score descending
  Maps to: swarm/tournament.py
```

**P1 — Conservation and Spectral:**

```
GET /conservation/status
  Returns: { fleet_gamma: float, fleet_eta: float, hebbian_intercept: float,
             circuit: str, anomalous_agents: [str] }
  Maps to: fleet/conservation_spectral_bridge.py ConservationSpectralEngine

GET /spectral/fingerprint
  Returns: { eigenvalues: [float], fiedler_vector: [float], spectral_gap: float,
             entropy_H: float, conservation_budget: float, n_agents: int }
  Maps to: SpectralFingerprint from conservation_spectral_bridge

POST /conservation/audit
  Returns: AuditResult (valid, violations, fleet_gamma, fleet_eta)
  Maps to: Go Audit() equivalent in Python
```

**P2 — Mesh and Gossip:**

```
GET /mesh/peers
  Returns: [{ peer_id, affinity, last_seen, blacklisted }]
  Maps to: swarm/hebbian_mesh.py HebbianMeshLayer

POST /mesh/gossip
  Body: GossipDigest (delta batch)
  Maps to: swarm/mesh_vector_gossip.py MeshVectorGossip.push_delta()

GET /mesh/diversity
  Returns: { diversity_score: float, chaos_factor: float, population_size: int,
             centroid_count: int }
  Maps to: swarm/hdc_novelty.py + HebbianMeshLayer.get_diversity_score()
```

**P3 — Tide Pool and Journals:**

```
GET /tide-pool/snapshot
  Returns: FleetSnapshot (n_agents, mean_fitness, diversity, thermal_state, recent_events)
  Maps to: logos/tide_pool_viz.py TidePoolVisualizer.generate_snapshot()

GET /tide-pool/render?format=html|ascii
  Returns: rendered visualization string
  Maps to: TidePoolVisualizer.render_html() or render_ascii()

GET /decisions?since=<timestamp>&scope=<agent_id>&limit=50
  Returns: [Decision] list (FLAME format)
  Maps to: logos/decision_journal.py get_decision_history()

POST /decisions
  Body: Decision (why, what, expected, scope, confidence)
  Maps to: log_human_command()
```

### 4.3 Common Response Envelope

Add the fleet standard envelope to `fleet/fleet_api.py`:

```python
# Add to fleet/fleet_api.py
from fastapi.responses import JSONResponse

def fleet_response(data: dict, confidence: float = 1.0) -> JSONResponse:
    return JSONResponse({
        "status": "success",
        "data": data,
        "confidence": confidence,
        "provenance": "sunset-ecosystem",
        "timestamp": time.time(),
    })
```

---

## 5. Module Extraction Candidates

The 89-file swarm/ and 265-file fleet/ are large enough to create maintenance friction. Nine modules are clean enough to extract now; the rest should wait for Construct API v2.

**Extraction criteria used:** (1) clear public interface with ≤5 external imports, (2) >1,000 lines of tested code, (3) useful in isolation outside sunset, (4) no circular imports with parent.

### 5.1 Extract Now (Ready)

| Candidate Repo | Source Files | Tests | Rationale |
|----------------|-------------|-------|-----------|
| `superinstance-ffi` | `superinstance-ffi/` Rust crate | `tests/test_superinstance_ffi*.py` | Already a Cargo crate; publish to crates.io as `superinstance-ffi`. The C header is the canonical contract for the entire ecosystem's constraint layer. |
| `agent-lifecycle-py` | `swarm/lifecycle_fsm.py` | `tests/test_lifecycle*.py` | Self-contained FSM with zero external deps. 6 states, 8 transitions, full transition log. Every fleet member needs this. |
| `fleet-journal-py` | `logos/decision_journal.py`, `logos/signed_wal.py`, `logos/wal_index.py`, `logos/wal_query.py` | `tests/test_*wal*.py`, `tests/test_decision*.py` | FLAME format + SignedWAL is a complete audit system. Import: `cryptography` only. |
| `fleet-thermal-py` | `swarm/thermal.py`, `swarm/thermal_auction.py`, `swarm/async_thermal.py` | `tests/test_thermal*.py` | VCG device auction + per-device budget tracking. No ML deps. Useful for any fleet with heterogeneous hardware. |

### 5.2 Extract After Testing Stabilizes (6-8 weeks)

| Candidate Repo | Source Files | Key Dependency | Extraction Blocker |
|----------------|-------------|---------------|-------------------|
| `spectral-breeding-py` | `swarm/spectral_breeding.py` | numpy, spectral-fleet-rs | Need to formalize spectral-fleet-rs Python bindings first |
| `fleet-bft-qd-py` | `swarm/fleet_bft_qd.py` | numpy, mesh_vector_tables | 39KB file — needs unit decomposition before extraction |
| `fleet-mesh-py` | `swarm/mesh_vector_tables.py`, `swarm/crdt_merge.py`, `swarm/mesh_vector_gossip.py` | numpy, turbovec | Arrow Flight dependency needs optional-ization |
| `tide-pool-py` | `logos/tide_pool_viz.py` | html templates, dataclasses | Straightforward; blocked only by branding decisions |

### 5.3 Do Not Extract (Keep in Monorepo)

| Module | Reason to Keep |
|--------|---------------|
| `swarm/breeder_daemon_v2.py` (76KB) | Central coordinator; imports 20+ modules — extraction would just move complexity |
| `nexus/fleet_conductor_v2.py` (57KB) | Same: imports everything |
| `nerve/room_grid.py` (30KB) | Tightly coupled to JEPA CUDA kernels in same directory |
| `swarm/flux_vector_table.py` | Depends on `turbovec` which is not yet stable API |

### 5.4 lau-constellation Comparison

When extracting lau-constellation's 6 tools, the pattern was:
1. Identify files with ≤3 external imports
2. Check that tests mock all inter-module calls
3. Create new repo from template
4. Copy files, run tests
5. Add CAPABILITY.toml
6. Publish

Apply the same pattern here. The 4 "Extract Now" candidates all pass the ≤3 external import test.

---

## 6. Cross-Repo INTEGRATION.md Priorities

These are the INTEGRATION.md files that need to be written or updated, ordered by how much integration value each unlocks.

### Priority 1 — Unblock the conservation law bridge (1 week)

**File:** `sunset-ecosystem/fleet/conservation_spectral_bridge.py` INTEGRATION.md  
**Write in:** `sunset-ecosystem/fleet/CONSERVATION_SPECTRAL_BRIDGE.md`

The bridge already exists but has no doc. This is the highest-value documentation gap. Engineers looking to add conservation enforcement to a new module have no starting point.

Content to cover:
- What `ConservationSpectralEngine` does: bridges `swarm/thermal.py` ThermalBudget → `conservation-law-rs` FleetConservation → `spectral-fleet-rs` AdjacencyMatrix
- How to add a new subsystem to the conservation monitor
- The Hebbian intercept shift (+13%) and how `hebbian_mesh.py` feeds into it
- When the circuit breaker trips and what to do

**File:** `agent-operations/INTEGRATION_NOTES/sunset-conservation.md`  
Add a cross-reference: "sunset-ecosystem provides `conservation-spectral-bridge`; conservation-law-rs provides `FleetConservation`. They are already wired. Do not add a new bridge — extend the existing one."

### Priority 2 — Formalize the FFI contract (1 week)

**File:** `sunset-ecosystem/superinstance-ffi/INTEGRATION.md`

The 12 functions in `superinstance_ffi.h` are the C-ABI contract for the entire ecosystem's constraint layer. Any language that wants to use Eisenstein norms, Laman rigidity, holonomy checks, or Pythagorean encoding calls these. The INTEGRATION.md must specify:
- Function signatures with units (see header — already clean)
- Mock vs. real loading (the `superinstance_ffi_mock.py` pattern)
- How to add a new function (add to .h, implement in Rust, re-run `cargo build --release`, copy .so)
- Which sunset modules use which functions

**File:** `si-core-c/INTEGRATION.md` (create)  
Cross-reference: "superinstance-ffi/ in sunset-ecosystem is the authoritative implementation. si-core-c should re-export the same functions. If adding a function, add it to both headers."

### Priority 3 — Lifecycle FSM adoption (2 weeks)

**File:** `sunset-ecosystem/swarm/lifecycle_fsm.py` → `agent-lifecycle-py/INTEGRATION.md`

After extraction (§5.1), write the INTEGRATION.md covering:
- The 6 states and 8 valid transitions
- How to hook `_emit_event` to fleet_events
- How other fleet members can observe a sunset agent's state via Keeper
- How t-minus-rs deadline propagation maps onto the FSM transitions

**File:** `agent-operations/INTEGRATION_NOTES/agent-lifecycle.md`  
This is the pattern document for all future fleet members. Every repo that has agents should reference this.

### Priority 4 — Nerve/RoomGrid ↔ si-runtime runtimes (3 weeks)

**File:** `sunset-ecosystem/nerve/INTEGRATION.md`

nerve/ is the hardest integration because it has three backends (CUDA, Rust persistent, numpy) selected at runtime. INTEGRATION.md must cover:
- Backend selection logic and thresholds (RUST_ONESHOT_THRESHOLD=500, CUDA_THRESHOLD=1000)
- How to add a new backend
- How the Rust `libjepa_kernel.so` persistent API works (jepa_grid_create, jepa_grid_tick, jepa_grid_destroy) and how it maps to si-runtime-go/cell.go Grid abstraction
- JEPA architecture and how WorldModel calibration maps to Cell.EquilibriumCheck

### Priority 5 — Mesh gossip ↔ CRDT documentation (3 weeks)

**File:** `sunset-ecosystem/swarm/mesh_vector_gossip.py` → INTEGRATION.md  

The CRDT anti-entropy gossip is the cross-node synchronization layer. It is tightly coupled to `arrow_flight_mesh.py` (Apache Arrow Flight) and `mesh_vector_tables.py`. INTEGRATION.md should cover:
- GossipDigest → DeltaBatch → merge cycle
- How MeshVectorTable.get_sync_payload() integrates with gossip
- How HebbianMeshLayer modulates routing chaos from diversity
- Fleet registry: how gossip peers are discovered (currently via config; should use Keeper :8900)

### Priority 6 — Decision journal ↔ PLATO tiles (4 weeks)

**File:** `sunset-ecosystem/logos/INTEGRATION.md`

Decision journal entries (FLAME format) should become PLATO tiles in the `agent.behavior` room (P2 Gate). INTEGRATION.md covers:
- Decision → Tile mapping (why→question, what→answer, confidence→blind_width)
- How to configure the journal to auto-submit to PLATO :8847
- The signed_wal.py provenance chain → PLATO provenance chain equivalence
- tide_pool_viz.py → WebSocket push to PLATO dashboard (future)

---

## 7. README Rewrite Plan

**Current state:** 213 lines. Covers: what it is, 30-second quickstart, feature table, and a module inventory table stub (truncated). Missing: real architecture depth, module-by-module API reference, integration guide for other fleet repos, test strategy, configuration reference, deployment.

**Target:** 800+ lines. Reader profile: (1) engineer from another SuperInstance repo trying to integrate, (2) new contributor adding a breeding algorithm, (3) Forgemaster GPU node trying to run a breeding round.

### Section Outline

```
# sunset-ecosystem                                     [keep — 30 lines]
  badges, one-paragraph pitch, the "what makes it different" table

## Architecture                                        [expand — 80 lines]
  Full ASCII diagram (extend current one)
  Layer table (Nerve/Swarm/Sunset/Logos/Nexus/Compiler/Perception)
  Data flow: signal → RoomGrid → tournament → breed → archive
  Conservation law connection (γ+η=C and Hebbian intercept)

## 30-Second Quickstart                                [keep — 25 lines]

## Module Reference                                    [NEW — 400 lines]
  ### nerve/ — Forward Inference (8 files)
    RoomGrid: backend selection, tick API, room lifecycle
    Metronome: bpm, harmonics, A2ASignalSource
    WorldModel: JEPA calibration, WanderingJEPA uncertainty
    Topology: COLLECT→SELECT→COMPILE→FEEDBACK→REGULATE cycle
    routing.py, fiber.py, adaptation.py — 2 lines each
  
  ### swarm/ — Breeding Engine (89 files, key 12)
    AgentLifecycleFSM: 6 states, 8 transitions
    BreederDaemonV2: SQLite WAL, FLUX gating, step() per tick
    ThermalBudget + ThermalAuction: VCG device slot allocation
    SpectralBreeder: complex genome, spectral convolution crossover
    FleetBFTNetwork: PBFT phases, QDArchive, MAP-Elites niche
    HebbianMeshLayer: affinity update rules, chaos modulation
    MeshVectorTables: CRDT merge, FleetVectorIndex KNN
    fleet_bft_qd.py, mesh_vector_gossip.py — 2 lines each
  
  ### sunset/ — Trinity Engine (22 files, key 5)
    trinity_scorer.py: ethos × pathos × logos product
    compiler.py: FLUX AST → codegen → hot-swap
    seed_bank.py: genome archive for extinct lineages
    plato_bridge.py: sunset memories → PLATO tiles
    unified_memory.py: agent working memory

  ### logos/ — Journals and Visualization (20 files, key 6)
    DecisionJournal: FLAME format, log_spawn/sunset/breed/human
    SignedWAL: cryptographic append-only log
    WALIndex + WALQuery: replay and query interface
    TidePoolVisualizer: FleetSnapshot, render_html, render_ascii
    IntentProtocol: structured command format
    OpcodeCapabilityIndex: opcode → capability routing

  ### ethos/ (7 files)
    AgentAllocator: capacity planning by hardware survey
    ThermalAutoCalibrate: target calibration for device budgets
  
  ### pathos/ (6 files)
    MomentScorer: emotional resonance scoring
    NeedTracker: agent need state (exploration, rest, breed)
  
  ### nexus/ (9 files)
    FleetConductorV2: orchestrates all subsystems, 15 enable_* flags
    FleetEventBus: pub/sub for in-process events
    DistributedConsensus: BFT coordinator wrapper
    HolonomyBridge: holonomy consistency across fleet consensus rounds

  ### fleet/ (265 files, key 10)
    fleet_api.py: FastAPI server, /health /status /agents /memory /swarm
    FleetBridgeServer: HTTP bridge on :8850 for Claw CLI
    conservation_spectral_bridge.py: conservation-law-rs + spectral-fleet-rs
    agent_identity_bridge.py: A2A identity + cryptographic signing
    FleetEventBus: async SSE for tide-pool dashboard
    gossip_protocol.py: epidemic O(log N) state propagation
    operational_trap.py: TrapRegistry circuit breakers
    a2a_signal_bridge.py: agent-to-agent signal routing
    fleet_scheduler_state.json: INTERVAL/CRON/ONESHOT job registry
    bernstein_orchestrator.py: multi-agent task decomposition

  ### superinstance-ffi/ (Rust crate)
    12 C-ABI functions (full list from superinstance_ffi.h)
    Mock vs. real loading pattern
    How to add a new function

## Configuration Reference                             [NEW — 80 lines]
  ConductorConfig fields (all 20 enable_* flags documented)
  ThermalConfig (default budgets, calibration targets)
  DiversityConfig (chaos bounds, blacklist threshold)
  Environment variables (KEEPER_URL, SUPERINSTANCE_REGISTRY_URL, etc.)

## Conservation Law Integration                        [NEW — 40 lines]
  How sunset_ecosystem connects to γ+η=C
  ThermalBudget → fleet_budgets table mapping
  Hebbian intercept: how hebbian_mesh.py feeds γ+H

## Fleet Registry Integration                          [NEW — 30 lines]
  How to register with Keeper :8900
  fleet_budgets heartbeat
  fleet_events lifecycle emissions

## Deployment                                          [NEW — 60 lines]
  Single-node (FleetConductorV2 + FleetBridgeServer)
  Multi-node (mesh gossip, Keeper peer discovery)
  Docker (Dockerfile present — document it)
  Systemd service (add service file to docs/)

## Testing                                             [expand — 40 lines]
  476 test files, 2215+ tests breakdown by module
  Mock FFI pattern (superinstance_ffi_mock.py)
  How to add a test for a new breeder
  Benchmark suite location (fleet-status/BENCHMARK*.py)

## Contributing                                        [keep — 20 lines]
  Link to CONTRIBUTING.md, DEVELOPER.md
```

**Rewrite process:**
1. Start with Module Reference — it is the highest value section and can be generated semi-automatically from the CAPABILITY.toml exports list
2. Configuration Reference — scrape all `@dataclass` fields from ConductorConfig, ThermalConfig, DiversityConfig
3. Architecture section — extend the existing ASCII diagram with the Nexus/Compiler/Perception layers that are currently missing
4. Conservation Law Integration — copy from SUPERINSTANCE_RUNTIME.md §3 and adapt
5. Deployment — document the existing Dockerfile and docker-compose.yml

**Do not:** rewrite the 30-Second Quickstart or the feature table. They are correct and tested.

---

## 8. Implementation Sequence

Ordered by value delivered per week of effort. Each step is independently shippable.

### Week 1 — Registry and Announcement

- [ ] Add `_push_budget_heartbeat()` to `claw_fleet_bridge.py` (§2.3)
- [ ] Add `_announce_to_keeper()` to `FleetBridgeServer.start()` (§3.2)
- [ ] Add `_emit_event()` to `AgentLifecycleFSM.transition()` (§2.4)
- [ ] Run `tools/register_sunset_capabilities.py` against production registry (§2.5)
- [ ] Verify: `si fleet status` shows sunset-ecosystem in agent list

**Done signal:** `psql $REGISTRY -c "SELECT COUNT(*) FROM capabilities WHERE repo_id=(SELECT id FROM repos WHERE name='sunset-ecosystem')"` returns 29.

### Week 2 — API Endpoints

- [ ] Add P0 breeding endpoints to `fleet/fleet_api.py` (§4.2): `/swarm/breed`, `/swarm/agents/{id}`, `/swarm/sunset/{id}`, `/swarm/leaderboard`
- [ ] Add conservation endpoints: `/conservation/status`, `/spectral/fingerprint`, `/conservation/audit`
- [ ] Add fleet standard response envelope to all responses (§4.3)
- [ ] Write INTEGRATION.md for `fleet/conservation_spectral_bridge.py` (§6 Priority 1)

**Done signal:** `curl http://oracle1:8850/conservation/status | jq .data.fleet_gamma` returns a float.

### Week 3 — FFI Consolidation

- [ ] Add all 12 `superinstance_ffi.h` functions to the planned `si-core-c` header (§1.2)
- [ ] Publish `superinstance-ffi` Rust crate to crates.io (§5.1)
- [ ] Write `superinstance-ffi/INTEGRATION.md` (§6 Priority 2)
- [ ] Add `no_std` feature flag to Cargo.toml for embedded targets

**Done signal:** `cargo add superinstance-ffi` works from any other SI repo.

### Week 4 — First Extractions

- [ ] Extract `agent-lifecycle-py` from `swarm/lifecycle_fsm.py` (§5.1)
- [ ] Extract `fleet-journal-py` from `logos/` WAL + journal files (§5.1)
- [ ] Write INTEGRATION.md for both extracted repos (§6 Priority 3)
- [ ] Add CAPABILITY.toml to each extracted repo

**Done signal:** `pip install agent-lifecycle-py` works; `from agent_lifecycle import AgentLifecycleFSM` passes import.

### Week 5 — README Rewrite

- [ ] Write Module Reference section (§7) — 400 lines
- [ ] Write Configuration Reference (§7)
- [ ] Write Conservation Law Integration section (§7)
- [ ] Expand Architecture diagram to include Nexus/Compiler/Perception

**Done signal:** README.md reaches 800+ lines; `si cap info sunset-ecosystem` renders without errors.

### Weeks 6-8 — Remaining Extractions and INTEGRATION.md

- [ ] Extract `fleet-thermal-py` (§5.1)
- [ ] Write nerve/ INTEGRATION.md (§6 Priority 4)
- [ ] Write mesh gossip INTEGRATION.md (§6 Priority 5)
- [ ] Write logos/ INTEGRATION.md (§6 Priority 6)
- [ ] Add tide-pool WebSocket feed to FleetConductorV2 SSE dashboard
- [ ] Begin `spectral-breeding-py` extraction (§5.2) — depends on spectral-fleet-rs Python bindings

---

## Appendix A: Full Module Inventory

| Dir | Files | Key Exports | Tests |
|-----|-------|-------------|-------|
| `nerve/` | 41 | RoomGrid, NerveTopology, Metronome, WorldModel, routing, fiber, bloom_filter.c, ring_buffer.c | ~180 |
| `swarm/` | 89 | BreederDaemonV2, AgentLifecycleFSM, ThermalBudget, SpectralBreeder, FleetBFTNetwork, HebbianMeshLayer, MeshVectorTables, FluxVectorTable | ~620 |
| `sunset/` | 22 | trinity_score, FLUX compiler, seed_bank, plato_bridge, unified_memory | ~200 |
| `logos/` | 20 | DecisionJournal, SignedWAL, TidePoolVisualizer, IntentProtocol, OpcodeCapabilityIndex | ~180 |
| `ethos/` | 7 | AgentAllocator, hardware_survey, ThermalAutoCalibrate | ~60 |
| `pathos/` | 6 | MomentScorer, NeedTracker, interaction_log | ~50 |
| `nexus/` | 9 | FleetConductorV2, FleetEventBus, DistributedConsensus, HolonomyBridge | ~80 |
| `fleet/` | 265 | FleetBridgeServer, fleet_api, conservation_spectral_bridge, agent_identity_bridge, gossip_protocol, operational_trap | ~700 |
| `superinstance-ffi/` | Rust | 12 C-ABI functions (eisenstein_norm, laman_*, holonomy_check, pythagorean48_encode, constraint_*, spline_interpolate, deadband_filter, manhattan_distance, cascade_match) | (in tests/) |
| `tests/` | 476 | — | 2215+ |

## Appendix B: Environment Variables Required

| Variable | Used By | Source |
|----------|---------|--------|
| `SUPERINSTANCE_REGISTRY_URL` | budget heartbeat, capability registration | Supabase DSN |
| `KEEPER_URL` | agent announcement | default `http://oracle1:8900` |
| `PLATO_URL` | decision journal → tiles | default `http://oracle1:8847` |
| `SUNSET_VESSEL_ID` | fleet_budgets agent_id prefix | default: `oracle1` |
| `TURBOVEC_INDEX_PATH` | FluxVectorTable persistence | default: `~/.sunset/vectors/` |
| `SUNSET_THERMAL_LIMITS` | ThermalBudget overrides | JSON string of DeviceType→max |

## Appendix C: Known Gaps (Things the Plan Doesn't Fix)

1. **No Zig integration yet.** `deadband_filter` in `superinstance_ffi.h` matches `deadband-zig` API exactly, but no one has written the bridge. Low effort, high value.
2. **Arrow Flight mesh dependency.** `swarm/arrow_flight_mesh.py` imports `pyarrow.flight` which has a large install footprint. The `fleet-mesh-py` extraction (§5.2) is blocked until this is optional-ized.
3. **`cocapn_traps` dependency.** `BreederDaemonV2` has a graceful fallback when `cocapn_traps` is missing, but `cocapn_traps` is not in any registry. It should be published or inlined.
4. **`turbovec` stability.** `FluxVectorTable` depends on `turbovec>=0.1.0`. turbovec's API is not stable. Pin version before any extraction.
5. **No test for Keeper announcement.** `_announce_to_keeper()` (§3.2) will be new code. Write an integration test against a Keeper mock before deploying.
