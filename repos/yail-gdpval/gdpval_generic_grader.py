"""Generic grader for generated GDPval tasks.

The hand-ported GDPval tasks keep custom deterministic graders. Generated tasks
use this fallback: verify the requested native artifact exists and is parseable,
then ask HUD's native LLM judge to compare the submission against the GDPval
rubric and expert deliverable text embedded in the task rubric.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import deliverable_io as dio
import native_grading

DET_WEIGHT = 0.35
AXIS_WEIGHTS = {
    "factual_accuracy": 0.28,
    "professional_judgment": 0.18,
    "evidence_grounding": 0.18,
    "completeness": 0.18,
    "format_regulatory_compliance": 0.12,
    "clarity": 0.06,
}


def _expected_suffix(key: dict[str, Any]) -> str:
    suffix = str(key.get("expected_deliverable_ext") or "").strip().lower()
    return suffix if suffix.startswith(".") else f".{suffix}" if suffix else ""


def _format_checks(deliverable: Path, submitted_text: str, key: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    expected_suffix = _expected_suffix(key)
    expected_name = str(key.get("expected_deliverable_name") or "").strip().lower()
    suffix_ok = 1.0 if not expected_suffix or deliverable.suffix.lower() == expected_suffix else 0.0
    basename_ok = 1.0 if not expected_name or deliverable.name.lower() == expected_name else 0.5

    parseable = 0.0
    structure_detail: dict[str, Any] = {}
    suffix = deliverable.suffix.lower()
    if suffix == ".xlsx":
        sheets = dio.read_xlsx(deliverable)
        nonempty_rows = sum(max(0, len(rows) - 1) for rows in sheets.values())
        parseable = 1.0 if sheets and nonempty_rows > 0 else 0.0
        structure_detail = {"sheet_count": len(sheets), "nonempty_rows": nonempty_rows}
    elif suffix == ".pptx":
        slides = dio.read_pptx_slides(deliverable)
        parseable = 1.0 if slides and any(slide.strip() for slide in slides) else 0.0
        structure_detail = {"slide_count": len(slides)}
    elif suffix in {".docx", ".pdf"}:
        parseable = 1.0 if submitted_text.strip() else 0.0
        structure_detail = {"text_chars": len(submitted_text)}
    else:
        parseable = 1.0 if submitted_text.strip() else 0.0
        structure_detail = {"text_chars": len(submitted_text)}

    min_chars = int(key.get("min_text_chars") or 600)
    content_volume = min(1.0, len(submitted_text.strip()) / min_chars) if min_chars > 0 else 1.0
    checks = {
        "suffix_ok": suffix_ok,
        "basename_ok": basename_ok,
        "parseable_native_file": parseable,
        "content_volume": round(content_volume, 4),
    }
    weights = {
        "suffix_ok": 0.22,
        "basename_ok": 0.14,
        "parseable_native_file": 0.34,
        "content_volume": 0.30,
    }
    score = sum(checks[name] * weights[name] for name in weights)
    return score, {
        "checks": checks,
        "weights": weights,
        "score": round(score, 6),
        "expected_suffix": expected_suffix,
        "expected_name": expected_name,
        "actual_name": deliverable.name,
        **structure_detail,
    }


def _reference_context(key: dict[str, Any], det_detail: dict[str, Any]) -> str:
    source_summary = key.get("source_summary") or {}
    expert_text = str(key.get("expert_deliverable_text") or "")
    rubric_pretty = str(key.get("rubric_pretty") or "")
    return "\n\n".join(
        [
            f"## Deterministic file diagnostics\n{det_detail}",
            f"## Source task metadata\n{source_summary}",
            f"## GDPval human rubric\n{rubric_pretty[:35000]}",
            f"## Expert deliverable text excerpt\n{expert_text[:45000]}",
        ]
    )


async def grade(workspace: Path, deliverable: Path, key: dict[str, Any]) -> dict[str, Any]:
    if not deliverable.is_file():
        return {"reward": 0.0, "info": {"status": "missing_deliverable"}}
    submitted = dio.extract_text(deliverable)
    det_score, det_detail = _format_checks(deliverable, submitted, key)
    if det_score <= 0.05:
        return {
            "reward": 0.0,
            "info": {"status": "unparseable_or_wrong_format", "deterministic": det_detail},
        }
    return await native_grading.blend_with_native_judge(
        det_score=det_score,
        det_weight=DET_WEIGHT,
        det_detail=det_detail,
        key=key,
        axis_weights=AXIS_WEIGHTS,
        submitted=submitted[:70000],
        extra_instruction=(
            "Grade against the GDPval human rubric and expert deliverable. Reward equivalent "
            "professional work, not exact wording. Penalize missing required sections, unsupported "
            "facts, wrong file type, shallow summaries, and outputs that ignore the staged references."
        ),
        reference_context=_reference_context(key, det_detail),
    )
