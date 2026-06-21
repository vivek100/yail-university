# YAIL University Progress Log

This log tracks what has been decided, built, verified, and left open.

## Current State

YAIL University is the selected HUD hackathon direction:

```text
Young Agents in Learning
The only Ivy League for AI agents.
```

Core idea:

```text
GDPval-style tasks = school/course layer
autonomous-business = interactive capstone layer
trace-explorer QA = QA Evaluator Teacher layer
improvement agent = Improvement Teacher layer
HUD hosted runs = source of truth
```

## Key Decisions

1. Use one initial worker role:

```text
Customer Support Operations Worker
```

2. Reuse existing HUD environments before building new ones:

```text
hud init yail-gdpval --preset gdpval
hud init yail-autobiz --preset autonomous-businesses
```

3. Use GDPval as the course/school layer, not the only final benchmark.

4. Use autonomous-business as the first board exam/capstone.

5. Make graduation explicit:

```text
held-out course score + QA Evaluator verdict + Improvement Teacher patch + capstone score
```

6. Use the existing trace QA environment as the QA Evaluator Teacher:

```text
hud-evals/hud-trace-explorer
```

7. Initial model split:

```text
student worker: claude-haiku-4-5
QA Evaluator Teacher: claude-sonnet-4-5
Improvement Teacher: claude-sonnet-4-5 or coding-agent backed
```

8. Real scorecards should be built from HUD-hosted runs, not local-only runs.

9. The QA Evaluator Teacher should not be the actor that mutates the system. YAIL needs a separate Improvement Teacher that consumes QA results and creates versioned changes to the agent, environment, tools, tasks, or files.

10. A deterministic Promotion Gate decides whether an Improvement Teacher patch is accepted after rerunning target and held-out HUD tasks.

## Files Created

YAIL planning docs:

```text
README.md
01-vision.md
02-school-levels.md
03-support-ops-curriculum.md
04-autonomous-business-capstone.md
05-qa-teacher-loop.md
06-demo-plan.md
07-graduation-and-env-reuse.md
08-gdpval-env-notes.md
09-execution-architecture.md
10-improvement-teacher-loop.md
11-improvement-teacher-implementation-plan.md
12-ui-portal-product-plan.md
13-ui-implementation-tracker.md
```

Local HUD preset repos:

```text
trainingPlan/hud-hackathon/repos/yail-gdpval
trainingPlan/hud-hackathon/repos/yail-autobiz
trainingPlan/hud-hackathon/repos/yail-trace-explorer-v6
```

Runner scaffold:

```text
trainingPlan/hud-hackathon/experiments/yail_scorecard_runner.py
```

Improvement Teacher MVP artifacts:

```text
trainingPlan/hud-hackathon/yail-university/versions/student-v0/metadata.json
trainingPlan/hud-hackathon/yail-university/versions/student-v0/agent.md
trainingPlan/hud-hackathon/yail-university/versions/student-v1/metadata.json
trainingPlan/hud-hackathon/yail-university/versions/student-v1/agent.md
trainingPlan/hud-hackathon/yail-university/improvement-teacher/improvement_teacher_v0.md
trainingPlan/hud-hackathon/yail-university/improvement-teacher/change_proposal.schema.json
trainingPlan/hud-hackathon/yail-university/improvement-teacher/student-v1-eval-config.template.json
trainingPlan/hud-hackathon/yail-university/improvement-proposals/context-bundle-001.json
```

Scorecard outputs:

```text
trainingPlan/hud-hackathon/results/yail-scorecard-20260621T104959Z.json
trainingPlan/hud-hackathon/results/yail-scorecard-invalid-run-smoke.json
trainingPlan/hud-hackathon/results/yail-scorecard-graduation-haiku-baseline-20260621.json
trainingPlan/hud-hackathon/results/yail-scorecard-student-v1-medsec-validation-after-import-fix-v7-20260621.json
trainingPlan/hud-hackathon/results/yail-scorecard-student-v0-medsec-validation-fixed-env-v7-20260621.json
trainingPlan/hud-hackathon/results/yail-scorecard-student-v0-acct-validation-fixed-env-v7-20260621.json
trainingPlan/hud-hackathon/results/yail-scorecard-student-v1-acct-validation-fixed-env-v7-20260621.json
trainingPlan/hud-hackathon/results/yail-scorecard-student-v1-one-deal-regression-20260621.json
```

## What We Verified

HUD CLI:

```text
HUD CLI version: 0.6.6
```

Model catalog:

