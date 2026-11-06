# OPSENTRY Automation Portfolio

Safely designed operations tooling for ISP audit, remediation, monitoring, and reporting workflows.

> **Publication status:** release candidate. The code is staged from a private operational workspace through an explicit allowlist and automated safety checks. Live credentials, customer data, browser sessions, internal evidence, and production configuration are not part of this repository.

## What this portfolio demonstrates

| Project | Purpose | Engineering highlights |
| --- | --- | --- |
| [Operations Dashboard](projects/operations-dashboard/README.md) | Turns validated audit runs into an assignment, verification, and reporting workflow. | Flask, Argon2 authentication, CSRF protection, revocable sessions, SQLite, role-based access. |
| [IP Autofix](projects/ip-autofix/README.md) | Collects TR-069 data and prepares a guarded remediation queue. | Playwright, dry-run gates, idempotency, bounded retries, strict IP validation. |
| [Router & Serial Automation](projects/router-serial-automation/README.md) | Diagnoses and safely stages router, plan, and serial corrections. | Checkpoints, resumable queues, pilots, reconciliation, human approval gates. |
| [Automation Orchestrator](projects/automation-orchestrator/README.md) | Coordinates specialized workers over a persistent queue. | SQLite concurrency, finite workflows, recovery, offline tests. |
| [Audit Reporting](projects/audit-reporting/README.md) | Produces daily/weekly reports and optional notifications. | Deterministic reporting, testable formatting, separation of config and runtime state. |

## Safety model

These projects automate sensitive operational work, so the public edition follows four rules:

1. Read-only discovery and dry-run happen before any write.
2. Real writes require explicit operator approval and a small pilot.
3. Credentials come from environment variables or local ignored files.
4. Every action must be attributable, resumable, and verifiable.

## Explore and run

Each project has its own README with architecture, setup, safety constraints, and test commands. Integrations with commercial platforms require your own authorized account and may need selector/configuration adaptation.

```powershell
git clone <repository-url>
cd opsentry-automation-portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r projects/operations-dashboard/demo/requirements.txt
cd projects/<project>/demo
python -m unittest discover -v
```

Never point a first run at production. Use synthetic data, dry-run mode, and a disposable test account.

## Repository quality

- CI checks Python syntax, tests, forbidden files, and secret-like content.
- Dependabot proposes dependency and workflow updates.
- Security reports follow a private disclosure process.
- Changes use pull requests and the included review checklist.

## License and ownership

No open-source license is attached to this release candidate yet. Public licensing must happen only after confirming that the publisher owns the code or has written authorization from the owner. Until then, all rights are reserved.

## Contact

Open a GitHub issue for technical questions. For hiring or consulting inquiries, add your preferred public contact details to this section before publication.

