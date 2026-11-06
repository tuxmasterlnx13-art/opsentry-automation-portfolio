# Automation Orchestrator

A persistent coordination layer for specialized audit and remediation workers. It models bounded phases, work reservation, concurrency limits, recovery, and verification over SQLite.

## Design goals

- Finite workflows with explicit stop conditions.
- Parallel analysis without uncontrolled parallel writes.
- Atomic reservation by customer and resource group.
- Resumability after interruption.
- Offline tests for contention and recovery.

This project is useful as an architecture example even when the external platform adapters are replaced.