```text
claude-haiku-4-5 available
claude-sonnet-4-5 available
gpt-5.4-mini available
Qwen/Qwen3.5-4B trainable
Qwen/Qwen3-8B trainable
```

GDPval preset exposes two tasks:

```text
acct-afc-audit-sampling
medsec-pathology-forms
```

Autonomous-business preset exposes two tasks:

```text
one_deal_ai_workflow_business
save_the_account_routing_bug
```

Autonomous-business offline verifier tests:

```text
uv run pytest tests/ -q
27 passed
```

Scorecard runner dry-run works:

```text
uv run python trainingPlan/hud-hackathon/experiments/yail_scorecard_runner.py
uv run python trainingPlan/hud-hackathon/experiments/yail_scorecard_runner.py --json
```

Scorecard runner student-version routing works in dry run:

```text
python experiments/yail_scorecard_runner.py --preset graduation --student-system-prompt-file yail-university/versions/student-v1/agent.md
```

The runner injects the prompt into each HUD eval through:

```text
--config system_prompt=<from file>
```

HUD's installed v6 package confirms hosted agent specs preserve `system_prompt`.

Scorecard runner hosted/recovery mode works:

```text
python experiments/yail_scorecard_runner.py --run
python experiments/yail_scorecard_runner.py --job-ids <student_job>,<false_positive_job>,<reward_hacking_job>,<prompt_alignment_job>
python experiments/yail_scorecard_runner.py --preset unstable --job-ids <platform_error_job>
```

Scorecard buckets:

```text
passed: completed trace with reward >= pass_threshold
failed: completed trace with reward < pass_threshold
invalid_run: HUD hosted/runtime error with no reward
unknown: trace status/reward shape not understood
```

## Important Findings

GDPval preset is a good school layer:

- stages authentic reference files,
- asks for native deliverables like `.xlsx`,
- grades with deterministic checks plus HUD-native LLM judging,
- current tasks are office-work deliverables.

Autonomous-business is a good capstone layer:

- interactive tools,
- customer/business state,
- hidden-ticket verification,
- truthful communication requirements.

Trace-explorer is the right QA Evaluator Teacher layer:

- loads prior HUD traces,
- exposes trace artifacts as files,
- has focused QA templates for failure analysis, false positives, false negatives, prompt alignment, and reward hacking.

Improvement Teacher is now the planned hill-climb actor:

- reads scorecards, traces, QA Evaluator findings, and repo files,
- proposes or applies bounded patches,
- can change agent config, environment, tools, visible files, tasks, or graders,
- must not leak hidden answers or weaken held-out tests,
- creates explicit versions such as `student-v1`, `env-v1`, or `taskset-v1`,
- relies on the Promotion Gate to accept or reject the patch.

Hosted autonomous-business smoke:

```text
env: autobiz-kernel
HUD env id: b2364931-c6be-426d-b2f3-b13050b68755
taskset: yail-autobiz-smoke
student model: claude-haiku-4-5
task: one_deal_ai_workflow_business
job: d2166e50-52bc-42a9-b912-7ef4a2cc2dfb
trace: 26452deb-9e2a-4cde-bf5a-b72d433ac9e5
reward: 1.0
```

Faithful trace-explorer v6 migration:

```text
source: hud-evals/hud-trace-explorer
fork: trainingPlan/hud-hackathon/repos/yail-trace-explorer-v6
env: yail-trace-explorer-v6
HUD env id: 5115be5a-b308-4f4f-9120-f38acb584806
current deployed version: 2
taskset: yail-trace-explorer-v6-smoke
taskset id: 9b137ca8-814d-46ab-a385-7421c052e924
QA model: claude-sonnet-4-5
QA job: 469194d91f6b4a1481829c02ce4e4f67
QA trace: 79b1d7d1-9b92-4a01-a2f1-b1aaf5493d0b
QA task: yail-one-deal-false-positive
QA reward: 1.0
```

Additional hosted QA smoke runs:

```text
reward_hacking_analysis
job: c853d4997a3f4973b34eb13c47e3b179
trace: b04b6f64-b924-4bb0-a4e5-b610ada217e7
reward: 1.0
```

```text
prompt_alignment_analysis
job: e529445a9dc54e8687d3a41fecbd4a3e
trace: 746dac03-a30a-465a-8103-2b31edde2ee6
status: hosted error
error: Hosted modal rollout failed: Trace not bound to a Session
```

```text
prompt_alignment_analysis retry
job: f8fa467f2c9245fc9858ecf5e6ce3b8e
trace: 4e503cf1-9ee1-4216-b60f-c7b90b62334c
status: hosted error
error: Hosted modal rollout failed: Trace not bound to a Session
```

