"""Verify generated GDPval reference files for gdpval-first-line-supervisors-of-office-and-admin-0353ee0c."""

from pathlib import Path

EXPECTED = ['Document A - Email Thread Task 8 Veterans.pdf', 'Document B - PACT Act Links.pdf']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-first-line-supervisors-of-office-and-admin-0353ee0c] generated reference files verified: {len(EXPECTED)}")
