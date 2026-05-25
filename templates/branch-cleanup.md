# Template: Branch Cleanup Sweep

## Task Prompt Template

```
Clean up stale branches across these repos. Merge what can be merged, delete what's stale.

## Repos

### 1. ORG/REPO-NAME
Main branch: main

### 2. ORG/REPO-NAME
Main branch: main

### 3. ORG/REPO-NAME
Main branch: master

### 4. ORG/REPO-NAME
Main branch: main

### 5. ORG/REPO-NAME
Main branch: main

## For each repo
1. gh repo clone ORG/REPO /tmp/REPO
2. List branches: git branch -r
3. For each non-main branch:
   a. Try: git checkout main && git merge origin/BRANCH
   b. If conflict: resolve by keeping both sides (union approach)
   c. If branch is clearly stale (>30 days, no unique commits): delete
4. git push origin main
5. Delete merged branches: git push origin --delete BRANCH
6. Report what was merged and what was deleted
```

## Verification

```bash
# After sweep, check branch counts
for repo in "$@"; do
  count=$(gh api "repos/ORG/$repo/branches" --jq 'length' 2>/dev/null)
  echo "$repo: $count branches"
done
```

## Conflict Resolution Strategy

For SuperInstance repos, use the **union approach**:
- Keep both sides of conflicts
- Never delete code from either branch
- If in doubt, keep both versions (the unused one can be removed later)
