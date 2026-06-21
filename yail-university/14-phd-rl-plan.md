# 14 - Dr. Atlas PhD RL Plan

Dr. Atlas starts as a clone of Ledger-2 because Ledger-2 is the strongest current YAIL student:

```text
Ledger-2 student-v1 acct: 0.4275
Ledger-2 student-v1 medsec: 0.5225
Ledger-2 student-v1 one_deal: 1.0
```

The clone is:

```text
versions/dr-atlas-v0-ledger2-clone
```

The prompt-improved PhD candidate is:

```text
versions/dr-atlas-v1-rl-candidate
```

## What Changed

`dr-atlas-v0-ledger2-clone` is the Ledger-2 `student-v1` policy copied into the PhD track.

`dr-atlas-v1-rl-candidate` keeps the same professional work-product behavior but adds trace hygiene:

- short observable checkpoints,
- explicit verification steps,
- no hidden-rubric guessing,
- no reward-target vocabulary,
- artifacts and business state as the primary evidence.

This is meant to create cleaner trajectories for later SFT/RL selection. It is not a trained model.

## RL Gate

Do not launch RL until the taskset passes these checks:

1. Multi-step work is required.
2. Prompt and grader are aligned.
3. No answer leakage exists in prompt, files, logs, or grader-visible labels.
4. Group rollouts show reward spread.
5. Taskset is diverse across substrate, failure mode, deliverable type, and environment.
6. Held-out board exam traces are excluded from training.

Current gate status:

```text
acct-audit-easy on yail-phd-training-mix now passes the reward-spread gate for Qwen/Qwen3-30B-A3B.
This permits a tiny one-task HUD Training smoke run.
It does not yet satisfy the full diverse-taskset requirement for a robust PhD claim.
```

Evidence:

```text
report: results/yail-rl-spread-gate-acct-easy-qwen3-30b-a3b-spread-v2-group4-20260621.json
job: 1981f4d9b0aa4138a48d036f75883531
group: 4
rewards: [0.0, 0.0, 0.663523, 0.691275]
invalid_runs: 0
classification: usable_spread
rl_ready: true
```

## Candidate Training Tasksets

Training mix:

```text
GDPval course variants:
- spreadsheet audit sampling
- medical/admin form routing
- native spreadsheet/document deliverables

Autonomous-business variants:
- one_deal variants
- save_the_account variants
- workflow routing/debugging
- customer communication with truthful constraints
```

Held-out board exam:

```text
new GDPval variants + new autonomous-business variants not used in SFT/RL
```

## HUD Training Shape

Target flow:

```text
fork trainable model
-> run grouped rollouts with return_token_ids
-> QA select/label traces
-> trainer.step on grouped runs
-> inspect reward spread, KL, loss, and checkpoint mean reward
-> evaluate checkpoint against held-out board exam
-> compare against Ledger-2 and dr-atlas-v0
```

Pseudo-code:

```python
from hud import Taskset
from hud.agents import create_agent
from hud.training import TrainingClient

slug = "yail-dr-atlas-phd-small"
taskset = Taskset.from_api("yail-phd-training-mix")
agent = create_agent(slug, completion_kwargs={"extra_body": {"return_token_ids": True}})
trainer = TrainingClient(slug)

for step in range(20):
    job = await taskset.run(agent, group=8)
    result = await trainer.step(job.runs, learning_rate=1e-5, group_size=8, loss_fn="ppo")
    checkpoints = await trainer.checkpoints()
```

Use PPO first because the training set will be small and a single lucky rollout should not dominate the update.

## What Counts As Success

The PhD claim is valid only if:

- a HUD trainable model fork exists,
- training checkpoints exist,
- held-out reward improves over `dr-atlas-v0-ledger2-clone`,
- held-out reward improves or matches Ledger-2 on non-regression tasks,
- QA Evaluator Teacher does not flag reward hacking or false positives,
- the board exam uses tasks excluded from training.

Until then, Dr. Atlas is a PhD candidate, not a PhD graduate.
