# 15 - Open Model RL Prep

This is the preparation plan for running Dr. Atlas on an open/trainable model.

## Current Recommendation

Use HUD Training first, not a separate Fireworks or Modal training loop.

Reason:

- HUD already owns the environment/task/trace/reward layer.
- HUD Training can fork trainable gateway models and update them from rewarded trajectories.
- HUD traces stay linked to the taskset, reward, model, and checkpoint.
- Modal/Daytona are useful for rollout runtime if we need cloud sandboxes, but they are not the first place to update model weights.
- Fireworks can still be useful later for serving or comparing an external fine-tune, but it is not needed for the first YAIL RL proof.

## Docs Basis

HUD Training says the loop is:

```text
roll out tasks
score each rollout
train from the rewarded trajectories
repeat
```

The hard prerequisite is reward spread. If every rollout in a group gets the same reward, GRPO produces zero advantage and no learning signal.

## Trainable Models Available Now

Checked with:

```bash
hud models list --json
```

Good first candidates:

| Candidate | HUD model_name | Why |
| --- | --- | --- |
| Qwen3.5 4B | `Qwen/Qwen3.5-4B` | cheapest likely smoke candidate |
| Llama 3.2 3B | `meta-llama/Llama-3.2-3B` | very small baseline, likely weaker anchor |
| Qwen3 8B | `Qwen/Qwen3-8B` | stronger small demo candidate |
| GPT-OSS 20B | `openai/gpt-oss-20b` | stronger open model if credits allow |
| Qwen3 30B A3B | `Qwen/Qwen3-30B-A3B` | better capability, higher cost |

Default choice:

```text
Smoke: Qwen/Qwen3.5-4B
Demo RL: Qwen/Qwen3-8B
Stretch: openai/gpt-oss-20b or Qwen/Qwen3-30B-A3B
```

## Fork Plan

Do not fork until the reward-spread gate is ready.

When ready:

```bash
hud models fork Qwen/Qwen3.5-4B --name yail-dr-atlas-qwen35-4b-smoke
```

Or for the stronger demo:

```bash
hud models fork Qwen/Qwen3-8B --name yail-dr-atlas-qwen3-8b
```

The new slug becomes both the sampled model and the trained model.

## Data And Task Prep

Do not train on the current held-out proof traces directly:

```text
one_deal trace: 0b699289-8cd2-4713-a978-b466b6a3b485
acct v1 trace: fecfac1d-c3a2-4561-a02c-643ba65bc386
medsec v1 trace: 176ff833-d173-4fed-88af-7b9305e7651c
```

Use those as demo/proof/board evidence, not training data.

Training needs variants:

```text
GDPval variants:
- acct audit variants with different sample sizes and risk patterns
- medsec/admin form variants with different schemas
- native spreadsheet/document deliverable variants

Autonomous-business variants:
- one_deal variants with different customer constraints
- save_the_account variants with different routing bugs
- workflow debugging variants
- customer communication variants with truthful constraints
```

## Reward Spread Gate

Before RL:

```text
for each candidate task:
  run base trainable model with group=8 or group=16
  inspect reward distribution
  reject saturated all-1.0 tasks
  investigate all-0.0 tasks
  keep tasks with meaningful partial/spread rewards
```

Target:

```text
not all 0
not all 1
some partial rewards
subscores explain where reward came from
```

The current `one_deal` result at `1.0` is useful as a non-regression board task, but it is likely saturated for training unless we create harder variants.

## Minimal RL Loop

```python
from hud import Taskset
from hud.agents import create_agent
from hud.eval import Job
from hud.training import TrainingClient

slug = "yail-dr-atlas-qwen3-8b"
taskset = Taskset.from_api("yail-phd-training-mix")

agent = create_agent(
    slug,
    completion_kwargs={"extra_body": {"return_token_ids": True}},
)
trainer = TrainingClient(slug)

session = await Job.start(slug, group=8)

for step in range(10):
    start = len(session.runs)
    await taskset.run(agent, job=session)
    batch = session.runs[start:]
    await trainer.step(batch, learning_rate=1e-5, group_size=8, loss_fn="ppo")
    head = await trainer.head()
    print(step, head.mean_reward, head.metrics)
```

