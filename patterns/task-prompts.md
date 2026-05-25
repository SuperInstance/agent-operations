# Task Prompt Patterns

## Pattern: Repo Sweep (README Upgrade)

**Success rate:** ~80% with 5-7 repos, ~50% with 8+, ~0% with style guides

### Good Prompt

```
Write README.md files for these repos. Clone each, study source, write, push.

## Repos

### 1. org/repo-a
"Single-header C engine — 250M checks/sec"
Study the C source. Document the API with code examples.

### 2. org/repo-b
"Rust constraint solver with 83 tests"
Study src/lib.rs. Document public API with Rust examples.

### 3. org/repo-c
"Python analysis toolkit"
Study the package. Document installation and usage.

## For each repo
1. gh repo clone org/REPO /tmp/REPO -- --depth=1
2. Read source files
3. Write README.md
4. git add README.md && git commit -m "docs: README" && git push
```

### Bad Prompt (will fail)

```
CRITICAL STYLE GUIDE — READ THIS FIRST:
- DO NOT use marketing language like "production-grade"
- DO NOT make claims — show code examples
- Engineers should have "ah-ha" moments from code, not adjectives
- If you wouldn't write it in an engineering doc, don't write it
- NO "blazing fast" NO "enterprise-ready" NO "production-grade"

Write README.md files for these 8 repos. Each README must have:
1. Name + one-line description + badges
2. What it does — 2-3 paragraphs
3. Key features (bullet list)
4. Installation / Quick Start
5. Usage examples with code
6. Architecture (if complex)
7. API Reference
8. Testing
9. Related repos
10. License

[... 8 repos with descriptions ...]
```

**Why it fails:** The style guide consumes reasoning tokens. The 10-section template adds output planning overhead. 8 repos exceeds the working limit. Total prompt is too long.

## Pattern: Single Deep Task

**Success rate:** ~85%

### Good Prompt

```
Study the EDDI codebase at /tmp/EDDI and write an adaptation plan.

## Key files to study
- src/main/java/ai/labs/eddi/modules/llm/ — LLM provider abstraction
- src/main/java/ai/labs/eddi/engine/a2a/ — Agent-to-agent protocol
- src/main/java/ai/labs/eddi/engine/mcp/ — MCP integration

## Output
Write /tmp/EDDI-ADAPTATION.md with:
1. Architecture analysis
2. Integration plan
3. Concrete steps
4. Example configs

Push to org/docs.
```

### Why This Works
- Single codebase (no context switching)
- Explicit file paths (no exploration needed)
- Structured output (model knows exactly what to produce)
- One output file (simple git operations)

## Pattern: Research & Documentation

**Success rate:** ~90%

### Good Prompt

```
Research X. Study these sources:
- /path/to/file1
- /path/to/file2
- URL (if web access available)

Write findings to /path/to/output.md with:
1. Summary
2. Key findings
3. Recommendations
```

### Why This Works
- Pure information synthesis (no git operations)
- Clear input → output mapping
- No style constraints

## Pattern: Code Generation

**Success rate:** ~70%

### Good Prompt

```
Create a new repo: org/new-repo

Write a Python package that does X. Requirements:
- numpy/scipy only (no sklearn, librosa)
- Every function needs docstrings
- Tests must run in <30 seconds

Create these files:
- src/package/__init__.py
- src/package/module1.py
- tests/test_module1.py
- pyproject.toml

Push to org/new-repo.
```

### Why Code Generation Fails More Often
- More files to track
- Import dependencies between files
- Tests need to actually pass
- Git operations interleaved with code generation

## Anti-Patterns to Avoid

### 1. The Kitchen Sink
```
Do X. Also do Y. And make sure Z. 
By the way, follow style guide A.
Don't forget to check B.
Output must match template C.
```
**Fix:** One task per agent. If you need style + task, use two agents.

### 2. The Vague Directive
```
Upgrade these repos to be better.
```
**Fix:** Be explicit. "Add CI workflow" > "improve CI". "Write 100+ line README with code examples" > "improve docs".

### 3. The Nested Conditional
```
If the repo has Rust code, do X.
If it has Python, do Y.
If it has both, do Z.
For each language, check if tests exist and if so...
```
**Fix:** One agent per condition. Or pre-sort repos and give each agent a homogeneous set.

### 4. The Quality Lecture
```
IMPORTANT: Your output must be excellent.
REMEMBER: Quality over quantity.
CRITICAL: Don't make mistakes.
```
**Fix:** Delete all of these. They consume tokens and don't improve output quality. Show what you want with examples instead.
