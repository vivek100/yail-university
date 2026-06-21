"""Local QA smoke tasks over traces generated from hud-evals/hud-blank.

This is a temporary v6-compatible stand-in until the real trace-explorer QA
environment is converted/deployed to the v6 registry.

Run:
    hud eval trainingPlan/hud-hackathon/experiments/hud_blank_qa_env.py claude-sonnet-4-5 --task-ids hud-blank-failure-analysis --yes -v --max-steps 20
"""

from pathlib import Path

from hud import Environment

HERE = Path(__file__).resolve().parent
TRACE_DIR = HERE / "traces"

env = Environment(name="hud-blank-qa-smoke")


def _read_trace(name: str) -> str:
    return (TRACE_DIR / name).read_text(encoding="utf-8")


@env.template(id="failure-analysis")
async def failure_analysis(trace_file: str = "hud_blank_eval_order_fail_trace.json"):
    """Ask a QA agent to explain why a hud-blank trace received reward 0."""

    trace = _read_trace(trace_file)
    prompt = f"""You are a QA trace analyst.

Analyze this HUD trace from the `hud-blank` environment and explain why it received reward 0.

Return a concise JSON object with:
- summary
- fault: one of agent | eval | platform | unclear
- evidence: concrete trace evidence
- what_should_have_happened

Trace JSON:
{trace}
"""
    answer = yield prompt

    # Smoke grader: requires the analysis to cite the actual failure evidence.
    text = str(answer).lower()
    mentions_value_three = any(pattern in text for pattern in ("value: 3", "value=3", "value 3"))
    yield 1.0 if ("add" in text and "9" in text and mentions_value_three) else 0.0


_failure = failure_analysis()
_failure.slug = "hud-blank-failure-analysis"

tasks = [_failure]
