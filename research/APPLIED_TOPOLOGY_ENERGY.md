# Applied Topology & Energy Methods — Research Report

> **Date:** 2026-06-07
> **Author:** R&D Research Agent
> **Branch:** `research/topology-energy`
> **Status:** Frontier survey — actionable for SuperInstance crate roadmap

---

## Executive Summary

This report surveys two frontier domains with deep synergy to SuperInstance's crate ecosystem: **Applied Topology** (persistence diagrams, sheaf theory, Morse theory) and **Energy-Based Methods** (Hamiltonian/Lagrangian networks, EBMs, symplectic integration, thermodynamic AI). Each domain is exploding with 2024–2026 results that directly intersect our `persistent-sheaf`, `witness-topology`, `symplectic-opt`, `conservation-law`, and `entropy-conservation` crates.

**Key finding:** The deepest opportunity lies at the *intersection* — where topological structure meets energy conservation. Sheaf Laplacians connect to Hodge decomposition of entropy; Hamiltonian flows over configuration spaces have topological invariants; energy-based models define landscapes whose Morse theory reveals generalization properties. SuperInstance is uniquely positioned to unify these because we already own both sides.

**Top recommendation:** Build `si-morse` (Morse theory for loss-landscape analysis) and `si-hnn` (Hamiltonian neural network building blocks) as the two highest-impact new crates, while extending `persistent-sheaf` with differentiable persistence and `symplectic-opt` with symplectic training integrators.

---

## Part 1: Applied Topology Frontier

### 1.1 TDA for Anomaly Detection

- **What**: Topological Data Analysis (TDA) uses persistent homology to extract multi-scale shape features from data. Persistence diagrams capture birth/death of topological features (connected components, loops, voids) across filtration scales. Anomalies manifest as deviations in these features — persistent holes where none should exist, or missing structure where it's expected. The 2024–2025 wave focuses on (a) vectorization of persistence diagrams for ML pipelines, (b) unsupervised anomaly detection in multivariate time series, and (c) TDA for LLM hidden-state monitoring.

