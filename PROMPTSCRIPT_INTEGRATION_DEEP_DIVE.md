# PromptScript × SuperInstance: Deep Integration Specification

> "The .prs file is the interface. The Rust crate is the implementation. The agent is the emergent behavior."

**Status:** Draft v1.0 — Technical Architecture Document  
**Date:** 2026-06-07  
**Author:** SuperInstance Core Engineering  
**Classification:** Internal — Core Team  
**Companion:** [AGI_CONVERGENCE_ROADMAP.md](./AGI_CONVERGENCE_ROADMAP.md)

---

## Table of Contents

1. [PromptScript Architecture Analysis](#section-1-promptscript-architecture-analysis)
2. [SuperInstance Integration Points](#section-2-superinstance-integration-points)
3. [The Killer App — "Open Mind"](#section-3-the-killer-app--open-mind)
4. [Implementation Roadmap](#section-4-implementation-roadmap)

---

## Section 1: PromptScript Architecture Analysis

### 1.1 Monorepo Structure

PromptScript is organized as a TypeScript monorepo under `packages/` with eleven packages forming a complete compilation pipeline:

```
packages/
├── core/          # Types (AST, SourceLocation, SkillDefinition), errors, utils
├── parser/        # Lexer → Grammar → AST (grammar/visitor.ts, lexer/lexer.ts, parse.ts)
├── compiler/      # Pipeline orchestrator: resolve → validate → format
├── formatters/    # 38 agent-specific output formatters
├── resolver/      # Inheritance (@inherit), imports (@use), extensions (@extend), skill composition
├── validator/     # 16+ validation rules, security presets, reference integrity
├── server/        # File watcher + HTTP compilation server
├── playground/    # Browser-based interactive editor
├── cli/           # Command-line interface
├── importer/      # Reverse-import from existing agent configs into .prs
└── browser-compiler/  # WASM-ready compiler for in-browser compilation
```

Each package exports a clean public API from `src/index.ts`, uses Vite for building, and has comprehensive test suites under `src/__tests__/`.

### 1.2 The Compiler Pipeline

The compilation pipeline is defined in `packages/compiler/src/compiler.ts` and follows three explicit stages:

#### Stage 1: Resolve

```typescript
// packages/compiler/src/compiler.ts, line ~155
resolved = await this.resolver.resolve(entryPath);
```

The `Resolver` (from `@promptscript/resolver`) takes an entry `.prs` file and:

1. **Loads and parses** the file using `@promptscript/parser`
2. **Resolves `@inherit` declarations** — loads the parent file, deep-merges blocks (child wins on conflict, text content is concatenated). This is implemented in `packages/resolver/src/inheritance.ts` using `deepMerge` from core.
3. **Resolves `@use` declarations** — imports skill fragments, optionally with template parameters and aliases. Implemented in `packages/resolver/src/imports.ts`.
4. **Resolves `@extend` blocks** — applies targeted modifications to existing blocks. Implemented in `packages/resolver/src/extensions.ts`.
5. **Resolves inline `@use` within `@skills`** — skill composition via `packages/resolver/src/skill-composition.ts`, which loads sub-skills as numbered phases with cycle detection (max depth 3, max content 256KB).
6. **Resolves guard `requires`** — `packages/resolver/src/guard-requires.ts` handles `requires:` dependencies in guard blocks.
7. **Auto-discovers native content** — `packages/resolver/src/auto-discovery.ts` finds `.md` files in skill directories and registers them as skills.
8. **Resolves skill references** — `packages/resolver/src/skills.ts` processes `references:` paths attached to skills, resolving relative paths to absolute.

The result is a `ResolvedAST` containing either a fully-merged `Program` AST or a list of `ResolveError`s.

#### Stage 1.5: Reference Integrity

When a lockfile with references is configured, the compiler verifies content hashes of all referenced files. This ensures that skill dependencies haven't been tampered with since the lockfile was generated. Controlled by `--ignore-hashes` flag.

#### Stage 2: Validate

```typescript
// packages/compiler/src/compiler.ts, line ~195
const validation = this.validator.validate(resolved.ast);
```

The `Validator` (from `@promptscript/validator`) checks the resolved AST against 16+ rules defined in `packages/validator/src/rules/`:

| Rule ID | Name | Purpose |
|---------|------|---------|
| PS001 | requiredMetaId | `@meta { id: "..." }` is required |
| PS002 | requiredMetaSyntax | `@meta { syntax: "..." }` is required |
| PS003 | validSemver | Syntax must be valid semver |
| PS004 | requiredGuards | Guards block must exist |
| PS005 | blockedPatterns | No blocked content patterns |
| PS006 | validPath | Path references must resolve |
| PS007 | deprecated | Deprecated features warning |
| PS008 | emptyBlock | No empty blocks |
| PS009 | validParams | Parameter definitions are valid |
| PS010 | suspiciousUrls | URL safety checks |
| PS011 | authorityInjection | Authority injection prevention |
| PS012 | obfuscatedContent | Obfuscation detection |
| PS013 | pathTraversal | Path traversal prevention |
| PS014 | unicodeSecurity | Unicode security checks |
| PS015 | duplicateSkills | No duplicate skill names |
| PS031 | referenceIntegrity | Lockfile hash verification |

Security presets (`SECURITY_STRICT`, `SECURITY_MODERATE`, `SECURITY_MINIMAL`) enable different subsets of these rules.

#### Stage 3: Format

```typescript
// packages/compiler/src/compiler.ts, line ~210
const output = formatter.format(resolved.ast, formatOptions);
```

Each registered formatter transforms the resolved AST into a platform-specific output. The formatter registry (`packages/formatters/src/section-registry.ts`) manages registration and lookup. Output includes:

- **Primary file**: The main instruction file (e.g., `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`)
- **Additional files**: Skill-specific files, command files, configuration files
- **Markers**: PromptScript generation markers (HTML comments or YAML comments) for overwrite detection

### 1.3 The AST Type System

The core type system is defined in `packages/core/src/types/ast.ts`. Key types:

**Program** (root node):
```typescript
interface Program {
  type: 'Program';
  meta?: MetaBlock;           // @meta { id, syntax, params }
  inherit?: InheritDeclaration; // @inherit @namespace/path
  uses: UseDeclaration[];     // @use declarations
  blocks: Block[];            // @identity, @context, @skills, etc.
  extends: ExtendBlock[];     // @extend modifications
}
```

**Block** (content container):
```typescript
interface Block {
  type: 'Block';
  name: BlockName;            // 'identity', 'context', 'skills', 'agents', etc.
  content: BlockContent;      // TextContent | ObjectContent | ArrayContent | MixedContent
}
```

**SkillDefinition** (skill schema):
```typescript
interface SkillDefinition {
  description: string;        // Required
  content?: string | TextContent;
  params?: ParamDefinition[];
  trigger?: string;
  userInvocable?: boolean;
  allowedTools?: string[];
  requires?: string[];        // Dependencies on other skills
  inputs?: Record<string, SkillContractField>;   // Input contract
  outputs?: Record<string, SkillContractField>;   // Output contract
  examples?: Record<string, ExampleDefinition>;
  references?: string[];      // File references
  composedFrom?: ComposedPhase[]; // Resolver-set metadata
}
```

The `SkillContractField` type defines typed input/output schemas with `description`, `type` (string|number|boolean|enum), optional `options`, and `default` values. This contract system is the foundation for compositional skill assembly.

### 1.4 The Skill System

Skills are the primary unit of capability in PromptScript. They are defined in the `@skills` block of a `.prs` file:

```
@skills {
  code-review: {
    description: "Reviews code for quality, security, and correctness"
    trigger: "review this code"
    userInvocable: true
    allowedTools: ["read", "exec", "github"]
    inputs: {
      code_path: { description: "File to review", type: "string" }
      focus: { description: "Review focus area", type: "enum", options: ["security", "quality", "performance"] }
    }
    outputs: {
      review_summary: { description: "Review findings", type: "string" }
      score: { description: "Quality score 1-10", type: "number" }
    }
    requires: ["read-file", "git-context"]
  }
}
```

**Key properties of the skill system:**

1. **Parameterization**: Skills can define `params` with types, defaults, and constraints. These are filled at import time via `@use @namespace/skill(param: "value")`.

2. **Contracts**: The `inputs`/`outputs` fields define typed interfaces. This enables:
   - **Type checking** at compile time (validator ensures contracts are satisfied)
   - **Composition**: Skills can require other skills whose outputs match their inputs
   - **Documentation**: Contracts serve as self-documenting interfaces

3. **Dependencies**: The `requires` field creates a dependency graph. Skills that aren't satisfied cause validation errors.

4. **Composition via `@use` inside `@skills`**: The `InlineUseDeclaration` type and `resolveSkillComposition()` function allow skills to import sub-skills as numbered phases. Each phase's context blocks (`knowledge`, `restrictions`, `standards`) are extracted and flattened into the parent skill.

5. **References**: The `references` field attaches file paths (resolved by the resolver) to skill context, providing the skill with domain-specific knowledge.

6. **Auto-discovery**: Native `.md` files in skill directories are automatically discovered and registered as skills via `discoverNativeContent()`.

### 1.5 The 38 Agent Formatters

The formatter directory (`packages/formatters/src/formatters/`) contains 38 formatters, each targeting a specific AI agent platform:

| Formatter | Output Target | Key Characteristic |
|-----------|--------------|-------------------|
| `claude.ts` | `CLAUDE.md` | Claude Code instructions |
| `cursor.ts` | `.cursor/rules/` | Cursor IDE rules (multiple files) |
| `github.ts` | `.github/prompts/` | GitHub Copilot prompts |
| `openclaw.ts` | `INSTRUCTIONS.md` / `.openclaw/` | OpenClaw agent instructions |
| `cline.ts` | `.clinerules/` | Cline rules |
| `roo.ts` | `.roo/` | Roo Code rules |
| `windsurf.ts` | `.windsurfrules` | Windsurf IDE |
| `codex.ts` | `CODEX.md` | OpenAI Codex |
| `gemini.ts` | `GEMINI.md` | Gemini CLI |
| `kiro.ts` | `.kiro/` | Kiro IDE |
| `junie.ts` | `.junie/` | Junie by JetBrains |
| `goose.ts` | `.goose/` | Goose agent |
| `augment.ts` | `.augment/` | Augment Code |
| `factory.ts` | Factory AI | YAML frontmatter |
| `continue.ts` | `.continue/` | Continue.dev |
| `trae.ts` | `.trae/` | Trae IDE |
| `amp.ts` | `AMP.md` | Amp agent |
| `crush.ts` | `CRUSH.md` | Crush agent |
| `antigravity.ts` | `.antigravity/` | Antigravity |
| `codebuddy.ts` | `.codebuddy/` | CodeBuddy |
| `cortex.ts` | `.cortex/` | Cortex |
| `iflow.ts` | `.iflow/` | iFlow |
| `kode.ts` | `.kode/` | Kode |
| `kilo.ts` | `.kilo/` | Kilo |
| `mux.ts` | `.mux/` | Mux |
| `neovate.ts` | `.neovate/` | Neovate |
| `opencode.ts` | `.opencode/` | OpenCode |
| `openhands.ts` | `.openhands/` | OpenHands |
| `pi.ts` | `PI.md` | Pi agent |
| `pochi.ts` | `.pochi/` | Pochi |
| `qoder.ts` | `.qoder/` | Qoder |
| `qwen-code.ts` | `QWEN_CODE.md` | Qwen Code |
| `zencoder.ts` | `.zencoder/` | ZenCoder |
| `adal.ts` | `.adal/` | Adal |
| `command-code.ts` | `.command-code/` | Command Code |
| `mcpjam.ts` | `.mcpjam/` | MCPJam |
| `mistral-vibe.ts` | `MISTRAL_VIBE.md` | Mistral Vibe |

Each formatter implements the `Formatter` interface:

```typescript
interface Formatter {
  readonly name: string;
  format(ast: Program, options?: FormatOptions): FormatterOutput;
  getSkillBasePath?(): string;
  getSkillFileName?(): string;
  transformInjectedSkillContent?(content: string): string;
}
```

The `FormatterOutput` contains the generated file path and content. Many formatters also produce `additionalFiles` for skill-specific output, command definitions, or multi-file rule sets.

The convention system (`packages/formatters/src/convention-renderer.ts`) and section registry (`packages/formatters/src/section-registry.ts`) provide shared rendering logic that formatters customize via configuration rather than reimplementing from scratch.

### 1.6 The Inheritance Model

PromptScript uses three mechanisms for composition:

**`@inherit`** — Single inheritance with deep merge:
```
@inherit @core/typescript-standards
```
- Parent's blocks merge with child's (child wins on conflict)
- Text content is concatenated (parent first, then child)
- Arrays are unique-concatenated
- Objects are deep-merged
- Only one `@inherit` per file (single inheritance)

**`@use`** — Import declarations:
```
@use @core/guards/compliance as security
@use @fragments/header(title: "Welcome") as header into skills/seo
```
- Imports fragments or skills with optional aliases
- Supports template parameters
- Optional `into "path"` for custom output directory

**`@extend`** — Targeted block modifications:
```
@extend standards.code {
  frameworks: [react]
}
```
- Dot-separated path targeting specific nested blocks
- Merges content into the target block

The combination of single inheritance (`@inherit`) + multiple imports (`@use`) + targeted extensions (`@extend`) gives PromptScript a composition model that is more composable than multiple inheritance but more structured than mixins.

### 1.7 The Browser Compiler

The `browser-compiler` package (`packages/browser-compiler/`) provides a WASM-ready compiler that works in browser environments. It uses:

- `virtual-fs.ts` — In-memory filesystem for `.prs` file resolution
- `shims/fs.ts` — Node.js `fs` API shims
- `compiler.ts` — Browser-compatible compilation pipeline
- `resolver.ts` — Browser-compatible resolver using virtual FS
- `registry.ts` — In-memory registry

This is critical for our integration: it proves the compiler can run in constrained environments, which means it can run inside a WASM runtime alongside our Rust crates.

---

## Section 2: SuperInstance Integration Points

### 2.1 Compiler → Conservation Laws

**Integration point:** `packages/compiler/src/compiler.ts` — the `compile()` method.

The PromptScript compiler pipeline (resolve → validate → format) currently measures timing stats but doesn't track computational resources. We insert conservation law enforcement at each stage boundary.

**Concrete changes:**

Create a new file `packages/compiler/src/conservation-tracker.ts`:

```typescript
import { ConservationBudget, type ConservationState } from '@superinstance/entropy-conservation';

export interface CompilationConservation {
  /** Initialize budget at compilation start */
  begin(totalCapacity: number): void;
  /** Deduct entropy cost for a pipeline stage */
  deductStage(stage: 'resolve' | 'validate' | 'format', tokensProcessed: number): ConservationState;
  /** Check if remaining budget allows continuation */
  canContinue(): boolean;
  /** Final state after compilation */
  finalize(): ConservationState;
}
```

The `Compiler` class is modified to:

1. **Before Stage 1 (Resolve):** Initialize a `ConservationBudget` with capacity `C` derived from the total AST node count estimate.
2. **After Stage 1:** Calculate entropy production `H_resolve` from the number of resolved nodes. Deduct from budget: `γ = C - H_resolve`. If `γ < γ_min` (minimum spectral gap for fleet stability), emit a warning.
3. **After Stage 2 (Validate):** Validation adds constraints, which reduces entropy. Calculate `H_validate` as the number of validation errors found. The spectral gap increases: `γ += H_errors_avoided`.
4. **After Stage 3 (Format):** Each formatter produces output that carries its own entropy budget. The formatter's output size in tokens is its entropy contribution.

The key invariant: **total output entropy ≤ C - γ_min**. If compilation would produce more output than the conservation budget allows, the compiler truncates or splits the output.

**API surface in `entropy-conservation` crate:**

```rust
// crates/entropy-conservation/src/budget.rs
pub struct ConservationBudget {
    capacity: f64,        // C
    spectral_gap: f64,    // γ
    entropy_rate: f64,    // H
}

impl ConservationBudget {
    pub fn new(capacity: f64) -> Self;
    pub fn deduct(&mut self, entropy_cost: f64) -> Result<ConservationState, BudgetExceeded>;
    pub fn remaining_gap(&self) -> f64;
    pub fn can_continue(&self) -> bool;
}
```

Compiled to WASM via `wasm-pack build --target web`, this runs inside the PromptScript compiler as a WebAssembly module.

### 2.2 Formatters → Spectral Methods

**Integration point:** `packages/formatters/src/formatters/factory.ts` — formatter selection.

Currently, formatter selection is user-specified (you pick which formatters to use). We add a spectral ranking layer that automatically selects the best formatter(s) for a given `.prs` input.

**Concrete approach:**

Create `packages/formatters/src/spectral-ranking.ts`:

```typescript
import { SpectralFleet } from '@superinstance/spectral-fleet-wasm';

interface FormatterRanking {
  formatter: string;
  score: number;       // Eigenvalue-weighted quality score
  eigenvalue: number;  // Spectral contribution
}

export async function rankFormatters(ast: Program): Promise<FormatterRanking[]> {
  // 1. Extract features from the AST (block types, skill counts, content size)
  const features = extractAstFeatures(ast);
  
  // 2. Build affinity graph: formatters × features
  //    Edge weight = how well a formatter handles that feature
  const graph = buildFormatterFeatureGraph(features, knownFormatters);
  
  // 3. Compute spectral decomposition
  const { eigenvalues, fiedlerVector } = await SpectralFleet.decompose(graph);
  
  // 4. Rank formatters by their projection onto the Fiedler vector
  //    Higher projection = better fit for the input's natural clustering
  return rankByFiedlerProjection(knownFormatters, fiedlerVector);
}
```

The spectral ranking replaces manual formatter selection in the compiler options. When `formatters: 'auto'` is specified, the compiler:

1. Runs a lightweight feature extraction on the resolved AST
2. Constructs a bipartite graph (formatters × features)
3. Computes the spectral decomposition via `spectral-fleet` WASM
4. Returns the top-N formatters ranked by Fiedler vector projection

This means a `.prs` file that defines many `@skills` with complex contracts automatically routes to formatters that handle skills well (e.g., `cursor`, `openclaw`). A `.prs` that's mostly `@identity` text routes to simpler formatters (e.g., `claude`, `codex`).

**API surface in `spectral-fleet` crate:**

```rust
// crates/spectral-fleet/src/decompose.rs
pub struct BipartiteGraph {
    left_nodes: usize,   // formatter count
    right_nodes: usize,  // feature count
    weights: Vec<f64>,   // edge weights
}

pub fn spectral_decompose(graph: &BipartiteGraph) -> SpectralResult {
    // Lanczos iteration for top-k eigenvalues
    // Returns eigenvalues + eigenvectors
}

pub struct SpectralResult {
    pub eigenvalues: Vec<f64>,
    pub eigenvectors: Vec<Vec<f64>>,
    pub fiedler_vector: Vec<f64>,
    pub spectral_gap: f64,
}
```

### 2.3 Skill System → Category Theory

**Integration point:** `packages/resolver/src/skill-composition.ts` + `packages/core/src/types/ast.ts` (`SkillDefinition`).

This is the deepest integration. PromptScript skills *are* objects in a category, and the skill composition system *is* categorical composition. We make this explicit.

**The category of skills:**

- **Objects**: `SkillDefinition` instances, identified by their `description` + contract signature
- **Morphisms**: Skill dependencies (`requires` field) + data flow through `outputs → inputs` contracts
- **Composition**: If skill A `outputs` match skill B's `inputs`, there exists a morphism `A → B`
- **Identity**: The trivial skill that passes through all inputs as outputs

**Concrete changes to `SkillDefinition`:**

```typescript
// Extension to packages/core/src/types/ast.ts
interface SkillDefinition {
  // ... existing fields ...
  
  /** Categorical composition metadata (set by resolver) */
  categorical?: {
    /** This skill's object ID in the category */
    objectId: string;
    /** Morphisms this skill participates in */
    morphisms: SkillMorphism[];
    /** Functor mapping from specification to implementation */
    functorMap?: FunctorMapping;
  };
}

interface SkillMorphism {
  source: string;        // Source skill objectId
  target: string;        // Target skill objectId
  /** Map from source outputs to target inputs */
  mapping: Record<string, string>;
  /** Whether composition is verified correct */
  verified: boolean;
}

interface FunctorMapping {
  specificationCategory: string;
  implementationCategory: string;
  /** The adjunction: best implementation adds least unnecessary structure */
  adjunctionQuality: number;
}
```

**Changes to skill composition resolver:**

In `packages/resolver/src/skill-composition.ts`, after resolving inline `@use` declarations, we add categorical verification:

1. **Build the composition graph**: Each phase becomes an object, each `outputs → inputs` match becomes a morphism.
2. **Verify associativity**: If A → B → C composes, then (A → B) → C must equal A → (B → C). We check this by comparing the flattened output schemas.
3. **Verify identity**: The trivial composition (zero phases) should produce the identity morphism.
4. **Compute functorial mappings**: Map from the "specification" category (what the `.prs` file describes) to the "implementation" category (what the resolved AST produces).

**API surface in `categorical-agents` crate:**

```rust
// crates/categorical-agents/src/composition.rs
pub struct SkillCategory {
    objects: Vec<SkillObject>,
    morphisms: Vec<SkillMorphism>,
}

pub fn verify_composition(category: &SkillCategory) -> CompositionResult {
    // Check associativity of morphism composition
    // Check identity laws
    // Return verified composition graph
}

pub fn functorial_map(
    spec_category: &SkillCategory,
    impl_category: &SkillCategory,
) -> FunctorMapping {
    // Find the functor from specification to implementation
    // Measure adjunction quality
}
```

The practical benefit: **when you compose skills in a `.prs` file, the categorical verification guarantees that the composition is correct without needing to test every possible combination**. If A works and B works and their contracts match, A+B works.

### 2.4 Resolver → Optimal Transport

**Integration point:** `packages/resolver/src/resolver.ts` — the `resolve()` method, specifically the deep merge in inheritance resolution.

Currently, when a child's block conflicts with a parent's block, the child wins unconditionally. This is a hard override. We replace this with an optimal transport approach: the resolution minimizes the Wasserstein distance between the parent configuration and the child configuration.

**Why optimal transport?**

Think of the parent's blocks as a probability distribution over "configuration space" and the child's modifications as another distribution. The merge should find the cheapest way to transform the parent distribution into something that incorporates the child's preferences. The "cost" is measured in Wasserstein distance — the minimum "earth moving" cost to reshape one distribution into the other.

**Concrete approach:**

Create `packages/resolver/src/ot-merge.ts`:

```typescript
import { WassersteinSolver } from '@superinstance/wasserstein-agents-wasm';

interface BlockDistribution {
  blockName: string;
  features: Float64Array;  // TF-IDF or embedding of block content
  weight: number;          // Relative importance
}

export function otMerge(
  parentBlocks: Block[],
  childBlocks: Block[],
): Block[] {
  // 1. Convert blocks to distributions
  const parentDist = blocksToDistribution(parentBlocks);
  const childDist = blocksToDistribution(childBlocks);
  
  // 2. Solve optimal transport problem
  const transport = WassersteinSolver.solve(parentDist, childDist, {
    metric: 'euclidean',
    regularization: 0.1,  // Entropic regularization for speed
  });
  
  // 3. Use transport plan to guide merge decisions
  //    High transport cost = child strongly overrides parent
  //    Low transport cost = parent content preserved
  return applyTransportPlan(parentBlocks, childBlocks, transport);
}
```

This replaces the current `deepMerge` in inheritance resolution with a transport-aware merge that:
- Preserves parent content where the child doesn't explicitly diverge
- Smoothly interpolates between parent and child preferences
- Quantifies the "cost" of each merge decision (useful for debugging)

**API surface in `wasserstein-agents` crate:**

```rust
// crates/wasserstein-agents/src/solver.rs
pub struct WassersteinSolver;

impl WassersteinSolver {
    pub fn solve(
        source: &Distribution,
        target: &Distribution,
        config: &SolverConfig,
    ) -> TransportPlan {
        // Sinkhorn algorithm with entropic regularization
        // Returns transport matrix + Wasserstein distance
    }
}

pub struct TransportPlan {
    pub matrix: Vec<Vec<f64>>,  // Transport matrix
    pub distance: f64,           // Wasserstein-1 distance
    pub cost: f64,               // Total transport cost
}
```

### 2.5 Validator → Lattice Cryptography

**Integration point:** `packages/validator/src/validator.ts` — the validation result.

After validation succeeds, we sign the validated AST with a lattice-based signature. This creates a tamper-proof record of what was validated and what rules were applied.

**Why lattice cryptography?**

Traditional RSA/ECDSA signatures are vulnerable to quantum computers. Lattice-based signatures (specifically, Module-LWE based schemes like Dilithium/ML-DSA) are post-quantum secure. Since agent configurations may be in use for years, we need signatures that remain secure against future quantum attacks.

**Concrete approach:**

Create `packages/validator/src/lattice-signer.ts`:

```typescript
import { LatticeSigner, type Signature } from '@superinstance/lattice-crypto-wasm';

export interface ValidatedAndSigned {
  valid: boolean;
  errors: ValidationMessage[];
  warnings: ValidationMessage[];
  signature?: {
    algorithm: 'ML-DSA-65';
    publicKey: Uint8Array;
    signature: Uint8Array;
    signedHash: string;  // SHA-3 hash of canonical AST
    timestamp: string;
  };
}

export async function signValidation(
  ast: Program,
  validationResult: ValidationResult,
): Promise<ValidatedAndSigned> {
  if (!validationResult.valid) {
    return { ...validationResult, signature: undefined };
  }
  
  // Canonical serialization of the AST
  const canonical = canonicalize(ast);
  
  // Sign with lattice-based signature
  const signer = await LatticeSigner.fromSeed(getSeed());
  const hash = await sha3_256(canonical);
  const signature = signer.sign(hash);
  
  return {
    ...validationResult,
    signature: {
      algorithm: 'ML-DSA-65',
      publicKey: signer.publicKey,
      signature: signature.bytes,
      signedHash: hash,
      timestamp: new Date().toISOString(),
    },
  };
}
```

Downstream consumers (agents, servers, fleet wardens) can verify the signature before using the configuration, ensuring it hasn't been tampered with since validation.

**API surface in `lattice-crypto` crate:**

```rust
// crates/lattice-crypto/src/signing.rs
pub struct MlDsaSigner {
    // Module-LWE based signer (Dilithium/ML-DSA)
}

impl MlDsaSigner {
    pub fn from_seed(seed: &[u8]) -> Self;
    pub fn sign(&self, message: &[u8]) -> Signature;
    pub fn verify(public_key: &[u8], message: &[u8], signature: &[u8]) -> bool;
}

pub struct Signature {
    pub bytes: Vec<u8>,
    pub algorithm: Algorithm,
}
```

### 2.6 Server → Fleet Warden

**Integration point:** `packages/server/src/server.ts` + `packages/server/src/watcher.ts`.

The PromptScript server watches `.prs` files and recompiles on change. We extend it to also monitor the health of agents consuming those compiled outputs, using Fleet Warden for anomaly detection.

**Architecture:**

```
.prs file changes
       ↓
  PromptScript Server (watcher)
       ↓ compile
  Compiled agent configs (.md, .mdc)
       ↓ distribute
  Agent Fleet (Claude, Cursor, OpenClaw, etc.)
       ↓ health metrics
  Fleet Warden (anomaly detection + circuit breakers)
       ↓ feedback
  PromptScript Server (recompile if needed)
```

**Concrete changes:**

Create `packages/server/src/fleet-monitor.ts`:

```typescript
import { FleetWarden, type AgentHealth, type AnomalyReport } from '@superinstance/fleet-warden-wasm';

export class FleetMonitor {
  private warden: FleetWarden;
  
  constructor() {
    this.warden = new FleetWarden({
      anomalyThreshold: 0.85,
      circuitBreakerThreshold: 3,  // 3 anomalies before breaking
      healthCheckInterval: 30000,  // 30 seconds
    });
  }
  
  /** Register an agent with the fleet */
  registerAgent(agentId: string, config: CompiledConfig): void;
  
  /** Report agent health metrics */
  reportHealth(agentId: string, metrics: AgentMetrics): AnomalyReport | null;
  
  /** Check if circuit breaker is tripped for an agent */
  isCircuitOpen(agentId: string): boolean;
  
  /** Get fleet-wide health summary */
  getFleetHealth(): FleetHealthSummary;
}
```

The server integrates FleetMonitor into its compilation loop:

1. **After compilation**: Register compiled configs with FleetMonitor
2. **On agent health report**: Check for anomalies
3. **On anomaly detection**: Log warning, potentially trigger recompilation with adjusted parameters
4. **On circuit breaker trip**: Stop distributing to the affected agent, alert operators

**API surface in `fleet-warden` crate:**

```rust
// crates/fleet-warden/src/warden.rs
pub struct FleetWarden {
    agents: HashMap<AgentId, AgentState>,
    anomaly_detector: AnomalyDetector,
    circuit_breakers: HashMap<AgentId, CircuitBreaker>,
}

pub struct AnomalyDetector {
    // Statistical process control (SPC) based detector
    // Uses exponentially weighted moving average (EWMA)
}

pub struct CircuitBreaker {
    failure_count: u32,
    threshold: u32,
    state: CircuitState,  // Closed, Open, HalfOpen
}
```

### 2.7 Temporal → T-Minus

**Integration point:** New package `packages/scheduler/` (or extension to `packages/server/`).

Skills defined in `.prs` files can have temporal activation rules. The T-Minus crate provides the temporal logic engine that enforces these schedules.

**Concrete approach — `@schedule` directive:**

```
@skills {
  security-audit: {
    description: "Periodic security audit using lattice-crypto verification"
    schedule: "0 */6 * * *"   // Every 6 hours
    temporal: {
      deadline: "2h"
      retry: { max: 3, backoff: "exponential" }
    }
    allowedTools: ["fleet-warden", "lattice-crypto"]
    outputs: {
      audit_report: { description: "Security audit findings", type: "string" }
    }
  }
}
```

The `schedule` field triggers the T-Minus temporal logic engine:

```typescript
import { TMinus, type TemporalConstraint } from '@superinstance/t-minus-wasm';

export class SkillScheduler {
  private engine: TMinus;
  
  constructor() {
    this.engine = new TMinus({
      clockMode: 'lamport',      // Lamport-style logical clocks
      spectralTimestamps: true,   // Augment with fleet state
    });
  }
  
  /** Register a skill's temporal constraints */
  registerSkill(skill: SkillDefinition): void {
    if (!skill.schedule) return;
    
    const constraint: TemporalConstraint = {
      cron: skill.schedule,
      deadline: skill.temporal?.deadline,
      retry: skill.temporal?.retry,
    };
    
    this.engine.schedule(constraint, () => this.executeSkill(skill));
  }
  
  /** Execute a scheduled skill through the compiler pipeline */
  private async executeSkill(skill: SkillDefinition): Promise<void>;
}
```

**API surface in `t-minus` crate:**

```rust
// crates/t-minus/src/engine.rs
pub struct TMinus {
    logical_clock: LamportClock,
    spectral_stamper: Option<SpectralStamper>,
    scheduler: CronScheduler,
}

pub struct TemporalConstraint {
    pub cron: String,
    pub deadline: Option<Duration>,
    pub retry: Option<RetryPolicy>,
}

impl TMinus {
    pub fn schedule(&mut self, constraint: TemporalConstraint, callback: Box<dyn Fn()>);
    pub fn propagate_deadline(&self, deadline: Instant) -> Vec<AgentId>;
    pub fn check_invariants(&self) -> Vec<TemporalViolation>;
}
```

---

## Section 3: The Killer App — "Open Mind"

### 3.1 Vision

**Open Mind** is a PromptScript-powered agent framework where:

- Users write `.prs` files that define agent **personalities** (`@identity`), **knowledge** (`@knowledge`, `@context`), and **capabilities** (`@skills` with Rust crate backends)
- Capabilities are backed by SuperInstance Rust crates compiled to WASM
- The agent's response **is** the application — there is no code generation step
- Multiple crate capabilities compose within a single conversation via categorical skill composition

The key insight: **every other agent framework treats the agent as a code generator**. You describe what you want, the agent generates code, and you run the code. Open Mind skips the code generation step. The agent *directly executes* mathematical operations via WASM-backed skills.

### 3.2 Architecture

```
┌─────────────────────────────────────────────┐
│                   User                       │
│         (writes .prs files)                  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│          PromptScript Compiler               │
│  (resolve → validate → format + conservation │
│   tracking + lattice signing)                │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│           Skill Runtime (WASM)               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ spectral- │ │wasserstein│ │categorical│   │
│  │  fleet    │ │ -agents  │ │ -agents  │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ lattice-  │ │ entropy- │ │ t-minus  │    │
│  │  crypto   │ │conserv.  │ │          │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ harmonic- │ │tropical- │ │persistent│    │
│  │   plr     │ │ harmony  │ │  sheaf   │    │
│  └──────────┘ └──────────┘ └──────────┘    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│            Open Mind Agent                   │
│  (personality + capabilities = emergent      │
│   behavior, no code generation)              │
└─────────────────────────────────────────────┘
```

### 3.3 Example 1: Music Theory Tutor

**`.prs` file: `music-theory-tutor.prs`**

```
@meta {
  id: "music-theory-tutor"
  syntax: "1.0.0"
}

@identity {
  """
  You are an expert music theory tutor with deep mathematical understanding
  of harmony. You analyze chord progressions using neo-Riemannian theory
  (PLR operations) and tropical geometry. You explain concepts in both
  musical and mathematical terms, adapting to the student's level.
  """
}

@context {
  """
  You have access to real-time harmonic analysis via the harmonic-plr and
  tropical-harmony crates. When a student plays a chord progression, you
  analyze it through multiple mathematical lenses:
  - PLR voice-leading distance (how smoothly voices move)
  - Tropical harmonic distances (geometric interpretation)
  - Tonnetz position (spatial harmony mapping)
  You provide both intuitive explanations and precise mathematical analysis.
  """
}

@skills {
  analyze-progression: {
    description: "Analyze a chord progression using PLR operations and tropical geometry"
    trigger: "analyze this progression"
    userInvocable: true
    inputs: {
      chords: { description: "Chord progression (e.g., C Am F G)", type: "string" }
      key: { description: "Musical key", type: "string" }
    }
    outputs: {
      plr_analysis: { description: "PLR voice-leading analysis", type: "string" }
      tropical_distance: { description: "Tropical geometric distance", type: "number" }
      tonnetz_path: { description: "Path on the Tonnetz", type: "string" }
    }
  }

  suggest-voicings: {
    description: "Suggest alternative voicings that minimize voice-leading distance"
    trigger: "suggest voicings"
    userInvocable: true
    requires: ["analyze-progression"]
    inputs: {
      chords: { description: "Original progression", type: "string" }
      target_distance: { description: "Maximum PLR distance", type: "number" }
    }
    outputs: {
      alternatives: { description: "Alternative voicings", type: "string" }
      distances: { description: "Voice-leading distances for each", type: "string" }
    }
  }

  explain-theory: {
    description: "Explain the music theory behind an analysis result"
    trigger: "explain"
    userInvocable: true
    requires: ["analyze-progression"]
  }
}
```

**What happens at runtime:**

1. Student types: "What's happening harmonically in C → A♭ → E → C?"
2. The agent invokes `analyze-progression`:
   - `harmonic-plr` WASM module computes: C→A♭ is an R operation (relative), A♭→E is an L operation (leading tone exchange), E→C is a P operation (parallel)
   - `tropical-harmony` WASM module computes the tropical distance: the progression traces a triangle on the Tonnetz with tropical perimeter 3.7
3. The agent synthesizes: "You've discovered the hexatonic pole relationship! C and A♭ are connected by an R operation (they share the note C). Then A♭→E is actually an L operation — they share G♭/F#. The whole thing traces a hexatonic cycle: R-L-P, which is one of the three maximally smooth cycles in neo-Riemannian theory."
4. No code was generated. The WASM modules computed real mathematical results that the agent interpreted conversationally.

### 3.4 Example 2: Security Consultant

**`.prs` file: `security-consultant.prs`**

```
@meta {
  id: "security-consultant"
  syntax: "1.0.0"
}

@identity {
  """
  You are a senior security consultant specializing in cryptographic systems
  and distributed infrastructure. You audit systems using lattice-based
  cryptography analysis and fleet-level anomaly detection.
  """
}

@skills {
  audit-cryptography: {
    description: "Audit a system's cryptographic posture using lattice-crypto analysis"
    trigger: "audit crypto"
    userInvocable: true
    inputs: {
      system_config: { description: "System configuration to audit", type: "string" }
    }
    outputs: {
      vulnerabilities: { description: "Identified vulnerabilities", type: "string" }
      quantum_readiness: { description: "Post-quantum readiness score", type: "number" }
      recommendations: { description: "Remediation recommendations", type: "string" }
    }
  }

  fleet-health-check: {
    description: "Check fleet health using anomaly detection"
    trigger: "check fleet health"
    userInvocable: true
    schedule: "0 */4 * * *"
    inputs: {
      fleet_config: { description: "Fleet configuration", type: "string" }
    }
    outputs: {
      health_report: { description: "Fleet health analysis", type: "string" }
      anomalies: { description: "Detected anomalies", type: "string" }
    }
  }

  sign-and-verify: {
    description: "Create and verify lattice-based signatures for agent configurations"
    trigger: "sign config"
    userInvocable: true
    inputs: {
      config: { description: "Configuration to sign", type: "string" }
    }
    outputs: {
      signature: { description: "ML-DSA signature", type: "string" }
      verified: { description: "Verification status", type: "boolean" }
    }
  }
}
```

### 3.5 Example 3: Research Assistant

**`.prs` file: `research-assistant.prs`**

```
@meta {
  id: "research-assistant"
  syntax: "1.0.0"
}

@identity {
  """
  You are a research assistant specializing in topological data analysis
  and optimal transport. You help researchers analyze complex datasets
  using persistent homology, sheaf theory, and Wasserstein distances.
  """
}

@skills {
  topological-analysis: {
    description: "Analyze data topology using persistent sheaf cohomology"
    trigger: "analyze topology"
    userInvocable: true
    inputs: {
      dataset: { description: "Dataset to analyze", type: "string" }
      dimensions: { description: "Max filtration dimension", type: "number" }
    }
    outputs: {
      persistence_diagram: { description: "Persistence diagram data", type: "string" }
      betti_numbers: { description: "Betti numbers", type: "string" }
      topological_features: { description: "Significant topological features", type: "string" }
    }
  }

  transport-analysis: {
    description: "Compute optimal transport between distributions"
    trigger: "compute transport"
    userInvocable: true
    inputs: {
      source_distribution: { description: "Source distribution", type: "string" }
      target_distribution: { description: "Target distribution", type: "string" }
    }
    outputs: {
      transport_plan: { description: "Optimal transport plan", type: "string" }
      wasserstein_distance: { description: "Wasserstein distance", type: "number" }
    }
  }

  combined-analysis: {
    description: "Combine topological and transport analysis for dataset comparison"
    trigger: "compare datasets"
    userInvocable: true
    requires: ["topological-analysis", "transport-analysis"]
  }
}
```

### 3.6 The "No Code Generation" Principle

The fundamental difference between Open Mind and every other agent framework:

**Traditional agent framework:**
```
User: "Analyze this chord progression"
Agent: *generates Python code*
Agent: "Here's the code to run: [code block]"
User: *copies code, runs it, pastes result back*
Agent: "Based on those results..."
```

**Open Mind:**
```
User: "Analyze this chord progression"
Agent: *invokes harmonic-plr WASM skill directly*
Agent: "The C→Am transition is a P (parallel) operation with distance 1.
       Am→F is an L (leading-tone) operation. The total voice-leading
       distance is 2, which is very smooth — this is why it sounds natural."
```

The agent doesn't generate code. It *is* the code. The WASM skills execute mathematical operations directly, and the agent's response is the interpreted result.

This is possible because PromptScript's skill system + SuperInstance's WASM crates create a runtime where skills aren't descriptions of code to write — they're executable capabilities.

### 3.7 Self-Improvement Loop

The most ambitious aspect of Open Mind: the agent improves its own skills through spectral feedback.

```
Agent uses skill → produces output
       ↓
Output quality measured (user feedback + automated metrics)
       ↓
Spectral decomposition of skill usage patterns
       ↓
Identify high-quality vs low-quality skill invocations
       ↓
Adjust skill parameters (prompts, tool selection, constraints)
       ↓
Recompile .prs with adjusted parameters
       ↓
Improved agent
```

This is where the conservation law becomes critical: the self-improvement loop must respect γ+H=C. Each improvement cycle increases entropy (more skill invocations, more data to process). The conservation budget ensures the loop doesn't spiral — there's a hard cap on how much the agent can change per cycle.

---

## Section 4: Implementation Roadmap

### Phase 1 (Week 1–2): PromptScript Fork with SuperInstance Provider

**Goal:** A working PromptScript compiler that targets z.ai and DeepInfra models exclusively.

**Tasks:**

1. **Fork `github.com/SuperInstance/promptscript`** into `github.com/SuperInstance/promptscript-si`

2. **Create `packages/provider/` package:**
   ```
   packages/provider/
   ├── src/
   │   ├── index.ts
   │   ├── zai-provider.ts      # z.ai API client
   │   ├── deepinfra-provider.ts # DeepInfra API client
   │   ├── provider-registry.ts  # Provider registration
   │   └── types.ts              # Provider interfaces
   └── package.json
   ```

3. **Modify `packages/compiler/src/types.ts`:**
   ```typescript
   export interface CompilerOptions {
     // ... existing fields ...
     provider?: {
       name: 'zai' | 'deepinfra' | 'local';
       model?: string;
       apiKeyEnv?: string;
       baseUrl?: string;
     };
   }
   ```

4. **Create `packages/formatters/src/formatters/superinstance.ts`:**
   - Output format optimized for z.ai models
   - Leverages z.ai's structured output capabilities
   - Includes WASM skill metadata in the formatter output

5. **Register in `packages/formatters/src/formatters/index.ts`:**
   ```typescript
   export { SuperInstanceFormatter } from './superinstance.js';
   ```

6. **Update CLI (`packages/cli/`) to add `--provider` flag:**
   ```bash
   prs compile ./project.prs --provider zai --model glm-5.1
   ```

**Deliverables:**
- Forked repo with SuperInstance provider package
- Two working formatters: `superinstance` (z.ai) and `deepinfra`
- CLI flag for provider selection
- Tests for provider-specific formatting

### Phase 2 (Week 3–4): WASM Compilation of Top 10 Rust Crates

**Goal:** The top 10 SuperInstance Rust crates compile to WASM and are loadable from JavaScript.

**Priority crates for WASM compilation:**

| # | Crate | WASM Feasibility | Why First |
|---|-------|-----------------|-----------|
| 1 | `entropy-conservation` | ✅ Pure math | Conservation tracking in compiler |
| 2 | `spectral-fleet` | ✅ Linear algebra | Formatter ranking |
| 3 | `categorical-agents` | ✅ Type theory | Skill composition verification |
| 4 | `wasserstein-agents` | ✅ Optimization | Resolver merge |
| 5 | `lattice-crypto` | ⚠️ Crypto primitives | Config signing |
| 6 | `harmonic-plr` | ✅ Music math | Demo app (music tutor) |
| 7 | `tropical-harmony` | ✅ Tropical geometry | Demo app (music tutor) |
| 8 | `persistent-sheaf` | ⚠️ Complex | Topological analysis |
| 9 | `fleet-warden` | ✅ Monitoring | Server integration |
| 10 | `t-minus` | ✅ Scheduling | Temporal skill activation |

**Tasks:**

1. **For each crate, create a WASM wrapper:**
   ```rust
   // crates/spectral-fleet/src/wasm.rs
   use wasm_bindgen::prelude::*;
   
   #[wasm_bindgen]
   pub struct BipartiteGraph { /* ... */ }
   
   #[wasm_bindgen]
   impl BipartiteGraph {
       #[wasm_bindgen(constructor)]
       pub fn new(left: usize, right: usize) -> Self;
       
       pub fn set_weight(&mut self, i: usize, j: usize, w: f64);
       
       pub fn decompose(&self) -> Result<JsValue, JsValue>;
   }
   ```

2. **Build pipeline:**
   ```bash
   wasm-pack build --target web --out-dir pkg/
   ```

3. **Create npm packages for each WASM module:**
   ```
   @superinstance/entropy-conservation-wasm
   @superinstance/spectral-fleet-wasm
   @superinstance/categorical-agents-wasm
   @superinstance/wasserstein-agents-wasm
   @superinstance/lattice-crypto-wasm
   @superinstance/harmonic-plr-wasm
   @superinstance/tropical-harmony-wasm
   @superinstance/persistent-sheaf-wasm
   @superinstance/fleet-warden-wasm
   @superinstance/t-minus-wasm
   ```

4. **Create `packages/wasm-runtime/`:**
   - WASM module loader
   - Shared memory management
   - Error bridging (Rust errors → TypeScript errors)

**Deliverables:**
- 10 npm packages with WASM builds
- CI pipeline that builds and publishes WASM packages
- Integration tests: each WASM module callable from TypeScript
- Performance benchmarks: WASM execution time vs. native

### Phase 3 (Week 5–6): Skill System Integration

**Goal:** Each Rust crate becomes a PromptScript skill that can be invoked from `.prs` files.

**Tasks:**

1. **Create `packages/skill-runtime/`:**
   ```
   packages/skill-runtime/
   ├── src/
   │   ├── index.ts
   │   ├── runtime.ts          # Skill execution runtime
   │   ├── wasm-loader.ts      # Load WASM modules on demand
   │   ├── skill-registry.ts   # Register WASM-backed skills
   │   ├── contract-checker.ts # Verify input/output contracts
   │   └── types.ts
   └── package.json
   ```

2. **Create skill definitions for each crate:**
   ```
   registry/
   ├── @superinstance/
   │   ├── spectral-analysis/
   │   │   └── skill.prs
   │   ├── conservation-tracker/
   │   │   └── skill.prs
   │   ├── category-compose/
   │   │   └── skill.prs
   │   ├── optimal-transport/
   │   │   └── skill.prs
   │   ├── lattice-sign/
   │   │   └── skill.prs
   │   ├── harmonic-analysis/
   │   │   └── skill.prs
   │   ├── tropical-harmonics/
   │   │   └── skill.prs
   │   ├── sheaf-topology/
   │   │   └── skill.prs
   │   ├── fleet-monitor/
   │   │   └── skill.prs
   │   └── temporal-schedule/
   │       └── skill.prs
   ```

3. **Example skill definition (`registry/@superinstance/spectral-analysis/skill.prs`):**
   ```
   @meta {
     id: "spectral-analysis"
     syntax: "1.0.0"
   }
   
   @identity {
     """
     Spectral analysis of agent configurations using eigenvalue decomposition.
     Ranks formatters, detects fleet instability, and computes natural clustering.
     """
   }
   
   @skills {
     decompose: {
       description: "Compute spectral decomposition of an agent feature graph"
       userInvocable: true
       inputs: {
         features: { description: "Feature matrix as JSON", type: "string" }
         top_k: { description: "Number of eigenvalues to compute", type: "number" }
       }
       outputs: {
         eigenvalues: { description: "Top-k eigenvalues", type: "string" }
         fiedler_vector: { description: "Fiedler vector for clustering", type: "string" }
         spectral_gap: { description: "Spectral gap (convergence rate)", type: "number" }
       }
     }
   }
   ```

4. **Modify resolver to support `@superinstance/` registry paths:**
   - In `packages/resolver/src/registry.ts`, add a `SuperInstanceRegistry` that resolves `@superinstance/*` paths to the WASM skill registry
   - Support versioned resolution: `@superinstance/spectral-analysis@1.2.0`

5. **Extend `SkillDefinition` type with WASM execution metadata:**
   ```typescript
   interface SkillDefinition {
     // ... existing fields ...
     wasmModule?: string;      // WASM module path
     wasmFunction?: string;    // Function name to invoke
     wasmMemory?: number;      // Required WASM memory (MB)
   }
   ```

**Deliverables:**
- 10 WASM-backed skills in the `@superinstance/` registry
- Skill runtime that loads and executes WASM modules
- Contract checking: inputs/outputs verified against skill definitions
- Resolver support for `@superinstance/` paths

### Phase 4 (Week 7–8): Open Mind MVP

**Goal:** A working agent that uses 3+ crate capabilities in a single conversation.

**Tasks:**

1. **Create the Open Mind application:**
   ```
   open-mind/
   ├── src/
   │   ├── index.ts            # Entry point
   │   ├── agent.ts            # Agent runtime
   │   ├── conversation.ts     # Conversation manager
   │   ├── skill-executor.ts   # Execute WASM skills in context
   │   ├── response-renderer.ts # Render results conversationally
   │   └── provider.ts         # z.ai/DeepInfra provider
   ├── skills/
   │   ├── music-tutor.prs     # Music theory tutor example
   │   ├── security.prs        # Security consultant example
   │   └── research.prs        # Research assistant example
   └── package.json
   ```

2. **Implement the agent runtime:**
   ```typescript
   class OpenMindAgent {
     private compiler: Compiler;
     private skillRuntime: SkillRuntime;
     private provider: AIProvider;
     
     async load(prsPath: string): Promise<void> {
       // Compile the .prs file
       const result = await this.compiler.compile(prsPath);
       
       // Extract skill definitions
       const skills = this.extractSkills(result);
       
       // Load WASM modules for each skill
       for (const skill of skills) {
         if (skill.wasmModule) {
           await this.skillRuntime.load(skill.wasmModule);
         }
       }
     }
     
     async respond(userMessage: string): Promise<string> {
       // 1. Check if message triggers a skill
       const triggeredSkill = this.matchTrigger(userMessage);
       
       if (triggeredSkill) {
         // 2. Extract inputs from message
         const inputs = this.extractInputs(userMessage, triggeredSkill);
         
         // 3. Execute WASM skill
         const outputs = await this.skillRuntime.execute(triggeredSkill, inputs);
         
         // 4. Generate conversational response using z.ai
         const response = await this.provider.generate(
           this.buildPrompt(userMessage, outputs, triggeredSkill)
         );
         
         return response;
       }
       
       // No skill triggered — normal conversation
       return this.provider.generate(userMessage);
     }
   }
   ```

3. **Build the music theory tutor demo:**
   - Uses `harmonic-plr` + `tropical-harmony` WASM modules
   - Real-time chord analysis with mathematical backing
   - Conversational output that interprets mathematical results

4. **Build the security consultant demo:**
   - Uses `lattice-crypto` + `fleet-warden` WASM modules
   - Cryptographic posture analysis
   - Fleet health monitoring with anomaly detection

5. **Build the research assistant demo:**
   - Uses `persistent-sheaf` + `wasserstein-agents` WASM modules
   - Topological data analysis
   - Optimal transport computation

**Deliverables:**
- Working Open Mind application
- Three demo agents (music, security, research)
- Each agent uses 2–3 WASM skills in a single conversation
- No code generation — direct WASM execution + conversational interpretation

### Phase 5 (Week 9–12): Self-Improvement Loop

**Goal:** Agent quality improves through spectral feedback.

**Tasks:**

1. **Create `packages/feedback/`:**
   ```
   packages/feedback/
   ├── src/
   │   ├── index.ts
   │   ├── quality-metrics.ts  # Measure output quality
   │   ├── spectral-feedback.ts # Eigenvalue-based feedback
   │   ├── parameter-adjuster.ts # Adjust skill parameters
   │   └── types.ts
   └── package.json
   ```

2. **Implement quality metrics:**
   ```typescript
   interface QualityMetrics {
     userSatisfaction: number;    // Explicit user rating (1-5)
     responseRelevance: number;   // Semantic similarity to expected
     skillExecutionTime: number;  // WASM execution latency
     outputCorrectness: number;   // Mathematical correctness check
     conservationBudget: number;  // Remaining γ after execution
   }
   ```

3. **Implement spectral feedback loop:**
   ```typescript
   class SpectralFeedback {
     private history: QualityMetrics[] = [];
     
     analyze(): FeedbackReport {
       // Build a graph: skill invocations × quality dimensions
       // Compute spectral decomposition
       // Identify high-quality "modes" and low-quality "modes"
       // Recommend parameter adjustments
     }
   }
   ```

4. **Conservation-constrained improvement:**
   ```typescript
   class ConservationConstrainedImprover {
     improve(current: SkillDefinition, feedback: FeedbackReport): SkillDefinition {
       // Each improvement increases entropy H
       // Must keep γ + H ≤ C
       // If budget exhausted, defer improvements to next cycle
       const improvementCost = this.estimateEntropyCost(feedback.adjustments);
       if (this.budget.canAfford(improvementCost)) {
         return this.applyAdjustments(current, feedback.adjustments);
       }
       // Queue for next cycle
       this.queueImprovement(current, feedback.adjustments);
       return current;
     }
   }
   ```

5. **Automated .prs regeneration:**
   - After parameter adjustment, regenerate the `.prs` file with updated values
   - The compiler's conservation tracker ensures regeneration stays within budget
   - User reviews changes before they're committed (red line: no autonomous deployment)

**Deliverables:**
- Feedback collection system (quality metrics per skill invocation)
- Spectral feedback analysis (identify improvement opportunities)
- Conservation-constrained improvement loop (hard cap on change rate)
- Automated `.prs` regeneration with human review gate

---

## Appendix A: File Map

All file paths referenced in this document:

### PromptScript Source (github.com/SuperInstance/promptscript)
| File | Purpose |
|------|---------|
| `packages/compiler/src/compiler.ts` | Pipeline orchestrator — resolve → validate → format |
| `packages/compiler/src/types.ts` | Compiler, formatter, and watcher type definitions |
| `packages/compiler/src/reference-verifier.ts` | Lockfile hash verification |
| `packages/core/src/types/ast.ts` | AST type system (Program, Block, SkillDefinition, etc.) |
| `packages/core/src/types/config.ts` | Configuration types |
| `packages/core/src/types/manifest.ts` | Lockfile manifest types |
| `packages/core/src/types/constants.ts` | Block names, known identifiers |
| `packages/core/src/utils/merge.ts` | deepMerge, deepClone utilities |
| `packages/core/src/errors/` | Error hierarchy (base, parse, resolve, validate) |
| `packages/parser/src/parse.ts` | Entry point: file → AST |
| `packages/parser/src/lexer/lexer.ts` | Token stream generation |
| `packages/parser/src/grammar/parser.ts` | Token stream → AST |
| `packages/parser/src/grammar/visitor.ts` | AST visitor pattern |
| `packages/resolver/src/resolver.ts` | Main resolver: @inherit, @use, @extend |
| `packages/resolver/src/inheritance.ts` | Deep merge for inheritance |
| `packages/resolver/src/imports.ts` | @use import resolution |
| `packages/resolver/src/extensions.ts` | @extend block modification |
| `packages/resolver/src/skill-composition.ts` | Inline @use in @skills → phase composition |
| `packages/resolver/src/guard-requires.ts` | Guard dependency resolution |
| `packages/resolver/src/skills.ts` | Native skill discovery and reference resolution |
| `packages/resolver/src/auto-discovery.ts` | Auto-discover .md files as skills |
| `packages/resolver/src/registry.ts` | FileSystemRegistry, HttpRegistry, CompositeRegistry |
| `packages/resolver/src/git-registry.ts` | Git-based registry |
| `packages/resolver/src/loader.ts` | File loading with registry markers |
| `packages/resolver/src/content-detector.ts` | Content type detection |
| `packages/resolver/src/alias-resolver.ts` | Alias-based URL resolution |
| `packages/validator/src/validator.ts` | Rule engine executor |
| `packages/validator/src/rules/index.ts` | All validation rules (PS001–PS031) |
| `packages/formatters/src/section-registry.ts` | Formatter registration and lookup |
| `packages/formatters/src/convention-renderer.ts` | Shared rendering logic |
| `packages/formatters/src/formatters/*.ts` | 38 agent-specific formatters |
| `packages/formatters/src/formatters/openclaw.ts` | OpenClaw formatter (our current target) |
| `packages/formatters/src/formatters/factory.ts` | Formatter factory |
| `packages/server/src/server.ts` | HTTP compilation server |
| `packages/server/src/watcher.ts` | File watcher for auto-recompilation |
| `packages/browser-compiler/src/compiler.ts` | Browser-compatible compiler |
| `packages/browser-compiler/src/virtual-fs.ts` | In-memory filesystem |
| `packages/browser-compiler/src/resolver.ts` | Browser-compatible resolver |

### New Files to Create
| File | Purpose |
|------|---------|
| `packages/provider/src/zai-provider.ts` | z.ai API client |
| `packages/provider/src/deepinfra-provider.ts` | DeepInfra API client |
| `packages/compiler/src/conservation-tracker.ts` | Conservation law enforcement during compilation |
| `packages/formatters/src/spectral-ranking.ts` | Spectral formatter ranking |
| `packages/resolver/src/ot-merge.ts` | Optimal transport merge for inheritance |
| `packages/validator/src/lattice-signer.ts` | Lattice-based signature for validated ASTs |
| `packages/server/src/fleet-monitor.ts` | Fleet health monitoring via Fleet Warden |
| `packages/scheduler/src/skill-scheduler.ts` | Temporal skill activation via T-Minus |
| `packages/skill-runtime/src/runtime.ts` | WASM skill execution runtime |
| `packages/wasm-runtime/src/index.ts` | WASM module loader and memory manager |
| `packages/feedback/src/spectral-feedback.ts` | Spectral feedback for self-improvement |
| `open-mind/src/agent.ts` | Open Mind agent runtime |

## Appendix B: Crate → Skill Mapping

| Rust Crate | WASM Package | PromptScript Skill | Integration Point |
|------------|-------------|-------------------|-------------------|
| `entropy-conservation` | `@superinstance/entropy-conservation-wasm` | `@superinstance/conservation-tracker` | Compiler pipeline (conservation tracking) |
| `spectral-fleet` | `@superinstance/spectral-fleet-wasm` | `@superinstance/spectral-analysis` | Formatter selection (ranking) |
| `categorical-agents` | `@superinstance/categorical-agents-wasm` | `@superinstance/category-compose` | Skill composition (verification) |
| `wasserstein-agents` | `@superinstance/wasserstein-agents-wasm` | `@superinstance/optimal-transport` | Resolver (merge decisions) |
| `lattice-crypto` | `@superinstance/lattice-crypto-wasm` | `@superinstance/lattice-sign` | Validator (config signing) |
| `harmonic-plr` | `@superinstance/harmonic-plr-wasm` | `@superinstance/harmonic-analysis` | Open Mind demo (music tutor) |
| `tropical-harmony` | `@superinstance/tropical-harmony-wasm` | `@superinstance/tropical-harmonics` | Open Mind demo (music tutor) |
| `persistent-sheaf` | `@superinstance/persistent-sheaf-wasm` | `@superinstance/sheaf-topology` | Open Mind demo (research assistant) |
| `fleet-warden` | `@superinstance/fleet-warden-wasm` | `@superinstance/fleet-monitor` | Server (agent health) |
| `t-minus` | `@superinstance/t-minus-wasm` | `@superinstance/temporal-schedule` | Server (scheduled skills) |

## Appendix C: Conservation Law Enforcement Points

The conservation law γ + H = C is enforced at five points in the integrated system:

1. **Compiler entry**: Total capacity C is set based on AST complexity
2. **After resolve**: Entropy H₁ deducted for resolved nodes, γ₁ = C - H₁
3. **After validate**: Entropy H₂ deducted for validation work, γ₂ = γ₁ - H₂
4. **After format**: Each formatter output carries entropy proportional to output size
5. **Self-improvement**: Each improvement cycle costs entropy; budget caps improvement rate

If at any point γ < γ_min (minimum spectral gap for fleet stability), the system:
- Emits a warning (first occurrence)
- Truncates output (second occurrence)
- Halts compilation (third occurrence — circuit breaker)

This ensures that the compilation process itself is physically constrained, preventing runaway resource consumption in agent configuration generation.

---

*"The .prs file describes what the agent should be. The WASM module computes what it can do. The conversation is what it becomes."*
