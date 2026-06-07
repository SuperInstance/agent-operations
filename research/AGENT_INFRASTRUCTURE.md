# Agent Infrastructure — Research Report

**Date:** 2026-06-07  
**Branch:** research/a2a-agents  
**Author:** R&D Research Agent  
**Status:** DRAFT — for SuperInstance fleet integration planning

---

## Executive Summary

The agent infrastructure landscape has matured rapidly through 2025-2026. Google's **A2A protocol** (v1.0.0, now under the Linux Foundation) and Anthropic's **MCP (Model Context Protocol)** have emerged as the two dominant open standards — A2A for agent-to-agent communication and MCP for agent-to-tool/context integration. Together they form the TCP/IP layer of the agentic web.

Multi-agent orchestration frameworks (CrewAI, AutoGen, LangGraph, OpenAI Agents SDK) are converging on similar patterns: sequential workflows, hierarchical delegation, and debate-based refinement. But none address the deep mathematical foundations — composition algebras, conservation laws, spectral ranking — that SuperInstance's crate stack provides.

This report maps the state of the art across 10 research domains to SuperInstance's existing crates and recommends a concrete integration path that positions our stack as the **mathematically rigorous infrastructure layer** for production agent fleets.

---

## Findings

### 1. Google A2A Protocol (2025)

- **What:** Agent2Agent is an open protocol enabling interoperability between opaque agentic applications. Now at v1.0.0 under the Linux Foundation (contributed by Google). Uses JSON-RPC 2.0 over HTTP(S) with SSE streaming. Three-layer architecture: Data Model (Task, Message, AgentCard, Part, Artifact), Abstract Operations (Send Message, Get Task, Cancel Task, etc.), and Protocol Bindings (JSON-RPC, gRPC, HTTP/REST). SDKs exist for Python, Go, JS, Java, .NET, and Rust. Core design: agents discover each other via "Agent Cards" (capability descriptors), negotiate interaction modalities, and collaborate on long-running tasks without exposing internal state.

