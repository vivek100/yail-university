# 10 - Improvement Teacher Loop

YAIL should not rely on a human or a coding assistant to decide every intervention. The loop needs a second teacher agent whose job is to turn QA evidence into a concrete next version.

## Two teachers

```text
QA Evaluator Teacher
  -> audits traces and task quality
  -> identifies failure modes, false positives, false negatives,
     prompt/grader mismatch, and reward hacking

Improvement Teacher
  -> consumes QA findings, trace artifacts, scorecards, and repo files
  -> decides what should change
  -> creates a versioned patch to agent, environment, tools, tasks, or files
```

The QA Evaluator answers:

```text
what happened and why?
```

The Improvement Teacher answers:

```text
what should change before the next run?
```

## What it can change

The Improvement Teacher can modify the training system, but only inside a typed change boundary.

Allowed change targets:

- `agent_config`: role prompt, workflow instructions, examples, tool-use policy, max steps, model choice if the experiment permits it.
- `environment`: capabilities, workspace setup, tool wrappers, runtime setup, visible files.
- `task`: task prompt, visible reference files, task metadata, task grouping.
- `grader`: only when QA evidence shows prompt/grader mismatch, grader bug, missing hidden case, or reward hacking.
- `curriculum`: assign remedial lesson, add retake, change course order.
- `dataset`: mark trace as positive, negative, invalid, or SFT candidate.

Not allowed:

- leak hidden answers into the prompt or visible files,
- make a held-out task easier just to improve score,
- edit the grader when the student simply failed a fair task,
- accept a version without held-out retest,
- train on evaluation-only held-out traces.

## Version objects

Every iteration should produce explicit version metadata.

```text
student-v0
  model: claude-haiku-4-5
  prompt: baseline
  tools: baseline

student-v1
  parent: student-v0
  changed_by: improvement-teacher-v0
  change_type: agent_config
  patch: prompts/student_v1.md
  reason: QA found missing workbook-verification workflow

env-v1
  parent: env-v0
  change_type: environment
  reason: QA found missing required binary/tool or broken workspace setup

taskset-v1
  parent: taskset-v0
  change_type: task_or_grader
  reason: QA found prompt/grader mismatch
```

## Loop

```text
1. Run student-vN on HUD taskset.
2. Collect HUD reward, trace_id, job_id, and artifacts.
3. Run QA Evaluator Teacher on selected traces.
4. Run Improvement Teacher with:
   - student trace,
   - QA findings,
   - scorecard,
   - relevant repo files,
   - allowed change targets.
5. Improvement Teacher emits a change proposal.
6. Apply the patch to create vN+1.
7. Deploy/sync if environment or taskset changed.
8. Rerun target task plus held-out checks.
9. Promotion Gate accepts or rejects vN+1.
```

## Change proposal schema

The Improvement Teacher should emit structured output before applying edits.

```json
{
  "change_id": "student-v1-workbook-checklist",
  "parent_versions": {
    "student": "student-v0",
    "environment": "yail-gdpval:v3",
    "taskset": "yail-gdpval-smoke"
  },
  "target": "agent_config",
  "failure_evidence": [
    {
      "trace_id": "b002338c-c79e-40df-8fc7-662c49c3c3fa",
      "qa_finding": "agent did not verify workbook sheets before final answer"
    }
  ],
  "proposed_change": "Add a spreadsheet-workflow checklist to the student prompt.",
  "files_to_change": [
    "agents/student_haiku_v1.md"
  ],
  "risk": "May overfit to spreadsheet tasks if used globally.",
  "validation_plan": [
    "rerun acct-afc-audit-sampling",
    "rerun medsec-pathology-forms",
    "rerun one_deal as non-regression"
  ],
  "promotion_rule": "accept only if GDPval reward improves and one_deal does not regress"
}
```

## Promotion Gate

The Promotion Gate is deterministic. It is not another vibes-based agent.

Accept a new version only if:

- target-task reward improves or reaches threshold,
- held-out task reward does not regress beyond tolerance,
- QA Evaluator finds no false positive or reward hacking,
- task-integrity checks pass,
- invalid hosted runs are excluded and rerun if needed.

Reject or quarantine if:

- score improves by leaking answers,
- grader was weakened without QA evidence,
- held-out performance regresses,
- QA finds false positive,
- the run is invalid due to platform/runtime failure.

## Hackathon MVP

For the first demo, keep the Improvement Teacher simple:

```text
input: scorecard + selected traces + QA findings
output: one versioned agent prompt/tool workflow patch
validation: rerun graduation preset
```

Do not start with SFT or RL. First prove that the agent-generated intervention improves a cheaper student model on HUD-hosted tasks.
