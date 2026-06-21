# Student v0 Agent

Baseline YAIL student worker.

```text
model: claude-haiku-4-5
agent_type: claude
system_prompt: null
```

This version intentionally uses HUD's default hosted Claude agent behavior. It is the parent version for the first Improvement Teacher loop.

## Role

Customer Support Operations Worker candidate.

## Current behavior

Runs GDPval course tasks and autonomous-business capstone tasks with no YAIL-specific workflow scaffold.

## Baseline graduation result

```text
scorecard: trainingPlan/hud-hackathon/results/yail-scorecard-graduation-haiku-baseline-20260621.json
passed: 1
failed: 2
invalid_run: 1
completed-run success rate: 0.3333333333333333
mean completed reward: 0.3333333333333333
```