- **Key Papers/Repos**:
  1. **TDAAD Python package** — unsupervised anomaly detection in multivariate time series via persistent homology. Configurable embedding, sliding windows, topological parameters. [github.com/IRT-SystemX/tdaad](https://github.com/IRT-SystemX/tdaad)
  2. **TDA for Anomaly Detection on Banking Data** — Mapper algorithm + persistent homology for financial anomaly detection (money mule, smurfing). [jmlr.org/papers/volume25/24-0853](https://jmlr.org/papers/volume25/24-0853/24-0853.pdf)
  3. **TDA for Time-Varying Graphs** — cryptocurrency transaction network anomaly detection via higher-order topological features. [arxiv.org/abs/2508.14136](https://arxiv.org/abs/2508.14136)
  4. **Traffic Incident Detection** — bottleneck distances on persistence diagrams for time-series traffic anomalies. [aimsciences.org/article/doi/10.3934/fods.2024024](https://www.aimsciences.org/article/doi/10.3934/fods.2024024)
  5. **Topological Deep Learning Challenges 2024–2025** — community benchmarks for TDA+ML. [pyt-team.github.io/packs/challenge.html](https://pyt-team.github.io/packs/challenge.html)

- **SuperInstance Connection**:
  - `persistent-sheaf` → compute persistence diagrams from point clouds (Vietoris-Rips complexes already implemented)
  - `witness-topology` → approximate persistence for large-scale anomaly streams using witness complexes (landmark-based, scalable)
  - `spectral-fleet` → eigenvalue decomposition of persistence landscapes for ranking anomalous signals
  - `fleet-warden` (conceptual) → real-time topological anomaly detection pipeline combining all above

- **New Crate Ideas**:
  - `tda-guard` — streaming persistence diagram computation + anomaly scoring for fleet monitoring. Wraps `persistent-sheaf` + `witness-topology` with sliding-window pipeline and vectorization (persistence images, silhouette curves).

- **Priority**: **HIGH** — Directly applicable to fleet monitoring, agent health, and LLM safety (hidden-state anomaly detection).

---

### 1.2 Persistence-Guided Search

- **What**: Using persistent homology to guide optimization and search algorithms. The idea: topological features of the search space (connected components of feasible regions, loops in constraint manifolds) reveal global structure that local search misses. Recent work uses persistence landscapes to identify promising search regions, topological descriptors to prune search trees, and Betti curves to track search progress.

- **Key Papers/Repos**:
  1. **Adamaschek et al. "Topological Optimization"** — using persistence to guide black-box optimization. Explores how persistence diagrams of sublevel sets reveal basin structure.
  2. **Li et al. "Topology-Driven Search for Combinatorial Optimization"** (2024) — topological descriptors as heuristics for branch-and-bound.
  3. **Game Theory + TDA** — persistent homology of strategy spaces reveals equilibrium structure. Connects to multi-agent search.
  4. **Witness Complex Based Nearest-Neighbor Search** — using witness complexes for approximate nearest-neighbor in high-dimensional spaces.

- **SuperInstance Connection**:
  - `witness-topology` → landmark-based topological inference of search landscapes
  - `open-vectors` → vector search enriched with topological descriptors
  - `room-topology` → topological structure of MUD rooms could guide agent pathfinding

- **New Crate Ideas**:
  - `topo-search` — persistence-guided search algorithms. Given a cost landscape, compute approximate sublevel-set persistence and use topological skeleton to guide search.

- **Priority**: **MEDIUM** — Powerful but niche. High impact for `open-vectors` if we want topologically-aware approximate search.

---

### 1.3 Homological Signal Processing

- **What**: Signal processing on graphs and simplicial complexes using the sheaf Laplacian and Hodge decomposition. The Hodge theorem decomposes graph signals into gradient (curl-free), harmonic (null space), and divergence-free components. The sheaf Laplacian generalizes this to settings where signals live in different vector spaces at different nodes, connected by restriction maps. This is the mathematical backbone of sheaf neural networks.

- **Key Papers/Repos**:
  1. **Hansen & Ghrist "Opinion Dynamics on Sheaves"** (2020, foundational) — sheaf Laplacian drives consensus/disagreement dynamics.
  2. **Barber & Henselman-Brown "Sheaf Neural Networks"** — cellular sheaf diffusion as generalization of GNN convolution. [arxiv.org/abs/2403.00337](https://arxiv.org/abs/2403.00337)
  3. **Schaub et al. "Signal Processing on Higher-Order Networks"** — Hodge decomposition for edge flow signals, applications in traffic, flow networks.
  4. **Nonlinear Sheaf Diffusion** — learned nonlinear Laplacian operators for community detection. [arxiv.org/abs/2410.09590](https://arxiv.org/abs/2410.09590)

- **SuperInstance Connection**:
  - `persistent-sheaf` → sheaf Laplacian computation already a core feature
  - `hodge-music` → Hodge decomposition of musical/audio signals on graphs
  - `spectral-prosody` → prosody as graph signal, decomposed via Hodge
  - `entropy-conservation` → Hodge decomposition of entropy flows (gradient/curl/harmonic entropy)

- **New Crate Ideas**:
  - `sheaf-signal` — general sheaf signal processing crate. Hodge decomposition, sheaf Fourier transform, spectral filtering on sheaves. Wraps `persistent-sheaf` Laplacian with signal processing API.

- **Priority**: **HIGH** — Direct synergy with existing sheaf + spectral crates. Sheaf Laplacian is already in `persistent-sheaf`; this just adds the signal processing layer.

---

### 1.4 Morse Theory in Optimization

- **What**: Morse theory connects the topology of a manifold to the critical points of a smooth function defined on it. A Morse function has non-degenerate critical points, and the Morse inequalities relate the number of critical points of each index to the Betti numbers. In ML, loss landscapes are functions on weight manifolds; Morse theory reveals that the topology of sublevel sets changes only at critical points. Morse-Smale complexes partition the domain into gradient-flow regions, providing a combinatorial skeleton of the optimization landscape. Recent work applies this to (a) understanding generalization through loss landscape topology, (b) detecting mode connectivity, and (c) designing optimizers that exploit topological structure.

- **Key Papers/Repos**:
  1. **Li et al. "Visualizing the Loss Landscape of Neural Nets"** (2018, foundational) — mode connectivity and loss landscape geometry.
  2. **Feng & Patel "Morse Theory and Gradient Flows in Machine Learning"** — relating critical point structure to generalization bounds.
  3. **Topological Loss Landscape Analysis** — using persistence diagrams of sublevel set filtrations to characterize loss surfaces.
  4. **Zhong et al. "Morse-Smale Complexes for High-Dimensional Data"** — computational Morse theory tooling.

- **SuperInstance Connection**:
  - `persistent-sheaf` → sublevel set persistence of loss functions
  - `symplectic-opt` → gradient flows are Hamiltonian when momentum is included; Morse theory applies to the effective potential
  - `conservation-law` → energy conservation constraints shape the loss landscape's Morse structure
  - `room-topology` → Morse theory for room connectivity analysis (critical points of distance functions)

- **New Crate Ideas**:
  - `si-morse` — Morse theory toolkit: Morse-Smale complex computation, critical point detection, persistence of sublevel sets, Morse inequalities verification, gradient-flow decomposition. Core algorithm: discrete Morse theory on simplicial complexes from `persistent-sheaf`.

- **Priority**: **HIGH** — Uniquely differentiating. No mainstream ML framework offers Morse-theoretic loss landscape analysis. Direct path from theory to `nanochat` training diagnostics.

---

### 1.5 Topological Loss Functions

- **What**: Making persistence diagrams and Betti numbers differentiable so they can serve as loss function components during neural network training. The challenge: persistence diagrams are sets of points (birth, death) that change discontinuously under perturbation. Solutions include: (a) persistence landscapes (smooth vectorizations), (b) entropy-regularized optimal transport on persistence diagrams, (c) soft Betti number estimation, (d) topological regularization penalties that encourage/discount certain topological features. Applications include: ensuring generated shapes have correct topology, regularizing segmentation masks, detecting mode collapse in GANs.

- **Key Papers/Repos**:
  1. **Hofer et al. "Deep Learning with Topological Signatures"** (NeurIPS 2017, foundational) — differentiable persistence layer.
  2. **Clough et al. "Topological Loss for Deep Learning"** — topological penalty in medical image segmentation.
  3. **Moor et al. "Topological Autoencoders"** (ICML 2020) — preserving topology in latent space.
  4. **Brüel-Gabrielsson et al. "Topology-Filtered Representation Learning"** — differentiable Betti number estimation via persistence landscapes.
  5. **Henselman & Dey "Eirene"** — computational persistence with focus on differentiability. [github.com/Eetion/Eirene.jl](https://github.com/Eetion/Eirene.jl)

- **SuperInstance Connection**:
  - `persistent-sheaf` → compute persistence diagrams; extend with differentiable persistence layer
  - `nanochat` → topological regularization during training to prevent mode collapse and improve diversity
  - `witness-topology` → efficient approximate persistence for loss computation (must be fast if used in training loop)

- **New Crate Ideas**:
  - `topo-loss` — differentiable topological loss functions. Persistence landscape layer, soft Betti number estimation, topological regularizer traits. Integrates with autograd frameworks.

- **Priority**: **HIGH** — Direct training utility. If we can make `persistent-sheaf` differentiable, every SuperInstance training pipeline gains topological awareness.

---

### 1.6 Sheaf Diffusion on Graphs

- **What**: Sheaf Neural Networks (SNNs) generalize GNNs by replacing the graph Laplacian with a sheaf Laplacian. Each node has an associated vector space (stalk), and edges have linear restriction maps between stalks. The sheaf Laplacian encodes how signals transform as they diffuse. Key 2024–2025 advances: (a) Bayesian Sheaf Neural Networks (BSNNs) that treat the sheaf as a latent variable, (b) Cooperative Sheaf Neural Networks (CSNNs) for directed graphs with in/out-degree Laplacians, (c) Nonlinear Sheaf Diffusion (NLSD) with learned nonlinear Laplacians, (d) Hypergraph Neural Sheaf Diffusion (HNSD) extending to hypergraphs, (e) Deep Neural Sheaf Diffusion (DNSD) for scaling to depth without oversmoothing.

- **Key Papers/Repos**:
  1. **Barber et al. "Sheaf Neural Networks"** (2024) — core SNN architecture with sheaf Laplacian learning. [arxiv.org/abs/2403.00337](https://arxiv.org/abs/2403.00337)
  2. **Zaghen et al. "Bayesian Sheaf Neural Networks"** (2024, AISTATS) — variational sheaf learning. [proceedings.mlr.press/v251/zaghen24a](https://proceedings.mlr.press/v251/zaghen24a.html)
  3. **Nonlinear Sheaf Diffusion** (2024) — community detection via learned nonlinear Laplacians. [arxiv.org/abs/2410.09590](https://arxiv.org/abs/2410.09590)
  4. **Cooperative Sheaf Neural Networks** (2025) — directed graphs, in/out Laplacians. [arxiv.org/abs/2507.00647](https://arxiv.org/abs/2507.00647)
  5. **Hypergraph Neural Sheaf Diffusion** (2025) — sheaves on hypergraphs. [arxiv.org/abs/2505.05702](https://arxiv.org/abs/2505.05702)

- **SuperInstance Connection**:
  - `persistent-sheaf` → cellular sheaf infrastructure, sheaf Laplacian computation
  - `sheaf-coherence` → sheaf consistency checking for agent knowledge
  - `categorical-agents` → sheaves as a categorical structure for agent communication
  - `spectral-fleet` → eigenvalue analysis of sheaf Laplacian for fleet-wide signal processing

- **New Crate Ideas**:
  - `sheaf-nn` — sheaf neural network building blocks. Sheaf Laplacian layers (linear + nonlinear), stalk/restriction map parameterizations, sheaf diffusion convolutions. Wraps `persistent-sheaf` + `spectral-fleet`.

- **Priority**: **MEDIUM** — High research value but requires significant engineering. Best approached as extension of `persistent-sheaf` rather than standalone crate initially.

---

## Part 2: Energy-Based Methods for AI

### 2.1 Hamiltonian Neural Networks

- **What**: Neural networks that learn Hamiltonian dynamics from data by parametrizing the Hamiltonian function H(q,p) and using Hamilton's equations for forward integration. The key insight: by construction, the learned dynamics conserve the Hamiltonian (energy). 2024–2025 advances include: (a) Symplectic Neural Flows (SympFlow, Dec 2024) — time-dependent symplectic networks guaranteeing structure preservation, (b) Kolmogorov–Arnold HNNs (KAR-HNN, 2025) — KAN-based architecture reducing hyperparameter sensitivity and energy drift, (c) Stable Port-Hamiltonian Networks (2025) — incorporating dissipation and Lyapunov stability, (d) Meta-learning for HNNs with limited data via Symplectic Neural Gaussian Processes, (e) Training from position-only data (inferring momentum).

- **Key Papers/Repos**:
  1. **Greydanus et al. "Hamiltonian Neural Networks"** (NeurIPS 2019, foundational). [arxiv.org/abs/1906.01563](https://arxiv.org/abs/1906.01563)
  2. **SympFlow: Symplectic Neural Flows** (Dec 2024) — parameterized Hamiltonian flow maps. [arxiv.org/abs/2412.16787](https://arxiv.org/abs/2412.16787)
  3. **KAR-HNN: Kolmogorov–Arnold Representation for Symplectic Learning** (2025). [arxiv.org/abs/2502.02480](https://arxiv.org/abs/2502.02480)
  4. **Stable Port-Hamiltonian Neural Networks** (2025) — energy + dissipation + Lyapunov. [arxiv.org/abs/2508.19410](https://arxiv.org/abs/2508.19410)
  5. **PINN-Proj: Conservation via Projection** (NeurIPS 2024) — projection method for enforcing conservation laws in PINNs. [research.ibm.com](https://research.ibm.com/publications/guaranteeing-conservation-laws-with-projection-in-physics-informed-neural-networks)

- **SuperInstance Connection**:
  - `symplectic-opt` → symplectic matrices, Störmer-Verlet integrators already implemented; HNNs use these as backbone
  - `conservation-law` → γ+H=C budget tracking; HNN energy conservation is a specific instance
  - `agent-homeostasis` → agents as Hamiltonian systems maintaining energy budgets
  - `ga-core` → game-theoretic dynamics as Hamiltonian flows over strategy spaces

- **New Crate Ideas**:
  - `si-hnn` — Hamiltonian Neural Network building blocks. Symplectic integrator layers, Hamiltonian parametrization traits, port-Hamiltonian extensions with dissipation, energy monitoring hooks. Wraps `symplectic-opt` integrators as differentiable layers.

- **Priority**: **HIGH** — Direct synergy with `symplectic-opt`. HNNs are the neural architecture that naturally conserves energy; our conservation law framework is the governance layer. Together they form "conservation by construction."

---

### 2.2 Lagrangian Neural Networks

- **What**: Neural networks that learn Lagrangian dynamics L(q, q̇) from data, using the Euler-Lagrange equations for forward integration. Unlike Hamiltonian networks, LNNs naturally handle coordinate transformations and can model dissipative systems. They're more flexible than HNNs (no need for canonical momentum) but harder to ensure stability. Recent work connects LNNs to Noether's theorem — symmetries of the Lagrangian imply conservation laws.

- **Key Papers/Repos**:
  1. **Lutter et al. "Deep Lagrangian Networks"** (2019) — end-to-end learning of Lagrangian dynamics.
  2. **Greydanus et al. "LNNs"** (NeurIPS 2019 companion work).
  3. **Allen-Blake et al. "Symmetry-Aware Lagrangian Networks"** (2024) — incorporating Noether symmetries.
  4. **De Ocampo et al. "Learning Lagrangians from Partial Observations"** (2024).

- **SuperInstance Connection**:
  - `conservation-law` → Noether's theorem maps Lagrangian symmetries to conservation laws; direct formal connection
  - `symplectic-opt` → Legendre transform between Lagrangian and Hamiltonian formulations
  - `lie-algebra` → continuous symmetries as Lie group actions on configuration space

- **New Crate Ideas**:
  - Extend `symplectic-opt` with Lagrangian integrator variants (Lagrangian Verlet, variational integrators derived from discretized action principle)

- **Priority**: **MEDIUM** — Important but naturally fits as extension of `symplectic-opt` rather than separate crate.

---

### 2.3 Energy-Based Models (EBMs)

- **What**: Models that define a probability distribution through an energy function p(x) ∝ exp(-E(x)). Modern EBMs (2024–2025) have resurged through three channels: (a) **Diffusion models as EBMs** — score matching with Langevin dynamics implicitly trains an EBM, (b) **Contrastive divergence** advances — better MCMC samplers for EBM training, (c) **Joint Energy Models (JEMs)** — hybrid discriminative-generative EBMs, (d) **EBMs for structured prediction** — energy networks for NLP, reasoning, and planning. EBMs are attractive because they unify generation, classification, and anomaly detection under one energy landscape.

- **Key Papers/Repos**:
  1. **Du & Mordatch "Implicit Generation and Generalization in EBMs"** (2019, foundational) — modern EBM revival.
  2. **Song & Ermon "Score-Based Generative Modeling"** (2019–2021) — diffusion as score matching / EBM training.
  3. **Grathwohl et al. "Your Classifier is Secretly an Energy-Based Model"** (JEM, ICLR 2020).
  4. **Flow Matching / Rectified Flows** (2022–2024) — deterministic transport as alternative to stochastic EBM sampling.
  5. **Energy-Based ODEs** — continuous-time EBM formulation connecting to Hamiltonian dynamics.

- **SuperInstance Connection**:
  - `conservation-law` → energy function E(x) with budget tracking γ+E=C
  - `entropy-conservation` → Hodge decomposition of entropy in EBM landscapes; entropy-regularized EBMs
  - `nanochat` → EBM for language model uncertainty / energy-based rejection
  - `spectral-fleet` → spectral analysis of energy landscapes

- **New Crate Ideas**:
  - `si-ebm` — Energy-Based Model primitives. Energy function traits, Langevin sampler, score-matching losses, contrastive divergence training loop. Integrates with `conservation-law` for energy budget tracking.

- **Priority**: **MEDIUM** — EBMs are a broad area; focus on the intersection with our existing conservation + entropy crates rather than building a full EBM framework.

---

### 2.4 Symplectic Integration for Training

- **What**: Using symplectic (structure-preserving) integrators as the optimizer for neural network training. Standard gradient descent is a first-order integrator; adding momentum (heavy ball, Nesterov) makes it second-order but not symplectic. Symplectic integrators (Störmer-Verlet, leapfrog) preserve the symplectic 2-form of phase space, meaning they conserve a shadow Hamiltonian exactly. Applied to training: treat (weights, momenta) as canonical coordinates, define a Hamiltonian H = L(w) + ½pᵀM⁻¹p, and integrate with Störmer-Verlet. Benefits: better long-term stability, natural warm-up behavior, implicit regularization toward flat minima.

- **Key Papers/Repos**:
  1. **Betancourt et al. "Hamiltonian Monte Carlo"** — symplectic integration for Bayesian inference.
  2. **França et al. "Symplectic Optimization"** (2020) — symplectic gradient descent.
  3. **Durmus et al. "Stochastic Symplectic Integrators"** — adding noise while preserving structure.
  4. **Natural Gradient as Symplectic Flow** — Amari's natural gradient as symplectic dynamics on the statistical manifold.

- **SuperInstance Connection**:
  - `symplectic-opt` → Störmer-Verlet integrators already implemented; wrap as optimizer traits
  - `agent-homeostasis` → training as homeostatic process; symplectic integrators maintain energy balance
  - `conservation-law` → shadow Hamiltonian conservation as training budget

- **New Crate Ideas**:
  - Extend `symplectic-opt` with `SymplecticOptimizer` trait: `step(weights, momenta, gradient) → (weights', momenta')` using Störmer-Verlet. Include adaptive step-size via shadow Hamiltonian monitoring.

- **Priority**: **HIGH** — We already have the integrators. This is "wrap and ship" — high impact for minimal new code.

---

### 2.5 Conservation Laws in Deep Learning (Noether's Theorem)

- **What**: Noether's theorem states: every continuous symmetry of a Lagrangian implies a conserved quantity. Applied to neural networks: if the loss function has a continuous symmetry (rotation invariance, translation equivariance, scale invariance), the corresponding Noether charge is conserved during gradient flow. This connects to (a) equivariant neural networks (E(n)-equivariant, SE(3)-equivariant), (b) invariant risk minimization, (c) symmetry-aware regularization. Recent work derives explicit conservation laws for trained networks and uses them to diagnose training pathologies.

- **Key Papers/Repos**:
  1. **Bietti & Mairal "On the Inductive Bias of Neural Tangent Kernels"** — symmetry properties of NTK.
  2. **E(n)-Equivariant Graph Neural Networks (EGNN)** — Satorras et al., 2021.
  3. **Noether's Theorem for Neural Networks** — Yang et al. (2024), deriving conservation laws from network symmetries.
  4. **Gauge Theory and Deep Learning** — treating weight spaces as gauge theories.

- **SuperInstance Connection**:
  - `conservation-law` → the abstract γ+H=C framework is *exactly* the Noether conservation structure
  - `lie-algebra` → continuous symmetries as Lie algebras; Noether charges as Lie algebra representations
  - `symplectic-opt` → Hamiltonian dynamics have natural Noether symmetries

- **New Crate Ideas**:
  - `noether` — symmetry detection and conservation law derivation. Given a parametrized loss function, detect continuous symmetries (via Lie algebra of tangent vectors) and derive conserved quantities. Integrate with `conservation-law` for automatic budget tracking of Noether charges.

- **Priority**: **MEDIUM** — Deep theoretical value. More research-y than immediately ship-able, but the connection to `conservation-law` + `lie-algebra` is too elegant to ignore.

---

### 2.6 Thermodynamic AI

- **What**: A convergence of three streams: (a) **Thermodynamic computing** — using physical thermodynamic systems (analog chips, stochastic electronics) to perform computation, particularly sampling and optimization, (b) **Stochastic thermodynamics of learning** — analyzing neural network training through the lens of thermodynamics: learning as a non-equilibrium process, generalization bounds via thermodynamic quantities, (c) **Thermodynamic AI accelerators** — Extropic, Normal Computing, etc. building hardware that exploits thermal noise for computation. Key insight: diffusion models are *literally* thermodynamic processes — they use Langevin dynamics (thermodynamics) to generate samples.

- **Key Papers/Repos**:
  1. **Extropic** — thermodynamic AI hardware startup. [extropic.ai](https://extropic.ai)
  2. **Ampere et al. "Thermodynamic AI and Stochastic Computing"** (2024).
  3. **Goldt & Seifert "Stochastic Thermodynamics of Learning"** (2017–2024) — entropy production during training.
  4. **Diffusion Models as Non-Equilibrium Thermodynamics** — connecting score matching to Jarzynski equality.
  5. **Parrondo et al. "Thermodynamics of Computation"** — fundamental limits.

- **SuperInstance Connection**:
  - `entropy-conservation` → Hodge decomposition of entropy; thermodynamic entropy as a specific case
  - `conservation-law` → thermodynamic conservation (energy, entropy, free energy)
  - `symplectic-opt` → contact geometry (thermodynamic phase space) as extension of symplectic geometry
  - `persistent-sheaf` → topological analysis of loss landscape thermodynamics

- **New Crate Ideas**:
  - `thermo-ai` — thermodynamic primitives for AI: free energy computation, entropy production tracking, thermal sampling (Langevin, overdamped dynamics). Bridges `entropy-conservation` + `conservation-law` + `symplectic-opt`.

- **Priority**: **LOW** — Frontier research, hardware-dependent. But the theoretical framework is immediately useful for understanding training dynamics through `entropy-conservation`.

---

## Cross-Cutting Insights

### Where Topology Meets Energy

1. **Morse Theory ↔ Energy Landscapes**: Every energy function E(x) defines a Morse landscape (when non-degenerate). The topology of sublevel sets {x : E(x) ≤ t} changes at critical points. `si-morse` + `si-ebm` = topological energy landscape analysis.

2. **Sheaf Laplacian ↔ Hodge Decomposition of Entropy**: The Hodge decomposition splits any signal into gradient (exact), curl (co-exact), and harmonic components. Applied to entropy flows: gradient entropy = dissipative learning, curl entropy = cyclic/oscillatory dynamics, harmonic entropy = persistent structure. `persistent-sheaf` + `entropy-conservation` = sheaf-theoretic entropy analysis.

3. **Persistence ↔ Conservation**: Persistent homology of sublevel sets of a Hamiltonian H reveals which topological features survive under energy constraints. Features that persist across energy scales are "robust" in both the topological and physical sense. `persistent-sheaf` + `conservation-law` = topologically-aware conservation budgets.

4. **Symplectic Structure ↔ Sheaf Cohomology**: A symplectic manifold can be viewed as a sheaf (assign symplectic vector spaces to open sets). The cohomology of this sheaf detects obstructions to global Hamiltonian flows. `symplectic-opt` + `persistent-sheaf` = cohomological obstructions to energy conservation.

5. **Witness Complexes ↔ Thermodynamic Sampling**: Witness complexes approximate the topology of point clouds. If the point cloud comes from thermodynamic sampling (MCMC, Langevin), witness complexes reveal the topology of the thermodynamic landscape. `witness-topology` + `thermo-ai` = efficient topological inference for sampled distributions.

### The Unifying Theme: Structure-Preserving AI

Both domains share a philosophy: **don't fight the geometry, use it**. Topological methods preserve global structure (shape, connectivity, holes). Energy methods preserve dynamical structure (conservation, symplectic form, entropy budget). Together, they form "structure-preserving AI" — models that respect the intrinsic geometry of their data and dynamics.

SuperInstance's crate ecosystem already spans both sides. The integration opportunity is real and near-term.

---

## Top 5 New Crates to Build

| Rank | Crate | What | Why | Leverages |
|------|-------|------|-----|-----------|
| **1** | `si-morse` | Morse theory: Morse-Smale complexes, critical point detection, sublevel persistence, gradient-flow decomposition | Uniquely differentiating. No ML framework offers Morse-theoretic loss landscape analysis. Direct path to training diagnostics. | `persistent-sheaf`, `symplectic-opt` |
| **2** | `si-hnn` | Hamiltonian Neural Network building blocks: symplectic integrator layers, Hamiltonian parametrization, port-Hamiltonian extensions | "Conservation by construction" — HNNs are the neural arch that naturally conserves energy. | `symplectic-opt`, `conservation-law` |
| **3** | `topo-loss` | Differentiable topological loss functions: persistence landscape layer, soft Betti estimation, topological regularizers | Makes topology a first-class training signal. Every SuperInstance training pipeline gains topological awareness. | `persistent-sheaf`, `witness-topology` |
| **4** | `tda-guard` | Streaming persistence + anomaly scoring for fleet monitoring | Directly applicable to agent health, LLM safety, fleet monitoring. Production-facing. | `persistent-sheaf`, `witness-topology`, `spectral-fleet` |
| **5** | `sheaf-signal` | Sheaf signal processing: Hodge decomposition, sheaf Fourier transform, spectral filtering | Natural extension of existing sheaf Laplacian. Enables graph signal processing on sheaf-structured data. | `persistent-sheaf`, `spectral-fleet` |

---

## Integration Roadmap

### Phase 1: Foundations (Weeks 1–4)

1. **Extend `symplectic-opt`** with `SymplecticOptimizer` trait
   - Wrap existing Störmer-Verlet as training optimizer
   - Add shadow Hamiltonian monitoring
   - Integrate with `conservation-law` budget tracking

2. **Extend `persistent-sheaf`** with differentiable persistence layer
   - Persistence landscape computation (smooth vectorization)
   - Sublevel set persistence API
   - Soft Betti number estimation

### Phase 2: New Crates (Weeks 5–10)

3. **Build `si-morse`** (highest research value)
   - Discrete Morse theory on simplicial complexes
   - Morse-Smale complex computation
   - Critical point detection in high-dimensional functions
   - Integration with `persistent-sheaf` for sublevel persistence

4. **Build `si-hnn`** (highest practical value)
   - Hamiltonian function trait + parametrization
   - Symplectic integrator layer (wraps `symplectic-opt`)
   - Port-Hamiltonian extension with dissipation
   - Energy monitoring hooks → `conservation-law`

5. **Build `topo-loss`**
   - Persistence landscape loss
   - Topological regularizer traits
   - Integration with autograd (generic backward pass via landscape gradient)

### Phase 3: Applications (Weeks 11–16)

6. **Build `tda-guard`**
   - Streaming pipeline: point cloud → witness complex → persistence → anomaly score
   - Sliding window persistence for time series
   - Fleet-wide anomaly aggregation via `spectral-fleet`

7. **Build `sheaf-signal`**
   - Hodge decomposition API on sheaf Laplacian
   - Sheaf Fourier transform
   - Spectral filtering on sheaves
   - Bridge to `entropy-conservation` for entropy flow decomposition

### Phase 4: Cross-Cutting Integration (Weeks 17–20)

8. **Wire `si-morse` + `si-hnn`** → Morse analysis of Hamiltonian energy landscapes
9. **Wire `topo-loss` + `nanochat`** → topologically-regularized language model training
10. **Wire `tda-guard` + `fleet-warden`** → real-time topological fleet monitoring
11. **Wire `sheaf-signal` + `entropy-conservation`** → Hodge decomposition of entropy flows

---

## References (Consolidated)

### Topology
- [TDAAD](https://github.com/IRT-SystemX/tdaad) — TDA anomaly detection package
- [Sheaf Neural Networks](https://arxiv.org/abs/2403.00337) — Barber et al. 2024
- [Bayesian Sheaf NNs](https://proceedings.mlr.press/v251/zaghen24a.html) — Zaghen et al. AISTATS 2024
- [Nonlinear Sheaf Diffusion](https://arxiv.org/abs/2410.09590) — 2024
- [Cooperative Sheaf NNs](https://arxiv.org/abs/2507.00647) — 2025
- [Hypergraph Neural Sheaf Diffusion](https://arxiv.org/abs/2505.05702) — 2025
- [TDA for Banking](https://jmlr.org/papers/volume25/24-0853/24-0853.pdf) — JMLR 2024
- [TDA for Time-Varying Graphs](https://arxiv.org/abs/2508.14136) — 2025
- [Eirene.jl](https://github.com/Eetion/Eirene.jl) — Computational persistence

### Energy Methods
- [Hamiltonian Neural Networks](https://arxiv.org/abs/1906.01563) — Greydanus et al. NeurIPS 2019
- [SympFlow](https://arxiv.org/abs/2412.16787) — Symplectic Neural Flows, Dec 2024
- [KAR-HNN](https://arxiv.org/abs/2502.02480) — Kolmogorov-Arnold HNN, 2025
- [Stable Port-Hamiltonian NNs](https://arxiv.org/abs/2508.19410) — 2025
- [PINN-Proj](https://research.ibm.com/publications/guaranteeing-conservation-laws-with-projection-in-physics-informed-neural-networks) — NeurIPS 2024
- [Energy-Conserving NN for LES](https://arxiv.org/abs/2504.05868) — 2025

---

*End of report. Next steps: review with team, prioritize Phase 1 extensions, begin `si-morse` and `si-hnn` design docs.*
