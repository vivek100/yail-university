# 11 - Improvement Teacher Implementation Plan

This is the next build item for YAIL University.

## Goal

Create the first Improvement Teacher MVP that can take a failed HUD graduation run plus QA Evaluator findings and produce a versioned patch for the next student/environment iteration.

The first target should be cheap and controlled:

```text
student-v0: claude-haiku-4-5 baseline
student-v1: same model, improved agent_config / workflow prompt
```

Do not start with SFT, RL, or grader changes.

Exception made during first validation: the hosted GDPval grader had runtime defects that collapsed valid deliverables to `0.0` and hid the reason. Those were measurement fixes, not reward-shaping or task-easier changes.

## Module 1 - Version Registry

Create version metadata files:

```text
yail-university/versions/student-v0/metadata.json
yail-university/versions/student-v0/agent.md
yail-university/versions/student-v1/metadata.json
yail-university/improvement-proposals/
```

Status:

```text
done: versions/student-v0/metadata.json
done: versions/student-v0/agent.md
done: versions/student-v1/metadata.json
done: versions/student-v1/agent.md first workflow prompt patch
done: improvement-proposals/
```

Version metadata should track:

- version id,
- parent version,
- model,
- prompt/config file,
- allowed tools,
- created_by,
- source scorecard,
- source QA findings,
- validation scorecard.

## Module 2 - QA Finding Bundle

Create a small JSON bundle from the graduation baseline and QA reviews.

Input:

```text
results/yail-scorecard-graduation-haiku-baseline-20260621.json
trace-explorer QA job outputs
```

Output:

```text
improvement-proposals/context-bundle-001.json
```

Status:

```text
done: improvement-proposals/context-bundle-001.json
```

Minimum fields:

- target role,
- parent student version,
- failed tasks,
- passed tasks for regression,
- trace IDs,
- rewards,
- QA findings,
- invalid runs,
- allowed change targets.

## Module 3 - Improvement Teacher Prompt

Create the first Improvement Teacher prompt as a file, not inline code:

```text
yail-university/improvement-teacher/improvement_teacher_v0.md
```

Status:

```text
done: improvement-teacher/improvement_teacher_v0.md
```

It should instruct the agent to:

- read the bundle,
- pick one bounded intervention,
- avoid hidden-answer leakage,
- avoid grader weakening,
- prefer `agent_config` changes first,
- emit a structured change proposal,
- include a validation plan.

## Module 4 - Change Proposal Schema

Create a proposal JSON schema:

```text
yail-university/improvement-teacher/change_proposal.schema.json
```

Status:

```text
done: improvement-teacher/change_proposal.schema.json
```

Required fields:

- `change_id`,
- `parent_versions`,
- `target`,
- `failure_evidence`,
- `proposed_change`,
- `files_to_change`,
- `risk`,
- `validation_plan`,
- `promotion_rule`.

## Module 5 - First Patch Target

For the first loop, the Improvement Teacher should patch only:

```text
yail-university/versions/student-v1/agent.md
```

Likely patch type:

```text
spreadsheet-workflow checklist
deliverable verification checklist
tool-use policy for inspecting generated files before final answer
```

This targets the two GDPval failures without changing the model or the task.

Status:

```text
done: student-v1-work-product-workflow proposal
done: versions/student-v1/agent.md patched with professional work-product workflow
verified: --student-system-prompt-file routes the prompt into hosted HUD claude runs
```

## Module 6 - Promotion Gate

Create a deterministic gate script or documented command flow.

First gate:

```text
rerun graduation preset with student-v1 if agent config routing is supported
compare against student-v0 baseline
accept only if:
  GDPval reward improves,
  one_deal does not regress,
  QA Evaluator finds no false positive,
  invalid runs are excluded or rerun
```

If HUD's `claude` agent cannot yet consume our custom student prompt/config cleanly, the immediate engineering task is to add that routing before claiming a v1 run.

Status:

```text
partial: scorecard runner now supports --student-system-prompt-file
verified: dry run routes --config system_prompt=<from file> into each HUD eval command
verified: hosted medsec run routes student-v1 system prompt into claude-haiku-4-5
partial lift: student-v1 and student-v0 both scored 0.5225 on medsec after GDPval v7 measurement fixes
partial lift: student-v1 improved acct from 0.369 to 0.4275
regression check: student-v1 passed one_deal at 1.0
promotion state: candidate pending QA Evaluator review and full gate
```

First validation evidence:

```text
student-v1 medsec scorecard: results/yail-scorecard-student-v1-medsec-validation-after-import-fix-v7-20260621.json
student-v1 job: 73409774b9ab44868c15e6e7e72da9f1
student-v1 trace: 176ff833-d173-4fed-88af-7b9305e7651c
student-v1 reward: 0.5225

student-v0 medsec scorecard: results/yail-scorecard-student-v0-medsec-validation-fixed-env-v7-20260621.json
student-v0 job: 9aacd526702741008744b5f355ed1cad
student-v0 trace: 56a02063-376b-435d-bcac-6c3c915c96e5
student-v0 reward: 0.5225

student-v1 acct scorecard: results/yail-scorecard-student-v1-acct-validation-fixed-env-v7-20260621.json
student-v1 acct job: b525dffdfafb4bf99c0d854bca867b78
student-v1 acct trace: fecfac1d-c3a2-4561-a02c-643ba65bc386
student-v1 acct reward: 0.4275

student-v0 acct scorecard: results/yail-scorecard-student-v0-acct-validation-fixed-env-v7-20260621.json
student-v0 acct job: e8d134facdec4721b7d1b5aeb662b6ec
student-v0 acct trace: 4f400d71-22e2-43d9-b8af-39703654e3aa
student-v0 acct reward: 0.369

student-v1 one_deal regression scorecard: results/yail-scorecard-student-v1-one-deal-regression-20260621.json
student-v1 one_deal job: 51b79002efeb4d52b7c242ba1d2136a7
student-v1 one_deal trace: 0b699289-8cd2-4713-a978-b466b6a3b485
student-v1 one_deal reward: 1.0
```

## Current blockers

1. Full QA `failure_analysis` exceeded model context on a GDPval trace.
2. Hosted trace-explorer still intermittently hits `Trace not bound to a Session`.
3. Custom student prompt/config routing into hosted `claude` is confirmed.
4. The first prompt patch did not show lift on medsec after the grader was fixed, but did improve acct. Promotion now needs QA review to confirm this is real improvement and not a grader artifact.
5. Hosted medsec grading currently reports `det_only:no_hud_api_key`, so LLM judge quality is not active in the observed score.

## Next command-level sequence

```text
1. Finish or rerun lightweight QA Evaluator reviews for the two GDPval failures.
2. Run QA Evaluator checks on acct v0/v1, medsec v0/v1, and one_deal v1 traces.
3. If QA passes, mark `student-v1` accepted for the deterministic course gate and run the broader graduation preset.
4. If QA flags a real issue, create a `student-v2` proposal if the issue is agent behavior, or an `env-v8`/task proposal if QA proves prompt-grader misalignment.
5. Rerun target plus held-out checks.
6. Record the final promotion decision.
```
