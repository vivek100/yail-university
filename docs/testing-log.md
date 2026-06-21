# Testing Log

Use this file to record every HUD experiment in a reproducible way.

## Experiment template

### Date

YYYY-MM-DD

### Goal

What are we trying to prove?

### Environment

```text
repo:
branch/commit:
HUD CLI version:
HUD_API_KEY present: yes/no
model/agent:
runtime: local | hud | remote
```

### Command

```bash
command goes here
```

### Result

```text
job_id:
trace_id:
reward:
status:
```

### What happened

Short summary.

### Failure, if any

Paste the smallest useful error excerpt.

### Next action

What to try next.

---

## 2026-06-20 - hud-blank deploy log review

### Goal

Determine whether the attached CodeBuild log shows an environment setup failure.

### Result

The build/deploy log appears healthy.

Evidence:

```text
BUILD State: SUCCEEDED
POST_BUILD State: SUCCEEDED
UPLOAD_ARTIFACTS State: SUCCEEDED
Introspection OK over the v6 control channel: env 'blank', 2 tasks, 1 capabilities
```

The `uv.lock` warning is benign because the Dockerfile falls back from `uv sync --frozen` to `uv sync`.

### Next action

If remote eval failed, collect:

```bash
hud jobs
hud jobs <job-id>
hud trace <trace-id>
hud trace <trace-id> --json
```

---

## 2026-06-20 - hosted trace-explorer smoke via HUD CLI

### Goal

Run the hosted `trace-explorer` QA environment from the current HUD CLI.

### Setup

HUD CLI installed:

```text
hud-python 0.6.6
```

Smoke task file:

```text
trainingPlan/hud-hackathon/experiments/trace_explorer_smoke_tasks.py
```

The task uses:

```text
env="trace-explorer"
id="analyze"
```

and a second variant:

```text
env="hud-evals/trace-explorer"
id="analyze"
```

### Commands

```bash
hud eval trainingPlan/hud-hackathon/experiments/trace_explorer_smoke_tasks.py claude-haiku-4-5 --remote --task-ids sample-analyze --yes -v --max-steps 20
hud eval trainingPlan/hud-hackathon/experiments/trace_explorer_smoke_tasks.py claude-haiku-4-5 --remote --task-ids sample-analyze-namespaced --yes -v --max-steps 20
```

### Result

Both fail at hosted rollout launch:

```text
No registry found for env 'trace-explorer'
No registry found for env 'hud-evals/trace-explorer'
```

The CLI is configured against:

```text
https://api.beta.hud.ai
https://inference.beta.hud.ai
https://mcp.beta.hud.ai
```

The dashboard curl example uses:

```text
https://api.hud.so/agent/run
```

### Interpretation

This looks like a HUD platform/API mismatch:

- The dashboard-hosted `trace-explorer` exists on the older scenario-style API.
- The installed `hud-python` 0.6.6 CLI submits v6 rollouts to the beta registry.
- That beta registry does not currently contain `trace-explorer`.

### Next action

Ask HUD which of these is intended:

1. A beta/v6 registry ID or env name for the hosted trace-explorer.
2. A valid API key/surface for `https://api.hud.so/agent/run`.
3. Whether we should deploy our own copy of trace-explorer to beta and run QA against that instead.

---

## 2026-06-20 - hud-blank QA smoke task

### Goal

Use `hud-evals/hud-blank` as a small source benchmark, generate a failed HUD trace,
then run a QA-style agent task over that trace.

### Environment

```text
repo: trainingPlan/hud-hackathon/repos/hud-blank
upstream: hud-evals/hud-blank
commit: b85bd01
HUD CLI version: 0.6.6
source model for failing trace: claude-haiku-4-5
QA model: claude-sonnet-4-5
runtime: local HUD eval via gateway
```

### Source trace command

```bash
cd trainingPlan/hud-hackathon/repos/hud-blank
hud eval tasks.py claude-haiku-4-5 --task-ids eval-order-of-ops --yes -v --max-steps 1
hud trace --json 1f8fc15d-b99a-4fca-b02b-e5dc301a88e1 > ..\..\experiments\traces\hud_blank_eval_order_fail_trace.json
```

### Source trace result

```text
job_id: 9564740e-af34-4566-b183-7c6a4e2a6b35
trace_id: 1f8fc15d-b99a-4fca-b02b-e5dc301a88e1
reward: 0.0
status: completed
```

### QA task command

```bash
hud eval trainingPlan/hud-hackathon/experiments/hud_blank_qa_env.py claude-sonnet-4-5 --task-ids hud-blank-failure-analysis --yes -v --max-steps 20
```

### QA task result

```text
job_id: 4bb99e11-d4ce-4453-9833-f75ae4d7cee4
trace_id: 726c3853-68e8-43bf-8a71-e5ed9d0085df
reward: 1.0
status: completed
```

### What happened

The source task failed because the run was intentionally capped at one agent
step. The trace shows the agent planned the right calculation for `3 + 2 * 3`,
called `add(n=3)`, received `Value: 3`, and was evaluated before it could finish
the remaining operations to reach `9`.

The QA task correctly identified this as premature evaluation caused by the run
configuration/platform cutoff, not a normal reasoning failure.

### Next action

Create several more `hud-blank` traces with different failure shapes, then make
the QA task grade structured failure labels instead of only checking for a few
evidence strings.
