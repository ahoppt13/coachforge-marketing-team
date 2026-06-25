# CoachForge AI — Content Engine Runbook

Operational guide for running the agent-based marketing team. Paste-ready kickoff
prompts for each agent, plus how to manage sessions.

---

## The team

| # | Agent | Skill | Job |
|---|---|---|---|
| 1 | Data Analyst | `data-analyst` | Pull daily metrics (IG/FB/TikTok/YouTube) via Metricool + trends via socialtrendscrape → Metrics & Trends; flag Repeat/Iterate/Kill/Watch |
| 2 | Content Strategist | `content-strategist` | Read the data → set weekly content mix, CTAs, pillar focus → draft Weekly Brief |
| 3 | Ideator | `ideator` | 30+ ideas → lock 7 → Content Calendar (Status=Idea) |
| 4 | Scripter | `scripter` | Filming-ready scripts → Scripts DB → move posts to Scripted (your Approval Queue) |
| 5 | Publishing Manager | `publishing-manager` | Schedule **Approved** posts via Metricool → Scheduled → Published |
| 6 | Head of Content | `head-of-content` | Roll the week's results into the Weekly Brief: Top Performer + Kill List → Delivered; move reported posts to Reported |

## Weekly run order

```
run the analyst → Strategist → Ideator → Scripter
        → YOU review the Approval Queue in Notion, move winners to "Approved"
        → Publishing Manager schedules the Approved posts
```

**The human gate:** nothing moves past `Approved` without you. That status change is yours alone.

---

## Setup facts (already done)

- Project dir: `/Users/aaronhopkins/coachforge-marketing-team`
- Metricool MCP server: installed, **user scope**, tools = `mcp__mcp-metricool__*`
- Metricool brand `coachforge.ai`, blogId **6446373**. Connected: Instagram, Facebook, TikTok, YouTube. **X = not connected (trend-only).**
- Secrets in `config/.env` (gitignored). Server creds live in `~/.claude.json` (not in repo).
- Winner bars: **own posts** judged vs your own recent baseline; **external** content uses 10k views + 1k likes.

---

## Session management

- Every Claude Code conversation auto-saves. You won't lose a chat by opening another.
- **New session:** open a new terminal window/tab → `cd /Users/aaronhopkins/coachforge-marketing-team` → `claude`. Launching from the project folder auto-loads the skills and Metricool tools.
- **Resume a past chat:** from that folder, `claude --resume` (pick from list) or `claude --continue` (most recent).
- Run all CoachForge work from the project folder so the Metricool tools + skills are present.

---

## Kickoff prompts

### 1 — Data Analyst (daily)

```
Work in /Users/aaronhopkins/coachforge-marketing-team. Run the Data Analyst.

1. Read .claude/skills/data-analyst/SKILL.md and follow it exactly.
2. Also read config/notion-workspace.md and brand/brand-voice-profile.md.

Then do the pull:
- Metricool blogId = 6446373. Connected: Instagram, Facebook, TikTok, YouTube.
  X is NOT connected (trend-only).
- Use mcp__mcp-metricool__* to pull the last 7 days of posts per connected
  platform (dates YYYY-MM-DD).
- Winner bars: judge MY posts vs my own recent baseline (Repeat/Iterate/Kill/
  Watch). Use 10k views + 1k likes only for external trend/competitor content.
- Write each notable post into the "Metrics & Trends" DB (Type=Post metric,
  Source=Metricool, with Verdict). Refresh "Competitors".
- Never invent numbers. If a source is empty, say so.
- Finish with a readout: top performers, kill list, trends to ride, competitor
  moves, data gaps.
```

### 2 — Content Strategist (start of week)

```
Work in /Users/aaronhopkins/coachforge-marketing-team. Run the Content Strategist.

Read .claude/skills/content-strategist/SKILL.md and follow it exactly. Also read
config/notion-workspace.md and brand/brand-voice-profile.md.

Task:
- Read the last 7-14 days of "Metrics & Trends" + "Competitors" (What's Working).
- Set this week's content mix. Default = 7 posts/week, Instagram-first:
  3 Reels, 2 Carousels, 1 Long-form video, 1 Thread (X). Adjust toward what the
  data shows working, and say why.
- Assign pillar focus across the 5 brand pillars. Pick 2-3 CTAs (UK English, £,
  NO FOMO/scarcity). Pick trends to ride (brand-fit only).
- Output: create ONE row in "Weekly Brief" (Status=Draft) with Trends to Ride +
  Next Week Focus, and a structured strategy in the page body.
- If data is sparse, say so and reason from brand pillars. Never invent numbers.
```

### 3 — Ideator

