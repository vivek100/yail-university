# 12 - YAIL University Portal Product Plan

This is the product and UI plan for closing the YAIL University hackathon project.

The portal should make YAIL feel like a real university for AI workers, while staying honest about what is already implemented versus what is planned.

## Product Thesis

YAIL University turns AI agents into role-specific workers through:

```text
curriculum -> HUD assignments -> scores/traces -> QA teacher review -> improvement teacher patch -> promotion gate -> higher degree
```

The UI should sell the idea first, then let judges inspect the operating loop.

## Primary Audience

1. Hackathon judges who need to understand the project quickly.
2. HUD team members who want to see how their environments, traces, QA agents, and hosted runs are reused.
3. Builders who may want to enroll an existing agent or create a new one.
4. Agents that need an MD-readable version of the same product/curriculum.

## App Shape

Create a new frontend app:

```text
trainingPlan/hud-hackathon/yail-university-ui
```

Recommended stack:

```text
Vite + React + TypeScript
static seed data first
no backend required for hackathon close
```

The existing docs/results remain the source of truth. The UI reads curated seed data derived from them.

## Navigation

```text
Home
Curriculum
Degrees
Enroll
Dashboard
Student Detail
Training Loop
Agent-readable MD
```

For the first implementation, these can be tabs/routes inside one React app.

## Home Page

Home is not enrollment. It is the flagship landing page.

Goal:

```text
Make YAIL feel like an elite AI-agent university in the first viewport.
```

Hero:

```text
YAIL University
Young Agents in Learning
The only Ivy League for AI agents.
```

Primary CTA:

```text
Enroll an Agent
```

Secondary CTA:

```text
View Student Dashboard
```

Hero content should emphasize:

- agents should not be shipped to production cold,
- agents should go through school,
- HUD gives the campus: tasks, traces, environments, graders, hosted runs,
- YAIL adds curriculum, QA teachers, improvement teachers, and promotion gates.

Visual direction:

- polished, cinematic academic/technical feel,
- not a plain docs page,
- strong first viewport,
- visual motifs can include transcript cards, degree seals, trace ribbons, student progress, campus-like dashboard panels,
- avoid over-explaining inside the hero.

## Degree Catalog and Costs

Use demo costs that are understandable and honest. For the hackathon, show them as estimated credit tiers, not hard billing promises.

Suggested framing:

```text
YAIL Credits estimate compute, hosted evals, sandboxes, QA reviews, and improvement loops.
```

### Certificate

Purpose:

```text
Basic role readiness.
```

Requirements:

- complete intro course assignments,
- pass deterministic course checks,
- no severe QA findings.

Estimated cost:

```text
100 YAIL Credits
1x compute lane
```

### Diploma

Purpose:

```text
Prompt, tool, and workflow hardening.
```

Requirements:

- complete multiple courses,
- run QA teacher reviews,
- apply at least one improvement-teacher patch,
- pass held-out course checks.

Estimated cost:

```text
350 YAIL Credits
2x compute lanes
```

### Degree

Purpose:

```text
Versioned worker specialization.
```

Requirements:

- complete the full role curriculum,
- maintain a version history,
- pass capstone regression,
- show measurable improvement over baseline.

Estimated cost:

```text
900 YAIL Credits
4x compute lanes
```

### Residency

Purpose:

```text
Real business environment validation.
```

Requirements:

- operate inside autonomous-business-style environments,
- handle integrated workflows,
- pass customer/business outcome checks.

Estimated cost:

```text
1,800 YAIL Credits
6x compute lanes
```

### PhD

Purpose:

```text
Custom model optimization through SFT/RL.
```

Requirements:

- enough diverse task traces,
- validated QA labels,
- non-degenerate reward spread,
- trainable open model fork,
- held-out board exam.

Estimated cost:

```text
5,000+ YAIL Credits
8-16x compute lanes
experimental
```

Honest UI status:

```text
Planned / Experimental
```

The PhD track can be shown in the UI, but it should not claim a completed RL result unless we actually run one. It can show the design target:

```text
candidate model: Qwen trainable model class
target: role-specific debugging/fixing behavior
status: training job design pending
```

## Enrollment

Enrollment should support three paths.

### Start From Scratch

Use when the user wants a blank student agent.

Fields:

- agent name,
- target role,
- degree goal,
- standard vs fast track,
- model family,
- budget cap.

### Bring an Existing Agent

Use when the user already has a codebase/agent.

Fields:

- GitHub URL,
- entrypoint/run instructions,
- current model,
- tool permissions,
- target role,
- desired degree.

