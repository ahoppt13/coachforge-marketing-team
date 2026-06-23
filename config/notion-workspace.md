# Notion Workspace Map — CoachForge AI Content Engine

Single source of truth for all database IDs, data-source IDs, and field schemas.
Every agent reads this before writing to Notion. Do not invent property names — use the exact names below.

**Hub page:** CoachForge AI — Content Engine → `3884adb2-1fc0-81fd-a595-f3c2e1b6a5a4`

---

## Content Calendar  (the spine)
- Database ID: `8582fb56-2238-4f14-998c-df8e81a74f97`
- Data source: `collection://3c329f63-8130-40c0-8b19-39afecee87ef`

| Property | Type | Options |
|---|---|---|
| Title | title | — |
| Status | select | Idea · Scripted · Approved · Scheduled · Published · Reported |
| Format | select | Carousel · Reel / Short · Static · Story · Long-form video · Thread |
| Platform | multi-select | Instagram · TikTok · YouTube · X · Facebook |
| Pillar | select | Prompt shortcuts · Busywork agitation · Behind-the-scenes · Content teardowns · Business receipts |
| Hook | text | the scroll-stopping first line |
| Publish Date | date | — |
| Owner | person | — |
| Live Link | url | filled after publishing |
| Notes | text | the angle / brief |
| Script | relation → Scripts | — |
| Metrics | relation → Metrics & Trends | — |
| Inspired By | relation → Competitors | — |
| Weekly Brief | relation → Weekly Brief | — |

**Status flow & ownership:**
`Idea` (Ideator) → `Scripted` (Scripter) → **`Approved` (HUMAN GATE — Aaron only)** → `Scheduled` (Publishing Mgr) → `Published` (Publishing Mgr) → `Reported` (Head of Content)

---

## Scripts
- Database ID: `7306e0f0-b068-4293-93e9-2a2fe8ba7097`
- Data source: `collection://de243793-a04c-4980-bcdf-660cad5db6db`

| Property | Type | Options |
|---|---|---|
| Script Title | title | — |
| Format | select | Reel / Short · Carousel · Long-form video · Thread |
| Hook Line | text | — |
| Script Status | select | Draft · Needs edit · Approved · Filmed |
| Word Count | number | — |
| Content Item | relation → Content Calendar | link back to the calendar row |
| Drafted | date | — |

> The full filming-ready script goes in the **page body** (Notion markdown), not a property.

---

## Metrics & Trends
- Database ID: `1222f0d2-9238-48e9-942e-89187df05f33`
- Data source: `collection://bf551baa-ee8a-42b1-bc87-fafb6e6d11fb`

| Property | Type | Options |
|---|---|---|
| Entry | title | — |
| Type | select | Post metric · Trend signal |
| Platform | multi-select | Instagram · TikTok · YouTube · X · Facebook |
| Date Logged | date | — |
| Reach / Engagements / Saves / Shares / Link Clicks | number | — |
| Source | select | Metricool · socialtrendscrape · Manual |
| Verdict | select | Repeat · Iterate · Kill · Watch |
| Trend Note | text | — |
| Content Item | relation → Content Calendar | — |

---

## Competitors
- Database ID: `b37c11d7-4d5f-4496-bbb8-55c1645ae60d`
- Data source: `collection://c6037a3f-3d0e-4c9d-a605-77b6d10d71a0`

| Property | Type | Options |
|---|---|---|
| Competitor | title | — |
| Handle | text | — |
| Platform | multi-select | Instagram · TikTok · YouTube · X · Facebook |
| Followers | number | — |
| Niche Overlap | select | Direct · Adjacent · Aspirational |
| Tracking Status | select | Active · Watching · Dropped |
| What's Working | text | — |
| Profile Link | url | — |
| Last Reviewed | date | — |

---

## Weekly Brief  (shared strategy + report hub)
- Database ID: `8a9fd0e9-38dc-465c-aed0-28a059c1a2a8`
- Data source: `collection://388d91ff-f86a-45ab-8b5c-ae7bd91bda27`

| Property | Type | Options |
|---|---|---|
| Week Of | title | e.g. "Week of 23 Jun 2026" |
| Date Range | date | Mon–Sun |
| Status | select | Draft · Delivered |
| Top Performer | text | (Head of Content fills) |
| Kill List | text | (Head of Content fills) |
| Trends to Ride | text | (Strategist fills) |
| Next Week Focus | text | (Strategist fills — content mix + CTA + pillar focus) |
| Related Content | relation → Content Calendar | the 7 posts for the week |

> The Weekly Brief is the weekly handoff hub. The **Content Strategist** opens it (Status: Draft) with the strategy; the **Head of Content** completes and delivers it.
