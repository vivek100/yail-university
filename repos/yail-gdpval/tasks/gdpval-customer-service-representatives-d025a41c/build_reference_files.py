"""Verify generated GDPval reference files for gdpval-customer-service-representatives-d025a41c."""

from pathlib import Path

EXPECTED = ['Case Three.docx', 'Case Two.docx', 'Case One.docx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-customer-service-representatives-d025a41c] generated reference files verified: {len(EXPECTED)}")
