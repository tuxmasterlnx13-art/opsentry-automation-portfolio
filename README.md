# OPSENTRY Automation Portfolio

[![Quality and safety](https://github.com/tuxmasterlnx13-art/opsentry-automation-portfolio/actions/workflows/quality.yml/badge.svg)](https://github.com/tuxmasterlnx13-art/opsentry-automation-portfolio/actions/workflows/quality.yml)
[![CodeQL](https://github.com/tuxmasterlnx13-art/opsentry-automation-portfolio/actions/workflows/codeql.yml/badge.svg)](https://github.com/tuxmasterlnx13-art/opsentry-automation-portfolio/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

Runnable, vendor-neutral examples for safer operations automation: audit pipelines, explainable reconciliation, guarded remediation plans, persistent work queues, dashboards, and deterministic reporting.

The repository is useful without access to a private network. Every demo runs with synthetic data, every write-oriented workflow stops at a reviewable plan, and CI rejects credentials, customer exports, browser sessions, databases, and private network addresses.

> **En español:** contiene demostraciones ejecutables de automatización segura. No incluye datos de clientes ni credenciales. Empieza con `scripts/setup.ps1` y después ejecuta `scripts/run-showcase.ps1`.

## Start in two minutes

### Windows PowerShell

```powershell
git clone https://github.com/tuxmasterlnx13-art/opsentry-automation-portfolio.git
cd opsentry-automation-portfolio
.\scripts\setup.ps1
.\scripts\run-showcase.ps1
```

### Linux or macOS

```bash
git clone https://github.com/tuxmasterlnx13-art/opsentry-automation-portfolio.git
cd opsentry-automation-portfolio
chmod +x scripts/*.sh
./scripts/setup.sh
./scripts/run-showcase.sh
```

The showcase executes four independent examples and creates only temporary synthetic files. To run the visual GUARDIAN application afterwards:

```powershell
.\.venv\Scripts\python.exe .\projects\fraudguard-community\demo\run_fraudguard.py
```

On Linux or macOS use `.venv/bin/python` instead.

## Included projects

| Project | What you can run | Main engineering ideas |
| --- | --- | --- |
| [GUARDIAN Community](projects/fraudguard-community/README.md) | Local web application and Windows installer for comparing sales and payment reports, reviewing differences, and exporting results. | Explainable rules, CSV hardening, SQLite persistence, CSRF protection, local-first privacy. |
| [Operations Dashboard](projects/operations-dashboard/README.md) | Synthetic case dashboard and JSON API. | Small Flask service, server-rendered UI, testable API boundary. |
| [IP Autofix](projects/ip-autofix/README.md) | Deterministic dry-run planner for authorized IP remediation. | CIDR validation, duplicate prevention, pilot eligibility, no production writes. |
| [Router & Serial Automation](projects/router-serial-automation/README.md) | Reviewable change-plan generator. | Human approval, exclusions, deterministic output, rollback-friendly evidence. |
| [Automation Orchestrator](projects/automation-orchestrator/README.md) | Persistent SQLite queue with atomic work claims. | Concurrency control, resumability, ownership-aware completion. |
| [Audit Reporting](projects/audit-reporting/README.md) | Deterministic Markdown report generator. | Stable summaries, separation of generation and delivery, offline tests. |

## Download GUARDIAN for Windows

Tagged releases build a Windows installer in GitHub Actions and publish it with a SHA-256 checksum. Download and verify the latest release automatically:

```powershell
.\scripts\download-guardian.ps1
```

Or on Linux/macOS:

```bash
./scripts/download-guardian.sh
```

The downloader refuses an installer whose hash does not match `SHA256SUMS.txt`. You can also open the repository's **Releases** page and verify the checksum manually.

## What the public edition does and does not do

This repository includes reusable algorithms, guarded workflow patterns, synthetic fixtures, tests, documentation, and a complete local reconciliation application. It intentionally excludes production selectors, vendor accounts, live recipient lists, operational databases, customer records, browser profiles, private URLs, and automatic production writes.

To adapt an integration, implement an authorized adapter behind the demonstrated validation and approval gates. Start with a disposable account and synthetic records. Never point a first run at production.

## Useful commands

```powershell
# Install dependencies and run every offline test
.\scripts\setup.ps1

# Run the terminal showcase again
.\scripts\run-showcase.ps1

# Run all tests without reinstalling
.\scripts\test-all.ps1

# Verify that the public tree contains no forbidden artifacts
.\tools\verify-public.ps1

# Start the synthetic dashboard
.\.venv\Scripts\python.exe .\projects\operations-dashboard\demo\app.py
```

## Safety model

1. Discovery and dry-run happen before any write.
2. Mutable actions require explicit human approval and a small pilot.
3. Credentials come from local environment configuration, never source control.
4. Work is attributable, resumable, bounded, and independently verifiable.
5. Synthetic offline tests exercise the public workflows without contacting vendors.

## Repository quality

- Windows CI runs the public-tree safety scanner, compiles every Python file, and executes all offline tests.
- CodeQL analyzes Python changes and runs weekly.
- Dependabot updates GitHub Actions and Python dependencies.
- Tagged GUARDIAN releases build and hash the Windows installer automatically.
- Issue forms support bug reports, feature requests, and professional inquiries without requesting confidential data.

## Contributing

Bug fixes, documentation improvements, new synthetic fixtures, and vendor-neutral adapters are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), open an issue, and keep examples reproducible without private infrastructure.

If this project helps you build safer automation, consider starring it. Stars make the examples easier for other operators and hiring teams to discover.

## License

Released under the [MIT License](LICENSE). External platforms and trademarks remain the property of their respective owners. Use integrations only on systems you own or are explicitly authorized to administer.

