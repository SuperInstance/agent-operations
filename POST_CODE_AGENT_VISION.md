# Post-Code Agent Vision: The SuperInstance/open-mind Architecture

**Authors:** SuperInstance Operations Division  
**Date:** 2026-06-07  
**Status:** Strategic Vision Document  
**Version:** 1.0

---

## Executive Summary

The software industry is in a transitional phase. Current AI agent systems generate code that humans then compile, deploy, and operate. This is a stopgap. The end state is radically different: **agents produce structured output that IS the application.** No compilation. No intermediate code. The agent's response is the runtime.

This document articulates the post-code thesis, maps PromptScript as the compositional glue that makes it possible, proposes the open-mind framework as the runtime substrate, and outlines ten killer applications where the agent IS the product. It concludes with a four-phase technical roadmap integrating our 300+ Rust crates via WASM into a unified agent-as-application platform.

---

## 1. The Post-Code Thesis

### 1.1 Code Generation Is Transitional

The current generation of AI coding tools—GitHub Copilot, Claude Code, Cursor, and their successors—operate in a code generation paradigm: the model receives a prompt, generates source code in a programming language, and a human or CI pipeline compiles and executes that code. This pattern treats the LLM as a sophisticated code synthesizer, but the fundamental architecture remains unchanged: write code → compile → run.

This is a transitional state for three reasons:

**First**, the compilation step introduces latency and fragility. Generated code must be syntactically correct, semantically meaningful, type-checked, dependency-resolved, and tested before it produces value. Every step in this chain is a potential failure point. Studies show that even state-of-the-art code generation models produce code that requires significant human correction—between 30-60% of generated snippets need modification before they work correctly.

**Second**, code generation imposes an unnecessary abstraction layer. When an agent needs to produce a decision tree for a classification task, the current paradigm forces it to generate Python or Rust code that constructs a `DecisionTree` data structure, populate it with split rules, and serialize it. But the agent already *knows* the tree. It has reasoned about the optimal splits. Why force it to express this knowledge through the indirection of source code?

**Third**, and most fundamentally, code is a medium for human instruction of machines. It exists because humans needed a precise language to tell computers what to do. When the machine is both the reasoner and the executor, the human-readable intermediate representation becomes overhead. The agent can produce structured output—JSON, protocol buffers, MIDI events, mathematical proofs, cryptographic key material—directly, and a thin runtime layer can interpret and act on it immediately.

### 1.2 The Direct-Output Model

In the post-code paradigm, agents produce structured responses that are directly consumed by runtime systems. Consider these concrete examples from our crate ecosystem:

**Agent-as-MIDI-Composer.** Our band crates (`band-backend`, `band-common`, `band-derive`, `band-macro`, `band-main`, `band-orchestration`, `band-performance`, `band-proc-macro`, `band-test`, `band-wasm`) provide a complete MIDI and music composition toolkit. In the current paradigm, an agent generates Rust code that calls these crates to produce MIDI events. In the post-code paradigm, the agent directly emits a structured MIDI sequence:

```json
{
  "type": "midi_sequence",
  "tempo": 120,
  "time_signature": [4, 4],
  "tracks": [
    {
      "instrument": "piano",
      "channel": 0,
      "events": [
        {"delta": 0, "note": 60, "velocity": 80, "duration": 480},
        {"delta": 480, "note": 64, "velocity": 75, "duration": 480},
        {"delta": 480, "note": 67, "velocity": 82, "duration": 960}
      ]
    }
  ]
}
```

This JSON IS the music. No Rust compilation. No intermediate build step. The agent composed it directly, and the runtime plays it.

**Agent-as-Decision-Engine.** Our `decision-tree-rs` crate implements decision tree learning and inference. Instead of generating code that constructs a tree, the agent produces the tree structure directly:

```json
{
  "type": "decision_tree",
  "root": {
    "feature": "age",
    "threshold": 35,
    "left": {
      "feature": "income",
      "threshold": 50000,
      "left": {"label": "deny", "confidence": 0.92},
      "right": {"label": "approve", "confidence": 0.87}
    },
    "right": {"label": "approve", "confidence": 0.95}
  }
}
```

This IS the model. The agent built it through reasoning over data. No training loop, no Python script, no compilation. The structured output is the final product.

**Agent-as-Proof-Engine.** Mathematical proofs are structured objects—sequences of logical steps from axioms to conclusions. An agent that produces a proof does not need to generate Lean or Coq code that is then verified. It produces the proof structure directly:

