# HUD Concepts In Noob Terms

## Environment

The world the agent acts inside.

For a coding agent, this is usually:

```text
a workspace folder
source files
tests
shell access
maybe browser or MCP tools
```

Example: `hud-blank` is an environment with a calculator MCP capability and two tasks.

## Template

A reusable eval recipe written as Python code.

It says:

```text
what prompt to give the agent
what tools/world the agent can use
how to grade the result
```

In code:

```python
@env.template()
async def fix_bug(...):
    answer = yield "Fix the bug"
    yield 1.0 if tests_pass() else 0.0
```

## Task

One filled-in instance of a template.

If the template is:

```text
fix_bug(bug_name)
```

Then these are tasks:

```text
fix_bug("login-bug")
fix_bug("csv-parser-bug")
fix_bug("date-format-bug")
```

A task is more than just a prompt. It is:

```text
prompt + template arguments + setup + grading rule
```

## Taskset

A list of tasks. This is basically a benchmark.

Example:

```text
trace-debugging-qa-50
  - reward_hacking_analysis(trace_id=A, ground_truth=true)
  - false_positive_analysis(trace_id=B, ground_truth=false)
  - prompt_alignment_analysis(trace_id=C, ground_truth=true)
```

## Agent

The thing being evaluated.

Agent = model + loop + tools/harness.

Examples:

```text
Claude agent
OpenAI agent
Gemini agent
Qwen model served through OpenAI-compatible API
our trained QA/debugger model
```

## Trace / Run

The recording of one agent attempt.

It includes things like:

```text
prompt
agent messages
tool calls
tool outputs
screenshots
file changes
logs
final answer
reward
```

## Reward / Grader

The score returned by the task.

For a coding task:

```text
pytest passes -> 1.0
pytest fails -> 0.0
```

For trace QA:

```text
QA agent says reward_hacking=true
ground_truth=true
reward=1.0
```

## Group

Repeated rollouts of the same task.

HUD training needs groups because GRPO compares rollouts against other rollouts for the same task. If every rollout gets the same reward, training has no signal.
