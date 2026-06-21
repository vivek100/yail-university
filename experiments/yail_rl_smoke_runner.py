"""Run a minimal HUD RL smoke for a YAIL PhD candidate.

This script is deliberately small and auditable:

1. Optionally fork a HUD trainable base model.
2. Run one grouped HUD taskset batch with token IDs recorded.
3. Send the grouped trajectories to ``hud.train.TrainingClient.step``.
4. Write a JSON report that the YAIL UI/docs can cite.

It does not mark an agent as graduated. Graduation needs a follow-up eval on a
held-out task after the checkpoint is created.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from hud import Taskset
from hud.agents.openai_compatible.agent import OpenAIChatAgent
from hud.agents.types import OpenAIChatConfig
from hud.eval import HostedRuntime
from hud.train import TrainingClient


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "repos" / "yail-gdpval"
RESULTS_DIR = ROOT / "results"
DEFAULT_PROMPT = ROOT / "yail-university" / "versions" / "dr-atlas-v1-rl-candidate" / "agent.md"
DEFAULT_HUD = REPO / ".venv" / "Scripts" / "hud.exe"


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


def to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, list | tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if hasattr(value, "model_dump"):
        return to_jsonable(value.model_dump())
    if hasattr(value, "__dict__"):
        return {
            key: to_jsonable(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return str(value)


def summarize_runs(job: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run in job.runs:
        rows.append(
            {
                "trace_id": getattr(run, "id", None),
                "status": getattr(run, "status", None),
                "reward": getattr(run, "reward", None),
                "error": getattr(run, "error", None),
                "task_id": getattr(getattr(run, "task", None), "id", None),
            }
        )
    return rows


def reward_stats(runs: list[dict[str, Any]]) -> dict[str, Any]:
    rewards = sorted(float(row["reward"]) for row in runs if row.get("reward") is not None)
    return {
        "rewards": rewards,
        "min_reward": min(rewards) if rewards else None,
        "max_reward": max(rewards) if rewards else None,
        "mean_reward": sum(rewards) / len(rewards) if rewards else None,
        "unique_rewards": sorted(set(rewards)),
        "completed_runs": len(rewards),
    }


def hud_command() -> str:
    return str(DEFAULT_HUD) if DEFAULT_HUD.is_file() else "hud"


def fork_model(source_model: str, fork_name: str, env: dict[str, str]) -> str:
    proc = subprocess.run(
        [hud_command(), "models", "fork", source_model, "--name", fork_name, "--json"],
        cwd=REPO,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"model fork failed: {proc.stderr or proc.stdout}")
    data = json.loads(proc.stdout)
    for key in ("model_name", "slug", "name"):
        if data.get(key):
            return str(data[key])
    raise RuntimeError(f"could not find fork slug in response: {data}")


def select_taskset(source: str, task_id: str) -> Taskset:
    taskset = Taskset.from_api(source)
    selected = [
        task
        for slug, task in taskset.items()
        if slug == task_id or task.id == task_id
    ]
    if not selected:
        raise ValueError(f"task {task_id!r} not found in taskset {source!r}")
    return Taskset(taskset.name, selected, origin=taskset.origin)


async def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    env = dict(os.environ)
    env.update(load_env_file(Path(args.env_file).resolve()))
    env.setdefault("HUD_API_URL", "https://api.beta.hud.ai")
    os.environ.update(env)

    model_slug = args.model_slug
    forked = False
    if not model_slug:
        stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        fork_name = args.fork_name or f"yail-dr-atlas-qwen30b-smoke-{stamp}"
        model_slug = fork_model(args.base_model, fork_name, env)
        forked = True

    prompt = Path(args.system_prompt_file).read_text(encoding="utf-8")
    taskset = select_taskset(args.taskset, args.task_id)
    agent = OpenAIChatAgent(
        OpenAIChatConfig(
            model=model_slug,
            max_steps=args.max_steps,
            auto_respond=True,
            system_prompt=prompt,
            completion_kwargs={"extra_body": {"return_token_ids": True}},
        )
    )

    trainer = TrainingClient(model_slug)
    available_losses = await trainer.available_losses()
    loss_fn = args.loss_fn
    if loss_fn not in available_losses:
        loss_fn = "importance_sampling" if "importance_sampling" in available_losses else available_losses[0]

    started = datetime.now(UTC).isoformat()
    job = await taskset.run(
        agent,
        runtime=HostedRuntime(),
        group=args.group,
        max_concurrent=args.max_concurrent,
    )
    runs = summarize_runs(job)
    stats = reward_stats(runs)
    if stats["completed_runs"] != args.group or len(stats["unique_rewards"]) < 2:
        return {
            "schema_version": 1,
            "status": "blocked_before_training",
            "reason": "Grouped trajectories did not produce a complete non-constant reward batch.",
            "started_at": started,
            "finished_at": datetime.now(UTC).isoformat(),
            "model_slug": model_slug,
            "forked": forked,
            "taskset": args.taskset,
            "task_id": args.task_id,
            "group": args.group,
            "loss_fn_requested": args.loss_fn,
            "available_losses": available_losses,
            "runs": runs,
            "reward_stats": stats,
        }

    train_result = await trainer.step(
        job.runs,
        learning_rate=args.learning_rate,
        loss_fn=loss_fn,
        group_size=args.group,
    )
    head = await trainer.head()
    checkpoints = await trainer.checkpoints()

    return {
        "schema_version": 1,
        "status": "training_step_completed",
        "started_at": started,
        "finished_at": datetime.now(UTC).isoformat(),
        "model_slug": model_slug,
        "forked": forked,
        "base_model": args.base_model,
        "taskset": args.taskset,
        "task_id": args.task_id,
        "group": args.group,
        "max_steps": args.max_steps,
        "learning_rate": args.learning_rate,
        "loss_fn_requested": args.loss_fn,
        "loss_fn_used": loss_fn,
        "available_losses": available_losses,
        "job_id": getattr(job, "id", None),
        "job_url": f"https://hud.ai/jobs/{getattr(job, 'id', '')}",
        "runs": runs,
        "reward_stats": stats,
        "train_result": to_jsonable(train_result),
        "head": to_jsonable(head),
        "checkpoint_count": len(checkpoints),
        "checkpoints_tail": to_jsonable(checkpoints[-5:]),
        "graduation_status": "needs_post_training_eval",
        "next_step": "Run the trained checkpoint on a held-out GDPval or autonomous-business capstone task.",
    }


def write_report(report: dict[str, Any], output: str) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if output:
        path = Path(output).resolve()
    else:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        path = RESULTS_DIR / f"yail-rl-smoke-{stamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-model", default="Qwen/Qwen3-30B-A3B")
    parser.add_argument("--model-slug", default="", help="Existing trainable fork slug. If omitted, create a fork.")
    parser.add_argument("--fork-name", default="")
    parser.add_argument("--taskset", default="yail-phd-training-mix")
    parser.add_argument("--task-id", default="acct-audit-easy")
    parser.add_argument("--group", type=int, default=4)
    parser.add_argument("--max-concurrent", type=int, default=1)
    parser.add_argument("--max-steps", type=int, default=30)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--loss-fn", default="ppo")
    parser.add_argument("--env-file", default=str(ROOT / "env.local"))
    parser.add_argument("--system-prompt-file", default=str(DEFAULT_PROMPT))
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = asyncio.run(run_smoke(args))
    output = write_report(report, args.output)
    print(json.dumps({"report": str(output), "status": report["status"]}, indent=2))
    return 0 if report["status"] == "training_step_completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