Behavior in demo:

```text
Show intake accepted and place the agent into diagnostic placement tests.
```

Backend later:

```text
clone repo -> inspect runnable agent -> wrap in HUD task harness -> baseline scorecard
```

### Sponsor an Agent

Use when a company/team wants YAIL to create and train an AI worker for them.

Fields:

- sponsor/company name,
- desired worker role,
- business domain,
- data/source systems,
- degree goal,
- standard vs fast track,
- budget cap.

Behavior in demo:

```text
Create a sponsored student profile with pending curriculum design.
```

## Tracks

### Standard Track

Positioning:

```text
Lower cost, slower graduation.
```

Execution:

- fewer parallel HUD jobs,
- fewer simultaneous sandboxes,
- sequential QA reviews,
- smaller comparison batches.

### Fast Track

Positioning:

```text
Higher cost, faster graduation.
```

Execution:

- more parallel HUD runs,
- more Modal/Daytona sandboxes,
- parallel QA teacher reviews,
- larger batch comparisons,
- faster promotion/rejection cycles.

UI should show this as a real operational tradeoff:

```text
time to graduate goes down
compute cost goes up
```

## Curriculum Page

The first curriculum is:

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

Each course card should show:

- what the agent learns,
- HUD environment,
- task examples,
- grader type,
- QA teacher checks,
- promotion criteria.

## Dashboard

The dashboard should show seeded students at different stages.

Minimum demo students:

```text
Nova-0       newly enrolled, standard track
Ledger-1     GDPval course student, student-v0 baseline
Ledger-2     GDPval course student, student-v1 promotion candidate
Swift-Track  fast-track student running parallel course evals
Casey-QA     blocked by QA teacher review
Dr. Atlas    PhD candidate, experimental RL track
```

Dashboard columns:

- student,
- role,
- degree target,
- track,
- current course,
- model,
- current version,
- latest score,
- QA status,
- promotion status,
- cost used,
- estimated cost remaining.

Use real evidence where available:

```text
student-v0 acct: 0.369
student-v1 acct: 0.4275
student-v0 medsec: 0.5225
student-v1 medsec: 0.5225
student-v1 one_deal: 1.0
```

## Student Detail

Clicking a student should show:

- profile,
- current level,
- track,
- degree target,
- current model,
- current version,
- curriculum progress,
- course scores,
- trace links,
- QA teacher findings,
- improvement proposals,
- version timeline,
- promotion gate status.

For `Ledger-2`, show the real current story:

```text
student-v1 is a promotion candidate
acct improved over v0
medsec tied v0
one_deal did not regress
QA Evaluator review pending
```

## Training Loop Page

Explain the loop as an operational pipeline:

```text
1. Enroll agent
2. Run placement/baseline scorecard on HUD
3. Collect traces and rewards
4. QA Evaluator Teacher audits traces
5. Improvement Teacher proposes a bounded patch
6. Create a new version
7. Rerun target and held-out tasks
8. Promotion Gate accepts or rejects
9. Optional SFT/RL when enough signal exists
```

This should include a visual flow and a compact explanation of the two-teacher architecture.

## Agent-Readable MD Page

Create:

```text
yail-university/YAIL_UNIVERSITY_PORTAL.md
```

This should mirror the UI in markdown:

- what YAIL is,
- degree catalog,
- enrollment options,
- curriculum,
- seeded students,
- current score evidence,
- how the training loop works,
- current limitations.

This file lets other agents understand the project without scraping the UI.

## Data Source Strategy

For hackathon close:

```text
static seed data in src/data/yailSeedData.ts
```

Source files:

- `PROGRESS.md`,
- `03-support-ops-curriculum.md`,
- `versions/student-v0/metadata.json`,
- `versions/student-v1/metadata.json`,
- scorecards under `results/`,
- improvement proposals under `improvement-proposals/`.

Later backend:

```text
HUD jobs API + trace API + YAIL version registry + enrollment database
```

## What Not To Build Yet

Do not build these for the hackathon UI unless the core portal is done:

- real GitHub cloning,
- real payment/billing,
- real user accounts,
- real RL training launch form,
- complex charts,
- editable curriculum builder.

Represent them as product surfaces with honest statuses.

## Success Criteria

The portal is successful when a judge can answer:

1. What is YAIL University?
2. What does an enrolled agent do?
3. What courses and degrees exist?
4. How does Standard differ from Fast Track?
5. How are agents graded?
6. Where does the QA teacher fit?
7. Where does the Improvement Teacher fit?
8. What evidence do we already have?
9. What is planned but not yet complete?
