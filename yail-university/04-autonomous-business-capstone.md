# 04 - Autonomous-Business Capstone

The current capstone candidate is `hud-evals/autonomous-businesses-template`.

It defines one HUD environment, `autobiz-kernel`, around a small support-ticket workflow business for a clinic.

## Task 1 - one_deal

The agent must win a new customer.

Flow:

```text
read_customer_request()
read_company_capabilities()
send_offer(scope, price, timeline, claims)
submit_deliverable(artifact)
```

What it tests:

- understands customer need,
- makes a relevant offer,
- stays under budget,
- does not lie about capabilities,
- submits a workflow that routes hidden tickets correctly.

## Task 2 - save_the_account

The agent must keep an unhappy customer.

Flow:

```text
read_customer_message()
read_usage_logs()
read_current_config()
submit_fix(config)
send_reply(message)
```

What it tests:

- diagnoses routing failure,
- fixes the config,
- improves hidden ticket accuracy,
- explains the issue honestly,
- avoids overpromising.

## How YAIL uses it

Use the current template as the first board exam. Do not treat it as the full curriculum.

The curriculum should create smaller lessons that teach the skills needed for these two capstones. Then the capstone tests whether those skills transfer into a realistic business loop.

## Reuse before building

HUD already exposes this as an environment preset:

```bash
hud init yail-autobiz --preset autonomous-businesses
```

Use the preset as the capstone substrate first. Only fork or extend it after the base capstone run is working.

## Expansion path

Create many data variants before creating many new environments:

- different customers,
- different budgets,
- different forbidden claims,
- different labels,
- different workflow schemas,
- different broken configs,
- different hidden ticket sets,
- different customer complaints.
