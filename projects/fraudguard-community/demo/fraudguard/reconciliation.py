"""Deterministic reconciliation of independent operational reports."""
from collections import defaultdict
from decimal import Decimal, InvalidOperation
import csv
import io
import re

from .profiles import normalize_transaction_headers, normalize_status, level_for


def read_report(data: bytes) -> list[dict[str, str]]:
    text = data.decode('utf-8-sig')
    try:
        dialect = csv.Sniffer().sniff(text[:16384], delimiters=',;\t')
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect, strict=True)
    headers = reader.fieldnames or []
    if not headers or len(set(headers)) != len(headers):
        raise ValueError('El reporte está vacío o tiene encabezados repetidos.')
    rows = []
    for line, row in enumerate(reader, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f'Fila {line}: cantidad de columnas incorrecta.')
        if any(str(value).strip() for value in row.values()):
            rows.append(row)
        if len(rows) > 50000:
            raise ValueError('Máximo 50.000 filas por reporte; divide el período.')
    if not rows:
        raise ValueError('El reporte no contiene registros.')
    return rows


def money(value: str) -> Decimal:
    value = str(value).strip().replace('\u00a0', '').replace(' ', '')
    if not re.fullmatch(r'-?\d[\d.,]*', value):
        raise ValueError('Importe inválido: ' + value)
    if ',' in value and '.' in value:
        decimal, grouping = (',', '.') if value.rfind(',') > value.rfind('.') else ('.', ',')
        whole, fraction = value.rsplit(decimal, 1)
        if len(fraction) not in (1, 2) or not re.fullmatch(r'-?\d{1,3}(?:' + re.escape(grouping) + r'\d{3})*', whole):
            raise ValueError('Separadores de importe ambiguos: ' + value)
        value = whole.replace(grouping, '') + '.' + fraction
    elif ',' in value:
        if value.count(',') != 1 or len(value.rsplit(',', 1)[1]) not in (1, 2):
            raise ValueError('Importe ambiguo; usa dos decimales: ' + value)
        value = value.replace(',', '.')
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Importe inválido') from exc
    if not parsed.is_finite():
        raise ValueError('Importe no finito')
    return parsed


def prepare(rows, source):
    normalized, _ = normalize_transaction_headers(rows)
    # A role-specific generic "amount/status" can be interpreted unambiguously.
    for row in normalized:
        if source == 'ventas':
            if 'expected_amount' not in row and 'charged_amount' in row:
                row['expected_amount'] = row.pop('charged_amount')
            if 'expected_status' not in row and 'actual_status' in row:
                row['expected_status'] = row.pop('actual_status')
    required = ('transaction_id', 'currency', 'expected_amount', 'expected_status') if source == 'ventas' else ('transaction_id', 'currency', 'charged_amount', 'actual_status')
    missing = [key for key in required if not normalized or key not in normalized[0]]
    if missing:
        raise ValueError(source + ': no se reconocen ' + ', '.join(missing))
    groups = defaultdict(list)
    for number, row in enumerate(normalized, 2):
        ref = row.get('transaction_id', '').strip()
        if not ref:
            raise ValueError(f'{source}, fila {number}: referencia vacía; no se puede cruzar.')
        groups[ref].append(row)
    return groups


def reconcile(sales, processor):
    left, right = prepare(sales, 'ventas'), prepare(processor, 'procesador')
    results = []
    known = {'approved', 'paid', 'settled', 'declined', 'pending', 'refunded', 'chargeback'}
    for ref in sorted(set(left) | set(right)):
        a, b = left.get(ref, []), right.get(ref, [])
        sale, payment = (a[0] if a else {}), (b[0] if b else {})
        reasons, codes = [], []
        def flag(code, message):
            codes.append(code)
            reasons.append(message)
        if not a:
            flag('missing_sale', 'El procesador reporta un pago que no aparece en ventas')
        if not b:
            flag('missing_payment', 'La venta no aparece en el reporte del procesador; verificar si se cobró')
        if len(a) > 1:
            flag('duplicate_sale', f'La venta repite esta referencia en {len(a)} filas; cruce ambiguo')
        if len(b) > 1:
            flag('duplicate_payment', f'El procesador repite la referencia en {len(b)} filas; revisar eventos y posible doble cobro')
        if len(a) == len(b) == 1:
            ca, cb = sale['currency'].strip().upper(), payment['currency'].strip().upper()
            if not ca or not cb or len(ca) != 3 or len(cb) != 3:
                flag('invalid_currency', 'Moneda ausente o inválida; usa código como BOB, USD o EUR')
            elif ca != cb:
                flag('currency_mismatch', f'Moneda distinta: venta {ca}, procesador {cb}; no se convierte automáticamente')
            try:
                expected, actual = money(sale['expected_amount']), money(payment['charged_amount'])
                if ca == cb and expected != actual:
                    flag('amount_mismatch', f'Importe distinto: venta {expected}, cobrado {actual}; diferencia {actual-expected}')
                if expected < 0 or actual < 0:
                    flag('refund', 'Importe negativo: revisar devolución o ajuste por separado del cobro')
            except ValueError as exc:
                flag('invalid_amount', str(exc))
            expected_status, actual_status = normalize_status(sale['expected_status']), normalize_status(payment['actual_status'])
            if expected_status not in known or actual_status not in known:
                flag('unknown_status', f'Estado desconocido: venta {sale["expected_status"]}, procesador {payment["actual_status"]}')
            elif expected_status != actual_status:
                if actual_status == 'declined':
                    flag('declined', 'El procesador rechazó un pago que ventas esperaba completar')
                elif actual_status == 'pending':
                    flag('pending', 'El procesador informa pendiente; aún no confirma el cobro o liquidación')
                elif actual_status == 'approved' and expected_status in {'paid', 'settled'}:
                    flag('not_settled', 'Pago aprobado/autorizado, pero no cobrado o liquidado según lo esperado')
                elif actual_status == 'paid' and expected_status == 'settled':
                    flag('not_settled', 'Pago cobrado, pero no liquidado; comprobar el abono del procesador')
                else:
                    flag('status_mismatch', f'Estado distinto: esperado {expected_status}, procesador {actual_status}')
            if actual_status in {'refunded', 'chargeback'}:
                flag('refund', 'Reembolso o contracargo: revisar la devolución y su vínculo con el cobro original')
            if actual_status == 'settled' and not payment.get('settled_at', '').strip():
                flag('missing_settlement', 'Figura liquidado pero falta la fecha de liquidación en el reporte')
        score = min(100, 65 if codes else 0)
        results.append({'record_id':ref, 'subject':sale.get('merchant_id', ''), 'category':payment.get('currency', sale.get('currency', '')), 'value':payment.get('charged_amount', 'Sin registro'), 'expected_value':sale.get('expected_amount', 'Sin venta'), 'status':payment.get('actual_status', 'No encontrado'), 'timestamp':payment.get('settled_at', ''), 'score':score, 'level':level_for(score), 'codes':codes, 'sales_rows':len(a), 'processor_rows':len(b), 'reasons':reasons or ['Referencia, importe, moneda y estado coinciden según los reportes cargados.']})
    return sorted(results, key=lambda item:(-item['score'], item['record_id']))
