"""Safe, vendor-neutral IP remediation planning primitives."""

from __future__ import annotations

from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network
from typing import Iterable


@dataclass(frozen=True)
class Candidate:
    customer_id: str
    current_ip: str
    proposed_ip: str


@dataclass(frozen=True)
class Decision:
    customer_id: str
    approved: bool
    reason: str
    proposed_ip: str | None = None


def build_plan(candidates: Iterable[Candidate], allowed_cidr: str = "100.64.0.0/10") -> list[Decision]:
    """Return a deterministic dry-run plan; this function never performs writes."""
    network: IPv4Network = ip_network(allowed_cidr)
    rows = list(candidates)
    proposed_counts: dict[IPv4Address, int] = {}
    parsed: dict[str, IPv4Address] = {}

    for row in rows:
        try:
            address = ip_address(row.proposed_ip)
            if not isinstance(address, IPv4Address):
                continue
            parsed[row.customer_id] = address
            proposed_counts[address] = proposed_counts.get(address, 0) + 1
        except ValueError:
            continue

    decisions: list[Decision] = []
    for row in sorted(rows, key=lambda item: item.customer_id):
        address = parsed.get(row.customer_id)
        if address is None:
            decisions.append(Decision(row.customer_id, False, "invalid IPv4"))
        elif address not in network or address in (network.network_address, network.broadcast_address):
            decisions.append(Decision(row.customer_id, False, "outside authorized range"))
        elif proposed_counts[address] > 1:
            decisions.append(Decision(row.customer_id, False, "duplicate proposed IP"))
        elif row.current_ip == row.proposed_ip:
            decisions.append(Decision(row.customer_id, False, "no change required"))
        else:
            decisions.append(Decision(row.customer_id, True, "eligible for pilot", str(address)))
    return decisions

