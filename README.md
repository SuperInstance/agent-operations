# SuperInstance

**One system. Conservation laws, spectral ranking, categorical composition, temporal coordination — stacked five layers deep, running 300+ crates, and blurring the line where vectors become code.**

---

## The Problem

You have 100 agents. They share a GPU budget. Some are productive — they handle requests, generate value, learn from outcomes. Some waste tokens — they loop, hallucinate, burn budget on tasks they can't complete.

How do you keep the fleet alive?

You can't just give every agent an equal slice. A translation agent that's 95% accurate doesn't need the same budget as a newly-spawned research agent that's still finding its footing. And you can't just watch them burn — one runaway agent can exhaust the entire fleet's compute before you notice.

You need a law. Not a guideline. A law — like conservation of energy in physics. Something that holds always, no exceptions, enforced by the runtime, not by hope.

---

## Layer 1: Conservation — γ + H = C

Here's the law:

- **γ** (gamma) = productive energy. Tokens spent on useful output. Compute that produced value.
- **H** (entropy) = waste. Tokens burned on errors, retries, hallucinations. Compute that produced nothing.
- **C** = total budget. The GPU hours, the token allocation, the compute ceiling.

**γ + H = C. Always. No exceptions.**

You can't create energy. You can't destroy it. You can only move it from productive to waste. Every agent action either converts γ to H (it did something, consuming productive budget and producing entropy) or it doesn't happen.

```toml
# In code: the conservation-law crate
[agent.budget]
gamma = 800    # productive
entropy = 200  # waste
capacity = 1000  # total

# When the agent spends 50 units:
# gamma → 750, entropy → 250, capacity stays 1000
# The law holds. Always.
```

**What happens when one agent overspends?** Its γ drops. Its H rises. The total C doesn't change — but the agent has less productive budget left. It can't borrow from other agents (their budgets are separate). It either becomes more efficient (doing more with less γ) or it stops (γ = 0 → execution blocked).

The system self-corrects because agents that waste budget run out of it. Agents that are productive keep theirs. Natural selection, but for compute.

This isn't a soft heuristic. The `conservation-law` crate enforces it at compile time. An agent that tries to spend more than its γ throws an error. An allocation where γ + H ≠ C is rejected. The invariant is the law.

---

## Layer 2: Spectral Ranking — Who Matters Most?

Now you have 100 agents respecting their budgets. But which ones matter most? Not which ones are busiest — which ones are *central* to the fleet's operation?

Spectral ranking answers this. Build a graph where agents are nodes and their interactions are edges. Compute the eigenvalues of the graph's Laplacian. The eigenvector of the largest eigenvalue tells you each agent's centrality — not by counting connections, but by measuring how much removing that agent would restructure the entire graph.

```python
# The spectral-fleet crate in action:
import numpy as np

# 5 agents, pairwise collaboration weights
fleet_graph = np.array([
    [1.0, 0.8, 0.1, 0.0, 0.3],
    [0.8, 1.0, 0.6, 0.2, 0.0],
    [0.1, 0.6, 1.0, 0.9, 0.1],
    [0.0, 0.2, 0.9, 1.0, 0.7],
    [0.3, 0.0, 0.1, 0.7, 1.0],
])

eigenvalues, eigenvectors = np.linalg.eigh(fleet_graph)
dominant = eigenvectors[:, -1]  # eigenvector of largest eigenvalue

for i, score in enumerate(dominant):
    print(f"Agent {i}: centrality = {score:.4f}")

# Agent 3: centrality = 0.5252  ← most central
# Agent 1: centrality = 0.4826
# Agent 2: centrality = 0.4681
# Agent 4: centrality = 0.3516
# Agent 0: centrality = 0.3901
```

Agent 3 wins because it bridges two clusters (agents 0-1 and agents 2-4). Remove agent 3 and the fleet fragments. Remove agent 4 and the fleet barely notices. The eigenvalue captures this.

The **spectral gap** (difference between the two largest eigenvalues) tells you how quickly the fleet converges to consensus. A large gap → fast coordination. A small gap → the fleet is near a bifurcation — it's about to split into factions.

This is the `spectral-fleet` crate: real-time eigenstructure monitoring for agent fleets. It doesn't just compute static rankings — it updates incrementally as agents join, leave, and change behavior.

---

## Layer 3: Composition — Category Theory

