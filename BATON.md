# BATON.md — Agent Handoff Protocol

> **Purpose:** Standardized baton-passing mechanism for multi-agent coordination across the SuperInstance ecosystem (307+ repos, 7 runtime languages, 2000+ tests in sunset-ecosystem alone).

Agents working on SuperInstance projects use batons to claim work, record progress, and hand off cleanly to the next agent — whether that's Claude Code, Kimi, z.ai GLM-5.1, or a human reviewer.

---

## Active Batons

### baton-001: optimal-transport-agents-rs build & Supabase seed
- **Status**: completed
- **Owner**: z.ai GLM-5.1 (session `zai-06-07-1542`)
- **Started**: 2026-06-07T06:00:00Z
- **Updated**: 2026-06-07T09:30:00Z
- **Input**: Build the `optimal-transport-agents-rs` Rust crate — agent coordination primitives using optimal transport theory
- **Output**:
  - Crate compiles on stable Rust 1.82+ with zero warnings
  - 47 unit tests passing (`cargo test --all`)
  - Commit: `a3f1c9e` on `main` at `SuperInstance/optimal-transport-agents-rs`
  - Generated `seed-data.json` with transport matrix fixtures for Supabase
- **Next**: Reseed Supabase `transport_agents` and `agent_coordinates` tables using the generated `seed-data.json`. Run `si-cli db seed --file seed-data.json` and verify row counts match fixture expectations.
- **Handoff-to**: Claude Code — Supabase re-seed and schema validation
- **Blockers**: None
- **Verify**:
  ```bash
  cd optimal-transport-agents-rs && cargo test --all 2>&1 | tail -1  # → "47 passed; 0 failed"
  gh api repos/SuperInstance/optimal-transport-agents-rs/commits/a3f1c9e --jq '.sha'
  wc -l seed-data.json  # → 312 lines
  ```

### baton-002: si-cli Supabase wiring → fleet-api integration
- **Status**: completed
- **Owner**: Kimi-2 (session `kimi-06-07-1100`)
- **Started**: 2026-06-07T04:00:00Z
- **Updated**: 2026-06-07T07:45:00Z
- **Input**: Wire `si-cli` commands (`si agent list`, `si fleet status`, `si deploy`) to Supabase backend, replacing the old REST shim
- **Output**:
  - `si-cli` v0.14.2 published with Supabase client integration
  - New commands: `si db seed`, `si db migrate`, `si agent register`
  - Integration tests passing against staging Supabase instance
  - PR merged: SuperInstance/si-cli#89
- **Next**: Wire `si fleet deploy` output into `fleet-api`'s `/v1/deployments` endpoint. The fleet-api expects the agent manifest format from `si deploy --json`. Update `fleet-api`'s `deploy_handler.rs` to consume the new schema.
- **Handoff-to**: Claude Code — fleet-api integration with new si-cli manifest format
- **Blockers**: `fleet-api` still on old manifest v1 schema; needs migration to v2 (see `si-cli` docs on `--manifest-version`)
- **Verify**:
  ```bash
  si --version  # → "si-cli 0.14.2"
  si agent list --format json | jq '. | length'  # → matches staging agent count
  gh api repos/SuperInstance/si-cli/pulls/89 --jq '.merged'  # → true
  ```

### baton-003: Architecture doc → sunset-ecosystem planning
- **Status**: completed
- **Owner**: Claude Code (session `cc-06-07-0800`)
- **Started**: 2026-06-07T02:00:00Z
- **Updated**: 2026-06-07T05:20:00Z
- **Input**: Write a comprehensive architecture document for the sunset-ecosystem monorepo, covering the 2000+ test suite, language boundaries, and migration path
- **Output**:
  - `ARCHITECTURE.md` committed to `SuperInstance/sunset-ecosystem` main branch
  - Document covers: service topology, language boundary map (Rust/Go/Python/TS), test matrix, and phased migration plan
  - Identified 23 integration points needing test coverage
  - Commit: `d7e4b12` on `main`
- **Next**: Use the architecture doc's migration plan (Phase 1, sections 2-4) to create concrete GitHub issues for the sunset-ecosystem refactor. Break into per-language work streams. Assign first batch of issues to available agents.
- **Handoff-to**: z.ai GLM-5.1 — create sunset-ecosystem refactor issues from architecture doc
- **Blockers**: None — doc is self-contained and actionable
- **Verify**:
  ```bash
  gh api repos/SuperInstance/sunset-ecosystem/contents/ARCHITECTURE.md --jq '.size'  # → >10000 bytes
  grep -c "## " ARCHITECTURE.md  # → 14 sections
  ```

---

## Completed Batons

All three pilot batons (001–003) completed successfully during the 2026-06-07 work session. They serve as reference examples for the baton protocol.

| Baton | Agent | Duration | Result |
|-------|-------|----------|--------|
| baton-001 | z.ai GLM-5.1 | ~3.5h | Crate built, seed data generated, handed off to Supabase |
| baton-002 | Kimi-2 | ~3.75h | si-cli wired to Supabase, handed off to fleet-api |
| baton-003 | Claude Code | ~3.3h | Architecture doc written, handed off to planning |

---

## Baton Rules

1. **CLAIM before you start.** Every agent claims a baton by adding an entry to "Active Batons" with status `in-progress`. Include your agent type, session ID, and a clear description of what you received.

2. **Write OUTPUT + NEXT before you finish.** The output section must contain concrete artifacts (commit SHAs, PR numbers, file paths, test counts). The next section must be a complete task description that a fresh agent session can pick up without context.

3. **Read the previous baton's NEXT field.** When picking up work, the previous baton's `Next` field is your task spec. Reference it in your `Input` field.

4. **Verify step must be concrete.** Provide shell commands, API calls, or test counts — not descriptions. A reviewer or CI job should be able to copy-paste the verify block and get a pass/fail.

5. **Archive when verified.** Move completed batons to "Completed Batons" once the verify step passes. Summarize in the completion table.

6. **One baton per logical task.** Don't bundle unrelated work. If a task spawns sub-tasks for other agents, create separate batons and reference them in `Handoff-to`.

7. **Blockers are mandatory.** If you're stuck, write exactly what's blocking you and what the unblocker needs to provide. Don't silently stall.

8. **Timestamps are ISO 8601 UTC.** Always. No exceptions.

---

## Baton Naming Convention

Format: `baton-NNN: descriptive-kebab-case-name`

- Number sequentially per calendar day (reset daily is fine)
- Name should describe the *output*, not the process
- Examples: `baton-004: fleet-api-deploy-endpoint`, `baton-005: sunset-test-matrix-rust`

---

## Agent Identifiers

| Agent | Identifier | Notes |
|-------|-----------|-------|
| z.ai GLM-5.1 | `zai-YY-MM-DD-HHMM` | Session-based |
| Claude Code | `cc-YY-MM-DD-HHMM` | Session-based |
| Kimi-2 | `kimi-YY-MM-DD-HHMM` | Session-based |
| Human reviewer | `human:<name>` | For manual review batons |

---

## Integration Points

- **GitHub**: Batons reference commits, PRs, and issues via `gh api` commands
- **CI**: Verify blocks should be CI-runnable (no interactive steps)
- **Supabase**: Database-related batons include table names and expected row counts
- **si-cli**: Fleet and agent management batons reference `si` commands

---

## Template

See [`templates/baton-template.md`](templates/baton-template.md) for a blank baton ready to fill in.
