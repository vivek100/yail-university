# YAIL University

**Young Agents in Learning. The only Ivy League for AI agents.**

YAIL University is a HUD hackathon project for training and evaluating AI workers through a curriculum of real agent tasks. Instead of treating a benchmark as a one-time leaderboard, YAIL turns benchmark failures into courses, scorecards, teacher reviews, version changes, and eventually reinforcement learning runs.

The demo is a registrar dashboard for AI agents: enroll a worker, run it through GDPval-style professional tasks, inspect HUD traces, promote or hold it back, and validate graduates in a business simulation.

## Why this exists

In 2040, every company should be able to spin up specialized AI workers as easily as making a web app today. The bottleneck is not only agent code. The hard part is creating a reliable school:

- tasks that represent real work
- graders that cannot be gamed
- trace QA that catches false positives, false negatives, and reward hacking
- promotion gates backed by held-out evaluations
- training loops that only run when the environment has reward signal

YAIL is that school for agents.

## What we built

- **YAIL University UI**: a Vite/React dashboard showing students, courses, degree tracks, agent versions, HUD run links, and real score evidence.
- **GDPval HUD environment**: a HUD v6 environment for professional knowledge-work tasks with staged reference files, native deliverable grading, and LLM-judge support.
- **Trace QA track**: planning and compatibility work for HUD trace-explorer style QA agents that review traces before a run becomes training data.
- **RL smoke runner**: a small HUD Training script that forks a trainable open model, collects grouped rollouts, and calls `hud.train.TrainingClient.step`.
- **Autonomous-business capstone link**: a graduation target where improved workers are tested in a more realistic business environment.

## Current evidence

The current public demo intentionally distinguishes evidence from aspiration.

| Agent | Evidence | Result |
| --- | --- | --- |
| Ledger-1 | GDPval `acct-afc-audit-sampling` baseline | `0.3690` |
| Ledger-2 | QA-guided prompt/workflow update on same GDPval task | `0.4275`, up `+0.0585` |
| Ledger-2 | Autonomous-business `one_deal_ai_workflow_business` capstone | `1.0` |
| Dr. Atlas | Qwen3-30B reward-spread gate on compact GDPval audit | usable spread `[0.0, 0.0, 0.663523, 0.691275]` |
| Dr. Atlas | HUD Training PPO smoke on Qwen3-30B fork | checkpoint `step-000001` created |
| Dr. Atlas | First post-training audit rerun | failed all-zero; not graduated yet |

The strongest honest claim today: **we have a working HUD eval -> trace evidence -> trainable-model fork -> PPO checkpoint loop.** The PhD candidate has not graduated yet because post-training held-out performance has not improved.

## How HUD is used

HUD is the evaluation and training substrate:

- **Environment**: where the agent acts. Our GDPval environment stages files and exposes workspace/tool capabilities.
- **Task**: a concrete prompt plus grader. A task yields a prompt to the agent and then yields a reward.
- **Trace**: the recorded run, including agent actions, tool calls, output, reward, and errors.
- **Taskset**: a group of tasks synced to HUD and run locally or remotely.
- **Training**: grouped rollouts from a trainable model are passed to `TrainingClient.step`.

Useful commands:

```bash
cd repos/yail-gdpval
hud deploy .
hud sync tasks yail-gdpval-smoke env.py
hud eval yail-gdpval-smoke claude --model claude-haiku-4-5 --remote
```

Run the RL smoke:

```bash
cd trainingPlan/hud-hackathon
./repos/yail-gdpval/.venv/Scripts/python.exe ./experiments/yail_rl_smoke_runner.py
```

## How Modal is used

Modal hosts the frontend as a public web app. The UI is built once with Vite, copied into a Modal image, and served with a small FastAPI ASGI app.

Modal docs used for this deployment pattern:

- Web Functions and `modal serve` / `modal deploy`: https://modal.com/docs/guide/webhooks
- ASGI apps with `@modal.asgi_app`: https://modal.com/docs/reference/modal.asgi_app
- Static React + FastAPI web app example: https://modal.com/docs/examples/doc_ocr_webapp

Build and deploy:

```bash
cd yail-university-ui
npm install
npm run build

cd ..
py -m modal deploy modal_app.py
```

For an ephemeral preview instead of a persistent deployment:

```bash
py -m modal serve modal_app.py
```

## Repository layout

```text
docs/                         HUD notes and planning docs
experiments/                  scorecard, spread-gate, and RL smoke runners
repos/yail-gdpval/            HUD v6 GDPval environment
yail-university/              project docs, agent versions, progress notes
yail-university-ui/           React frontend
modal_app.py                  Modal ASGI static frontend host
```

## Frontend

```bash
cd yail-university-ui
npm install
npm run dev
npm run build
```

## Project status

This is a hackathon prototype. It already has real HUD runs and a real HUD Training checkpoint, but the graduation loop is still experimental. The next technical step is to expand from one compact GDPval RL task to a broader GDPval-derived taskset, then train only on tasks that show within-group reward spread and evaluate on held-out GDPval/business tasks.

## License

MIT
