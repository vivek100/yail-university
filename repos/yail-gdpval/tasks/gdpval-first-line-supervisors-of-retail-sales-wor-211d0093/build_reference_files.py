"""Verify generated GDPval reference files for gdpval-first-line-supervisors-of-retail-sales-wor-211d0093."""

from pathlib import Path

EXPECTED = ['Daily Tasks.docx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-first-line-supervisors-of-retail-sales-wor-211d0093] generated reference files verified: {len(EXPECTED)}")
