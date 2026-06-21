# HUD Trace Explorer

Repo: `hud-evals/hud-trace-explorer`

This is a HUD environment for analyzing existing HUD traces. It is not the original benchmark. It is a second environment where a QA/debugger agent investigates a previous agent run.

## Big picture

```text
original agent runs benchmark task
  -> HUD records trace_id
  -> trace-explorer loads that trace
  -> QA agent inspects trace files
  -> QA agent returns structured verdict
  -> trace-explorer grades that verdict
```

## Main templates

- `analyze`: general trace question answering.
- `failure_analysis`: why did a low-reward or failed trace fail?
- `false_positive_analysis`: did the original agent get undeserved credit?
- `false_negative_analysis`: did the original agent succeed but get unfairly failed?
- `prompt_alignment_analysis`: did the original task prompt and grader match?
- `reward_hacking_analysis`: did the original agent game the reward?

## Important clarification

`prompt_alignment_analysis` checks the original task prompt and original grader, not the QA agent's own prompt.

It asks:

```text
Was the benchmark prompt fair relative to what the benchmark grader checked?
```

## What the QA agent can see

Trace explorer writes files into `/workspace`, such as:

```text
metadata.json
prompt.txt
trajectory.json
trajectory_summary.txt
file_changes.txt
evaluation_result.json
scenario_setup.json
scenario_code.py
environment_logs.txt
worker_logs.txt
screenshots_index.txt
screenshots/
task_codebase/
```

The QA agent usually sees tool call inputs/outputs and trace artifacts. It does not automatically see provider-hidden system prompts, secrets, or tool source code unless those were captured or available in the downloaded task source.

## Why ground truth matters

Without `ground_truth`, some templates are useful for ad hoc analysis but not for benchmarking.

For a benchmark, every row should include a label:

```python
reward_hacking_analysis(
    trace_id="...",
    hud_api_key=HUD_API_KEY,
    ground_truth=True,
)
```

For `failure_analysis`, ground truth is a pipe-separated set of acceptable labels:

```python
failure_analysis(
    trace_id="...",
    hud_api_key=HUD_API_KEY,
    ground_truth="agent_failure|implementation_bug|skipped_verification",
)
```

## How this fits the hackathon

First compare:

```text
HUD baseline QA agent vs our QA/debugger agent
```

on the same labeled trace taskset.

Then improve:

```text
trace QA prompts
structured output schema
ground-truth labels
verifier checks
grading rules
```

Only after the QA benchmark works should we train a small open model.
