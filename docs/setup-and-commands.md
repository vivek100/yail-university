# Setup And Commands

## Install HUD docs skill

The HUD docs agent suggested:

```bash
npx skills add https://docs.hud.ai
```

This should install the HUD docs skill if the skill endpoint is supported by `npx skills`.

## Install HUD CLI

```bash
uv tool install hud-python --python 3.12
hud set HUD_API_KEY=your-key-here
```

Check:

```bash
hud version
hud models list
```

## Scaffold a new environment

```bash
hud init my-env
cd my-env
```

## Run local eval

```bash
hud eval tasks.py claude
```

Run all tasks:

```bash
hud eval tasks.py claude --full
```

Run one task slug:

```bash
hud eval tasks.py claude --task-ids count-r-strawberry
```

## Deploy environment

```bash
hud deploy .
```

Deployment builds and registers the environment image. It does not replace the need to sync task rows.

## Sync taskset

```bash
hud sync tasks blank tasks.py
```

Dry run:

```bash
hud sync tasks blank tasks.py --dry-run
```

## Run remotely

```bash
hud eval blank claude --remote --full
```

Start with a simple text-only task before a tool task:

```bash
hud eval blank claude --remote --task-ids count-r-strawberry -v
```

## Inspect failures

```bash
hud jobs
hud jobs <job-id>
hud trace <trace-id>
hud trace <trace-id> --json
```

## Notes from hud-blank deploy log

The line below is not a failure when followed by successful fallback:

```text
error: Unable to find lockfile at `uv.lock`, but `--frozen` was provided
```

`hud-blank` uses:

```bash
uv sync --frozen --no-dev || uv sync --no-dev
```

So missing `uv.lock` first fails the frozen command, then normal `uv sync` succeeds.

Healthy deploy evidence:

```text
Introspection OK over the v6 control channel: env 'blank', 2 tasks, 1 capabilities
POST_BUILD State: SUCCEEDED
```
