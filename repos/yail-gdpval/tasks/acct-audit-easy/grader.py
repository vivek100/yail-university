"""Deterministic-heavy grader for the compact AFC audit task."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import deliverable_io as dio
import native_grading

DET_WEIGHT = 0.78
AXIS_WEIGHTS = {
    "factual_accuracy": 0.24,
    "professional_judgment": 0.24,
    "evidence_grounding": 0.18,
    "completeness": 0.16,
    "format_regulatory_compliance": 0.10,
    "clarity": 0.08,
}


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _norm_id(value: Any) -> str:
    f = _to_float(value)
    if f is not None and f == int(f):
        return str(int(f))
    return str(value).strip()


def _header_index(header: list[str], candidates: tuple[str, ...]) -> int | None:
    normalized = [item.lower().strip() for item in header]
    for candidate in candidates:
        candidate_lower = candidate.lower()
        for idx, item in enumerate(normalized):
            if candidate_lower == item or candidate_lower in item:
                return idx
    return None


def _meets_criterion(row: dict[str, Any], criteria: dict[str, Any]) -> bool:
    country = str(row.get("Country", "")).strip()
    q3 = _to_float(row.get("Q3 2024 KRI"))
    q2 = _to_float(row.get("Q2 2024 KRI"))
    zero = q3 == 0 or q2 == 0
    variance = None if q2 in (None, 0) or q3 is None else (q3 - q2) / q2
    return (
        country in criteria.get("high_risk_countries", [])
        or (criteria.get("zero_value_selects") and zero)
        or (variance is not None and abs(variance) > criteria.get("variance_threshold", 0.15))
    )


def _risk_components(row: dict[str, Any], criteria: dict[str, Any]) -> dict[str, float | bool]:
    country = str(row.get("Country", "")).strip()
    q3 = _to_float(row.get("Q3 2024 KRI"))
    q2 = _to_float(row.get("Q2 2024 KRI"))
    zero = q3 == 0 or q2 == 0
    variance = None if q2 in (None, 0) or q3 is None else abs((q3 - q2) / q2)
    values = [abs(value) for value in (q2, q3) if value is not None]
    materiality = min(math.log10(max(values) + 1) / 10, 1.0) if values else 0.0
    return {
        "high_risk_country": country in criteria.get("high_risk_countries", []),
        "zero_value": bool(criteria.get("zero_value_selects") and zero),
        "large_variance": variance is not None and variance > criteria.get("variance_threshold", 0.15),
        "variance_score": min((variance or 0.0) / 1.0, 1.0),
        "materiality_score": materiality,
    }


def _row_risk_score(row: dict[str, Any], criteria: dict[str, Any]) -> float:
    components = _risk_components(row, criteria)
    return round(
        (0.35 if components["high_risk_country"] else 0.0)
        + (0.25 if components["zero_value"] else 0.0)
        + (0.30 * float(components["variance_score"]))
        + (0.10 * float(components["materiality_score"])),
        6,
    )


def _quality_scores(
    population: dict[str, dict[str, Any]], selected_ids: list[str], criteria: dict[str, Any]
) -> dict[str, Any]:
    if not population or not selected_ids:
        return {
            "risk_quality": 0.0,
            "top_risk_recall": 0.0,
            "criteria_coverage": 0.0,
            "average_selected_risk": 0.0,
            "ideal_average_risk": 0.0,
            "top_risk_selected": 0,
            "top_risk_pool_size": 0,
        }

    ranked = sorted(
        ((row_id, _row_risk_score(row, criteria)) for row_id, row in population.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    selected_set = set(selected_ids)
    selected_scores = [score for row_id, score in ranked if row_id in selected_set]
    sample_size = len(selected_scores)
    ideal_scores = [score for _, score in ranked[:sample_size]]
    avg_selected = sum(selected_scores) / sample_size if sample_size else 0.0
    avg_ideal = sum(ideal_scores) / sample_size if sample_size else 0.0
    risk_quality = min(avg_selected / avg_ideal, 1.0) if avg_ideal else 0.0

    top_pool_size = min(20, len(ranked))
    top_pool = {row_id for row_id, _ in ranked[:top_pool_size]}
    top_risk_selected = len(selected_set & top_pool)
    top_risk_recall = top_risk_selected / top_pool_size if top_pool_size else 0.0

    selected_components = [_risk_components(population[row_id], criteria) for row_id in selected_ids]
    criteria_hits = sum(
        1
        for name in ("high_risk_country", "zero_value", "large_variance")
        if any(bool(components[name]) for components in selected_components)
    )
    return {
        "risk_quality": round(risk_quality, 4),
        "top_risk_recall": round(top_risk_recall, 4),
        "criteria_coverage": round(criteria_hits / 3, 4),
        "average_selected_risk": round(avg_selected, 6),
        "ideal_average_risk": round(avg_ideal, 6),
        "top_risk_selected": top_risk_selected,
        "top_risk_pool_size": top_pool_size,
    }


def _population(workspace: Path) -> dict[str, dict[str, Any]]:
    path = workspace / "reference_files" / "Population easy.xlsx"
    sheets = dio.read_xlsx(path)
    rows = next(iter(sheets.values()), [])
    if not rows:
        return {}
    header = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
    out: dict[str, dict[str, Any]] = {}
    for row in rows[1:]:
        record = dict(zip(header, row))
        key = _norm_id(record.get("No", ""))
        if key:
            out[key] = record
    return out


def _selected_rows(sheets: dict[str, list[list[Any]]], population: dict[str, dict[str, Any]]) -> list[str]:
    selected: list[str] = []
    for sheet_name, rows in sheets.items():
        if not rows:
            continue
        header = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
        no_idx = _header_index(header, ("No", "row id", "source row"))
        selected_idx = _header_index(header, ("selected", "sample flag", "include"))
        if no_idx is None:
            continue
        for row in rows[1:]:
            if no_idx >= len(row):
                continue
            key = _norm_id(row[no_idx])
            if key not in population:
                continue
            flag_value = row[selected_idx] if selected_idx is not None and selected_idx < len(row) else None
            sheet_is_sample = "sample" in sheet_name.lower()
            flagged = sheet_is_sample or str(flag_value).strip().lower() in {"y", "yes", "true", "1", "selected"}
            if flagged:
                selected.append(key)
    return selected


def _has_rationale(sheets: dict[str, list[list[Any]]]) -> bool:
    for rows in sheets.values():
        if not rows:
            continue
        header = [str(cell).lower().strip() if cell is not None else "" for cell in rows[0]]
        rationale_idx = _header_index(header, ("rationale", "reason", "justification"))
        if rationale_idx is None:
            continue
        values = [
            str(row[rationale_idx]).strip()
            for row in rows[1:]
            if rationale_idx < len(row) and row[rationale_idx] is not None
        ]
        if sum(1 for value in values if len(value) >= 8) >= 5:
            return True
    return False


def _deterministic(workspace: Path, deliverable: Path, key: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    sheets = dio.read_xlsx(deliverable)
    text = dio.extract_text(deliverable).lower()
    population = _population(workspace)
    selected = _selected_rows(sheets, population)
    unique_selected = sorted(set(selected), key=lambda item: int(item))
    criteria = key.get("selection_criteria", {})
    meeting = [item for item in unique_selected if _meets_criterion(population[item], criteria)]
    n_pop = len(population)
    n_sel = len(unique_selected)

    divisions = {str(population[item].get("Division", "")).strip() for item in unique_selected}
    countries = {str(population[item].get("Country", "")).strip() for item in unique_selected}
    lo, hi = key.get("sample_size_expectation", {}).get("plausible_n_range", [12, 30])
    precision = len(meeting) / n_sel if n_sel else 0.0
    quality = _quality_scores(population, unique_selected, criteria)
    sample_size_quality = 1.0 if 16 <= n_sel <= 24 else (0.9 if lo <= n_sel <= hi else (0.45 if 1 <= n_sel < n_pop else 0.0))
    coverage = 0.5 * min(len(divisions) / 4, 1.0) + 0.5 * min(len(countries) / 4, 1.0)

    checks = {
        "parseable_xlsx": 1.0 if sheets else 0.0,
        "has_sample_size_tab": 1.0 if any("sample size" in name.lower() for name in sheets) else 0.0,
        "has_risk_analysis_tab": 1.0 if any("risk" in name.lower() or "analysis" in name.lower() for name in sheets) else 0.0,
        "variance_present": 1.0 if "variance" in text or "qoq" in text or "quarter" in text else 0.0,
        "selected_rows_present": 1.0 if n_sel > 0 else 0.0,
        "sample_size_quality": round(sample_size_quality, 4),
        "sample_not_population": 1.0 if 0 < n_sel <= 0.35 * n_pop else 0.0,
        "selection_precision": round(precision, 4),
        "risk_quality": quality["risk_quality"],
        "top_risk_recall": quality["top_risk_recall"],
        "criteria_coverage": quality["criteria_coverage"],
        "coverage": round(coverage, 4),
        "rationale_present": 1.0 if _has_rationale(sheets) else 0.0,
    }
    weights = {
        "parseable_xlsx": 0.06,
        "has_sample_size_tab": 0.05,
        "has_risk_analysis_tab": 0.05,
        "variance_present": 0.06,
        "selected_rows_present": 0.05,
        "sample_size_quality": 0.08,
        "sample_not_population": 0.05,
        "selection_precision": 0.10,
        "risk_quality": 0.20,
        "top_risk_recall": 0.20,
        "criteria_coverage": 0.06,
        "coverage": 0.03,
        "rationale_present": 0.01,
    }
    score = sum(weights[name] * checks[name] for name in weights)
    detail = {
        "checks": checks,
        "weights": weights,
        "score": round(score, 6),
        "population_size": n_pop,
        "selected_size": n_sel,
        "selected_meeting_criterion": len(meeting),
        "selected_ids": unique_selected[:40],
        "divisions_covered": sorted(item for item in divisions if item),
        "countries_covered": sorted(item for item in countries if item),
        "risk_quality": quality,
    }
    return score, detail


def _reference_context(workspace: Path, deliverable: Path, det_detail: dict[str, Any], key: dict[str, Any]) -> str:
    population = _population(workspace)
    selected_ids = det_detail.get("selected_ids", [])
    selected_rows = [population[item] for item in selected_ids if item in population]
    return "\n\n".join(
        [
            f"## Deterministic diagnostics\n{det_detail}",
            f"## Allowed risk criteria\n{key.get('selection_criteria', {})}",
            "## Selected source rows\n" + "\n".join(str(row) for row in selected_rows),
        ]
    )


async def grade(workspace: Path, deliverable: Path, key: dict[str, Any]) -> dict[str, Any]:
    if not deliverable.is_file():
        return {"reward": 0.0, "info": {"status": "missing_deliverable"}}
    det_score, det_detail = _deterministic(workspace, deliverable, key)
    return await native_grading.blend_with_native_judge(
        det_score=det_score,
        det_weight=DET_WEIGHT,
        det_detail=det_detail,
        key=key,
        axis_weights=AXIS_WEIGHTS,
        submitted=dio.extract_text(deliverable)[:40000],
        extra_instruction=(
            "Reward useful partial work, but do not give top-band credit unless the workbook includes "
            "traceable selected rows, risk analysis, and a defensible sample."
        ),
        reference_context=_reference_context(workspace, deliverable, det_detail, key),
    )
