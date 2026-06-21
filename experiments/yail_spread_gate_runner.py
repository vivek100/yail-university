"""Run grouped HUD rollouts and classify reward spread for RL readiness.

This is intentionally separate from yail_scorecard_runner.py. Scorecards answer
"did this version pass?" Spread gates answer "does this task produce a training
signal for policy-gradient RL?"
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPOS = ROOT / "repos"
RESULTS_DIR = ROOT / "results"

JOB_URL_RE = re.compile(r"https://hud\.ai/jobs/([0-9a-fA-F-]+)")


@dataclass(frozen=True)
class SpreadTask:
    suite: str
    source: str
    repo: str
    task_id: str
    max_steps: int
    description: str

    @property
    def repo_path(self) -> Path:
        return REPOS / self.repo


SPREAD_TASKS = [
    SpreadTask(
        suite="gdpval",
        source="yail-phd-training-mix",
        repo="yail-gdpval",
        task_id="acct-audit-easy",
        max_steps=30,
        description="Compact authentic GDPval audit task; created to test open-model reward spread before RL.",
    ),
    SpreadTask(
        suite="gdpval",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="acct-afc-audit-sampling",
        max_steps=40,
        description="GDPval spreadsheet/audit task; current known partial rewards exist.",
    ),
    SpreadTask(
        suite="gdpval",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="medsec-pathology-forms",
        max_steps=30,
        description="GDPval spreadsheet/form task; useful no-regression but may saturate.",
    ),
    SpreadTask(
        suite="autobiz",
        source="yail-autobiz-smoke",
        repo="yail-autobiz",
        task_id="one_deal_ai_workflow_business",
        max_steps=12,
        description="Autonomous-business capstone; current strong model passes, trainable model may spread.",
    ),
    SpreadTask(
        suite="autobiz",
        source="yail-autobiz-smoke",
        repo="yail-autobiz",
        task_id="save_the_account_routing_bug",
        max_steps=16,
        description="Autonomous-business account-save capstone; previously had hosted instability.",
    ),
]

GENERATED_GDPVAL_TASKS = [
    SpreadTask(
        suite="gdpval-generated",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="gdpval-accountants-and-auditors-7b08cd4d",
        max_steps=40,
        description="Real GDPval finance workbook task generated from openai/gdpval.",
    ),
    SpreadTask(
        suite="gdpval-generated",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="gdpval-editors-3a4c347c",
        max_steps=40,
        description="Real GDPval editorial DOCX task generated from openai/gdpval.",
    ),
    SpreadTask(
        suite="gdpval-generated",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="gdpval-customer-service-representatives-87da214f",
        max_steps=40,
        description="Real GDPval customer remediation PPTX task generated from openai/gdpval.",
    ),
    SpreadTask(
        suite="gdpval-generated",
        source="yail-gdpval-smoke",
        repo="yail-gdpval",
        task_id="gdpval-first-line-supervisors-of-retail-sales-wor-211d0093",
        max_steps=35,
        description="Real GDPval retail task-list PDF task generated from openai/gdpval.",
    ),
]

PRESETS: dict[str, list[SpreadTask]] = {
    "phd-spread-easy": [SPREAD_TASKS[0]],
    "phd-spread-smoke": [SPREAD_TASKS[1], SPREAD_TASKS[3]],
    "phd-spread-gdpval": SPREAD_TASKS[1:3],
    "phd-spread-gdpval-generated": GENERATED_GDPVAL_TASKS,
    "phd-spread-gdpval-expanded": SPREAD_TASKS[:3] + GENERATED_GDPVAL_TASKS,
    "phd-spread-autobiz": SPREAD_TASKS[3:],
    "phd-spread-all": SPREAD_TASKS,
}


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


def eval_command(
    task: SpreadTask,
    agent: str,
    model: str,
    group: int,
    remote: bool,
    max_concurrent: int,
    system_prompt: str | None,
    auto_respond: bool,
) -> list[str]:
    cmd = [
        hud_command(task.repo_path),
        "eval",
        task.source,
        agent,
        "--model",
        model,
        "--task-ids",
        task.task_id,
        "--max-steps",
        str(task.max_steps),
        "--group",
        str(group),
        "--max-concurrent",
        str(max_concurrent),
        "--yes",
    ]
    if system_prompt:
        cmd.extend(["--config", f"system_prompt={system_prompt}"])
    if auto_respond:
        cmd.append("--auto-respond")
    if remote:
        cmd.append("--remote")
    return cmd


def extract_job_id(output: str) -> str | None:
    matches = JOB_URL_RE.findall(output)
    return matches[-1] if matches else None


def fetch_job_traces(task: SpreadTask, job_id: str, env: dict[str, str]) -> list[dict[str, Any]]:
    cmd = [hud_command(task.repo_path), "jobs", "--json", job_id]
    proc = run_command(cmd, task.repo_path, env)
    if proc.returncode != 0:
        raise RuntimeError(f"`hud jobs --json {job_id}` failed: {proc.stderr or proc.stdout}")
    parsed = json.loads((proc.stdout or "").strip())
    if not isinstance(parsed, list):
        raise RuntimeError(f"`hud jobs --json {job_id}` returned {type(parsed).__name__}, expected list")
    return parsed


def classify_spread(rewards: list[float], invalid_count: int, expected_group: int) -> str:
    if invalid_count:
        return "blocked_by_invalid_runs"
    if len(rewards) < expected_group:
        return "incomplete"
    if not rewards:
        return "no_completed_runs"
    unique = sorted(set(rewards))
    if len(unique) == 1 and unique[0] == 1.0:
        return "saturated_all_pass"
    if len(unique) == 1 and unique[0] == 0.0:
        return "all_zero_investigate"
    if len(unique) == 1:
        return "constant_reward_no_advantage"
    if pstdev(rewards) <= 0.02:
        return "weak_spread"
    return "usable_spread"


def pstdev(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def summarize(task: SpreadTask, traces: list[dict[str, Any]], expected_group: int) -> dict[str, Any]:
    rewards: list[float] = []
    invalid = []
    normalized = []
    for trace in traces:
        reward = trace.get("reward")
        status = trace.get("status")
        error = trace.get("error")
        if reward is None or (str(status).lower() == "error" and error):
            invalid.append(trace)
        else:
            rewards.append(float(reward))
        normalized.append(
            {
                "trace_id": trace.get("id"),
                "status": status,
                "reward": reward,
                "error": error,
                "task_id": (trace.get("metadata") or {}).get("task_id"),
                "model": ((trace.get("metadata") or {}).get("agent_config") or {}).get("config", {}).get("model"),
            }
        )

    rewards_sorted = sorted(rewards)
    return {
        "task": asdict(task),
        "completed_runs": len(rewards),
        "invalid_runs": len(invalid),
        "expected_group": expected_group,
        "rewards": rewards_sorted,
        "unique_rewards": sorted(set(rewards_sorted)),
        "mean_reward": sum(rewards) / len(rewards) if rewards else None,
        "min_reward": min(rewards) if rewards else None,
        "max_reward": max(rewards) if rewards else None,
        "reward_std": pstdev(rewards),
        "spread_classification": classify_spread(rewards, len(invalid), expected_group),
        "traces": normalized,
    }


def write_report(report: dict[str, Any], output: Path | None) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if output is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        output = RESULTS_DIR / f"yail-rl-spread-gate-{stamp}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return output


def build_overall(results: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for result in results:
        key = result["spread"]["spread_classification"]
        counts[key] = counts.get(key, 0) + 1
    usable = counts.get("usable_spread", 0)
    return {
        "spread_classification_counts": counts,
        "usable_task_count": usable,
        "rl_ready": usable > 0 and not counts.get("blocked_by_invalid_runs"),
    }


def select_tasks(preset: str, task_ids: str) -> list[SpreadTask]:
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
    parser.add_argument("--preset", choices=sorted(PRESETS), default="phd-spread-smoke")
    parser.add_argument("--task-ids", default="", help="Optional comma-separated task IDs from the selected preset")
    parser.add_argument("--agent", default="openai_compatible", help="HUD agent type")
    parser.add_argument("--model", default="Qwen/Qwen3.5-4B", help="HUD model_name to evaluate")
    parser.add_argument("--group", type=int, default=2, help="Runs per task")
    parser.add_argument("--max-concurrent", type=int, default=1)
    parser.add_argument("--auto-respond", action="store_true", help="Prompt the agent to continue if it stops early")
    parser.add_argument("--run", action="store_true", help="Execute HUD evals; otherwise print commands only")
    parser.add_argument("--local", action="store_true", help="Do not pass --remote")
    parser.add_argument("--env-file", default=str(ROOT / "env.local"))
    parser.add_argument("--output", default="")
    parser.add_argument("--student-system-prompt-file", default="")
    parser.add_argument("--json", action="store_true", help="Print selected task manifest and exit")
    args = parser.parse_args()

    if args.group < 2:
        raise SystemExit("--group must be >= 2 for a spread gate")

    tasks = select_tasks(args.preset, args.task_ids)
    if args.json:
        print(json.dumps([asdict(task) for task in tasks], indent=2))
        return 0

    system_prompt: str | None = None
    if args.student_system_prompt_file:
        prompt_path = Path(args.student_system_prompt_file).resolve()
        if not prompt_path.is_file():
            raise SystemExit(f"Missing --student-system-prompt-file: {prompt_path}")
        system_prompt = prompt_path.read_text(encoding="utf-8").strip()

    if not args.run:
        for task in tasks:
            cmd = eval_command(
                task,
                agent=args.agent,
                model=args.model,
                group=args.group,
                remote=not args.local,
                max_concurrent=args.max_concurrent,
                system_prompt="<from file>" if system_prompt else None,
                auto_respond=args.auto_respond,
            )
            print(f"\n[{task.suite}] {task.task_id}")
            print(task.description)
            print(f"cd {task.repo_path}")
            print(" ".join(cmd))
        print("\nDry run only. Pass --run to execute.")
        return 0

    env = dict(os.environ)
    env.update(load_env_file(Path(args.env_file).resolve()))
    env.setdefault("HUD_API_URL", "https://api.beta.hud.ai")

    started = datetime.now(UTC).isoformat()
    results = []
    for task in tasks:
        print(f"[spread] {task.suite}/{task.task_id} model={args.model} group={args.group}", flush=True)
        cmd = eval_command(
            task,
            agent=args.agent,
            model=args.model,
            group=args.group,
            remote=not args.local,
            max_concurrent=args.max_concurrent,
            system_prompt=system_prompt,
            auto_respond=args.auto_respond,
        )
        proc = run_command(cmd, task.repo_path, env)
        combined = "\n".join(part for part in (proc.stdout, proc.stderr) if part)
        job_id = extract_job_id(combined)
        result: dict[str, Any] = {
            "task": asdict(task),
            "command": cmd,
            "returncode": proc.returncode,
            "job_id": job_id,
            "job_url": f"https://hud.ai/jobs/{job_id}" if job_id else None,
        }
        if job_id:
            traces = fetch_job_traces(task, job_id, env)
            result["spread"] = summarize(task, traces, args.group)
        else:
            result["spread"] = {
                "task": asdict(task),
                "completed_runs": 0,
                "invalid_runs": args.group,
                "expected_group": args.group,
                "rewards": [],
                "unique_rewards": [],
                "mean_reward": None,
                "min_reward": None,
                "max_reward": None,
                "reward_std": 0.0,
                "spread_classification": "launcher_failed",
                "traces": [],
            }
            result["stdout_tail"] = (proc.stdout or "")[-4000:]
            result["stderr_tail"] = (proc.stderr or "")[-4000:]
        results.append(result)

    report = {
        "schema_version": 1,
        "run_started_at": started,
        "run_finished_at": datetime.now(UTC).isoformat(),
        "preset": args.preset,
        "model": args.model,
        "agent": args.agent,
        "group": args.group,
        "remote": not args.local,
        "auto_respond": args.auto_respond,
        "student_system_prompt_file": str(Path(args.student_system_prompt_file).resolve())
        if args.student_system_prompt_file
        else None,
        "overall": build_overall(results),
        "results": results,
    }
    output = Path(args.output).resolve() if args.output else None
    output_path = write_report(report, output)
    print(json.dumps({"report": str(output_path), "overall": report["overall"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
