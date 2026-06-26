# <BRAND NAME> — Brand Config

> The machine-readable config card for this brand. The brand-onboarding and
> publishing-manager skills read this before any run. Fill every field. Do not
> invent IDs — leave a field blank and flag it rather than guess.

## Identity
- **Slug:** `<slug>`  (folder name, lowercase, no spaces)
- **Handle:** `@<handle>`  (the social @, used as the carousel footer handle)
- **One-line identity:** <what they do, for whom>

## Metricool
- **Brand name in Metricool:** `<exact brand name>`
- **blog_id:** `<number>`  (from `get_brands`)
- **Timezone:** `<e.g. Europe/London>`
- **Connected networks:** `<e.g. Instagram, TikTok, X>`  (only what `get_brands` actually returns)
- **Auto-fire networks:** `<usually X only — IG/TikTok are manual-publish on this account>`

## Notion databases (filled in by onboarding once created)
- **Content Calendar** — Database ID: `<id>` · Data source: `collection://<id>`
- **Scripts** — Database ID: `<id>` · Data source: `collection://<id>`
- **Metrics & Trends** — Database ID: `<id>` · Data source: `collection://<id>`
- **Hub page:** `<page id>`

> Calendar / Scripts / Metrics schemas mirror the CoachForge originals
> (see `config/notion-workspace.md`) unless noted below.

## Carousel
- **Theme file:** `brands/<slug>/theme.json`
- **Spec folder:** `brands/<slug>/carousel/`  · rendered PNGs in `brands/<slug>/carousel/out/<spec-slug>/`
- Render with: `python3 carousel/render.py --spec brands/<slug>/carousel/<spec>.json --out brands/<slug>/carousel/out/<spec-slug> --theme brands/<slug>/theme.json`

## Files in this folder
- `brand.md` — this config card
- `brand-voice-profile.md` — the voice rules every writing step obeys
- `hashtag-bank.md` — the 5-per-post tag set
- `pillars.md` — content pillars (also become the Calendar `Pillar` select options)
- `theme.json` — carousel visual theme for `render.py --theme`
