"""A quiet, monochrome graphite-on-paper theme for the app: one ink color,
one font (Inter), hierarchy from opacity and hairlines rather than color.
Selectors below were confirmed against the installed Streamlit build's
actual rendered DOM (see data-testid values), not guessed."""
from __future__ import annotations

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
<style>
:root {
  --paper: #fbfbfa;
  --ink: #1c1c1e;
  --platinum: #c7c7cc;
  --hairline: rgba(28,28,30,.10);
  --hairline-soft: rgba(28,28,30,.07);
  --divider: rgba(28,28,30,.12);
  --tick: rgba(28,28,30,.28);
}

html, body, [class*="css"], .stApp, .stMarkdown, .stMarkdown p, button, input, textarea, select {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp { background: var(--paper) !important; }
::selection { background: var(--ink); color: var(--paper); }

/* frosted sticky header */
[data-testid="stHeader"] {
  background: rgba(251,251,250,0.72) !important;
  backdrop-filter: saturate(140%) blur(10px);
  -webkit-backdrop-filter: saturate(140%) blur(10px);
  border-bottom: 1px solid var(--hairline-soft);
}

[data-testid="stMainBlockContainer"] { max-width: 860px; padding-top: 5.5rem; padding-bottom: 3rem; }

h1, h2, h3 { color: var(--ink) !important; letter-spacing: -0.03em; font-weight: 600 !important; }
p, li, label { color: rgba(28,28,30,.8); }
[data-testid="stCaptionContainer"] { color: rgba(28,28,30,.55) !important; }

/* every bordered container (st.container(border=True)) becomes a quiet
   hairline card with a soft long shadow and two corner registration ticks */
[data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"] {
  position: relative !important;
  border: 1px solid var(--hairline-soft) !important;
  border-radius: 20px !important;
  background: rgba(255,255,255,0.55);
  box-shadow: 0 1px 0 rgba(255,255,255,0.7) inset, 0 30px 60px -40px rgba(28,28,30,0.16);
  padding: 1.9rem 2.1rem !important;
  margin-bottom: 1.1rem;
}
[data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"]::before {
  content: ""; position: absolute; width: 13px; height: 13px; top: -7px; left: -7px;
  border-top: 1px solid var(--tick); border-left: 1px solid var(--tick); pointer-events: none;
}
[data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"]::after {
  content: ""; position: absolute; width: 13px; height: 13px; bottom: -7px; right: -7px;
  border-bottom: 1px solid var(--tick); border-right: 1px solid var(--tick); pointer-events: none;
}

/* buttons */
[data-testid="stBaseButton-primary"] {
  background: var(--ink) !important; color: var(--paper) !important;
  border: none !important; border-radius: 999px !important;
  padding: 0.6rem 1.5rem !important; font-weight: 500 !important;
  box-shadow: none !important; transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stBaseButton-primary"]:hover {
  transform: translateY(-1px); box-shadow: 0 10px 24px -10px rgba(28,28,30,0.45) !important;
}
[data-testid="stBaseButton-primary"] p { color: var(--paper) !important; }
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] {
  background: transparent !important; color: rgba(28,28,30,.82) !important;
  border: 1px solid var(--hairline) !important; border-radius: 999px !important;
  font-weight: 460 !important; padding: 0.6rem 1.5rem !important; box-shadow: none !important;
}
[data-testid="stBaseButton-secondary"]:hover {
  border-color: rgba(28,28,30,.32) !important; background: rgba(28,28,30,0.025) !important;
}

/* tabs -> quiet pill tabs */
[data-testid="stTabs"] [role="tablist"] { border-bottom: none !important; gap: .35rem; flex-wrap: wrap; }
[data-testid="stTab"] {
  border-radius: 999px !important; border: 1px solid var(--hairline) !important;
  padding: .3rem .95rem !important; color: rgba(28,28,30,.62) !important; font-weight: 460 !important;
}
[data-testid="stTab"][aria-selected="true"] {
  background: var(--ink) !important; color: var(--paper) !important; border-color: var(--ink) !important;
}
[data-testid="stTab"] p { font-size: .84rem !important; }

/* inputs */
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
  border-radius: 12px !important; border: 1px solid var(--hairline) !important; background: var(--paper) !important;
}
[data-testid="stFileUploaderDropzone"] {
  border-radius: 16px !important; border: 1px dashed var(--hairline) !important; background: rgba(28,28,30,0.015) !important;
}
/* multiselect tags: hairline chips instead of Streamlit's solid-fill default
   (which collides with our near-black primaryColor and goes text-on-text) */
[data-testid="stMultiSelectTagsContainer"] span[data-tag] {
  background: var(--paper) !important; border: 1px solid var(--hairline) !important; border-radius: 999px !important;
}
[data-testid="stMultiSelectTagsContainer"] span[data-tag] * { color: var(--ink) !important; fill: var(--ink) !important; }
[data-baseweb="radio"] label { color: rgba(28,28,30,.75) !important; }

