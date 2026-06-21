"""Smoke tasks for the hosted HUD trace-explorer environment.

Run:
    hud task list -s trainingPlan/hud-hackathon/experiments/trace_explorer_smoke_tasks.py
    hud eval trainingPlan/hud-hackathon/experiments/trace_explorer_smoke_tasks.py claude-haiku-4-5 --remote --task-ids sample-analyze --yes -v
"""

from hud import Task
from hud.settings import settings

SAMPLE_TRACE_ID = "c34369f6-3d10-4a58-a35e-7171d7b4df5d"

_sample_analyze = Task(
    env="trace-explorer",
    id="analyze",
    args={
        "trace_id": SAMPLE_TRACE_ID,
        "query": "Summarize what happened in this trace in one sentence.",
        "hud_api_key": settings.api_key,
        "data_sources": ["telemetry"],
    },
    slug="sample-analyze",
)

_sample_analyze_namespaced = _sample_analyze.model_copy(update={"env": "hud-evals/trace-explorer", "slug": "sample-analyze-namespaced"})

tasks = [_sample_analyze, _sample_analyze_namespaced]
