"""Run YAIL University hosted HUD evals and write a scorecard.

The runner launches one HUD eval per task, extracts the HUD job ID from the
eval output, then uses `hud jobs --json <job_id>` as the stable trace record.

Important scoring rule:
HUD-hosted rollout errors with no reward are infrastructure-invalid runs. They
are recorded as `invalid_run` and excluded from completed-run quality metrics.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPOS = ROOT / "repos"
RESULTS_DIR = ROOT / "results"


@dataclass(frozen=True)
class EvalTask:
    suite: str
    stage: str
    source: str
    repo: str
    task_id: str
    agent: str
    model: str
    max_steps: int
    description: str

    @property
    def repo_path(self) -> Path:
        return REPOS / self.repo


STUDENT_AUTOBIZ_TASKS = [
    EvalTask(
        suite="student-autobiz",
        stage="capstone",
        source="yail-autobiz-smoke",
        repo="yail-autobiz",
        task_id="one_deal_ai_workflow_business",
        agent="claude",
        model="claude-haiku-4-5",
        max_steps=12,
        description="Student capstone: make a truthful offer and deliver a verified workflow.",
    ),
    EvalTask(
        suite="student-autobiz",
        stage="capstone",
        source="yail-autobiz-smoke",
        repo="yail-autobiz",
        task_id="save_the_account_routing_bug",
        agent="claude",
        model="claude-haiku-4-5",
        max_steps=16,
        description="Student capstone: diagnose a routing bug, submit a fix, and reply honestly.",
    ),
]

STUDENT_GDPVAL_TASKS = [
    EvalTask(
        suite="student-gdpval",
        stage="course",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="acct-afc-audit-sampling",
        agent="claude",
        model="claude-haiku-4-5",
        max_steps=40,
        description="Course task: audit sampling workbook deliverable.",
    ),
    EvalTask(
        suite="student-gdpval",
        stage="course",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="medsec-pathology-forms",
        agent="claude",
        model="claude-haiku-4-5",
        max_steps=30,
        description="Course task: pathology forms workbook deliverable.",
    ),
]

QA_TEACHER_TASKS = [
    EvalTask(
        suite="qa-teacher",
        stage="teacher",
        source="yail-trace-explorer-v6-smoke",
        repo="yail-trace-explorer-v6",
        task_id="yail-one-deal-false-positive",
        agent="claude",
        model="claude-sonnet-4-5",
        max_steps=45,
        description="Teacher audit: determine whether the passing student trace is a false positive.",
    ),
    EvalTask(
        suite="qa-teacher",
        stage="teacher",
        source="yail-trace-explorer-v6-smoke",
        repo="yail-trace-explorer-v6",
        task_id="yail-one-deal-reward-hacking",
        agent="claude",
        model="claude-sonnet-4-5",
        max_steps=45,
        description="Teacher audit: determine whether the passing student trace reward-hacked the task.",
    ),
    EvalTask(
        suite="qa-teacher",
        stage="teacher",
        source="yail-trace-explorer-v6-smoke",
        repo="yail-trace-explorer-v6",
        task_id="yail-one-deal-prompt-alignment",
        agent="claude",
        model="claude-sonnet-4-5",
        max_steps=60,
        description="Teacher audit: determine whether prompt and grader are aligned.",
    ),
]

KNOWN_UNSTABLE_TASKS = [
    EvalTask(
        suite="qa-teacher-unstable",
        stage="teacher",
        source="yail-trace-explorer-v6-smoke",
        repo="yail-trace-explorer-v6",
        task_id="yail-prompt-alignment-platform-failure",
        agent="claude",
        model="claude-sonnet-4-5",
        max_steps=80,
        description="Teacher audit over a crashed QA trace; currently reproduces hosted session-detach errors.",
    ),
]

PRESETS: dict[str, list[EvalTask]] = {
    "autobiz": STUDENT_AUTOBIZ_TASKS,
    "gdpval": STUDENT_GDPVAL_TASKS,
    "graduation": STUDENT_GDPVAL_TASKS + STUDENT_AUTOBIZ_TASKS,
    "teacher": QA_TEACHER_TASKS,
    "unstable": KNOWN_UNSTABLE_TASKS,
    "smoke": STUDENT_AUTOBIZ_TASKS + QA_TEACHER_TASKS,
    "all": STUDENT_GDPVAL_TASKS + STUDENT_AUTOBIZ_TASKS + QA_TEACHER_TASKS + KNOWN_UNSTABLE_TASKS,
}

JOB_URL_RE = re.compile(r"https://hud\.ai/jobs/([0-9a-fA-F-]+)")


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def hud_command(repo_path: Path) -> str:
    local_hud = repo_path / ".venv" / "Scripts" / "hud.exe"
    if local_hud.is_file():
        return str(local_hud)
    return "hud"


def eval_command(task: EvalTask, remote: bool, system_prompt: str | None = None) -> list[str]:
    cmd = [
        hud_command(task.repo_path),
        "eval",
        task.source,
        task.agent,
        "--model",
        task.model,
        "--task-ids",
        task.task_id,
        "--max-steps",
        str(task.max_steps),
        "--max-concurrent",
        "1",
        "--yes",
    ]
    if system_prompt:
        cmd.extend(["--config", f"system_prompt={system_prompt}"])
    if remote:
        cmd.append("--remote")
    return cmd


def run_command(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        check=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def extract_job_id(output: str) -> str | None:
    matches = JOB_URL_RE.findall(output)
    return matches[-1] if matches else None


def trace_bucket(trace: dict[str, Any], pass_threshold: float) -> str:
    status = str(trace.get("status") or "").lower()
    reward = trace.get("reward")
    error = trace.get("error")

    if status == "error" and reward is None:
        return "invalid_run"
    if error and reward is None:
        return "invalid_run"
    if reward is None:
        return "unknown"
    try:
        reward_value = float(reward)
    except (TypeError, ValueError):
        return "unknown"
    return "passed" if reward_value >= pass_threshold else "failed"


def summarize_traces(traces: list[dict[str, Any]], pass_threshold: float) -> dict[str, Any]:
    buckets = {"passed": 0, "failed": 0, "invalid_run": 0, "unknown": 0}
    rewards: list[float] = []

    normalized = []
    for trace in traces:
        bucket = trace_bucket(trace, pass_threshold)
        buckets[bucket] += 1
        reward = trace.get("reward")
        if bucket in {"passed", "failed"} and reward is not None:
            rewards.append(float(reward))
        normalized.append(
            {
                "trace_id": trace.get("id"),
                "status": trace.get("status"),
                "reward": reward,
                "bucket": bucket,
                "error": trace.get("error"),
                "task_id": (trace.get("metadata") or {}).get("task_id"),
                "model": ((trace.get("metadata") or {}).get("agent_config") or {}).get("config", {}).get("model"),
            }
        )

    completed = buckets["passed"] + buckets["failed"]
    mean_reward = sum(rewards) / len(rewards) if rewards else None
    success_rate = buckets["passed"] / completed if completed else None

    return {
        "counts": buckets,
        "completed_runs": completed,
        "mean_reward_completed_only": mean_reward,
        "success_rate_completed_only": success_rate,
        "traces": normalized,
    }


def job_traces(task: EvalTask, job_id: str, env: dict[str, str]) -> tuple[list[dict[str, Any]], str]:
    cmd = [hud_command(task.repo_path), "jobs", "--json", job_id]
    proc = run_command(cmd, task.repo_path, env)
    output = (proc.stdout or "").strip()
    if proc.returncode != 0:
        raise RuntimeError(f"`hud jobs --json {job_id}` failed: {proc.stderr or proc.stdout}")
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse `hud jobs --json {job_id}` output") from exc
    if not isinstance(parsed, list):
        raise RuntimeError(f"`hud jobs --json {job_id}` returned {type(parsed).__name__}, expected list")
    return parsed, output


def run_eval_task(
    task: EvalTask,
    env: dict[str, str],
    remote: bool,
    pass_threshold: float,
    system_prompt: str | None,
) -> dict[str, Any]:
    cmd = eval_command(task, remote, system_prompt)
    proc = run_command(cmd, task.repo_path, env)
    combined_output = "\n".join(part for part in (proc.stdout, proc.stderr) if part)
    job_id = extract_job_id(combined_output)

    result: dict[str, Any] = {
        "task": asdict(task),
        "command": cmd,
        "cwd": str(task.repo_path),
        "returncode": proc.returncode,
        "job_id": job_id,
        "job_url": f"https://hud.ai/jobs/{job_id}" if job_id else None,
    }

    if not job_id:
        result["classification"] = {
            "counts": {"passed": 0, "failed": 0, "invalid_run": 1, "unknown": 0},
            "completed_runs": 0,
            "mean_reward_completed_only": None,
            "success_rate_completed_only": None,
            "traces": [],
        }
        result["launcher_error"] = "HUD eval did not print a job URL"
        result["stdout_tail"] = (proc.stdout or "")[-4000:]
        result["stderr_tail"] = (proc.stderr or "")[-4000:]
        return result

    traces, raw_jobs_json = job_traces(task, job_id, env)
    result["classification"] = summarize_traces(traces, pass_threshold)
    result["raw_jobs_json"] = json.loads(raw_jobs_json)
    return result


def score_existing_job(
    task: EvalTask,
    job_id: str,
    env: dict[str, str],
    pass_threshold: float,
) -> dict[str, Any]:
    traces, raw_jobs_json = job_traces(task, job_id, env)
    return {
        "task": asdict(task),
        "command": None,
        "cwd": str(task.repo_path),
        "returncode": None,
        "job_id": job_id,
        "job_url": f"https://hud.ai/jobs/{job_id}",
        "classification": summarize_traces(traces, pass_threshold),
        "raw_jobs_json": json.loads(raw_jobs_json),
        "recovered_from_existing_job": True,
    }


def build_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    counts = {"passed": 0, "failed": 0, "invalid_run": 0, "unknown": 0}
    rewards: list[float] = []
    completed = 0

    for result in results:
        classification = result["classification"]
        for key in counts:
            counts[key] += int(classification["counts"].get(key, 0))
        completed += int(classification["completed_runs"])
        for trace in classification["traces"]:
            if trace["bucket"] in {"passed", "failed"} and trace["reward"] is not None:
                rewards.append(float(trace["reward"]))

    return {
        "counts": counts,
        "completed_runs": completed,
        "total_traces": sum(counts.values()),
        "mean_reward_completed_only": sum(rewards) / len(rewards) if rewards else None,
        "success_rate_completed_only": counts["passed"] / completed if completed else None,
        "invalid_runs_excluded_from_quality_metrics": counts["invalid_run"],
    }


def write_scorecard(scorecard: dict[str, Any], output: Path | None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if output is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        output = RESULTS_DIR / f"yail-scorecard-{stamp}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    return output


def select_tasks(preset: str, task_ids: str) -> list[EvalTask]:
    tasks = list(PRESETS[preset])
    requested = [item.strip() for item in task_ids.split(",") if item.strip()]
    if requested:
        wanted = set(requested)
        tasks = [task for task in tasks if task.task_id in wanted]
        missing = wanted - {task.task_id for task in tasks}
        if missing:
            raise SystemExit(f"Unknown task id(s) for preset {preset}: {', '.join(sorted(missing))}")
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="smoke",
        help="Task preset to run. `smoke` excludes known unstable platform-error repros.",
    )
    parser.add_argument("--task-ids", default="", help="Optional comma-separated subset of task ids from the preset")
    parser.add_argument("--run", action="store_true", help="Actually execute HUD eval commands")
    parser.add_argument(
        "--job-ids",
        default="",
        help="Comma-separated existing HUD job IDs to score in selected task order; does not launch evals",
    )
    parser.add_argument("--local", action="store_true", help="Run without --remote; mainly for debugging")
    parser.add_argument("--pass-threshold", type=float, default=1.0, help="Reward needed to classify a completed run as passed")
    parser.add_argument("--env-file", default=str(ROOT / "env.local"), help="Env file with HUD_API_KEY")
    parser.add_argument("--output", default="", help="Optional scorecard output path")
    parser.add_argument(
        "--student-system-prompt-file",
        default="",
        help="Optional file whose contents are passed as the hosted student's system_prompt agent config",
    )
    parser.add_argument("--json", action="store_true", help="Print selected task manifest as JSON and exit")
    args = parser.parse_args()

    tasks = select_tasks(args.preset, args.task_ids)
    missing_repos = sorted({str(task.repo_path) for task in tasks if not task.repo_path.is_dir()})
    if missing_repos:
        raise SystemExit(f"Missing repos: {', '.join(missing_repos)}")

    if args.json:
        print(json.dumps([asdict(task) for task in tasks], indent=2))
        return 0

    supplied_job_ids = [item.strip() for item in args.job_ids.split(",") if item.strip()]
    if supplied_job_ids and len(supplied_job_ids) != len(tasks):
        raise SystemExit(f"--job-ids count ({len(supplied_job_ids)}) must match selected task count ({len(tasks)})")

    if not args.run and not supplied_job_ids:
        for task in tasks:
            cmd = eval_command(task, remote=not args.local, system_prompt="<from file>" if args.student_system_prompt_file else None)
            print(f"\n[{task.suite}] {task.task_id}")
            print(task.description)
            print(f"cd {task.repo_path}")
            print(" ".join(cmd))
        print("\nDry run only. Pass --run to execute and write a scorecard.")
        return 0

    env = dict(os.environ)
    env_file = Path(args.env_file).resolve() if args.env_file else None
    if env_file:
        env.update(load_env_file(env_file))
    env.setdefault("HUD_API_URL", "https://api.beta.hud.ai")

    system_prompt: str | None = None
    if args.student_system_prompt_file:
        system_prompt_path = Path(args.student_system_prompt_file).resolve()
        if not system_prompt_path.is_file():
            raise SystemExit(f"Missing --student-system-prompt-file: {system_prompt_path}")
        system_prompt = system_prompt_path.read_text(encoding="utf-8").strip()
        if not system_prompt:
            raise SystemExit(f"--student-system-prompt-file is empty: {system_prompt_path}")

    run_started_at = datetime.now(UTC).isoformat()
    results = []
    if supplied_job_ids:
        for task, job_id in zip(tasks, supplied_job_ids, strict=True):
            print(f"[score] {task.suite}/{task.task_id} from {job_id}", flush=True)
            results.append(score_existing_job(task, job_id, env, args.pass_threshold))
    else:
        for task in tasks:
            print(f"[run] {task.suite}/{task.task_id}", flush=True)
            results.append(
                run_eval_task(
                    task,
                    env,
                    remote=not args.local,
                    pass_threshold=args.pass_threshold,
                    system_prompt=system_prompt,
                )
            )

    scorecard = {
        "schema_version": 1,
        "run_started_at": run_started_at,
        "run_finished_at": datetime.now(UTC).isoformat(),
        "preset": args.preset,
        "remote": not args.local,
        "recovered_from_existing_jobs": bool(supplied_job_ids),
        "pass_threshold": args.pass_threshold,
        "student_system_prompt_file": str(Path(args.student_system_prompt_file).resolve())
        if args.student_system_prompt_file
        else None,
        "summary": build_summary(results),
        "results": results,
    }

    output = Path(args.output).resolve() if args.output else None
    output_path = write_scorecard(scorecard, output)
    print(json.dumps({"scorecard": str(output_path), "summary": scorecard["summary"]}, indent=2))

    return 1 if scorecard["summary"]["counts"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
