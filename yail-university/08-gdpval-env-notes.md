# 08 - GDPval Environment Notes

## Local presets

Materialized HUD presets:

```text
trainingPlan/hud-hackathon/repos/yail-gdpval
trainingPlan/hud-hackathon/repos/yail-autobiz
```

Commands used:

```bash
hud init yail-gdpval --preset gdpval
hud init yail-autobiz --preset autonomous-businesses
```

## GDPval preset shape

The GDPval preset is a HUD environment for knowledge-work deliverables.

It stages reference files into the agent workspace, asks the agent to create a native deliverable, then grades the deliverable with task-local deterministic checks plus HUD-native LLM judging.

Current included tasks:

```text
acct-afc-audit-sampling
medsec-pathology-forms
```

### acct-afc-audit-sampling

Occupation:

```text
Accountants and Auditors
```

Deliverable:

```text
deliverable/Sample.xlsx
```

What the agent must do:

- read `Population v2.xlsx`,
- document sample-size calculation,
- compute quarter-on-quarter variance,
- select a risk-based audit sample,
- preserve traceable row identifiers.

Grading:

- parseable `.xlsx`,
- sample-size tab exists,
- variance appears,
- selected rows meet risk criteria,
- sample is not the whole population,
- coverage across divisions/countries,
- LLM judge for professional quality.

YAIL fit:

```text
Business analyst / audit analyst coursework.
Not directly support-ops, but useful for general office-work curriculum and scorecard examples.
```

### medsec-pathology-forms

Occupation:

```text
Medical Secretaries and Administrative Assistants
```

Deliverable:

```text
deliverable/pathology_bulk_forms.xlsx
```

What the agent must do:

- read a bulk pathology-order workbook,
- split patient rows into one sheet per lab,
- preserve required patient fields,
- add lab/month headers,
- avoid mixing or dropping patients.

Grading:

- parseable `.xlsx`,
- one sheet per lab,
- required columns present,
- patient routing F1,
- LLM judge for format/professional quality.

YAIL fit:

```text
Strong first "school" task for an operations worker.
It is close to ticket-routing logic: classify records, split work by destination, preserve required fields, and produce a professional spreadsheet.
```

## Autonomous-business preset shape

The autonomous-business preset is an interactive business capstone, not a knowledge-work deliverable task.

Current tasks:

```text
one_deal
save_the_account
```

`one_deal` tests truthful selling plus verified workflow delivery.

`save_the_account` tests diagnosis, config repair, and honest customer communication.

Verification status:

```text
uv run pytest tests/ -q
27 passed
```

## How to use both in YAIL

Use GDPval as the course layer and autonomous-business as the capstone layer.

```text
GDPval-style school:
  medsec-pathology-forms
    -> record routing / spreadsheet operations
  acct-afc-audit-sampling
    -> audit judgment / evidence-grounded deliverables

Autonomous-business board exam:
  one_deal
    -> honest commercial action + workflow delivery
  save_the_account
    -> operational diagnosis + fix + customer reply
```

## Graduation test implication

The school needs held-out tests at two levels:

1. GDPval/course level: did the agent create correct professional deliverables?
2. Business/capstone level: did the agent use tools to create verified business value?

This means a YAIL worker should not graduate based only on GDPval deliverables. It should also pass an interactive business capstone.

## Immediate next build

Create a thin YAIL runner that can:

```text
1. run a base agent on selected GDPval course tasks,
2. record scores and trace ids,
3. run the base agent on autonomous-business capstones,
4. produce a graduation scorecard,
5. later insert QA Evaluator review and Improvement Teacher versioning between attempts.
```

Do not build new environments yet. Reuse the presets first.

Scaffold added:

```bash
python trainingPlan/hud-hackathon/experiments/yail_scorecard_runner.py --json
python trainingPlan/hud-hackathon/experiments/yail_scorecard_runner.py
python trainingPlan/hud-hackathon/experiments/yail_scorecard_runner.py --run
```

The runner is dry-run first and only loads `env.local` when `--run` is used.
