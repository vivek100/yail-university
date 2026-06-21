"""Verify generated GDPval reference files for gdpval-customer-service-representatives-87da214f."""

from pathlib import Path

EXPECTED = ['ID Theft Policy (1).docx', 'Policy Reimbursement Account Sample.xlsx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-customer-service-representatives-87da214f] generated reference files verified: {len(EXPECTED)}")
