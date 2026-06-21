"""Compact GDPval-derived AFC audit sampling task for RL signal checks."""

from __future__ import annotations

GDPVAL_TASK_ID = "83d10b06-26d1-4636-a32c-23f92c57f30b"
TASK_SLUG = "acct-audit-easy"
DELIVERABLE = "deliverable/Sample.xlsx"

PROMPT = """You're helping internal audit test the Anti-Financial-Crime risk metrics reported
for Q2 and Q3 2024. The compact population is in `reference_files/Population easy.xlsx`.
It has one row per KRI with the Division, Sub-Division, Country, Legal Entity, KRI name,
and Q3/Q2 values.

Please create a workbook saved exactly as `deliverable/Sample.xlsx`:

1. Add a "Sample Size Calculation" tab. Use a simple, documented approach for a 90%
   confidence level and 10% tolerable error rate, then state the sample size you chose.
2. Add a "Risk Analysis" tab that computes quarter-on-quarter variance for each KRI.
3. Add a "Selected Sample" tab with a risk-based audit sample of 12 to 30 rows. Prioritise
   items with large QoQ variance, zero Q2/Q3 values, and high-risk jurisdictions. Cover at
   least three divisions and three countries.
4. Keep the source row identifier ("No"), flag selected rows, and include a short rationale
   for each selected row.

The point is a defensible audit sample, not selecting the whole population.

You have spreadsheet tools available. A good workflow is: use `read_xlsx` to inspect
the population, choose 12-30 source row IDs, then call `write_audit_sample_workbook`
with those selected IDs to create the workbook.
"""

GRADER_CONFIG = {
    "axes": [
        "factual_accuracy",
        "professional_judgment",
        "evidence_grounding",
        "completeness",
        "format_regulatory_compliance",
        "clarity",
    ],
    "det_weight": 0.78,
    "deliverable": DELIVERABLE,
}

TASK_ARGS = {"prompt": PROMPT, "task_slug": TASK_SLUG, "deliverable": DELIVERABLE}


def build_task():
    from hud.eval.task import Task

    return Task(
        env={"name": "gdpval-template"},
        scenario="gdpval_task",
        slug=TASK_SLUG,
        args=TASK_ARGS,
        metadata={
            "gdpval_task_id": GDPVAL_TASK_ID,
            "occupation": "Accountants and Auditors",
            "sector": "Professional, Scientific, and Technical Services",
            "deliverable_format": "xlsx",
            "bundle_status": "compact_authentic_gdpval_reference_file",
            "grader_det_weight": GRADER_CONFIG["det_weight"],
            "primary_failure_mode": "spread-friendly risk sampling and workbook construction",
        },
    )
