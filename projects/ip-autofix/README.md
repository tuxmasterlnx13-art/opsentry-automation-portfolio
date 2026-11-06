# IP Autofix

A two-stage automation for authorized ISP environments: collect the eligible TR-069 address, validate identity and network constraints, then prepare a guarded remediation queue.

## Safety properties

- Collection is read-only and blocks mutable HTTP methods.
- IPs must belong to the configured carrier-grade NAT range and be unique.
- Dry-run, pilot, and explicit approval precede any production write.
- SQLite claims work atomically; uncertain writes are not retried blindly.
- Bounded retries, checkpoints, idempotency keys, and per-item evidence make runs recoverable and auditable.

## Testing

Offline tests use simulated HTML and browser doubles. They must not contact a vendor platform. Real integration testing requires an authorized disposable account and synthetic records.

