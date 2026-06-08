# Fleet CI/CD Strategy

**Date:** 2026-06-07  
**Scope:** 307+ SuperInstance repositories across 7 language stacks  
**Current state:** Only `sunset-ecosystem` has comprehensive CI. 21 Rust crates, si-runtime-go, and most other repos have zero workflows.  
**Goal:** Every repo gets CI without every repo getting a custom workflow. Shared callable templates in this repo; individual repos call them with two lines.

---

## Table of Contents

1. [CI Matrix by Repo Type](#1-ci-matrix-by-repo-type)
2. [Shared Workflow Templates](#2-shared-workflow-templates)
3. [Fleet-Wide Test Counting and Reporting](#3-fleet-wide-test-counting-and-reporting)
4. [Release Coordination](#4-release-coordination)
5. [si-cli CI Audit](#5-si-cli-ci-audit)
6. [Rollout Sequence](#6-rollout-sequence)
7. [Secrets and Configuration](#7-secrets-and-configuration)

---

## 1. CI Matrix by Repo Type

### 1.1 Current Landscape

From a survey of repos with local clones + the org auto-index:

| Language | Build System | Example Repos | Local Clone Count | Has CI |
|----------|-------------|---------------|-------------------|--------|
| Rust | `cargo` | conservation-law-rs, spectral-fleet-rs, si-runtime-go (Cargo embedded), open-tui | 21 | 1 (open-tui only) |
| Python | `pyproject.toml` / `pytest` | sunset-ecosystem, open-mind | 2+ | 1 (sunset only) |
| Go | `go.mod` / `go test` | si-runtime-go | 1 | 0 |
| TypeScript/Node | `package.json` / `npm test` | schemas, open-application | 2+ | 0 |
| Zig | `build.zig` / `zig build test` | deadband-zig, si-runtime-zig | 0 (planned) | 0 |
| C | `Makefile` / `make test` | si-core-c, nerve/ bloom_filter | 0 (embedded) | 0 |
| WASM | `wasm-pack` | si-runtime-wasm, any Rust→WASM target | 0 (planned) | 0 |

Estimated 307+ repos total based on org auto-index. Breakdown by language at that scale:
- ~180 Rust crates (the 58+ published crates + wave repos + lau-* + others)
- ~60 Python repos
- ~20 TypeScript/Node repos
- ~15 Go repos
- ~10 C repos
- ~7 Zig repos (planned)
- ~15 multi-language or mixed

### 1.2 CI Job Matrix

What each language stack needs, and what level of strictness to apply.

```
TIER A — Required to merge (blocking)
TIER B — Run on push, non-blocking (warning on failure)
TIER C — Weekly scheduled only
```

#### Rust (`cargo`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `cargo test` | A | `cargo test --all-features` | Core correctness |
| `cargo clippy` | A | `cargo clippy -- -D warnings` | Lint as error |
| `cargo fmt --check` | A | — | Format gate |
| `cargo deny check` | A | licenses + advisories | Security |
| `cargo doc` | B | `RUSTDOCFLAGS=-Dwarnings cargo doc` | No broken docs |
| `cargo test --no-default-features` | B | — | Catch feature flag bugs |
| MSRV check | B | `cargo check` on `rust-version` from Cargo.toml | Compatibility |
| WASM build (if `wasm32` target in Cargo.toml) | B | `cargo build --target wasm32-unknown-unknown` | |
| `cargo-machete` (unused deps) | C | — | Keep Cargo.toml clean |
| `cargo audit` | C | — | Supply chain |

#### Python (`pyproject.toml` + `pytest`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `pytest` | A | `pytest -q --tb=short` | Core correctness |
| `ruff check` | A | — | Fast linter |
| `mypy` | B | `--ignore-missing-imports` | Type check |
| `bandit` | B | `-ll` (low severity threshold) | Security |
| `pip-audit` | C | — | Dependency CVEs |
| Coverage | B | `--cov-fail-under=70` | Don't let coverage regress |

#### Go (`go.mod`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `go test ./...` | A | `-race -count=1` | Race detector on |
| `go vet ./...` | A | — | Basic static analysis |
| `staticcheck` | B | — | `honnef.co/go/tools` |
| `go build ./...` | A | — | Compilation gate |
| `golangci-lint` | B | — | Comprehensive lint |

#### TypeScript/Node (`package.json`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `npm test` | A | — | Core correctness |
| `npm run build` | A | — | TypeScript compile |
| `npm run lint` | B | `eslint` / `biome` | Lint |
| `npm audit` | C | `--audit-level=high` | CVEs |

#### Zig (`build.zig`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `zig build test` | A | — | Core correctness |
| `zig build` | A | — | Compilation gate |
| `zig fmt --check` | A | — | Format gate |

#### C (`Makefile`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `make test` | A | — | Core correctness |
| `make build` | A | — | Compilation gate |
| `valgrind` (Linux) | B | `--error-exitcode=1` | Memory safety |
| `cppcheck` | B | — | Static analysis |
| `clang-format --check` | B | — | Format |

#### WASM (`wasm-pack`)

| Job | Tier | Command | Notes |
|-----|------|---------|-------|
| `wasm-pack build` | A | `--target web` | Build gate |
| `wasm-pack test --headless --chrome` | A | — | Browser test |
| `wasm-pack test --node` | B | — | Node environment |
| Size check | B | `wasm-opt` output < 500KB | Bundle size budget |

### 1.3 Decision Table: Which Template Does a Repo Use?

```
Does repo have Cargo.toml at root?
  YES → use rust-ci.yml
    Does it also have wasm32 in [lib] targets or Cargo.toml features?
      YES → also add wasm step (flag: enable_wasm: true)
    Does it have pyproject.toml too?
      YES → add python step (flag: enable_python: true)
  
  Does repo have pyproject.toml (no Cargo.toml)?
    YES → use python-ci.yml

  Does repo have go.mod?
    YES → use go-ci.yml

  Does repo have build.zig?
    YES → use zig-ci.yml

  Does repo have package.json (no Cargo.toml)?
    YES → use node-ci.yml

  Does repo have Makefile + .c files?
    YES → use c-ci.yml
```

Apply this decision tree with `discover_integrations.py` extended to emit a CI template recommendation per repo.

---

## 2. Shared Workflow Templates

All templates live in `agent-operations/.github/workflows/` and are called via
`workflow_call` trigger. Individual repos reference them with two lines:

```yaml
# <individual-repo>/.github/workflows/ci.yml
jobs:
  ci:
    uses: SuperInstance/agent-operations/.github/workflows/rust-ci.yml@master
    secrets: inherit
```

That is the entire file for a simple Rust crate. No duplication.

### 2.1 Inputs and Outputs (all templates)

Every template accepts these standard inputs:

| Input | Type | Default | Purpose |
|-------|------|---------|---------|
| `report_to_fleet` | boolean | `true` | Push test results to `fleet_events` |
| `fleet_registry_url` | string | `""` | Supabase DSN (from secret if empty) |
| `min_coverage` | number | `70` | Coverage threshold (Python) |
| `rust_toolchain` | string | `stable` | Rust toolchain version |
| `python_version` | string | `"3.12"` | Python version |
| `go_version` | string | `"stable"` | Go toolchain |
| `enable_security` | boolean | `true` | Run security scans |
| `enable_wasm` | boolean | `false` | Add WASM build step |

Every template emits these outputs (consumed by `fleet-report.yml`):

| Output | Type | Meaning |
|--------|------|---------|
| `test_count` | number | Tests collected and run |
| `test_passed` | number | Tests that passed |
| `test_failed` | number | Tests that failed |
| `coverage_pct` | number | Line coverage 0–100 |
| `repo_name` | string | `${{ github.repository }}` |
| `run_id` | string | `${{ github.run_id }}` |

### 2.2 Template: `rust-ci.yml`

See `.github/workflows/rust-ci.yml` in this repo for the full file.

Key design decisions:
- Uses `Swatinem/rust-cache@v2` — fastest available Rust cache action
- `dtolnay/rust-toolchain` pinned over `actions-rs/toolchain` (maintained)
- `cargo deny check` split into two matrix legs (advisories + licenses) so a new advisory advisory doesn't block a PR
- MSRV read from `rust-version` in Cargo.toml — no hardcoded version
- Test count extracted via `cargo test -- --list 2>&1 | grep "test$" | wc -l` before running

### 2.3 Template: `python-ci.yml`

See `.github/workflows/python-ci.yml`.

Key decisions:
- `uv` for dependency install (10× faster than pip on cold cache)
- `pytest-json-report` for machine-readable test output → fleet reporting
- `ruff` replaces flake8 + isort + pyupgrade (one tool, one install)
- Coverage via `pytest-cov` with XML output for Codecov AND for fleet counting

### 2.4 Template: `go-ci.yml`

See `.github/workflows/go-ci.yml`.

Key decisions:
- `-race` flag on all test runs (catches data races that plague Go agent code)
- `golangci-lint` v1.60+ with `.golangci.yml` config included in template
- Go version from `go.mod` via `actions/setup-go@v5` auto-detection

### 2.5 Template: `node-ci.yml`

See `.github/workflows/node-ci.yml`.

Key decisions:
- pnpm preferred over npm (faster, deterministic)
- TypeScript checked via `tsc --noEmit` separate from `npm test`
- Schema repos: add `ajv` JSON schema validation step

### 2.6 Template: `zig-ci.yml`

See `.github/workflows/zig-ci.yml`.

Key decisions:
- Pin Zig version via `mlugg/setup-zig@v1` (not system Zig — too old)
- `zig build test --summary all` for test count output
- Cache `zig-cache/` and `~/.cache/zig`

### 2.7 Template: `c-ci.yml`

See `.github/workflows/c-ci.yml`.

Key decisions:
- Build matrix: gcc + clang (catches compiler-specific warnings)
- AddressSanitizer (`-fsanitize=address`) on Linux for memory safety
- `cppcheck --error-exitcode=1` blocks on errors, warns on style
- Valgrind only on Linux (not macOS — too slow in CI)

### 2.8 Template: `wasm-ci.yml`

See `.github/workflows/wasm-ci.yml`.

Key decisions:
- Build via `wasm-pack build --target web` and `--target bundler`
- Test via `wasm-pack test --headless --chrome` (Chrome installed on ubuntu-latest)
- `wasm-opt` size check: fail if `.wasm` output exceeds 500KB (configurable)
- Report: extract test count from wasm-pack JSON output

### 2.9 Template: `fleet-report.yml`

See `.github/workflows/fleet-report.yml`.

The reporting template is called by other templates as a final step. It:
1. Collects test counts, coverage, pass/fail from prior job outputs
2. Inserts a `fleet_events` record with `event_type='ci_run'`
3. Updates `repos.health_status` based on result

---

## 3. Fleet-Wide Test Counting and Reporting

### 3.1 The Problem

At 307+ repos, you need to know: "How many tests does the fleet run in total? Did that go up or down this week?" The answer isn't in any one place. It's the sum across all repos' CI runs.

### 3.2 The Schema (extending SUPERINSTANCE_RUNTIME.md §5)

Add two columns to `repos`:

```sql
ALTER TABLE repos
  ADD COLUMN last_ci_run_at   TIMESTAMPTZ,
  ADD COLUMN last_test_count  INTEGER DEFAULT 0,
  ADD COLUMN last_test_passed INTEGER DEFAULT 0,
  ADD COLUMN last_coverage    FLOAT4  DEFAULT NULL;

-- View: fleet-wide test health
CREATE VIEW fleet_test_health AS
SELECT
  language,
  COUNT(*)                           AS repo_count,
  SUM(last_test_count)               AS total_tests,
  SUM(last_test_passed)              AS total_passing,
  ROUND(AVG(last_coverage)::numeric, 1) AS avg_coverage_pct,
  COUNT(*) FILTER (WHERE health_status = 'green') AS green_repos,
  COUNT(*) FILTER (WHERE last_ci_run_at IS NULL)  AS no_ci_repos
FROM repos
GROUP BY language
ORDER BY total_tests DESC;
```

Fleet-wide total test query:
```sql
SELECT SUM(last_test_count) AS fleet_total_tests,
       SUM(last_test_passed) AS fleet_passing,
       ROUND(100.0 * SUM(last_test_passed) / NULLIF(SUM(last_test_count), 0), 1) AS pass_rate_pct
FROM repos
WHERE last_ci_run_at > now() - interval '7 days';
```

### 3.3 The `fleet_events` CI Record

Each CI run emits one record:

```sql
-- Inserted by fleet-report.yml after every CI run
INSERT INTO fleet_events (event_type, agent_id, vessel_id, payload, severity)
VALUES (
  'ci_run',
  'ci:SuperInstance/<repo-name>',
  'github-actions',
  jsonb_build_object(
    'repo',         'SuperInstance/conservation-law-rs',
    'branch',       'main',
    'run_id',       '12345678',
    'trigger',      'push',             -- push | pull_request | schedule
    'language',     'Rust',
    'test_count',   42,
    'test_passed',  42,
    'test_failed',  0,
    'coverage_pct', 87.3,
    'duration_s',   124,
    'workflow',     'rust-ci.yml',
    'status',       'success'           -- success | failure | cancelled
  ),
  CASE WHEN test_failed > 0 THEN 'error' ELSE 'info' END
);
```

### 3.4 The Fleet Report Script

`tools/fleet-test-report.py` — runs as a scheduled workflow (weekly) or on-demand via `si fleet audit --ci`:

```python
#!/usr/bin/env python3
"""Generate fleet-wide CI health report from fleet_events + repos tables."""

import os
import psycopg2
from datetime import datetime, timedelta

def fleet_ci_report(days: int = 7) -> dict:
    dsn = os.environ["SUPERINSTANCE_REGISTRY_URL"]
    since = datetime.utcnow() - timedelta(days=days)

    with psycopg2.connect(dsn) as conn:
        with conn.cursor() as cur:
            # Fleet-wide totals
            cur.execute("""
                SELECT
                    COUNT(DISTINCT r.name)        AS repos_with_ci,
                    SUM(r.last_test_count)        AS total_tests,
                    SUM(r.last_test_passed)       AS total_passing,
                    ROUND(AVG(r.last_coverage)::numeric, 1) AS avg_coverage
                FROM repos r
                WHERE r.last_ci_run_at > %s
            """, (since,))
            totals = cur.fetchone()

            # Repos with no CI
            cur.execute("""
                SELECT name, language, health_status
                FROM repos
                WHERE last_ci_run_at IS NULL
                   OR last_ci_run_at < %s
                ORDER BY language, name
            """, (since,))
            no_ci = cur.fetchall()

            # Recent failures
            cur.execute("""
                SELECT agent_id, payload->>'status', occurred_at
                FROM fleet_events
                WHERE event_type = 'ci_run'
                  AND payload->>'status' = 'failure'
                  AND occurred_at > %s
                ORDER BY occurred_at DESC
                LIMIT 20
            """, (since,))
            failures = cur.fetchall()

    return {
        "period_days": days,
        "totals": totals,
        "repos_without_recent_ci": no_ci,
        "recent_failures": failures,
    }
```

### 3.5 Fleet Test Count Targets

| Date | Target Total Tests | Notes |
|------|-------------------|-------|
| Now (2026-06-07) | ~2,500 | Only sunset (2215) + a few others |
| After Rust CI rollout (Week 3) | ~3,500 | +~1,000 from 21 Rust crates |
| After Python + Go CI (Week 5) | ~4,000 | |
| After all stacks (Week 8) | ~5,000+ | |
| 6-month target | ~10,000 | As new crates are extracted |

The fleet test count is a lagging indicator of ecosystem health. A week where count drops is a week where tests were deleted without replacement — worth investigating.

---

## 4. Release Coordination

### 4.1 The Problem

At 307+ repos spanning crates.io, PyPI, and npm:
- crates.io rate-limits: 1 publish per 10 minutes per user account
- PyPI: no publish rate limit, but needs per-package token or trusted publisher
- npm: needs org token with `publish` scope

Publishing all 180 Rust crates serially takes 30 hours. Publishing in parallel hits rate limits.

### 4.2 Release Workflow: Rust Crates (`release-rust.yml`)

See `.github/workflows/release-rust.yml`.

**Strategy: dependency-ordered batch publish**

```
Layer 0 (no SI deps):    conservation-law-rs, spectral-fleet-rs, categorical-agents-rs
Layer 1 (deps on L0):    entropy-conservation-rs (deps: conservation-law-rs)
Layer 2 (deps on L0+L1): wasserstein-agents-rs, witness-topology-rs
...
```

Compute layers with `discover_integrations.py --emit-publish-order`. Each layer publishes in parallel; layers are serialized with `needs:` in the workflow.

Within a layer, rate-limit with a sleep:
```yaml
- name: Publish with rate limiting
  run: |
    cargo publish --no-verify
    sleep 600  # 10 minutes between publishes in same account
```

For the 180-crate scenario, with 5 crates per layer average:
- 36 layers × (publish + 10min sleep) ≈ 6 hours per account
- With 3 bot accounts: ≈ 2 hours total

**Versioning rule:** All SI crates share a version epoch. Major version bumps require a fleet-wide release meeting. Minor/patch: individual crate maintainers decide.

**Tag format:** `<repo-name>/v<semver>` — allows one repo to have multiple crates released independently.

```yaml
# Individual repo calls this:
# .github/workflows/release.yml
on:
  push:
    tags:
      - "v*"
jobs:
  release:
    uses: SuperInstance/agent-operations/.github/workflows/release-rust.yml@master
    with:
      crate_name: conservation-law
      layer: 0           # no SI deps — publish immediately
    secrets: inherit
```

### 4.3 Release Workflow: Python Packages (`release-python.yml`)

See `.github/workflows/release-python.yml`.

**Strategy: trusted publisher (OIDC) — no long-lived tokens**

```yaml
# Uses GitHub's OIDC identity — no PYPI_API_TOKEN needed
- uses: pypa/gh-action-pypi-publish@release/v1
  with:
    attestations: true   # PEP 740 attestations for supply chain
```

Set up once per PyPI project: `pypi.org → Project → Publishing → GitHub Actions`.

**Order for multi-package repos:** If a repo ships multiple packages (e.g., `agent-lifecycle-py` + `fleet-journal-py` from sunset extraction), publish in dependency order. Script: `uv pip tree --invert | python tools/publish-order.py`.

### 4.4 Release Workflow: npm Packages (`release-node.yml`)

See `.github/workflows/release-node.yml`.

**Strategy: npm provenance + org token**

```yaml
- run: npm publish --provenance --access public
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

npm provenance (SLSA Level 3) links the published package to the GitHub Actions run. Required for `@superinstance/` scoped packages.

### 4.5 Cross-Language Version Synchronization

When a C ABI function changes in `superinstance-ffi`:
1. Bump `superinstance-ffi` Rust crate (triggers crates.io publish)
2. Bump `sunset-ecosystem` Python dep on FFI (triggers PyPI publish)  
3. Bump `@superinstance/keeper-beacon` npm if TypeScript types changed

This cascade is manual today. Automate with `tools/version-cascade.py`:

```python
# tools/version-cascade.py
# Given a changed repo + semver bump type (patch|minor|major),
# compute the set of repos that need version bumps and in what order.
# Uses CAPABILITY.toml [requires] sections to walk the dependency graph.

def cascade_bumps(root_repo: str, bump_type: str) -> list[tuple[str, str]]:
    """Return ordered list of (repo, bump_type) to update."""
    ...
```

### 4.6 Release Checklist (added to each release PR)

```markdown
## Release Checklist

- [ ] CHANGELOG.md entry written (what changed, why)
- [ ] CAPABILITY.toml version updated
- [ ] `cargo publish --dry-run` passes (Rust)
- [ ] `python -m build && twine check dist/*` passes (Python)
- [ ] All tests green on main
- [ ] No `cargo deny` license violations
- [ ] fleet_events record will be emitted by release workflow
- [ ] Downstream repos notified if API changed (list: `si cap dependents <repo>`)
```

---

## 5. si-cli CI Audit

### 5.1 Command Surface

```bash
# Show CI status across all registered fleet repos
si fleet audit --ci

# Output:
# Fleet CI Status (as of 2026-06-07 22:00 UTC)
# ═══════════════════════════════════════════════
# Repos with CI:      127 / 307 (41%)
# Fleet total tests:  4,832 (↑ 312 from last week)
# Fleet pass rate:    98.7%
# Repos failing CI:   3
# Repos with no CI:   180 (see: si fleet audit --ci --missing)
#
# Failing:
#   ✗ SuperInstance/entropy-conservation-rs  — last run 2h ago — 2 failures
#   ✗ SuperInstance/flux-sdk-python          — last run 4h ago — import error
#   ✗ SuperInstance/lau-banach-agents        — last run 1d ago — timeout

# List repos with no CI workflows
si fleet audit --ci --missing --language Rust

# Repos missing CI (Rust, 163 repos):
#   SuperInstance/conservation-law-rs  (21 tests in last local run)
#   SuperInstance/spectral-fleet-rs    (38 tests)
#   ...

# Add CI to a specific repo
si fleet ci add --repo SuperInstance/conservation-law-rs
# → creates PR in that repo with .github/workflows/ci.yml calling rust-ci.yml

# Show test count trend for the fleet
si fleet audit --ci --trend --days 30

# Show per-language breakdown
si fleet audit --ci --by-language
```

### 5.2 How `si fleet audit --ci` Works

The command queries two sources:

**Source 1: GitHub API** (live CI status)
```python
# For each registered repo in fleet_registry:
result = gh.get(f"/repos/{repo}/actions/runs",
                params={"per_page": 1, "status": "completed"})
# → last run status, timestamp, test counts (if fleet-report.yml was run)
```

**Source 2: Supabase** (historical test counts)
```python
# Fleet-wide summary from repos table + fleet_events
rows = conn.execute("""
    SELECT r.name, r.language, r.last_ci_run_at,
           r.last_test_count, r.last_test_passed,
           r.health_status
    FROM repos r
    ORDER BY r.last_ci_run_at DESC NULLS LAST
""").fetchall()
```

**Missing CI detection:**
```python
# A repo "has CI" if it has at least one workflow file with
# a ci_run event in fleet_events within the last 30 days
# OR has .github/workflows/*.yml files visible via GitHub API
def has_ci(repo_name: str) -> bool:
    workflows = gh.get(f"/repos/{repo_name}/actions/workflows")
    return workflows["total_count"] > 0
```

### 5.3 `si fleet ci add` — Auto-PR Generator

When a repo has no CI, `si fleet ci add` generates and opens a PR with the correct template call:

```python
def generate_ci_pr(repo_name: str, detected_language: str) -> str:
    """Generate .github/workflows/ci.yml content for a repo."""
    template_map = {
        "Rust":       "rust-ci.yml",
        "Python":     "python-ci.yml",
        "Go":         "go-ci.yml",
        "TypeScript": "node-ci.yml",
        "Zig":        "zig-ci.yml",
        "C":          "c-ci.yml",
    }
    template = template_map.get(detected_language, "rust-ci.yml")

    return f"""name: CI
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
jobs:
  ci:
    uses: SuperInstance/agent-operations/.github/workflows/{template}@master
    secrets: inherit
"""
```

The PR title: `ci: add CI via fleet shared workflow ({language})`.  
The PR body links back to this plan document.

### 5.4 CI Status as Fleet Health Signal

CI status is a first-class fleet health signal, alongside conservation budget and spectral eigenvalues. When `si fleet audit` runs:

1. Repos with failing CI → `fleet_events` INSERT (`event_type='ci_failure'`, `severity='warn'`)
2. Repos with no CI for >7 days → `fleet_events` INSERT (`event_type='ci_missing'`, `severity='info'`)  
3. Test count drop >10% from prior week → `fleet_events` INSERT (`event_type='test_regression'`, `severity='warn'`)

These events appear in the fleet's circuit-breaker logic: a repo with 3 consecutive `ci_failure` events automatically has its `health_status` set to `'yellow'` in the `repos` table.

### 5.5 Fleet CI Dashboard (Tide Pool Integration)

The `TidePoolVisualizer` in sunset-ecosystem already renders ASCII and HTML fleet health. Add CI status to `FleetSnapshot`:

```python
@dataclass
class FleetSnapshot:
    # ... existing fields ...
    ci_pass_rate: float      # fleet-wide CI pass rate 0-1
    ci_total_tests: int      # sum of last_test_count across all repos
    repos_failing_ci: int    # count of repos with failed last CI run
    repos_missing_ci: int    # count of repos with no CI workflow
```

The tide pool bioluminescent display: repos with failing CI render in red; repos missing CI render in grey; green = CI passing.

---

## 6. Rollout Sequence

Ordered by value per effort-day. Each phase is independently shippable.

### Phase 1 — Templates live, sunset calling them (Week 1)

- [x] Create shared workflow templates in this repo (done in this PR)
- [ ] Update `sunset-ecosystem/.github/workflows/ci.yml` to call `python-ci.yml` instead of inline steps
- [ ] Verify: sunset CI still passes after migration
- [ ] Add `fleet-report.yml` call at end of sunset CI
- [ ] Verify: `fleet_events` gets a `ci_run` record after sunset push

**Done signal:** `SELECT event_type FROM fleet_events WHERE event_type='ci_run' LIMIT 1` returns a row.

### Phase 2 — Rust crates get CI (Week 2-3)

Priority order based on Layer 0 (no SI deps first):

1. `conservation-law-rs` (33 tests, Layer 0)
2. `spectral-fleet-rs` (38 tests, Layer 0)
3. `categorical-agents-rs` (Layer 0)
4. `t-minus-rs` (Layer 0)
5. `entropy-conservation-rs` (Layer 1)
6. `wasserstein-agents-rs` (Layer 2)
7. ... remaining 15 Rust crates

Use `si fleet ci add` to batch-generate PRs. Merge 3-4 per day to avoid CI queue saturation.

**Done signal:** `SELECT SUM(last_test_count) FROM repos WHERE language='Rust'` > 1000.

### Phase 3 — Go and Node CI (Week 4)

- `si-runtime-go`: `go-ci.yml` with `-race` flag
- `schemas` package: `node-ci.yml` with TypeScript check
- `open-application` (Tauri): Rust + Node hybrid; use both templates

**Done signal:** `si-runtime-go` CI passes with race detector enabled.

### Phase 4 — Release automation (Week 5-6)

- Set up crates.io CARGO_REGISTRY_TOKEN secret (org level)
- Set up PyPI trusted publisher for `sunset-ecosystem` and extracted packages
- Set up npm token for `@superinstance/` scope
- Publish first fully-automated release: `conservation-law` 0.1.1

**Done signal:** `cargo add conservation-law` installs 0.1.1 from crates.io.

### Phase 5 — C and Zig CI (Week 7-8)

- `si-core-c`: `c-ci.yml` with gcc + clang matrix
- `deadband-zig` (when created): `zig-ci.yml`
- WASM builds for conservation-law-rs and spectral-fleet-rs

**Done signal:** `si fleet audit --ci --by-language` shows all 7 stacks with at least one green repo.

### Phase 6 — Fleet-wide test count target 10,000 (Month 3)

- `si fleet ci add --batch --missing --language Rust` to catch all remaining crates
- Weekly cron report sent to fleet_events
- `TidePoolVisualizer` updated with CI status overlay

---

## 7. Secrets and Configuration

### 7.1 Required Secrets (org-level in GitHub)

Set at `github.com/organizations/SuperInstance/settings/secrets/actions`:

| Secret | Used By | Notes |
|--------|---------|-------|
| `SUPERINSTANCE_REGISTRY_URL` | `fleet-report.yml` | Supabase DSN with write perms to repos + fleet_events |
| `CARGO_REGISTRY_TOKEN` | `release-rust.yml` | crates.io publish token. One token per publish account. |
| `NPM_TOKEN` | `release-node.yml` | npm org token with `publish` scope |
| `CODECOV_TOKEN` | `rust-ci.yml`, `python-ci.yml` | Coverage upload (optional but recommended) |

PyPI: use trusted publisher (no secret needed after initial setup).

### 7.2 No Per-Repo Secrets Needed

The "call shared workflow + `secrets: inherit`" pattern passes org-level secrets automatically. Individual repos do not need to be configured with any secrets. This is the key operational advantage of the callable workflow approach.

### 7.3 Concurrency Limits

GitHub-hosted runners: 20 concurrent jobs on free tier, 60+ on paid.

With 307 repos all pushing at once (unlikely but possible), job queue saturation is a real concern. Mitigate:
- Use `concurrency:` groups on all templates (already done: `group: ${{ github.workflow }}-${{ github.head_ref || github.run_id }}`)
- Self-hosted runner on Oracle1 for fleet-internal repos (the fleet's own hardware running the fleet's own CI is appropriate)
- `fleet-report.yml` runs last and is always `continue-on-error: true` so it never blocks a merge

### 7.4 Self-Hosted Runner Setup (Oracle1)

```yaml
# In any workflow that should use Oracle1:
jobs:
  ci:
    uses: SuperInstance/agent-operations/.github/workflows/rust-ci.yml@master
    with:
      runner: self-hosted  # add this input to rust-ci.yml
    secrets: inherit
```

Runner registration:
```bash
# On oracle1:
mkdir actions-runner && cd actions-runner
curl -O -L https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-arm64-2.323.0.tar.gz
tar xzf ./actions-runner-linux-arm64-2.323.0.tar.gz
./config.sh --url https://github.com/SuperInstance --token <ORG_RUNNER_TOKEN>
sudo ./svc.sh install && sudo ./svc.sh start
```

The ARM64 Ampere Altra on Oracle1 runs Rust/Go/Python builds 2-3× faster than GitHub-hosted x86-64 runners for compute-intensive crates. Use it for: conservation-law-rs (proptest fuzzing is slow on x86), spectral-fleet-rs (matrix operations), and sunset-ecosystem benchmarks.

---

## Appendix A: Workflow Template Locations

```
agent-operations/.github/workflows/
├── rust-ci.yml          # Rust: cargo test + clippy + fmt + deny
├── python-ci.yml        # Python: pytest + ruff + mypy + bandit
├── go-ci.yml            # Go: go test -race + vet + golangci-lint
├── node-ci.yml          # Node/TS: npm test + tsc + eslint
├── zig-ci.yml           # Zig: zig build test + fmt check
├── c-ci.yml             # C: make test + valgrind + cppcheck
├── wasm-ci.yml          # WASM: wasm-pack build + test + size check
├── release-rust.yml     # crates.io publish with dependency ordering
├── release-python.yml   # PyPI publish via OIDC trusted publisher
├── release-node.yml     # npm publish with provenance
└── fleet-report.yml     # Push test results to Supabase fleet_events
```

## Appendix B: Per-Repo CI File (Two-Line Pattern)

Once the templates are in place, every repo's CI file is:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
jobs:
  ci:
    uses: SuperInstance/agent-operations/.github/workflows/rust-ci.yml@master
    secrets: inherit
```

For a repo that needs both Rust and Python:
```yaml
jobs:
  rust:
    uses: SuperInstance/agent-operations/.github/workflows/rust-ci.yml@master
    secrets: inherit
  python:
    uses: SuperInstance/agent-operations/.github/workflows/python-ci.yml@master
    secrets: inherit
```

The `needs:` keyword is not required — both run in parallel.

## Appendix C: Test Count Extraction by Language

How the fleet-report script counts tests (used in fleet_events payload):

| Language | Command | Parse |
|----------|---------|-------|
| Rust | `cargo test -- --list 2>&1 \| grep ': test$' \| wc -l` | integer from stdout |
| Python | `pytest --collect-only -q 2>&1 \| tail -1` | `"N tests collected"` |
| Go | `go test -v ./... 2>&1 \| grep -c '^--- '` | count of `--- PASS` + `--- FAIL` lines |
| Node | `jest --listTests 2>&1 \| wc -l` or `npm test -- --reporter=json \| jq '.numTotalTests'` | integer |
| Zig | `zig build test --summary all 2>&1 \| grep 'tests passed'` | parse `"N/M tests passed"` |
| C | `make test 2>&1 \| grep -c 'PASS'` | count PASS lines (convention: each test prints PASS/FAIL) |
| WASM | `wasm-pack test --headless --chrome -- --reporter json 2>&1 \| jq '.numTests'` | integer |
