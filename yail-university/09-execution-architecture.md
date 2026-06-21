# 09 - Execution Architecture

YAIL runs should happen on HUD, not as local-only experiments. Local runs are allowed for smoke tests, but real scorecards should use HUD-hosted tasks, HUD model gateway models, and HUD traces.

## First model split

Use this initial split:

```text
student worker: claude-haiku-4-5
QA Evaluator Teacher: claude-sonnet-4-5
Improvement Teacher: claude-sonnet-4-5 or stronger coding agent
```

Rationale:

- Haiku 4.5 is fast enough for repeated student attempts.
- Sonnet 4.5 is already used by the trace QA verifier subagent and is strong enough for trace review.
- The Improvement Teacher needs code-editing and systems judgment; it should start as Sonnet 4.5 / coding-agent backed, then later become trainable if the loop produces enough data.

Later student comparisons:

```text
gpt-5.4-mini
gemini-3.5-flash
Qwen/Qwen3.5-4B
Qwen/Qwen3-8B
```

## Run shape

Every YAIL scored run has three layers:

```text
1. Student task run
   - run claude-haiku-4-5 on GDPval or autonomous-business task
   - collect reward, trace_id, task metadata

2. QA Evaluator Teacher trace review
   - run trace-explorer on the student trace_id
   - use claude-sonnet-4-5 as the QA agent
   - collect QA verdicts for failure, false positives, false negatives,
     prompt/grader alignment, and reward hacking

3. Improvement Teacher versioning
   - consume scorecard, QA verdicts, trace artifacts, and repo files
   - propose or apply a bounded patch to agent config, env, tools, tasks, or files
   - create a new explicit version
   - rerun target and held-out checks
```

The graduation scorecard combines both:

```text
task_reward + trace_id + QA verdicts + improvement proposal + promotion decision
```

## Existing QA environment

Use `hud-evals/hud-trace-explorer` as the QA Evaluator Teacher environment.

Current useful templates:

```text
failure_analysis
false_positive_analysis
false_negative_analysis
prompt_alignment_analysis
reward_hacking_analysis
```

The QA environment loads a previous HUD trace and writes trace artifacts into the QA workspace:

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
screenshots/
task_codebase/
```

## v6 compatibility work

The current trace explorer repo uses older scenario-style HUD APIs. YAIL should either:

1. reuse the deployed trace-explorer if it works on HUD today, or
2. upgrade/wrap the trace QA evaluator to v6 before depending on it for the final demo.

Do not reimplement trace ingestion unless the existing environment blocks us.

## Hosted execution target

Real runs should follow this shape:

```bash
hud deploy
hud sync tasks <taskset_name>
hud eval <taskset_name> claude --model claude-haiku-4-5 --remote
```

Then run trace QA against the resulting trace IDs with:

```text
trace-explorer + claude-sonnet-4-5
```

Then run the Improvement Teacher:

```text
scorecard + QA findings + selected trace artifacts + repo files
  -> versioned patch
  -> deploy/sync if needed
  -> rerun graduation preset
```

The exact orchestration can be CLI-first or Python-first, but the output should be the same: a scorecard with student reward, QA Evaluator review, improvement proposal, and promotion decision for every task.