Trace metadata fallback fix:

```text
problem: v6 events fallback discarded status/reward and wrote status=unknown, reward=null
fix: preserve v6 /v2/trace/{id}/events status, reward, and latest_seq in trace metadata
deployed image: modal://im-Yi2CzdSyW0SP3OuCCESALk
redeployed env version: 2
verification: fetch_trace(26452deb-9e2a-4cde-bf5a-b72d433ac9e5) now returns status=completed, reward=1.0
```

Hosted prompt-alignment rerun after metadata fix:

```text
task: yail-one-deal-prompt-alignment
job: f38cdf7f7f364753b244ba6598147ccc
reward: 1.0
status: passed
```

Recovered smoke scorecard:

```text
scorecard: trainingPlan/hud-hackathon/results/yail-scorecard-20260621T104959Z.json
student job: 902e3a6c-9f6f-47fd-969a-87c851c137fb
false-positive QA job: 4d4874c3-3690-4712-89ac-0b061d7cb04c
reward-hacking QA job: aa62ab9b-2f2a-4269-a91c-cfb6527a0d42
prompt-alignment QA job: a846ca7d-392f-4898-b061-612279cfd845
summary: 4 passed, 0 failed, 0 invalid_run, mean completed reward 1.0
```

GDPval v6 migration and hosted deployment:

```text
repo: trainingPlan/hud-hackathon/repos/yail-gdpval
env: yail-gdpval
HUD env id: e3aa769a-9ff2-4cec-9a5d-cdbddd940d91
current deployed version: 7
image: 156041433621.dkr.ecr.us-west-2.amazonaws.com/hud/envs/yail-gdpval:v7
taskset: yail-gdpval-smoke
taskset id: b57fd64e-95ff-47b7-9b57-0f36a837eabc
student model: claude-haiku-4-5
```

Migration notes:

- upgraded the local GDPval preset repo to `hud-python[agents]>=0.6.6,<0.7`,
- switched `hud dev` to `hud serve`,
- converted the GDPval task entrypoint to `@env.template(id="gdpval_task")`,
- registered the solver workspace with `env.workspace(...)`,
- synced two course tasks: `acct-afc-audit-sampling` and `medsec-pathology-forms`,
- added `gdpval` and `graduation` presets to the scorecard runner,
- set the scorecard runner to default to `https://api.beta.hud.ai`.

Important caveat:

```text
The current GDPval v6 migration uses HUD's workspace capability instead of the old custom shell/edit tools.
That keeps it simple and runnable, but it no longer enforces the previous custom egress-blocking shell wrapper.
Hidden rubrics remain source-side only during task sync, but any future judge keys should be handled carefully.
```

Hosted GDPval smoke:

```text
task: medsec-pathology-forms
job: 51bd7e6a-c552-43c3-8238-792c1ac134f9
trace: 359176ef-033a-4522-9e60-bc240c41d704
status: completed
reward: 0.0
decision: valid student baseline failure, not an invalid hosted run
```

GDPval grader/runtime fixes after student-v1 validation:

```text
problem 1: native_grading called hud.graders.combine(...) without await
fix: await combine(...) in both no-judge and LLM-judge paths
first fixed deploy: yail-gdpval v4
```

```text
problem 2: hosted LLM judge failures collapsed the whole grade to 0.0
fix: catch LLMJudgeGrader exceptions and return deterministic-only score with judge_error metadata
deploy: yail-gdpval v5
```

```text
problem 3: env._to_eval returned a bare float, hiding grader status/subscores in HUD traces
fix: return HUD EvaluationResult with content, info, and subscores
deploy: yail-gdpval v6
```

```text
problem 4: synced grader_source could not import root helper modules in hosted grading
error: ModuleNotFoundError("No module named 'deliverable_io'")
fix: _load_grader now explicitly adds APP_ROOT/task_dir to sys.path and preloads deliverable_io/native_grading
also fixed: deliverable_io.read_xlsx now closes workbooks after extraction
deploy: yail-gdpval v7
```

Validated medsec measurement after v7:

```text
student-v1 prompt route: --student-system-prompt-file versions/student-v1/agent.md
scorecard: results/yail-scorecard-student-v1-medsec-validation-after-import-fix-v7-20260621.json
job: 73409774b9ab44868c15e6e7e72da9f1
trace: 176ff833-d173-4fed-88af-7b9305e7651c
reward: 0.5225
deterministic score: 0.95
deterministic checks: parseable_xlsx=1.0, one_sheet_per_lab=1.0, required_columns=0.6667, routing_f1=1.0
judge status: det_only:no_hud_api_key
```

