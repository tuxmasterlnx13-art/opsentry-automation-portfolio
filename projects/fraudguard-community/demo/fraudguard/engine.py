"""Vendor-neutral and explainable fraud-screening rules."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Iterable

REQUIRED_COLUMNS = (
    "transaction_id",
    "customer_id",
    "amount",
    "timestamp",
    "country",
    "device_id",
    "payment_method",
)


@dataclass(frozen=True)
class Settings:
    high_amount: Decimal = Decimal("5000")
    velocity_count: int = 4
    velocity_minutes: int = 10
    country_window_minutes: int = 60
    shared_device_customers: int = 3


@dataclass(frozen=True)
class Finding:
    transaction_id: str
    customer_id: str
    amount: str
    timestamp: str
    country: str
    device_id: str
    payment_method: str
    score: int
    level: str
    reasons: tuple[str, ...]


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00")).replace(tzinfo=None)


def _parse_amount(value: str) -> Decimal:
    return Decimal(value.strip().replace(",", "."))


def validate_columns(columns: Iterable[str] | None) -> list[str]:
    available = set(columns or ())
    return [name for name in REQUIRED_COLUMNS if name not in available]


def analyze(rows: Iterable[dict[str, str]], settings: Settings | None = None) -> tuple[list[Finding], list[str]]:
    """Analyze rows without modifying or transmitting them."""
    config = settings or Settings()
    normalized: list[dict[str, object]] = []
    errors: list[str] = []

    for number, raw in enumerate(rows, start=2):
        try:
            normalized.append({
                **{key: str(raw.get(key, "")).strip() for key in REQUIRED_COLUMNS},
                "_amount": _parse_amount(str(raw.get("amount", ""))),
                "_time": _parse_time(str(raw.get("timestamp", ""))),
            })
        except (InvalidOperation, ValueError) as exc:
            errors.append(f"Fila {number}: importe o fecha inválidos ({exc}).")

    id_counts = Counter(str(row["transaction_id"]) for row in normalized)
    device_customers: dict[str, set[str]] = defaultdict(set)
    customer_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in normalized:
        device_customers[str(row["device_id"])].add(str(row["customer_id"]))
        customer_rows[str(row["customer_id"])].append(row)

    rapid_ids: set[str] = set()
    country_switch_ids: set[str] = set()
    for customer_items in customer_rows.values():
        ordered = sorted(customer_items, key=lambda item: item["_time"])
        for index, row in enumerate(ordered):
            start = row["_time"] - timedelta(minutes=config.velocity_minutes)
            nearby = [item for item in ordered[: index + 1] if item["_time"] >= start]
            if len(nearby) >= config.velocity_count:
                rapid_ids.update(str(item["transaction_id"]) for item in nearby)
            country_start = row["_time"] - timedelta(minutes=config.country_window_minutes)
            recent = [item for item in ordered[: index + 1] if item["_time"] >= country_start]
            if len({str(item["country"]).upper() for item in recent}) > 1:
                country_switch_ids.update(str(item["transaction_id"]) for item in recent)

    findings: list[Finding] = []
    for row in normalized:
        transaction_id = str(row["transaction_id"])
        reasons: list[str] = []
        score = 0
        if id_counts[transaction_id] > 1:
            score += 50
            reasons.append("ID de transacción duplicado")
        if row["_amount"] >= config.high_amount:
            score += 25
            reasons.append(f"Importe igual o superior a {config.high_amount}")
        if transaction_id in rapid_ids:
            score += 30
            reasons.append("Alta velocidad de operaciones del mismo cliente")
        if transaction_id in country_switch_ids:
            score += 35
            reasons.append("Cambio rápido de país para el mismo cliente")
        if len(device_customers[str(row["device_id"])]) >= config.shared_device_customers:
            score += 30
            reasons.append("Dispositivo compartido por varios clientes")

        level = "Alto" if score >= 60 else "Medio" if score >= 30 else "Bajo" if score else "Sin alerta"
        findings.append(Finding(
            transaction_id=transaction_id,
            customer_id=str(row["customer_id"]),
            amount=str(row["amount"]),
            timestamp=str(row["timestamp"]),
            country=str(row["country"]),
            device_id=str(row["device_id"]),
            payment_method=str(row["payment_method"]),
            score=min(score, 100),
            level=level,
            reasons=tuple(reasons) or ("Sin patrones configurados",),
        ))

    return sorted(findings, key=lambda item: (-item.score, item.timestamp, item.transaction_id)), errors

