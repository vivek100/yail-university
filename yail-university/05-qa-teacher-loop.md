# 05 - QA Evaluator Teacher Loop

The QA Evaluator Teacher reviews both the student agent and the curriculum itself. It does not decide or apply fixes. Its job is to produce evidence about what happened.

For the first implementation, the QA Evaluator Teacher should be HUD's existing trace QA environment:

```text
baseline source: hud-evals/hud-trace-explorer
YAIL v6 fork: yail-trace-explorer-v6
QA model: claude-sonnet-4-5
```

The YAIL v6 fork should be treated as a faithful migration baseline, not as our improved QA agent.
The QA prompts and rubrics should stay aligned with HUD's original trace-explorer. Changes belong in
SDK/runtime plumbing unless we explicitly create a separate improved teacher version.

The student worker should initially be:

```text
student model: claude-haiku-4-5
```

YAIL now uses two teachers:

```text
QA Evaluator Teacher
  -> audits traces and task quality

Improvement Teacher
  -> uses QA findings to create the next version of the agent, env, tools, tasks, or files
```

This document covers only the QA Evaluator Teacher. The Improvement Teacher is defined in `10-improvement-teacher-loop.md`.

## Before a task runs

The QA Evaluator Teacher reviews task design:

- is the prompt clear,
- does the grader match the prompt,
- are expected outputs correct,
- are hidden tests fair,
- is there answer leakage,
- can the task be reward-hacked,
- is the task too easy or too hard,
- will there be reward spread.

## After a task runs

The QA Evaluator Teacher reviews the trace:

- what did the student do,
- did it use the right tools,
- did it solve the actual task,
- did it game the grader,
- was a low score justified,
- was a high score deserved,
- what weakness should the next lesson target.

Use trace-explorer templates as separate review lenses:

- `failure_analysis`: why did a low-reward trace fail?
- `false_positive_analysis`: did the student get undeserved credit?
- `false_negative_analysis`: did the student solve it but get unfairly failed?
- `prompt_alignment_analysis`: did the prompt and grader match?
- `reward_hacking_analysis`: did the student game the reward?

## Loop

```text
student attempts lesson
  -> HUD records trace and reward
  -> trace-explorer QA Evaluator Teacher reviews trace_id with claude-sonnet-4-5
  -> QA findings are written to the scorecard
  -> Improvement Teacher consumes those findings
  -> Improvement Teacher proposes or applies a versioned patch
  -> Promotion Gate decides whether the new version is accepted
  -> high-quality traces enter dataset
```

Real loop runs should be HUD-hosted. Local runs are only smoke tests.

## Dataset outputs

The loop should produce:

- labeled student traces,
- QA Evaluator feedback,
- task-design audits,
- improvement proposals,
- versioned patches,
- corrected examples,
- SFT-ready conversations,
- RL-ready HUD rewards.

## v6 work

The original trace QA environment was older scenario-style HUD code. YAIL now has a v6 migration fork:

```text
repo: trainingPlan/hud-hackathon/repos/yail-trace-explorer-v6
HUD env: yail-trace-explorer-v6
```

Migration rule:

```text
preserve HUD QA prompts/rubrics
change only SDK plumbing, packaging, runtime, and trace-fetch compatibility
```

Hosted smoke already passed for `false_positive_analysis` on the first YAIL autonomous-business trace.
`reward_hacking_analysis` also passed on the same trace.

Current blocker:

```text
prompt_alignment_analysis and one failure_analysis retry hit a hosted Modal runtime error:
"Trace not bound to a Session"
```

Do not treat those failed runs as QA-agent verdict failures. They are hosted runtime failures until HUD confirms otherwise.
