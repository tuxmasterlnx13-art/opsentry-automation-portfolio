"""Synthetic portfolio dashboard; it never reads production data."""

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

SYNTHETIC_CASES = [
    {"id": "DEMO-001", "type": "Router mismatch", "state": "Assigned"},
    {"id": "DEMO-002", "type": "Serial mismatch", "state": "Pending verification"},
    {"id": "DEMO-003", "type": "IP duplicate", "state": "Resolved"},
]

PAGE = """
<!doctype html><html lang="en"><meta charset="utf-8"><title>OPSENTRY Demo</title>
<style>body{font-family:system-ui;margin:3rem;max-width:70rem}table{border-collapse:collapse;width:100%}th,td{padding:.7rem;border-bottom:1px solid #ddd;text-align:left}</style>
<h1>OPSENTRY synthetic dashboard</h1><p>Portfolio demo — no production connection.</p>
<table><tr><th>Case</th><th>Finding</th><th>State</th></tr>{% for item in cases %}<tr><td>{{item.id}}</td><td>{{item.type}}</td><td>{{item.state}}</td></tr>{% endfor %}</table>
"""


@app.get("/")
def index():
    return render_template_string(PAGE, cases=SYNTHETIC_CASES)


@app.get("/api/cases")
def cases():
    return jsonify(SYNTHETIC_CASES)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

