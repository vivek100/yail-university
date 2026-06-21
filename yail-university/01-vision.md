# 01 - Vision

YAIL University is an agent school. It turns professional work into structured curricula, then uses HUD environments to grade whether agents can actually perform that work.

The project should stay focused on one claim:

> We can make role-specific AI workers improve through curriculum, QA evaluation, and agent-generated improvements before doing expensive model training.

## What this is

- A curriculum generator for AI workers.
- A training and evaluation process built on HUD tasks, traces, and rewards.
- A QA Evaluator Teacher that reviews both student behavior and task quality.
- An Improvement Teacher that creates the next version of the agent, environment, tools, tasks, or files.
- A path from versioned prompt/tool/environment improvement to SFT and eventually RL.

## What this is not

- Not a generic coding-agent benchmark.
- Not a claim that GDPval alone is enough to train an employee.
- Not a claim that RL is the first milestone.
- Not a general company simulator on day one.

## Why GDPval

GDPval gives realistic professional task shapes: deliverables, occupations, rubrics, and supporting files. We use it as curriculum inspiration and task-source material.

HUD provides the executable layer: environments, tools, rewards, traces, and held-out capstones.
