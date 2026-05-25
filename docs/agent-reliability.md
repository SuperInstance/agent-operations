# Agent Reliability Analysis

## The Problem

When running AI agent swarms on multi-repo projects, agent failure rate is the dominant bottleneck. A 50% failure rate means half your parallelism is wasted — and you don't know which half until after waiting minutes per agent.

## Failure Modes

### Mode 1: Silent Failure (0 Tokens)

**Symptoms:** Agent reports "completed successfully" but used 0 tokens. No output produced.

**Frequency:** ~42% of runs in production data.

**Root Cause (hypothesized):** The model receives the task prompt, begins reasoning about approach, hits a context or reasoning limit during planning, and returns without generating any output. The "success" status comes from the runtime, not the model.

**Triggers observed:**
- Task prompts with meta-instructions (style guides, rules)
- More than 7 repos per agent
- Complex multi-step instructions with branching logic
- Very long task descriptions (>2000 words)

**Mitigation:**
- Keep task prompts under 1000 words
- Use procedural (numbered steps) not descriptive (paragraphs) instructions
- Limit to 5-7 work items per agent
- Separate style/meta concerns from task concerns

### Mode 2: Timeout

**Symptoms:** Agent uses tokens but doesn't finish within the timeout window.

**Frequency:** ~8% of runs.

**Root Cause:** Task is genuinely too large for the allocated time, or the model got stuck in a loop (re-reading files, re-planning).

**Mitigation:**
- Set generous timeouts (10min minimum for multi-repo tasks)
- Break large tasks into smaller chunks
- Monitor token consumption mid-run if possible

### Mode 3: Partial Completion

**Symptoms:** Agent completes some items but not all. May or may not push partial results.

**Frequency:** ~15% of runs.

**Root Cause:** Running out of context, hitting token limits, or losing track of remaining items.

**Mitigation:**
- Explicit checklist in task prompt
- "Push after EACH repo, not at the end"
- Fewer items per agent

## Success Patterns

### What Works

1. **Numbered procedural steps**
   ```
   For each repo:
   1. gh repo clone SuperInstance/REPO /tmp/REPO -- --depth=1
   2. Read ALL source files
   3. Write README.md
   4. git add README.md && git commit -m "docs: README" && git push
   ```

2. **Repetitive identical tasks**
   When every repo gets the same treatment, the agent can parallelize its reasoning.

3. **Concrete examples in the prompt**
   Showing a sample README or output gives the model a template to follow.

4. **Single responsibility per agent**
   One agent does READMEs. Another does CI. Another does descriptions. Don't mix.

### What Doesn't Work

1. **Meta-instructions about quality/style**
   "CRITICAL: Don't use marketing language" — the model reasons about this instead of working.

2. **Template requirements**
   "Each README must have sections 1-10" — adds constraint tracking overhead.

3. **Conditional logic**
   "If the repo has tests, do X, otherwise do Y" — increases cognitive load.

4. **More than 7 items**
   Success rate drops sharply above 7 repos per agent.

## The Task Prompt Formula

```
[ONE SENTENCE: What the agent does]

## Repos (N repos, max 5-7)

### 1. org/repo-name
"GitHub description"
[1-2 sentences about what to do specifically for this repo]

### 2. org/repo-name
...

## Steps (for each repo)
1. Clone
2. [Specific action]
3. [Specific action]
4. Commit and push
```

Total length: 500-1000 words. No style guides. No meta-instructions. No templates.

## Monitoring

Always verify agent output:
```bash
# Check if agent actually pushed
for repo in repo1 repo2 repo3; do
  lines=$(gh api "repos/org/$repo/contents/README.md" --jq '.content' | base64 -d | wc -l)
  echo "$repo: $lines lines"
done
```

## Recovery

When an agent fails:
1. Check token count — 0 tokens means silent failure
2. Check what was pushed — partial output is still valuable
3. Create a new agent with FEWER repos and SIMPLER instructions
4. Never retry the exact same prompt — it'll fail again
