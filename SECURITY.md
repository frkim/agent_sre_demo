# Security policy

## Reporting a vulnerability

Report suspected vulnerabilities privately to @frkim or through GitHub private vulnerability reporting when enabled. Do not open a public issue for exploitable security bugs.

Include:

- Affected component and environment
- Reproduction steps
- Expected and actual impact
- Any logs or screenshots with secrets removed

## Security baseline

- Azure access uses managed identities and least-privilege RBAC.
- GitHub Actions authenticate to Azure with OIDC when configured.
- Secrets must not be committed, logged, or stored in SRE Agent knowledge files.
- Package restores use Microsoft-protected feeds.
- GitHub Actions are pinned to full commit SHAs.
