"""Échoue si un module de l'intégration a une couverture (lignes+branches) <= seuil.

Usage : python tools/check_coverage.py coverage.json [seuil=95]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    report = json.loads(Path(argv[1]).read_text())
    threshold = float(argv[2]) if len(argv) > 2 else 95.0
    expected = {p.as_posix() for p in Path("custom_components/phase_lune").rglob("*.py")}
    files = report["files"]
    missing = sorted(expected - set(files))
    bad = {f: d["summary"]["percent_covered"] for f, d in files.items()
           if d["summary"]["percent_covered"] <= threshold}
    for f in sorted(files):
        print(f"{files[f]['summary']['percent_covered']:6.2f}%  {f}")
    if missing:
        print("Modules absents du rapport :", ", ".join(missing))
    if bad:
        print(f"Modules <= {threshold}% :", bad)
    return 1 if missing or bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
