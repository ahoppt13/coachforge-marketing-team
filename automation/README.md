# Phase 5 — Automation

Local scheduling for the CoachForge AI content pipeline. Each job runs `claude`
headlessly in this repo, under a **scoped permission allowlist**, on a `launchd`
schedule. Everything runs on your Mac — it reuses the local Metricool MCP and the
Notion connector your CLI is already logged into. The human approval gate is never
crossed: automation produces and reports, but only **you** move a row to `Approved`.

## Why local (not remote cloud routines)
The Metricool MCP is a **local stdio binary** (`~/.local/bin/mcp-metricool`).
Remote cloud agents can only use hosted URL connectors, so they can't run it — a
cloud Analyst would have no metrics. Hence everything here is local.

## The jobs

| Job | Schedule (Europe/London) | What it does | Publishes? |
|---|---|---|---|
| `analyst`   | Daily 07:00 | Pull metrics → Metrics & Trends; trends; competitors | no |
| `publisher` | Daily 07:30 | Create Metricool **drafts** from `Approved` rows → `Scheduled` (= drafted) | no — drafts only; you publish |
| `creative`  | Mon 06:30   | Strategist → Ideator → Scripter → Carousel slides → stop at Approval Queue | no |
| `reporting` | Sun 18:00   | Head of Content rolls up the week → Brief `Delivered` | no |

Each job = `prompts/<job>.txt` (the instruction) + `settings/<job>.settings.json`
(its allowlist) + `launchd/com.coachforge.<job>.plist` (its schedule), run via
`run-job.sh`. Logs land in `logs/<job>-<timestamp>.log` (`<job>-latest.log` points
at the newest). A macOS notification fires when each job finishes.

## The approval gate (now two)
- `creative` **stops at `Scripted`** (and renders carousel slides) — it never sets `Approved`.
- `publisher` **only touches `Approved`** rows and only ever creates **drafts**
  (`autoPublish: false`) — it never auto-publishes anything, including X.
- You review the Approval Queue in Notion and flip winners to `Approved` yourself
  (gate 1), then review the real composed post in Metricool and hit publish (gate 2).
- The `analyst`, `creative`, and `reporting` settings files **deny** the Metricool
  scheduler tools outright, so they physically cannot touch the scheduler.

## Install
```bash
cd /Users/aaronhopkins/coachforge-marketing-team/automation

./install.sh                  # analyst + creative + reporting (nothing publishes)
./install.sh --with-publisher # also enable the daily draft-builder (drafts only)
./install.sh --wake           # also set a 06:25 daily wake-from-sleep (sudo)
```
The **publisher is opt-in**. Leave it off until you've watched one draft run and
trust it; then re-run with `--with-publisher`. Even on, it only ever creates drafts.

## Run a job by hand (recommended first step)
Watch one run live before trusting the schedule:
```bash
./run-job.sh analyst      # safe: reads metrics, writes Metrics & Trends
tail -f logs/analyst-latest.log
```
`publisher` creates Metricool drafts for Approved rows (never publishes) — but only run it when ready.

## Sleep / power
- A **sleeping** Mac can run these if it wakes for them. A **powered-off** Mac can't.
- `./install.sh --wake` sets a daily 06:25 wake (covers the morning jobs). `pmset`
  only holds one repeating wake, so the **Sun 18:00** roll-up needs the Mac awake
  then (or run `reporting` by hand). Keep the Mac plugged in.
- Check/clear: `pmset -g sched` · `sudo pmset repeat cancel`.

## Manage
```bash
launchctl list | grep coachforge        # what's loaded
./uninstall.sh                           # remove all jobs
launchctl start com.coachforge.analyst   # fire one now
```

## Health checks
- `claude mcp list` — Metricool and `claude.ai Notion` must both show **Connected**.
  If Notion says *Needs authentication*, re-auth (the connector's OAuth lapsed) or
  the Notion jobs will fail.
- If a job logs `NONE`/permission denials, the tool isn't in that job's
  `settings/<job>.settings.json` allowlist — add it there.