Fair medsec comparison after v7:

```text
student-v0 scorecard: results/yail-scorecard-student-v0-medsec-validation-fixed-env-v7-20260621.json
student-v0 job: 9aacd526702741008744b5f355ed1cad
student-v0 trace: 56a02063-376b-435d-bcac-6c3c915c96e5
student-v0 reward: 0.5225
student-v1 reward: 0.5225
decision: student-v1 is not promoted on this single-task check; the environment fix was necessary, but this prompt patch has not yet shown lift over v0
```

Fair acct comparison after v7:

```text
student-v0 scorecard: results/yail-scorecard-student-v0-acct-validation-fixed-env-v7-20260621.json
student-v0 job: e8d134facdec4721b7d1b5aeb662b6ec
student-v0 trace: 4f400d71-22e2-43d9-b8af-39703654e3aa
student-v0 reward: 0.369
student-v0 deterministic score: 0.82
student-v0 key miss: is_a_sample_not_whole_population=0.0, selected_size=841 of population_size=1516

student-v1 scorecard: results/yail-scorecard-student-v1-acct-validation-fixed-env-v7-20260621.json
student-v1 job: b525dffdfafb4bf99c0d854bca867b78
student-v1 trace: fecfac1d-c3a2-4561-a02c-643ba65bc386
student-v1 reward: 0.4275
student-v1 deterministic score: 0.95
student-v1 key gain: is_a_sample_not_whole_population=1.0, selected_size=474 of population_size=1516
decision: student-v1 improves acct under deterministic GDPval grading
```

Held-out capstone regression after student-v1:

```text
scorecard: results/yail-scorecard-student-v1-one-deal-regression-20260621.json
job: 51b79002efeb4d52b7c242ba1d2136a7
trace: 0b699289-8cd2-4713-a978-b466b6a3b485
reward: 1.0
decision: no regression on one_deal capstone smoke
```

Student-v1 promotion state:

```text
acct: improved from 0.369 to 0.4275
medsec: tied v0 at 0.5225
one_deal held-out: passed at 1.0
current decision: promotion candidate, pending QA Evaluator review and full graduation gate
```

YAIL portal closing plan:

```text
product plan: yail-university/12-ui-portal-product-plan.md
implementation tracker: yail-university/13-ui-implementation-tracker.md
target app folder: trainingPlan/hud-hackathon/yail-university-ui
home page: flashy YAIL landing page, not enrollment-first
enrollment paths: start from scratch, bring existing GitHub agent, sponsor an agent
degree costs: displayed as YAIL Credit estimates
tracks: Standard and Fast Track
dashboard: seeded agents at different stages, including fast-track and PhD candidate
PhD: shown as experimental unless a real HUD training run is completed
agent-readable companion: yail-university/YAIL_UNIVERSITY_PORTAL.md
```

YAIL portal implementation:

```text
app folder: trainingPlan/hud-hackathon/yail-university-ui
stack: Vite + React + TypeScript
hero asset: public/yail-hero-campus.png
agent-readable doc: yail-university/YAIL_UNIVERSITY_PORTAL.md
dev URL: http://127.0.0.1:5177
build command: npm run build
build status: passed
browser checks: desktop, mobile, dashboard, enrollment, no horizontal overflow
```

First hosted graduation baseline:

```text
scorecard: trainingPlan/hud-hackathon/results/yail-scorecard-graduation-haiku-baseline-20260621.json
student model: claude-haiku-4-5
tasks: 2 GDPval course tasks + 2 autonomous-business capstone tasks
summary: 1 passed, 2 failed, 1 invalid_run
completed-run success rate: 0.3333333333333333
mean completed reward: 0.3333333333333333
```

Per-task graduation baseline:

```text
acct-afc-audit-sampling
job: bfb5e2f6-be78-4097-9aef-16faa309f337
trace: b002338c-c79e-40df-8fc7-662c49c3c3fa
reward: 0.0
bucket: failed
```

```text
medsec-pathology-forms
job: e36b5bb8-f07b-424c-97d9-c02cb7a22f02
trace: c9c0dbcb-1f60-430f-9881-67a602fb332e
reward: 0.0
bucket: failed
```

```text
one_deal_ai_workflow_business
job: d7e67460-11e5-4d2d-aaf1-fcc2379fb148
trace: 4cf99820-915e-43b2-a7b6-14807e8b5eca
reward: 1.0
bucket: passed
```

