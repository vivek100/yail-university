# 02 - School Levels

The curriculum levels describe how an agent improves. They are not all model-training stages.

## Certificate

The base agent passes simple role lessons with its existing model.

Example:

```text
Given five support tickets, classify each as billing, login, bug, or other.
```

## Diploma

The agent improves through role prompts, tool instructions, workflow scaffolding, examples, QA Evaluator feedback, and Improvement Teacher patches.

This is the first hackathon target. It is cheap and fast because no model weights change.

## Degree

The agent gets SFT on audited curriculum traces:

- successful student traces,
- failed traces with corrected teacher feedback,
- high-quality teacher reviews,
- task-design reviews.

## Residency

The agent is trained with RL/RFT on HUD rewards in interactive environments.

This should happen only after the curriculum produces reliable reward spread and the graders are not easy to game.

## Board Exam

The agent is evaluated on held-out autonomous-business tasks it never saw during curriculum construction or training.

Passing the board exam means the worker is ready for a simulated business deployment.

## Graduation Gates

Every level needs a test. The agent does not graduate because the QA Evaluator wrote useful feedback or the Improvement Teacher made a patch; it graduates because the accepted version passes held-out HUD tasks after the improvement loop.

Each gate should include:

- held-out lessons,
- minimum score,
- QA Evaluator verdict,
- Improvement Teacher change proposal,
- regression check against the base agent,
- capstone score when applicable.

Example:

```text
Diploma: prompt/tool/workflow-updated agent must beat the base agent on held-out support-ops lessons.
Degree: SFT agent must beat the diploma agent on held-out lessons.
Residency: RL agent must improve reward on held-out interactive tasks without reward hacking.
Board exam: worker must clear the autonomous-business capstone threshold.
```
