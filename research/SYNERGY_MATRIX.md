# SuperInstance Synergy Matrix — Cutting-Edge Math × AI

**Research Date:** 2025-06-07  
**Scope:** 2024–2026 papers, repos, and emerging ideas  
**Purpose:** Map the frontier of mathematical AI to our crate ecosystem

---

## Executive Summary

The most explosive synergies lie at the intersection of **sheaf theory + graph learning**, **tropical geometry + ReLU network theory**, and **Hamiltonian/Lagrangian neural networks + conservation laws** — all areas where SuperInstance already has production crates. The emerging field of **Geometric Algebra Transformers (GATr)** directly validates our `ga-core` investment, while **Kolmogorov-Arnold Networks** represent the highest-value new crate opportunity. Cross-cutting themes reveal that *structure-preserving learning* — building networks that inherently respect geometric, algebraic, and physical constraints — is the dominant paradigm shift of 2024–2026, and SuperInstance's mathematical stack is uniquely positioned to capture it.

---

## Findings

### 1. Tropical Geometry in Deep Learning

- **What**: Tropical geometry has matured from a theoretical lens into a practical toolkit for understanding and compressing ReLU networks. ReLU networks are mathematically equivalent to tropical rational maps, meaning their decision boundaries are tropical hypersurfaces. In 2024–2025, this equivalence has been exploited for: (a) tropical polynomial division algorithms that compress networks by eliminating redundant neurons, (b) novel tropical-derived activation functions that replace ReLU while maintaining piecewise linearity, and (c) tropical polynomial regression as a network training alternative. The ICASSP 2024 tutorial and AMS January 2025 special session signal mainstream recognition.

- **Key Papers/Repos**:
  - Zhang et al., "Tropical Polynomials as a Replacement for ReLU" — AMS JMM 2025 (arXiv:2502.01247)
  - "Real Tropical Geometry of Neural Networks" (arXiv:2403.11871)
  - "Tropical Polynomial Regression" — alternating minimization for tropical rational functions (arXiv:2405.20174)
  - "Tropical Activations and Network Structure" — training GPT-2 and ConvNeXt with tropical activations (ICML 2025)
  - Maragos et al., ICASSP 2024 Tutorial on Tropical Algebra, Geometry, and ML (NTUA)

- **SuperInstance Connection**: `tropical-geometry` provides the semiring algebra foundation; `tropical-harmony` implements tropical neural network primitives. The tropical polynomial division work maps directly to a network compression module. Our `conservation-law` crate could integrate tropical conservation of linear regions as a regularizer.

- **New Crate Ideas**:
  - `tropical-compress` — Tropical polynomial division for neural network compression (neuron pruning, parameter reduction)
  - `tropical-activations` — Tropical-derived activation functions as drop-in replacements for ReLU/SiLU

- **Priority**: **HIGH** — Tropical geometry is now the rigorous mathematical explanation for why ReLU networks work. This directly strengthens our core differentiator.

- **Estimated Effort**: 2–4 weeks for `tropical-compress` (division algorithms + network pruning pipeline); 1–2 weeks for `tropical-activations`.

---

### 2. Sheaf Neural Networks

- **What**: Sheaf neural networks (SNNs) have become one of the hottest topics in graph ML (2024–2025). They extend GNNs by attaching vector spaces to nodes and "restriction maps" to edges, controlling how information flows. This solves the over-smoothing problem (nodes becoming indistinguishable after many layers) and dramatically improves performance on heterophilous graphs (where neighbors have different labels). Key advances include: Nonlinear Sheaf Diffusion (NLSD), Directed Sheaf Neural Networks (DSNNs) with complex-valued restriction maps, Bayesian Sheaf Neural Networks (BSNNs) for uncertainty quantification, Cooperative Sheaf Neural Networks (CSNNs) for directed graphs, and Deep Neural Sheaf Diffusion (DNSD) for graph foundation models.