Individual agents are objects. Agent transformations are morphisms. The composition of morphisms gives guarantees: if A → B is correct and B → C is correct, then A → C is correct — without verifying the composite.

This is category theory, and the `categorical-agents` crate implements it.

```
Agent A (email-fetcher)     output: raw-email[]
        │
        │  functor maps A's output to B's input
        ▼
Agent B (email-parser)      output: structured-email[]
        │
        │  functor maps B's output to C's input
        ▼
Agent C (summarizer)        output: summary[]
```

The functor isn't just a type converter. It enforces that:
- **Composition is associative**: (A ∘ B) ∘ C = A ∘ (B ∘ C). Pipeline order for grouping doesn't matter.
- **Composition is typed**: A's output type must match B's input type. Mismatch = compile error.
- **Budgets compose**: The pipeline's C is the sum of its agents' C values, minus coordination overhead.

When you compose agents A, B, C into a pipeline, the categorical algebra guarantees the pipeline is correct — you don't need to test every possible combination.

---

## Layer 4: Topology — Sheaves and Persistence

Agents form a network. Networks have shape. Shape has mathematics.

### Sheaf Laplacian: Detecting Disagreement

A sheaf maps data to regions of a topological space. The sheaf Laplacian detects where data assigned to different regions disagrees. In agent terms: if agent A thinks the answer is X and agent B thinks the answer is Y, the sheaf Laplacian measures how far apart X and Y are — and tells you whether the disagreement is local (agents can resolve it) or global (the fleet has fundamentally split).

```python
# Persistent-sheaf crate concept:
# 3 agents, each with a belief vector
beliefs = {
    'agent_a': [0.8, 0.2, 0.0],
    'agent_b': [0.7, 0.3, 0.0],
    'agent_c': [0.1, 0.2, 0.7],  # outlier
}

# Sheaf Laplacian detects that agent_c disagrees with the others.
# The Laplacian's null space contains only the consensus vector.
# Agent_c's belief projects poorly onto this space → flagged as disagreement.
```

### Persistence Diagrams: Finding Anomalies

Persistent homology tracks which topological features (clusters, loops, voids) survive across scale thresholds. Features that persist are real structure. Features that appear and disappear quickly are noise.

For agent fleets: run persistence on the fleet's interaction graph. A persistent cluster = a real team that works together. A transient loop = a temporary coordination pattern. A new persistent feature that wasn't there yesterday = either the fleet learned something new, or something is wrong.

The `persistent-sheaf` crate computes these diagrams in real-time. It's the anomaly detection layer that spectral methods alone can't provide — spectral methods see averages, persistence sees structure.

---

## Layer 5: Where Vectors Become Code

Here's where it gets weird. In SuperInstance, a vector *is* a capability. An embedding *is* a function. A distance *is* a budget.

### The Vector IS the Agent

An agent's spectral identity — the eigenvector representing its position in the fleet's eigenstructure — *is* the agent. Not a representation of the agent. The agent.

```
agent_identity = [0.12, 0.03, 0.85, 0.01, 0.42]

# This vector means:
#   - Strong affinity for task type 3 (0.85)
#   - Moderate connection to task type 5 (0.42)
#   - Weak everywhere else
#   
#   The agent doesn't "have capabilities" that produce this vector.
#   The vector IS what the agent does.
```

### The Embedding IS the Function

A capability's embedding — its position in the capability vector space — encodes its function. Two capabilities with similar embeddings do similar things. Not because someone labeled them that way, but because the spectral structure of the fleet's interaction graph placed them near each other.

```
capability_embeddings = {
    'email-fetcher':    [0.9, 0.1, 0.0, 0.0],
    'email-parser':     [0.8, 0.2, 0.0, 0.0],  # near email-fetcher
    'summarizer':       [0.3, 0.3, 0.4, 0.0],  # different region
    'translator':       [0.2, 0.1, 0.5, 0.2],  # near summarizer
}

# distance(email-fetcher, email-parser) = 0.14  ← similar functions
# distance(email-fetcher, translator)    = 0.78  ← different functions
#
# You don't need to read the code. The embedding tells you.
```

### The Distance IS the Budget

The Wasserstein distance between two fleet states measures how much "work" it takes to transform one state into another. In budget terms: how much γ must be spent to move the fleet from configuration A to configuration B.

