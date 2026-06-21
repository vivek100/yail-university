# 13 - YAIL University UI Implementation Tracker

This tracker converts the portal plan into buildable modules.

## Current State

The first YAIL frontend app now exists.

Current YAIL assets:

```text
yail-university/*.md                product/planning docs
yail-university/versions/*          student version registry
yail-university/improvement-*       teacher/proposal artifacts
results/*.json                      HUD scorecards and trace IDs
repos/yail-gdpval                   GDPval v7 environment code
repos/yail-trace-explorer-v6        QA Evaluator Teacher environment
```

Recommended new app:

```text
trainingPlan/hud-hackathon/yail-university-ui
```

Implemented app:

```text
trainingPlan/hud-hackathon/yail-university-ui
stack: Vite + React + TypeScript
hero asset: public/yail-hero-campus.png
dev URL: http://127.0.0.1:5177
```

## Implementation Boundary

### Build Now

- polished landing/home page,
- degree catalog with estimated costs,
- enrollment surface with three paths,
- curriculum and course detail surface,
- dashboard with seeded agents,
- student detail view,
- alumni workplace outcomes,
- training loop explainer,
- agent-readable markdown page,
- static seed-data adapter.

### Preserve

- existing YAIL docs,
- existing HUD repos,
- existing scorecard runner,
- existing scorecard JSON files,
- existing version/proposal artifacts.

### Defer

- real GitHub cloning,
- real account/auth,
- real billing,
- real live HUD API dashboard,
- real PhD RL launch form,
- real enrollment database.

## Module 1 - App Scaffold

### Purpose

Create the standalone frontend app that can be developed and demoed independently.

### Responsibilities

- initialize Vite React TypeScript app,
- add basic routing or tab state,
- set build/dev scripts,
- define global styles,
- keep app independent from existing `landing/`.

### Primary Files

```text
yail-university-ui/package.json
yail-university-ui/index.html
yail-university-ui/src/main.tsx
yail-university-ui/src/App.tsx
yail-university-ui/src/styles.css
```

### Depends On

None.

### Done When

- app starts locally,
- app builds,
- no unrelated files are changed.

### Test Requirements

- `npm run build`
- manual browser smoke check.

## Module 2 - Seed Data Adapter

### Purpose

Keep demo data centralized and grounded in real YAIL evidence.

### Responsibilities

- define typed degree catalog,
- define enrollment tracks,
- define curriculum/course data,
- define seeded agents,
- include real scorecard/trace references,
- distinguish implemented, candidate, blocked, and planned states.

### Primary Files

```text
yail-university-ui/src/data/yailSeedData.ts
yail-university-ui/src/types.ts
```

### Depends On

Module 1.

### Done When

Seed data includes:

- degree costs,
- Standard/Fast Track details,
- enrollment paths,
- 5-6 demo students,
- real `student-v0` and `student-v1` results,
- PhD candidate with experimental status.

### Test Requirements

- TypeScript build validates the data shape.
- Spot-check score values against current scorecards.

## Module 3 - Visual Shell and Navigation

### Purpose

Provide the portal structure without mixing product data into layout code.

### Responsibilities

- header/nav,
- active section state,
- responsive layout,
- primary CTA routing to enroll,
- dashboard CTA routing.

### Primary Files

```text
yail-university-ui/src/App.tsx
yail-university-ui/src/components/Nav.tsx
yail-university-ui/src/components/Layout.tsx
```

### Depends On

Modules 1 and 2.

### Done When

- all major sections are reachable,
- mobile and desktop nav work,
- CTAs navigate to the expected section.

### Test Requirements

- `npm run build`
- browser check desktop and mobile widths.

### User Validation Checkpoint

User should approve the overall visual direction before deeper polish.

## Module 4 - Home Landing Page

### Purpose

Make YAIL feel like a compelling university/product, not a form page.

### Responsibilities

- flashy hero,
- YAIL name/tagline,
- campus/product value proposition,
- CTA buttons,
- proof/evidence strip,
- short degree/curriculum preview,
- avoid making enrollment the first screen.

### Primary Files

```text
yail-university-ui/src/components/HomePage.tsx
yail-university-ui/src/components/HomePage.css
```

### Depends On

Modules 2 and 3.

### Done When

- first viewport communicates YAIL clearly,
- enrollment is available but not dominant,
- real evidence is visible without clutter.

### Test Requirements

- desktop/mobile screenshot check,
- text does not overlap at narrow widths.

### User Validation Checkpoint

User should approve hero tone: elite university + AI operations, flashy but credible.

## Module 5 - Degree Catalog

### Purpose

Show what agents can earn and what each degree costs.

### Responsibilities

