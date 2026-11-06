# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

root = Path(SPECPATH).parent / "demo"

a = Analysis(
    [str(root / "run_fraudguard.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "fraudguard" / "templates"), "fraudguard/templates"),
        (str(root / "fraudguard" / "static"), "fraudguard/static"),
    ],
    hiddenimports=["fraudguard.app", "fraudguard.engine", "fraudguard.sample"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FraudGuardCommunity",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="FraudGuardCommunity",
)

