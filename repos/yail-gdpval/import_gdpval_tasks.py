"""Generate HUD task packages from the public openai/gdpval gold subset.

This is an authoring-time importer. It downloads solver-visible reference
files and hidden expert deliverables from Hugging Face, writes task packages
under ``tasks/<slug>/``, and stores the GDPval rubric in ``_hidden/rubric.json``.

Generated tasks use ``gdpval_generic_grader.grade``. They are intended to expand
the curriculum quickly; hand-port high-value rows later when deterministic
checks need to be stronger.
"""

from __future__ import annotations

import argparse
import json
import re
import textwrap
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import deliverable_io as dio


ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "tasks"
DATASET = "openai/gdpval"
ROWS_API = "https://datasets-server.huggingface.co/rows"
SUPPORTED_EXTS = {".xlsx", ".docx", ".pptx", ".pdf"}
REQUIRED_AXES = {
    "factual_accuracy": "Correctness of facts, calculations, conclusions, and domain-specific claims.",
    "professional_judgment": "Quality of expert choices, assumptions, prioritization, and business reasoning.",
    "evidence_grounding": "Uses the staged reference material and avoids unsupported claims.",
    "completeness": "Covers the requested deliverable, sections, outputs, and required details.",
    "format_regulatory_compliance": "Matches requested file type, naming, structure, and any compliance constraints.",
    "clarity": "Readable, organized, and appropriate for the target business audience.",
}


def fetch_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset in range(0, 220, 100):
        url = f"{ROWS_API}?dataset={urllib.parse.quote(DATASET)}&config=default&split=train&offset={offset}&length=100"
        with urllib.request.urlopen(url, timeout=90) as resp:
            rows.extend(item["row"] for item in json.load(resp)["rows"])
    return rows


def slugify(row: dict[str, Any]) -> str:
    occupation = str(row.get("occupation") or "task").lower()
    stem = re.sub(r"[^a-z0-9]+", "-", occupation).strip("-")[:42]
    return f"gdpval-{stem}-{str(row['task_id'])[:8]}"


def ext_of(path: str) -> str:
    return Path(path).suffix.lower()


def file_name(path_or_url: str) -> str:
    path = urllib.parse.urlparse(path_or_url).path if "://" in path_or_url else path_or_url
    return urllib.parse.unquote(Path(path).name)


def choose_rows(rows: list[dict[str, Any]], limit: int, include_existing: bool) -> list[dict[str, Any]]:
    existing_ids = existing_gdpval_ids() if not include_existing else set()
    candidates: list[dict[str, Any]] = []
    for row in rows:
        if row.get("task_id") in existing_ids:
            continue
        refs = row.get("reference_file_urls") or []
        deliverables = row.get("deliverable_files") or []
        deliverable_urls = row.get("deliverable_file_urls") or []
        if not refs or len(refs) > 4:
            continue
        if len(deliverables) != 1 or len(deliverable_urls) != 1:
            continue
        if ext_of(deliverables[0]) not in SUPPORTED_EXTS:
            continue
        candidates.append(row)

    # Round-robin by sector for a less same-shaped starter curriculum.
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in candidates:
        buckets.setdefault(str(row.get("sector") or "unknown"), []).append(row)
    chosen: list[dict[str, Any]] = []
    while len(chosen) < limit and any(buckets.values()):
        for sector in sorted(buckets):
            if buckets[sector] and len(chosen) < limit:
                chosen.append(buckets[sector].pop(0))
    return chosen


def existing_gdpval_ids() -> set[str]:
    ids: set[str] = set()
    for task_py in TASKS_DIR.glob("*/task.py"):
        text = task_py.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'GDPVAL_TASK_ID\s*=\s*["\']([^"\']+)["\']', text)
        if match:
            ids.add(match.group(1))
    return ids


def download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "yail-gdpval-importer/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return len(data)


