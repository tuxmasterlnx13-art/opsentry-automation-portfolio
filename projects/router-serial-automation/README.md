# Router & Serial Automation

Tools for diagnosing and staging router, plan, serial-number, and cancellation corrections while preserving human review and rollback evidence.

## Workflow

1. Build a candidate set from a complete validated audit.
2. Exclude cancelled, ambiguous, duplicated, or unsupported cases.
3. Produce a dry-run and a small pilot plan.
4. Require operator approval before applying changes.
5. Reconcile the observed result against the intended change.

The public source is an integration reference. Selectors and configuration must be adapted to an authorized test environment before use.

## Try it

From the repository root run `scripts/run-showcase.ps1` on Windows or
`scripts/run-showcase.sh` on Linux/macOS. The synthetic example creates one
reviewable router change and excludes a cancelled record. No external system is
contacted.

