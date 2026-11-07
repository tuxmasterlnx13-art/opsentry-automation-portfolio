"""Windows-friendly launcher for local and protected LAN modes."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import secrets
import socket
import threading
import time
import webbrowser

from waitress import serve
from werkzeug.security import generate_password_hash

from .app import create_app


def app_data_dir() -> Path:
    root = os.environ.get("LOCALAPPDATA") or str(Path.home())
    path = Path(root) / "GuardianCommunity"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_or_create_config(*, require_access_key: bool = False, reset_access_key: bool = False) -> tuple[dict[str, str], str | None]:
    path = app_data_dir() / "config.json"
    config: dict[str, str] = {}
    if path.exists():
        config = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    if not config.get("secret_key"):
        config["secret_key"] = secrets.token_urlsafe(48)
        changed = True
    visible_key = None
    if require_access_key and (reset_access_key or not config.get("access_key_hash")):
        visible_key = "FG-" + "-".join(secrets.token_hex(2).upper() for _ in range(2))
        config["access_key_hash"] = generate_password_hash(visible_key)
        changed = True
    if changed:
        path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return config, visible_key


def lan_address() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
            probe.connect(("192.0.2.1", 80))
            return str(probe.getsockname()[0])
    except OSError:
        return socket.gethostbyname(socket.gethostname())


def notify(title: str, message: str) -> None:
    try:
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    except Exception:
        print(f"{title}\n{message}")


def main() -> None:
    parser = argparse.ArgumentParser(description="GUARDIAN Community")
    parser.add_argument("--lan", action="store_true", help="Allow protected company LAN access")
    parser.add_argument("--reset-access-key", action="store_true", help="Generate a new company access key")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    config, new_key = load_or_create_config(require_access_key=args.lan, reset_access_key=args.reset_access_key)
    app = create_app(lan_mode=args.lan, access_key_hash=config.get("access_key_hash"), review_db=str(app_data_dir() / "guardian-reviews.sqlite3"))
    app.secret_key = config["secret_key"]
    host = "0.0.0.0" if args.lan else "127.0.0.1"
    local_url = f"http://127.0.0.1:{args.port}"

    if args.lan:
        share_url = f"http://{lan_address()}:{args.port}"
        key_note = f"\n\nClave inicial: {new_key}" if new_key else "\n\nLa clave existente sigue activa."
        notify("GUARDIAN — acceso de empresa", f"Comparte esta dirección solo dentro de tu red:\n{share_url}{key_note}")

    def open_browser() -> None:
        time.sleep(1)
        webbrowser.open(local_url)

    if os.environ.get("FRAUDGUARD_NO_BROWSER") != "1":
        threading.Thread(target=open_browser, daemon=True).start()
    serve(app, host=host, port=args.port, threads=8)


if __name__ == "__main__":
    main()

