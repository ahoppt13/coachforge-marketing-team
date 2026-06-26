#!/usr/bin/env python3
"""
Carousel slide renderer (multi-brand).

Turns a JSON slide spec into on-brand PNG slides using headless Chrome.
No external Python deps required for rendering (Chrome does the work); Pillow
is used only for an optional post-render sanity check of dimensions.

The visual system is driven by a THEME. With no --theme flag the renderer uses
the built-in CoachForge AI theme (below), so existing CoachForge specs render
exactly as before. Pass --theme brands/<slug>/theme.json to render another
brand's look (colours, fonts, brandmark, card border) without touching code.

CoachForge default visual system (brand/brand-voice-profile.md §9):
  bg      Obsidian Navy  #070B14
  card    Deep Navy      #0B1628
  border  Navy Mid       #1A2F52
  accent  Molten Amber   #E8930C   (amber on dark ONLY, one tone per slide)
  text    Warm Ivory     #F2EDE4
  muted   Slate          #6B80A3
  display Cormorant Garamond 600  (brand moments / headlines)
  body    DM Sans 400/600         (everything functional)

Usage:
  python3 render.py --spec slides.json --out out [--size 1080x1350] [--theme theme.json]

Spec shape (slides.json):
{
  "handle": "@coachforge.ai",
  "slides": [
    {"type": "cover",   "eyebrow": "PROMPT SHORTCUTS", "headline": "Stop typing 'write me a caption'", "footer": "Swipe →"},
    {"type": "content", "kicker": "01", "headline": "Tell Claude who you are first", "body": ["Paste your offer + tone once.", "Save it as a Project."]},
    {"type": "cta",     "headline": "Run your business from your phone", "subtext": "Grab the AI Phone guide.", "cta": "Comment PHONE"}
  ]
}

Theme shape (theme.json) — every key optional; missing keys fall back to the
CoachForge default, so a minimal theme can override just the colours:
{
  "bg": "#070B14", "card": "#0B1628", "border": "#1A2F52",
  "accent": "#E8930C", "text": "#F2EDE4", "muted": "#6B80A3",
  "font_import": "@import url('https://fonts.googleapis.com/...');",
  "display": "'Cormorant Garamond', Georgia, serif",
  "body": "'DM Sans', -apple-system, Helvetica, Arial, sans-serif",
  "brandmark_html": "Coach<b>Forge</b> AI",   // <b> gets the accent colour
  "card_border": true,                          // draw the inset rounded frame
  "accent_shape": "square"                      // bullet/marker: "square" | "round"
}
"""
import argparse
import html
import json
import os
import subprocess
import sys
import tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Built-in CoachForge AI theme. Any key a custom theme omits falls back to here.
DEFAULT_THEME = {
    "bg": "#070B14",
    "card": "#0B1628",
    "border": "#1A2F52",
    "accent": "#E8930C",
    "accent_hover": "#F5A832",
    "text": "#F2EDE4",
    "muted": "#6B80A3",
    # Web fonts (fetched at render time; Chrome is online on this Mac).
    # Fallbacks keep a failed fetch legible rather than blank.
    "font_import": (
        "@import url('https://fonts.googleapis.com/css2?"
        "family=Cormorant+Garamond:wght@500;600;700&"
        "family=DM+Sans:wght@400;500;600;700&display=swap');"
    ),
    "display": "'Cormorant Garamond', Georgia, serif",
    "body": "'DM Sans', -apple-system, Helvetica, Arial, sans-serif",
    "brandmark_html": "Coach<b>Forge</b> AI",
    "card_border": True,
    "accent_shape": "square",  # "square" -> radius 3px marker; "round" -> pill/circle
}


def load_theme(path):
    """Merge a theme JSON file over DEFAULT_THEME. None/missing -> defaults."""
    theme = dict(DEFAULT_THEME)
    if path:
        with open(path) as f:
            custom = json.load(f)
        theme.update({k: v for k, v in custom.items() if v is not None})
    return theme


def esc(s):
    return html.escape(str(s), quote=True)


