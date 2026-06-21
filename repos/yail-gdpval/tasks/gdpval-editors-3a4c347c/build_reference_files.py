"""Verify generated GDPval reference files for gdpval-editors-3a4c347c."""

from pathlib import Path

EXPECTED = ['Boilerplate.docx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-editors-3a4c347c] generated reference files verified: {len(EXPECTED)}")
