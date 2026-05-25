# Template: Multi-Repo CI Addition

## Task Prompt Template

```
Add GitHub Actions CI to these repos. Clone, add workflow, push.

## Repos

### 1. ORG/REPO-NAME
Language: Python
Test runner: pytest

### 2. ORG/REPO-NAME
Language: Rust
Test runner: cargo test

### 3. ORG/REPO-NAME
Language: C
Build: make && make test

### 4. ORG/REPO-NAME
Language: TypeScript
Test runner: npm test

### 5. ORG/REPO-NAME
Language: Go
Test runner: go test ./...

## For each repo
1. gh repo clone ORG/REPO /tmp/REPO -- --depth=1
2. Check if .github/workflows/ exists already (skip if so)
3. Create .github/workflows/ci.yml with appropriate matrix
4. git add .github/ && git commit -m "ci: add GitHub Actions" && git push
```

## CI Templates by Language

### Python
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest
```

### Rust
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cargo test
      - run: cargo clippy -- -D warnings
```

### C
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        cc: [gcc, clang]
    steps:
      - uses: actions/checkout@v4
      - run: make CC=${{ matrix.cc }}
      - run: make test
```

### TypeScript
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm install
      - run: npm test
```