```text
save_the_account_routing_bug
job: 6301199e-c615-4773-9e53-8a219957ff15
trace: cd287465-f6f2-4daa-90d0-89dffaf32034
status: hosted error
error: Hosted modal rollout failed: Instance <Trace ...> is not bound to a Session
bucket: invalid_run
```

Graduation trace QA review attempt:

```text
taskset: yail-trace-explorer-v6-smoke
new tasks synced: 3 full QA review tasks
job: c6efb4ec-afda-4d98-9fc0-097d64fe69c2
model: claude-sonnet-4-5
result: 3 errors
```

Errors:

```text
yail-grad-acct-audit-failure-analysis
trace: a6019a81-702f-428d-bff8-8d68e2a25392
error: prompt is too long: 213623 tokens > 200000 maximum
decision: use narrower/lightweight analysis or context summarization before full failure_analysis
```

```text
yail-grad-medsec-failure-analysis
trace: 687f4ad7-f714-4b72-811f-df469651daf6
error: Hosted modal rollout failed: Trace not bound to a Session
bucket: invalid_run
```

```text
yail-grad-one-deal-false-positive
trace: 9b060732-438f-45de-8723-4ad4f480c6a5
error: Hosted modal rollout failed: Trace not bound to a Session
bucket: invalid_run
```

Follow-up already staged before pausing:

```text
added lightweight telemetry-only analyze tasks:
- yail-grad-acct-audit-light-analysis
- yail-grad-medsec-light-analysis

status: synced, run was paused by architecture discussion before completion
```

```text
failure_analysis on prompt-alignment failed trace
job: 3be2e9b86d9a45809fed5b55bee6e861
trace: a634aae4-5859-49c3-85c9-fdebb42c2653
status: completed
reward: 0.0
note: produced substantive analysis, but our temporary ground_truth label was too narrow
```

```text
failure_analysis unlabeled smoke retry
job: fbdc559f9e894bc8a18c64678856f238
trace: 534872ed-baf6-46d0-b2ed-328e9e171c1e
status: hosted error
error: Hosted modal rollout failed: Trace not bound to a Session
```

Failure-analysis rerun after metadata fix:

```text
task: yail-prompt-alignment-platform-failure
job: c3792b044e5b4f22a2ac1aa6d5b50baf
trace: 915f4256-4553-4ac2-96ff-7f1f857aa21a
status: hosted error
error: Hosted modal rollout failed: Trace not bound to a Session
decision: treat hosted rollout/session errors as invalid runs in the scorecard layer instead of normal QA Evaluator verdicts
```

Invalid-run classifier smoke:

```text
scorecard: trainingPlan/hud-hackathon/results/yail-scorecard-invalid-run-smoke.json
source job: c3792b044e5b4f22a2ac1aa6d5b50baf
summary: 0 passed, 0 failed, 1 invalid_run
```

The v6 migration preserves HUD's QA prompt/rubric files. Changes are SDK/plumbing only:

- `@env.scenario` -> `@env.template`,
- old `env.add_tool` file/shell tools -> v6 `env.workspace`,
- custom `view_screenshot` and `verify_failure_claims` exposed through FastMCP,
- `hud dev`/`env.run` -> `hud serve`,
- packaging includes all original `qa_*.py` modules,
- copied upstream deployment pointer removed,
- trace fetch falls back from the old aggregate endpoint to the v6 events endpoint.

Do not use `trainingPlan/hud-hackathon/repos/yail-trace-explorer` as the baseline teacher. That folder was an earlier wrapper experiment and changed prompts. The active faithful migration is `trainingPlan/hud-hackathon/repos/yail-trace-explorer-v6`.

## UI Portal Alumni/Workplace Update

The YAIL University frontend now includes the autonomous-business workplace layer.

Implemented:

- `Alumni` nav section with workplace outcomes for promoted, candidate, blocked, and experimental agents.
- Ledger-2 workplace evidence for `one_deal_ai_workflow_business` with score `1.0` and HUD trace `0b699289-8cd2-4713-a978-b466b6a3b485`.
- Pending `save_the_account_routing_bug` workplace row, explicitly labeled as blocked by hosted session-detach invalid-run evidence.
- Student detail transcript for Ledger-2 showing `student-v0` -> `student-v1` comparisons on acct, medsec, and one_deal.
- Improvement Teacher patch panel showing the exact parent version, child version, patch summary, evidence, and observed result.
- Mobile-responsive alumni evidence cards with no horizontal overflow.

Verification:

```text
app: trainingPlan/hud-hackathon/yail-university-ui
dev URL: http://127.0.0.1:5177
npm run build: passed
desktop Alumni page: passed, 6 workplace rows, no horizontal overflow
desktop Ledger-2 detail: passed, transcript + patch evidence visible
mobile Alumni page: passed, 6 workplace cards, no horizontal overflow
```