/* sidebar */
[data-testid="stSidebar"] { background: #f3f3f1 !important; border-right: 1px solid var(--hairline-soft); }
[data-testid="stSidebar"] * { color: rgba(28,28,30,.85); }

/* --- custom decorative components (raw HTML) --- */
.eyebrow {
  display: inline-flex; align-items: center; gap: .5rem;
  border: 1px solid var(--hairline); border-radius: 999px;
  padding: .3rem .85rem; font-size: .7rem; font-weight: 500;
  text-transform: uppercase; letter-spacing: .14em;
  color: rgba(28,28,30,.7); background: var(--paper);
}
.eyebrow .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--ink); position: relative; }
.eyebrow .dot::after {
  content: ""; position: absolute; inset: -4px; border-radius: 50%;
  background: rgba(28,28,30,.14); animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { transform: scale(1); opacity: .7; } 50% { transform: scale(1.6); opacity: 0; } }

.brand-row {
  display: flex; align-items: center; justify-content: center; gap: .6rem;
  margin: .25rem 0 .25rem 0;
}
.brand-tile {
  width: 26px; height: 26px; border-radius: 8px; background: var(--ink);
  color: var(--paper); display: grid; place-items: center; font-size: 13px; font-weight: 700;
}
.brand-word { font-size: .95rem; font-weight: 600; letter-spacing: -0.02em; color: var(--ink); }

.hero-headline {
  font-size: 2.15rem; font-weight: 600; letter-spacing: -0.035em; line-height: 1.08;
  color: var(--ink); text-align: center; margin: 1.1rem 0 .7rem 0;
}
.hero-underline { position: relative; white-space: nowrap; }
.hero-underline::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: -3px; height: 1px;
  background: linear-gradient(to right, transparent, var(--platinum), transparent);
}
.hero-sub { max-width: 460px; margin: 0 auto; color: rgba(28,28,30,.7); font-size: .96rem; line-height: 1.55; text-align: center; }

.trust-line {
  display: flex; flex-wrap: wrap; justify-content: center; gap: 0 1.1rem; margin-top: 1.4rem;
  font-size: .76rem; color: rgba(28,28,30,.6); text-align: center;
}

.status-pill {
  display: inline-flex; align-items: center; gap: .45rem; font-size: .74rem; color: rgba(28,28,30,.68);
  border: 1px solid var(--hairline); border-radius: 999px; padding: .28rem .75rem; background: var(--paper);
}
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--ink); }
.status-dot.off { background: rgba(28,28,30,.28); }

.tag-chip {
  display: inline-block; border: 1px solid var(--hairline); border-radius: 999px;
  padding: .15rem .65rem; font-size: .78rem; color: rgba(28,28,30,.75);
  margin: .15rem .3rem .15rem 0; background: var(--paper);
}

.meter-row { margin-bottom: .65rem; }
.meter-track { flex: 1; height: 4px; background: var(--hairline); border-radius: 2px; overflow: hidden; }
.meter-fill { height: 100%; background: var(--ink); }
.meter-score { font-size: .74rem; color: rgba(28,28,30,.55); min-width: 2.6rem; text-align: right; }
.meter-hook { font-size: .89rem; color: var(--ink); margin-top: .32rem; }
.meter-notes { font-size: .74rem; color: rgba(28,28,30,.5); margin-top: .12rem; }

.footer-bar {
  margin-top: 2.5rem; background: var(--ink); color: rgba(251,251,250,.7);
  border-radius: 16px; padding: 1.35rem 1.6rem; text-align: center; font-size: .78rem;
}
.footer-bar .status-dot { background: var(--platinum); }
</style>
"""


def brand_row(status_active: bool, status_label: str) -> str:
    dot_cls = "status-dot" if status_active else "status-dot off"
    return f"""
    <div class="brand-row">
      <div class="brand-tile">&#9670;</div>
      <div class="brand-word">Recast</div>
    </div>
    <div style="text-align:center; margin-bottom:.5rem;">
      <span class="status-pill"><span class="{dot_cls}"></span>{status_label}</span>
    </div>
    """


def eyebrow(text: str) -> str:
    return f'<div style="text-align:center;"><span class="eyebrow"><span class="dot"></span>{text}</span></div>'


def headline(pre: str, underlined: str) -> str:
    return f'<div class="hero-headline">{pre} <span class="hero-underline">{underlined}</span></div>'


def subhead(text: str) -> str:
    return f'<div class="hero-sub">{text}</div>'


def trust_line(items: list[str]) -> str:
    inner = "<span>&middot;</span>".join(f"<span>{i}</span>" for i in items)
    return f'<div class="trust-line">{inner}</div>'


def hook_meter(score: int, hook: str, notes: str) -> str:
    score = max(0, min(100, score if isinstance(score, int) else 0))
    return f"""
    <div class="meter-row">
      <div style="display:flex; align-items:center; gap:.6rem;">
        <div class="meter-track"><div class="meter-fill" style="width:{score}%;"></div></div>
        <span class="meter-score">{score}/100</span>
      </div>
      <div class="meter-hook">{hook}</div>
      {f'<div class="meter-notes">{notes}</div>' if notes else ""}
    </div>
    """


def tag_chips(tags: list[str]) -> str:
    return "".join(f'<span class="tag-chip">{t}</span>' for t in tags)


def footer(status_active: bool, status_label: str) -> str:
    dot_cls = "status-dot" if status_active else "status-dot off"
    return f"""
    <div class="footer-bar">
      Recast generates every post on this machine. No data leaves your Mac.
      &nbsp;&nbsp;<span class="status-pill" style="background:transparent; border-color:rgba(251,251,250,.25); color:rgba(251,251,250,.7);">
        <span class="{dot_cls}"></span>{status_label}
      </span>
    </div>
    """
