# Contributing

## GitHub Flow

### Workflow

1. **Create branch** from `main`
2. **Make changes** and commit
3. **Open Pull Request**
4. **Code review** and discussion
5. **Merge** to `main`

### Commands

```bash
# Create feature branch
git checkout -b feature/add-items-endpoint

# Make changes and commit
git add .
git commit -m "feat: add items endpoint"

# Push and create PR
git push -u origin feature/add-items-endpoint
gh pr create --title "Add items endpoint" --body "Description"

# After approval
gh pr merge --squash
```

### Branch Naming

| Prefix | Purpose |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `refactor/` | Code refactoring |
| `docs/` | Documentation |

### Commit Messages

Format:
```
<type>: <short description>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

Examples:
- `feat: add user authentication`
- `fix: resolve database connection leak`
- `docs: update installation guide`

## Before Submitting PR

1. Run tests: `pytest`
2. Check formatting: `ruff check .`
3. Update documentation if needed

## Documentation

- [Development Guide](docs/development.md) — adding models, routes, services
- [Testing Guide](docs/testing.md) — writing and running tests
