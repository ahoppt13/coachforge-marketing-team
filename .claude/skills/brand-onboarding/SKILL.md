---
name: brand-onboarding
description: Onboard a NEW brand into the CoachForge marketing pipeline from a brand voice + brand guidelines + a connected Metricool brand, then run the same weekly content build that CoachForge uses. Creates a per-brand brands/<slug>/ config folder, a custom carousel theme, fresh per-brand Notion databases (Content Calendar + Scripts + Metrics & Trends), and produces a week of posts as scripts → rendered carousels → Metricool drafts. Use when Aaron says "onboard <brand>", "set up a new brand", "add a brand", or "run a week for <brand>".
---

# Brand Onboarding — CoachForge Pipeline (multi-brand)

You take everything we built for CoachForge AI and make it repeatable for *another* brand. The owner gives you three things: a **brand voice**, **brand guidelines**, and a **brand already set up in Metricool**. You turn that into a self-contained `brands/<slug>/` folder, stand up that brand's own Notion databases, design its own carousel look, and then run the weekly build exactly as we do for CoachForge.

This skill has **two modes**:
- **Onboard** — one-time setup for a brand that has no `brands/<slug>/` folder yet.
- **Weekly run** — the recurring build for a brand that's already onboarded.

Always check first: does `brands/<slug>/` already exist? If no → Onboard, then offer the first Weekly run. If yes → Weekly run.

## The non-negotiables (inherited from the whole pipeline)
These carry over to every brand, unchanged:
- **Two human gates.** (1) Aaron flips a Content Calendar row to `Status = Approved` in Notion — only Aaron, never you. (2) Aaron publishes from Metricool. You only ever produce **drafts**.
- **Drafts only in unattended runs.** Every Metricool post you create sets `autoPublish: false` + `draft: true`. Never create a post that auto-publishes. The one exception that exists for CoachForge — X auto-fire — is **opt-in per brand** and only on Aaron's explicit say-so (see brand.md `Auto-fire networks`); default is draft.
- **Metricool does NOT auto-post Instagram or TikTok** — manual publish every time, on every brand. Never tell the owner a post "will go out automatically" for IG/TikTok.
- **Never fabricate** a media URL, a scheduled time, a Live Link, a follower count, or a metric. Missing data → flag it, don't fill it.
- **Per-brand isolation.** A brand's voice, hashtags, theme, pillars, Notion DBs, and Metricool blog_id all live under that brand. Never let one brand's config bleed into another's run. Read the *target brand's* files each run; don't assume CoachForge defaults.

## What you read before any run
For the **target brand** (not CoachForge):
1. `brands/<slug>/brand.md` — IDs, Metricool blog_id/networks/timezone, Notion DB ids.
2. `brands/<slug>/brand-voice-profile.md` — the voice every draft must obey.
3. `brands/<slug>/hashtag-bank.md` — the 5-per-post tag set.
4. `brands/<slug>/pillars.md` — the content pillars.
5. `brands/<slug>/theme.json` — the carousel visual theme.

Reference (shared, read-only patterns): `config/notion-workspace.md` (the CoachForge schema you mirror), `.claude/skills/publishing-manager/SKILL.md` (the draft-mode publishing rules).

---

## MODE 1 — ONBOARD a new brand

### Step 0 — Gather the inputs
You need, from Aaron:
- The brand's **voice** (a doc, paste, or link) and **brand guidelines** (positioning, tone, colours, fonts, imagery rules).
- The **Metricool brand** must already exist and be connected. You'll confirm it with `get_brands`.
- A **slug** (lowercase, no spaces — e.g. `acme-coaching`). Derive one and confirm it.

If any of the three is missing, stop and ask. Do not invent a brand voice.

### Step 1 — Scaffold the brand folder
Copy the template into the new brand:
```
brands/<slug>/
  brand.md
  brand-voice-profile.md
  hashtag-bank.md
  pillars.md
  theme.json
  carousel/            (specs go here; rendered PNGs in carousel/out/<spec>/)
```
Start from `brands/_template/` and fill every placeholder from the supplied voice + guidelines. **Translate, don't copy** — none of CoachForge's specifics (obsidian/amber, "forge", coaching niche) may survive unless the new brand genuinely shares them.

