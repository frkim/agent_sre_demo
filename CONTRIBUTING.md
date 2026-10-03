# Contributing

Thank you for contributing to Contoso Trek.

## Workflow

1. Create a short-lived branch from `main`.
2. Keep pull requests focused on one logical change.
3. Use Conventional Commit titles such as `feat:`, `fix:`, `docs:`, or `ci:`.
4. Update documentation and SRE configuration alongside behavior changes.
5. Run relevant validation locally before opening a PR.

## Validation

Infrastructure changes:

```bash
az bicep build --file infra/main.bicep
az bicep lint --file infra/main.bicep
find scripts -name '*.sh' -print0 | xargs -0 -n1 bash -n
```

Application changes are validated by the GitHub Actions workflow with ruff/pytest for `src/api` and npm build/test for `src/web`.

## Supply chain

Use Microsoft-protected package feeds. Do not add public PyPI or NuGet registry URLs to configuration, Dockerfiles, scripts, or workflows.
