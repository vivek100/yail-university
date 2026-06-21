"""Verify generated GDPval reference files for gdpval-accountants-and-auditors-7b08cd4d."""

from pathlib import Path

EXPECTED = ['Fall Music Tour Ref File.xlsx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-accountants-and-auditors-7b08cd4d] generated reference files verified: {len(EXPECTED)}")