```json
{
  "type": "mathematical_proof",
  "theorem": "Every bounded monotone sequence converges",
  "steps": [
    {"axiom": "Completeness of real numbers"},
    {"inference": "monotone_convergence", "from": [1]},
    {"substitution": "bound_applies", "from": ["hypothesis"]},
    {"conclusion": "limit_exists"}
  ],
  "verification_hash": "sha256:a3f2..."
}
```

The proof IS the output. The verification is a hash check, not a compilation step.

### 1.3 Why This Matters Now

Three converging trends make the post-code paradigm viable in 2026:

1. **Structured output maturity.** LLMs now reliably produce JSON, XML, and protocol-buffer output conforming to predefined schemas. OpenAI, Anthropic, and Google all offer native structured output modes with guaranteed schema compliance. The technology for agents to produce precise, typed output is production-ready.

2. **WASM as universal runtime.** WebAssembly provides a portable, sandboxed execution layer that can run Rust, C, C++, and Go compiled modules anywhere—browsers, servers, edge devices, embedded systems. Our 300+ Rust crates can compile to WASM and serve as capability plugins for agent runtimes. The "compilation" happens once, at the crate level, and the runtime interprets agent-structured output against these pre-compiled capabilities.

3. **Agent reasoning capability.** Current frontier models demonstrate genuine chain-of-thought reasoning, planning, and multi-step problem decomposition. They can analyze data, identify patterns, and make decisions that previously required algorithmic code. The reasoning IS the algorithm.

### 1.4 The Spectrum: From Code Generation to Direct Output

The transition is not binary. It exists on a spectrum:

| Stage | Agent Output | Runtime Role | Human Role |
|-------|-------------|-------------|-----------|
| **Stage 0: Code generation** | Source code | Compiler + execution | Review, debug, deploy |
| **Stage 1: Templated generation** | Code with templates | Compile with parameters | Configure parameters |
| **Stage 2: Structured instructions** | JSON/YAML workflows | Workflow engine | Define schemas |
| **Stage 3: Direct structured output** | Typed data objects | Thin interpreter | Define constraints |
| **Stage 4: Autonomous output** | Self-validating output | Minimal validation | Set goals |

We are currently in the transition from Stage 0 to Stage 2. This document proposes the architecture for Stages 3 and 4.

---

## 2. PromptScript as the Glue

### 2.1 PromptScript's Architecture

PromptScript is a domain-specific language that compiles `.prs` files into native instruction formats for 37 AI coding agents. Its architecture provides exactly the compositional primitives needed for the post-code paradigm:

- **`@meta` blocks** define identity, syntax version, and typed template parameters
- **`@inherit`** provides single-inheritance hierarchies (organization → team → project)
- **`@use`** provides mixin-style composition with multiple imports
- **`@extend`** allows targeted modification of imported blocks with sealed-property protection
- **`@skills`** define reusable capabilities with typed inputs/outputs, references, and tool permissions
- **`@agents`** declare sub-agents with dedicated models and tool access
- **Parameterized templates** via `{{variable}}` interpolation enable reusable, type-safe compositions
- **Registry resolver** supports Go-style URL imports from Git repositories with version pinning and lockfiles

This is not just a prompt compilation tool. It is a **declarative composition system for agent capabilities.**

### 2.2 From Prompt Compilation to Agent Definition

In the post-code paradigm, PromptScript's role evolves. Currently, it compiles agent instructions (system prompts, coding standards, restrictions) into formats consumed by coding assistants. In the evolved architecture, it becomes the **definition language for agent-as-application deployments:**

```promptscript
@meta {
  id: "midi-composer-agent"
  syntax: "1.2.0"
  params: {
    genre: enum("jazz", "classical", "electronic") = "jazz"
    tempo: number = 120
    complexity: enum("simple", "moderate", "complex") = "moderate"
  }
}

@inherit @superinstance/base-agent

@identity {
  """
  You are a musical composer that produces MIDI sequences directly.
  Your output IS the music — no code, no compilation, just structured sound.
  You reason about harmony, rhythm, melody, and arrangement simultaneously.
  """
}

@skills {
  compose: {
    description: "Compose a musical piece in {{genre}} style"
    inputs: {
      mood: { type: "string", description: "Emotional character" }
      duration_bars: { type: "number", description: "Length in bars" }
      key: { type: "string", description: "Musical key" }
    }
    outputs: {
      midi_sequence: { type: "object", description: "Complete MIDI sequence" }
    }
    allowedTools: ["band-wasm", "music-theory"]
    references: ["./refs/harmony-theory.md", "./refs/{{genre}}-patterns.md"]
  }
}
```

This `.prs` file does not generate code. It defines an agent whose output schema is a MIDI sequence. The compiled output targets not just coding assistants, but the **open-mind runtime** that executes the agent's structured responses directly.

