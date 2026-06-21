"""Verify generated GDPval reference files for gdpval-child-family-and-school-social-workers-76d10872."""

from pathlib import Path

EXPECTED = ['Paternity Test Results for Michael Reynolds (Case PT-2025-1782).pdf', 'Order of Child Support for Michael Reynolds (Case PT-2025-1782).pdf', 'Case Detail Summary for Michael Reynolds (Case PT-2025-1782).pdf', 'Case Creation Guide for Michael Reynolds (Case PT-2025-1782).pdf']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-child-family-and-school-social-workers-76d10872] generated reference files verified: {len(EXPECTED)}")
