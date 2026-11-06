"""Flask user interface for GUARDIAN Community."""

from __future__ import annotations

import csv
import io
from dataclasses import asdict
from decimal import Decimal, InvalidOperation
from functools import wraps
from pathlib import Path

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from .engine import REQUIRED_COLUMNS, Settings, analyze, validate_columns
from .sample import SAMPLE_ROWS

MAX_UPLOAD_BYTES = 10 * 1024 * 1024


def create_app(*, lan_mode: bool = False, access_key_hash: str | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.update(
        SECRET_KEY="development-only-replaced-by-launcher",
        MAX_CONTENT_LENGTH=MAX_UPLOAD_BYTES,
        LAN_MODE=lan_mode,
        ACCESS_KEY_HASH=access_key_hash,
        RESULTS=[],
        SOURCE_NAME="",
        ANALYSIS_SETTINGS=Settings(),
    )

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
        results = app.config["RESULTS"]
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
            source_name=app.config["SOURCE_NAME"],
            required_columns=", ".join(REQUIRED_COLUMNS),
            lan_mode=app.config["LAN_MODE"],
            settings=app.config["ANALYSIS_SETTINGS"],
        )

    def run_analysis(rows: list[dict[str, str]], source_name: str):
        missing = validate_columns(rows[0].keys() if rows else None)
        if missing:
            flash("Faltan columnas: " + ", ".join(missing), "error")
            return redirect(url_for("index"))
        findings, errors = analyze(rows, app.config["ANALYSIS_SETTINGS"])
        app.config["RESULTS"] = [asdict(item) for item in findings]
        app.config["SOURCE_NAME"] = source_name
        if errors:
            flash(f"Se omitieron {len(errors)} filas inválidas. La primera: {errors[0]}", "warning")
        flash(f"Análisis terminado: {len(findings)} operaciones revisadas.", "success")
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
            text = uploaded.stream.read().decode("utf-8-sig")
            rows = list(csv.DictReader(io.StringIO(text)))
        except (UnicodeDecodeError, csv.Error) as exc:
            flash(f"No se pudo leer el CSV: {exc}", "error")
            return redirect(url_for("index"))
        return run_analysis(rows, Path(uploaded.filename).name)

    @app.post("/demo")
    @require_access
    def demo():
        return run_analysis(list(SAMPLE_ROWS), "demostración sintética")

    @app.get("/plantilla")
    @require_access
    def template_csv():
        """Download a ready-to-open example for Excel and similar tools."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerow(SAMPLE_ROWS[0])
        return Response(
            "\ufeff" + output.getvalue(),
            mimetype="text/csv; charset=utf-8",
            headers={"Content-Disposition": "attachment; filename=plantilla_guardian.csv"},
        )

    @app.get("/export")
    @require_access
    def export():
        output = io.StringIO()
        fields = [*REQUIRED_COLUMNS, "score", "level", "reasons"]
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for result in app.config["RESULTS"]:
            writer.writerow({**result, "reasons": " | ".join(result["reasons"])})
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

