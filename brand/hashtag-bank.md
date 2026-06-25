# CoachForge AI — Hashtag Bank

The source set every writing agent draws from when adding hashtags to a post.

## The honest bit (read first)
There is **no measured "best-performing hashtags" feed** in the Metricool MCP — no
tool returns a ranked hashtag leaderboard. So "top 5" does **not** mean "5 proven by
our own engagement data." It means **5 well-chosen tags**: brand + niche + one
trending/relevant pick. Do not present them as data-proven winners. As the Analyst
logs which posts performed, this bank gets refined over time (see "Refinement").

## The rule — 5 per post, per platform
Pick **exactly 5** hashtags per post, composed as:
1. **1 brand tag** — always `#coachforgeai`.
2. **2 niche tags** — from the niche set below, matched to the post's topic.
3. **1 pillar tag** — matched to the post's brand pillar.
4. **1 trending/relevant tag** — pulled fresh per post via `socialtrendscrape` for the
   coaching / AI-for-coaches niche, **only if** it genuinely fits the post and the brand
   voice (no guru/hype tags). If nothing fits, use a second niche tag instead — never
   pad with an off-brand trend.

Keep them lowercase, no spaces. UK spelling where it matters.

## Platform placement
- **Instagram:** put the 5 hashtags in the **first comment**, not the caption (cleaner caption, same reach). The carousel-builder/scripter supplies the first-comment text.
- **TikTok:** 3–5 in the caption is normal; keep to the 5.
- **X:** 1–2 max, inline, only if they read naturally. Over-tagging looks spammy on X — trim the 5 down.
- **Facebook:** 2–3 max; Facebook hashtags add little, so don't force all 5.
- **YouTube:** in the description; the 5 is fine, plus the channel's standing tags.

## Brand tag
- `#coachforgeai`

## Niche tags (pick 2, topic-matched)
Coaching business / online coaching:
- `#onlinecoach` · `#coachingbusiness` · `#fitnesscoach` · `#businesscoach` · `#lifecoach`
- `#coachingtips` · `#coachmarketing` · `#clientattraction` · `#scaleyourcoaching`

AI-for-coaches / workflow:
- `#aiforcoaches` · `#aiforbusiness` · `#contentsystems` · `#worksmarter`
- `#claudeai` · `#aiworkflow` · `#contentrepurposing` · `#solopreneur`

## Pillar tags (pick 1, by the post's pillar)
| Brand pillar | Tag |
|---|---|
| Built by a coach, for coaches | `#builtbyacoach` |
| Systems over hustle | `#systemsoverhustle` |
| AI as leverage, not replacement | `#aileverage` |
| Premium without pretence | `#coachingsystems` |
| Action over information | `#dontjustlearndo` |
| UK at heart, global in reach | `#ukcoaches` |

## Banned in tags (same spirit as the voice profile)
No `#hustle` · `#hustler` · `#passiveincome` · `#sixfigures` · `#grindset` ·
`#manifest` · `#gamechanger` · `#guru` — or any tag that promises overnight riches,
uses FOMO, or reads as guru/hype. If a trending tag is one of these, drop it.

## Refinement (how this gets smarter)
When the Data Analyst logs `Post metric` rows, note in the `Trend Note` which hashtags
the post carried if a post clearly over/under-performs. Over a few weeks, promote tags
that recur on `Repeat` posts and quietly retire tags that only appear on `Kill` posts.
This is directional learning from our own results — still not a precise leaderboard, and
never written up as one.