Use `ppo` first because the training batch will be small and we do not want one lucky rollout to dominate the update.

## Runtime Choice

Start with HUD platform runtime:

```text
deployed HUD env + HUDRuntime
```

Use Modal/Daytona only when:

- HUD hosted runtime blocks on missing system dependencies,
- we need custom cloud sandbox shape,
- we need more control over rollout hardware/timeouts,
- or HUD team recommends it for a sponsor demo.

The model training still goes through HUD Training/Tinker for the first proof.

## First Concrete Experiment

1. Create 8-12 training variants:
   - 4 GDPval spreadsheet variants,
   - 4 autonomous-business workflow variants,
   - optional 4 communication/debugging variants.
2. Sync as:

```text
yail-phd-training-mix
```

3. Run spread check on:

```text
Qwen/Qwen3.5-4B
Qwen/Qwen3-8B
claude-haiku-4-5 as reference only, not trainable
```

4. Pick model:

```text
if Qwen3.5 4B has usable spread -> use it for cheap smoke
else use Qwen3 8B
```

5. Fork selected trainable model.
6. Run 3-5 RL steps only.
7. Evaluate checkpoint on held-out board:

```text
acct held-out variant
medsec held-out variant
one_deal non-regression
save_the_account non-regression if runtime is stable
```

8. Compare:

```text
base trainable model
dr-atlas-v0-ledger2-clone prompt behavior
dr-atlas-v1-rl-candidate prompt behavior
trained fork checkpoint
```

## Success Criteria

A demo-safe RL result requires:

- a real forked trainable model slug,
- at least one checkpoint,
- checkpoint metrics visible from `hud models checkpoints`,
- held-out board score improvement over the base fork,
- no regression on one_deal,
- QA Evaluator Teacher does not flag false-positive or reward-hacking behavior.

If we cannot get reward spread, do not run RL. Show the spread audit instead; it is a credible reason to stop.

## Spread Gate Results - 2026-06-21

Implemented spread-gate runner:

```text
experiments/yail_spread_gate_runner.py
```

### Smoke 1 - Qwen 4B

Command:

```bash
py experiments/yail_spread_gate_runner.py \
  --preset phd-spread-smoke \
  --model Qwen/Qwen3.5-4B \
  --group 2 \
  --student-system-prompt-file yail-university/versions/dr-atlas-v1-rl-candidate/agent.md \
  --run \
  --output results/yail-rl-spread-gate-qwen35-4b-smoke-20260621.json
```

Result:

```text
overall: blocked_by_invalid_runs
usable_task_count: 0
rl_ready: false
```

Findings:

```text
acct-afc-audit-sampling:
  model: Qwen/Qwen3.5-4B
  job: d4b86ebea4c84cd1833673bd335e2241
  traces:
    379ba71d-3a8f-4c5a-9fc9-4856003760f1
    469076bb-f96d-4e30-9331-13012dbb2fff
  error:
    prompt length plus max_tokens exceeded 65,536 context

one_deal_ai_workflow_business:
  model: Qwen/Qwen3.5-4B
  job: bcdfb0112b27462abd1f5cc01e44e1bc
  completed rewards: [1.0]
  invalid runs: 1 hosted session-detach error
```

Decision:

```text
Qwen3.5 4B is too short-context for current GDPval and did not produce a clean two-run autonomous-business spread sample.
Do not fork/train it yet.
```

### Smoke 2 - Kimi 128K

Command:

```bash
py experiments/yail_spread_gate_runner.py \
  --preset phd-spread-gdpval \
  --task-ids acct-afc-audit-sampling \
  --model moonshotai/Kimi-K2.5:peft:131072 \
  --group 2 \
  --student-system-prompt-file yail-university/versions/dr-atlas-v1-rl-candidate/agent.md \
  --run \
  --output results/yail-rl-spread-gate-kimi-k25-128k-acct-20260621.json
```

Result:

```text
overall: all_zero_investigate
usable_task_count: 0
rl_ready: false
```

Findings:

```text
acct-afc-audit-sampling:
  model: moonshotai/Kimi-K2.5:peft:131072
  job: dd0a59a9654e4ad0935afaed9936b8d1
  traces:
    5fb7c639-adcf-48e7-aa4e-d1e04094065a
    88ceb4ed-1e7f-439c-b9c4-4df357f99eb4
  rewards: [0.0, 0.0]
```

Decision:

```text
Kimi 128K can run the long GDPval prompt, but group=2 produced no reward spread.
Do not train yet.
```

## Updated Next Step

The next step is not model forking. The next step is curriculum shaping:

```text
create easier and medium GDPval variants
or add lower-level deterministic partial reward tasks
then rerun the spread gate
```

Good candidate variants:

```text
acct-audit-easy:
  smaller population, explicit sample-size hint, same workbook output

acct-audit-medium:
  same shape as current task, but fewer columns and clearer risk flags

medsec-easy:
  fewer forms, fewer required fields, deterministic grade with partial field rewards

autobiz-one-deal-hard:
  avoid all-1 saturation by varying customer budget, forbidden claims, and workflow checks
```

Fork only after at least one task has:

```text
completed_runs >= group size
invalid_runs = 0
unique_rewards > 1
reward_std > 0.02
```

## Spread Gate V2 Results - 2026-06-21

Implemented the first compact spread-ready GDPval task:

```text
task: acct-audit-easy
taskset: yail-phd-training-mix
environment: yail-gdpval
reference: compact authentic GDPval-derived Population easy.xlsx
```

Important implementation detail:

```text
openai_compatible agents did not have enough native write capability for spreadsheet deliverables.
Added MCP tools to the environment:
- read_xlsx
- write_xlsx
- write_audit_sample_workbook
```

The helper writes the workbook, but it does not select the sample. The model still has to inspect the population and choose row IDs.

The first working helper runs saturated under the original coarse grader:

```text
GPT-OSS 120B 128K helper run:
  job: 7874cc847d6745a3af5bfcc7cc6ec81a
  rewards: [0.78, 0.78]
  classification: constant_reward_no_advantage

Qwen3-30B-A3B helper run:
  job: 5cb9a67337354af38106bf589188b551
  rewards: [0.78, 0.78]
  classification: constant_reward_no_advantage
```

Root cause:

```text
The old deterministic grader treated different valid samples as equally perfect.
Because hosted grading was det_only:no_hud_api_key, both perfect deterministic scores became 0.78.
```

Spread-friendly grader update:

```text
Added continuous deterministic checks:
- risk_quality
- top_risk_recall
- criteria_coverage
- sample_size_quality
- continuous division/country coverage
```

Hosted verification after syncing the updated grader:

```text
model: Qwen/Qwen3-30B-A3B
agent: openai_compatible
auto_respond: true
student prompt: dr-atlas-v1-rl-candidate
report: results/yail-rl-spread-gate-acct-easy-qwen3-30b-a3b-spread-v2-group4-20260621.json
job: 1981f4d9b0aa4138a48d036f75883531
group: 4
completed_runs: 4
invalid_runs: 0
rewards: [0.0, 0.0, 0.663523, 0.691275]
reward_std: 0.3388415898148425
classification: usable_spread
rl_ready: true
```

Interpretation:

```text
This is enough to justify a tiny RL smoke run on one compact task.
It is not enough to claim a robust PhD training result.
For the stronger hackathon story, add one more spread-ready task or run the smoke with very clear labeling.
```