### 2.3 Skill Composition as Capability Composition

PromptScript's skill system maps directly to capability composition in the post-code paradigm:

**Inheritance maps to capability hierarchies.** An organization defines base capabilities (`@superinstance/base-agent`), teams extend them (`@team/audio-agents`), and projects specialize them (`@project/jazz-composer`). Each layer adds or constrains capabilities, exactly like class inheritance in OOP but for agent behavior.

**Skills map to capability plugins.** Each `@skills` entry in a `.prs` file declares a typed, composable capability with explicit inputs, outputs, allowed tools, and reference documentation. In the post-code runtime, these skills become invokable endpoints backed by WASM-compiled Rust crates.

**Overlays map to runtime configuration.** The `@extend` mechanism, with its replace/append/sealed strategies, provides the precise semantics needed for runtime configuration: base capabilities are extended with project-specific parameters, references are appended without breaking the base, and critical properties are sealed against accidental override.

**Parameterized templates map to agent instances.** A single `.prs` template with `{{genre}}`, `{{tempo}}`, and `{{complexity}}` parameters can spawn a family of composer agents—each one a distinct application, compiled from the same source of truth.

### 2.4 The .prs → Agent → Structured Output Pipeline

The complete pipeline from PromptScript definition to application output:

```
.prs file
  │
  ├── prs compile ──► Agent system prompt (37 formats)
  │
  ├── prs compile --target open-mind ──► Agent capability manifest
  │     │
  │     ├── skill definitions ──► WASM module bindings
  │     ├── input/output schemas ──► Runtime type validators
  │     ├── tool permissions ──► Capability sandbox policies
  │     └── references ──► RAG context for agent reasoning
  │
  └── Agent execution ──► Structured output (JSON/Protobuf/MIDI/...)
        │
        └── Runtime interpreter ──► Direct action (sound, decision, proof, ...)
```

PromptScript serves as the single source of truth for both the agent's instructions (traditional role) and its capability bindings (new role). One `.prs` file defines what the agent does, what tools it can use, what inputs it accepts, and what outputs it produces.

### 2.5 OpenClaw's Skill System: A Working Precedent

OpenClaw's existing skill system provides a concrete, working precedent for the skill composition model described here. OpenClaw skills are defined in `SKILL.md` files with YAML frontmatter specifying:

- **Name and description** for skill discovery
- **Allowed tools** constraining what the agent can do
- **Trigger conditions** for automatic activation
- **User-invocable** flag for explicit invocation
- **References** for context injection
- **Compatibility** for multi-platform targeting

This is structurally identical to PromptScript's `@skills` block, and both align with the post-code capability model. The key insight: OpenClaw skills already compose agent capabilities at the instruction level. The next step is composing them at the output level—skills that don't just tell the agent *how* to do something, but define *what structured output* the agent produces.

The integration point is natural: OpenClaw skills that reference PromptScript definitions, where the `.prs` file specifies both the skill instructions and the output schema. The agent reads the skill, invokes the appropriate WASM-backed capabilities, and produces structured output that the runtime interprets directly.

---

## 3. open-mind Integration Architecture

### 3.1 What Is open-mind?

**open-mind** is a proposed open-source framework where agents ARE applications. It is not another agent orchestration layer, chatbot framework, or code generation tool. It is a runtime substrate designed specifically for the post-code paradigm.

The name reflects its core principle: an open architecture where any mind (agent) can produce any kind of output, unconstrained by the code-generation bottleneck. The agent's mind IS the application.

**Core design principles:**

1. **Output-first.** Everything in open-mind is designed around the output the agent produces. Schemas define what outputs look like. Validators check outputs against schemas. Renderers transform outputs into actions. The agent's reasoning process is internal; the output is external and primary.

2. **Capability-driven.** Agents access external functionality through typed capability plugins, not code generation. A capability plugin is a WASM module with a defined interface: given structured input, produce structured output. The agent reasons about *which* capabilities to invoke and *what* inputs to provide; it never generates the capability's implementation code.

3. **Composable.** Agent capabilities compose through PromptScript's inheritance and overlay system. Adding a new capability to an agent means adding a `@use` or `@extend` directive to its `.prs` definition—not writing new code.

4. **Self-improving.** Agents in open-mind can evaluate their own output quality using feedback loops (the SIA²—Self-Improving Agent Applications—pattern). An agent produces output, a validator scores it, and the agent adjusts its approach for the next invocation.

