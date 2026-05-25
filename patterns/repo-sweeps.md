# Multi-Repo Sweep Operations

## The Problem

You have 100 repos. You need to upgrade all of them. How do you parallelize this across agents without wasting 50% of them on failures?

## Strategy: Batch Waves

### Wave 1: Assess (Sequential)
Run a single agent (or do it yourself) to categorize all repos:
```bash
for repo in $(gh repo list ORG --limit 100 --json name --jq '.[].name'); do
  lines=$(gh api "repos/ORG/$repo/contents/README.md" --jq '.content' | base64 -d | wc -l)
  lang=$(gh api "repos/ORG/$repo" --jq '.primaryLanguage.name')
  echo "$repo|$lang|$lines"
done
```

Sort into buckets:
- **Needs README** (0-30 lines)
- **Needs improvement** (30-100 lines)  
- **Good enough** (100+ lines)
- **Stub/empty** (no source files)

### Wave 2: Batch by Task Type

Group repos by the SAME task. Don't mix:
```
Agent 1: 5 repos that need CI added
Agent 2: 5 repos that need READMEs written
Agent 3: 5 repos that need descriptions fixed
Agent 4: Deep study of one complex repo
```

**Why same-task batching works:** The agent learns the pattern on repo 1 and applies it faster to repos 2-5. Mixed tasks prevent this learning effect.

### Wave 3: Verify & Fix (Sequential)
```bash
for repo in $(cat wave2-targets.txt); do
  # Check what actually got pushed
  gh api "repos/ORG/$repo/contents/README.md" --jq '.content' | base64 -d | wc -l
done
```

Re-run failed repos individually (not as subagents — direct work).

## Optimal Batch Sizes

From production data:

| Repos per agent | Success rate | Avg runtime |
|----------------|-------------|-------------|
| 1-3 | 95% | 2-3 min |
| 4-5 | 85% | 3-5 min |
| 6-7 | 70% | 5-7 min |
| 8-10 | 40% | 3-8 min (often fails) |
| 10+ | 20% | usually fails |

**Recommendation: 5 repos per agent.** This gives 85% success rate with good throughput.

## Parallelism Limits

Maximum concurrent agents depends on your system:
- **GLM-5.1 (z.ai):** 5 concurrent subagents max
- **Claude Code CLI:** 1 session (session limits apply)
- **Kimi CLI:** 1 tmux session
- **OpenAgent:** depends on deployment

With 5 concurrent agents × 5 repos each = 25 repos per wave. Two waves covers 50 repos in ~10 minutes.

## Failure Recovery Protocol

When an agent fails (0 tokens):

1. **Don't retry the same prompt.** It will fail again.
2. **Reduce scope.** If agent had 8 repos, retry with 4.
3. **Simplify instructions.** Remove style guides, templates, and meta-instructions.
4. **Do it directly.** For 1-2 repos, direct work is faster than debugging the agent.

```bash
# Quick manual README for a single repo
cd /tmp && gh repo clone ORG/repo -- --depth=1 && cd repo
# Study, write, push
```

## Progress Tracking

Maintain a sweep state file:

```json
{
  "wave": 2,
  "total_repos": 100,
  "completed": 60,
  "failed": 12,
  "remaining": 28,
  "failures": [
    {"repo": "org/repo-x", "agent": "wave2-agent3", "reason": "0 tokens"},
    {"repo": "org/repo-y", "agent": "wave2-agent3", "reason": "0 tokens"}
  ]
}
```

This lets you resume after breaks and avoid re-processing completed repos.
