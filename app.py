"""Recast turns one written piece into platform-native posts for X,
Instagram, Facebook, LinkedIn, YouTube, TikTok, and your newsletter.

No paid API. Uses a local Ollama model when available for richer writing,
and an instant zero setup template engine otherwise. Either way it costs
nothing to run and nothing leaves your machine unless you post it yourself.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

import theme
from engine import export, extract, gemini_client, generator, limits, ollama_client

ROOT = Path(__file__).resolve().parent
VOICE_PATH = ROOT / "voice.md"
SAMPLE_PATH = ROOT / "sample_input.md"

st.set_page_config(page_title="Recast", page_icon="\U0001F501", layout="wide")
st.html(theme.CSS)


def _load_voice() -> str:
    if VOICE_PATH.exists():
        return VOICE_PATH.read_text(encoding="utf-8")
    return ""


def _char_limit_for(platform: str, part: str = "body") -> dict:
    if platform == "youtube":
        key = "youtube_title" if part == "title" else "youtube_desc"
    elif platform == "newsletter":
        key = "newsletter_subject" if part == "title" else "newsletter_body"
    else:
        key = platform
    return limits.CHAR_LIMITS.get(key, {"ideal": 99999, "hard": 999999})


def _limit_caption(text: str, platform: str, part: str = "body") -> str:
    lim = _char_limit_for(platform, part)
    n = len(text)
    if n <= lim["ideal"]:
        tag = "within ideal range"
    elif n <= lim["hard"]:
        tag = "longer than ideal but still allowed"
    else:
        tag = "past this platform's limit"
    return f"{n} / {lim['hard']} chars ({tag})"


ollama_up = ollama_client.is_available()
model_name = ollama_client.default_model() if ollama_up else None
gemini_up = gemini_client.is_available()
ai_up = (ollama_up and model_name) or gemini_up

if ollama_up and model_name:
    engine_label = f"Local AI &middot; {model_name}"
    engine_label_plain = f"Local AI · {model_name}"
elif gemini_up:
    engine_label = "Gemini"
    engine_label_plain = "Gemini"
else:
    engine_label = "Template engine (instant)"
    engine_label_plain = "Template engine (instant)"

# ---------------------------------------------------------------- sidebar --
st.sidebar.markdown("**Recast**")
st.sidebar.caption("Free to run, always. No signup needed for the default setup.")

if ollama_up and model_name:
    st.sidebar.success(f"Local AI engine: **{model_name}** (via Ollama)")
elif ollama_up:
    st.sidebar.warning("Ollama is running but no model is pulled yet. Using the template engine.")
elif gemini_up:
    st.sidebar.success("AI engine: **Gemini** (free tier)")
else:
    st.sidebar.info("Template engine active. Instant, zero setup.")
    with st.sidebar.expander("Want richer AI written variants? (optional)"):
        st.markdown(
            "Two free options, pick either:\n\n"
            "**Local, offline** — install [Ollama](https://ollama.com). No signup, "
            "no API key, nothing sent over the internet.\n"
            "```bash\nbrew install ollama\nollama pull llama3.2:3b\n```\n\n"
            "**Cloud, free tier** — get a free key from "
            "[Google AI Studio](https://aistudio.google.com/apikey), then add it to "
            "`.streamlit/secrets.toml` as `GEMINI_API_KEY = \"...\"` (or as a secret "
            "in your Streamlit Cloud app settings, if deployed).\n\n"
            "Then reload this page."
        )

use_ai = st.sidebar.toggle("Use AI when available", value=True)

st.sidebar.divider()
st.sidebar.subheader("Your voice")
if "voice_text" not in st.session_state:
    st.session_state.voice_text = _load_voice()
with st.sidebar.expander("Edit voice.md", expanded=False):
    st.session_state.voice_text = st.text_area(
        "Voice notes", value=st.session_state.voice_text, height=240, label_visibility="collapsed"
    )
    if st.button("Save voice.md"):
        VOICE_PATH.write_text(st.session_state.voice_text, encoding="utf-8")
        st.success("Saved.")

st.sidebar.divider()
st.sidebar.subheader("Platforms")
selected_platforms = st.sidebar.multiselect(
    "Generate for:",
    options=limits.PLATFORMS,
    default=limits.PLATFORMS,
    format_func=lambda p: limits.DISPLAY_NAME[p],
)

with st.sidebar.expander("Best time to post (cheat sheet)"):
    for p in limits.PLATFORMS:
        st.markdown(f"**{limits.DISPLAY_NAME[p]}**: {limits.BEST_TIMES[p]}")

# ------------------------------------------------------------------ main --
st.html(theme.brand_row(ai_up, engine_label))

if "source_text" not in st.session_state:
    st.session_state.source_text = ""

with st.container(border=True):
    st.html(theme.eyebrow("From draft to every platform"))
    st.html(theme.headline("Stop rewriting the same post", "seven times."))
    st.html(
        theme.subhead(
            "Drop in one article and get platform native posts for X, Instagram, Facebook, "
            "LinkedIn, YouTube, TikTok, and your newsletter. Same voice, ready to publish."
        )
    )

    st.write("")
    input_mode = st.radio("Input", ["Upload a file", "Paste text"], horizontal=True, label_visibility="collapsed")

    if input_mode == "Upload a file":
        uploaded = st.file_uploader("Upload your written content", type=["txt", "md", "markdown", "pdf", "docx"])
        if uploaded is not None:
            raw = extract.extract_text(uploaded.name, uploaded.getvalue())
            st.session_state.source_text = extract.clean_text(raw)
    else:
        st.session_state.source_text = st.text_area(
            "Paste your content", value=st.session_state.source_text, height=200, label_visibility="collapsed"
        )

    word_count = len(st.session_state.source_text.split())
    if st.session_state.source_text:
        st.caption(f"{word_count} words loaded")

    bcol1, bcol2, bcol3 = st.columns([2, 2, 3])
    with bcol1:
        go = st.button("Repurpose content", type="primary", disabled=not st.session_state.source_text.strip())
    with bcol2:
        if st.button("Load sample"):
            if SAMPLE_PATH.exists():
                st.session_state.source_text = SAMPLE_PATH.read_text(encoding="utf-8")
                st.rerun()

    st.html(
        theme.trust_line(["No paid API", "Runs 100% locally", "Same voice everywhere"])
    )

if go:
    if not selected_platforms:
        st.error("Pick at least one platform in the sidebar.")
    else:
        with st.status(f"Writing {len(selected_platforms)} platforms...", expanded=True) as status:
            def _progress(platform, result):
                status.write(f"**{limits.DISPLAY_NAME[platform]}** done · {result.get('engine', '?')} engine")

            results = generator.run(
                selected_platforms,
                st.session_state.source_text,
                st.session_state.voice_text,
                use_ai=use_ai,
                on_progress=_progress,
            )
            lint_hits = generator.lint_against_voice(results, st.session_state.voice_text)
            saved_path = export.write_bundle(results)
            status.update(label="Done", state="complete")
        st.session_state.results = results
        st.session_state.lint_hits = lint_hits
        st.session_state.saved_path = str(saved_path)

if st.session_state.get("results"):
    results = st.session_state.results
    lint_hits = st.session_state.get("lint_hits", {})

    st.success(f"Saved to `{st.session_state.saved_path}`")
    if lint_hits:
        st.warning(
            "Voice-rule check flagged banned phrases in: "
            + ", ".join(f"{limits.DISPLAY_NAME[p]} ({', '.join(v)})" for p, v in lint_hits.items())
        )

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download all platforms (.zip)",
            data=export.build_zip(results),
            file_name="recast_bundle.zip",
            mime="application/zip",
        )
    with col2:
        st.download_button(
            "Download content calendar (.csv)",
            data=export.build_calendar_csv(results),
            file_name="content_calendar.csv",
            mime="text/csv",
        )

    tabs = st.tabs([limits.DISPLAY_NAME[p] for p in selected_platforms if p in results])
    for tab, platform in zip(tabs, [p for p in selected_platforms if p in results]):
        result = results[platform]
        with tab:
            with st.container(border=True):
                engine_used = result.get("engine", "?")
                st.caption(f"Engine: **{engine_used}** · Best time to post: {limits.BEST_TIMES[platform]}")

                if result.get("title"):
                    label = "Video title" if platform == "youtube" else "Subject line"
                    st.text_input(label, value=result["title"], key=f"title_{platform}")
                    st.caption(_limit_caption(result["title"], platform, "title"))

                st.markdown("**Hook options**")
                for hook, score in zip(result["hooks"], result.get("hook_scores", [])):
                    notes = " &middot; ".join(score.get("notes", []))
                    st.html(theme.hook_meter(score.get("score", 0), hook, notes))

                st.markdown("**Post**")
                edited = st.text_area(
                    "Post body", value=result["body"], height=220, key=f"body_{platform}", label_visibility="collapsed"
                )
                st.caption(_limit_caption(edited, platform, "body"))

                if result.get("hashtags"):
                    st.markdown("**Hashtags**")
                    st.html(theme.tag_chips(result["hashtags"]))

st.html(theme.footer(ai_up, engine_label))