### 3.2 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        open-mind Runtime                     │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                │
│  │ Agent A  │   │ Agent B  │   │ Agent C  │  ...            │
│  │(Composer)│   │(Analyst) │   │(Teacher) │                 │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘                │
│       │              │              │                        │
│  ┌────▼──────────────▼──────────────▼─────┐                 │
│  │         Capability Bus (WASM)          │                 │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────────┐  │                 │
│  │  │MIDI │ │Tree │ │Latt.│ │Persist. │  │                 │
│  │  │Crate│ │Crate│ │Crypt│ │Sheaf    │  │                 │
│  │  └─────┘ └─────┘ └─────┘ └─────────┘  │                 │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────────┐  │                 │
│  │  │Spec.│ │Anom.│ │Room │ │Conserv. │  │                 │
│  │  │Lib  │ │Detect│ │Topo │ │Law      │  │                 │
│  │  └─────┘ └─────┘ └─────┘ └─────────┘  │                 │
│  └────────────────────────────────────────┘                 │
│       │                                                      │
│  ┌────▼─────────────────────────────────────┐               │
│  │         Output Validator & Router         │               │
│  │  Schema check → Type validate → Route    │               │
│  └──────────────────────────────────────────┘               │
│       │                                                      │
│  ┌────▼─────────────────────────────────────┐               │
│  │           Output Renderers                │               │
│  │  Audio │ Visual │ Data │ Proof │ Action   │               │
│  └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Component Specification

**Agent Definition Layer.** Agent definitions are `.prs` files compiled by PromptScript. Each agent definition specifies:
- Identity and persona (via `@identity`)
- Available capabilities (via `@skills` with `allowedTools` mapping to WASM modules)
- Input/output schemas (via skill `inputs` and `outputs`)
- Composition rules (via `@inherit`, `@use`, `@extend`)
- Safety constraints (via `@restrictions`)

**Capability Bus.** A WASM-based runtime that loads Rust crates compiled to WASM modules as capability plugins. Each plugin exposes:
- A typed interface (request/response schemas)
- A resource budget (memory, compute, time limits)
- A permission scope (what the plugin can access)
- A version and integrity hash (for reproducibility)

The capability bus is the bridge between the agent's structured output and the underlying computation. When an agent produces output that requires MIDI rendering, the bus routes to the `band-wasm` module. When an agent produces a decision tree, the bus routes to `decision-tree-rs`. The agent never writes code that calls these modules—it produces structured output that the bus interprets.

**Output Validator.** Validates agent output against the schemas defined in the `.prs` skill definitions. Uses JSON Schema or Protocol Buffer validation, depending on the output type. Invalid output triggers re-prompting with error context, following the SIA² feedback loop.

**Output Router.** Routes validated output to the appropriate renderer. Output types include:
- **Audio** (MIDI sequences → audio rendering via `band-backend`)
- **Visual** (diagrams, charts → SVG/Canvas rendering)
- **Data** (JSON/Protobuf → database storage, API responses)
- **Proof** (mathematical proof structures → verification via proof assistants)
- **Action** (structured commands → execution via capability bus)
- **Decision** (decision trees, risk assessments → business logic integration)

### 3.4 Integration with SuperInstance Rust Crates

Our crate ecosystem provides the capability plugins for open-mind agents. Key mappings:

| Crate Category | Capability | Agent Application |
|---------------|-----------|-------------------|
| `band-*` (10 crates) | Music composition, MIDI, orchestration | Agent-as-composer, Agent-as-music-collaborator |
| `decision-tree-rs` | Decision tree learning and inference | Agent-as-analyst |
| `lattice-crypto` | Lattice-based cryptography | Agent-as-security-auditor |
| `persistent-sheaf` | Topological data analysis | Agent-as-research-partner |
| `anomaly-detection` | Statistical anomaly detection | Agent-as-analyst, Agent-as-security-auditor |
| `room-topology` | Spatial topology for virtual environments | Agent-as-game-master |
| `conservation-law` | Conservation law enforcement for budgets | Agent-as-therapist, Agent-as-project-manager |
| `spectral` | Spectral analysis and feedback | Agent-as-teacher |
| `categorical-agents` | Category-theoretic agent composition | All agents (meta-capability) |

Each crate compiles to a WASM module with a JSON-based interface. The PromptScript `@skills` block references the crate by name in `allowedTools`, and the runtime resolves the WASM module at execution time.

### 3.5 PromptScript Compilation to open-mind Targets

A new PromptScript formatter target—`open-mind`—compiles `.prs` files into:

1. **Agent manifest** (`agent.json`): Metadata, capability bindings, input/output schemas
2. **Skill bindings** (`skills/*.json`): Per-skill capability mappings and parameter schemas
3. **Permission policies** (`policies.json`): Derived from `@restrictions` and `allowedTools`
4. **Context references** (`context/`): Referenced documentation files for RAG injection

