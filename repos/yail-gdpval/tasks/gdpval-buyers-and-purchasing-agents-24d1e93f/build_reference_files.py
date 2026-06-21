"""Verify generated GDPval reference files for gdpval-buyers-and-purchasing-agents-24d1e93f."""

from pathlib import Path

EXPECTED = ['Quotations and volume projection for model I headlamp.docx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-buyers-and-purchasing-agents-24d1e93f] generated reference files verified: {len(EXPECTED)}")
