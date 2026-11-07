"""Adaptable monitoring profiles beyond payment fraud."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
import re
import unicodedata


AUDIT_COLUMNS = (
    "record_id",
    "entity_id",
    "category",
    "current_value",
    "expected_value",
    "status",
    "updated_at",
)
TRANSACTION_COLUMNS = (
    "transaction_id", "merchant_id", "expected_amount", "charged_amount",
    "currency", "expected_status", "actual_status", "created_at", "settled_at",
)

PROFILE_INFO = {
    "transactions": {
        "name": "Conciliación de transacciones",
        "description": "Comprueba si el pago quedó aprobado, cobrado y liquidado por el importe correcto.",
    },
    "audit": {
        "name": "Auditoría de sistemas",
        "description": "Compara valores actuales y esperados: planes, IP, seriales, estados o inventario.",
    },
    "generic": {
        "name": "Calidad de cualquier CSV",
        "description": "Busca duplicados, campos vacíos, valores de error y formatos descuidados.",
    },
}

TRANSACTION_SAMPLE_ROWS = [
    {"transaction_id":"TX-1001","merchant_id":"TIENDA-01","expected_amount":"250.00","charged_amount":"250.00","currency":"BOB","expected_status":"settled","actual_status":"settled","created_at":"2026-11-05T09:00:00","settled_at":"2026-11-05T09:03:00"},
    {"transaction_id":"TX-1002","merchant_id":"TIENDA-01","expected_amount":"89.90","charged_amount":"89.90","currency":"BOB","expected_status":"settled","actual_status":"declined","created_at":"2026-11-05T09:10:00","settled_at":""},
    {"transaction_id":"TX-1003","merchant_id":"TIENDA-02","expected_amount":"120.00","charged_amount":"132.00","currency":"BOB","expected_status":"settled","actual_status":"settled","created_at":"2026-11-05T10:00:00","settled_at":"2026-11-05T10:05:00"},
    {"transaction_id":"TX-1004","merchant_id":"TIENDA-01","expected_amount":"45.00","charged_amount":"45.00","currency":"BOB","expected_status":"settled","actual_status":"pending","created_at":"2026-11-03T08:30:00","settled_at":""},
    {"transaction_id":"TX-1005","merchant_id":"TIENDA-03","expected_amount":"60.00","charged_amount":"60.00","currency":"BOB","expected_status":"settled","actual_status":"settled","created_at":"2026-11-05T12:00:00","settled_at":"2026-11-05T12:04:00"},
    {"transaction_id":"TX-1005","merchant_id":"TIENDA-03","expected_amount":"60.00","charged_amount":"60.00","currency":"BOB","expected_status":"settled","actual_status":"settled","created_at":"2026-11-05T12:00:00","settled_at":"2026-11-05T12:04:00"},
]

HEADER_ALIASES = {
    "transaction_id": {"transaction_id", "transactionid", "id_transaccion", "transaccion_id", "referencia", "reference", "payment_id", "id_pago", "id_de_pago", "order_id", "id_orden", "folio", "operation_id"},
    "merchant_id": {"merchant_id", "merchant", "comercio", "tienda", "store", "business_name", "nombre_comercio"},
    "expected_amount": {"expected_amount", "importe_esperado", "monto_esperado", "total_venta", "sale_amount", "order_amount", "monto_venta", "amount_expected"},
    "charged_amount": {"charged_amount", "amount", "importe_cobrado", "monto_cobrado", "importe", "monto", "total_cobrado", "gross_amount", "transaction_amount"},
    "currency": {"currency", "moneda", "divisa", "currency_code", "codigo_moneda"},
    "expected_status": {"expected_status", "estado_esperado", "estado_venta", "sale_status", "order_status", "expected_payment_status"},
    "actual_status": {"actual_status", "status", "estado", "payment_status", "estado_pago", "estado_del_pago", "resultado", "result", "transaction_status", "payment_state"},
    "created_at": {"created_at", "fecha_creacion", "fecha_venta", "sale_date", "order_date", "fecha_transaccion", "timestamp"},
    "settled_at": {"settled_at", "fecha_liquidacion", "fecha_deposito", "deposit_date", "paid_at", "payment_date", "fecha_pago", "fecha_acreditacion"},
}

STATUS_ALIASES = {
    "approved": "approved", "aprobado": "approved", "autorizado": "approved", "authorized": "approved",
    "paid": "paid", "pagado": "paid", "cobrado": "paid", "captured": "paid", "capturado": "paid",
    "settled": "settled", "liquidado": "settled", "acreditado": "settled", "depositado": "settled", "completed": "settled", "completado": "settled",
    "declined": "declined", "rechazado": "declined", "denegado": "declined", "failed": "declined", "fallido": "declined", "error": "declined",
    "pending": "pending", "pendiente": "pending", "processing": "pending", "procesando": "pending", "en_proceso": "pending",
    "refunded": "refunded", "reembolsado": "refunded", "devuelto": "refunded", "chargeback": "chargeback", "contracargo": "chargeback",
}


def _key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(value).strip().lower())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")


def normalize_transaction_headers(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    mapping = {}
    for canonical, aliases in HEADER_ALIASES.items():
        mapping[_key(canonical)] = canonical
        mapping.update({_key(alias): canonical for alias in aliases})
    normalized = []
    unknown = set()
    for row in rows:
        item = {}
        for original, value in row.items():
            canonical = mapping.get(_key(original))
            if canonical:
                if canonical in item:
                    raise ValueError(f'Dos columnas representan {canonical}; conserva una o renómbralas para distinguirlas.')
                item[canonical] = str(value or "").strip()
            else:
                unknown.add(str(original))
        normalized.append(item)
    required = ("transaction_id", "expected_amount", "charged_amount", "currency", "expected_status", "actual_status")
    missing = [field for field in required if not normalized or field not in normalized[0]]
    return normalized, missing


def normalize_status(value: str) -> str:
    return STATUS_ALIASES.get(_key(value), _key(value))


def analyze_transactions(rows: list[dict[str, str]], *, pending_hours: int = 24) -> tuple[list[dict], list[str]]:
    try:
        rows, missing = normalize_transaction_headers(rows)
    except ValueError as exc:
        return [], [str(exc)]
    if missing:
        return [], ["Faltan columnas: " + ", ".join(missing)]
    ids = Counter(str(row.get("transaction_id", "")).strip() for row in rows)
    parsed = []
    for row in rows:
        try:
            parsed.append(datetime.fromisoformat(str(row.get("created_at", "")).replace("Z", "+00:00")).replace(tzinfo=None))
        except ValueError:
            pass
    reference_time = max(parsed) if parsed else datetime.now()
    results = []
    for row in rows:
        reasons = []
        score = 0
        tid = str(row.get("transaction_id", "")).strip()
        expected_status = normalize_status(row.get("expected_status", ""))
        actual_status = normalize_status(row.get("actual_status", ""))
        if ids[tid] > 1:
            score += 60
            reasons.append("Referencia de transacción duplicada: posible doble registro o doble cobro")
        try:
            expected = Decimal(str(row.get("expected_amount", "")).replace(",", "."))
            charged = Decimal(str(row.get("charged_amount", "")).replace(",", "."))
            if expected != charged:
                score += 60
                reasons.append(f"Importe distinto: esperado {expected}, cobrado {charged}")
        except InvalidOperation:
            score += 35
            reasons.append("Importe esperado o cobrado no es válido")
        if expected_status in {"settled", "approved", "paid", "liquidado", "pagado", "aprobado"} and actual_status in {"declined", "failed", "rejected", "fallido", "rechazado"}:
            score += 70
            reasons.append("El sistema esperaba un pago completado, pero la transacción fue rechazada o falló")
        elif expected_status in {"settled", "approved", "paid", "liquidado", "pagado", "aprobado"} and actual_status in {"pending", "processing", "pendiente", "procesando"}:
            try:
                created = datetime.fromisoformat(str(row.get("created_at", "")).replace("Z", "+00:00")).replace(tzinfo=None)
                age = (reference_time - created).total_seconds() / 3600
                if age >= pending_hours:
                    score += 55
                    reasons.append(f"Sigue pendiente después de {pending_hours} horas; comprobar liquidación con el procesador")
            except ValueError:
                score += 20
                reasons.append("No se pudo validar la antigüedad del pago pendiente")
        if actual_status in {"settled", "paid", "liquidado", "pagado"} and not str(row.get("settled_at", "")).strip():
            score += 35
            reasons.append("Figura como pagado, pero no tiene fecha de liquidación")
        score = min(score, 100)
        results.append({"record_id": tid or "SIN-REFERENCIA", "subject": row.get("merchant_id", ""), "category": row.get("currency", ""), "value": row.get("charged_amount", ""), "expected_value": row.get("expected_amount", ""), "status": row.get("actual_status", ""), "timestamp": row.get("created_at", ""), "score": score, "level": level_for(score), "reasons": tuple(reasons) or ("El estado e importe coinciden; se registró liquidación.",)})
    return sorted(results, key=lambda item: (-item["score"], item["record_id"])), []

AUDIT_SAMPLE_ROWS = [
    {"record_id": "AUD-100", "entity_id": "CLIENTE-01", "category": "plan", "current_value": "100 Mbps", "expected_value": "300 Mbps", "status": "active", "updated_at": "2026-11-01T09:00:00"},
    {"record_id": "AUD-101", "entity_id": "CLIENTE-02", "category": "ip", "current_value": "192.0.2.8", "expected_value": "192.0.2.8", "status": "active", "updated_at": "2026-11-05T10:00:00"},
    {"record_id": "AUD-102", "entity_id": "CLIENTE-03", "category": "serial", "current_value": "ONU-OLD-77", "expected_value": "ONU-NEW-88", "status": "error", "updated_at": "2026-08-01T08:00:00"},
    {"record_id": "AUD-102", "entity_id": "CLIENTE-03", "category": "serial", "current_value": "ONU-OLD-77", "expected_value": "ONU-NEW-88", "status": "error", "updated_at": "2026-08-01T08:00:00"},
]

GENERIC_SAMPLE_ROWS = [
    {"id": "REG-01", "area": "Ventas", "responsable": "Ana", "estado": "ok"},
    {"id": "REG-02", "area": "Soporte", "responsable": "", "estado": "unknown"},
    {"id": "REG-02", "area": "Soporte", "responsable": "", "estado": "unknown"},
    {"id": "REG-03", "area": " Operaciones ", "responsable": "Luis", "estado": "failed"},
]


def level_for(score: int) -> str:
    return "Alto" if score >= 60 else "Medio" if score >= 30 else "Bajo" if score else "Sin alerta"


def validate_audit_columns(columns) -> list[str]:
    available = set(columns or ())
    return [name for name in AUDIT_COLUMNS if name not in available]


def analyze_audit(rows: list[dict[str, str]], *, stale_days: int = 30) -> tuple[list[dict], list[str]]:
    missing = validate_audit_columns(rows[0].keys() if rows else None)
    if missing:
        return [], ["Faltan columnas: " + ", ".join(missing)]

    id_counts = Counter(str(row.get("record_id", "")).strip() for row in rows)
    entity_values: dict[tuple[str, str], set[str]] = defaultdict(set)
    parsed_times: list[datetime] = []
    for row in rows:
        entity_values[(str(row.get("entity_id", "")).strip(), str(row.get("category", "")).strip().lower())].add(str(row.get("current_value", "")).strip())
        try:
            parsed_times.append(datetime.fromisoformat(str(row.get("updated_at", "")).strip().replace("Z", "+00:00")).replace(tzinfo=None))
        except ValueError:
            pass
    newest = max(parsed_times) if parsed_times else None
    stale_before = newest - timedelta(days=stale_days) if newest else None

    results: list[dict] = []
    errors: list[str] = []
    bad_statuses = {"error", "failed", "suspended", "cancelled", "unknown", "n/a", "null"}
    for number, row in enumerate(rows, start=2):
        clean = {key: str(row.get(key, "")).strip() for key in AUDIT_COLUMNS}
        reasons: list[str] = []
        score = 0
        empty = [key for key, value in clean.items() if not value]
        if empty:
            score += min(45, len(empty) * 15)
            reasons.append("Campos vacíos: " + ", ".join(empty))
        if clean["record_id"] and id_counts[clean["record_id"]] > 1:
            score += 50
            reasons.append("Identificador de registro duplicado")
        if clean["current_value"] and clean["expected_value"] and clean["current_value"].casefold() != clean["expected_value"].casefold():
            score += 40
            reasons.append("El valor actual no coincide con el esperado")
        if clean["status"].casefold() in bad_statuses:
            score += 25
            reasons.append(f"Estado que requiere revisión: {clean['status']}")
        key = (clean["entity_id"], clean["category"].casefold())
        if clean["entity_id"] and len(entity_values[key]) > 1:
            score += 25
            reasons.append("La misma entidad tiene valores actuales contradictorios")
        try:
            updated = datetime.fromisoformat(clean["updated_at"].replace("Z", "+00:00")).replace(tzinfo=None)
            if stale_before and updated < stale_before:
                score += 20
                reasons.append(f"Registro sin actualizar por más de {stale_days} días")
        except ValueError:
            if clean["updated_at"]:
                score += 20
                reasons.append("Fecha de actualización inválida")
                errors.append(f"Fila {number}: fecha inválida.")
        score = min(score, 100)
        results.append({
            "record_id": clean["record_id"] or f"FILA-{number}",
            "subject": clean["entity_id"] or "Sin entidad",
            "category": clean["category"] or "Sin categoría",
            "value": clean["current_value"],
            "expected_value": clean["expected_value"],
            "status": clean["status"],
            "timestamp": clean["updated_at"],
            "score": score,
            "level": level_for(score),
            "reasons": tuple(reasons) or ("Sin inconsistencias configuradas",),
        })
    return sorted(results, key=lambda item: (-item["score"], item["record_id"])), errors


def analyze_generic(rows: list[dict[str, str]], *, missing_fields_limit: int = 1) -> tuple[list[dict], list[str]]:
    if not rows or not rows[0]:
        return [], ["El CSV está vacío o no tiene encabezados."]
    headers = list(rows[0].keys())
    id_field = headers[0]
    subject_field = headers[1] if len(headers) > 1 else headers[0]
    ids = Counter(str(row.get(id_field, "")).strip() for row in rows)
    signatures = Counter(tuple(str(row.get(key, "")).strip() for key in headers) for row in rows)
    suspicious = {"error", "failed", "unknown", "n/a", "null", "none", "invalid"}
    results: list[dict] = []
    for number, row in enumerate(rows, start=2):
        raw_values = [str(row.get(key, "")) for key in headers]
        values = [value.strip() for value in raw_values]
        reasons: list[str] = []
        score = 0
        missing_count = sum(not value for value in values)
        record_id = values[0] or f"FILA-{number}"
        if ids[values[0]] > 1 and values[0]:
            score += 40
            reasons.append(f"Identificador duplicado en la columna {id_field}")
        if signatures[tuple(values)] > 1:
            score += 35
            reasons.append("Fila completamente duplicada")
        if missing_count >= missing_fields_limit:
            score += min(45, missing_count * 15)
            reasons.append(f"{missing_count} campo(s) vacío(s)")
        if any(raw != clean for raw, clean in zip(raw_values, values)):
            score += 10
            reasons.append("Espacios sobrantes que pueden causar diferencias")
        markers = sorted({value for value in values if value.casefold() in suspicious})
        if markers:
            score += 20
            reasons.append("Valores que indican error o dato desconocido: " + ", ".join(markers))
        score = min(score, 100)
        results.append({
            "record_id": record_id,
            "subject": values[1] if len(values) > 1 else record_id,
            "category": "Calidad de datos",
            "value": " · ".join(values[2:5]) if len(values) > 2 else values[0],
            "expected_value": "Completo, único y consistente",
            "status": "Revisar" if score else "Correcto",
            "timestamp": "",
            "score": score,
            "level": level_for(score),
            "reasons": tuple(reasons) or ("Sin inconsistencias configuradas",),
        })
    return sorted(results, key=lambda item: (-item["score"], item["record_id"])), []