- `brand-voice-profile.md` — port the source voice into the 10-section shape. Capture the banned-words list and hard reject rules explicitly; those are what keep drafts on-brand.
- `pillars.md` — 4–6 pillars. These become the Notion `Pillar` select options; keep them identical in both places.
- `hashtag-bank.md` — brand tag + niche set + one pillar tag per pillar.
- `theme.json` — see Step 2.
- `brand.md` — fill Identity + Metricool from `get_brands`; leave the Notion IDs blank until Step 3 creates them.

### Step 2 — Design the carousel theme (custom layout per brand)
The renderer `carousel/render.py` is theme-driven. Build `brands/<slug>/theme.json` from the brand's visual guidelines. Keys (all optional; anything omitted falls back to the CoachForge default):
- `bg`, `card`, `border`, `accent`, `accent_hover`, `text`, `muted` — hex colours straight from the guidelines.
- `font_import` — a Google Fonts `@import` line for the brand's display + body fonts.
- `display` — font stack for headlines / brand moments. `body` — font stack for everything else.
- `brandmark_html` — the wordmark for the cover slide; wrap the accent-coloured part in `<b>…</b>` (e.g. `"Acme<b>Coaching</b>"`).
- `card_border` — `true`/`false` for the inset rounded frame.
- `accent_shape` — `"square"` or `"round"` (bullet markers + CTA chip corners).

**Contrast check (do not skip):** the layout puts `text` and `accent` on `bg`/`card`. If the brand's palette is light, set `bg`/`card` light and `text` dark — don't leave CoachForge's dark defaults under a light accent or the slides will be unreadable. After writing the theme, render a one-off test spec and **look at the PNG** before continuing:
```
python3 carousel/render.py --spec brands/<slug>/carousel/_themecheck.json \
  --out brands/<slug>/carousel/out/_themecheck --theme brands/<slug>/theme.json
```
(Use a 3-slide cover/content/cta spec as `_themecheck.json`.) Read the rendered PNGs, confirm legibility and that it looks like the brand, adjust the theme, re-render. Only proceed when it looks right.

### Step 3 — Stand up the brand's Notion databases (new Notion per brand)
Each brand gets its **own** Calendar + Scripts + Metrics databases so brands never share a pipeline. Mirror the CoachForge schemas in `config/notion-workspace.md` exactly — same property names, types, and status flow — with two brand-specific differences:
- The **Pillar** select options come from this brand's `pillars.md`, not CoachForge's.
- The **Platform** multi-select options = the brand's connected Metricool networks.

Do this:
1. Pick/create a **hub page** for the brand (ask Aaron where it should live, or create a top-level page named "`<Brand> — Content Engine`").
2. Create the three databases under that hub (use the Notion create-database tool). Property-for-property copies of:
   - **Content Calendar** — Title, Status (Idea·Scripted·Approved·Scheduled·Published·Reported), Format (Carousel·Reel / Short·Static·Story·Long-form video·Thread), Platform (multi-select = brand networks), Pillar (select = brand pillars), Hook (text), Publish Date (date), Owner (person), Live Link (url), Notes (text), Script (relation → Scripts), Metrics (relation → Metrics & Trends).
   - **Scripts** — Script Title, Format (Reel / Short·Carousel·Long-form video·Thread — note: **no "Static"**), Hook Line (text), Script Status (Draft·Needs edit·Approved·Filmed), Word Count (number), Content Item (relation → Calendar), Drafted (date). Full script goes in the page body, not a property.
   - **Metrics & Trends** — Entry, Type (Post metric·Trend signal), Platform (multi-select), Date Logged (date), Reach/Engagements/Saves/Shares/Link Clicks (number), Source (Metricool·socialtrendscrape·Manual), Verdict (Repeat·Iterate·Kill·Watch), Trend Note (text), Content Item (relation → Calendar).
3. Wire the relations (Calendar ↔ Scripts, Calendar ↔ Metrics).
4. **Write the new IDs back into `brands/<slug>/brand.md`** (Database IDs + `collection://` data-source IDs + hub page id). These are how every later run finds the brand's databases. If a create call doesn't return an ID, stop and flag — never guess one.

