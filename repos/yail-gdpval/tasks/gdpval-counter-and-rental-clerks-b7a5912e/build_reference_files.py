"""Verify generated GDPval reference files for gdpval-counter-and-rental-clerks-b7a5912e."""

from pathlib import Path

EXPECTED = ['Closed Rental Agreements- June 27, 2025.xlsx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-counter-and-rental-clerks-b7a5912e] generated reference files verified: {len(EXPECTED)}")