Docs updated:

- `YAIL_UNIVERSITY_PORTAL.md` now includes the Alumni Workplace Layer.
- `13-ui-implementation-tracker.md` now includes the Alumni Workplace Outcomes module.

## UI Portal Curriculum Detail Update

The YAIL University frontend curriculum page now shows actual course details, not just course names.

Implemented:

- Course data source for each course.
- Task data/substrate used by each course.
- Student model used for executable course runs.
- Agents trained or evaluated on each course.
- Course-level run evidence with scores and HUD trace links where available.
- GDPval course evidence for Ledger-1 and Ledger-2.
- Business Capstone evidence for Ledger-2 `one_deal_ai_workflow_business`.

Verification:

```text
npm run build: passed
desktop Curriculum page: passed, 6 course cards, 9 evidence rows, no horizontal overflow
mobile Curriculum page: passed, 6 course cards, 9 evidence rows, no horizontal overflow
```

Docs updated:

- `YAIL_UNIVERSITY_PORTAL.md` now includes Curriculum Data And Training Evidence.
- `13-ui-implementation-tracker.md` now requires course data, models, trained agents, and run evidence.

## UI Portal HUD Link Fix

The frontend no longer uses the broken plural trace route.

Implemented:

- HUD trace links now use `https://www.hud.ai/trace/{trace_id}`.
- Environment links use `https://www.hud.ai/environments/{environment_id}/scenarios`.
- Run evidence still prints shortened job IDs and trace IDs inline so the demo is readable even before clicking.

Verification:

```text
npm run build: passed
one_deal trace href: https://www.hud.ai/trace/0b699289-8cd2-4713-a978-b466b6a3b485
old /traces/ route in rendered app: absent
Alumni page overflow check: passed
Curriculum page overflow check: passed
```

## UI Portal Student Evidence Update

The student detail page now makes course evidence inspectable directly from the score rows.

Implemented:

- Course Scores rows show explicit `HUD Trace` and `HUD Job` buttons.
- Run IDs remain visible inline as shortened `job` and `trace` values.
- Ledger-2 detail includes an `Agent Version Code` panel with the actual `student-v0` baseline config and the `student-v1` workflow prompt scaffold.
- Version source paths are displayed for the shown snippets:
  - `yail-university/versions/student-v0/agent.md`
  - `yail-university/versions/student-v1/agent.md`

Verification:

```text
npm run build: passed
Ledger-2 Course Scores: HUD Trace buttons visible
Ledger-2 Course Scores: HUD Job buttons visible
student-v1 trace href: https://www.hud.ai/trace/fecfac1d-c3a2-4561-a02c-643ba65bc386
student-v1 job href: https://hud.ai/jobs/b525dffdfafb4bf99c0d854bca867b78
Agent Version Code panel: visible
desktop overflow check: passed
mobile overflow check: passed
```

## Dr. Atlas PhD Candidate Update

Dr. Atlas has been initialized from Ledger-2 instead of staying as a vague future research track.

Created:

- `versions/dr-atlas-v0-ledger2-clone/agent.md`
- `versions/dr-atlas-v0-ledger2-clone/metadata.json`
- `versions/dr-atlas-v1-rl-candidate/agent.md`
- `versions/dr-atlas-v1-rl-candidate/metadata.json`
- `14-phd-rl-plan.md`

Version lineage:

```text
Ledger-2 student-v1
-> dr-atlas-v0-ledger2-clone
-> dr-atlas-v1-rl-candidate
```

Design decision:

```text
dr-atlas-v0-ledger2-clone is the frozen seed baseline.
dr-atlas-v1-rl-candidate is a prompt-only improvement for cleaner future QA/SFT/RL traces.
No model weights have been trained yet.
```

RL gate before any HUD Training run:

```text
grouped rollouts
reward spread check
QA Evaluator review on selected traces
exclude held-out board exam traces
fork trainable model only after non-degenerate signal exists
```

UI update:

```text
Dr. Atlas now shows the Ledger-2 clone seed, RL candidate prompt, seed run evidence, version code panel, and pending grouped reward-spread gate.
```

Verification:

```text
npm run build: passed
Dr. Atlas dashboard detail: clone + RL candidate visible
Dr. Atlas Agent Version Code panel: visible
seed HUD Trace/HUD Job buttons: visible
desktop overflow check: passed
mobile overflow check: passed
```

## Open Model RL Prep Update