- **Key Projects/Papers:**
  - [a2aproject/A2A](https://github.com/a2aproject/A2A) — Official spec and repo
  - [A2A Specification v1.0.0](https://a2a-protocol.org/latest/specification/) — Full protocol spec
  - [A2A Python SDK](https://github.com/a2aproject/a2a-python) — `pip install a2a-sdk`
  - [A2A Rust SDK](https://github.com/a2aproject/a2a-rs) — `cargo add a2a-lf`
  - [Google DeepLearning.AI Course](https://goo.gle/dlai-a2a) — A2A + MCP integration course with IBM Research

- **SuperInstance Connection:**
  - `a2a-future`: Our reverse-actualization and deliberation protocols should implement A2A's AgentCard as the discovery mechanism, with our deliberation layer extending A2A's task lifecycle
  - `si-runtime`: Direct integration point — our multi-language runtime should expose A2A-compliant endpoints natively
  - `CAPABILITY.toml`: Maps directly to A2A's AgentCard concept; we should generate AgentCard JSON from CAPABILITY.toml

- **Integration Strategy:**
  1. Implement A2A server/client traits in `si-runtime` so every agent auto-exposes A2A endpoints
  2. Build CAPABILITY.toml → AgentCard converter
  3. Extend A2A's Task model with our deliberation protocol ( γ+H=C budget per task)
  4. Use A2A's push notification system as transport for `t-minus` scheduling signals
  5. Implement our spectral-fleet eigenvalue ranking as an A2A middleware

- **Priority:** **HIGH** — A2A is becoming the HTTP of agents. Must be native.

---

### 2. Anthropic MCP (Model Context Protocol)

- **What:** An open-source standard for connecting AI applications to external systems — tools, data sources, and workflows. Client-server architecture: MCP Host (AI app) → MCP Client → MCP Server (context provider). JSON-RPC 2.0 based. Two layers: Data layer (tools, resources, prompts, notifications) and Transport layer (STDIO for local, Streamable HTTP for remote). Supported by Claude, ChatGPT, VS Code, Cursor, and many others. Think "USB-C for AI" — standardized connector.

- **Key Projects/Papers:**
  - [modelcontextprotocol.io](https://modelcontextprotocol.io) — Official docs
  - [MCP Specification](https://modelcontextprotocol.io/specification/latest) — Protocol spec
  - [MCP Servers](https://github.com/modelcontextprotocol/servers) — Reference implementations
  - [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — Dev tooling

- **SuperInstance Connection:**
  - `CAPABILITY.toml`: Our self-describing capability system is semantically richer than MCP's tool descriptions; we should expose CAPABILITY.toml capabilities as MCP tools/resources
  - `a2a-future`: A2A handles agent-to-agent; MCP handles agent-to-tool. They're complementary, not competing. Our stack should speak both.
  - `A2A-native-notebookLM`: Should expose NotebookLM content as MCP resources for other agents to consume

- **Integration Strategy:**
  1. Build an MCP Server adapter in `si-runtime` that auto-exposes agent capabilities as MCP tools
  2. Build an MCP Client that lets our agents consume external MCP servers as tools
  3. Bridge CAPABILITY.toml → MCP tool descriptions (and vice versa for discovery)
  4. Use MCP's resource subscription for `agent-homeostasis` monitoring signals

- **Priority:** **HIGH** — MCP is the tool-integration standard. A2A + MCP = complete agent connectivity.

---

### 3. Multi-Agent Orchestration Frameworks

- **What:** The framework landscape has consolidated around key patterns:

  | Framework | Backed By | Key Pattern | Notable |
  |-----------|-----------|-------------|---------|
  | **CrewAI** | CrewAI Inc | Role-based crews, sequential/hierarchical | 60% of Fortune 500, 450M+ workflows/month |
  | **AutoGen** | Microsoft | Conversational agents, multi-agent chat | Flexible agent topology, code execution |
  | **LangGraph** | LangChain | Graph-based state machines | Cyclical workflows, persistence |
  | **OpenAI Agents SDK** | OpenAI | Single/multi-agent orchestration | Responses API, built-in tools, tracing |
  | **Semantic Kernel** | Microsoft | Enterprise orchestration | Planners, connectors, .NET/Python/Java |
  | **Agno** | Agno | Lightweight, fast multi-agent | Model-agnostic, minimal overhead |
  | **Letta** | Letta (MemGPT) | Stateful agents with memory | Long-term memory management |
  | **Claude Agent SDK** | Anthropic | Simple composable patterns | Augmented LLM building blocks |

  Anthropic's engineering blog emphasizes: *the most successful implementations use simple, composable patterns rather than complex frameworks.* Key patterns identified: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.

- **Key Projects/Papers:**
  - [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Patterns & best practices
  - [CrewAI](https://crewai.com/) — Enterprise agent platform
  - [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents) — Responses API + orchestration
  - [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) — Stateful graph workflows
  - [AutoGen](https://microsoft.github.io/autogen/) — Conversational multi-agent

- **SuperInstance Connection:**
  - `categorical-agents`: Our composition algebra is strictly more powerful than any framework's orchestration — functors and monoidal categories subsume sequential, parallel, and hierarchical patterns as special cases
  - `fleet-warden`: All frameworks lack built-in anomaly detection and circuit breakers — our fleet-warden provides this as middleware
  - `conservation-law`: No framework has resource budget tracking — our γ+H=C conservation gives formal guarantees

- **Integration Strategy:**
  1. Position SuperInstance not as "another framework" but as the **infrastructure/math layer** that frameworks can build on
  2. Build adapters: CrewAI agent → SuperInstance agent, LangGraph node → categorical-agents morphism
  3. Publish our orchestration patterns (via categorical-agents) as composable A2A-compatible workflows
  4. Whitepaper: "Category Theory for Multi-Agent Orchestration" showing our mathematical advantages

- **Priority:** **MEDIUM** — We don't compete with frameworks; we provide the formal substrate they lack.

---

### 4. Agent Communication Languages

- **What:** The field has evolved through three eras:
  1. **KQML (1993):** DARPA Knowledge Sharing Effort. Performatives (ask-one, tell, achieve) based on speech act theory (Searle, 1960s; Winograd & Flores, 1970s). Communication facilitators coordinate multi-agent interactions.
  2. **FIPA-ACL (2000s):** Standardized agent communication. Ontology-based: agents share a common ontology defining communicative acts. Implemented in JADE, FIPA-OS. Now largely superseded.
  3. **Modern (2025+):** Two approaches:
     - **A2A:** Structured JSON-RPC protocol with typed message parts (text, files, structured data)
     - **NLIP (Natural Language Interaction Protocol):** Ecma International standard (Dec 2025). Uses generative AI to translate between natural language and local ontologies — no shared ontology required. Hot-extensible.

  Speech act theory remains foundational: agents perform performatives (inform, request, promise, declare) on each other's knowledge and goal stores.

- **Key Projects/Papers:**
  - [KQML Specification](http://www.cs.umbc.edu/KQML/kqmlspec.ps) — Finin et al., 1993
  - [FIPA-ACL](https://en.wikipedia.org/wiki/FIPA-ACL) — Foundation for Intelligent Physical Agents
  - [NLIP — Ecma International](https://www.ecma-international.org/) — Natural Language Interaction Protocol, Dec 2025
  - Searle, J.R. "Speech Acts" (1969) — Foundational theory
  - Winograd, T. & Flores, F. "Understanding Computers and Cognition" (1986)

- **SuperInstance Connection:**
  - `categorical-agents`: Speech act performatives map to morphisms in our agent category. Inform = identity morphism on knowledge; Request = covariant functor; Promise = contravariant obligation. Our composition algebra gives formal semantics to speech act composition.
  - `a2a-future`: Should support NLIP-style natural language interaction alongside structured A2A messages

- **Integration Strategy:**
  1. Define a "speech act" type system in categorical-agents mapping Searle's taxonomy to category-theoretic morphisms
  2. Support both structured (A2A JSON-RPC) and natural (NLIP) communication modes in si-runtime
  3. Use our monoidal category structure to compose complex multi-step speech acts with formal correctness guarantees

- **Priority:** **MEDIUM** — Foundational for formal verification of agent interactions.

---

### 5. Consensus in Agent Systems

- **What:** Classical distributed consensus algorithms apply to multi-agent systems:
  - **Raft:** Leader election + log replication. Simple to understand. Used etcd, Consul.
  - **PBFT (Practical Byzantine Fault Tolerance):** Tolerates up to f Byzantine nodes with 3f+1 total. Used in Hyperledger Fabric.
  - **HotStuff (2018):** Linear BFT consensus. Used in Meta's Diem (formerly Libra).
  - **Tendermint:** BFT PoS consensus. Powers Cosmos ecosystem.
  
  For AI agents specifically: consensus becomes opinion aggregation. Agents may disagree on task decomposition, resource allocation, or strategic decisions. Traditional consensus assumes binary agreement; agent consensus must handle continuous-valued disagreements.

- **Key Projects/Papers:**
  - Ongaro, D. & Ousterhout, J. "In Search of an Understandable Consensus Algorithm" (Raft, 2014)
  - Castro, M. & Liskov, B. "Practical Byzantine Fault Tolerance" (PBFT, 1999)
  - Yin, M. et al. "HotStuff: BFT Consensus with Linearity and Responsiveness" (2018)
  - Kwon, J. "Tendermint: Consensus without Mining" (2014)

- **SuperInstance Connection:**
  - `hodge-consensus`: Our Hodge decomposition of disagreements is novel — decompose agent disagreement vector fields into exact (resolvable), co-exact (irreducible divergence), and harmonic (genuine ambiguity) components. This goes beyond binary agreement.
  - `conservation-law`: Budget constraints provide an invariant that consensus must preserve
  - `spectral-fleet`: Eigenvalue ranking determines which agents' opinions get more weight in consensus

- **Integration Strategy:**
  1. Implement Hodge decomposition as the consensus mechanism for multi-agent deliberation
  2. Prove that γ+H=C invariant is preserved through Hodge consensus rounds
  3. Use harmonic components (genuine ambiguity) to trigger human-in-the-loop escalation
  4. Publish: "Hodge-Theoretic Consensus for Multi-Agent Systems"

- **Priority:** **HIGH** — hodge-consensus is a unique differentiator with no equivalent in the ecosystem.

---

### 6. Agent Marketplaces & Economics

- **What:** Multi-agent economics draws from mechanism design and auction theory:
  - **VCG (Vickrey-Clarke-Groves) Auctions:** Truthful mechanism for task allocation. Agents bid true values.
  - **Contract Net Protocol:** Task announcement → bidding → awarding. Used in KQML/MAS since 1980s.
  - **Reinforcement Learning-based Allocation:** Agents learn optimal bidding strategies.
  - **Token/credit economies:** Agents earn and spend computational credits.
  
  No dominant standard exists yet. Most frameworks use simple priority queues or round-robin. The gap: no one has formalized resource conservation laws in agent economies.

- **Key Projects/Papers:**
  - Smith, R.G. "The Contract Net Protocol" (1980) — Foundational task allocation
  - Nisan, N. & Ronen, A. "Algorithmic Mechanism Design" (1999) — VCG for computation
  - Parkes, D.C. "Iterative Combinatorial Auctions" (2006) — Multi-round allocation
  - Prophet Inequality theory for online task allocation

- **SuperInstance Connection:**
  - `bid-engine`: Our auction mechanism for task allocation
  - `conservation-law`: γ+H=C provides the invariant that no existing agent marketplace has — formal budget conservation. Total system resources are conserved; budget flows are tracked.
  - `spectral-fleet`: Eigenvalue ranking determines agent priority in competitive allocation

- **Integration Strategy:**
  1. Implement VCG-inspired truthful auction in bid-engine with γ+H=C as the budget constraint
  2. Prove incentive compatibility under conservation law
  3. Build an "Agent Marketplace" UI where agents bid on tasks with budget credits
  4. Use spectral-fleet ranking as reputation signal in marketplace

- **Priority:** **MEDIUM** — Important for scaling but not blocking.

---

### 7. Formal Verification of Multi-Agent Systems

- **What:** Model checking for agent protocols uses temporal logics (LTL, CTL, ATL) to verify properties:
  - **Model Checking (Clarke, Emerson, Sifakis — Turing Award 2007):** Exhaustive state-space exploration. Tools: SPIN, NuSMV, PRISM.
  - **Agent-Based Verification:** ATL (Alternating-Time Temporal Logic) reasons about what coalitions of agents can achieve.
  - **Runtime Verification:** Monitor properties at runtime (e.g., "budget never exceeds C").
  - **SMT-based Verification:** Use Z3/CVC5 to prove protocol properties.
  
  Key challenge: state-space explosion in multi-agent systems. Compositional verification (verify components independently) is essential.

- **Key Projects/Papers:**
  - Alur, R. et al. "Alternating-Time Temporal Logic" (ATL, 2002)
  - Kwiatkowska, M. et al. "PRISM: Probabilistic Model Checking" (2009)
  - Clarkson, M. & Schneider, F. "Hyperproperties" (2010) — For multi-agent security

- **SuperInstance Connection:**
  - `conservation-law`: The γ+H=C invariant is a hyperproperty (relates multiple traces). We can formally verify it using SMT solvers.
  - `categorical-agents`: Category theory provides compositional verification — verify functors independently, compose results.
  - `fleet-warden`: Circuit breakers can be verified to maintain safety invariants.

- **Integration Strategy:**
  1. Write Z3/lean4 formalization of γ+H=C conservation law
  2. Build a PRISM model of fleet-warden circuit breaker behavior
  3. Prove categorical-agents composition preserves conservation invariants
  4. Publish: "Formal Verification of Conservation Laws in Agent Fleets"

- **Priority:** **MEDIUM** — Formal verification is a differentiator for enterprise/safety-critical deployments.

---

### 8. Swarm Intelligence Patterns

- **What:** Nature-inspired coordination without central control:
  - **Stigmergy:** Agents coordinate through environment modifications (ant pheromone trails). No direct communication needed. Key insight: *trace left by one action stimulates succeeding actions by same or different agent.* Self-organization emerges from simple local rules.
  - **Ant Colony Optimization (ACO):** Pheromone-based path optimization. Applied to routing, scheduling.
  - **Particle Swarm Optimization (PSO):** Agents move through solution space, influenced by personal best and global best.
  - **Firefly Algorithm:** Agents synchronize flashing patterns — useful for consensus timing.
  
  Modern application: agent task queues as pheromone trails; error patterns as stigmergic signals.

- **Key Projects/Papers:**
  - Grassé, P.P. "La reconstruction du nid" (1959) — Original stigmergy paper
  - Dorigo, M. & Gambardella, L.M. "Ant Colonies for the Traveling Salesman Problem" (1997)
  - Kennedy, J. & Eberhart, R. "Particle Swarm Optimization" (1995)
  - Parunak, H.V.D. "Making Swarming Happen" (2003) — Stigmergy in software agents

- **SuperInstance Connection:**
  - `error-forest`: Our mycorrhizal mesh network is directly inspired by biological stigmergy. Error signals propagate through the mesh like pheromone trails, enabling agents to avoid known failure patterns.
  - `fleet-warden`: Anomaly detection as stigmergic signaling — anomalous patterns leave "traces" that other agents detect.
  - `categorical-agents`: Swarm composition as monoidal product of simple agent behaviors.

- **Integration Strategy:**
  1. Formalize error-forest propagation as a stigmergic protocol (pheromone decay → error relevance timeout)
  2. Implement ACO-style task routing: agents "lay pheromone" on successful task paths
  3. Build PSO-based hyperparameter optimization for agent fleet tuning
  4. Publish: "Mycorrhizal Mesh Networks: Biological Stigmergy for Agent Error Propagation"

- **Priority:** **LOW** — Conceptually valuable, but error-forest already captures the core insight.

---

### 9. Agent Memory & Knowledge Management

- **What:** Long-term memory architectures for agents have evolved rapidly:
  - **RAG (Retrieval-Augmented Generation):** Vector databases (Pinecone, Weaviate, ChromaDB) + embedding models. Standard pattern: embed → retrieve → augment prompt.
  - **MemGPT / Letta:** Virtual context management — tiered memory (core, archival, recall) with LLM-managed paging. Enables infinite context windows.
  - **Shared Knowledge Bases:** Agents read/write to common vector stores or graph databases.
  - **Episodic Memory:** Agents remember past interactions and outcomes for learning.
  - **Semantic Memory:** Structured knowledge graphs (entity-relationship triples).

- **Key Projects/Papers:**
  - Packer, C. et al. "MemGPT: Towards LLMs as Operating Systems" (2023) → Now Letta
  - Lewis, P. et al. "Retrieval-Augmented Generation" (2020) — Original RAG paper
  - [Letta](https://www.letta.com/) — Stateful agent memory platform
  - ChromaDB, Pinecone, Weaviate — Vector database ecosystems

- **SuperInstance Connection:**
  - `open-mind`: Our shared knowledge base for agent fleets
  - `persistent-sheaf`: Sheaf-theoretic persistent memory — local agent memory sections glued together via sheaf restriction maps. This is mathematically richer than simple RAG.
  - `A2A-native-notebookLM`: Self-service knowledge management for agents, analogous to Google NotebookLM but for agent consumption

- **Integration Strategy:**
  1. Implement persistent-sheaf with A2A-compliant read/write endpoints
  2. Build NotebookLM-style interface where agents can "upload" knowledge and query it
  3. Integrate sheaf cohomology to detect "knowledge gaps" (non-trivial cohomology classes = missing information)
  4. Publish: "Sheaf-Theoretic Memory Management for Multi-Agent Systems"

- **Priority:** **HIGH** — Memory is critical. persistent-sheaf is a unique approach.

---

### 10. Agent Safety & Alignment

- **What:** Safety in multi-agent systems is an emerging concern:
  - **Guardrails:** Input/output filtering, content safety classifiers (NVIDIA NeMo Guardrails, Llama Guard).
  - **Constitutional AI (CAI):** Anthropic's approach — AI systems guided by principles/constraints. RL from AI Feedback (RLAIF).
  - **Red-Teaming Multi-Agent Systems:** Testing adversarial interactions between agents. Prompt injection in multi-agent pipelines.
  - **Agent Confinement:** Sandboxing agent actions, limiting tool access.
  - **Budget as Safety:** Constraining agent resource consumption as a safety mechanism (compute budget = impact budget).
  
  Key insight: multi-agent systems amplify safety risks. One compromised agent can poison information for the entire fleet.

- **Key Projects/Papers:**
  - Bai, Y. et al. "Constitutional AI: Harmlessness from AI Feedback" (Anthropic, 2022)
  - [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) — Programmable safety rails
  - Meta Llama Guard — LLM-based safety classifier
  - "Red-Teaming Large Language Models" (various, 2023-2025)

- **SuperInstance Connection:**
  - `conservation-law`: γ+H=C budget constraints ARE safety constraints — agents literally cannot exceed their resource allocation. Budget = safety invariant.
  - `fleet-warden`: Anomaly detection as safety monitoring. Circuit breakers prevent cascading failures.
  - `agent-homeostasis`: Self-regulation as alignment — agents maintain internal equilibrium.
  - `categorical-agents`: Functors preserve structure — safety properties are preserved through composition.

- **Integration Strategy:**
  1. Position γ+H=C as "conservation-based safety" — a novel safety paradigm distinct from guardrails and constitutional AI
  2. Implement fleet-warden as a multi-agent safety monitor with circuit breaker per agent
  3. Prove: if each agent satisfies conservation law, the composed system is safe (categorical proof)
  4. Build red-team test suite for multi-agent adversarial scenarios
  5. Publish: "Conservation Laws as Safety Invariants in Multi-Agent Systems"

- **Priority:** **HIGH** — Safety is table-stakes for enterprise adoption. Our approach is unique.

---

## Protocol Comparison Matrix

| Feature | A2A | MCP | NLIP | SuperInstance |
|---------|-----|-----|------|---------------|
| **Purpose** | Agent ↔ Agent | Agent ↔ Tool | Agent ↔ Agent (NL) | Both + Math |
| **Transport** | JSON-RPC / HTTP / gRPC | JSON-RPC / STDIO / HTTP | Application layer | All + custom |
| **Discovery** | AgentCard | Tool/Resource listing | N/A | CAPABILITY.toml |
| **Streaming** | SSE | Server-Sent Events | N/A | Native + backpressure |
| **State Mgmt** | Task lifecycle | Stateless | N/A | persistent-sheaf |
| **Budget/Resource** | None | None | None | γ+H=C conservation |
| **Safety** | Auth/Z | Permission model | Security built-in | Conservation + fleet-warden |
| **Consensus** | None | None | None | hodge-consensus |
| **Composition** | Manual orchestration | Manual chaining | N/A | categorical-agents algebra |
| **Ranking** | None | None | None | spectral-fleet eigenvalues |
| **Runtime** | Per-language SDKs | Per-language SDKs | Per-language SDKs | si-runtime unified API |
| **Memory** | None (stateless tasks) | Resources (read-only) | N/A | persistent-sheaf + open-mind |
| **Anomaly Detection** | None | None | None | fleet-warden |
| **Scheduling** | None | None | None | t-minus |
| **Formal Basis** | Spec only | Spec only | Spec only | Category theory + Hodge theory |

**Key takeaway:** A2A and MCP are necessary but not sufficient. They provide connectivity; SuperInstance provides **correctness, conservation, and composition**.

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SuperInstance Fleet                    │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Agent Alpha  │  │  Agent Beta   │  │  Agent Gamma  │  │
│  │  (Rust)       │  │  (Python)     │  │  (TypeScript) │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │            │
│  ═══════╪═════════════════╪═════════════════╪══════════  │
│         │     si-runtime (unified agent API) │           │
│  ═══════╪═════════════════╪═════════════════╪══════════  │
│         │                 │                 │            │
│  ┌──────┴─────────────────┴─────────────────┴──────┐   │
│  │              categorical-agents                  │   │
│  │     (composition algebra, functors, monoids)     │   │
│  └──────────────────────┬──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────┼──────────────────────────┐   │
│  │     conservation-law │  hodge-consensus          │   │
│  │     (γ+H=C budget)   │  (Hodge decomposition)    │   │
│  └──────────────────────┼──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────┼──────────────────────────┐   │
│  │  fleet-warden        │  spectral-fleet           │   │
│  │  (anomaly, circuit)  │  (eigenvalue ranking)     │   │
│  └──────────────────────┼──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────┼──────────────────────────┐   │
│  │  t-minus             │  agent-homeostasis        │   │
│  │  (scheduling)        │  (self-regulation)        │   │
│  └──────────────────────┼──────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────┼──────────────────────────┐   │
│  │  persistent-sheaf    │  error-forest             │   │
│  │  (memory)            │  (stigmergic errors)      │   │
│  └──────────────────────┴──────────────────────────┘   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │          A2A Layer (Agent ↔ Agent comms)           │  │
│  │  AgentCard ← CAPABILITY.toml  │  Task lifecycle   │  │
│  │  JSON-RPC + SSE + gRPC        │  Push notifications│  │
│  └───────────────────────┬───────────────────────────┘  │
│                          │                              │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │          MCP Layer (Agent ↔ Tool comms)            │  │
│  │  Tools ← CAPABILITY.toml  │  Resources  │ Prompts │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Layer ordering (inside → outside):**
1. **Core math layer:** conservation-law, categorical-agents, hodge-consensus
2. **Infrastructure layer:** fleet-warden, spectral-fleet, t-minus, agent-homeostasis
3. **Memory layer:** persistent-sheaf, open-mind, error-forest
4. **Protocol layer:** A2A (agent-agent) + MCP (agent-tool)
5. **Runtime layer:** si-runtime (unified multi-language API wrapping everything)

---

## Top 5 Integration Priorities

### 1. A2A Compliance in si-runtime (HIGH, Week 1-2)
**Why:** A2A is becoming the standard. Every SuperInstance agent must speak it.  
**What:** Implement A2A server/client traits in si-runtime. Auto-generate AgentCard from CAPABILITY.toml. Support JSON-RPC, SSE streaming, and push notifications.  
**Deliverable:** Any agent built on si-runtime is automatically A2A-compliant.

### 2. CAPABILITY.toml → AgentCard + MCP Tool Bridge (HIGH, Week 2-3)
**Why:** Our CAPABILITY.toml is richer than both A2A AgentCard and MCP tool descriptions.  
**What:** Build converters: CAPABILITY.toml → AgentCard JSON, CAPABILITY.toml → MCP tool definitions. Bidirectional sync.  
**Deliverable:** One CAPABILITY.toml drives both A2A discovery and MCP tool exposure.

### 3. Conservation-Law Formal Verification (HIGH, Week 3-5)
**Why:** γ+H=C is our core differentiator. Proving it formally enables enterprise/safety-critical adoption.  
**What:** Formalize in lean4 or Z3. Prove invariance under composition (categorical-agents), consensus (hodge-consensus), and scaling (fleet-warden).  
**Deliverable:** Mechanically verified proof that budget conservation holds across all fleet operations.

### 4. Hodge-Consensus Implementation (HIGH, Week 4-6)
**Why:** No other system has Hodge-theoretic consensus. Unique IP.  
**What:** Implement Hodge decomposition for agent disagreement fields. Exact → resolve, co-exact → escalate, harmonic → human-in-loop.  
**Deliverable:** Working consensus protocol with formal disagreement decomposition.

### 5. persistent-sheaf with A2A Endpoints (HIGH, Week 5-8)
**Why:** Memory is critical. Sheaf-theoretic approach is novel.  
**What:** Implement persistent-sheaf with A2A-compliant read/write. Sheaf cohomology for gap detection.  
**Deliverable:** Shared agent memory with mathematical guarantees about knowledge completeness.

---

## Appendix: Competitive Landscape Summary

| Player | What They Have | What They Lack | SuperInstance Advantage |
|--------|---------------|----------------|------------------------|
| Google A2A | Interop protocol | No math, no safety, no memory | categorical-agents + conservation-law |
| Anthropic MCP | Tool integration | No agent-agent, no budgets | si-runtime speaks both A2A + MCP |
| CrewAI | Enterprise orchestration | No formal basis, no conservation | Our stack is the formal substrate |
| OpenAI Agents SDK | Simple orchestration | No fleet management, no ranking | fleet-warden + spectral-fleet |
| LangGraph | Graph workflows | No consensus, no budgets | hodge-consensus + conservation-law |
| Letta | Agent memory | No sheaf theory, no composition | persistent-sheaf + categorical-agents |
| AutoGen | Conversational agents | No formal verification | conservation-law formal proofs |

**Positioning:** SuperInstance is not "another agent framework." We are the **formal infrastructure layer** — the mathematics that makes agent fleets provably correct, budget-safe, and composable. We sit *below* frameworks, *above* protocols.

---

*"The best protocols are the ones that make mathematics invisible."* — SuperInstance Engineering Principle