### Step 4 — Confirm Metricool
Call `get_brands`, find the brand, record its `blog_id`, `timezone`, and the exact `networks` list into `brand.md`. If a network the owner expects isn't connected, note it as not-connected — never schedule a network Metricool doesn't list.

### Step 5 — Onboarding summary
Report: the folder created, the theme (with the test PNG path), the three Notion DB IDs, the Metricool blog_id + connected networks, and what's still needed from Aaron (e.g. confirm pillars, approve the look). Then offer to run the first week.

---

## MODE 2 — WEEKLY RUN (already-onboarded brand)

This is the same flow we ran for CoachForge, pointed at the brand's own files and databases. Default shape: **7 posts (daily), 2 of 7 with video, the rest carousels** — but confirm the count/mix with Aaron if he hasn't said.

1. **Plan the week.** Using the brand's `pillars.md` + `brand-voice-profile.md`, draft 7 angles spread across pillars. Each gets: Title, Pillar, Format, Platform(s), Hook, and a one-line Notes brief. Two are video (Reel / Short), the rest Carousel (adjust per Aaron).
2. **Write scripts** in the brand voice (Register per the voice profile). Carousel posts get a slide spec (cover / content×N / cta) saved to `brands/<slug>/carousel/<spec-slug>.json` with the brand `handle`. Video posts get a filming script.
3. **Render carousels** with the brand theme:
   ```
   python3 carousel/render.py --spec brands/<slug>/carousel/<spec>.json \
     --out brands/<slug>/carousel/out/<spec-slug> --theme brands/<slug>/theme.json
   ```
   Slides land as `slide-NN.png`. (The renderer also accepts a `"theme"` key inside the spec, but passing `--theme` is explicit and preferred.)
4. **Create Notion rows.** In the brand's Content Calendar: one row per post (Status `Scripted`), with Title/Pillar/Format/Platform/Hook/Publish Date/Notes. Create the linked Scripts row (Script Title, Format, Hook Line, Word Count, Content Item → the Calendar row, Drafted) and put the full script in the Scripts page body. Link them. **Stop at `Scripted`** — that's the Approval Queue. Never set `Approved` yourself.
5. **Hand to the publisher.** Once Aaron approves rows (`Approved`), the **publishing-manager** skill stages them as Metricool drafts against this brand's `blog_id`. Carousels: the draft carries caption + first 5 hashtags; the slide PNGs (give the `brands/<slug>/carousel/out/<spec>/` paths) get attached in the Metricool composer at review. Video: caption + flag to attach the video. Follow publishing-manager's rules verbatim — drafts only, X ≤280, skip unconnected networks, advance Approved→Scheduled only for what actually drafted.
6. **Run summary** in the publishing-manager format: drafted / attach-at-review / skipped X / blocked / Notion status changes / needs-Aaron.

> In a weekly run you produce drafts up to the Approval Queue (`Scripted`). Pushing to Metricool happens **after** Aaron approves — either Aaron triggers the publisher, or, if he's pre-approved, the publisher runs on `Approved` rows only.

---

## Hard rules (read every run)
- **Onboard vs run:** if `brands/<slug>/` is missing, you must onboard before running. Never run a week for a brand with no config folder.
- **Read the target brand's files** — voice, hashtags, pillars, theme, brand.md — every run. Never apply CoachForge's voice/theme to another brand.
- **New Notion per brand:** each brand uses its own Calendar/Scripts/Metrics DBs. Never write another brand's content into CoachForge's databases (data source `3c329f63-…`) or vice-versa.
- **Custom theme per brand:** always pass `--theme brands/<slug>/theme.json`. Look at a rendered PNG before trusting a new/changed theme — contrast bugs are invisible in JSON.
- **Stop at the gate.** Scripter work ends at `Scripted`. Only Aaron sets `Approved`. Only the publisher acts on `Approved`, and only as drafts.
- **Never fabricate** IDs, URLs, times, or metrics. A blank field that's flagged beats a confident guess.
- Write any newly created Notion IDs back into `brands/<slug>/brand.md` immediately, so the next run can find them.