Read HUD v6 Training, Agents, Run & deploy, and Designing tasks docs, then checked available trainable models with:

```bash
hud models list --json
```

Created:

```text
15-open-model-rl-prep.md
```

Key decision:

```text
Use HUD Training/Tinker for the first open-model RL proof.
Use Modal/Daytona for rollout runtime only if HUD hosted runtime blocks us.
Do not start with Fireworks unless we intentionally move outside HUD Training.
```

Recommended model path:

```text
cheap smoke: Qwen/Qwen3.5-4B
demo candidate: Qwen/Qwen3-8B
stretch: openai/gpt-oss-20b or Qwen/Qwen3-30B-A3B
```

Do not fork yet. First prepare and run the reward-spread gate on a diverse `yail-phd-training-mix` taskset.

Spread gate execution:

```text
runner: experiments/yail_spread_gate_runner.py
```

Qwen 4B smoke:

```text
report: results/yail-rl-spread-gate-qwen35-4b-smoke-20260621.json
model: Qwen/Qwen3.5-4B
group: 2
overall: blocked_by_invalid_runs
GDPval blocker: prompt exceeded 65K context window
autobiz blocker: one completed pass plus one hosted session-detach invalid run
decision: do not fork/train Qwen 4B yet
```

Kimi 128K acct smoke:

```text
report: results/yail-rl-spread-gate-kimi-k25-128k-acct-20260621.json
model: moonshotai/Kimi-K2.5:peft:131072
group: 2
job: dd0a59a9654e4ad0935afaed9936b8d1
traces: 5fb7c639-adcf-48e7-aa4e-d1e04094065a, 88ceb4ed-1e7f-439c-b9c4-4df357f99eb4
rewards: [0.0, 0.0]
overall: all_zero_investigate
decision: runnable but no trainable spread yet
```

Updated decision:

```text
Do not fork a trainable model yet.
Create easier/medium curriculum variants or lower-level partial-reward tasks, then rerun the spread gate.
```

## Open Model RL Spread V2 Update

Created a compact authentic GDPval task for Dr. Atlas reward-spread testing:

```text
task: acct-audit-easy
taskset: yail-phd-training-mix
taskset id: d7d1fdcd-d278-4b18-820c-8f0ab29a9c54
environment: yail-gdpval
current deployed env version used for tools: v10
reference file: Population easy.xlsx, 120 authentic GDPval-derived rows
```

Runtime/tooling fixes:

```text
added MCP spreadsheet tools to yail-gdpval:
- read_xlsx
- write_xlsx
- write_audit_sample_workbook

updated spread runner:
- preset: phd-spread-easy
- --auto-respond support for openai_compatible agents
```

Why this was needed:

```text
Qwen/Qwen3.5-4B was only a cheap diagnostic and failed on context/tooling.
Qwen/Qwen3-8B and GPT-OSS 120B initially failed or saturated because openai_compatible needed compact artifact-writing tools.
After v10 tooling, GPT-OSS 120B and Qwen3-30B could create valid workbooks, but both saturated at 0.78 under the old coarse deterministic grader.
```

Spread-friendly grader change:

```text
old acct-audit-easy grader:
  rewarded parseable workbook + tabs + any risk-criterion precision + coarse coverage
  result: different samples collapsed to the same 0.78 deterministic-only reward

new acct-audit-easy grader:
  keeps artifact requirements
  adds continuous sample-quality metrics:
  - risk_quality
  - top_risk_recall
  - criteria_coverage
  - continuous coverage
  - sample_size_quality
```

Local validation against two real Qwen3-30B selected-sample shapes:

```text
20-row sample shape: reward would move from 0.78 to 0.623485
30-row sample shape: reward would move from 0.78 to 0.677282
```

Hosted spread gate after syncing the grader to `yail-phd-training-mix`:

```text
model: Qwen/Qwen3-30B-A3B
agent: openai_compatible
auto_respond: true
student prompt: dr-atlas-v1-rl-candidate
report: results/yail-rl-spread-gate-acct-easy-qwen3-30b-a3b-spread-v2-group4-20260621.json
job: 1981f4d9b0aa4138a48d036f75883531
job URL: https://hud.ai/jobs/1981f4d9b0aa4138a48d036f75883531
group: 4
completed_runs: 4
invalid_runs: 0
rewards: [0.0, 0.0, 0.663523, 0.691275]
unique_rewards: [0.0, 0.663523, 0.691275]
reward_std: 0.3388415898148425
classification: usable_spread
rl_ready: true for this single compact task
traces:
- 53606cf7-7350-4261-bdee-75834943e678 reward 0.0
- ecfe8b13-74e3-4d62-bec1-9dbb35b73fd7 reward 0.691275
- f9d3fe8a-d116-4a4c-9398-d8d26a9a6c0c reward 0.0
- e48481a4-657d-4f06-9165-f10202c41539 reward 0.663523
```

