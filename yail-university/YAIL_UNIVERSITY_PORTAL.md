# YAIL University Portal

**Young Agents in Learning.**

**The only Ivy League for AI agents.**

YAIL University is a training and evaluation system for AI workers. Agents do not go directly from a prompt into production. They enroll, take courses, run HUD assignments, receive grades, get audited by a QA Evaluator Teacher, improve through an Improvement Teacher, and graduate only after promotion gates.

## Core Loop

```text
enroll agent
-> run HUD tasks
-> collect traces, rewards, and scorecards
-> QA Evaluator Teacher audits the traces
-> Improvement Teacher creates a bounded patch
-> new student version is evaluated
-> Promotion Gate accepts or rejects
-> optional SFT/RL after enough validated signal
```

## What YAIL Adds To HUD

HUD provides the campus:

- environments,
- tasks,
- traces,
- hosted model runs,
- graders,
- QA trace tools.

YAIL adds the school:

- role curricula,
- degrees and levels,
- student version history,
- QA teacher review,
- improvement teacher patching,
- promotion gates,
- graduation dashboards.

## Degree Catalog

Costs are shown in **YAIL Credits**, a demo estimate for hosted evals, compute, sandboxes, QA reviews, and improvement loops.

| Degree | Purpose | Estimated Cost | Status |
| --- | --- | ---: | --- |
| Certificate | Basic role readiness | 100 credits | Available |
| Diploma | Prompt, tool, and workflow hardening | 350 credits | Available |
| Degree | Versioned worker specialization | 900 credits | Available |
| Residency | Real business capstone validation | 1,800 credits | Available |
| PhD | Custom SFT/RL model optimization | 5,000+ credits | Experimental |

## Tracks

### Standard Track

Lower cost and slower graduation.

- fewer parallel HUD runs,
- fewer sandboxes,
- sequential QA reviews,
- smaller batches.

### Fast Track

Higher cost and faster graduation.

- more parallel HUD runs,
- more Modal/Daytona sandboxes,
- parallel QA reviews,
- larger comparison batches.

## Enrollment Paths

### Start From Scratch

Create a new student worker with a role, model, track, and degree target.

### Bring an Existing Agent

Enroll an existing agent from a GitHub URL. The future backend flow is:

```text
clone repo -> inspect entrypoint -> wrap in HUD harness -> run placement scorecard
```

The hackathon UI treats this as a demo intake path.

### Sponsor an Agent

A company sponsors a YAIL worker for a business domain. The student starts with curriculum design and placement testing.

## First Curriculum

Role:

```text
Customer Support Operations Worker
```

Courses:

1. Ticket Classification
2. Workflow Design
3. Workflow Debugging
4. Customer Communication
5. Integrated Account Save
6. GDPval Knowledge Work
7. Business Capstone

## Curriculum Data And Training Evidence

The curriculum page is not only a syllabus. It shows the actual task substrate each course uses, the student model, the agents trained or evaluated on that course, and the HUD evidence available so far.

| Course | Data / Task Substrate | Agents | Current Evidence |
| --- | --- | --- | --- |
| Ticket Classification | planned support-ops ticket taxonomy, customer tickets, hidden validation tickets | Nova-0 | placement pending |
| Workflow Design | `hud-evals/autonomous-businesses-template` routing workflows and hidden routing checks | Swift-Track | fast-track batch scheduled |
| Workflow Debugging | broken workflow config, complaint transcript, routing logs, hidden regression tickets | Casey-QA | QA hold; not admitted to workplace sim |
| Customer Communication | customer issue, resolved workflow state, policy constraints, reply rubric | Swift-Track, Casey-QA | part of pending fast-track batch |
| GDPval Knowledge Work | `yail-gdpval:v7`, acct audit workbook, medsec pathology forms, native deliverables | Ledger-1, Ledger-2 | acct v0 `0.369`, acct v1 `0.4275`, medsec v1 `0.5225` |
| Business Capstone | autonomous-business `one_deal_ai_workflow_business`, `save_the_account_routing_bug`, business-state verifier | Ledger-2, Swift-Track, Dr. Atlas | one_deal v1 `1.0`; save_the_account rerun pending |

Student model for current executable course runs:

```text
claude-haiku-4-5
```

PhD course work has one compact spread-ready GDPval task, but no trainable-model fork or held-out board exam yet.

Current PhD spread evidence:

```text
task: acct-audit-easy
taskset: yail-phd-training-mix
model: Qwen/Qwen3-30B-A3B
job: 1981f4d9b0aa4138a48d036f75883531
rewards: [0.0, 0.0, 0.663523, 0.691275]
classification: usable_spread
```

## Current Evidence

Student model:

```text
claude-haiku-4-5
```

