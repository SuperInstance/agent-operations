# Template: Repo README Sweep

Use this template when upgrading READMEs across multiple repos.

## Task Prompt Template

```
Write README.md files for these repos. Clone each, study source, write, push.

## Repos

### 1. ORG/REPO-NAME
"GitHub description here"
Study the source. Document the API with code examples.

### 2. ORG/REPO-NAME
"GitHub description here"  
Study the package. Document installation and usage.

### 3. ORG/REPO-NAME
"GitHub description here"
Study the source. Document key functions.

### 4. ORG/REPO-NAME
"GitHub description here"
Study the crate. Document public API.

### 5. ORG/REPO-NAME
"GitHub description here"
Study the source. Document the protocol.

## For each repo
1. gh repo clone ORG/REPO /tmp/REPO -- --depth=1
2. Read source files (find . -name '*.rs' -o -name '*.py' -o -name '*.c' etc.)
3. Write README.md with: description, features, installation, usage examples, API, related repos
4. git add README.md && git commit -m "docs: engineering README" && git push
```

## Verification Script

```bash
#!/bin/bash
# verify-sweep.sh — Check which repos got updated
for repo in "$@"; do
  lines=$(gh api "repos/ORG/$repo/contents/README.md" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null | wc -l)
  if [ "$lines" -lt 30 ]; then
    echo "NEEDS WORK: $repo ($lines lines)"
  else
    echo "OK: $repo ($lines lines)"
  fi
done
```

## Failure Recovery

If agent fails:
1. Check which repos it completed (run verification script)
2. Create new agent for FAILED repos only
3. Use 3-4 repos instead of 5
4. Simplify instructions further