- **Key Papers/Repos**:
  - Hansen & Gebhart, "Sheaf Neural Networks" (NeurIPS 2020, foundational)
  - "Nonlinear Sheaf Diffusion" — AAAI 2025 (arXiv:2410.09590)
  - "Cooperative Sheaf Neural Networks" — ICML 2024 (proceedings.mlr.press/v251/zaghen24a)
  - "Bayesian Sheaf Neural Networks" — variational sheaf learning (OpenReview 2025)
  - "Directed Sheaf Neural Networks" — complex-valued restriction maps (arXiv:2507.00647)
  - "Sheaf4Rec" — sheaf-based recommendation systems (2025)

- **SuperInstance Connection**: `persistent-sheaf` implements sheaf cohomology and the sheaf Laplacian; `sheaf-coherence` provides sheaf-theoretic consistency checking. The sheaf Laplacian is the core primitive of SNNs — we already have it. Restriction map learning is a natural extension.

- **New Crate Ideas**:
  - `sheaf-gnn` — Sheaf Neural Network layer implementations (sheaf diffusion, restriction map learning, NLSD)
  - `sheaf-bayesian` — Bayesian treatment of sheaf structure with uncertainty quantification

- **Priority**: **HIGH** — Sheaf GNNs are a direct extension of our existing sheaf infrastructure into one of the fastest-moving areas of graph ML.

- **Estimated Effort**: 4–6 weeks for `sheaf-gnn` (core diffusion layers + restriction map learning + benchmarking on heterophilous datasets); 3–4 weeks for `sheaf-bayesian`.

---

### 3. Category Theory in ML