def base_css(w, h, t):
    marker_radius = "3px" if t.get("accent_shape") == "square" else "50%"
    chip_radius = "14px" if t.get("accent_shape") == "square" else "40px"
    return f"""
{t['font_import']}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; }}
body {{
  background:{t['bg']}; color:{t['text']}; font-family:{t['body']};
  width:{w}px; height:{h}px; overflow:hidden; position:relative;
  -webkit-font-smoothing:antialiased;
}}
.slide {{
  width:{w}px; height:{h}px; padding:96px 88px;
  display:flex; flex-direction:column; position:relative;
}}
.eyebrow {{
  font-family:{t['body']}; font-weight:600; font-size:26px; letter-spacing:0.22em;
  text-transform:uppercase; color:{t['accent']};
}}
.kicker {{
  font-family:{t['display']}; font-weight:600; font-size:120px; line-height:1;
  color:{t['accent']}; opacity:0.95;
}}
.headline {{
  font-family:{t['display']}; font-weight:600; color:{t['text']};
  font-size:92px; line-height:1.04; letter-spacing:-0.01em;
}}
.headline.big {{ font-size:104px; }}
.subtext {{ font-family:{t['body']}; font-weight:400; font-size:40px; line-height:1.4; color:{t['text']}; }}
.body-list {{ list-style:none; display:flex; flex-direction:column; gap:34px; }}
.body-list li {{
  font-family:{t['body']}; font-weight:400; font-size:42px; line-height:1.35; color:{t['text']};
  padding-left:46px; position:relative;
}}
.body-list li::before {{
  content:''; position:absolute; left:0; top:18px; width:20px; height:20px;
  background:{t['accent']}; border-radius:{marker_radius};
}}
.footer {{
  font-family:{t['body']}; font-weight:600; font-size:30px; color:{t['muted']};
  letter-spacing:0.04em;
}}
.handle {{ font-family:{t['body']}; font-weight:600; font-size:30px; color:{t['muted']}; }}
.brandmark {{
  font-family:{t['display']}; font-weight:600; font-size:34px; color:{t['text']};
}}
.brandmark b {{ color:{t['accent']}; font-weight:700; }}
.spacer {{ flex:1 1 auto; }}
.rule {{ width:120px; height:6px; background:{t['accent']}; border-radius:3px; }}
.cta-chip {{
  align-self:flex-start; font-family:{t['body']}; font-weight:700; font-size:38px;
  color:{t['bg']}; background:{t['accent']}; padding:22px 40px; border-radius:{chip_radius};
}}
.topbar {{ display:flex; justify-content:space-between; align-items:center; }}
.cardborder {{ position:absolute; inset:40px; border:2px solid {t['border']}; border-radius:28px; pointer-events:none; }}
"""


def render_cover(s, t):
    eyebrow = f'<div class="eyebrow">{esc(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    footer = f'<div class="footer">{esc(s["footer"])}</div>' if s.get("footer") else ""
    return f"""
<div class="topbar"><div class="brandmark">{t['brandmark_html']}</div></div>
<div class="spacer"></div>
{eyebrow}
<div style="height:28px"></div>
<div class="rule"></div>
<div style="height:36px"></div>
<div class="headline big">{esc(s["headline"])}</div>
<div class="spacer"></div>
{footer}
"""


def render_content(s, t):
    kicker = f'<div class="kicker">{esc(s["kicker"])}</div>' if s.get("kicker") else ""
    items = "".join(f"<li>{esc(b)}</li>" for b in s.get("body", []))
    body = f'<ul class="body-list">{items}</ul>' if items else ""
    return f"""
{kicker}
<div style="height:36px"></div>
<div class="headline">{esc(s["headline"])}</div>
<div style="height:48px"></div>
{body}
<div class="spacer"></div>
"""


def render_cta(s, t):
    sub = f'<div class="subtext">{esc(s["subtext"])}</div>' if s.get("subtext") else ""
    chip = f'<div style="height:40px"></div><div class="cta-chip">{esc(s["cta"])}</div>' if s.get("cta") else ""
    return f"""
<div class="spacer"></div>
<div class="rule"></div>
<div style="height:36px"></div>
<div class="headline">{esc(s["headline"])}</div>
<div style="height:28px"></div>
{sub}
{chip}
<div class="spacer"></div>
"""


RENDERERS = {"cover": render_cover, "content": render_content, "cta": render_cta}


def slide_html(slide, handle, w, h, t):
    inner = RENDERERS[slide["type"]](slide, t)
    handle_el = f'<div class="handle">{esc(handle)}</div>' if handle else ""
    foot = f'<div class="topbar" style="margin-top:auto">{handle_el}</div>' if handle else ""
    card = '<div class="cardborder"></div>' if t.get("card_border") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{base_css(w,h,t)}</style></head>
<body><div class="slide">{card}{inner}{foot}</div></body></html>"""


def shoot(html_str, out_png, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html_str)
        path = f.name
    try:
        cmd = [
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--no-sandbox", "--force-device-scale-factor=1",
            f"--window-size={w},{h}",
            "--default-background-color=00000000",
            f"--screenshot={out_png}", f"--virtual-time-budget=2500",
            f"file://{path}",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 and not os.path.exists(out_png):
            sys.stderr.write(r.stderr + "\n")
            raise SystemExit(f"Chrome failed to render {out_png}")
    finally:
        os.unlink(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", default="out")
    ap.add_argument("--size", default="1080x1350")
    ap.add_argument("--theme", default=None,
                    help="Path to a brand theme JSON. Omit for the CoachForge default theme.")
    args = ap.parse_args()

    w, h = (int(x) for x in args.size.lower().split("x"))
    with open(args.spec) as f:
        spec = json.load(f)
    handle = spec.get("handle", "")
    # A spec may name its own theme; an explicit --theme flag wins.
    theme = load_theme(args.theme or spec.get("theme"))
    os.makedirs(args.out, exist_ok=True)

    made = []
    for i, slide in enumerate(spec["slides"], 1):
        if slide["type"] not in RENDERERS:
            raise SystemExit(f"Unknown slide type: {slide['type']}")
        out_png = os.path.join(args.out, f"slide-{i:02d}.png")
        shoot(slide_html(slide, handle, w, h, theme), out_png, w, h)
        made.append(out_png)
        print(f"  rendered {out_png}")

    # Optional dimension sanity check
    try:
        from PIL import Image
        for p in made:
            with Image.open(p) as im:
                print(f"  {os.path.basename(p)}  {im.size[0]}x{im.size[1]}")
    except Exception:
        pass
    print(f"Done: {len(made)} slide(s) -> {args.out}/")


if __name__ == "__main__":
    main()