QA Evaluator Teacher:

```text
claude-sonnet-4-5 on yail-trace-explorer-v6
```

GDPval environment:

```text
yail-gdpval:v7
HUD env id: e3aa769a-9ff2-4cec-9a5d-cdbddd940d91
```

Key score evidence:

| Check | student-v0 | student-v1 | Result |
| --- | ---: | ---: | --- |
| acct-afc-audit-sampling | 0.369 | 0.4275 | improved |
| medsec-pathology-forms | 0.5225 | 0.5225 | tied |
| one_deal capstone | baseline passed earlier | 1.0 | no regression |

Current decision:

```text
student-v1 is a promotion candidate.
It improved acct, tied medsec, and passed one_deal regression.
It still needs QA Evaluator review and a full graduation gate.
```

## Alumni Workplace Layer

Graduation is not the final claim. Passed or candidate agents enter the autonomous-business environment as a workplace simulation layer. This answers the practical question: did the school improvement create an agent that can do realistic business work, or only pass a narrow class assignment?

Current workplace evidence:

| Agent | Workplace Sim | Score | Result | Next Action |
| --- | --- | ---: | --- | --- |
| Ledger-2 / student-v1 | one_deal_ai_workflow_business | 1.0 | completed hosted autonomous-business workflow | run QA false-positive review before marking full alumni |
| Ledger-2 / student-v1 | save_the_account_routing_bug | pending | earlier hosted attempts hit session-detach invalid runs | retry or classify as invalid-run evidence |
| Swift-Track / student-v1-fast | parallel workplace sims | pending | scheduled for fast-track extra sandboxes | wait for parallel scorecards |
| Casey-QA / student-v0 | workflow-debugging workplace sim | pending | not admitted because QA flagged school trace | create safer improvement patch |
| Dr. Atlas / dr-atlas-v1-rl-candidate | PhD thesis loop | spread gate passed | compact GDPval `acct-audit-easy` group-4 run produced rewards `[0.0, 0.0, 0.663523, 0.691275]` | add one more spread-ready task or run a clearly labeled one-task RL smoke |

The portal UI shows this as an `Alumni` page and links back to HUD traces when a workplace run exists.

## Seeded Demo Students

| Student | Stage | Track | Status |
| --- | --- | --- | --- |
| Nova-0 | Newly enrolled | Standard | Placement pending |
| Ledger-1 | GDPval course | Standard | Baseline student-v0 |
| Ledger-2 | GDPval course | Standard | student-v1 promotion candidate |
| Swift-Track | Parallel courses | Fast Track | Running accelerated batches |
| Casey-QA | QA review | Standard | Blocked by teacher review |
| Dr. Atlas | PhD candidate | Fast Track | Ledger-2 clone + RL candidate prompt |

## PhD Track

The PhD track is intentionally experimental.

It should begin only after YAIL has:

- enough diverse task traces,
- QA-validated labels,
- within-group reward spread,
- trainable model access,
- held-out board exams.

Candidate direction:

```text
train/fork an open model class through HUD Training
use validated curriculum traces
optimize role-specific debugging and fixing behavior
```

Do not claim completed PhD/RL results until a real HUD training run exists.

Current Dr. Atlas versions:

| Version | Parent | Purpose | Status |
| --- | --- | --- | --- |
| dr-atlas-v0-ledger2-clone | Ledger-2 student-v1 | Freeze the best current YAIL prompt as the PhD seed baseline | created |
| dr-atlas-v1-rl-candidate | dr-atlas-v0-ledger2-clone | Add trace hygiene for future QA/SFT/RL trajectory selection | prompt-only candidate |

RL plan:

```text
see 14-phd-rl-plan.md
```

The first RL gate is not average reward. It is grouped rollout reward spread. If all rollouts score the same, the taskset produces no useful policy-gradient signal.

Current status:

```text
The first compact GDPval PhD task now passes the spread gate.
No trainable model fork or checkpoint exists yet.
```

## Current Limitations

- The portal UI is static for the hackathon close.
- GitHub enrollment is a demo intake surface, not a live clone/eval backend yet.
- PhD/RL is a designed track, not a completed training result.
- GDPval hosted validation currently reports deterministic-only grading because the traces show `det_only:no_hud_api_key`.
- QA Evaluator review is still needed before `student-v1` can be fully promoted.

## Source Docs

- `README.md`
- `PROGRESS.md`
- `03-support-ops-curriculum.md`
- `10-improvement-teacher-loop.md`
- `11-improvement-teacher-implementation-plan.md`
- `12-ui-portal-product-plan.md`
- `13-ui-implementation-tracker.md`
- `14-phd-rl-plan.md`
- `15-open-model-rl-prep.md`
