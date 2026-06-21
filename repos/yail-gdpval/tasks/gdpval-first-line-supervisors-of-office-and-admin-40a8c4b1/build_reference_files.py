"""Verify generated GDPval reference files for gdpval-first-line-supervisors-of-office-and-admin-40a8c4b1."""

from pathlib import Path

EXPECTED = ['Priorities and Conditions for Scheduling Grand Rounds.docx', 'Scheduled Meetings.docx', 'Grand Rounds Template.xlsx']

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {missing}")
    print(f"[gdpval-first-line-supervisors-of-office-and-admin-40a8c4b1] generated reference files verified: {len(EXPECTED)}")
