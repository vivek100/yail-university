"""Verify generated GDPval reference files for gdpval-compliance-officers-dfb4e0cd."""

from pathlib import Path

EXPECTED = ['Award Data Report.xlsx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-compliance-officers-dfb4e0cd] generated reference files verified: {len(EXPECTED)}")