This is analogous to how PromptScript currently compiles to `CLAUDE.md` for Claude Code or `.github/copilot-instructions.md` for GitHub Copilot—but instead of generating a system prompt for a coding assistant, it generates a complete agent deployment manifest for the open-mind runtime.

---

## 4. Ten Killer App Concepts

The following ten applications illustrate the post-code paradigm in practice. Each is an agent whose structured output IS the product—no code generation, no compilation, direct value delivery.

### 4.1 Agent-as-Therapist

**Concept:** A conversational agent that conducts structured therapy sessions, producing session notes, emotional state assessments, and treatment progress reports as structured output.

**Structured Output:**
```json
{
  "type": "therapy_session",
  "session_id": "uuid",
  "emotional_state": {
    "valence": 0.4,
    "arousal": 0.6,
    "dominance": 0.3,
    "primary_emotions": ["anxiety", "hope"],
    "conservation_budget": {
      "emotional_energy_remaining": 0.65,
      "cognitive_load": 0.7
    }
  },
  "therapeutic_interventions": [
    {"technique": "cognitive_reframing", "target": "catastrophizing", "effectiveness": 0.8}
  ],
  "session_summary": "...",
  "recommended_followup": "journaling_exercise"
}
```

**Why post-code:** Therapy is fundamentally about structured conversation and assessment. No code needs to be written. The agent reasons about emotional state, applies therapeutic techniques (defined as capability plugins via our `conservation-law` crate for energy budgets), and produces structured clinical output.

**PromptScript definition highlights:**
- `allowedTools: ["conservation-law", "spectral"]` for emotional energy tracking and feedback analysis
- `@restrictions` enforcing HIPAA-like privacy constraints, escalation rules for crisis detection
- Parameterized templates for different therapeutic modalities (CBT, DBT, psychodynamic)

### 4.2 Agent-as-Composer

**Concept:** An agent that composes original music by directly producing MIDI sequences, using our band crates as capability plugins.

**Structured Output:** Complete MIDI sequences with metadata (key, tempo, dynamics, articulation, expression).

**Why post-code:** Music composition is an act of reasoning about harmony, rhythm, melody, and form. The agent does not need to write code to compose—it needs to think musically and output the notes. The `band-wasm` module renders the sequence; the agent creates it.

**PromptScript definition highlights:**
- `@skills` with typed outputs (`midi_sequence` object)
- `@inherit @superinstance/musician-base` for shared musical knowledge
- Parameterized by genre, tempo, complexity, ensemble configuration
- Skill dependencies: `requires: ["harmony-check", "rhythm-validation"]`

### 4.3 Agent-as-Analyst

**Concept:** An agent that produces decision trees, anomaly reports, and risk assessments from data, using `decision-tree-rs` and `anomaly-detection` crates.

**Structured Output:**
```json
{
  "type": "analysis_report",
  "decision_trees": [...],
  "anomalies": [
    {"entity": "transaction_7842", "score": 0.94, "type": "statistical_outlier", "features": [...]}
  ],
  "risk_assessment": {
    "overall_risk": "high",
    "factors": [...],
    "recommendations": [...]
  }
}
```

**Why post-code:** Data analysis produces structured artifacts—trees, clusters, anomaly scores, risk matrices. These are the output. The agent reasons about the data, invokes statistical capabilities via WASM, and produces the analysis directly. No Python notebooks, no R scripts.

### 4.4 Agent-as-Mathematician

**Concept:** An agent that produces mathematical proofs, conjectures, and theoretical frameworks as structured proof objects.

**Structured Output:** Proof trees with axiom references, inference steps, variable bindings, and verification hashes.

**Why post-code:** A mathematical proof is a structured object. Current systems require mathematicians to formalize proofs in Lean, Coq, or Isabelle—essentially writing code that represents the proof. In the post-code paradigm, the agent produces the proof structure directly, and a verifier (itself a WASM capability plugin) checks logical consistency. The proof IS the product.

### 4.5 Agent-as-Teacher

**Concept:** An adaptive learning agent that produces personalized curricula, assessments, and feedback using spectral analysis of student performance.

**Structured Output:**
```json
{
  "type": "learning_session",
  "curriculum": {
    "current_module": "calculus_derivatives",
    "mastery_level": 0.72,
    "next_topics": ["chain_rule", "product_rule"],
    "adaptation_reason": "spectral_analysis indicates conceptual gap in composite functions"
  },
  "assessment": {
    "questions": [...],
    "difficulty_calibration": 0.68,
    "engagement_score": 0.85
  },
  "feedback": {
    "strengths": [...],
    "areas_for_improvement": [...],
    "recommended_practice": [...]
  }
}
```

