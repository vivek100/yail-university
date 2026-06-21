# 06 - Demo Plan

## MVP

Show one worker going through YAIL University:

```text
base agent
  -> GDPval / GDPval-style role lessons
  -> support-ops lessons
  -> QA Evaluator Teacher feedback
  -> Improvement Teacher creates v1
  -> retest
  -> autonomous-business capstone
```

Initial model choices:

```text
student worker: claude-haiku-4-5
QA Evaluator Teacher: claude-sonnet-4-5 through trace-explorer
Improvement Teacher: claude-sonnet-4-5 or coding-agent backed
```

## Success Metrics

Track:

- lesson scores before vs after diploma updates,
- capstone score before vs after curriculum,
- graduation pass/fail on held-out lessons,
- QA Evaluator Teacher findings,
- improvement proposals and accepted patches,
- number of audited traces collected,
- cost and time to graduate one worker.

## Hackathon Demo Script

1. Start with a base agent on the autonomous-business capstone.
2. Show where it fails.
3. Enroll it in support-ops courses using GDPval / GDPval-style tasks.
4. Run lessons and show HUD traces.
5. Run trace-explorer QA on the lesson traces; QA Evaluator Teacher identifies weak skills or task flaws.
6. Run the Improvement Teacher; it creates a versioned agent/env/tool/task patch.
7. Rerun held-out lessons.
8. Rerun autonomous-business capstone.
9. Show score improvement and graduation report.

## Existing Environment Setup

Use HUD presets before writing custom environments:

```bash
hud init yail-gdpval --preset gdpval
hud init yail-autobiz --preset autonomous-businesses
```

The demo should reuse these where possible, then add only the thin YAIL layer: course definitions, QA Evaluator reviews, Improvement Teacher patches, scorecards, and graduation gates.

## Hosted Run Requirement

Real demo runs should happen on HUD using HUD models. Local runs are for smoke testing only.

Target shape:

```text
deploy/sync GDPval and autobiz tasksets
  -> run claude-haiku-4-5 student on HUD
  -> collect trace IDs
  -> run trace-explorer QA with claude-sonnet-4-5
  -> run Improvement Teacher to create student-v1 or env-v1
  -> rerun HUD-hosted graduation preset
  -> aggregate scorecard
```

## Stretch

After the diploma loop works, create a small SFT dataset from audited traces and train a degree-level worker.
