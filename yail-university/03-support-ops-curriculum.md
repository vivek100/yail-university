# 03 - Customer Support Ops Curriculum

This is the first YAIL University curriculum.

## Role

Customer Support Operations Worker.

The worker manages support-ticket workflows for small businesses. It must classify tickets, design workflow configs, debug broken routing, and communicate honestly with customers.

## Course 1 - Ticket Classification

Objective: map customer tickets to labels.

Inputs:

- ticket text,
- label taxonomy,
- short policy notes.

Grader:

- exact label accuracy,
- optional partial credit by class.

## Course 2 - Workflow Design

Objective: create a JSON routing workflow.

Inputs:

- customer request,
- required labels,
- schema,
- examples.

Grader:

- JSON schema validity,
- hidden ticket routing accuracy,
- no missing required labels.

## Course 3 - Workflow Debugging

Objective: diagnose and fix a broken workflow config.

Inputs:

- customer complaint,
- usage logs,
- current config,
- schema.

Grader:

- fixed config improves hidden ticket accuracy,
- no invalid schema,
- no no-op fixes.

## Course 4 - Customer Communication

Objective: send an honest customer reply after a fix.

Inputs:

- root cause evidence,
- company policy,
- customer message.

Grader:

- explains the real root cause,
- states what changed,
- professional tone,
- no impossible guarantees,
- no unsolicited compensation if policy says not to offer it.

## Course 5 - Integrated Account Save

Objective: combine diagnosis, fix, and reply in one task.

This maps to the HUD `save_the_account` capstone.

## Promotion Criteria

The agent advances when it meets a minimum score on held-out lessons, not just training lessons.

```text
classification accuracy >= target
workflow hidden accuracy >= target
customer reply passes policy judge
QA Evaluator Teacher finds no major task-gaming behavior
```