- Certificate, Diploma, Degree, Residency, PhD,
- estimated YAIL Credit costs,
- compute lane differences,
- status labels,
- requirements and graduation criteria.

### Primary Files

```text
yail-university-ui/src/components/DegreesPage.tsx
yail-university-ui/src/components/DegreeCard.tsx
```

### Depends On

Module 2.

### Done When

- every degree has cost, requirements, and status,
- PhD is shown as experimental/planned unless backed by a real run.

### Test Requirements

- TypeScript build,
- visual check for card density and readability.

## Module 6 - Curriculum Page

### Purpose

Show the role curriculum and how courses map to HUD tasks/environments.

### Responsibilities

- course list,
- course detail panel,
- HUD environment used,
- actual data/task substrate used by each course,
- trained or evaluated agents per course,
- model used for course runs,
- course-level run evidence with trace links,
- grader type,
- QA teacher checks,
- promotion criteria.

### Primary Files

```text
yail-university-ui/src/components/CurriculumPage.tsx
yail-university-ui/src/components/CourseDetail.tsx
```

### Depends On

Module 2.

### Done When

- Customer Support Ops curriculum is readable,
- GDPval and autonomous-business reuse is explicit,
- courses feel like school, not random eval tasks.
- course details show actual task data and agent evidence rather than only course names.

### Test Requirements

- TypeScript build,
- browser check for course/detail interaction.

## Module 7 - Enrollment Page

### Purpose

Let users understand how an agent enters YAIL.

### Responsibilities

- Start From Scratch path,
- Bring Existing Agent path with GitHub URL,
- Sponsor an Agent path,
- degree goal selector,
- Standard/Fast Track selector,
- budget/cost preview,
- demo-only submit behavior.

### Primary Files

```text
yail-university-ui/src/components/EnrollPage.tsx
yail-university-ui/src/components/EnrollmentPathCard.tsx
```

### Depends On

Modules 2 and 5.

### Done When

- enrollment options are clear,
- GitHub/adopt path is visible,
- sponsor path is visible,
- Fast Track cost tradeoff is visible.

### Test Requirements

- form state smoke test by manual browser interaction,
- TypeScript build.

## Module 8 - Dashboard

### Purpose

Show enrolled agents and their school status.

### Responsibilities

- seeded student table/cards,
- filters by level/status/track,
- visible scores,
- current version,
- QA status,
- promotion status,
- click-through to student detail.

### Primary Files

```text
yail-university-ui/src/components/DashboardPage.tsx
yail-university-ui/src/components/StudentTable.tsx
```

### Depends On

Module 2.

### Done When

Dashboard includes:

- newly enrolled student,
- standard-track course student,
- fast-track student,
- QA-blocked student,
- promotion candidate,
- PhD candidate.

### Test Requirements

- TypeScript build,
- browser check that row/card click opens student detail.

## Module 9 - Student Detail

### Purpose

Make the improvement loop inspectable at the student level.

### Responsibilities

- profile summary,
- degree/track,
- curriculum progress,
- score history,
- version timeline,
- trace/job links,
- QA findings,
- improvement proposals,
- promotion gate status.

### Primary Files

```text
yail-university-ui/src/components/StudentDetailPage.tsx
yail-university-ui/src/components/VersionTimeline.tsx
yail-university-ui/src/components/ScoreBreakdown.tsx
```

### Depends On

Modules 2 and 8.

### Done When

`Ledger-2` shows:

```text
student-v1
acct improved over v0
medsec tied v0
one_deal passed
QA pending
promotion candidate
```

### Test Requirements

- TypeScript build,
- manual check against current `PROGRESS.md`.

## Module 10 - Training Loop Explainer

### Purpose

Explain how YAIL actually hill-climbs agents.

### Responsibilities

- two-teacher architecture,
- HUD hosted run as source of truth,
- QA Evaluator Teacher,
- Improvement Teacher,
- Promotion Gate,
- optional SFT/RL path.

### Primary Files

```text
yail-university-ui/src/components/TrainingLoopPage.tsx
yail-university-ui/src/components/LoopDiagram.tsx
```

### Depends On

Module 2.

### Done When

- viewer can explain the loop after reading the page,
- PhD/RL is shown as downstream from enough validated trace data.

### Test Requirements

- TypeScript build,
- visual check for diagram readability.

## Module 12 - Alumni Workplace Outcomes

### Purpose

Show whether YAIL graduates or promotion candidates perform in the autonomous-business workplace simulation, not just in school tasks.

### Responsibilities

- list alumni/candidate agents,
- show autonomous-business workplace tasks,
- show score, pending, blocked, and invalid-run states,
- link passing workplace runs to HUD traces,
- explain how workplace failures feed the next curriculum loop.

### Primary Files