**Why post-code:** Teaching produces structured artifacts: lesson plans, assessments, feedback reports, progress tracking. The agent reasons about the learner's state (using our `spectral` crate for performance signal analysis), adapts the curriculum, and produces structured teaching output. No LMS code to write.

### 4.6 Agent-as-Security-Auditor

**Concept:** An agent that produces security audit reports, generates lattice-based cryptographic keys, and detects anomalies in system behavior.

**Structured Output:** Audit reports with findings (severity, CVSS scores, remediation steps), generated cryptographic key material, anomaly detection results.

**Why post-code:** Security auditing produces structured findings. Key generation produces cryptographic material. Anomaly detection produces scores and classifications. None of these require code generation—the agent produces the audit artifacts directly, using `lattice-crypto` and `anomaly-detection` as capability plugins.

### 4.7 Agent-as-Project-Manager

**Concept:** An agent that coordinates task fleets, propagates deadlines across dependency graphs, and produces project status reports.

**Structured Output:**
```json
{
  "type": "project_state",
  "tasks": [
    {"id": "T-001", "status": "in_progress", "deadline": "2026-06-15", "dependencies": [], "assignee": "agent:coder-3"}
  ],
  "deadline_propagation": {
    "critical_path": ["T-001", "T-004", "T-007"],
    "at_risk": [{"task": "T-004", "reason": "blocked by T-001 delay", "slack": "2 days"}]
  },
  "fleet_coordination": {
    "active_agents": 5,
    "pending_assignments": 3,
    "resource_utilization": 0.78
  }
}
```

**Why post-code:** Project management is fundamentally about structured state: tasks, dependencies, deadlines, assignments, risks. The agent maintains and updates this state, propagates changes through the dependency graph (using `conservation-law` for resource budget enforcement), and produces structured project reports. No project management tool configuration needed.

### 4.8 Agent-as-Game-Master

**Concept:** An agent that runs a MUD-style game environment using our `room-topology` crate for spatial modeling, with NPC agents as sub-agents.

**Structured Output:** Game state updates including player position, room descriptions, NPC dialogue, event triggers, and world state mutations.

**Why post-code:** A game master produces narrative and state changes. The agent reasons about the game world (spatial topology via WASM), generates NPC behavior (via sub-agents), and produces structured game state updates. The room topology engine handles spatial reasoning; the agent handles narrative reasoning. The output IS the game.

**PromptScript composition:** The game-master agent uses `@agents` to define NPC sub-agents, each with their own `.prs` definition. The `room-topology` capability plugin manages the spatial model. The composition:

```promptscript
@meta { id: "game-master" syntax: "1.1.0" }

@skills {
  run_encounter: {
    description: "Generate and execute a game encounter"
    requires: ["room-topology"]
    allowedTools: ["room-topology", "narrative-engine"]
    outputs: {
      game_state: { type: "object", description: "Updated world state" }
      narrative: { type: "string", description: "Narrative description" }
    }
  }
}

@agents {
  npc-merchant: { description: "Traveling merchant NPC", model: "haiku" }
  npc-guard: { description: "Town guard NPC", model: "haiku" }
  narrator: { description: "Omniscient narrator", model: "sonnet" }
}
```

### 4.9 Agent-as-Research-Partner

**Concept:** An agent that performs topological analysis of academic literature using persistent sheaf theory, producing research synthesis reports.

**Structured Output:**
```json
{
  "type": "research_synthesis",
  "literature_topology": {
    "clusters": [
      {"theme": "transformer attention mechanisms", "papers": 47, "centrality": 0.89},
      {"theme": "efficient inference", "papers": 31, "centrality": 0.72}
    ],
    "bridging_concepts": ["sparse attention", "knowledge distillation"],
    "gaps": ["formal complexity bounds for sparse attention"]
  },
  "sheaf_analysis": {
    "cohomology_classes": 3,
    "persistent_features": [...],
    "novel_connections": [...]
  }
}
```

**Why post-code:** Research synthesis is an act of reasoning over structured information. The agent uses `persistent-sheaf` to identify topological features in citation networks and concept spaces, then produces structured analysis. No data science pipelines, no Python scripts—just direct topological reasoning and structured output.

### 4.10 Agent-as-Music-Collaborator

**Concept:** An agent that improvises in real-time alongside human musicians, listening to MIDI input and producing complementary MIDI output.

