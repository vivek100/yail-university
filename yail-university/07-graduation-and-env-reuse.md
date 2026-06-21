# 07 - Graduation Tests and HUD Environment Reuse

YAIL needs explicit graduation gates. A course is not complete just because the agent attempted lessons; it graduates only when it passes held-out tests under the same HUD grading harness.

## Graduation model

Each course should have:

- training lessons,
- retake lessons,
- held-out graduation lessons,
- a minimum score,
- QA Evaluator Teacher review,
- Improvement Teacher proposal when the agent fails,
- regression checks.

The agent can improve through prompt, tooling, workflow, examples, or later SFT/RL. The graduation test is always measured on held-out tasks the agent did not see during the improvement loop.

Initial model choices:

```text
student: claude-haiku-4-5
QA Evaluator Teacher: claude-sonnet-4-5
Improvement Teacher: claude-sonnet-4-5 or coding-agent backed
```

## Course loop

```text
student agent attempts course lessons
  -> HUD records rewards and traces
  -> trace-explorer QA Evaluator Teacher reviews task design and student traces
  -> Improvement Teacher creates the next version of agent/env/tools/tasks/files
  -> Promotion Gate accepts only if held-out score improves without QA objections
  -> rerun held-out graduation lessons
  -> award course credit only if score and QA checks pass
```

## Graduation scorecard

For every worker, produce a scorecard:

```text
role: Customer Support Operations Worker
level: Diploma
course_scores:
  ticket_classification: 0.92
  workflow_design: 0.81
  workflow_debugging: 0.78
  customer_communication: 0.86
capstone_scores:
  one_deal: 0.80
  save_the_account: 0.75
qa_teacher_verdict: pass
improvement_version: student-v1
promotion_decision: accepted
known_weaknesses:
  - slower on ambiguous billing/login tickets
  - sometimes overexplains customer replies
```

## Existing HUD environments first

Do not build from scratch if HUD already has the substrate.

Use existing presets and templates first:

```bash
hud init yail-gdpval --preset gdpval
hud init yail-autobiz --preset autonomous-businesses
```

The local HUD SDK lists both presets:

- `gdpval`: GDPval benchmark tasks.
- `autonomous-businesses`: autonomous business loop for support-ticket triage.

## How GDPval fits

GDPval is the curriculum source and exam bank for professional work-product tasks.

Use it to derive:

- role taxonomy,
- course topics,
- assignment prompts,
- supporting files,
- expected deliverables,
- rubrics.

If HUD's GDPval environment already exposes runnable tasks, reuse it directly for lessons and exams instead of converting GDPval manually.

## How autonomous-business fits

Autonomous-business is the first interactive business capstone.

It tests whether the worker can use tools, act in a business loop, and create verified business value. It is especially useful after GDPval-style lessons because GDPval is mostly work-product oriented, while autonomous-business is action/state oriented.

## Pass / fail rule

A worker graduates only if all three are true:

1. Held-out course scores clear the threshold.
2. Trace-explorer QA Evaluator Teacher finds no major task-design flaw or reward-hacking behavior.
3. The Improvement Teacher's accepted version beats the parent version on target tasks without held-out regression.
4. Held-out capstone score improves over the base agent and clears the minimum graduation bar.

## Hosted only for real scorecards

Use local runs only to debug environment setup. Scorecards used in the hackathon should be built from HUD-hosted runs so trace IDs, artifacts, and model routing are consistent.
