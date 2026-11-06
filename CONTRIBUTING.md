# Contributing

1. Open an issue describing the problem and intended behavior.
2. Work on a focused branch and keep production data out of fixtures.
3. Add or update tests for behavior changes.
4. Run `powershell -File tools/verify-public.ps1` before committing.
5. Submit a pull request using the repository template.

Changes that weaken dry-run, approval, idempotency, audit logging, or input validation require an explicit security review.