**Structured Output:** Real-time MIDI event streams that respond to input MIDI within latency constraints (<50ms).

**Why post-code:** Real-time musical improvisation is perhaps the purest expression of the post-code paradigm. The agent receives MIDI input (structured data), reasons about harmonic and rhythmic context, and produces MIDI output (structured data). There is no time for code generation. The response must be immediate. The agent's output IS the music, and it must flow in real-time.

This application pushes the architecture to its limits: low-latency WASM execution for the band crates, streaming input/output for real-time MIDI, and split-second decision-making for musical choices. It demonstrates that the post-code paradigm is not limited to batch-processing or asynchronous workflows—it can handle real-time, interactive applications.

---

## 5. Technical Roadmap

### Phase 1: PromptScript Skills with Rust Crate WASM Bindings (Months 1-3)

**Objective:** Enable PromptScript `@skills` to reference Rust crates as typed capability plugins via WASM.

**Deliverables:**

1. **WASM compilation pipeline.** Automated build system that compiles selected Rust crates to WASM modules with JSON-based interfaces. Start with `band-wasm` (already exists), then add `decision-tree-rs`, `anomaly-detection`, and `conservation-law`.

2. **PromptScript `open-mind` formatter.** A new formatter target that compiles `.prs` files into agent deployment manifests:
   - `agent.json`: Agent metadata, skill bindings, permission policies
   - `skills/*.json`: Per-skill schemas mapping to WASM module interfaces
   - `context/`: Referenced documentation for RAG injection

3. **Capability registry schema.** A manifest format for publishing WASM capability plugins:
   ```json
   {
     "name": "band-wasm",
     "version": "0.1.0",
     "interface": {
       "inputs": {"action": "string", "params": "object"},
       "outputs": {"result": "object", "midi": "bytes"}
     },
     "permissions": ["audio_output"],
     "resource_limits": {"memory_mb": 64, "compute_ms": 100}
   }
   ```

4. **Proof-of-concept agent.** The Agent-as-Composer, producing MIDI output from a PromptScript-defined agent using `band-wasm`. This validates the end-to-end pipeline: `.prs` → agent manifest → WASM capabilities → structured output → rendered result.

**Success criteria:** A PromptScript file compiles to an agent manifest, the agent invokes `band-wasm` through the capability bus, and produces a valid MIDI file that plays correctly.

### Phase 2: Structured Output Schemas Per Capability (Months 3-6)

**Objective:** Define and validate structured output schemas for every capability plugin, enabling type-safe agent output.

**Deliverables:**

1. **Schema definition library.** JSON Schema and Protocol Buffer definitions for all output types:
   - `MidiSequence` schema for music-related agents
   - `DecisionTree` schema for analytical agents
   - `AnomalyReport` schema for detection agents
   - `CryptoKeyMaterial` schema for security agents
   - `ProofObject` schema for mathematical agents
   - `ProjectState` schema for management agents
   - `LearningSession` schema for educational agents
   - `ResearchSynthesis` schema for research agents
   - `GameState` schema for game-master agents
   - `TherapySession` schema for therapeutic agents

2. **Output validator runtime.** A runtime component that validates agent output against schemas before routing to renderers. Supports strict mode (reject invalid output) and lenient mode (log warnings, attempt recovery).

3. **Schema-aware PromptScript.** Extend PromptScript's skill `inputs`/`outputs` to reference schema definitions by name, not just inline types:
   ```promptscript
   @skills {
     compose: {
       outputs: { midi: { schema: "MidiSequence/v1" } }
     }
   }
   ```

4. **Five killer app prototypes.** Implement Agent-as-Composer, Agent-as-Analyst, Agent-as-Mathematician, Agent-as-Teacher, and Agent-as-Game-Master with full structured output validation.

**Success criteria:** Any agent output that fails schema validation is caught and re-prompted. Five agent applications produce validated, rendered output without any code generation step.

### Phase 3: Agent Runtime That Executes Structured Responses Directly (Months 6-12)

**Objective:** Build the full open-mind runtime that loads agent manifests, invokes capabilities, validates output, and routes to renderers.

**Deliverables:**

1. **open-mind runtime core.** The runtime substrate:
   - Agent manifest loader (reads PromptScript-compiled manifests)
   - Capability bus (loads and executes WASM modules)
   - Output validator (schema checking)
   - Output router (dispatches to renderers)
   - Session manager (maintains agent state across invocations)

2. **Streaming execution support.** For real-time applications (Agent-as-Music-Collaborator), support streaming input/output with sub-100ms latency. This requires:
   - Streaming WASM execution with incremental output
   - Event-driven capability invocation
   - Real-time MIDI I/O via the band crates