```
Work in /Users/aaronhopkins/coachforge-marketing-team. Run the Ideator.

Read .claude/skills/ideator/SKILL.md and follow it exactly. Also read
config/notion-workspace.md and brand/brand-voice-profile.md.

Task:
- Read the latest Status=Draft row in "Weekly Brief". Follow its content mix,
  pillar focus, CTAs, and trends. (If none exists, tell me to run the Content
  Strategist first — don't guess.)
- Brainstorm 30+ topic ideas mapped to the 5 pillars. Turn each trend into 2-3
  CoachForge-specific angles.
- Cut to the 7 best, matching the brief's format mix. Draft a strong hook line
  for each (Register 1, specific, no banned words).
- Output: create 7 rows in "Content Calendar" (Status=Idea) with Title, Format,
  Platform, Pillar, Hook, Publish Date (spread across the week), Notes (angle +
  CTA), related to this week's Weekly Brief.
- Keep the full 30+ list in your reply.
```

### 4 — Scripter

```
Work in /Users/aaronhopkins/coachforge-marketing-team. Run the Scripter.

Read .claude/skills/scripter/SKILL.md AND brand/brand-voice-profile.md IN FULL.
Also read config/notion-workspace.md.

Task:
- Take every Status=Idea row in "Content Calendar" (or the ones I name).
- For each, write a full filming-ready script in the correct register (R1 for
  feed/Reels/hooks; R2 only for teaching content), opening with one of the
  proven hook formats in the skill.
- Output per idea: create a "Scripts" row (Script Status=Draft, full script in
  page body, Hook Line, Word Count, Format, Drafted date, related to its Calendar
  item), then move that Calendar row to Status=Scripted.
- Self-check every script: reject if it has banned words, FOMO, US English/$,
  fake intimacy, adjective stacks, or positions AI as replacing the coach.
- STOP at Scripted. Nothing goes past Approved without me. List the Approval Queue.
```

### 5 — Publishing Manager (Phase 3 — build, then run)

```
Work in /Users/aaronhopkins/coachforge-marketing-team. Build Phase 3: the
Publishing Manager.

Read config/notion-workspace.md, .claude/skills/data-analyst/SKILL.md (for house
style), and brand/brand-voice-profile.md.

Build .claude/skills/publishing-manager/SKILL.md. It must:
- Take ONLY "Content Calendar" rows with Status=Approved (human gate).
- Schedule each to its Platform(s) at its Publish Date via the Metricool
  scheduler tools (mcp__mcp-metricool__* ; /v2/scheduler/posts). blogId = 6446373.
- After scheduling set Status=Scheduled; once live set Published + fill Live Link.
- DM-funnel auditing stays a manual weekly checklist (DM data is locked down).
- Never publish to X (not connected).
Then dry-run the scheduler (don't publish live without my OK) and commit the skill.
```

### 6 — Head of Content (end of week)

```
Work in /Users/aaronhopkins/coachforge-marketing-team. Run the Head of Content.

Read .claude/skills/head-of-content/SKILL.md and follow it exactly. Also read
config/notion-workspace.md and brand/brand-voice-profile.md.

Task:
- Find THIS week's "Weekly Brief" row (the one the Strategist opened as Draft).
  Complete that same row — do not create a new one.
- Read this week's "Metrics & Trends" (Type=Post metric + Verdict) and the
  "Content Calendar" rows that reached Status=Published this week.
- Pick the Top Performer (post + proof number + reusable lesson) and build the
  Kill List (underperformers + reason + drop/retry). No standout? Say so.
- Fill Top Performer + Kill List, relate the week's posts via Related Content,
  put a scannable results readout in the page body, set Status=Delivered.
- Move each reported Content Calendar row Published -> Reported.
- Never invent a metric or a winner. Thin data = report thin data.
- Finish with the verdict, top performer, kill list, what feeds next week, gaps.
```

---

## Phase 5 — Automation (built)

Local `launchd` jobs run the pipeline on a schedule — see [`automation/README.md`](automation/README.md).
Everything is local (the Metricool MCP is a local binary, so cloud routines can't run it).

| Job | When (Europe/London) | Publishes? |
|---|---|---|
| `analyst`   | Daily 07:00 | no |
| `publisher` | Daily 07:30 | yes — **Approved only**, opt-in |
| `creative`  | Mon 06:30   | no — stops at Approval Queue |
| `reporting` | Sun 18:00   | no |

```bash
cd automation
./install.sh                  # analyst + creative + reporting (nothing publishes)
./install.sh --with-publisher # also enable real scheduling of Approved rows
./run-job.sh analyst          # run one by hand; tail logs/analyst-latest.log
```

The approval gate holds: `creative` stops at `Scripted`, `publisher` only touches
`Approved` rows and never posts to X, and the non-publishing jobs are denied the
Metricool scheduler tools outright. You alone move a row to `Approved`.

## What's left

- **Optional:** wake-from-sleep tuning for the Sun 18:00 roll-up (pmset holds one
  repeating wake; see automation/README.md), and your first supervised
  `--with-publisher` run before trusting unattended scheduling.
