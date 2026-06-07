# Integration Guide: agent-operations

## What This Repository Provides

agent-operations is NOT a Rust crate — it is the **strategic operations center** for the entire SuperInstance ecosystem. It holds:

- **AGI Convergence Roadmap** (7,200 words) — The thesis that 300+ repos are 5 computational layers of one system
- **Post-Code Agent Vision** (5,200 words) — Agents produce structured output that IS the application
- **PromptScript Integration Deep Dive** (7,500 words) — `.prs` files as the deployment language for agent capabilities
- **Agent Reliability Playbook** — Hard-won data: procedural prompts succeed at 90%+, 5-repo limit, agents fail silently
- **Task Prompt Patterns** — How to write agent prompts that work
- **Repo Sweep Playbooks** — How to process N repos with M parallel agents
- **A2A Protocol** — Agent-to-agent handoff format with failure recovery
- **Templates** — Copy-paste task definitions for README sweeps, CI addition, branch cleanup

### The 5-Layer Mathematical Stack

| Layer | Domain | Key Crates | Guarantee |
|-------|--------|------------|-----------|
| **1: Physics** | Conservation laws (γ + H = C) | conservation-law, entropy-conservation | Agent actions respect energy budget |
| **2: Coordination** | Spectral methods | spectral-fleet | Fleet convergence bounded by spectral gap |
| **3: Composition** | Category theory | categorical-agents | Compositions are correct by construction |
| **4: Timing** | Temporal logic | t-minus | Temporal constraints satisfied |
| **5: Proof** | Musical math | self-improving-band, hodge-music | Live formal verification with aesthetic output |

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

## How to Use This Repository

```bash
git clone https://github.com/SuperInstance/agent-operations.git
cd agent-operations

# Start with agent reliability
cat docs/agent-reliability.md

# Then task prompt patterns
cat patterns/task-prompts.md

# Then the convergence thesis
cat AGI_CONVERGENCE_ROADMAP.md
```

## Integration Points

### Everything — This Is the Hub

agent-operations integrates with every SuperInstance crate because it defines the architecture that connects them all.

#### conservation-law → spectral-fleet → categorical-agents → t-minus (The Stack)

- **Why**: These 4 crates form the mathematical core. agent-operations defines how they compose into the 5-layer stack and why the guarantees compose.
- **How**: Read `AGI_CONVERGENCE_ROADMAP.md` §2 for the full stack specification. Each layer's guarantee is a consequence of the layer below.

```
conservation-law (Layer 1)     → "Energy is conserved"
spectral-fleet (Layer 2)       → "Coordination converges" (depends on conservation)
categorical-agents (Layer 3)   → "Composition is correct" (uses spectral clustering)
t-minus (Layer 4)              → "Timing is satisfied" (respects categorical ordering)
```

#### fleet-warden (Production Operations)

- **Why**: fleet-warden keeps development environments clean; agent-operations defines the operational playbooks for running agent swarms at scale.
- **How**: Use `patterns/repo-sweeps.md` to run fleet-warden across 300+ repos in parallel batches of 5.

#### wasserstein-agents (Measurement)

- **Why**: Wasserstein distance is the improvement metric in the self-improvement loop. agent-operations specifies when and how to measure.
- **How**: After each improvement cycle, compute W₂ between fleet states. Monotone decrease confirms convergence.

#### lattice-crypto (Security)

- **Why**: The post-code vision requires cryptographic agent identity. agent-operations specifies the security model.
- **How**: Each agent gets a `RingLWE` key pair. Every action is signed. The provenance chain is tamper-evident.

#### persistent-sheaf (Topological Analysis)

- **Why**: Persistent homology reveals fleet structure that spectral methods alone miss. agent-operations identifies when to use topological vs. spectral analysis.
- **How**: Use persistent-sheaf for anomaly detection (topology changes = fleet structure changes). Use spectral-fleet for real-time monitoring.

#### self-improving-band (Proof of Concept)

- **Why**: The band is the simplest non-trivial system that exercises all 5 layers. It is simultaneously art, formal verification, and stress test.
- **How**: The band demo validates the entire stack. If 5 agents can self-organize musically with provable improvement, the architecture generalizes.

#### A2A Protocol (Agent Coordination)

- **Why**: Multi-agent systems need a standard handoff protocol. The A2A protocol (`a2a-protocol/README.md`) defines how agents pass work, handle failures, and coordinate across models.
- **How**: Use `HANDOFF.md` as the contract between agents. Zero-token output = silent failure — always verify.

## For AI Agents

- **Context needed**: Which layer(s) you're integrating, the specific guarantee you need, the operational playbook to follow
- **Key documents**: Start with `docs/agent-reliability.md`, then `patterns/task-prompts.md`, then `AGI_CONVERGENCE_ROADMAP.md`
- **Integration pattern**: Read the relevant document → extract the applicable pattern → instantiate with crate-specific types → verify the guarantee
- **Operational rules**:
  - 5 repos per task max (90%+ success rate)
  - Procedural > descriptive ("Do X, then Y" beats style guides)
  - Always verify output (agents fail silently)
  - Use different models for different task types

## For Humans

- **Prerequisites**: Familiarity with at least one SuperInstance crate; understanding of what the ecosystem is trying to achieve
- **Learning path**:
  1. `docs/agent-reliability.md` — How agents fail and how to fix it (5 min)
  2. `patterns/task-prompts.md` — Writing prompts that work (5 min)
  3. `AGI_CONVERGENCE_ROADMAP.md` — The full mathematical stack (30 min)
  4. `POST_CODE_AGENT_VISION.md` — The future vision (20 min)
  5. `PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md` — The technical glue (30 min)
- **Common pitfalls**:
  - This repo is documentation, not code — don't try to `cargo build` it
  - The convergence thesis is a claim, not a proof — read the argument critically
  - Operational playbooks are empirically derived, not theoretically guaranteed
  - The 5-layer stack is aspirational — not every crate implements every layer perfectly yet