3. **Multi-agent coordination.** Support for agent hierarchies where parent agents coordinate sub-agents:
   - PromptScript `@agents` compiled to sub-agent manifests
   - Inter-agent communication via structured message passing
   - Fleet coordination for Agent-as-Project-Manager

4. **All ten killer apps.** Complete implementations of all ten applications described in Section 4, running on the open-mind runtime.

**Success criteria:** All ten killer apps run on the open-mind runtime, producing structured output that is directly consumed by end users or downstream systems. No code generation occurs at any point in the pipeline.

### Phase 4: Self-Improving Agent Applications (Months 12-18)

**Objective:** Implement the SIA² (Self-Improving Agent Applications) loop, where agents evaluate and improve their own output quality.

**Deliverables:**

1. **Feedback loop infrastructure.**
   - Output quality scoring (automated metrics per output type)
   - Prompt self-adjustment based on quality scores
   - A/B testing framework for agent output variants
   - Learning from human feedback (explicit ratings and implicit signals)

2. **Meta-agent capabilities.** Agents that can:
   - Analyze their own output quality over time
   - Adjust their PromptScript parameters dynamically (within sealed constraints)
   - Request capability upgrades (new WASM modules) when output quality plateaus
   - Generate new skill compositions by combining existing capabilities

3. **Automated skill authoring.** Agents that can author new `.prs` skill definitions:
   - Identify capability gaps from failed output validation
   - Propose new skill compositions using existing capabilities
   - Generate PromptScript-compatible skill definitions
   - Submit skills for human review before deployment

4. **Quality metrics dashboard.** Real-time monitoring of:
   - Agent output quality across all applications
   - Schema validation pass/fail rates
   - Capability plugin utilization
   - Self-improvement trajectories

**Success criteria:** Agents demonstrate measurable output quality improvement over 100+ invocations without human intervention. The SIA² loop closes: agents produce output, evaluate it, and improve autonomously.

---

## 6. Strategic Implications

### 6.1 Competitive Moat

The combination of PromptScript's compositional power with 300+ Rust crates compiled to WASM creates a unique competitive position. No other system offers:

- **Declarative agent definition** with inheritance, overlays, and parameterized templates
- **Typed capability plugins** from a mature Rust crate ecosystem
- **Structured output validation** with schema enforcement
- **Self-improving agents** with closed-loop quality feedback

This is not a feature advantage—it is a paradigm advantage. Competitors operating in the code-generation paradigm cannot match the latency, reliability, and directness of the post-code approach.

### 6.2 Ecosystem Effects

Open-sourcing the open-mind runtime creates ecosystem effects:

- **Capability plugin marketplace.** Third parties can publish WASM capability plugins that any agent can use.
- **PromptScript skill marketplace.** Reusable `.prs` skill definitions become shareable artifacts.
- **Agent application marketplace.** Complete agent-as-application deployments become distributable products.

PromptScript's registry system (`@use github.com/org/registry`) already supports the distribution infrastructure. The open-mind runtime provides the execution substrate. Together, they enable a marketplace where agent capabilities compose and compound.

### 6.3 Research Implications

The post-code paradigm opens research directions:

- **Output-space reasoning.** How do agents reason differently when their output is structured data vs. code?
- **Capability composition theory.** Using our `categorical-agents` crate to formally model capability composition via category theory.
- **Conservation law budgets.** Applying our `conservation-law` crate to formalize resource constraints on agent output (emotional energy in therapy, creative energy in composition, analytical energy in research).
- **Topological agent analysis.** Using `persistent-sheaf` to analyze the structure of agent output spaces.

---

## 7. Conclusion

The post-code paradigm is not a distant vision—it is the natural endpoint of the trajectory we are already on. LLMs produce structured output. WASM provides universal runtime. Rust provides the capability substrate. PromptScript provides the compositional glue. What is missing is the integrating framework: the runtime that connects these pieces into a coherent whole.

That framework is open-mind. It is the runtime substrate where agents ARE applications—where the agent's structured response IS the product, not code that produces the product.

The roadmap is clear. Phase 1 validates the core pipeline with music composition. Phase 2 establishes schemas and validation for all output types. Phase 3 builds the full runtime with all ten killer apps. Phase 4 closes the loop with self-improving agents.

This is the SuperInstance thesis: that the future of software is not software at all. It is structured intelligence, directly delivered, composed on demand, and continuously improving. The code was never the point. The output was always the point.

---

*Document generated: 2026-06-07*  
*Repository: github.com/SuperInstance/agent-operations*  
*Related: github.com/SuperInstance/promptscript*
