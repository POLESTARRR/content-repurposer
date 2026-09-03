"""Thin wrapper around Google Gemini's free tier, the middle engine.

Same fail-soft contract as ollama_client: `is_available()` never raises,
`generate()` returns None on any failure so the caller falls back cleanly.
Kept signature-compatible with ollama_client.generate() so generator.py can
try one, then the other, without special-casing either.

Unlike Ollama, nothing here is local -- the source text and voice notes are
sent to Google's API. Only used when the key below is actually configured;
never on by default.
"""
from __future__ import annotations

import streamlit as st

TIMEOUT_GENERATE = 60

# Tried in order; a free-tier model can 503 under load, so falling through
# to the next one beats surfacing a transient error as "AI unavailable".
MODELS = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-3.1-flash-lite"]

_client = None
_client_checked = False


def _api_key() -> str | None:
    """Checks Streamlit secrets first (works locally via .streamlit/secrets.toml
    and identically once deployed, via Streamlit Community Cloud's own secrets
    manager), then falls back to a plain environment variable for anyone
    running this outside Streamlit's secrets mechanism entirely."""
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass  # no secrets.toml at all -- st.secrets can raise rather than return {}
    import os
    return os.environ.get("GEMINI_API_KEY") or None


def is_available() -> bool:
    return bool(_api_key())


def _get_client():
    global _client, _client_checked
    if _client_checked:
        return _client
    _client_checked = True
    key = _api_key()
    if not key:
        return None
    try:
        from google import genai
        _client = genai.Client(api_key=key)
    except Exception:
        _client = None
    return _client


def generate(prompt: str, model: str | None = None, temperature: float = 0.7, num_predict: int = 400) -> str | None:
    """Run one generation. Returns None on any failure so callers can fall back cleanly."""
    client = _get_client()
    if client is None:
        return None

    models = [model] if model else MODELS
    for m in models:
        try:
            response = client.models.generate_content(
                model=m,
                contents=prompt,
                # thinking_budget=0: these flash models reserve part of
                # max_output_tokens for internal reasoning by default, which
                # silently truncates short, format-sensitive outputs like
                # ours before the real answer even finishes. This is fast
                # templated writing, not a reasoning task -- turn it off so
                # the whole token budget goes to the actual response.
                config={
                    "temperature": temperature,
                    "max_output_tokens": num_predict,
                    "thinking_config": {"thinking_budget": 0},
                },
            )
            text = (getattr(response, "text", None) or "").strip()
            if text:
                return text
        except Exception:
            continue
    return None