- **What**: Category theory is emerging as the foundational language for compositional AI systems. A comprehensive August 2024 survey (updated Feb 2025) maps categorical approaches to four pillars: gradient-based learning, probability-based learning, invariance/equivalence learning, and topos-based learning. Key developments include: Markov categories for categorical probability (diagrammatic treatment of independence, conditioning, and information flow), "Categorical Deep Learning" position papers proposing algebraic theories of neural architectures, "deep functors" for transfer learning, and major institutional investment (Topos UK + Glaive lab funded by UK's ARIA for category-theory-based AI verification). The ICERM September 2025 workshop and "AI Meets Algebra" tutorial signal field-wide recognition.

- **Key Papers/Repos**:
  - "Category Theory-Derived Machine Learning" survey (arXiv:2408.14014, Feb 2025 update)
  - "Categorical Deep Learning: An Algebraic Theory of Architectures" (2024–2025 position paper)
  - "Categorical Probability Distributions as Neural Network Outputs" — ICML 2024
  - "Deep Functor" — functors for transfer learning (becominghuman.ai, 2024)
  - "Categories for AI" lecture series (cats.for.ai)
  - ICERM Workshop "Category Theory, Combinatorics, and ML" (September 2025)

- **SuperInstance Connection**: `categorical-agents` already implements functors, monoidal categories, and composition algebra. The Markov category framework maps directly to our existing categorical infrastructure. Categorical probability could extend `dial-theory`'s information geometry with diagrammatic reasoning.

- **New Crate Ideas**:
  - `categorical-probability` — Markov categories, diagrammatic probability, conditional independence via string diagrams
  - `categorical-dl` — Algebraic theory of neural architectures (compositional construction of architectures from categorical building blocks)

- **Priority**: **MEDIUM** — High intellectual value and strong fit, but category theory in ML is still more foundational than immediately deployable. Best positioned as a 6-month strategic investment.

- **Estimated Effort**: 6–8 weeks for `categorical-probability`; 8–12 weeks for `categorical-dl`.

---

### 4. Kolmogorov-Arnold Networks (KANs)

- **What**: KANs, introduced by Liu et al. (April 2024, accepted ICLR 2025), replace fixed activation functions on nodes with learnable B-spline activation functions on edges. Instead of the MLP paradigm (linear transformation → fixed activation), KANs learn univariate functions parameterized by B-splines on each edge. This yields superior function approximation (Kolmogorov-Arnold representation theorem), built-in interpretability (splines are visualizable), and natural compatibility with physics-informed models. An explosion of follow-ups includes Graph KANs (GKAN), Physics-Informed KANs, Chebyshev KANs, Wavelet KANs, KANs for quantum architecture search, and hybrid B-spline/neural operators. The mathematical generalization paper (Sept 2025) unifies KAN variants under a common framework.

- **Key Papers/Repos**:
  - Liu et al., "KAN: Kolmogorov-Arnold Networks" (arXiv:2404.19756, ICLR 2025)
  - "GKAN: Graph Kolmogorov-Arnold Networks" (2024)
  - "Physics-Informed Deep B-Spline Networks" (TMLR 2026, arXiv Oct 2025)
  - "Mathematical Generalization of KANs and Their Variants" (arXiv Sept 2025)
  - "KANQAS: KAN for Quantum Architecture Search" (2024)
  - "Kolmogorov-Arnold Networks Still Catastrophically Forget but Differently" — AAAI 2025

- **SuperInstance Connection**: KANs have no direct existing crate but connect deeply to multiple: `tropical-geometry` (tropical splines as activation functions), `optimal-transport` (B-spline parameterized transport maps), `symplectic-opt` (physics-informed KANs use Hamiltonian structure), and `dial-theory` (statistical manifold of spline parameters).

- **New Crate Ideas**:
  - `si-kan` — Core KAN implementation: B-spline edge activations, KAN layers, efficient forward/backward passes
  - `kan-physics` — Physics-informed KANs leveraging our symplectic and conservation-law infrastructure
  - `tropical-kan` — Tropical spline activations for KAN (combining tropical-geometry + KAN)

- **Priority**: **HIGH** — KANs are the most impactful new architecture since Transformers for structured domains. A Rust KAN crate would be first-mover advantage.

- **Estimated Effort**: 4–6 weeks for `si-kan` core; 3–4 weeks for `kan-physics`; 2–3 weeks for `tropical-kan`.

---

### 5. State Space Models (Mamba/Mamba-2)

- **What**: Mamba introduced selective state space models with input-dependent parameterization and hardware-aware parallel algorithms, achieving linear-time sequence processing that rivals Transformers. Mamba-2 (May 2024) established the Structured State Space Duality (SSD) framework, proving a theoretical connection between SSMs and attention mechanisms, enabling 2–8× faster training and state dimensions up to 256. Hybrid architectures (Jamba = Mamba + Transformer blocks) are gaining traction. The mathematical structure is deeply Hamiltonian: SSMs discretize continuous-time linear systems via zero-order hold or bilinear transforms, and the state transition matrix must remain stable (eigenvalue constraints). Mamba-3 (2025) explores complex-valued updates and MIMO formulations. Edge deployments (eMamba, LightMamba, Mamba-X) optimize for resource-constrained hardware.

- **Key Papers/Repos**:
  - Gu & Dao, "Mamba: Linear-Time Sequence Modeling with Selective State Spaces" (2023, widely cited 2024)
  - Gu & Dao, "Mamba-2: Structured State Space Duality" (arXiv May 2024)
  - "Jamba: AI21's Hybrid Mamba-Transformer" (March 2024)
  - state-spaces/mamba — official repo (github.com/state-spaces/mamba)
  - "eMamba" — edge deployment framework (2025)
  - "LightMamba" — FPGA quantized Mamba (2025)

- **SuperInstance Connection**: `symplectic-opt` implements Hamiltonian systems and symplectic integrators — the SSM state transition is a discretized Hamiltonian flow. Our `spectral-fleet` eigenvalue tools apply to SSM stability analysis (transition matrix eigenvalues must stay within unit circle). The bilinear transform used in SSM discretization is a Möbius transformation connectable to `ga-core` conformal geometry.

- **New Crate Ideas**:
  - `si-ssm` — State space model primitives with symplectic discretization guarantees, eigenvalue stability enforcement
  - `symplectic-mamba` — Mamba-style architecture built on our symplectic integrators

- **Priority**: **MEDIUM** — SSMs are hot but the space is crowded with well-funded implementations. Our edge is the mathematical rigor (symplectic guarantees, spectral stability).

- **Estimated Effort**: 6–8 weeks for `si-ssm`; 8–12 weeks for `symplectic-mamba` (full Mamba architecture).

---

### 6. Liquid Neural Networks

- **What**: Liquid Neural Networks (LNNs) are continuous-time recurrent networks where neural states evolve via ODEs with input-dependent time constants. Each neuron's dynamics are governed by differential equations where the time constant is itself a function of the input, creating adaptive temporal behavior. Closed-form Continuous-time (CfC) networks provide efficient closed-form solutions avoiding expensive ODE solvers. Liquid AI (MIT spinoff, October 2024) launched production models emphasizing parameter efficiency (orders of magnitude fewer parameters than Transformers), interpretability, and robustness to distribution shift. Applications span time-series, autonomous vehicles, telecom, and embedded AI. Memory-augmented CfC networks (2025) extend temporal modeling capability.

- **Key Papers/Repos**:
  - Hasani et al., "Liquid Time-Constant Networks" (AAAI 2021, foundational)
  - Hasani et al., "Closed-form Continuous-time Neural Networks" (NeurIPS 2021)
  - "Liquid Neural Networks: Next-Generation AI for Telecom" (April 2025)
  - "Memory-Augmented Closed-form Continuous-time Networks" (2025)
  - Liquid AI model launch (October 2024) — liquid.ai

- **SuperInstance Connection**: `conservation-law` implements continuous-time dynamics with conservation guarantees (γ+H=C). Liquid networks' ODE-based evolution is a direct application domain. Our `symplectic-opt` integrators can replace the ODE solvers in LNNs with structure-preserving alternatives. `entropy-conservation` provides the thermodynamic framework for LNN energy budgets.

- **New Crate Ideas**:
  - `liquid-instance` — Liquid neural network layer built on our conservation-law + symplectic integrator infrastructure
  - `conservation-ode` — Conservation-law-preserving ODE solver layer for continuous-time networks

- **Priority**: **MEDIUM** — Strong conceptual fit but LNNs haven't yet achieved Transformer-scale results. Strategic bet on edge/efficiency trajectory.

- **Estimated Effort**: 4–6 weeks for `liquid-instance`; 2–3 weeks for `conservation-ode`.

---

### 7. Information Geometry for Optimization

- **What**: Information geometry applies Riemannian geometry to the space of probability distributions, using the Fisher information matrix as a metric tensor. Natural gradient descent follows the steepest direction in this curved parameter space, converging faster than Euclidean gradient methods. Recent work extends this to: Riemannian optimization on general manifolds (Stiefel, Grassmannian), mirror descent connections, natural gradient methods for large models via Kronecker-factored approximate curvature (K-FAC), and information-geometric approaches to variational inference. The interplay with optimal transport (Wasserstein natural gradient) is a key 2024–2025 theme.

- **Key Papers/Repos** (based on field knowledge — search rate-limited):
  - Amari & Nagaoka, "Methods of Information Geometry" (foundational)
  - "Natural Gradient Descent for Large Models" — K-FAC and extensions (2024)
  - "Wasserstein Natural Gradient" — connecting optimal transport + information geometry (2024)
  - "Riemannian Optimization on Neural Network Parameter Spaces" (2024–2025)
  - Khan & Rue, "The Bayesian Learning Rule" — unifying perspective connecting natural gradient to Bayesian inference

- **SuperInstance Connection**: `dial-theory` implements statistical manifolds. `optimal-transport` provides Wasserstein distances. The Fisher-Rao metric and Wasserstein distance are dual perspectives on the geometry of distributions. Extending `dial-theory` with natural gradient computation and connecting it to `wasserstein-agents` would create a unified information-geometric optimization framework.

- **New Crate Ideas**:
  - `natural-gradient` — Fisher information computation, K-FAC approximations, natural gradient descent for model training
  - `info-geometry-bridge` — Unified Fisher-Rao + Wasserstein geometry (connecting dial-theory + optimal-transport)

- **Priority**: **MEDIUM** — Theoretical depth is immense and the fit is perfect, but practical demand is more niche. Best as an extension to existing crates.

- **Estimated Effort**: 4–6 weeks for `natural-gradient`; 3–4 weeks for the bridge integration.

---

### 8. Topological Deep Learning

- **What**: Topological Deep Learning (TDL) has matured from using persistent homology as a feature extractor to integrating topology throughout the learning pipeline. Key 2024–2025 advances include: topological loss functions that enforce Betti number constraints during training (especially for medical image segmentation), Multi-Cellular Networks (MCN/SMCN) that overcome expressivity limitations of standard TDL architectures, persistent topological Laplacians and Dirac operators providing spectral representations beyond simple Betti numbers, a unified spectral-persistent homology framework with "Topological Drift" metrics, and the ICML 2024 Topological Deep Learning Challenge. TDA for model selection (using topology of loss landscapes) is an emerging practice. Cell complexes, path complexes, and hypergraphs extend TDL beyond graphs.

- **Key Papers/Repos**:
  - "Topological Data Analysis and TDL Beyond Persistent Homology — A Review" (July 2025)
  - "A Persistent Homology-Based Topological Loss for Image Segmentation" (2024)
  - "Unified Spectral-Persistent Homology Framework for Stable TDL" (Nov 2025)
  - "Multi-Cellular Networks" — overcoming topological blind spots (2025)
  - ICML Topological Deep Learning Challenge 2024 (pyt-team.github.io)
  - GUDHI, TopoX software libraries

- **SuperInstance Connection**: `persistent-sheaf` implements persistent homology with sheaf-theoretic extensions. `witness-topology` and `room-topology` provide TDA primitives. The persistent topological Laplacian is a natural extension of our sheaf Laplacian. Topological loss functions integrate with our Hodge decomposition (`hodge-consensus`).

- **New Crate Ideas**:
  - `topo-loss` — Differentiable topological loss functions (Betti number constraints, persistence diagram distances)
  - `persistent-laplacian` — Persistent topological Laplacians and Dirac operators beyond standard persistent homology
  - `topo-model-select` — Topology of loss landscapes for model selection and hyperparameter tuning

- **Priority**: **HIGH** — TDL is rapidly moving from academic curiosity to practical tooling, and we have all the mathematical prerequisites.

- **Estimated Effort**: 3–4 weeks for `topo-loss`; 4–6 weeks for `persistent-laplacian`; 2–3 weeks for `topo-model-select`.

---

### 9. Geometric Algebra in Physics Simulation

- **What**: Geometric Algebra has had a breakthrough year in robotics and simulation. The GAFRO library (C++/Python/ROS, 2024–2025) applies Conformal GA to robot kinematics and dynamics. The Geometric Algebra Transformer (GATr) and Projective GA Transformer (P-GATr) process geometric data using multivector representations with built-in E(3)-equivariance. P-GATr is being integrated into diffusion policies for robot manipulation. GA is unifying screw theory, Lie algebra, and dual quaternions into a single framework for 6D pose, constraint, and motion representation. AGACSE 2024 and RAGA 2025 conferences signal growing industrial adoption.

- **Key Papers/Repos**:
  - "GAFRO: Geometric Algebra for Robotics" — IEEE RAM 2025
  - "Geometric Algebra Transformers" (GATr) — ICML 2024 (proceedings.mlr.press/v238/haan24a)
  - "P-GATr: Projective GA Transformer" (2024–2025)
  - "PGA in Robotics and Control" — biquaternion isomorphism for screw theory (2024)
  - AGACSE 2024 conference proceedings (University of Amsterdam)
  - Calinon, "Geometric Algebra for Robotics" — Annual Review 2026 (preprint)

- **SuperInstance Connection**: `ga-core` implements Cl(3,1) conformal GA with rotors and multivectors. This is the exact algebraic foundation used by GAFRO and GATr. Our existing multivector operations and rotor infrastructure map directly to the primitives needed for GA-based robotics and simulation.

- **New Crate Ideas**:
  - `ga-robotics` — GAFRO-style kinematics and dynamics using ga-core (forward/inverse kinematics, Jacobians, dynamics)
  - `ga-transformer` — Geometric Algebra Transformer layer using multivector attention
  - `pga-core` — Projective Geometric Algebra (PGA) as complementary to our conformal GA

- **Priority**: **HIGH** — GA Transformers are the most direct "productization" path for our ga-core crate. Robotics is a massive market with clear mathematical fit.

- **Estimated Effort**: 6–8 weeks for `ga-robotics`; 6–8 weeks for `ga-transformer`; 3–4 weeks for `pga-core`.

---

### 10. Energy-Based Models & Conservation

- **What**: Energy-conserving neural networks have matured from a niche idea to a design principle. Stable Port-Hamiltonian Neural Networks (NeurIPS 2025) integrate energy conservation, dissipation, and Lyapunov stability into a single learnable architecture. Hamiltonian Neural PDE Solvers extend HNNs to partial differential equations with learnable kernel integrals. Lagrangian Flow Networks (ICLR 2024) model fluid dynamics while inherently satisfying the continuity equation. PINN-Proj guarantees conservation law adherence via projection methods. Structure-Preserving ML (SpML) provides model reduction that respects Hamiltonian/Lagrangian structure. An energy-conserving architecture for turbulence closure (April 2025) uses skew-symmetric design to preserve physical conservation laws.

- **Key Papers/Repos**:
  - "Stable Port-Hamiltonian Neural Networks" — NeurIPS 2025
  - "Hamiltonian Neural PDE Solvers through Functional Approximation" (Sept 2025)
  - "Lagrangian Flow Networks" — ICLR 2024
  - "PINN-Proj: Guaranteeing Conservation Laws with Projection" — NeurIPS 2024 Workshop
  - "Structure-Preserving ML for Model Reduction" (Feb 2024, SIAM)
  - "Energy-Conserving Neural Network Closure Model for LES" (April 2025)

- **SuperInstance Connection**: `conservation-law` (γ+H=C) is the exact framework these papers implement. `symplectic-opt` provides the symplectic integrators needed for HNNs. `entropy-conservation` handles the thermodynamic conservation side. Port-Hamiltonian networks are a natural extension of our conservation-law crate. Lagrangian Flow Networks connect to `optimal-transport` (fluid flows as transport maps).

- **New Crate Ideas**:
  - `port-hamiltonian` — Port-Hamiltonian neural network layers with guaranteed stability and energy conservation
  - `lagrangian-flow` — Lagrangian Flow Networks for density/velocity modeling with mass conservation
  - `structure-preserving` — General structure-preserving ML primitives (symplectic autoencoders, Poisson-preserving networks)

- **Priority**: **HIGH** — This is our *core thesis*. Conservation laws in AI are moving from theory to production. Every paper in this domain validates our architecture.

- **Estimated Effort**: 4–6 weeks for `port-hamiltonian`; 3–4 weeks for `lagrangian-flow`; 4–6 weeks for `structure-preserving`.

---

## Cross-Cutting Themes

### Theme 1: Structure-Preserving Learning
The dominant meta-trend across ALL 10 domains: building neural networks that *inherently respect* geometric, algebraic, physical, and topological constraints rather than hoping to learn them from data. This manifests as:
- Conservation laws preserved by architecture (Domains 10, 6)
- Equivariance built into representations (Domains 9, 2)
- Algebraic structure baked into computations (Domains 1, 3, 7)
- Topological invariants enforced during training (Domain 8)
- Smooth approximation structure guaranteed by construction (Domains 4, 5)

**Implication**: SuperInstance's entire crate ecosystem serves this single meta-trend. Positioning should emphasize "structure-preserving AI infrastructure."

### Theme 2: Sheaf-Theoretic Unification
Sheaf theory appears in: sheaf GNNs (Domain 2), topological DL via sheaf cohomology (Domain 8), categorical structure via sheaf-valued functors (Domain 3), and information geometry via parametric sheaves (Domain 7). Sheaves are emerging as the *universal glue* between geometry, topology, and data.

### Theme 3: Hamiltonian/Symplectic Structure Everywhere
Hamiltonian dynamics underpin: SSMs (Domain 5), liquid networks (Domain 6), energy-conserving networks (Domain 10), and symplectic optimization (Domain 7). The discrete-time↔continuous-time bridge (via symplectic integrators) is the enabling technology.

### Theme 4: Tropical + Algebraic Geometry as Network Theory
Tropical geometry explains ReLU networks (Domain 1). KANs use spline algebra (Domain 4). Both point to algebraic geometry as the correct language for understanding what neural networks compute — and `tropical-geometry` sits at the center.

### Theme 5: The Convergence of Continuous and Discrete
Liquid networks (continuous ODEs), SSMs (discretized continuous systems), KANs (continuous spline functions), and Hamiltonian networks (continuous physics) all blur the line between continuous mathematics and discrete computation. Our `symplectic-opt` (discretization) and `conservation-law` (continuous invariants) crates are the bridge.

---

## Recommended Next 5 Crates to Build

| Rank | Crate | Rationale | Impact | Effort |
|------|-------|-----------|--------|--------|
| 1 | **`si-kan`** | First-mover Rust KAN; connects to 4+ existing crates; KANs are the hot architecture | ★★★★★ | 4–6 wk |
| 2 | **`sheaf-gnn`** | Direct extension of existing sheaf crates into the fastest-growing GNN paradigm | ★★★★☆ | 4–6 wk |
| 3 | **`ga-transformer`** | Productizes ga-core into a deployable architecture; robotics market is massive | ★★★★☆ | 6–8 wk |
| 4 | **`port-hamiltonian`** | Core thesis validation; conservation-law networks going to production (NeurIPS 2025) | ★★★★☆ | 4–6 wk |
| 5 | **`topo-loss`** | Low effort, high utility; differentiable topological losses for any training pipeline | ★★★☆☆ | 3–4 wk |

---

## Integration Opportunities

### Existing Crates to Extend

| Crate | Extension | Connection |
|-------|-----------|------------|
| `tropical-geometry` | Add tropical polynomial division + network compression | Domain 1 |
| `tropical-harmony` | Add tropical activation functions | Domains 1, 4 |
| `persistent-sheaf` | Add sheaf Laplacian → SNN layer; add persistent topological Laplacian | Domains 2, 8 |
| `sheaf-coherence` | Add restriction map learning for SNNs | Domain 2 |
| `ga-core` | Add PGA subalgebra; add multivector attention mechanism | Domain 9 |
| `conservation-law` | Add Port-Hamiltonian layer type | Domain 10 |
| `symplectic-opt` | Add SSM discretization mode; add structure-preserving autoencoder | Domains 5, 10 |
| `dial-theory` | Add Fisher information metric + natural gradient computation | Domain 7 |
| `hodge-consensus` | Integrate topological losses via Hodge decomposition | Domain 8 |
| `spectral-fleet` | Add SSM eigenvalue stability analysis mode | Domain 5 |

---

## Appendix: Conference & Community Signals

| Signal | Date | Relevance |
|--------|------|-----------|
| ICASSP 2024 Tutorial: Tropical Algebra & ML | Mar 2024 | Domain 1 |
| KAN paper accepted ICLR 2025 | Apr 2024 | Domain 4 |
| Jamba (Mamba+Transformer) released | Mar 2024 | Domain 5 |
| Mamba-2 (SSD framework) | May 2024 | Domain 5 |
| AGACSE 2024 (GA conference) | 2024 | Domain 9 |
| NeurIPS 2024 Workshop: PINN-Proj | Dec 2024 | Domain 10 |
| AMS JMM 2025: Tropical Polynomials for ReLU | Jan 2025 | Domain 1 |
| Liquid AI production models launch | Oct 2024 | Domain 6 |
| ICERM Workshop: Category Theory & ML | Sep 2025 | Domain 3 |
| GTML 2025 Workshop | Nov 2025 | Domain 8 |
| RAGA 2025 (Applied GA) | 2025 | Domain 9 |
| Stable Port-HNN at NeurIPS | 2025 | Domain 10 |

---

*This document is a living research artifact. Re-scan quarterly as these fields move fast.*