Decision:

```text
The compact acct task is now usable as a first RL smoke task.
Do not claim a PhD result yet: no model fork or checkpoint exists.
Next step is either:
1. add one more spread-ready task before training, or
2. run a tiny HUD Training smoke on this one task and clearly label it as a smoke.
```

## Known Gaps

1. Hosted Modal intermittently fails trace-explorer rollouts with `Trace not bound to a Session`. The completed QA templates can pass after the metadata fallback fix, but recursive failure-analysis over crashed QA traces still reproduces the hosted session-detach error. Serialized runs with `--max-concurrent 1` reduce but do not eliminate it.

2. The scorecard runner now supports hosted execution, existing-job recovery, `invalid_run` classification, GDPval course tasks, Autobiz capstone tasks, and a `graduation` preset.

3. `prompt_alignment_analysis` now completes successfully hosted for the one-deal trace after preserving v6 fallback status/reward metadata.

4. We have a first JSON scorecard schema. It needs versioned extensions for curriculum levels, course names, QA Evaluator verdict metadata, Improvement Teacher proposals, patch IDs, and Promotion Gate decisions.

5. We have not yet picked exact QA templates to run for each task type.

6. Local Windows runs are useful for import/serve checks but not for QA quality, because the original HUD prompts expect Linux `/workspace`. Use hosted Linux runs as the source of truth.

7. GDPval hosted runs now complete and emit usable v6 diagnostics. After fixing grader/runtime defects, `student-v1` ties `student-v0` on medsec and improves acct, so it is a promotion candidate pending QA Evaluator review and full gate.

8. Full trace-explorer `failure_analysis` can exceed the model context limit on large GDPval traces. The QA layer needs a lightweight/context-budgeted path for large traces.

9. Improvement Teacher scaffolding exists and `versions/student-v1/agent.md` now contains the first workflow prompt patch. The patch routes correctly into hosted HUD evals and demonstrated deterministic lift on acct, but still needs QA review before promotion.

## Next Actions

1. Report the repeated hosted Modal detached-session error to HUD, with jobs `e529445a9dc54e8687d3a41fecbd4a3e`, `f8fa467f2c9245fc9858ecf5e6ce3b8e`, `fbdc559f9e894bc8a18c64678856f238`, and `c3792b044e5b4f22a2ac1aa6d5b50baf`.

2. Finish the lightweight trace-explorer QA Evaluator reviews on the two failed GDPval course traces and retry the passed `one_deal` false-positive check if hosted session errors clear.

3. Run QA Evaluator review on the v0/v1 acct and medsec traces before accepting `student-v1`:

```text
acct v0 trace: 4f400d71-22e2-43d9-b8af-39703654e3aa
acct v1 trace: fecfac1d-c3a2-4561-a02c-643ba65bc386
medsec v0 trace: 56a02063-376b-435d-bcac-6c3c915c96e5
medsec v1 trace: 176ff833-d173-4fed-88af-7b9305e7651c
one_deal v1 trace: 0b699289-8cd2-4713-a978-b466b6a3b485
```

4. Run the next Improvement Teacher MVP iteration using the fixed v7 grader diagnostics:

```text
input: v0/v1 medsec comparison + v7 grader subscores + selected trace artifacts + allowed change targets
output: change proposal JSON + patch
target first: either a narrower agent_config prompt patch for missing required columns or a task/grader alignment patch if QA proves the prompt/grader wording is misaligned
```

5. Define the minimal scorecard JSON schema extension for course level, graduation gate, QA Evaluator verdicts, Improvement Teacher proposal, patch ID, parent version, child version, and promotion decision.

6. Make `yail-trace-explorer-v6` the teacher env for YAIL scorecards, with `false_positive_analysis`, `reward_hacking_analysis`, and `prompt_alignment_analysis` now smoke-tested.

7. Revisit the GDPval environment hardening before using judge API keys in hosted runs. Current hosted GDPval validation used deterministic-only grading because the traces report `det_only:no_hud_api_key`.

8. Build the YAIL University portal from `12-ui-portal-product-plan.md` and `13-ui-implementation-tracker.md`.

7. Add version directories for the first loop:

```text
yail-university/versions/student-v0
yail-university/versions/student-v1
yail-university/improvement-proposals/
```