```text
yail-university-ui/src/components/AlumniPage.tsx
yail-university-ui/src/data/yailSeedData.ts
yail-university-ui/src/types.ts
```

### Depends On

Modules 2, 8, and 9.

### Done When

The Alumni page shows:

```text
Ledger-2 student-v1 one_deal_ai_workflow_business score 1.0
save_the_account_routing_bug pending due hosted invalid-run evidence
Swift-Track pending parallel workplace sims
Casey-QA blocked from workplace sim by QA hold
Dr. Atlas PhD workplace loop marked experimental
```

### Test Requirements

- TypeScript build,
- browser check desktop and mobile widths,
- no horizontal overflow,
- visible trace link for scored workplace run.

## Module 11 - Agent-Readable Markdown

### Purpose

Mirror the UI in a markdown file that agents can consume directly.

### Responsibilities

- summarize YAIL,
- list degree catalog and costs,
- list enrollment paths,
- list curriculum,
- list seeded students,
- list current score evidence,
- explain training loop,
- state limitations.

### Primary Files

```text
yail-university/YAIL_UNIVERSITY_PORTAL.md
```

### Depends On

Modules 2-10 conceptually, but can be written before the app.

### Done When

- markdown is readable standalone,
- agents can use it as project context,
- it links to deeper docs.

### Test Requirements

- manual read-through,
- links checked for local files.

## Module Order

Build in this order:

```text
1. Module 11 - Agent-readable Markdown
2. Module 1 - App Scaffold
3. Module 2 - Seed Data Adapter
4. Module 3 - Visual Shell and Navigation
5. Module 4 - Home Landing Page
6. Module 5 - Degree Catalog
7. Module 6 - Curriculum Page
8. Module 7 - Enrollment Page
9. Module 8 - Dashboard
10. Module 9 - Student Detail
11. Module 10 - Training Loop Explainer
12. Module 12 - Alumni Workplace Outcomes
```

Reason:

```text
The markdown locks the story first.
The seed data locks the contract.
The shell and landing define the demo feel.
The operational pages then plug into stable data.
```

## Tracker

| Module | Status | Notes |
| --- | --- | --- |
| Agent-readable Markdown | Done | `YAIL_UNIVERSITY_PORTAL.md` created |
| App Scaffold | Done | New Vite React app in `yail-university-ui` |
| Seed Data Adapter | Done | Real values from scorecards/progress included |
| Visual Shell/Nav | Done | Tab-style navigation implemented |
| Home Landing Page | Done | Flashy YAIL-first page with generated campus asset |
| Degree Catalog | Done | Includes YAIL Credit costs |
| Curriculum Page | Done | Customer Support Ops first |
| Enrollment Page | Done | Scratch/GitHub/Sponsor paths |
| Dashboard | Done | 6 demo students |
| Student Detail | Done | Ledger-2 and other student records available |
| Training Loop Explainer | Done | Two-teacher + promotion gate |
| Alumni Workplace Outcomes | Done | Autonomous-business workplace layer with real one_deal evidence |
| PhD Candidate Lineage | Done | Dr. Atlas cloned from Ledger-2 and prompt-improved for RL planning |

## Verification

```text
npm install
npm run build
dev server: http://127.0.0.1:5177
desktop screenshot check: passed
mobile screenshot check: passed
dashboard click/detail check: passed
student transcript/detail evidence check: passed
alumni workplace page check: passed
enrollment page check: passed
horizontal overflow check: passed
hero asset load check: passed
```

## Demo Acceptance Criteria

The UI is demo-ready when:

1. The home page feels like YAIL University, not a form.
2. Enrollment supports scratch, GitHub/adopt, and sponsor paths.
3. Degree costs are visible.
4. Standard vs Fast Track tradeoff is clear.
5. Dashboard shows at least 6 agents at different stages.
6. Student detail shows real `student-v0`/`student-v1` evidence.
7. Alumni workplace page shows autonomous-business outcomes and pending/invalid-run states.
8. PhD exists as an experimental track, not an over-claimed completed result.
9. Agent-readable markdown exists.
10. `npm run build` passes.
11. Browser checks pass at desktop and mobile widths.

## Open Product Questions

1. Should costs be displayed only in YAIL Credits, or also as approximate USD?
2. Should the hero visual be a university/campus metaphor, a trace dashboard metaphor, or a hybrid?
3. Should enrollment submit create local-only demo state, or just show a confirmation?
4. Should the PhD candidate show a specific model name or stay model-family-level until we run training?

Default decisions unless changed:

```text
costs: YAIL Credits only
hero: hybrid elite university + trace operating system
enrollment: local demo confirmation only
PhD: Ledger-2 clone seed, claude-haiku-4-5 prompt candidate, future trainable fork experimental
```