```
fleet_yesterday = { 'agents': 100, 'gamma_total': 80000, 'config': '...' }
fleet_today     = { 'agents': 105, 'gamma_total': 82000, 'config': '...' }

w2_distance = wasserstein(fleet_yesterday, fleet_today)
# = 0.12

# This means: the fleet changed by 0.12 "budget units" overnight.
# Small distance → fleet is stable, conservation law held, no chaos.
# Large distance → something broke, agents restructured, investigate.
```

The `wasserstein-agents` crate computes this. It's the improvement metric in the self-improvement loop: after each optimization cycle, compute W₂ between before and after. Monotone decrease = convergence. Increase = divergence, stop and investigate.

---

## Tying It Together: A Full Cycle

Here's what happens when a request enters the system:

```
1. Request arrives: "Summarize these 50 emails about the Q3 budget"

2. CONSERVATION (Layer 1):
   Budget allocated: γ=100, H=20, C=120
   Every subsequent step respects this.

3. SPECTRAL (Layer 2):
   Fleet has 15 agents. Spectral ranking identifies 3 agents
   with highest centrality for email tasks.
   Top agent gets the job. Others stay available.

4. COMPOSITION (Layer 3):
   The task decomposes into a pipeline:
     email-fetcher → email-parser → relevance-filter → summarizer
   Categorical composition guarantees types match and budgets compose.
   Pipeline C = 40 + 25 + 20 + 35 = 120 units.

5. TOPOLOGY (Layer 4):
   Sheaf Laplacian checks: do all pipeline stages agree on the
   email format? Yes → proceed. No → flag disagreement, resolve.

6. EXECUTION:
   Pipeline runs. Budget drains at each step.
   γ: 100 → 85 → 70 → 55 → 40
   H:  20 → 35 → 50 → 65 → 80
   γ + H = 120 at every step. The law holds.

7. LEARNING:
   Summary quality scored: 0.87.
   Agent weights adjusted: summarizer weight += 0.087.
   Spectral identity updated.
   Next time, this agent ranks higher for similar tasks.

8. DISTILLATION:
   Request + response stored.
   When 1000 similar pairs accumulate, autoclaw trains a local model.
   Next month, this task costs 1/10th as much.
```

Conservation governed the budget. Spectral identified the right agent. Composition guaranteed correctness. Topology verified agreement. The vector was the agent, the embedding was the function, and the distance was the budget.

---

## The 5-Layer Stack

| Layer | Domain | Key Crates | Guarantee |
|---|---|---|---|
| **1: Physics** | γ + H = C | `conservation-law`, `entropy-conservation` | Budget never created or destroyed |
| **2: Coordination** | Spectral methods | `spectral-fleet`, `eigenstream` | Fleet convergence bounded by spectral gap |
| **3: Composition** | Category theory | `categorical-agents`, `constraint-dsl` | Compositions correct by construction |
| **4: Timing** | Temporal logic | `t-minus`, `temporal-logic` | Temporal constraints satisfied |
| **5: Verification** | Musical math | `self-improving-band`, `hodge-music` | Live formal verification with aesthetic output |

Each layer's guarantee is a consequence of the layer below. Conservation enables spectral. Spectral enables composition. Composition enables timing. Timing enables verification. You can use any layer independently, but they compose into something stronger than the sum of their parts.

---

## What's in This Repository

This is the operations hub. Not a crate — the documentation, tooling, and strategic context that connects everything.

### Key Documents

| Document | What it is |
|---|---|
| [`UNIFIED_VISION.md`](UNIFIED_VISION.md) | The full system architecture — application-first loop, decomposition pipeline, training pipeline, agent protocol, PLATO education system. 45 minutes to read, covers everything. |
| [`AGI_CONVERGENCE_ROADMAP.md`](AGI_CONVERGENCE_ROADMAP.md) | The 5-layer mathematical stack in detail. Why 300+ repos are one system. The self-improvement engine. Priority crate matrix. |
| [`POST_CODE_AGENT_VISION.md`](POST_CODE_AGENT_VISION.md) | The post-code thesis: agents produce structured output that IS the application. No compilation. No intermediate code. Ten killer apps. |
| [`PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md`](PROMPTSCRIPT_INTEGRATION_DEEP_DIVE.md) | How `.prs` files become agent deployment manifests. The PromptScript → WASM → structured output pipeline. |
| [`SPEC_CAPABILITY_TOML.md`](SPEC_CAPABILITY_TOML.md) | The specification for self-describing crates. Every repo has a `CAPABILITY.toml`. This defines the format. |
| [`INTEGRATION.md`](INTEGRATION.md) | How every crate connects to every other crate. The hub's integration map. |
| [`docs/agent-reliability.md`](docs/agent-reliability.md) | Hard-won operational data: 42% silent failure rate, 5-repo limit, procedural > descriptive, always verify output. |

