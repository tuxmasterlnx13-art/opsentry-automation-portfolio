"""Flask user interface for GUARDIAN Community."""

from __future__ import annotations

import csv
import io
import sqlite3
import json
import uuid
import secrets
import hmac
from .reconciliation import reconcile, read_report
from contextlib import closing
from dataclasses import asdict
from decimal import Decimal, InvalidOperation
from functools import wraps
from pathlib import Path

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from .engine import REQUIRED_COLUMNS, Settings, analyze, validate_columns
from .sample import SAMPLE_ROWS
from .profiles import (
    AUDIT_COLUMNS, AUDIT_SAMPLE_ROWS, GENERIC_SAMPLE_ROWS, PROFILE_INFO,
    TRANSACTION_COLUMNS, TRANSACTION_SAMPLE_ROWS, analyze_audit, analyze_generic,
    analyze_transactions, normalize_transaction_headers,
)

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
SALES_COLUMNS = ("transaction_id", "merchant_id", "expected_amount", "currency", "expected_status")
PROCESSOR_COLUMNS = ("transaction_id", "charged_amount", "currency", "actual_status", "settled_at")


def create_app(*, lan_mode: bool = False, access_key_hash: str | None = None, review_db: str | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(
        SECRET_KEY="development-only-replaced-by-launcher",
        MAX_CONTENT_LENGTH=MAX_UPLOAD_BYTES,
        LAN_MODE=lan_mode,
        ACCESS_KEY_HASH=access_key_hash,
        RESULTS=[],
        SOURCE_NAME="",
        ANALYSIS_SETTINGS=Settings(),
        ACTIVE_PROFILE="transactions",
        CSRF_ENABLED=True,
        REVIEW_DB=review_db or str(Path(app.instance_path) / "guardian-reviews.sqlite3"),
    )
    Path(app.config['REVIEW_DB']).parent.mkdir(parents=True, exist_ok=True)

    def init_review_db():
        with closing(sqlite3.connect(app.config["REVIEW_DB"])) as db:
            db.execute("CREATE TABLE IF NOT EXISTS reviews (transaction_id TEXT PRIMARY KEY, status TEXT NOT NULL DEFAULT 'Pendiente', assigned_to TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '', updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            db.execute("CREATE TABLE IF NOT EXISTS review_history (id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_id TEXT NOT NULL, status TEXT NOT NULL, assigned_to TEXT NOT NULL, note TEXT NOT NULL, changed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            db.execute("CREATE TABLE IF NOT EXISTS analyses (id TEXT PRIMARY KEY, source TEXT NOT NULL, profile TEXT NOT NULL, results TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
            db.commit()

    def review_for(transaction_id: str) -> dict:
        with closing(sqlite3.connect(app.config["REVIEW_DB"])) as db:
            row = db.execute("SELECT status, assigned_to, note, updated_at FROM reviews WHERE transaction_id=?", (transaction_id,)).fetchone()
            count = db.execute("SELECT COUNT(*) FROM review_history WHERE transaction_id=?", (transaction_id,)).fetchone()[0]
            history = db.execute("SELECT changed_at,status,assigned_to,note FROM review_history WHERE transaction_id=? ORDER BY id DESC LIMIT 20", (transaction_id,)).fetchall()
        return {"review_status": row[0], "assigned_to": row[1], "note": row[2], "review_updated": row[3], "history_count": count, "history": history} if row else {"review_status": "Pendiente", "assigned_to": "", "note": "", "review_updated": "", "history_count": 0, "history": []}

    init_review_db()

    @app.context_processor
    def form_security():
        session.setdefault('csrf_token', secrets.token_urlsafe(32))
        return {'csrf_token': session['csrf_token']}

    @app.before_request
    def protect_forms():
        if request.method == 'POST' and app.config['CSRF_ENABLED']:
            supplied = request.form.get('csrf_token', '')
            if not supplied or not hmac.compare_digest(supplied, session.get('csrf_token', '')):
                return render_template('error.html'), 400

    @app.after_request
    def secure_response(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'same-origin'
        response.headers['Cache-Control'] = 'no-store' if request.endpoint != 'static' else 'no-cache'
        return response

    def save_run(results, source, profile):
        run_id = uuid.uuid4().hex
        with closing(sqlite3.connect(app.config["REVIEW_DB"])) as db:
            db.execute("INSERT INTO analyses(id,source,profile,results) VALUES(?,?,?,?)", (run_id, source, profile, json.dumps(results, ensure_ascii=False)))
            db.commit()
        session["run_id"] = run_id
        app.config.update(RESULTS=results, SOURCE_NAME=source, ACTIVE_PROFILE=profile)

    def load_run():
        with closing(sqlite3.connect(app.config["REVIEW_DB"])) as db:
            run_id = request.form.get("run_id") or request.args.get("run") or session.get("run_id")
            row = db.execute("SELECT id,source,profile,results FROM analyses WHERE id=?", (run_id,)).fetchone() if run_id else None
            if not row:
                row = db.execute("SELECT id,source,profile,results FROM analyses ORDER BY rowid DESC LIMIT 1").fetchone()
        if row:
            session["run_id"] = row[0]
            return row[0], row[1], row[2], json.loads(row[3])
        return "", "", "transactions", []

    def authenticated() -> bool:
        return not app.config["LAN_MODE"] or bool(session.get("authenticated"))

    def require_access(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not authenticated():
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    @app.get("/login")
    @app.post("/login")
    def login():
        if not app.config["LAN_MODE"]:
            return redirect(url_for("index"))
        if request.method == "POST":
            supplied = request.form.get("access_key", "")
            stored = app.config.get("ACCESS_KEY_HASH")
            if stored and check_password_hash(stored, supplied):
                session.clear()
                session["authenticated"] = True
                return redirect(url_for("index"))
            flash("Clave incorrecta.", "error")
        return render_template("login.html")

    @app.post("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.get("/")
    @require_access
    def index():
        selected_profile = request.args.get("profile")
        if selected_profile in PROFILE_INFO:
            app.config["ACTIVE_PROFILE"] = selected_profile
        run_id, source, run_profile, results = load_run()
        results = [{**item, **review_for(run_id + ":" + item["record_id"])} for item in results]
        with closing(sqlite3.connect(app.config["REVIEW_DB"])) as db:
            runs = db.execute("SELECT id,source,created_at FROM analyses ORDER BY rowid DESC LIMIT 25").fetchall()
        summary = {
            "total": len(results),
            "flagged": sum(1 for item in results if item["score"] > 0),
            "high": sum(1 for item in results if item["level"] == "Alto"),
            "medium": sum(1 for item in results if item["level"] == "Medio"),
        }
        return render_template(
            "index.html",
            results=results,
            summary=summary,
            source_name=source,
            runs=runs,
            run_id=run_id,
            required_columns=", ".join(REQUIRED_COLUMNS),
            lan_mode=app.config["LAN_MODE"],
            settings=app.config["ANALYSIS_SETTINGS"],
            profiles=PROFILE_INFO,
            active_profile=app.config["ACTIVE_PROFILE"],
            profile=PROFILE_INFO[app.config["ACTIVE_PROFILE"]],
            review_open=sum(1 for item in results if item["score"] and item.get("review_status", "Pendiente") in {"Pendiente", "Confirmada"}),
            missing=sum(1 for item in results if any("no aparece" in reason.lower() for reason in item.get("reasons", ()))),
            amount_mismatch=sum(1 for item in results if any("importe distinto" in reason.lower() for reason in item.get("reasons", ()))),
            failed=sum(1 for item in results if 'declined' in item.get('codes', ()) or any("rechazad" in reason.lower() or "fall" in reason.lower() for reason in item.get("reasons", ()))),
        )

    def run_analysis(rows: list[dict[str, str]], source_name: str, profile: str | None = None):
        profile = profile or request.form.get("profile", app.config["ACTIVE_PROFILE"])
        if profile not in PROFILE_INFO:
            profile = "transactions"
        app.config["ACTIVE_PROFILE"] = profile
        missing = []
        if missing:
            flash("Faltan columnas: " + ", ".join(missing), "error")
            return redirect(url_for("index"))
        if profile == "transactions":
            results, errors = analyze_transactions(rows)
        elif profile == "audit":
            results, errors = analyze_audit(rows)
        else:
            results, errors = analyze_generic(rows)
        if errors and not results:
            flash(errors[0], "error")
            return redirect(url_for("index") + "#analizar")
        save_run(results, source_name, profile)
        if errors:
            flash(f"Se encontraron {len(errors)} detalles de formato. El primero: {errors[0]}", "warning")
        flash(f"Análisis terminado: {len(results)} registros revisados.", "success")
        return redirect(url_for("index"))

    @app.post("/reglas")
    @require_access
    def update_rules():
        try:
            settings = Settings(
                high_amount=Decimal(request.form["high_amount"].replace(",", ".")),
                velocity_count=int(request.form["velocity_count"]),
                velocity_minutes=int(request.form["velocity_minutes"]),
                country_window_minutes=int(request.form["country_window_minutes"]),
                shared_device_customers=int(request.form["shared_device_customers"]),
            )
            if settings.high_amount <= 0 or any(value <= 0 for value in (
                settings.velocity_count,
                settings.velocity_minutes,
                settings.country_window_minutes,
                settings.shared_device_customers,
            )):
                raise ValueError("todos los valores deben ser mayores que cero")
        except (KeyError, InvalidOperation, ValueError) as exc:
            flash(f"No se guardaron las reglas: revisa los números ({exc}).", "error")
            return redirect(url_for("index") + "#reglas")
        app.config["ANALYSIS_SETTINGS"] = settings
        flash("Reglas guardadas para esta sesión. Se aplicarán en el próximo análisis.", "success")
        return redirect(url_for("index") + "#reglas")

    @app.post("/upload")
    @require_access
    def upload():
        uploaded = request.files.get("file")
        if not uploaded or not uploaded.filename:
            flash("Selecciona un archivo CSV.", "error")
            return redirect(url_for("index"))
        if Path(uploaded.filename).suffix.lower() != ".csv":
            flash("Solo se aceptan archivos .csv.", "error")
            return redirect(url_for("index"))
        try:
            rows = read_report(uploaded.stream.read())
        except (UnicodeDecodeError, csv.Error, ValueError) as exc:
            flash(f"No se pudo leer el CSV: {exc}", "error")
            return redirect(url_for("index"))
        return run_analysis(rows, Path(uploaded.filename).name)

    @app.post("/conciliar")
    @require_access
    def reconcile_sources():
        def load_csv(field: str) -> list[dict[str, str]]:
            uploaded = request.files.get(field)
            if not uploaded or not uploaded.filename or Path(uploaded.filename).suffix.lower() != ".csv":
                raise ValueError("Selecciona los dos archivos CSV.")
            return read_report(uploaded.stream.read())
        try:
            sales = load_csv("sales_file")
            processor = load_csv("processor_file")
        except (ValueError, UnicodeDecodeError, csv.Error) as exc:
            flash(str(exc) or "No se pudieron leer los dos CSV.", "error")
            return redirect(url_for("index") + "#analizar")
        try:
            results = reconcile(sales, processor)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index") + "#cruce")
        save_run(results, "Cruce ventas + procesador", "transactions")
        flash(f"Conciliación completa: {len(results)} referencias comparadas.", "success")
        return redirect(url_for("index") + "#dashboard")

    @app.post("/revisar/<path:transaction_id>")
    @require_access
    def save_review(transaction_id: str):
        run_id, _, _, results = load_run()
        if not any(item["record_id"] == transaction_id for item in results):
            return "Caso no encontrado en esta conciliación", 404
        case_key = run_id + ":" + transaction_id
        status = request.form.get("review_status", "Pendiente")
        if status not in {"Pendiente", "Confirmada", "Resuelta", "Falso positivo"}:
            status = "Pendiente"
        with closing(sqlite3.connect(app.config["REVIEW_DB"])) as db:
            db.execute("INSERT INTO reviews(transaction_id,status,assigned_to,note,updated_at) VALUES(?,?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(transaction_id) DO UPDATE SET status=excluded.status,assigned_to=excluded.assigned_to,note=excluded.note,updated_at=CURRENT_TIMESTAMP", (case_key, status, request.form.get("assigned_to", "")[:120], request.form.get("note", "")[:1000]))
            db.execute("INSERT INTO review_history(transaction_id,status,assigned_to,note) VALUES(?,?,?,?)", (case_key, status, request.form.get("assigned_to", "")[:120], request.form.get("note", "")[:1000]))
            db.commit()
        flash(f"Caso {transaction_id}: revisión guardada.", "success")
        return redirect(url_for("index") + "#dashboard")

    @app.post("/demo")
    @require_access
    def demo():
        profile = request.form.get("profile", "transactions")
        rows = {"transactions": TRANSACTION_SAMPLE_ROWS, "audit": AUDIT_SAMPLE_ROWS, "generic": GENERIC_SAMPLE_ROWS}.get(profile, TRANSACTION_SAMPLE_ROWS)
        return run_analysis(list(rows), "demostración sintética", profile)

    @app.get("/plantilla")
    @require_access
    def template_csv():
        """Download a ready-to-open example for Excel and similar tools."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=TRANSACTION_COLUMNS)
        writer.writeheader()
        writer.writerow(TRANSACTION_SAMPLE_ROWS[0])
        return Response(
            "\ufeff" + output.getvalue(),
            mimetype="text/csv; charset=utf-8",
            headers={"Content-Disposition": "attachment; filename=plantilla_guardian.csv"},
        )

    @app.get("/ejemplo/<profile>")
    @require_access
    def example_csv(profile: str):
        rows = {"transactions": TRANSACTION_SAMPLE_ROWS, "audit": AUDIT_SAMPLE_ROWS, "generic": GENERIC_SAMPLE_ROWS}.get(profile)
        if profile in {'ventas', 'procesador'}:
            keys = SALES_COLUMNS if profile == 'ventas' else PROCESSOR_COLUMNS
            rows = [{key: row.get(key, '') for key in keys} for row in TRANSACTION_SAMPLE_ROWS]
        if rows is None:
            return redirect(url_for("index"))
        output = io.StringIO()
        fields = list(rows[0].keys())
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        return Response("\ufeff" + output.getvalue(), mimetype="text/csv; charset=utf-8", headers={"Content-Disposition": f"attachment; filename=ejemplo_{profile}.csv"})

    @app.get("/export")
    @require_access
    def export():
        output = io.StringIO()
        fields = ["record_id", "subject", "category", "value", "expected_value", "status", "timestamp", "score", "level", "reasons"]
        fields += ['review_status', 'assigned_to', 'note']
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        run_id, _, _, export_results = load_run()
        for result in export_results:
            result = {**result, **review_for(run_id + ':' + result['record_id'])}
            values = {key: (' | '.join(result['reasons']) if key == 'reasons' else result.get(key, '')) for key in fields}
            # Prevent spreadsheet formulas from executing when a report is opened.
            writer.writerow({key: ("'" + str(value) if str(value).lstrip().startswith(('=', '+', '-', '@')) else value) for key, value in values.items()})
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=guardian_resultados.csv"},
        )

    @app.errorhandler(413)
    def too_large(_error):
        flash("El archivo supera el límite de 10 MB.", "error")
        return redirect(url_for("index"))

    return app

