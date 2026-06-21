# YAIL University

**Young Agents in Learning.**

**The only Ivy League for AI agents.**

YAIL University is the HUD hackathon track for turning GDPval-style professional tasks into curricula for AI workers. The idea is not to teach generic tool use; frontier and open models already have a lot of that. The goal is to teach role-specific work behavior through courses, grades, QA evaluation, improvement-teacher patches, and held-out business capstones.

## Core thesis

In 2040, AI workers should not be prompted into production cold. They should go through school:

```text
role curriculum
  -> assignments in HUD environments
  -> traces and grades
  -> QA evaluator teacher review
  -> improvement teacher creates a new version
  -> audited trace dataset
  -> optional SFT/RL
  -> held-out business capstone
```

## First track

Start with a **Customer Support Operations Worker** because it maps cleanly to the current HUD autonomous-business template:

- classify support tickets,
- design routing workflows,
- debug broken routing configs,
- write honest customer replies,
- pass the `one_deal` and `save_the_account` capstones.

## Folder map

- `PROGRESS.md`: decisions, verified setup, gaps, and next actions.
- `01-vision.md`: story, scope, and what YAIL is not.
- `02-school-levels.md`: certificate, diploma, degree, residency, and board exam.
- `03-support-ops-curriculum.md`: the first role curriculum.
- `04-autonomous-business-capstone.md`: how the current HUD business environment works and how we use it.
- `05-qa-teacher-loop.md`: how the QA agent acts as teacher and curriculum auditor.
- `06-demo-plan.md`: hackathon MVP and success metrics.
- `07-graduation-and-env-reuse.md`: graduation tests, scorecards, and reuse of HUD's GDPval/autonomous-business presets.
- `08-gdpval-env-notes.md`: inspection notes from the local HUD GDPval and autonomous-business presets.
- `09-execution-architecture.md`: hosted HUD run shape, model choices, and trace QA evaluator integration.
- `10-improvement-teacher-loop.md`: the second teacher agent that turns QA findings into versioned fixes.
- `11-improvement-teacher-implementation-plan.md`: concrete next build steps for the Improvement Teacher MVP.
- `12-ui-portal-product-plan.md`: product plan for the YAIL University hackathon portal.
- `13-ui-implementation-tracker.md`: module tracker for building the portal, dashboard, enrollment flow, and agent-readable markdown.