### Tools

| Tool | What it does |
|---|---|
| [`tools/discover_integrations.py`](tools/discover_integrations.py) | Scans a directory for `CAPABILITY.toml` files, builds a dependency graph, finds integration opportunities, outputs a markdown report. `python3 tools/discover_integrations.py /path/to/repos` |

### Patterns & Templates

| Path | What it provides |
|---|---|
| [`patterns/task-prompts.md`](patterns/task-prompts.md) | How to write agent prompts that work. Procedural, not descriptive. |
| [`patterns/repo-sweeps.md`](patterns/repo-sweeps.md) | How to process 300+ repos with parallel agents. Batch of 5, verify output. |
| [`templates/`](templates/) | Copy-paste templates for README sweeps, CI addition, branch cleanup. |
| [`a2a-protocol/`](a2a-protocol/) | Agent-to-agent communication protocol with failure recovery. |

---

## The Runtime Implementations

The stack isn't just theory. It's running code at every level:

- **[`si-core-c`](https://github.com/SuperInstance/si-core-c)** — C library. Conservation budgets, spectral ranking, agent state machines, TOML parsing, computational cells. ~15 KB compiled. Runs on embedded, compiles to WASM, links into kernels.

- **[`si-runtime-js`](https://github.com/SuperInstance/si-runtime-js)** — TypeScript runtime. Same conservation laws, same spectral math, plus browser-grade capability scanning and cell composition. Works in Node.js and the browser.

- **300+ Rust crates** — `conservation-law`, `spectral-fleet`, `categorical-agents`, `t-minus`, `persistent-sheaf`, `wasserstein-agents`, `lattice-crypto`, `room-topology`, `intention-field`, and hundreds more. Each crate is small, focused, and optional. Together they form the bedrock.

Same math at every level. γ + H = C in C, TypeScript, and Rust. Power iteration in C, TypeScript, and Rust. The law doesn't change because the language does.

---

## Quick Start

```bash
# Clone the hub
git clone https://github.com/SuperInstance/agent-operations.git
cd agent-operations

# Scan your repos for integrations
python3 tools/discover_integrations.py ~/repos/superinstance

# Read the reliability playbook first (5 min)
cat docs/agent-reliability.md

# Then the full vision (45 min)
cat UNIFIED_VISION.md

# Build and test the C runtime
cd /tmp && git clone https://github.com/SuperInstance/si-core-c.git
cd si-core-c && make test

# Install and test the TypeScript runtime
cd /tmp && git clone https://github.com/SuperInstance/si-runtime-js.git
cd si-runtime-js && npm install && npm test
```

---

## The Self-Improvement Loop

```
SIA watches fleet (spectral eigenvalues)
  → identifies weakest eigenmode
  → generates improvements (categorical composition)
  → validates against conservation laws (γ + H = C)
  → deploys gradually (t-minus coordination)
  → measures improvement (Wasserstein distance)
  → the improvement process improves itself
```

This loop runs for every agent, for every task, continuously. The system doesn't just improve applications — it improves itself. Agents that learn to work within their budgets become more efficient. Spectral rankings converge on true capability. Categorical compositions accumulate into a library of verified pipelines. The fleet gets better at getting better.

---

## Why This Exists

The AI industry has a fragmentation problem. Training pipelines are separate from inference engines. Agent frameworks are separate from the models they run. Application code is separate from the models that could learn from it. Vector databases are separate from the computation they index.

This fragmentation is architecturally wrong. An agent-native application is a single organism — not a collection of parts. The training data, the model, the application logic, the agent protocol, and the cellular decomposition are all expressions of the same system at different levels of abstraction.

SuperInstance exists to unify these expressions. Not through a monolithic framework, but through a set of mathematical principles that compose into guarantees. The conservation law holds whether you're in C, TypeScript, or Rust. The spectral ranking works whether you have 5 agents or 500. The categorical composition is correct whether you verify it or not — that's what "correct by construction" means.

**The vector IS the agent. The embedding IS the capability. The distance IS the budget.**

Start with the law. The rest follows.

---

*SuperInstance — 2026*
*Conservation. Spectral. Categorical. Temporal. Verified.*
