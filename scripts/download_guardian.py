"""Download the latest GUARDIAN Windows installer and verify its SHA-256."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "opsentry-downloader"})
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as target:
        while block := response.read(1024 * 1024):
            target.write(block)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="tuxmasterlnx13-art/opsentry-automation-portfolio")
    parser.add_argument("--destination", type=Path, default=Path("downloads"))
    args = parser.parse_args()
    api = f"https://api.github.com/repos/{args.repo}/releases/latest"
    request = urllib.request.Request(api, headers={"Accept": "application/vnd.github+json", "User-Agent": "opsentry-downloader"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            release = json.load(response)
    except Exception as exc:
        raise SystemExit(f"No published GUARDIAN release is available yet: {exc}")
    assets = {asset["name"]: asset["browser_download_url"] for asset in release.get("assets", [])}
    required = ("Guardian-Community-Setup.exe", "SHA256SUMS.txt")
    if any(name not in assets for name in required):
        raise SystemExit("The latest release does not contain the installer and checksum.")
    args.destination.mkdir(parents=True, exist_ok=True)
    paths = {name: args.destination / name for name in required}
    for name in required:
        download(assets[name], paths[name])
    expected = paths["SHA256SUMS.txt"].read_text(encoding="utf-8-sig").split()[0].lower()
    actual = hashlib.sha256(paths["Guardian-Community-Setup.exe"].read_bytes()).hexdigest()
    if actual != expected:
        paths["Guardian-Community-Setup.exe"].unlink(missing_ok=True)
        raise SystemExit("SHA-256 verification failed; the installer was removed.")
    print(f"Downloaded and verified: {paths['Guardian-Community-Setup.exe'].resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