def extract_hidden_expert_text(paths: list[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        text = dio.extract_text(path)
        if text.strip():
            chunks.append(f"## {path.name}\n{text}")
    return "\n\n".join(chunks)[:90000]


def build_rubric(row: dict[str, Any], expected_name: str, expected_ext: str, expert_text: str) -> dict[str, Any]:
    rubric_pretty = str(row.get("rubric_pretty") or "")
    rubric_json_raw = row.get("rubric_json")
    try:
        rubric_items = json.loads(rubric_json_raw) if isinstance(rubric_json_raw, str) else rubric_json_raw
    except json.JSONDecodeError:
        rubric_items = []
    penalize = [
        "wrong or missing deliverable file",
        "claims not supported by staged reference files",
        "missing required sections from the GDPval rubric",
        "shallow summary when the task asks for analysis or a native artifact",
    ]
    return {
        "correct_analysis": rubric_pretty[:20000],
        "do_not_overreward": penalize,
        "axis_definitions": REQUIRED_AXES,
        "llm_judge_reference": {
            "task_goal": str(row.get("prompt") or "")[:4000],
            "hidden_reference": rubric_pretty[:25000],
            "credit": "Credit submissions that satisfy the GDPval human rubric using the staged reference material.",
            "penalize": "; ".join(penalize),
        },
        "rubric_pretty": rubric_pretty,
        "rubric_items": rubric_items,
        "expert_deliverable_text": expert_text,
        "expected_deliverable_name": expected_name,
        "expected_deliverable_ext": expected_ext,
        "min_text_chars": 700 if expected_ext != ".xlsx" else 250,
        "source_summary": {
            "dataset": DATASET,
            "task_id": row.get("task_id"),
            "sector": row.get("sector"),
            "occupation": row.get("occupation"),
            "reference_files": row.get("reference_files") or [],
            "deliverable_files": row.get("deliverable_files") or [],
        },
    }


def task_prompt(row: dict[str, Any], deliverable_path: str) -> str:
    prompt = str(row.get("prompt") or "").strip()
    return (
        f"{prompt}\n\n"
        f"Use the staged files under `reference_files/`. Save the final deliverable exactly at "
        f"`{deliverable_path}`. Do not put the final answer only in chat; the file is the graded artifact."
    )


def write_task(row: dict[str, Any], *, force: bool) -> str:
    slug = slugify(row)
    task_dir = TASKS_DIR / slug
    if task_dir.exists() and not force:
        return f"skip existing {slug}"

    refs = row.get("reference_file_urls") or []
    ref_names = [file_name(item) for item in (row.get("reference_files") or refs)]
    deliverable_source = (row.get("deliverable_files") or ["deliverable/output" + ext_of(row["deliverable_file_urls"][0])])[0]
    expected_name = file_name(deliverable_source)
    expected_ext = ext_of(expected_name)
    deliverable_path = f"deliverable/{expected_name}"

    task_dir.mkdir(parents=True, exist_ok=True)
    ref_dir = task_dir / "reference_files"
    hidden_dir = task_dir / "_hidden"
    hidden_deliverables = hidden_dir / "expert_deliverables"
    ref_dir.mkdir(exist_ok=True)
    hidden_deliverables.mkdir(parents=True, exist_ok=True)

    for url, name in zip(refs, ref_names):
        download(url, ref_dir / name)

    expert_paths: list[Path] = []
    for url in row.get("deliverable_file_urls") or []:
        dest = hidden_deliverables / file_name(url)
        download(url, dest)
        expert_paths.append(dest)

    expert_text = extract_hidden_expert_text(expert_paths)
    rubric = build_rubric(row, expected_name, expected_ext, expert_text)
    (hidden_dir / "rubric.json").write_text(json.dumps(rubric, indent=2), encoding="utf-8")

    prompt = task_prompt(row, deliverable_path)
    task_py = f'''"""Generated GDPval task from {DATASET}.

Source task_id: {row["task_id"]}
Sector: {row.get("sector")}
Occupation: {row.get("occupation")}
"""

from __future__ import annotations

GDPVAL_TASK_ID = {row["task_id"]!r}
TASK_SLUG = {slug!r}
DELIVERABLE = {deliverable_path!r}
PROMPT = {prompt!r}

TASK_ARGS = {{"prompt": PROMPT, "task_slug": TASK_SLUG, "deliverable": DELIVERABLE}}
'''
    (task_dir / "task.py").write_text(task_py, encoding="utf-8")
    (task_dir / "grader.py").write_text("from gdpval_generic_grader import grade\n", encoding="utf-8")
    build_script = f'''"""Verify generated GDPval reference files for {slug}."""

from pathlib import Path

EXPECTED = {ref_names!r}

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    missing = [name for name in EXPECTED if not (here / "reference_files" / name).is_file()]
    if missing:
        raise SystemExit(f"missing generated reference files: {{missing}}")
    print(f"[{slug}] generated reference files verified: {{len(EXPECTED)}}")
'''
    (task_dir / "build_reference_files.py").write_text(build_script, encoding="utf-8")
    return f"generated {slug} refs={len(refs)} deliverable={expected_name}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--include-existing", action="store_true")
    parser.add_argument("--list", action="store_true", help="List selected rows without writing files")
    args = parser.parse_args()

    rows = fetch_rows()
    selected = choose_rows(rows, args.limit, args.include_existing)
    if args.list:
        for row in selected:
            deliverable = (row.get("deliverable_files") or [""])[0]
            print(
                f"{slugify(row)}\t{row.get('sector')}\t{row.get('occupation')}\t"
                f"refs={len(row.get('reference_file_urls') or [])}\tdeliverable={file_name(deliverable)}"
            )
        return 0

    for row in selected:
        print(write_task(row, force=args.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
