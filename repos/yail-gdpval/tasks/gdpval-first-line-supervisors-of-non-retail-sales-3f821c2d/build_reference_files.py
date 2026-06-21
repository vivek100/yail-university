"""Verify generated GDPval reference files for gdpval-first-line-supervisors-of-non-retail-sales-3f821c2d."""

from pathlib import Path

EXPECTED = ['Sales & Stock Last Year Data.xlsx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-first-line-supervisors-of-non-retail-sales-3f821c2d] generated reference files verified: {len(EXPECTED)}")
